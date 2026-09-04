with open('app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'val isAnime = initialTitle.contains("anime", ignoreCase = true) || initialTitle.contains("أنمي", ignoreCase = true)',
    'val isAnime = initialTitle.contains("anime", ignoreCase = true) || initialTitle.contains("انمي", ignoreCase = true) || initialTitle.contains("أنمي", ignoreCase = true) || initialTitle.contains("Animation", ignoreCase = true)'
)

with open('app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt', 'w') as f:
    f.write(content)
