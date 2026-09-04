package com.example.ui.screens.player

import android.annotation.SuppressLint
import android.os.Handler
import android.os.Looper
import android.webkit.*
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.viewinterop.AndroidView
import com.example.data.repository.ScraperRepository
import com.example.utils.SiteVerificationManager
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

@OptIn(ExperimentalMaterial3Api::class)
@SuppressLint("SetJavaScriptEnabled")
@Composable
fun ServerSelectionDialog(
    title: String,
    isMovie: Boolean,
    season: Int = 1,
    episode: Int = 1,
    isAnime: Boolean = false,
    onDismiss: () -> Unit,
    onPlay: (String, String, String) -> Unit
) {
    val scope = rememberCoroutineScope()
    var currentSiteName by remember { mutableStateOf("جاري اختيار الموقع...") }
    var currentStatus by remember { mutableStateOf("جاري التحضير...") }
    var extractedUrl by remember { mutableStateOf<String?>(null) }
    var currentWebsite by remember { mutableStateOf("") }
    var isVerifyingSite by remember { mutableStateOf(false) }

    val animeSites = listOf("WitAnime", "Anime4up", "AnimeBlkom", "Animeat", "Arabanime", "AnimeLuxe")
    val movieSites = listOf("EgyDead TV10", "QFilm", "TopCinema", "Laaroza", "Almeshkah", "ArabSeed", "ArabSeed Wine", "CimaLight", "Egy Best", "Stardima", "Brstej")
    val seriesSites = listOf("TopCinema", "EgyDead TV10", "Egy Best", "ArabSeed Wine", "Laaroza", "Almeshkah", "QFilm", "ArabSeed", "CimaLight", "Stardima", "Brstej")

    val siteList = when {
        isAnime -> animeSites
        isMovie -> movieSites
        else -> seriesSites
    }

    var siteIndex by remember { mutableStateOf(0) }
    var watchUrlToExtract by remember { mutableStateOf<String?>(null) }

    fun processNextSite() {
        if (siteIndex < siteList.size) {
            currentWebsite = siteList[siteIndex]
            currentSiteName = currentWebsite
            val baseUrl = ScraperRepository.getBaseUrl(currentWebsite)
            
            if (!SiteVerificationManager.verifiedSites.contains(baseUrl) && baseUrl.isNotEmpty()) {
                currentStatus = "فحص الموقع والتأكد من عدم وجود حماية (Cloudflare)..."
                isVerifyingSite = true
                return
            }
            
            isVerifyingSite = false
            currentStatus = "جاري البحث عن العمل في: $currentWebsite"
            
            scope.launch {
                val url = withContext(Dispatchers.IO) {
                    ScraperRepository.getWatchUrl(currentWebsite, title, isMovie, season, episode)
                }
                if (url != null) {
                    currentStatus = "تم العثور على العمل! جاري استخراج السيرفرات..."
                    watchUrlToExtract = url
                } else {
                    siteIndex++
                    processNextSite()
                }
            }
        } else {
            currentStatus = "لم يتم العثور على روابط. جرب في وقت لاحق."
            isVerifyingSite = false
        }
    }

    LaunchedEffect(Unit) {
        processNextSite()
    }

    // Timeout for extraction
    LaunchedEffect(watchUrlToExtract) {
        if (watchUrlToExtract != null) {
            kotlinx.coroutines.delay(15000) // 15 seconds to extract video
            if (extractedUrl == null) {
                // Timeout, try next site
                watchUrlToExtract = null
                siteIndex++
                processNextSite()
            }
        }
    }

    ModalBottomSheet(
        onDismissRequest = onDismiss,
        containerColor = Color(0xFF1C1C1E),
        shape = RoundedCornerShape(topStart = 24.dp, topEnd = 24.dp)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = "البحث عن السيرفرات",
                color = Color.White,
                fontSize = 20.sp,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(16.dp))
            CircularProgressIndicator(color = Color(0xFFE50914))
            Spacer(modifier = Modifier.height(16.dp))
            Text(
                text = currentStatus,
                color = Color.LightGray,
                fontSize = 14.sp
            )
            Spacer(modifier = Modifier.height(32.dp))
            
            if (isVerifyingSite && currentWebsite.isNotEmpty()) {
                val baseUrl = ScraperRepository.getBaseUrl(currentWebsite)
                Box(modifier = Modifier.size(1.dp).background(Color.Transparent)) {
                    AndroidView(
                        factory = { context ->
                            WebView(context).apply {
                                settings.javaScriptEnabled = true
                                settings.domStorageEnabled = true
                                settings.userAgentString = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                                webViewClient = object : WebViewClient() {
                                    override fun onPageFinished(view: WebView, url: String) {
                                        super.onPageFinished(view, url)
                                        val checkScript = """
                                            (function() {
                                                setInterval(function() {
                                                    var cf = document.querySelector('.cf-turnstile-wrapper, #challenge-stage, input[type="checkbox"], #challenge-form, .mark-as-human');
                                                    if (cf) { cf.click(); }
                                                }, 1500);
                                                
                                                setTimeout(function() {
                                                    var title = document.title.toLowerCase();
                                                    var isCloudflare = title.includes("just a moment") || document.getElementById('challenge-stage') != null || document.querySelector('.cf-turnstile-wrapper') != null;
                                                    if (!isCloudflare) {
                                                        AndroidBridge.siteVerified();
                                                    }
                                                }, 3000);
                                            })();
                                        """.trimIndent()
                                        view.evaluateJavascript(checkScript, null)
                                    }
                                }
                                addJavascriptInterface(object {
                                    @JavascriptInterface
                                    fun siteVerified() {
                                        Handler(Looper.getMainLooper()).post {
                                            if (isVerifyingSite && baseUrl.isNotEmpty()) {
                                                SiteVerificationManager.markSiteVerified(baseUrl)
                                                isVerifyingSite = false
                                                processNextSite()
                                            }
                                        }
                                    }
                                }, "AndroidBridge")
                                loadUrl(baseUrl)
                            }
                        }
                    )
                }
            }

            if (watchUrlToExtract != null) {
                Box(modifier = Modifier.size(1.dp).background(Color.Transparent)) {
                    HiddenVideoExtractor(
                        url = watchUrlToExtract!!,
                        isMovie = isMovie,
                        season = season,
                        episode = episode,
                        targetServer = null,
                        onVideoUrlFound = { url ->
                            if (extractedUrl == null) {
                                extractedUrl = url
                                onPlay(url, "تلقائي", currentWebsite)
                            }
                        },
                        onServersFound = { servers ->
                            // Optional: handle servers
                        }
                    )
                }
            }
        }
    }
}
