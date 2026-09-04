import re

with open('app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'fun PlayerScreen(mediaId: String, isMovie: Boolean, title: String, url: String? = null, onBack: () -> Unit, viewModel: PlayerViewModel = viewModel()) {',
    'fun PlayerScreen(mediaId: String, isMovie: Boolean, title: String, url: String? = null, targetServer: String? = null, website: String? = null, onBack: () -> Unit, viewModel: PlayerViewModel = viewModel()) {'
)

content = content.replace(
    'viewModel.initialize(mediaId, isMovie, title, url)',
    'viewModel.initialize(mediaId, isMovie, title, url, targetServer, website)'
)

# And make sure HiddenVideoExtractor uses the right state
content = content.replace(
    'targetServer = uiState.currentServer,',
    'targetServer = uiState.currentServer ?: targetServer,'
)

with open('app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt', 'w') as f:
    f.write(content)

