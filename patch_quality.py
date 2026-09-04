import re

with open('app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt', 'r') as f:
    content = f.read()

# 1. Add state for available qualities
new_state = """    var currentQuality by remember { mutableStateOf("Auto") }
    var availableQualities by remember { mutableStateOf(listOf("Auto")) }"""
content = content.replace('var currentQuality by remember { mutableStateOf("Auto") }', new_state)

# 2. Extract qualities when Player is ready
old_listener = """                override fun onPlaybackStateChanged(state: Int) {
                    if (state == Player.STATE_READY) {
                        totalDuration = duration.coerceAtLeast(0L)
                    }
                }"""

new_listener = """                override fun onPlaybackStateChanged(state: Int) {
                    if (state == Player.STATE_READY) {
                        totalDuration = duration.coerceAtLeast(0L)
                        
                        // Extract actual qualities from ExoPlayer
                        val trackInfo = trackSelector.currentMappedTrackInfo
                        if (trackInfo != null) {
                            val qualities = mutableListOf("Auto")
                            for (i in 0 until trackInfo.rendererCount) {
                                if (trackInfo.getRendererType(i) == androidx.media3.common.C.TRACK_TYPE_VIDEO) {
                                    val trackGroups = trackInfo.getTrackGroups(i)
                                    for (g in 0 until trackGroups.length) {
                                        val group = trackGroups.get(g)
                                        for (t in 0 until group.length) {
                                            val format = group.getFormat(t)
                                            if (format.height > 0) {
                                                qualities.add("${format.height}p")
                                            }
                                        }
                                    }
                                }
                            }
                            // Keep unique and sort descending by height, but put Auto first
                            val uniqueQualities = qualities.distinct().toMutableList()
                            uniqueQualities.remove("Auto")
                            uniqueQualities.sortByDescending { it.replace("p", "").toIntOrNull() ?: 0 }
                            uniqueQualities.add(0, "Auto")
                            availableQualities = uniqueQualities
                        }
                    }
                }"""
content = content.replace(old_listener, new_listener)

# 3. Use availableQualities in the bottom sheet
old_sheet = """                val qualities = listOf("Auto", "4K", "1080p", "720p", "480p", "360p")
                qualities.forEach { q ->"""

new_sheet = """                availableQualities.forEach { q ->"""
content = content.replace(old_sheet, new_sheet)

# 4. Use currentQuality state variable in the bottom bar action, not uiState.currentQuality
old_action = "QualityAction(uiState.currentQuality, onClick = { showQualitySheet = true })"
new_action = "QualityAction(currentQuality, onClick = { showQualitySheet = true })"
content = content.replace(old_action, new_action)

with open('app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt', 'w') as f:
    f.write(content)
print("Patched PlayerScreen.kt for real qualities")
