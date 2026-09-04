import urllib.request
import re

url = "https://tv10.egydead.live/series/prison-break-%d9%85%d8%aa%d8%b1%d8%ac%d9%85/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
html = urllib.request.urlopen(req).read().decode('utf-8')

for link in re.finditer(r'<a[^>]*href=\"([^\"]+)\"[^>]*>([^<]*)</a>', html, re.IGNORECASE):
    href = link.group(1)
    if 'tv10.egydead' in href and 'prison-break' in href:
        print(link.group(0))

