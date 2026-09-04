import re

with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'r') as f:
    content = f.read()

# Make sure ServerSelectionDialog is imported
if 'import com.example.ui.screens.player.ServerSelectionDialog' not in content:
    content = content.replace('import androidx.compose.runtime.*', 'import androidx.compose.runtime.*\nimport com.example.ui.screens.player.ServerSelectionDialog')

# Patch MovieDetailsScreen
movie_patch = """
            if (showSourceSheet) {
                ServerSelectionDialog(
                    title = movie.title,
                    isMovie = true,
                    onDismiss = { showSourceSheet = false },
                    onPlay = { url, serverName, website ->
                        showSourceSheet = false
                        onPlay(movie.title, url) // We just pass the extracted video URL or server URL here
                    }
                )
            }
"""
content = re.sub(r'if \(showSourceSheet\) \{[\s\S]*?SourceSelectionSheet\([\s\S]*?onDismiss = \{ showSourceSheet = false \}[\s\S]*?\}\s*\}', movie_patch.strip(), content)

# Patch SeriesDetailsScreen
# SeriesDetailsScreen doesn't seem to have showSourceSheet right now, let's check its code.
with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'w') as f:
    f.write(content)

