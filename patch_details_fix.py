import re

with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'r') as f:
    content = f.read()

# For MovieDetailsScreen
fix_movie = """
            if (showSourceSheet) {
                ServerSelectionDialog(
                    title = movie.title,
                    isMovie = true,
                    onDismiss = { showSourceSheet = false },
                    onPlay = { url, serverName, website ->
                        showSourceSheet = false
                        if (isDownloadMode) {
                            scope.launch {
                                downloadRepository.addToDownloads(com.example.domain.models.DownloadItem(
                                    id = movie.id, title = movie.title, posterUrl = movie.posterUrl, isMovie = true, quality = serverName
                                ))
                                com.example.utils.AndroidDownloader.downloadVideo(context, url, "${movie.title} - $serverName")
                            }
                        } else {
                            scope.launch {
                                historyRepository.addToHistory(
                                    com.example.domain.models.HistoryItem(
                                        id = movie.id,
                                        title = movie.title,
                                        posterUrl = movie.posterUrl,
                                        isMovie = true,
                                        progress = 0f,
                                        duration = 1L
                                    )
                                )
                                onPlay(movie.title, url, serverName, website)
                            }
                        }
                    }
                )
            }
"""

content = re.sub(r'if \(showSourceSheet\) \{[\s\S]*?ServerSelectionDialog\([\s\S]*?\}\s*\)\s*\}\s*\} else \{[\s\S]*?onPlay\(movie\.title, source\.url, null, null\)[\s\S]*?\}\s*\}\s*\)\s*\}', fix_movie.strip(), content)

with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'w') as f:
    f.write(content)

