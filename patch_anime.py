import re

with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'r') as f:
    content = f.read()

# Replace isAnime logic
content = content.replace(
    'isAnime = movie.genres.any { it.contains("Anime", ignoreCase = true) || it.contains("انمي", ignoreCase = true) }',
    'isAnime = movie.genres.any { it.contains("Anime", ignoreCase = true) || it.contains("انمي", ignoreCase = true) || it.contains("Animation", ignoreCase = true) || it.contains("رسوم", ignoreCase = true) }'
)
content = content.replace(
    'isAnime = series.genres.any { it.contains("Anime", ignoreCase = true) || it.contains("انمي", ignoreCase = true) }',
    'isAnime = series.genres.any { it.contains("Anime", ignoreCase = true) || it.contains("انمي", ignoreCase = true) || it.contains("Animation", ignoreCase = true) || it.contains("رسوم", ignoreCase = true) }'
)

with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'w') as f:
    f.write(content)
print("Patched isAnime logic")
