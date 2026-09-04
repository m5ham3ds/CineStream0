import re

with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'r') as f:
    content = f.read()

series_patch = """
            if (selectedEpisodeForSource != null) {
                ServerSelectionDialog(
                    title = series.title,
                    isMovie = false,
                    season = uiState.selectedSeason?.seasonNumber ?: 1,
                    episode = selectedEpisodeForSource?.episodeNumber ?: 1,
                    isAnime = series.genres.any { it.name.contains("Anime", ignoreCase = true) },
                    onDismiss = { selectedEpisodeForSource = null },
                    onPlay = { url, serverName, website ->
                        val ep = selectedEpisodeForSource!!
                        selectedEpisodeForSource = null
                        if (isDownloadMode) {
                            scope.launch {
                                val fullTitle = "${series.title} - S${uiState.selectedSeason?.seasonNumber}E${ep.episodeNumber}"
                                downloadRepository.addToDownloads(com.example.domain.models.DownloadItem(
                                    id = ep.id, title = fullTitle, posterUrl = ep.thumbnailUrl, isMovie = false, quality = serverName
                                ))
                                com.example.utils.AndroidDownloader.downloadVideo(context, url, "$fullTitle - $serverName")
                            }
                        } else {
                            scope.launch {
                                val fullTitle = "${series.title} - S${uiState.selectedSeason?.seasonNumber}E${ep.episodeNumber}"
                                historyRepository.addToHistory(
                                    com.example.domain.models.HistoryItem(
                                        id = ep.id, title = fullTitle, posterUrl = ep.thumbnailUrl, isMovie = false, progress = 0f, duration = 1L
                                    )
                                )
                                onPlay(fullTitle, url)
                            }
                        }
                    }
                )
            }
"""

content = re.sub(r'if \(selectedEpisodeForSource != null\) \{[\s\S]*?SourceSelectionSheet\([\s\S]*?onDismiss = \{ selectedEpisodeForSource = null \},[\s\S]*?onSourceSelected = \{ source ->[\s\S]*?\}[\s\S]*?\}\s*\}', series_patch.strip(), content)

with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'w') as f:
    f.write(content)

