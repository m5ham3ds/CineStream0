import urllib.request
import re

url = "https://tv10.egydead.live/the-runner-2026-1080p-web-dl/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
html = urllib.request.urlopen(req).read().decode('utf-8')

m = re.search(r'(<div class="watchAreaMaster".*?</div>\s*</div>)', html, re.IGNORECASE | re.DOTALL)
if m:
    print(m.group(1)[:1000])
else:
    print("Not found")

m2 = re.search(r'(<ul class="serversList".*?</ul>)', html, re.IGNORECASE | re.DOTALL)
if m2:
    print("\n--- SERVERS LIST ---")
    print(m2.group(1))
else:
    print("serversList not found")
