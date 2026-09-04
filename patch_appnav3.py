with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'r') as f:
    content = f.read()

# Replace the states
content = content.replace("var isUpdatingData by remember { mutableStateOf(com.example.utils.NetworkUtils.isInternetAvailable(context)) }", "")
content = content.replace("var updateFinishedShowGreen by remember { mutableStateOf(false) }", "")

# Replace the LaunchedEffect block
old_effect = """    androidx.compose.runtime.LaunchedEffect(updateFinishedShowGreen) {
        if (updateFinishedShowGreen) {
            kotlinx.coroutines.delay(2000)
            isUpdatingData = false
            updateFinishedShowGreen = false
        }
    }"""
content = content.replace(old_effect, "")

# Remove extensionUrls array
import re
ext_urls = re.compile(r'val extensionUrls = remember \{\s*listOf\([\s\S]*?\)\s*\}')
content = ext_urls.sub('', content)

# Remove BackgroundWebView
bg_webview = re.compile(r'if \(isUpdatingData && currentRoute != Screen\.Splash\.route && currentRoute != Screen\.Auth\.route && currentRoute != Screen\.Onboarding\.route && !updateFinishedShowGreen\) \{\s*SiteVerificationManager\.isVerificationStarted = true\s*BackgroundWebView\([\s\S]*?\)\s*\}')
content = bg_webview.sub('', content)

# Remove Top Bar Banner
top_banner = re.compile(r'if \(\(isUpdatingData \|\| updateFinishedShowGreen\) && currentRoute != Screen\.Splash\.route && currentRoute != Screen\.Auth\.route && currentRoute != Screen\.Onboarding\.route\) \{[\s\S]*?\}[\s\S]*?\}[\s\S]*?\}[\s\S]*?\},')
# Actually, the banner is at the end of the topBar block
# Let's just find the exact code block for the red/green banner
banner_str = """                if ((isUpdatingData || updateFinishedShowGreen) && currentRoute != Screen.Splash.route && currentRoute != Screen.Auth.route && currentRoute != Screen.Onboarding.route) {
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .background(if (updateFinishedShowGreen) Color(0xFF4CAF50) else Color(0xFFE50914))
                                .padding(vertical = 4.dp),
                            contentAlignment = Alignment.Center
                        ) {
                            Text(
                                text = if (updateFinishedShowGreen) "تم التحقق من جميع المواقع بنجاح" else stringResource(R.string.updating_data),
                                color = MaterialTheme.colorScheme.onBackground,
                                fontSize = 12.sp,
                                fontWeight = FontWeight.Bold
                            )
                        }
                    }"""

content = content.replace(banner_str, "")

# Clean up any remaining references
content = content.replace("isUpdatingData && ", "")
content = content.replace("|| updateFinishedShowGreen", "")

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'w') as f:
    f.write(content)
print("Removed general site checking banner")

