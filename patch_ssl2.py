with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'r') as f:
    content = f.read()

replacement = """                webViewClient = object : WebViewClient() {
                    var found = false

                    override fun onReceivedSslError(view: WebView?, handler: android.webkit.SslErrorHandler?, error: android.net.http.SslError?) {
                        handler?.proceed()
                    }

                    override fun onPageStarted(view: WebView?, url: String?, favicon: android.graphics.Bitmap?) {"""

content = content.replace("""                webViewClient = object : WebViewClient() {
                    var found = false

                    override fun onPageStarted(view: WebView?, url: String?, favicon: android.graphics.Bitmap?) {""", replacement)

with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'w') as f:
    f.write(content)
