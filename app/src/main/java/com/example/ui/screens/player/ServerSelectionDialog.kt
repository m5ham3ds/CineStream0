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
    val prioritySeriesSites = listOf("TopCinema", "EgyDead TV10", "Egy Best", "ArabSeed Wine", "Almeshkah", "Laaroza", "QFilm", "ArabSeed", "CimaLight", "Brstej")

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
        var directUrl: String? = null
        try {
            directUrl = ScraperRepository.getWatchUrl(currentSiteName, title, isMovie, season, episode)
        } catch (e: Exception) {
            // Ignore error, fallback below
        }

        if (directUrl != null) {
            loadingMessage = "جاري استخراج الفيديو من $currentSiteName..."
            watchUrlToLoad = directUrl
        } else {
            // Fallback: If Jsoup fails (due to Cloudflare or layout changes), construct the search URL
            // and let the WebView bypass Cloudflare and click through results
            loadingMessage = "جاري البحث المتقدم في $currentSiteName..."
            val encodedTitle = java.net.URLEncoder.encode(title, "UTF-8")
            val domain = when (currentSiteName) {
                "WitAnime" -> "witanime.you"
                "Anime4up" -> "w1.anime4up.rest"
                "AnimeBlkom" -> "animeblkom.net"
                "Animeat" -> "animeat.net"
                "Arabanime" -> "arabanime.net"
                "Animerco" -> "det.animerco.org"
                "AnimeLuxe" -> "vip.animeluxe.org"
                "Stardima" -> "stardima.com"
                "Watch Stardima" -> "watch.stardima.com"
                "EgyDead TV10" -> "tv10.egydead.live"
                "QFilm" -> "a.qfilm.tv"
                "TopCinema" -> "topcinema.io"
                "Laaroza" -> "laaroza.space"
                "Almeshkah" -> "z1.almeshkah.net"
                "ArabSeed Wine" -> "arabseed.wine"
                "ArabSeed" -> "arabseed-tv.com"
                "Egy Best" -> "egybests.live"
                "CimaLight" -> "e.cimalight.co"
                "Brstej" -> "uo.brstej.com"
                else -> currentSiteName
            }
            
            watchUrlToLoad = when {
                domain.contains("egydead") -> "https://$domain/page/1/?s=$encodedTitle"
                domain.contains("qfilm") -> "https://$domain/search.php?keywords=$encodedTitle"
                domain.contains("arabseed") -> "https://$domain/page/1/?s=$encodedTitle"
                domain.contains("stardima") -> "https://$domain/search?query=$encodedTitle&page=1"
                domain.contains("witanime") -> "https://$domain/?search_param=animes&s=$encodedTitle"
                domain.contains("anime4up") -> "https://$domain/?s=$encodedTitle"
                domain.contains("cima4u") -> "https://$domain/search.php?keywords=$encodedTitle"
                domain.contains("faselhd") -> "https://$domain/?s=$encodedTitle"
                domain == "animeat.net" -> "https://animeat.net/?search=$encodedTitle"
                domain == "det.animerco.org" -> "https://det.animerco.org/?s=$encodedTitle&page=1"
                domain == "e.cimalight.co" -> "https://e.cimalight.co/search.php?keywords=$encodedTitle"
                domain == "egybests.live" -> "https://egybests.live/?s=$encodedTitle&page=1"
                domain == "uo.brstej.com" -> "https://uo.brstej.com/search.php?keywords=$encodedTitle"
                domain == "vip.animeluxe.org" -> "https://vip.animeluxe.org/anime?s=$encodedTitle&page=1"
                domain == "topcinema.io" -> "https://$domain/search/?query=$encodedTitle&page=1"
                domain == "laaroza.space" -> "https://$domain/search.php?page=1&keywords=$encodedTitle"
                domain == "z1.almeshkah.net" -> "https://$domain/search.php?page=1&keywords=$encodedTitle"
                else -> "https://$domain/?s=$encodedTitle"
            }
        }
    }

    // 45 second timeout for WebView extraction
    LaunchedEffect(watchUrlToLoad) {
        if (watchUrlToLoad != null) {
            delay(45000)
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
                                        
                                        // 1. Search Results Click
                                        var isSearchPage = window.location.href.includes('?s=') || window.location.href.includes('&s=') || window.location.href.includes('search') || window.location.href.includes('?query=') || window.location.href.includes('/page/');
                                        var searchResults = document.querySelectorAll('.pm-ul-browse-videos li a, .movieItem a, .anime-card-poster a, .box-5x1 a, article.item a, a.group\\/card, div.as-episode a, a.postBlock, div.embla__slide a, div.poster a, div.Small--Box a, div.anime-card-container a');
                                        if (isSearchPage && searchResults && searchResults.length > 0 && !window.location.href.toLowerCase().includes('watch') && !window.location.href.toLowerCase().includes('episode')) {
                                            if (window.location.href.split('#')[0].replace(/\\/$/, '') !== searchResults[0].href.split('#')[0].replace(/\\/$/, '')) {
                                                searchResults[0].click();
                                                return;
                                            }
                                        }

                                        var hasVideoOrServers = document.getElementsByTagName('iframe').length > 0 || document.querySelectorAll('video').length > 0 || document.querySelectorAll('ul.servers li, .server-list li, .serversList li, .watch-servers li, .list-servers li, .servers-list li, .mob-servers ul li, #servers li, .server_list li, .watch-btn, .DownloadServers li, ul#episode-servers li, ul.NavTabs li, .server-list a, .watch-servers a, .servers-container li, .btn-server, .servers a, .item-server, .server-item, .server-btn, .server-link, a.server-link, ul.donwload-servers-list li, .servers-container button, ul.servers__list li, div.embeding ul li, ul#watch-servers-list li, button.watchButton, div.servers span.server a, div.watch--servers--list li.server--item, ul.WatchServers li, ul.list_servers li').length > 0;

                                        // 2. Episodes Click
                                        if (${!isMovie} && !hasVideoOrServers && (window.location.href.toLowerCase().includes('series') || window.location.href.toLowerCase().includes('anime') || window.location.href.toLowerCase().includes('show') || document.querySelectorAll('.EpsList, .episodes-list, .SeasonsEpisodes, .all-episodes-list, .episodes-card-container, #eps, .episodes__list, .episodes__blocks__holder, .tabcontent, .row, .all-episodes, .EpisodesList, #episodes-list-container, .episodes-lists, .episodes-links, .episodes-card-title').length > 0)) {
                                            var epLinks = document.querySelectorAll('.EpsList a, .episodes-list a, .SeasonsEpisodes a, .all-episodes-list a, .episodes-card-container a, div#eps a.list-group-item, ul.episodes__list li a, ul.episodes__blocks__holder a, div.SeasonsEpisodesMain div.tabcontent a, div.row a, div.all-episodes a, div.EpisodesList a, ul#episodes-list-container a, ul.episodes-lists a, ul.episodes-links a, div.episodes-card-title a');
                                            if (epLinks && epLinks.length > 0) {
                                                var targetEp = Array.from(epLinks).find(l => l.innerText.includes('${episode}') || l.href.includes('${episode}'));
                                                var epToClick = targetEp ? targetEp : epLinks[0];
                                                // Prevent loop if already on the episode page
                                                if (epToClick && epToClick.href && epToClick.href.includes('javascript:void(0)')) {
                                                    epToClick.click();
                                                    return;
                                                } else if (epToClick && window.location.href.split('#')[0].replace(/\\/$/, '') !== epToClick.href.split('#')[0].replace(/\\/$/, '')) {
                                                    epToClick.click();
                                                    return;
                                                }
                                            }
                                        }

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
                                        
                                        var serverList = document.querySelectorAll('ul.servers li, .server-list li, .serversList li, .watch-servers li, .list-servers li, .servers-list li, .mob-servers ul li, #servers li, .server_list li, .watch-btn, .DownloadServers li, ul#episode-servers li, ul.NavTabs li, .server-list a, .watch-servers a, .servers-container li, .btn-server, .servers a, .item-server, .server-item, .server-btn, .server-link, a.server-link, ul.donwload-servers-list li, .servers-container button, ul.servers__list li, div.embeding ul li, ul#watch-servers-list li, button.watchButton, div.servers span.server a, div.watch--servers--list li.server--item, ul.WatchServers li, ul.list_servers li');
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
