with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'r') as f:
    content = f.read()

content = content.replace('val lastUrl = webView.getTag() as? String', 'val lastUrl = webView.getTag(com.example.R.id.tag_url) as? String')
content = content.replace('val lastServer = webView.getTag(android.R.id.text2) as? String', 'val lastServer = webView.getTag(com.example.R.id.tag_server) as? String')
content = content.replace('webView.setTag(url)', 'webView.setTag(com.example.R.id.tag_url, url)')
content = content.replace('webView.setTag(android.R.id.text2, serverName)', 'webView.setTag(com.example.R.id.tag_server, serverName)')

with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'w') as f:
    f.write(content)
