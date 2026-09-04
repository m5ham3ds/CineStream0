import sys

with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'r') as f:
    content = f.read()

start_str = "if (selectedEpisodeForSource != null) {"
end_str = "if (showBatchDownloadSheet) {"

start_idx = content.find(start_str)
end_idx = content.find(end_str)

if start_idx == -1 or end_idx == -1:
    print("Could not find blocks for Series")
    sys.exit(1)

new_block = """if (selectedEpisodeForSource != null) {
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
                                onPlay(fullTitle, url, serverName, website)
                            }
                        }
                    }
                )
            }

            """

content = content[:start_idx] + new_block + content[end_idx:]

with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'w') as f:
    f.write(content)

