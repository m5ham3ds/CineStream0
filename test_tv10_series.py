import urllib.request
import re

url = "https://tv10.egydead.live/series/prison-break-%d9%85%d8%aa%d8%b1%d8%ac%d9%85/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
html = urllib.request.urlopen(req).read().decode('utf-8')

m = re.search(r'(<ul[^>]*episode[^>]*>.*?</ul>|<div[^>]*episode[^>]*>.*?</div>)', html, re.IGNORECASE | re.DOTALL)
if m:
    print("Found episodes container!")
    print(m.group(1)[:1000])
else:
    print("episodes container not found")
    
# Let's just find any links that have "episode" or "حلقة" in them
for link in re.finditer(r'<a[^>]*href=\"([^\"]+)\"[^>]*>([^<]*)</a>', html, re.IGNORECASE):
    if 'episode' in link.group(1) or 'حلقة' in link.group(2) or 'حلقه' in link.group(2):
        print(link.group(0))

