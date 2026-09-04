with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

content = content.replace('val lastUrl = webView.getTag() as? String', 'val lastUrl = webView.getTag(com.example.R.id.tag_url) as? String')
content = content.replace('webView.setTag(searchUrl)', 'webView.setTag(com.example.R.id.tag_url, searchUrl)')

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
    f.write(content)
