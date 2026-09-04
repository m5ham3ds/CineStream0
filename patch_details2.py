import re

with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'r') as f:
    content = f.read()

# Series patch
old_series = 'navController.navigate("player?mediaId=${series.id}&isMovie=false&title=${series.title}")'
new_series = 'navController.navigate("player?mediaId=${series.id}&isMovie=false&title=${java.net.URLEncoder.encode(series.title, "UTF-8")}&season=${uiState.selectedSeason?.seasonNumber ?: 1}&episode=${ep.episodeNumber}")'
content = content.replace(old_series, new_series)

# Movie patch
old_movie = 'navController.navigate("player?mediaId=${movie.id}&isMovie=true&title=${movie.title}")'
new_movie = 'navController.navigate("player?mediaId=${movie.id}&isMovie=true&title=${java.net.URLEncoder.encode(movie.title, "UTF-8")}&season=1&episode=1")'
content = content.replace(old_movie, new_movie)

with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'w') as f:
    f.write(content)
print("Patched DetailsScreens.kt navigation params")
