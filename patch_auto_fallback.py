import re

with open('app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt', 'r') as f:
    content = f.read()

old_gen = """    private fun generateExtractionUrl() {
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
            } else {
                _uiState.value = _uiState.value.copy(isLoading = false)
            }
        }
    }"""

new_gen = """    private fun generateExtractionUrl() {
        val state = _uiState.value
        
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true, extractionUrl = null)
            val watchUrl = kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.IO) {
                com.example.data.repository.ScraperRepository.getWatchUrl(
                    website = state.currentWebsite,
                    query = state.title,
                    isMovie = state.isMovie,
                    season = state.currentSeasonNumber,
                    episode = state.currentEpisodeNumber
                )
            }
            
            if (watchUrl != null) {
                _uiState.value = _uiState.value.copy(extractionUrl = watchUrl, isLoading = true)
            } else {
                // Auto Fallback to next site
                val currentIdx = state.availableWebsites.indexOf(state.currentWebsite)
                if (currentIdx != -1 && currentIdx < state.availableWebsites.size - 1) {
                    val nextSite = state.availableWebsites[currentIdx + 1]
                    _uiState.value = _uiState.value.copy(currentWebsite = nextSite)
                    generateExtractionUrl()
                } else {
                    _uiState.value = _uiState.value.copy(isLoading = false)
                }
            }
        }
    }

    fun onExtractionFailed() {
        val state = _uiState.value
        val currentIdx = state.availableWebsites.indexOf(state.currentWebsite)
        if (currentIdx != -1 && currentIdx < state.availableWebsites.size - 1) {
            val nextSite = state.availableWebsites[currentIdx + 1]
            _uiState.value = _uiState.value.copy(currentWebsite = nextSite, currentVideoUrl = null)
            generateExtractionUrl()
        } else {
            _uiState.value = _uiState.value.copy(isLoading = false, currentVideoUrl = null)
        }
    }"""

content = content.replace(old_gen, new_gen)

with open('app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt', 'w') as f:
    f.write(content)
print("Patched PlayerViewModel.kt for auto fallback")

