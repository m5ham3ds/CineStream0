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
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import com.example.data.repository.ScraperRepository
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

@SuppressLint("SetJavaScriptEnabled")
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ServerSelectionDialog(
    title: String,
    isMovie: Boolean,
    season: Int = 1,
    episode: Int = 1,
    isAnime: Boolean = false,
    onDismiss: () -> Unit,
    onPlay: (url: String, serverName: String, website: String) -> Unit
) {
    val priorityAnimeSites = listOf("WitAnime", "Anime4up", "AnimeBlkom", "Animeat", "Arabanime", "Animerco", "AnimeLuxe", "Stardima", "Watch Stardima")
    val priorityMovieSites = listOf("EgyDead TV10", "QFilm", "TopCinema", "Laaroza", "Almeshkah", "ArabSeed Wine", "ArabSeed", "Egy Best", "CimaLight", "Brstej")
    val prioritySeriesSites = listOf("TopCinema", "EgyDead TV10", "Almeshkah", "Laaroza", "QFilm", "ArabSeed Wine", "ArabSeed", "Egy Best", "CimaLight", "Brstej")

    val prioritySites = if (isAnime) priorityAnimeSites else if (isMovie) priorityMovieSites else prioritySeriesSites

    var currentSiteIndex by remember { mutableStateOf(0) }
    var currentSiteName by remember { mutableStateOf(prioritySites[0]) }
    
    var isLoading by remember { mutableStateOf(true) }
    var loadingMessage by remember { mutableStateOf("جاري البحث...") }
    var isFailed by remember { mutableStateOf(false) }

    // Holds the URL to load in the WebView
    var watchUrlToLoad by remember { mutableStateOf<String?>(null) }
    var foundVideoUrl by remember { mutableStateOf(false) }

    // Move to next site
    val tryNextSite: () -> Unit = {
        if (currentSiteIndex < prioritySites.size - 1) {
            currentSiteIndex++
            currentSiteName = prioritySites[currentSiteIndex]
            watchUrlToLoad = null
            foundVideoUrl = false
        } else {
            isLoading = false
            isFailed = true
        }
    }

    LaunchedEffect(currentSiteIndex) {
        isLoading = true
        loadingMessage = "البحث في موقع $currentSiteName..."
        watchUrlToLoad = null
        foundVideoUrl = false

        // 1. Fast Jsoup search
        try {
            val url = ScraperRepository.getWatchUrl(currentSiteName, title, isMovie, season, episode)
            if (url != null) {
                loadingMessage = "جاري استخراج الفيديو من $currentSiteName..."
                watchUrlToLoad = url
            } else {
                tryNextSite()
            }
        } catch (e: Exception) {
            // If connection fails, move to next site safely
            tryNextSite()
        }
    }

    // 25 second timeout for WebView extraction
    LaunchedEffect(watchUrlToLoad) {
        if (watchUrlToLoad != null) {
            delay(25000)
            if (!foundVideoUrl) {
                tryNextSite()
            }
        }
    }

    if (watchUrlToLoad != null && !foundVideoUrl) {
        AndroidView(
            modifier = Modifier.size(1.dp).alpha(0.01f),
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
                    }
                    val cookieManager = CookieManager.getInstance()
                    cookieManager.setAcceptCookie(true)
                    cookieManager.setAcceptThirdPartyCookies(this, true)

                    webViewClient = object : WebViewClient() {
                        override fun onReceivedSslError(view: WebView?, handler: android.webkit.SslErrorHandler?, error: android.net.http.SslError?) {
                            handler?.proceed()
                        }
                        
                        override fun shouldInterceptRequest(view: WebView?, request: WebResourceRequest?): WebResourceResponse? {
                            val reqUrl = request?.url.toString()
                            if (!foundVideoUrl && (reqUrl.contains(".m3u8") || reqUrl.contains(".mp4") || reqUrl.contains(".mkv") || reqUrl.contains("videodelivery.net") || reqUrl.contains("v.mp4"))) {
                                if (!reqUrl.contains("adsystem") && !reqUrl.contains("tracker") && !reqUrl.contains("googleads") && !reqUrl.contains("facebook") && !reqUrl.contains("tiktok")) {
                                    foundVideoUrl = true
                                    Handler(Looper.getMainLooper()).post {
                                        onPlay(reqUrl, "Direct", currentSiteName)
                                    }
                                }
                            }
                            return super.shouldInterceptRequest(view, request)
                        }

                        override fun onPageFinished(view: WebView, url: String) {
                            super.onPageFinished(view, url)
                            val autoPlayScript = """
                                (function() {
                                    setInterval(function() {
                                        var cf = document.querySelector('.cf-turnstile-wrapper, #challenge-stage, input[type="checkbox"], #challenge-form, .mark-as-human');
                                        if (cf) { cf.click(); }
                                        try {
                                            var iframesCF = document.querySelectorAll('iframe');
                                            for (var i = 0; i < iframesCF.length; i++) {
                                                try {
                                                    var innerBtn = iframesCF[i].contentWindow.document.querySelector('input[type="checkbox"]');
                                                    if (innerBtn) innerBtn.click();
                                                } catch (err) {}
                                            }
                                        } catch(e) {}
                                        var iframes = document.getElementsByTagName('iframe');
                                        for (var i = 0; i < iframes.length; i++) {
                                            try {
                                                var playBtn = iframes[i].contentWindow.document.querySelector('.play-button, .jw-icon-display, video, .vjs-big-play-button, .fp-play');
                                                if (playBtn) playBtn.click();
                                            } catch(e) {}
                                        }
                                        var localPlay = document.querySelector('.play-button, .jw-icon-display, video, .vjs-big-play-button');
                                        if (localPlay) localPlay.click();
                                        
                                        var watchBtn = document.querySelector('.watch-btn, #watch-btn, a.watch, .btn-watch, .play-btn');
                                        if (watchBtn && !window.location.href.toLowerCase().includes('watch')) watchBtn.click();
                                        
                                        var serverList = document.querySelectorAll('ul.servers li, .server-list li, .serversList li, .watch-servers li, .list-servers li, .servers-list li, .mob-servers ul li, #servers li, .server_list li, .watch-btn, .DownloadServers li, ul#episode-servers li, ul.NavTabs li, .server-list a, .watch-servers a, .servers-container li, .btn-server, .servers a, .item-server, .server-item, .server-btn, .server-link, a.server-link, ul.donwload-servers-list li, .servers-container button');
                                        if (serverList && serverList.length > 0 && document.getElementsByTagName('iframe').length === 0 && document.querySelectorAll('video').length === 0) {
                                            serverList[0].click();
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
                val lastUrl = webView.getTag(com.example.R.id.tag_url) as? String
                if (lastUrl != watchUrlToLoad) {
                    webView.setTag(com.example.R.id.tag_url, watchUrlToLoad)
                    webView.loadUrl(watchUrlToLoad!!)
                }
            }
        )
    }

    Dialog(
        onDismissRequest = onDismiss,
        properties = DialogProperties(usePlatformDefaultWidth = false, dismissOnBackPress = true, dismissOnClickOutside = false)
    ) {
        Surface(
            modifier = Modifier.fillMaxWidth(0.9f).wrapContentHeight(),
            shape = MaterialTheme.shapes.large,
            color = MaterialTheme.colorScheme.surface
        ) {
            Column(
                modifier = Modifier.fillMaxWidth().padding(16.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = "جاري تحضير الفيديو",
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = FontWeight.Bold
                    )
                    IconButton(onClick = onDismiss) {
                        Icon(Icons.Default.Close, contentDescription = "إغلاق")
                    }
                }
                Spacer(modifier = Modifier.height(16.dp))
                if (isLoading) {
                    CircularProgressIndicator(color = MaterialTheme.colorScheme.primary)
                    Spacer(modifier = Modifier.height(16.dp))
                    Text(text = loadingMessage, color = MaterialTheme.colorScheme.onSurfaceVariant)
                } else if (isFailed) {
                    Text(
                        text = "عذراً، لم نتمكن من العثور على سيرفرات تعمل لهذا العمل في جميع المواقع المدعومة.",
                        color = MaterialTheme.colorScheme.error,
                        style = MaterialTheme.typography.bodyLarge
                    )
                }
            }
        }
    }
}
