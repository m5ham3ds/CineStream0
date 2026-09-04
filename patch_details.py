import re

with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'r') as f:
    content = f.read()

# Remove import
content = content.replace('import com.example.ui.screens.player.ServerSelectionDialog\n', '')

# For Movie
movie_dialog = """            if (showSourceSheet) {
                ServerSelectionDialog(
                    title = movie.title,
                    isMovie = true,
                    onDismiss = { showSourceSheet = false },
                    onPlay = { url, serverName, website ->
                        showSourceSheet = false
                        if (isDownloadMode) {
                            scope.launch {
                                downloadRepository.addToDownloads(com.example.data.model.DownloadItem(
                                    id = movie.id, title = movie.title, posterUrl = movie.posterUrl, isMovie = true, quality = serverName
                                ))
                                com.example.utils.AndroidDownloader.downloadVideo(context, url, "${movie.title} - $serverName")
                            }
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
                                navController.navigate("player?mediaId=${movie.id}&isMovie=true&title=${movie.title}&url=${java.net.URLEncoder.encode(url, "UTF-8")}&server=$serverName&website=$website")
                            }
                        }
                    }
                )
            }"""

movie_replacement = """            if (showSourceSheet) {
                showSourceSheet = false
                if (isDownloadMode) {
                    // Downloads require extracted URL, we can't do this instantly without extraction.
                    // To keep it simple, we don't support direct download without extraction.
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
                        // Launch player without direct URL, letting PlayerViewModel determine it
                        navController.navigate("player?mediaId=${movie.id}&isMovie=true&title=${movie.title}")
                    }
                }
            }"""

content = content.replace(movie_dialog, movie_replacement)

# For Series
series_dialog = """            if (selectedEpisodeForSource != null) {
                ServerSelectionDialog(
                    title = series.title,
                    isMovie = false,
                    season = uiState.selectedSeason?.seasonNumber ?: 1,
                    episode = selectedEpisodeForSource?.episodeNumber ?: 1,
                    isAnime = series.genres.any { it.contains("Anime", ignoreCase = true) },
                    onDismiss = { selectedEpisodeForSource = null },
                    onPlay = { url, serverName, website ->
                        val ep = selectedEpisodeForSource!!
                        selectedEpisodeForSource = null
                        if (isDownloadMode) {
                            scope.launch {
                                val fullTitle = "${series.title} - S${uiState.selectedSeason?.seasonNumber}E${ep.episodeNumber}"
                                downloadRepository.addToDownloads(com.example.data.model.DownloadItem(
                                    id = ep.id, title = fullTitle, posterUrl = ep.thumbnailUrl, isMovie = false, quality = serverName
                                ))
                                com.example.utils.AndroidDownloader.downloadVideo(context, url, "$fullTitle - $serverName")
                            }
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
                                navController.navigate("player?mediaId=${series.id}&isMovie=false&title=${series.title}&url=${java.net.URLEncoder.encode(url, "UTF-8")}&server=$serverName&website=$website")
                            }
                        }
                    }
                )
            }"""

series_replacement = """            if (selectedEpisodeForSource != null) {
                val ep = selectedEpisodeForSource!!
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
                        navController.navigate("player?mediaId=${series.id}&isMovie=false&title=${series.title}")
                    }
                }
            }"""

content = content.replace(series_dialog, series_replacement)

with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'w') as f:
    f.write(content)
print("Patched DetailsScreens.kt")

