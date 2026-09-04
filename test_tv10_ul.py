import urllib.request
import re

url = "https://tv10.egydead.live/the-runner-2026-1080p-web-dl/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
html = urllib.request.urlopen(req).read().decode('utf-8')

import json
# maybe the servers are inside some <script> JSON or specific divs?
for line in html.split('\n'):
    if 'iframe' in line.lower() or 'vidmoly' in line.lower() or 'mega' in line.lower():
        print(line.strip())
