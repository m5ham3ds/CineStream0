with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'r') as f:
    content = f.read()

content = content.replace('val lastUrl = webView.getTag(android.R.id.text1) as? String', 'val lastUrl = webView.getTag() as? String')
content = content.replace('webView.setTag(android.R.id.text1, url)', 'webView.setTag(url)')

with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'w') as f:
    f.write(content)
