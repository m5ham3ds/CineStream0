import re

# 1. Fix DetailsScreens.kt
with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'r') as f:
    content = f.read()

content = content.replace('com.example.domain.models.DownloadItem', 'com.example.data.model.DownloadItem')
content = content.replace('com.example.domain.models.HistoryItem', 'com.example.data.model.HistoryItem')
content = content.replace('it.name.contains("Anime"', 'it.contains("Anime"')

with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'w') as f:
    f.write(content)

# 2. Fix PlayerViewModel.kt
with open('app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt', 'r') as f:
    pvm_content = f.read()

pvm_content = pvm_content.replace('currentServer = targetServer', 'currentServer = targetServer ?: ""')
pvm_content = pvm_content.replace('currentWebsite = bestWebsite', 'currentWebsite = bestWebsite ?: ""')

with open('app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt', 'w') as f:
    f.write(pvm_content)

