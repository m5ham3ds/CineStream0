import re

with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'r') as f:
    content = f.read()

# Add import
content = 'import com.example.ui.screens.player.ServerSelectionDialog\n' + content

# Movie
movie_old = """showSourceSheet = false
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
                        onPlay(movie.title, null, null, null, 1, 1)
                    }
                }"""

movie_new = """ServerSelectionDialog(
                    title = movie.title,
                    isMovie = true,
                    isAnime = movie.genres.any { it.contains("Anime", ignoreCase = true) || it.contains("انمي", ignoreCase = true) },
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
                                onPlay(movie.title, url, serverName, website, 1, 1)
                            }
                        }
                    }
                )"""
content = content.replace(movie_old, movie_new)

# Series
series_old = """val ep = selectedEpisodeForSource!!
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
                        onPlay(series.title, null, null, null, uiState.selectedSeason?.seasonNumber ?: 1, ep.episodeNumber)
                    }
                }"""

series_new = """val ep = selectedEpisodeForSource!!
                ServerSelectionDialog(
                    title = series.title,
                    isMovie = false,
                    season = uiState.selectedSeason?.seasonNumber ?: 1,
                    episode = ep.episodeNumber,
                    isAnime = series.genres.any { it.contains("Anime", ignoreCase = true) || it.contains("انمي", ignoreCase = true) },
                    onDismiss = { selectedEpisodeForSource = null },
                    onPlay = { url, serverName, website ->
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
                                onPlay(series.title, url, serverName, website, uiState.selectedSeason?.seasonNumber ?: 1, ep.episodeNumber)
                            }
                        }
                    }
                )"""
content = content.replace(series_old, series_new)

with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'w') as f:
    f.write(content)
print("Patched DetailsScreens.kt back")

