import re

with open('app/src/main/java/com/example/ui/components/BackgroundWebView.kt', 'r') as f:
    content = f.read()

# Add timeout logic to BackgroundWebView
# Find: if (urls.isEmpty()) { ... }
# Insert a timeout effect

timeout_effect = """
    LaunchedEffect(currentUrl) {
        if (currentUrl != null) {
            delay(20000) // 20 seconds maximum per URL
            onSiteVerified(currentUrl) // Skip it so we don't get stuck forever
            currentIndex++
        }
    }
"""

content = re.sub(r'(var currentIndex by remember \{ mutableStateOf\(0\) \}\s*val currentUrl = if \(currentIndex < urls\.size\) urls\[currentIndex\] else null)', r'\1\n' + timeout_effect, content)

with open('app/src/main/java/com/example/ui/components/BackgroundWebView.kt', 'w') as f:
    f.write(content)

