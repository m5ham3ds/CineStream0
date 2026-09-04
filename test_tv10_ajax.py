import urllib.request
import re

url = "https://tv10.egydead.live/the-runner-2026-1080p-web-dl/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
html = urllib.request.urlopen(req).read().decode('utf-8')

for line in html.split('\n'):
    if 'ajax' in line.lower() or '.php' in line.lower():
        print(line.strip())
