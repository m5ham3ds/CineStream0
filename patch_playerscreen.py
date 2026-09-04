import re

with open('app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt', 'r') as f:
    content = f.read()

old_fun = """@Composable
fun PlayerScreen(
    mediaId: String,
    isMovie: Boolean,
    title: String,
    url: String? = null,
    server: String? = null,
    website: String? = null,
    onBack: () -> Unit
) {"""

new_fun = """@Composable
fun PlayerScreen(
    mediaId: String,
    isMovie: Boolean,
    title: String,
    url: String? = null,
    server: String? = null,
    website: String? = null,
    seasonNum: Int = 1,
    episodeNum: Int = 1,
    onBack: () -> Unit
) {"""

content = content.replace(old_fun, new_fun)

old_init = "viewModel.initialize(mediaId, isMovie, title, url, server, website)"
new_init = "viewModel.initialize(mediaId, isMovie, title, url, server, website, seasonNum, episodeNum)"
content = content.replace(old_init, new_init)

# Remove the "Ready to Play" dialog (showInitialSelection) completely.
# We want it to just play automatically!
# The user said: تظهر له نافرة اختيار جودة داخل صفحة تشغيل الفيديو لا اود ذالك بل يتم اختيار جودة بشكل تلقائي دون اي تدخل من المستخدم
content = re.sub(r'var showInitialSelection by remember \{ mutableStateOf\(true\) \}', 'var showInitialSelection by remember { mutableStateOf(false) }', content)
content = content.replace('if (showInitialSelection) {', 'if (false) {')

with open('app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt', 'w') as f:
    f.write(content)
print("Patched PlayerScreen.kt")
