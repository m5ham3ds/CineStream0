import re

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

old_search = "a.overlay');"
new_search = "a.overlay, a.absolute.inset-0');"

if old_search in content:
    content = content.replace(old_search, new_search)
    with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
        f.write(content)
    print("Added stardima search selector")
else:
    print("Old search string not found")

