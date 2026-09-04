import urllib.request
import re

url = "https://tv10.egydead.live/series/prison-break-%d9%85%d8%aa%d8%b1%d8%ac%d9%85/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
html = urllib.request.urlopen(req).read().decode('utf-8')

title = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
if title: print("Title:", title.group(1))

# Let's find any div or block with class season or episode
m = re.findall(r'<div[^>]*class=\"[^\"]*(?:season|episode)[^\"]*\"[^>]*>.*?</div>', html, re.IGNORECASE | re.DOTALL)
print(f"Found {len(m)} season/episode divs")
if m: print(m[0][:500])

