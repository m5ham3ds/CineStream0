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
start_idx = content.find('private fun generateExtractionUrl() {')
end_idx = content.find('    }\n}', start_idx) + 6

new_gen = """private fun generateExtractionUrl() {
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

content = content[:start_idx] + new_gen + content[end_idx:]

with open('app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt', 'w') as f:
    f.write(content)

