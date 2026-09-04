with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'r') as f:
    content = f.read()

content = content.replace('import com.example.ui.screens.player.ServerSelectionDialog\npackage com.example.ui.screens.details\n', 'package com.example.ui.screens.details\nimport com.example.ui.screens.player.ServerSelectionDialog\n')

with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'w') as f:
    f.write(content)
