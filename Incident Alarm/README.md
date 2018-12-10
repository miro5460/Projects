# README file for Lab 6: The Incident Alarm

# Michael Robinson
# 7/18/18

1. This tool is a detection tool that alerts the user to stealthy scans performed on the specified network interface, or in individual pcap files. It is also capable of detecting usernames and passwords sent in the clear in these files or on the network.
2. This incident alarm works by listening/sniffing on a specified interface or reading a pcap file. Once it has these packets, it looks to see if the packet was sent by TCP. If it was, it checks the flags that were attached to the packet and if they were part of a FIN/XMAS or no flags were attached at all (NULL) reports accordingly. The program then checks the port being scanned is HTTP or FTP (ports 80 and 21 respectively) and looks to see if any username and password info is being sent in-the-clear and returns it.
3. All aspects of this lab have been correctly implemented. I discussed nmap testing as well as how to identify plaintext passwords in http/ftp with Jay Facultad. I have spent approximately 5hrs on this assignment.
4. The heuristics used in this assignment are satisfactory, but could be altered to provide a more nuanced analysis of what is occuring in/on a particular file/interface. Currently, there is an overabundance of information provided by the alarm. A simple nmap NULL/FIN/XMAS scan causes many hundreds of alert messages to be returned. This isn't very practical from a "real world" usability perspective because a user won't have an easy time sifting through this large quantity of alerts to understand what is going on, or if there is a more specific, veiled threat. That being said, for it is useful and effetive in detecting stealth scans and information sent in-the-clear.
5. Given more time, I would want to pare down or reconfigure how many alerts are sent out for scans. I also think it would be interesting to add functionality to the alarm in order to detect other types of scans. For example, it a flag for SYN and ACK could be added as well as the destination IP, which would give a more fleshed-out picture of who is talking to who. I would also be interested in adding functionality to caputure data on FTP-DATA, which would give this alarm the ability to see files sent in-the-clear.

Cited sources:
1. TCP Codes Reference: https://stackoverflow.com/questions/20429674/get-tcp-flags-with-scapy
2. Correcting padding on a string for base 64 decoding:  https://stackoverflow.com/questions/2941995/python-ignore-incorrect-padding-error-when-base64-decoding (specifically 3rd answer down)
3. Processing HTTP Header for 'Authorization: Basic' section: https://medium.com/!ismailakkila/black-hat-python-parsing-http-payloads-with-scapy-d937d01af9b1