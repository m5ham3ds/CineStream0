import re

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'r') as f:
    content = f.read()

old_route = 'composable("player?mediaId={mediaId}&isMovie={isMovie}&title={title}&url={url}&server={server}&website={website}") {'
new_route = 'composable("player?mediaId={mediaId}&isMovie={isMovie}&title={title}&url={url}&server={server}&website={website}&season={season}&episode={episode}") {'

content = content.replace(old_route, new_route)

old_args = """                    val decodedTitle = URLDecoder.decode(title, "UTF-8")
                    val decodedUrl = if (url.isNotEmpty()) URLDecoder.decode(url, "UTF-8") else ""
                    val decodedServer = if (server.isNotEmpty()) URLDecoder.decode(server, "UTF-8") else ""
                    val decodedWebsite = if (website.isNotEmpty()) URLDecoder.decode(website, "UTF-8") else ""
                    
                    com.example.ui.screens.player.PlayerScreen(
                        mediaId = mediaId,
                        isMovie = isMovie,
                        title = decodedTitle,
                        url = decodedUrl,
                        server = decodedServer,
                        website = decodedWebsite,
                        onBack = { navController.popBackStack() }
                    )"""
                    
new_args = """                    val seasonStr = backStackEntry.arguments?.getString("season") ?: "1"
                    val episodeStr = backStackEntry.arguments?.getString("episode") ?: "1"
                    val season = seasonStr.toIntOrNull() ?: 1
                    val episode = episodeStr.toIntOrNull() ?: 1

                    val decodedTitle = URLDecoder.decode(title, "UTF-8")
                    val decodedUrl = if (url.isNotEmpty()) URLDecoder.decode(url, "UTF-8") else ""
                    val decodedServer = if (server.isNotEmpty()) URLDecoder.decode(server, "UTF-8") else ""
                    val decodedWebsite = if (website.isNotEmpty()) URLDecoder.decode(website, "UTF-8") else ""
                    
                    com.example.ui.screens.player.PlayerScreen(
                        mediaId = mediaId,
                        isMovie = isMovie,
                        title = decodedTitle,
                        url = decodedUrl,
                        server = decodedServer,
                        website = decodedWebsite,
                        seasonNum = season,
                        episodeNum = episode,
                        onBack = { navController.popBackStack() }
                    )"""

content = content.replace(old_args, new_args)
with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'w') as f:
    f.write(content)
print("Patched AppNavigation.kt")

