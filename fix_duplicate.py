with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

content = content.replace('@android.webkit.JavascriptInterface\n                        @android.webkit.JavascriptInterface', '@android.webkit.JavascriptInterface')

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
    f.write(content)
