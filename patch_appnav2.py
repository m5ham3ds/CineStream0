import re

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'r') as f:
    content = f.read()

# Remove state variables
content = re.sub(r'var isUpdatingData by remember \{ mutableStateOf\(com\.example\.utils\.NetworkUtils\.isInternetAvailable\(context\)\) \}', '', content)
content = re.sub(r'var updateFinishedShowGreen by remember \{ mutableStateOf\(false\) \}', '', content)

# Remove LaunchedEffect for updateFinishedShowGreen
launched_effect = r"""androidx\.compose\.runtime\.LaunchedEffect\(updateFinishedShowGreen\) \{
        if \(updateFinishedShowGreen\) \{
            kotlinx\.coroutines\.delay\(2000\)
            isUpdatingData = false
            updateFinishedShowGreen = false
        \}
    \}"""
content = re.sub(launched_effect, '', content)

# Remove BackgroundWebView
bg_webview = r"""if \(isUpdatingData .*?\) \{.*?BackgroundWebView\(.*?\)[\s\S]*?\}"""
# we need to be careful with regex here. Let's do it using string replacement.
