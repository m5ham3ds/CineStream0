package com.example.ui.screens.player

import android.annotation.SuppressLint
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
import com.example.data.repository.ScraperRepository
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
    var currentStatus by remember { mutableStateOf("جاري البحث عن روابط المشاهدة...") }
    var extractedUrl by remember { mutableStateOf<String?>(null) }
    var currentWebsite by remember { mutableStateOf("") }
    
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
            currentStatus = "جاري فحص الموقع: $currentWebsite"
            
            scope.launch {
                val url = withContext(Dispatchers.IO) {
                    ScraperRepository.getWatchUrl(currentWebsite, title, isMovie, season, episode)
                }
                if (url != null) {
                    watchUrlToExtract = url
                } else {
                    siteIndex++
                    processNextSite()
                }
            }
        } else {
            currentStatus = "لم يتم العثور على روابط. جرب في وقت لاحق."
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