import urllib.request
import re

url = "https://tv10.egydead.live/the-runner-2026-1080p-web-dl/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    for line in html.split('\n'):
        if 'servers' in line.lower() or 'server' in line.lower() or 'watch' in line.lower():
            print(line.strip()[:100])
except Exception as e:
    print(f"Error: {e}")
