package com.example.ui.screens.player

import android.annotation.SuppressLint
import android.os.Handler
import android.os.Looper
import android.webkit.CookieManager
import android.webkit.WebResourceRequest
import android.webkit.WebResourceResponse
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.compose.foundation.layout.size
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView

@SuppressLint("SetJavaScriptEnabled")
@Composable
fun HiddenVideoExtractor(
    url: String,
    isMovie: Boolean = true,
    season: Int = 1,
    episode: Int = 1,
    targetServer: String? = null,
    onVideoUrlFound: (String) -> Unit,
    onServersFound: ((List<String>) -> Unit)? = null
) {
    AndroidView(
        modifier = Modifier.size(1.dp).alpha(0f), // Completely invisible but active in layout
        factory = { ctx ->
            WebView(ctx).apply {
                setLayerType(android.view.View.LAYER_TYPE_SOFTWARE, null)
                settings.apply {
                    javaScriptEnabled = true
                    domStorageEnabled = true
                    databaseEnabled = true
                    javaScriptCanOpenWindowsAutomatically = true
                    userAgentString = WebSettings.getDefaultUserAgent(ctx)
                    mixedContentMode = WebSettings.MIXED_CONTENT_ALWAYS_ALLOW
                    cacheMode = WebSettings.LOAD_DEFAULT
                    // This is critical: force media to auto-play so we can catch the network request
                    mediaPlaybackRequiresUserGesture = false 
                }

                val cookieManager = CookieManager.getInstance()
                cookieManager.setAcceptCookie(true)
                cookieManager.setAcceptThirdPartyCookies(this, true)

                addJavascriptInterface(object {
                    @android.webkit.JavascriptInterface
                    fun sendServers(serversStr: String) {
                        val servers = serversStr.split(",").filter { it.isNotBlank() }
                        if (servers.isNotEmpty()) {
                            Handler(Looper.getMainLooper()).post {
                                onServersFound?.invoke(servers)
                            }
                        }
                    }
                }, "AndroidBridge")

                webViewClient = object : WebViewClient() {
                    var found = false

                    override fun onReceivedSslError(view: WebView?, handler: android.webkit.SslErrorHandler?, error: android.net.http.SslError?) {
                        handler?.proceed()
                    }

                    override fun onPageStarted(view: WebView?, url: String?, favicon: android.graphics.Bitmap?) {
                        found = false
                        super.onPageStarted(view, url, favicon)
                    }

                    override fun shouldInterceptRequest(
                        view: WebView?,
                        request: WebResourceRequest?
                    ): WebResourceResponse? {
                        val reqUrl = request?.url.toString()
                        
                        // Look for standard streaming formats
                        if (!found && (reqUrl.contains(".m3u8") || reqUrl.contains(".mp4"))) {
                            // Avoid common ad scripts that might have these strings
                            if (!reqUrl.contains("adsystem") && !reqUrl.contains("tracker") && !reqUrl.contains("googleads")) {
                                found = true
                                Handler(Looper.getMainLooper()).post {
                                    onVideoUrlFound(reqUrl)
                                }
                            }
                        }
                        
                        return super.shouldInterceptRequest(view, request)
                    }

                    override fun onPageFinished(view: WebView, url: String) {
                        super.onPageFinished(view, url)
                        // Inject script to automatically click play buttons to force stream load
                        val autoPlayScript = """
                            (function() {
                                var isMovie = ${isMovie};
                                var epNum = ${episode};
                                var targetServer = "${targetServer ?: ""}";
                                var loc = window.location.href.toLowerCase();
                                
                                // 1. Auto-Play Players & Cloudflare Bypass
                                setInterval(function() {
                                    // Bypass Cloudflare Turnstile / Captcha
                                    var cf = document.querySelector('.cf-turnstile-wrapper, #challenge-stage, input[type="checkbox"], #challenge-form, .mark-as-human');
                                    if (cf) { cf.click(); }
                                    try {
                                        var iframesCF = document.querySelectorAll('iframe');
                                        for (var i = 0; i < iframesCF.length; i++) {
                                            var innerBtn = iframesCF[i].contentWindow.document.querySelector('input[type="checkbox"]');
                                            if (innerBtn) innerBtn.click();
                                        }
                                    } catch(e) {}

                                    var iframes = document.getElementsByTagName('iframe');
                                    for (var i = 0; i < iframes.length; i++) {
                                        try {
                                            var playBtn = iframes[i].contentWindow.document.querySelector('.play-button, .jw-icon-display, video, .vjs-big-play-button');
                                            if (playBtn) playBtn.click();
                                        } catch(e) {}
                                    }
                                    var localPlay = document.querySelector('.play-button, .jw-icon-display, video, .vjs-big-play-button');
                                    if (localPlay) localPlay.click();
                                    
                                    // Some sites need us to click a watch button first
                                    var watchBtn = document.querySelector('.watch-btn, #watch-btn, a.watch, .btn-watch, .play-btn');
                                    if(watchBtn && !loc.includes('watch')) watchBtn.click();
                                    
                                    // Some sites use servers list to load iframe
                                    var serverList = document.querySelectorAll('ul.servers li, .server-list li, .serversList li, .watch-servers li, .list-servers li, .servers-list li, .mob-servers ul li');
                                    var clickedTarget = false;
                                    if (serverList && serverList.length > 0) {
                                        if (targetServer !== "") {
                                            for(var i=0; i<serverList.length; i++) {
                                                if(serverList[i].innerText.trim() === targetServer) {
                                                    serverList[i].click();
                                                    clickedTarget = true;
                                                    break;
                                                }
                                            }
                                        }
                                        if (!clickedTarget && document.getElementsByTagName('iframe').length === 0) {
                                            serverList[0].click();
                                        }
                                    }
                                    
                                    // Send servers back to Kotlin
                                    if (serverList && serverList.length > 0 && typeof AndroidBridge !== 'undefined') {
                                        var serverNames = [];
                                        for(var i=0; i<serverList.length; i++) {
                                            serverNames.push(serverList[i].innerText.trim());
                                        }
                                        AndroidBridge.sendServers(serverNames.join(','));
                                    }
                                    
                                }, 1500);
                            })();
                        """.trimIndent()
                        view.evaluateJavascript(autoPlayScript, null)
                    }
                }
            }
        },
        update = { webView ->
            // Use getTag to store the original loaded url to avoid reloading when webView.url changes due to internal navigation
            val lastUrl = webView.getTag(com.example.R.id.tag_url) as? String
            val lastServer = webView.getTag(com.example.R.id.tag_server) as? String

            if (lastUrl != url) {
                webView.setTag(com.example.R.id.tag_url, url)
                webView.setTag(android.R.id.text2, targetServer)
                webView.loadUrl(url)
            } else if (lastServer != targetServer) {
                webView.setTag(android.R.id.text2, targetServer)
                webView.reload() // Server changed, reload the page
            }
        }
    )
}
