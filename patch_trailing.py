import re

with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'r') as f:
    content = f.read()

content = content.replace('isMovie = true,\n                                        \n                                    )', 'isMovie = true\n                                    )')
content = content.replace('isMovie = false, \n                                    )', 'isMovie = false\n                                    )')

with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'w') as f:
    f.write(content)

