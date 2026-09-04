with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

replacement = """                    webViewClient = object : WebViewClient() {
                        override fun onReceivedSslError(view: WebView?, handler: android.webkit.SslErrorHandler?, error: android.net.http.SslError?) {
                            handler?.proceed()
                        }

                        override fun onPageFinished(view: WebView, url: String) {"""

content = content.replace('                    webViewClient = object : WebViewClient() {\n                        override fun onPageFinished(view: WebView, url: String) {', replacement)

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
    f.write(content)
