import re

with open('app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt', 'r') as f:
    content = f.read()

init_patch = """
    fun initialize(mediaId: String, isMovie: Boolean, initialTitle: String, directUrl: String? = null, targetServer: String? = null, website: String? = null) {
        val hasArabic = initialTitle.any { it in '\u0600'..'\u06FF' }
        val isAnime = initialTitle.contains("anime", ignoreCase = true) || initialTitle.contains("أنمي", ignoreCase = true)
        
        val bestWebsite = website ?: when {
            isAnime -> "witanime.you"
            else -> "tv10.egydead.live"
        }

        _uiState.value = _uiState.value.copy(
            mediaId = mediaId,
            isMovie = isMovie,
            title = initialTitle,
            currentWebsite = bestWebsite,
            currentServer = targetServer
        )

        if (!directUrl.isNullOrEmpty() && (directUrl.contains(".mp4") || directUrl.contains(".m3u8") || directUrl.startsWith("local_offline_file"))) {
            _uiState.value = _uiState.value.copy(currentVideoUrl = directUrl, isLoading = false)
        } else if (!directUrl.isNullOrEmpty()) {
            // It's a watch url (webpage), we need to extract from it
            _uiState.value = _uiState.value.copy(extractionUrl = directUrl, isLoading = true)
        } else if (!isMovie) {
            loadEpisodes(mediaId, 1) // Default to season 1
        } else {
            generateExtractionUrl()
        }
    }
"""

content = re.sub(r'fun initialize\(mediaId: String, isMovie: Boolean, initialTitle: String, directUrl: String\? = null\).*?generateExtractionUrl\(\)\s*\}\s*\}', init_patch.strip(), content, flags=re.DOTALL)

with open('app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt', 'w') as f:
    f.write(content)

