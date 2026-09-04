import sys

with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'r') as f:
    content = f.read()

start_str = "if (showSourceSheet) {"
end_str = "Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = \"Back\", tint = MaterialTheme.colorScheme.onBackground)"

start_idx = content.find(start_str)
end_idx = content.find(end_str)

if start_idx == -1 or end_idx == -1:
    print("Could not find blocks")
    sys.exit(1)

new_block = """if (showSourceSheet) {
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

            IconButton(
                onClick = onBack,
                modifier = Modifier
                    .padding(top = padding.calculateTopPadding() + 8.dp, start = 16.dp)
                    .background(Color.Black.copy(alpha=0.3f), CircleShape)
            ) {
                """

content = content[:start_idx] + new_block + content[end_idx:]

with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'w') as f:
    f.write(content)

