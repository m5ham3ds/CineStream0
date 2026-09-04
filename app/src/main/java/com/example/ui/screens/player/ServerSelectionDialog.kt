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
    
    val animeSites = listOf("tv10.egydead.live", "witanime.cyou", "anime4up.cam", "animeat.net", "vip.animeluxe.org", "det.animerco.org", "stardima.com", "watch.stardima.com")
    val movieSites = listOf("tv10.egydead.live", "egydead.plus", "arabseed.show", "qfilm.tv", "cima4u.skin", "faselhd.wtf", "a.qfilm.tv", "arabseed.wine", "egybests.live")
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
    val searchUrl = when {
        currentSiteName.contains("egydead") -> "https://$currentSiteName/page/1/?s=$encodedTitle"
        currentSiteName.contains("qfilm") -> "https://$currentSiteName/search.php?keywords=$encodedTitle"
        currentSiteName.contains("arabseed") -> "https://$currentSiteName/page/1/?s=$encodedTitle"
        currentSiteName.contains("stardima") -> "https://$currentSiteName/search?query=$encodedTitle&page=1"
        currentSiteName.contains("witanime") -> "https://$currentSiteName/?search_param=animes&s=$encodedTitle"
        currentSiteName.contains("anime4up") -> "https://$currentSiteName/?search_param=animes&s=$encodedTitle"
        currentSiteName.contains("cima4u") -> "https://$currentSiteName/search.php?keywords=$encodedTitle"
        currentSiteName.contains("faselhd") -> "https://$currentSiteName/?s=$encodedTitle"
        currentSiteName == "animeat.net" -> "https://animeat.net/?search=$encodedTitle"
        currentSiteName == "det.animerco.org" -> "https://det.animerco.org/?s=$encodedTitle&page=1"
        currentSiteName == "e.cimalight.co" -> "https://e.cimalight.co/search.php?keywords=$encodedTitle"
        currentSiteName == "egybests.live" -> "https://egybests.live/?s=$encodedTitle&page=1"
        currentSiteName == "uo.brstej.com" -> "https://uo.brstej.com/search.php?keywords=$encodedTitle"
        currentSiteName == "vip.animeluxe.org" -> "https://vip.animeluxe.org/anime?s=$encodedTitle&page=1"
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
                        private var lastFailedSiteIndex = -1

                        @android.webkit.JavascriptInterface
                        fun sendFailed() {
                            Handler(Looper.getMainLooper()).post {
                                if (lastFailedSiteIndex != currentSiteIndex) {
                                    lastFailedSiteIndex = currentSiteIndex
                                    currentSiteIndex++
                                }
                            }
                        }

                        @android.webkit.JavascriptInterface
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
                        }
                    }, "AndroidBridge")

                    webViewClient = object : WebViewClient() {
                        override fun onReceivedSslError(view: WebView?, handler: android.webkit.SslErrorHandler?, error: android.net.http.SslError?) {
                            handler?.proceed()
                        }

                        override fun onPageFinished(view: WebView, url: String) {
                            super.onPageFinished(view, url)
                            
                            val isMovieStr = if (isMovie) "true" else "false"
                            val autoPlayScript = """
                                (function() {
                                    var isMovie = $isMovieStr;
                                    var season = $season;
                                    var epNum = $episode;
                                    var loc = window.location.href.toLowerCase();
                                    
                                    var intervalId = setInterval(function() {
                                        // Bypass Cloudflare
                                        var cf = document.querySelector('.cf-turnstile-wrapper, #challenge-stage, input[type="checkbox"], #challenge-form, .mark-as-human');
                                        if (cf) { cf.click(); return; }
                                        
                                        var isJustAMoment = document.title.includes('Just a moment') || document.title.includes('Cloudflare') || document.title.includes('Attention Required');
                                        var isCloudflare = cf || isJustAMoment;

                                        // 1. Search Results -> Click item
                                        if (loc.includes('?s=') || loc.includes('search') || loc.includes('query=')) {
                                            var result = document.querySelector('a.postBlock, section.main-section ul.posts-list li.movieItem a, .movieItem a, .postBlock a,  ul.pm-ul-browse-videos li a, ul.movie__blocks__ul li a.movie__block, ul.series__ul li a, div.media-block a.image, div.owl-animes a.overlay, div.embla__slide a, .movie-card a, .anime-card a, .item-list a, article a, .post a, .thumb a, .Blocks-Area a.Block-Item, .ep-card a, .episode-card a, .box-item a, .hover-content a, .anime-list-content a, .half-post a, .Block-Item, a.header-featured-item, a.movie-item__link, .pm-video-thumb a, .lucodeia-slider-slide-item, a.overlay, a.absolute.inset-0');
                                            if (result) { 
                                                clearInterval(intervalId);
                                                window.location.href = result.href; 
                                                return; 
                                            }
                                        }
                                        
                                        // 2. Series Page -> Click Season/Episode
                                        var serverList = document.querySelectorAll('ul.servers li, .server-list li, .serversList li, .watch-servers li, .list-servers li, .servers-list li, .mob-servers ul li, #servers li, .server_list li, .watch-btn, .DownloadServers li, ul#episode-servers li, ul.NavTabs li, .server-list a, .watch-servers a, .servers-container li, .btn-server, .servers a, .item-server, .server-item, .server-btn, .server-link, a.server-link, ul.donwload-servers-list li, .servers-container button');
                                        var hasServers = serverList && serverList.length > 0;
                                        
                                        // Click play buttons to reveal iframe if hidden
                                        var playBtn = document.querySelector('.play-button, .jw-icon-display, video, .vjs-big-play-button, .play-icon, #play-video, .btn-play');
                                        if (playBtn) playBtn.click();
                                        
                                        var iframes = document.querySelectorAll('iframe');
                                        var hasIframe = false;
                                        for(var i=0; i<iframes.length; i++) {
                                            if(iframes[i].src && !iframes[i].src.includes('cloudflare') && !iframes[i].src.includes('facebook') && !iframes[i].src.includes('twitter')) {
                                                hasIframe = true; break;
                                            }
                                        }

                                        var videoTags = document.querySelectorAll('video');
                                        var hasVideo = videoTags.length > 0;

                                        if (!isMovie && !hasServers && !hasIframe && !hasVideo) {
                                            var epLinks = document.querySelectorAll('.episodes__list li a, .EpsList li a, .episodes-list li a, .all-episodes-list li a, .SeasonsEpisodes a, .episodelist a, .episodes a, .ListEp a, ul.episodes li a, .ep-card a, .episode-card a, .List-Episodes a, .list-episodes a, .EpisodesList a, .eplist a, .episode-list a');
                                            if (epLinks.length > 0) {
                                                clearInterval(intervalId);
                                                var targetEp = null;
                                                for(var i=0; i<epLinks.length; i++) {
                                                    var text = epLinks[i].innerText || "";
                                                    if(text.trim() === epNum.toString() || text.includes(" " + epNum.toString() + " ") || text.includes("حلقة " + epNum) || text.includes("الحلقة " + epNum)) {
                                                        targetEp = epLinks[i];
                                                        break;
                                                    }
                                                }
                                                if(targetEp) {
                                                    window.location.href = targetEp.href;
                                                } else {
                                                    for(var i=0; i<epLinks.length; i++) {
                                                        if((epLinks[i].innerText || "").includes(epNum.toString())) {
                                                            targetEp = epLinks[i]; break;
                                                        }
                                                    }
                                                    window.location.href = targetEp ? targetEp.href : epLinks[0].href;
                                                }
                                                return;
                                            }
                                        }
                                        
                                        // 3. Extract Servers on Watch Page
                                        if (hasServers || hasIframe || hasVideo) {
                                            var serverNames = [];
                                            if (hasServers) {
                                                for(var i=0; i<serverList.length; i++) {
                                                    var serverName = serverList[i].innerText.trim();
                                                    if (serverName) {
                                                        var sName = serverName.replace(/1080p|720p|480p|360p|240p|1080|720|480|360|240/gi, '').trim();
                                                        if (sName === "" || sName.includes('جودة') || sName.includes('FHD') || sName.includes('HD') || sName.includes('SD')) {
                                                            sName = "سيرفر " + (i+1);
                                                        }
                                                        serverNames.push(sName);
                                                    }
                                                }
                                            }
                                            if (serverNames.length === 0 && (hasIframe || hasVideo)) {
                                                serverNames.push("السيرفر الرئيسي");
                                            }
                                            
                                            if (serverNames.length > 0) {
                                                // Make unique
                                                var uniqueServers = [...new Set(serverNames)];
                                                clearInterval(intervalId);
                                                if (typeof AndroidBridge !== 'undefined') {
                                                    AndroidBridge.sendServers(uniqueServers.join(','), window.location.href);
                                                }
                                                return;
                                            }
                                        }
                                        
                                        // 4. Fast Fail (if no search results or servers found after loading)
                                        if (!isCloudflare && document.readyState === 'complete') {
                                            window._failCount = (window._failCount || 0) + 1;
                                            if (window._failCount >= 6) {
                                                clearInterval(intervalId);
                                                if (typeof AndroidBridge !== 'undefined') AndroidBridge.sendFailed();
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
                val lastUrl = webView.getTag(com.example.R.id.tag_url) as? String
                if (lastUrl != searchUrl) {
                    webView.setTag(com.example.R.id.tag_url, searchUrl)
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
                        text = "اختر السيرفر",
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
                        text = "تم جلب السيرفرات من: $currentSiteName",
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
