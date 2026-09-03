import re

with open('app/src/main/java/com/example/data/repository/ScraperRepository.kt', 'r') as f:
    content = f.read()

# Replace Jsoup.connect(...) with Jsoup.connect(...).userAgent("Mozilla/5.0 ...").header(...)
replacement = r"""Jsoup.connect(\1).userAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36").header("Accept-Language", "ar,en-US;q=0.9,en;q=0.8").header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8").referrer("https://google.com/")"""

content = re.sub(r'Jsoup\.connect\((.*?)\)', replacement, content)

with open('app/src/main/java/com/example/data/repository/ScraperRepository.kt', 'w') as f:
    f.write(content)

