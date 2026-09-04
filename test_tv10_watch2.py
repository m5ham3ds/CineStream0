import urllib.request
import re

url = "https://tv10.egydead.live/the-runner-2026-1080p-web-dl/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
html = urllib.request.urlopen(req).read().decode('utf-8')

print("Elements with data-link:")
for m in re.finditer(r'<([a-zA-Z0-9]+)[^>]*?data-link="([^"]*)"[^>]*>(.*?)<\/\1>', html, re.IGNORECASE | re.DOTALL):
    print("MATCH:", m.group(1), m.group(2)[:50], m.group(3).strip())

