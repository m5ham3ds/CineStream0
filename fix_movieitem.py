import re

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

old_search = "li.movieItem a,"
new_search = "li.movieItem a, .movieItem a, .postBlock a, "

if old_search in content:
    content = content.replace(old_search, new_search)
    with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
        f.write(content)
    print("Fixed movieItem search selector")
else:
    print("Old search string not found")

