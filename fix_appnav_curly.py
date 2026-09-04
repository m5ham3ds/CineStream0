with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'r') as f:
    content = f.read()

# Fix extra curly braces at the end
content = content.replace("}\n}\n}\n// Trending", "}\n// Trending")

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'w') as f:
    f.write(content)
