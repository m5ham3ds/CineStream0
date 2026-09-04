import re

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

# Let's inspect the JavaScript
js_start = content.find("val autoPlayScript =")
js_end = content.find("}, \"AndroidBridge\")", js_start)

if js_start != -1 and js_end != -1:
    print(content[js_start:js_end])
else:
    print("JS not found")
