import re

with open('app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt', 'r') as f:
    content = f.read()

# Restore the sliders
sliders_code = """
                    // Left Vertical Slider (Brightness)
                    Box(modifier = Modifier.align(Alignment.CenterStart).padding(start = 24.dp)) {
                        VerticalSlider(
                            value = brightness, 
                            onValueChange = { brightness = it }
                        )
                    }

                    // Right Vertical Slider (Volume)
                    Box(modifier = Modifier.align(Alignment.CenterEnd).padding(end = 24.dp)) {
                        VerticalSlider(
                            value = volume, 
                            onValueChange = { volume = it }
                        )
                    }
                    
                    // Center Playback Controls"""

content = content.replace("                    // Center Playback Controls", sliders_code)

# Fix VerticalSlider signature and remove icons
vs_original = """fun VerticalSlider(
    value: Float,
    onValueChange: (Float) -> Unit,
    topIcon: ImageVector,
    bottomIcon: ImageVector
) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Icon(topIcon, contentDescription = null, tint = Color.White, modifier = Modifier.size(28.dp))
        Spacer(modifier = Modifier.height(16.dp))"""

vs_replacement = """fun VerticalSlider(
    value: Float,
    onValueChange: (Float) -> Unit
) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {"""

content = content.replace(vs_original, vs_replacement)

# Remove bottom icon
bottom_icon_original = """
        Spacer(modifier = Modifier.height(16.dp))
        Icon(bottomIcon, contentDescription = null, tint = Color.White, modifier = Modifier.size(28.dp))
    }
}"""

bottom_icon_replacement = """
    }
}"""

content = content.replace(bottom_icon_original, bottom_icon_replacement)

with open('app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt', 'w') as f:
    f.write(content)
print("Sliders restored without icons")
