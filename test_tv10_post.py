import urllib.request
import urllib.parse
import re

url = "https://tv10.egydead.live/the-runner-2026-1080p-web-dl/"
data = urllib.parse.urlencode({'View': '1'}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
html = urllib.request.urlopen(req).read().decode('utf-8')

m = re.search(r'(<ul class="serversList".*?</ul>)', html, re.IGNORECASE | re.DOTALL)
if m:
    print("Found serversList!")
    print(m.group(1)[:500])
else:
    print("serversList still not found")
