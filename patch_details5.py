import re

with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'r') as f:
    content = f.read()

# Fix MovieDetailsScreen missing params
content = content.replace('onPlay(movie.title, "local_offline_file://${downloadItem.id}", null, null)', 'onPlay(movie.title, "local_offline_file://${downloadItem.id}", null, null, 1, 1)')
content = content.replace('onPlay("Trailer", "trailer:${trailer.key}", null, null)', 'onPlay("Trailer", "trailer:${trailer.key}", null, null, 1, 1)')

# Fix SeriesDetailsScreen signature
content = content.replace('onPlay: (String, String, String?, String?) -> Unit\n) {', 'onPlay: (String, String?, String?, String?, Int, Int) -> Unit\n) {')
content = content.replace('onPlay: (String, String, String?, String?) -> Unit) {', 'onPlay: (String, String?, String?, String?, Int, Int) -> Unit) {')
content = content.replace('onPlay: (String, String, String?, String?) -> Unit', 'onPlay: (String, String?, String?, String?, Int, Int) -> Unit')


with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'w') as f:
    f.write(content)
print("Patched DetailsScreens.kt signatures completely")
