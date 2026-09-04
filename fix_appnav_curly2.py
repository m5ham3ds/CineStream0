with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'r') as f:
    content = f.read()

content = content.replace("}\n// Trending and Watching added at the end using sed later", "}\n}\n// Trending and Watching added at the end using sed later")

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'w') as f:
    f.write(content)
