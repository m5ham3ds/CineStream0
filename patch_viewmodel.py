import re

with open('app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt', 'r') as f:
    content = f.read()

old_init = "fun initialize(mediaId: String, isMovie: Boolean, initialTitle: String, directUrl: String? = null, targetServer: String? = null, website: String? = null) {"

new_init = """fun initialize(mediaId: String, isMovie: Boolean, initialTitle: String, directUrl: String? = null, targetServer: String? = null, website: String? = null, seasonNum: Int = 1, episodeNum: Int = 1) {"""

content = content.replace(old_init, new_init)

old_logic = """        val bestWebsite = website ?: when {
            isAnime -> "witanime.you"
            else -> "tv10.egydead.live"
        }"""

new_logic = """        val animeSites = listOf("WitAnime", "Anime4up", "AnimeBlkom", "Animeat", "Arabanime", "AnimeLuxe")
        val movieSites = listOf("EgyDead TV10", "QFilm", "TopCinema", "ArabSeed", "ArabSeed Wine", "CimaLight", "Egy Best", "Stardima", "Brstej")
        val seriesSites = listOf("TopCinema", "EgyDead TV10", "Egy Best", "ArabSeed Wine", "QFilm", "ArabSeed", "CimaLight", "Stardima", "Brstej")

        val siteList = when {
            isAnime -> animeSites
            isMovie -> movieSites
            else -> seriesSites
        }

        val bestWebsite = website ?: siteList.first()
        
        _uiState.value = _uiState.value.copy(
            availableWebsites = siteList
        )"""

content = content.replace(old_logic, new_logic)

# Replace the initial states for season and episode in initialize
old_state = """        _uiState.value = _uiState.value.copy(
            mediaId = mediaId,
            isMovie = isMovie,
            title = initialTitle,
            currentWebsite = bestWebsite ?: "",
            currentServer = targetServer ?: ""
        )"""
new_state = """        _uiState.value = _uiState.value.copy(
            mediaId = mediaId,
            isMovie = isMovie,
            title = initialTitle,
            currentWebsite = bestWebsite ?: "",
            currentServer = targetServer ?: "",
            currentSeasonNumber = seasonNum,
            currentEpisodeNumber = episodeNum
        )"""
content = content.replace(old_state, new_state)

with open('app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt', 'w') as f:
    f.write(content)
print("Patched PlayerViewModel.kt")
