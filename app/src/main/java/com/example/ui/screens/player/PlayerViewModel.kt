package com.example.ui.screens.player

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.data.repository.TmdbMediaRepositoryImpl
import com.example.domain.models.Episode
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay

data class PlayerUiState(
    val isLoading: Boolean = true,
    val mediaId: String = "",
    val isMovie: Boolean = true,
    val isAnime: Boolean = false,
    val title: String = "",

    // Website (Provider)
    val availableWebsites: List<String> = emptyList(),
    val currentWebsite: String = "",
    val fallbackWebsites: List<String> = emptyList(),

    // Server
    val availableServers: List<String> = emptyList(),
    val currentServer: String = "",

    // Quality
    val availableQualities: List<String> = listOf("Auto", "1080p", "720p"),
    val currentQuality: String = "Auto",

    // Episodes
    val episodes: List<Episode> = emptyList(),
    val currentEpisodeId: String = "",
    val currentSeasonNumber: Int = 1,
    val currentEpisodeNumber: Int = 1,

    // Extracted URL
    val currentVideoUrl: String? = null,
    val extractionUrl: String? = null // The URL to feed to the hidden WebView
)

class PlayerViewModel : ViewModel() {
    private val tmdbRepo = TmdbMediaRepositoryImpl()

    private val _uiState = MutableStateFlow(PlayerUiState())
    val uiState: StateFlow<PlayerUiState> = _uiState.asStateFlow()

    private var extractionTimeoutJob: kotlinx.coroutines.Job? = null

    fun initialize(mediaId: String, isMovie: Boolean, initialTitle: String, directUrl: String? = null, targetServer: String? = null, website: String? = null) {
        val hasArabic = initialTitle.any { it in '؀'..'ۿ' }
        val isAnime = initialTitle.contains("anime", ignoreCase = true) || initialTitle.contains("أنمي", ignoreCase = true)
        
        val allAnimeSites = listOf("WitAnime", "Anime4up", "AnimeBlkom", "Animeat", "Arabanime", "Animerco", "AnimeLuxe")
        val allMovieSeriesSites = listOf("EgyDead TV10", "QFilm", "TopCinema", "Egy Best", "ArabSeed Wine", "ArabSeed", "CimaLight", "Stardima", "Brstej", "Watch Stardima", "Laaroza", "Almeshkah")

        val fallbackList = when {
            isAnime -> listOf("WitAnime", "Anime4up", "AnimeBlkom") + allAnimeSites.filter { it !in listOf("WitAnime", "Anime4up", "AnimeBlkom") }
            isMovie -> listOf("EgyDead TV10", "QFilm", "TopCinema") + allMovieSeriesSites.filter { it !in listOf("EgyDead TV10", "QFilm", "TopCinema") }
            else -> listOf("TopCinema", "EgyDead TV10", "Egy Best", "ArabSeed Wine") + allMovieSeriesSites.filter { it !in listOf("TopCinema", "EgyDead TV10", "Egy Best", "ArabSeed Wine") }
        }
        
        val availableList = if (isAnime) allAnimeSites else allMovieSeriesSites
        
        val bestWebsite = website ?: fallbackList.first()
        val remainingFallbacks = if (website == null) fallbackList.drop(1) else emptyList()

        _uiState.value = _uiState.value.copy(
            mediaId = mediaId,
            isMovie = isMovie,
            isAnime = isAnime,
            title = initialTitle,
            availableWebsites = availableList,
            currentWebsite = bestWebsite,
            fallbackWebsites = remainingFallbacks,
            currentServer = targetServer ?: ""
        )

        if (!directUrl.isNullOrEmpty() && (directUrl.contains(".mp4") || directUrl.contains(".m3u8") || directUrl.startsWith("local_offline_file"))) {
            _uiState.value = _uiState.value.copy(currentVideoUrl = directUrl, isLoading = false)
        } else if (!directUrl.isNullOrEmpty()) {
            // It's a watch url (webpage), we need to extract from it
            _uiState.value = _uiState.value.copy(extractionUrl = directUrl, isLoading = true)
            startExtractionTimeout()
        } else if (!isMovie) {
            loadEpisodes(mediaId, 1) // Default to season 1
        } else {
            generateExtractionUrl()
        }
    }

    private fun loadEpisodes(seriesId: String, seasonNumber: Int) {
        viewModelScope.launch {
            try {
                // Fetch full series details to get episodes for the season
                val series = tmdbRepo.getSeriesById(seriesId)
                val season = series?.seasons?.find { it.seasonNumber == seasonNumber }
                if (season != null) {
                    val fullSeason = tmdbRepo.getSeasonEpisodes(seriesId, seasonNumber)
                    _uiState.value = _uiState.value.copy(
                        episodes = fullSeason,
                        currentEpisodeId = fullSeason.firstOrNull()?.id ?: "",
                        currentSeasonNumber = seasonNumber,
                        currentEpisodeNumber = fullSeason.firstOrNull()?.episodeNumber ?: 1
                    )
                }
                generateExtractionUrl()
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }

    fun selectWebsite(website: String) {
        _uiState.value = _uiState.value.copy(currentWebsite = website, isLoading = true, currentVideoUrl = null, fallbackWebsites = emptyList())
        generateExtractionUrl()
    }

    fun selectServer(server: String) {
        _uiState.value = _uiState.value.copy(currentServer = server, isLoading = true, currentVideoUrl = null)
        generateExtractionUrl() // In a real app, this might change the iframe URL params
    }

    fun selectEpisode(episode: Episode) {
        _uiState.value = _uiState.value.copy(
            currentEpisodeId = episode.id,
            currentEpisodeNumber = episode.episodeNumber,
            title = episode.title,
            isLoading = true,
            currentVideoUrl = null
        )
        generateExtractionUrl()
    }

    fun setExtractedUrl(url: String) {
        extractionTimeoutJob?.cancel()
        // Only set if we don't already have one, or if it's a new quality selection
        if (_uiState.value.currentVideoUrl != url) {
            _uiState.value = _uiState.value.copy(
                currentVideoUrl = url,
                isLoading = false
            )
        }
    }

    fun updateServers(servers: List<String>) {
        if (_uiState.value.availableServers != servers && servers.isNotEmpty()) {
            _uiState.value = _uiState.value.copy(
                availableServers = servers,
                currentServer = servers.first()
            )
        }
    }

    private fun startExtractionTimeout() {
        extractionTimeoutJob?.cancel()
        extractionTimeoutJob = viewModelScope.launch {
            delay(25000) // 25 seconds timeout
            if (_uiState.value.currentVideoUrl == null) {
                tryNextFallback()
            }
        }
    }
    
    private fun tryNextFallback() {
        val fallbacks = _uiState.value.fallbackWebsites
        if (fallbacks.isNotEmpty()) {
            val nextSite = fallbacks.first()
            _uiState.value = _uiState.value.copy(
                currentWebsite = nextSite,
                fallbackWebsites = fallbacks.drop(1),
                isLoading = true,
                currentVideoUrl = null
            )
            generateExtractionUrl()
        } else {
            _uiState.value = _uiState.value.copy(isLoading = false)
        }
    }

    private fun generateExtractionUrl() {
        val state = _uiState.value
        
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true, extractionUrl = null)
            val watchUrl = com.example.data.repository.ScraperRepository.getWatchUrl(
                website = state.currentWebsite,
                query = state.title,
                isMovie = state.isMovie,
                season = state.currentSeasonNumber,
                episode = state.currentEpisodeNumber
            )
            
            if (watchUrl != null) {
                _uiState.value = _uiState.value.copy(extractionUrl = watchUrl, isLoading = true)
                startExtractionTimeout()
            } else {
                tryNextFallback()
            }
        }
    }
}
