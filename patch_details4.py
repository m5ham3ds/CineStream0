import re

with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'r') as f:
    content = f.read()

# Fix MovieDetailsScreen signature
old_movie_sig = "onPlay: (String, String, String?, String?) -> Unit,"
new_movie_sig = "onPlay: (String, String?, String?, String?, Int, Int) -> Unit,"
content = content.replace(old_movie_sig, new_movie_sig)

# Fix SeriesDetailsScreen signature
old_series_sig = "onPlay: (String, String, String?, String?) -> Unit,"
new_series_sig = "onPlay: (String, String?, String?, String?, Int, Int) -> Unit,"
content = content.replace(old_series_sig, new_series_sig)

# Fix trailer play calls
content = content.replace('onPlay("Trailer", "trailer:${trailer.key}", null, null)', 'onPlay("Trailer", "trailer:${trailer.key}", null, null, 1, 1)')

# Fix Movie play call
movie_pattern = re.compile(r"""scope\.launch \{\s*historyRepository\.addToHistory\(\s*com\.example\.data\.model\.HistoryItem\(\s*id = movie\.id,\s*title = movie\.title,\s*posterUrl = movie\.posterUrl,\s*isMovie = true\s*\)\s*\)\s*navController\.navigate\("player\?mediaId=\$\{movie\.id\}&isMovie=true&title=\$\{java\.net\.URLEncoder\.encode\(movie\.title, "UTF-8"\)\}&season=1&episode=1"\)\s*\}""")
movie_rep = """scope.launch {
                        historyRepository.addToHistory(
                            com.example.data.model.HistoryItem(
                                id = movie.id,
                                title = movie.title,
                                posterUrl = movie.posterUrl,
                                isMovie = true
                            )
                        )
                        onPlay(movie.title, null, null, null, 1, 1)
                    }"""
content = movie_pattern.sub(movie_rep, content)

# Fix Series play call
series_pattern = re.compile(r"""scope\.launch \{\s*val fullTitle = "\$\{series\.title\} - S\$\{uiState\.selectedSeason\?\.seasonNumber\}E\$\{ep\.episodeNumber\}"\s*historyRepository\.addToHistory\(\s*com\.example\.data\.model\.HistoryItem\(\s*id = series\.id,\s*title = fullTitle,\s*posterUrl = ep\.thumbnailUrl,\s*isMovie = false\s*\)\s*\)\s*navController\.navigate\("player\?mediaId=\$\{series\.id\}&isMovie=false&title=\$\{java\.net\.URLEncoder\.encode\(series\.title, "UTF-8"\)\}&season=\$\{uiState\.selectedSeason\?\.seasonNumber \?: 1\}&episode=\$\{ep\.episodeNumber\}"\)\s*\}""")
series_rep = """scope.launch {
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
                    }"""
content = series_pattern.sub(series_rep, content)

with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'w') as f:
    f.write(content)
print("Patched DetailsScreens.kt signatures and callbacks")
