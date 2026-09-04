with open('app/src/main/java/com/example/ui/components/BackgroundWebView.kt', 'r') as f:
    content = f.read()

replacement = """                    webViewClient = object : WebViewClient() {
                        private var timeoutHandler = Handler(Looper.getMainLooper())
                        private var checkRunnable: Runnable? = null
                        private var isBypassed = false

                        override fun onReceivedSslError(view: WebView?, handler: android.webkit.SslErrorHandler?, error: android.net.http.SslError?) {
                            handler?.proceed()
                        }

                        override fun onPageFinished(view: WebView, url: String) {"""

content = content.replace("""                    webViewClient = object : WebViewClient() {
                        private var timeoutHandler = Handler(Looper.getMainLooper())
                        private var checkRunnable: Runnable? = null
                        private var isBypassed = false

                        override fun onPageFinished(view: WebView, url: String) {""", replacement)

with open('app/src/main/java/com/example/ui/components/BackgroundWebView.kt', 'w') as f:
    f.write(content)
