package com.example.ui.screens.player

import android.annotation.SuppressLint
import android.os.Handler
import android.os.Looper
import android.webkit.CookieManager
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
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
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import java.net.URLEncoder

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
    val coroutineScope = rememberCoroutineScope()
    
    val animeSites = listOf("witanime.you", "animeat.net", "vip.animeluxe.org", "det.animerco.org", "stardima.com", "watch.stardima.com")
    val movieSites = listOf("tv10.egydead.live", "a.qfilm.tv", "arabseed.wine", "arabseed-tv.com", "egybests.live", "e.cimalight.co", "uo.brstej.com")
    val prioritySites = if (isAnime) animeSites else movieSites

    var currentSiteIndex by remember { mutableStateOf(0) }
    var currentSiteName by remember { mutableStateOf(prioritySites[0]) }
    
    var isLoading by remember { mutableStateOf(true) }
    var loadingMessage by remember { mutableStateOf("جاري الفحص وتخطي الحماية...") }
    
    var extractedServers by remember { mutableStateOf<List<String>>(emptyList()) }
    var finalWatchUrl by remember { mutableStateOf<String?>(null) }
    var isFailed by remember { mutableStateOf(false) }

    LaunchedEffect(currentSiteIndex) {
        if (currentSiteIndex >= prioritySites.size) {
            isLoading = false
            isFailed = true
            return@LaunchedEffect
        }
        
        currentSiteName = prioritySites[currentSiteIndex]
        loadingMessage = "جاري الفحص في موقع $currentSiteName..."
        extractedServers = emptyList()
        finalWatchUrl = null
        
        // 25 seconds timeout per site to account for Cloudflare
        delay(25000)
        if (extractedServers.isEmpty()) {
            currentSiteIndex++
        }
    }

    val encodedTitle = URLEncoder.encode(title, "UTF-8")
    val searchUrl = when (currentSiteName) {
        "tv10.egydead.live" -> "https://tv10.egydead.live/page/1/?s=$encodedTitle"
        "a.qfilm.tv" -> "https://a.qfilm.tv/search.php?keywords=$encodedTitle"
        "animeat.net" -> "https://animeat.net/?search=$encodedTitle"
        "arabseed-tv.com" -> "https://arabseed-tv.com/page/1/?s=$encodedTitle"
        "arabseed.wine" -> "https://www.arabseed.wine/page/1/?s=$encodedTitle"
        "det.animerco.org" -> "https://det.animerco.org/?s=$encodedTitle&page=1"
        "e.cimalight.co" -> "https://e.cimalight.co/search.php?keywords=$encodedTitle"
        "egybests.live" -> "https://egybests.live/?s=$encodedTitle&page=1"
        "stardima.com" -> "https://www.stardima.com/search?query=$encodedTitle&page=1"
        "uo.brstej.com" -> "https://uo.brstej.com/search.php?keywords=$encodedTitle"
        "vip.animeluxe.org" -> "https://vip.animeluxe.org/anime?s=$encodedTitle&page=1"
        "watch.stardima.com" -> "https://watch.stardima.com/watch/search_gcse-2/?s=$encodedTitle&page=1"
        "witanime.you" -> "https://witanime.com/?search_param=animes&s=$encodedTitle"
        else -> "https://$currentSiteName/?s=$encodedTitle"
    }

    if (isLoading && !isFailed) {
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
                    
                    addJavascriptInterface(object {
                        @android.webkit.JavascriptInterface
                        fun sendServers(serversStr: String, url: String) {
                            val servers = serversStr.split(",").filter { it.isNotBlank() }.distinct()
                            if (servers.isNotEmpty() && extractedServers.isEmpty()) {
                                Handler(Looper.getMainLooper()).post {
                                    finalWatchUrl = url
                                    extractedServers = servers
                                    isLoading = false
                                }
                            }
                        }
                    }, "AndroidBridge")

                    webViewClient = object : WebViewClient() {
                        override fun onPageFinished(view: WebView, url: String) {
                            super.onPageFinished(view, url)
                            
                            val isMovieStr = if (isMovie) "true" else "false"
                            val autoPlayScript = """
                                (function() {
                                    var isMovie = $isMovieStr;
                                    var season = $season;
                                    var epNum = $episode;
                                    var loc = window.location.href.toLowerCase();
                                    
                                    setInterval(function() {
                                        // Bypass Cloudflare
                                        var cf = document.querySelector('.cf-turnstile-wrapper, #challenge-stage, input[type="checkbox"], #challenge-form, .mark-as-human');
                                        if (cf) { cf.click(); }
                                        
                                        // 1. Search Results -> Click item
                                        if (loc.includes('?s=') || loc.includes('search')) {
                                            var result = document.querySelector('a.postBlock, section.main-section ul.posts-list li.movieItem a, ul.pm-ul-browse-videos li a, ul.movie__blocks__ul li a.movie__block, ul.series__ul li a, div.media-block a.image, div.owl-animes a.overlay, div.embla__slide a');
                                            if (result) { window.location.href = result.href; return; }
                                        }
                                        
                                        // 2. Series Page -> Click Season/Episode
                                        if (!isMovie && !loc.includes('episode') && !loc.includes('ep-') && !loc.includes('watch')) {
                                            var epLinks = document.querySelectorAll('.episodes__list li a, .EpsList li a, .episodes-list li a, .all-episodes-list li a, .SeasonsEpisodes a');
                                            if (epLinks.length > 0) {
                                                for(var i=0; i<epLinks.length; i++) {
                                                    var text = epLinks[i].innerText || "";
                                                    if(text.includes(epNum.toString())) {
                                                        window.location.href = epLinks[i].href;
                                                        return;
                                                    }
                                                }
                                                // Fallback to first episode
                                                window.location.href = epLinks[0].href;
                                                return;
                                            }
                                        }
                                        
                                        // 3. Extract Servers on Watch Page
                                        var serverList = document.querySelectorAll('ul.servers li, .server-list li, .serversList li, .watch-servers li, .list-servers li, .servers-list li, .mob-servers ul li');
                                        if (serverList && serverList.length > 0) {
                                            var serverNames = [];
                                            for(var i=0; i<serverList.length; i++) {
                                                serverNames.push(serverList[i].innerText.trim());
                                            }
                                            if (typeof AndroidBridge !== 'undefined') {
                                                AndroidBridge.sendServers(serverNames.join(','), window.location.href);
                                            }
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
                val lastUrl = webView.getTag(android.R.id.text1) as? String
                if (lastUrl != searchUrl) {
                    webView.setTag(android.R.id.text1, searchUrl)
                    webView.loadUrl(searchUrl)
                }
            }
        )
    }

    Dialog(
        onDismissRequest = onDismiss,
        properties = DialogProperties(usePlatformDefaultWidth = false)
    ) {
        Surface(
            modifier = Modifier
                .fillMaxWidth(0.9f)
                .wrapContentHeight(),
            shape = MaterialTheme.shapes.large,
            color = MaterialTheme.colorScheme.surface
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = "اختر السيرفر أو الجودة",
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
                } else if (extractedServers.isNotEmpty()) {
                    Text(
                        text = "تم جلب الجودات من: $currentSiteName",
                        color = MaterialTheme.colorScheme.primary,
                        style = MaterialTheme.typography.labelLarge,
                        modifier = Modifier.padding(bottom = 8.dp)
                    )
                    
                    LazyColumn(
                        modifier = Modifier.fillMaxWidth(),
                        verticalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        items(extractedServers) { server ->
                            Card(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .clickable {
                                        onPlay(finalWatchUrl ?: searchUrl, server, currentSiteName)
                                    },
                                colors = CardDefaults.cardColors(
                                    containerColor = MaterialTheme.colorScheme.surfaceVariant
                                )
                            ) {
                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(16.dp),
                                    verticalAlignment = Alignment.CenterVertically,
                                    horizontalArrangement = Arrangement.Center
                                ) {
                                    Text(
                                        text = server,
                                        style = MaterialTheme.typography.titleMedium,
                                        fontWeight = FontWeight.Bold
                                    )
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
