with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

replacement = """
                        private var lastFailedSiteIndex = -1

                        @android.webkit.JavascriptInterface
                        fun sendFailed() {
                            Handler(Looper.getMainLooper()).post {
                                if (lastFailedSiteIndex != currentSiteIndex) {
                                    lastFailedSiteIndex = currentSiteIndex
                                    currentSiteIndex++
                                }
                            }
                        }"""

content = content.replace("""
                        @android.webkit.JavascriptInterface
                        fun sendFailed() {
                            Handler(Looper.getMainLooper()).post {
                                currentSiteIndex++
                            }
                        }""", replacement)

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
    f.write(content)
