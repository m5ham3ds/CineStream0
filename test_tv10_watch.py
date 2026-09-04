import urllib.request
import re
from bs4 import BeautifulSoup

url = "https://tv10.egydead.live/the-runner-2026-1080p-web-dl/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
html = urllib.request.urlopen(req).read().decode('utf-8')

soup = BeautifulSoup(html, 'html.parser')
ul_tags = soup.find_all('ul')
for ul in ul_tags:
    if ul.get('class'):
        print("UL Class:", ul.get('class'))
        if 'servers' in ' '.join(ul.get('class')).lower():
            for li in ul.find_all('li'):
                print(" -", li.text.strip(), li.get('data-link', ''))

print("\n--- Any elements with data-link ---")
for el in soup.find_all(attrs={'data-link': True}):
    print(el.name, el.get('class', []), el.get('data-link'))
