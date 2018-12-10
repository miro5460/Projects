#!/usr/bin/python

from scapy.all import *
import pcapy
import argparse
import socket
import re
import base64

TOTAL_ALERTS = 0 # keeps track of number of alerts, global
FIN = 0x01
SYN = 0x02
RST = 0x04
PSH = 0x08
ACK = 0x10
URG = 0x20
ECE = 0x40
CWR = 0x80


def main():
  parser = argparse.ArgumentParser(description='A network sniffer that identifies basic vulnerabilities')
  parser.add_argument('-i', dest='interface', help='Network interface to sniff on', default='eth0')
  parser.add_argument('-r', dest='pcapfile', help='A PCAP file to read')
  args = parser.parse_args()

  if args.pcapfile:
    try:
      print "Reading PCAP file %(filename)s..." % {"filename" : args.pcapfile}
      sniff(offline=args.pcapfile, prn=packetcallback)
      #getFlag(args.pcapfile)
    except:
      print "Sorry, something went wrong reading PCAP file %(filename)s!" % {"filename" : args.pcapfile}
  else:
    print "Sniffing on %(interface)s... " % {"interface" : args.interface}
    try:
      sniff(iface=args.interface, prn=packetcallback)
      #getFlag(args.interface)
    except pcapy.PcapError:
      print "Sorry, error opening network interface %(interface)s. It does not exist." % {"interface" : args.interface}
    except:
      print "Sorry, can\'t read network traffic. Are you root?"

def scanPacket(aPacket):
  if TCP in aPacket:
    ipAddr = aPacket[IP].src
    typeOfScan(aPacket, ipAddr)

def typeOfScan(packet, ipAddr):
  global TOTAL_ALERTS
  
  packetFlag = packet[TCP].flags
  packetPort = packet[TCP].sport
  
  if (packetFlag & FIN) and not (packetFlag & SYN) and not (packetFlag & RST) and not (packetFlag & PSH) and not (packetFlag & ACK) and not (packetFlag & URG) and not (packetFlag & ECE) and not (packetFlag & CWR):
    TOTAL_ALERTS += 1
    print 'Alert #' + str(TOTAL_ALERTS) + ': ' + 'FIN scan detected from ' + str(ipAddr) + ' (port: ' + str(packetPort) + ')!'

  elif (packetFlag & FIN) and not (packetFlag & SYN) and not (packetFlag & RST) and (packetFlag & PSH) and not (packetFlag & ACK) and (packetFlag & URG) and not (packetFlag & ECE) and not (packetFlag & CWR):
    TOTAL_ALERTS += 1
    print 'Alert #' + str(TOTAL_ALERTS) + ': ' + 'XMAS scan detected from ' + str(ipAddr) + ' (port: ' + str(packetPort) + ')!'

  elif not (packetFlag & FIN) and not (packetFlag & SYN) and not (packetFlag & RST) and not (packetFlag & PSH) and not (packetFlag & ACK) and not (packetFlag & URG) and not (packetFlag & ECE) and not (packetFlag & CWR): #packetFlag == 0:
    TOTAL_ALERTS += 1
    print 'Alert #' + str(TOTAL_ALERTS) + ': ' + 'NULL scan detected from ' + str(ipAddr) + ' (port: ' + str(packetPort) + ')!'

def httpHeadCheck(httpHeader, ipAddr):
  global TOTAL_ALERTS
  httpHeader_Parsed = httpHeader.find('Authorization: Basic')
  if httpHeader_Parsed != -1:
    httpHeader_String = str(httpHeader)
    find_Auth = dict(re.findall(r"(?P<USER>.*?): (?P<PASS>.*?)\r\n", httpHeader_String))
    if "Authorization" in find_Auth.keys():
      TOTAL_ALERTS += 1
      toDecode = find_Auth['Authorization']
      toDecode = toDecode.rsplit(" ", 1)
      newDecode = toDecode[1].replace("=", "")
      newDecode += "=" * ((4 - len(newDecode) % 4) % 4)
      isDecoded = base64.b64decode(newDecode)
      print 'Alert #' + str(TOTAL_ALERTS) + ': Usernames and passwords sent in-the-clear (HTTP) from ' + ipAddr + ' (' + isDecoded + ')'

def ftpCheck(tcpPayload, ipAddr):
  global TOTAL_ALERTS
  if "USER" in tcpPayload :
    TOTAL_ALERTS += 1
    aUser = tcpPayload
    print 'Alert #' + str(TOTAL_ALERTS) + ': Username sent in-the-clear (FTP) from ' + ipAddr + ' (' + aUser.rstrip() + ')'
  elif "PASS" in tcpPayload:
    TOTAL_ALERTS += 1
    aPass = tcpPayload
    print 'Alert #' + str(TOTAL_ALERTS) + ': Password sent in-the-clear (FTP) from ' + ipAddr + ' (' + aPass.rstrip() + ')'
  
    
def packetcallback(aPacket):
  scanPacket(aPacket)
  if TCP in aPacket:
    ipAddr = aPacket[IP].src
  try:
    if aPacket[TCP].dport == 80:
      #print "HTTP (web) traffic detected!"
      tcpPayload = bytes(aPacket[TCP].payload) 
      httpHeader = tcpPayload[tcpPayload.index(b"HTTP/1.1"):tcpPayload.index(b"\r\n\r\n")+2]
      httpHeadCheck(httpHeader, ipAddr)

    if aPacket[TCP].dport == 21:
      #print "FTP traffic detected!"
      tcpPayload = str(aPacket[TCP].payload)
      ftpCheck(tcpPayload, ipAddr)
  
  except:
    pass

if __name__== "__main__":
  main()

