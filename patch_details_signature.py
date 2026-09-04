import re

with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'r') as f:
    content = f.read()

content = content.replace('onPlay: (String, String) -> Unit', 'onPlay: (String, String, String?, String?) -> Unit')

# And patch the calls
# In MovieDetailsScreen:
# onPlay(movie.title, url) -> onPlay(movie.title, url, serverName, website)
content = content.replace('onPlay(movie.title, url) // We just pass the extracted video URL or server URL here', 'onPlay(movie.title, url, serverName, website)')
content = content.replace('onPlay(movie.title, "")', 'onPlay(movie.title, "", null, null)')
content = content.replace('onPlay(movie.title, "local_offline_file://${downloadItem.id}")', 'onPlay(movie.title, "local_offline_file://${downloadItem.id}", null, null)')

# In SeriesDetailsScreen:
# onPlay(fullTitle, url) -> onPlay(fullTitle, url, serverName, website)
content = content.replace('onPlay(fullTitle, url)', 'onPlay(fullTitle, url, serverName, website)')
# What about the generic source.url in old code?
content = content.replace('onPlay("${series.title} - ${ep.title}", source.url)', 'onPlay("${series.title} - ${ep.title}", source.url, null, null)')
content = content.replace('onPlay(movie.title, source.url)', 'onPlay(movie.title, source.url, null, null)')

with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'w') as f:
    f.write(content)

