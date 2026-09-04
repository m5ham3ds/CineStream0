import urllib.request
from html.parser import HTMLParser

url = "https://tv10.egydead.live/the-runner-2026-1080p-web-dl/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    # Print a small window around 'serversList'
    import re
    m = re.search(r'serversList.*', html, re.IGNORECASE | re.DOTALL)
    if m:
        print(m.group(0)[:500])
    else:
        print("Not found")
except Exception as e:
    print(f"Error: {e}")
