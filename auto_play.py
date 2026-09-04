import re

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

old_send = """                        @android.webkit.JavascriptInterface
                        fun sendServers(serversStr: String, url: String) {
                            val servers = serversStr.split(",").filter { it.isNotBlank() }.distinct()
                            if (servers.isNotEmpty() && extractedServers.isEmpty()) {
                                Handler(Looper.getMainLooper()).post {
                                    finalWatchUrl = url
                                    extractedServers = servers
                                    isLoading = false
                                }
                            }
                        }"""

new_send = """                        @android.webkit.JavascriptInterface
                        fun sendServers(serversStr: String, url: String) {
                            val servers = serversStr.split(",").filter { it.isNotBlank() }.distinct()
                            if (servers.isNotEmpty() && extractedServers.isEmpty()) {
                                Handler(Looper.getMainLooper()).post {
                                    finalWatchUrl = url
                                    extractedServers = servers
                                    isLoading = false
                                    // Auto-play the first server immediately!
                                    onPlay(url, servers.first(), currentSiteName)
                                }
                            }
                        }"""

if old_send in content:
    content = content.replace(old_send, new_send)
    with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
        f.write(content)
    print("Patched auto-play")
else:
    print("Could not find old_send")
