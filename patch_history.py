import re

with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'r') as f:
    content = f.read()

# Fix movie history
content = re.sub(r'progress\s*=\s*0f,\s*duration\s*=\s*1L', '', content)
# It could leave trailing commas. Let's do a cleaner regex or direct string replace

content = content.replace('isMovie = true,\n                                        progress = 0f,\n                                        duration = 1L', 'isMovie = true')
content = content.replace('isMovie = false, progress = 0f, duration = 1L', 'isMovie = false')

with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'w') as f:
    f.write(content)

