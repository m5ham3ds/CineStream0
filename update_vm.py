import re

with open('app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt', 'r') as f:
    content = f.read()

# Replace availableWebsites
websites = """    val availableWebsites: List<String> = listOf(
        "EgyDead TV10",
        "QFilm",
        "Animeat",
        "Arabanime",
        "ArabSeed",
        "ArabSeed Wine",
        "Animerco",
        "CimaLight",
        "Egy Best",
        "Stardima",
        "Brstej",
        "AnimeLuxe",
        "Watch Stardima",
        "WitAnime"
    ),
    val currentWebsite: String = "EgyDead TV10","""
content = re.sub(r'val availableWebsites: List<String> = listOf\([^)]+\),\s+val currentWebsite: String = "[^"]+",', websites, content, flags=re.MULTILINE)

# Replace generateExtractionUrl
new_gen = """
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
            } else {
                // Fallback or error
                _uiState.value = _uiState.value.copy(isLoading = false)
            }
        }
    }
"""
content = re.sub(r'private fun generateExtractionUrl\(\)\s*\{.*?(?=\n\s*\n|\n\})', new_gen, content, flags=re.DOTALL | re.MULTILINE)

# Wait, the regex for generateExtractionUrl is risky because the function is large. Let's just do a simpler replace.
