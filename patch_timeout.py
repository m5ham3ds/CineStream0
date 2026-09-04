import re

with open('app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt', 'r') as f:
    content = f.read()

old_extractor = """                HiddenVideoExtractor(
                    url = url,
                    isMovie = uiState.isMovie,
                    season = uiState.currentSeasonNumber,
                    episode = uiState.currentEpisodeNumber,
                    targetServer = uiState.currentServer ?: targetServer,
                    onVideoUrlFound = { extractedUrl ->
                        viewModel.setExtractedUrl(extractedUrl)
                    },
                    onServersFound = { servers ->
                        viewModel.updateServers(servers)
                    }
                )"""

new_extractor = """                // Timeout logic
                LaunchedEffect(url) {
                    kotlinx.coroutines.delay(20000) // 20 seconds timeout
                    if (uiState.currentVideoUrl == null) {
                        viewModel.onExtractionFailed()
                    }
                }

                HiddenVideoExtractor(
                    url = url,
                    isMovie = uiState.isMovie,
                    season = uiState.currentSeasonNumber,
                    episode = uiState.currentEpisodeNumber,
                    targetServer = uiState.currentServer ?: targetServer,
                    onVideoUrlFound = { extractedUrl ->
                        viewModel.setExtractedUrl(extractedUrl)
                    },
                    onServersFound = { servers ->
                        viewModel.updateServers(servers)
                    }
                )"""

content = content.replace(old_extractor, new_extractor)

with open('app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt', 'w') as f:
    f.write(content)
print("Patched PlayerScreen.kt for timeout")

