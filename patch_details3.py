import re

with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'r') as f:
    content = f.read()

# Replace ServerSelectionDialog block for movie
# It starts with `ServerSelectionDialog(` and ends with `)` after `onPlay` lambda
movie_pattern = re.compile(r'ServerSelectionDialog\(\s*title = movie\.title,\s*isMovie = true,\s*onDismiss = \{ showSourceSheet = false \},\s*onPlay = \{ url, serverName, website ->.*?\}\s*\)', re.DOTALL)

movie_replacement = """showSourceSheet = false
                if (isDownloadMode) {
                    // Not supported instantly
                } else {
                    scope.launch {
                        historyRepository.addToHistory(
                            com.example.data.model.HistoryItem(
                                id = movie.id,
                                title = movie.title,
                                posterUrl = movie.posterUrl,
                                isMovie = true
                            )
                        )
                        navController.navigate("player?mediaId=${movie.id}&isMovie=true&title=${java.net.URLEncoder.encode(movie.title, "UTF-8")}&season=1&episode=1")
                    }
                }"""

content = movie_pattern.sub(movie_replacement, content)

series_pattern = re.compile(r'ServerSelectionDialog\(\s*title = series\.title,\s*isMovie = false,\s*season = .*?onPlay = \{ url, serverName, website ->.*?\}\s*\)', re.DOTALL)

series_replacement = """val ep = selectedEpisodeForSource!!
                selectedEpisodeForSource = null
                if (isDownloadMode) {
                    // Not supported instantly
                } else {
                    scope.launch {
                        val fullTitle = "${series.title} - S${uiState.selectedSeason?.seasonNumber}E${ep.episodeNumber}"
                        historyRepository.addToHistory(
                            com.example.data.model.HistoryItem(
                                id = series.id,
                                title = fullTitle,
                                posterUrl = ep.thumbnailUrl,
                                isMovie = false
                            )
                        )
                        navController.navigate("player?mediaId=${series.id}&isMovie=false&title=${java.net.URLEncoder.encode(series.title, "UTF-8")}&season=${uiState.selectedSeason?.seasonNumber ?: 1}&episode=${ep.episodeNumber}")
                    }
                }"""

content = series_pattern.sub(series_replacement, content)

with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'w') as f:
    f.write(content)
print("Patched DetailsScreens.kt successfully")
