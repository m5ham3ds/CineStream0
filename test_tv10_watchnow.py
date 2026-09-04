import urllib.request
import re

url = "https://tv10.egydead.live/the-runner-2026-1080p-web-dl/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
html = urllib.request.urlopen(req).read().decode('utf-8')

m = re.search(r'(<div class="watchNow".*?</div>)', html, re.IGNORECASE | re.DOTALL)
if m:
    print(m.group(1)[:1000])
else:
    print("Not found")

