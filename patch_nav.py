import re

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'r') as f:
    content = f.read()

# Update composable route signature
old_route = r'composable\("player\?mediaId=\{mediaId\}&isMovie=\{isMovie\}&title=\{title\}&url=\{url\}"\) \{ backStackEntry ->'
new_route = r"""composable("player?mediaId={mediaId}&isMovie={isMovie}&title={title}&url={url}&server={server}&website={website}") { backStackEntry ->"""
content = re.sub(old_route, new_route, content)

# Add extraction of server and website
extraction_patch = """
                    val title = backStackEntry.arguments?.getString("title") ?: "Unknown"
                    val url = backStackEntry.arguments?.getString("url") ?: ""
                    val server = backStackEntry.arguments?.getString("server") ?: ""
                    val website = backStackEntry.arguments?.getString("website") ?: ""
                    
                    val decodedTitle = URLDecoder.decode(title, "UTF-8")
                    val decodedUrl = if (url.isNotEmpty()) URLDecoder.decode(url, "UTF-8") else ""
                    val decodedServer = if (server.isNotEmpty()) URLDecoder.decode(server, "UTF-8") else ""
                    val decodedWebsite = if (website.isNotEmpty()) URLDecoder.decode(website, "UTF-8") else ""
"""
content = re.sub(r'val title = [^\n]+\n\s*val url = [^\n]+\n\s*val decodedTitle = [^\n]+\n\s*val decodedUrl = [^\n]+\n', extraction_patch.strip() + '\n', content)

# Update PlayerScreen call
player_screen_call = """
                    com.example.ui.screens.player.PlayerScreen(
                        mediaId = mediaId,
                        isMovie = isMovie,
                        title = decodedTitle,
                        url = decodedUrl,
                        targetServer = decodedServer,
                        website = decodedWebsite,
                        onBack = { navController.popBackStack() }
                    )
"""
content = re.sub(r'com\.example\.ui\.screens\.player\.PlayerScreen\([\s\S]*?onBack = \{ navController\.popBackStack\(\) \}\s*\)', player_screen_call.strip(), content)

# Update DetailsScreens onPlay callbacks inside AppNavigation.kt
onplay_patch = r"""
                        onPlay = { title, url, server, website -> 
                            if (url.startsWith("trailer:")) {
                                val trailerId = url.removePrefix("trailer:")
                                navController.navigate("trailer/$trailerId")
                            } else {
                                val encodedUrl = URLEncoder.encode(url, "UTF-8")
                                val encodedTitle = URLEncoder.encode(title, "UTF-8")
                                val encodedServer = URLEncoder.encode(server ?: "", "UTF-8")
                                val encodedWebsite = URLEncoder.encode(website ?: "", "UTF-8")
                                navController.navigate("player?mediaId=$movieId&isMovie=true&title=$encodedTitle&url=$encodedUrl&server=$encodedServer&website=$encodedWebsite")
                            }
                        }
"""
content = re.sub(r'onPlay = \{ title, url ->[\s\S]*?navController\.navigate\("player\?mediaId=\$movieId[^\n]*\n\s*\}\n\s*\}', onplay_patch.strip(), content)

onplay_series_patch = r"""
                        onPlay = { title, url, server, website -> 
                            if (url.startsWith("trailer:")) {
                                val trailerId = url.removePrefix("trailer:")
                                navController.navigate("trailer/$trailerId")
                            } else {
                                val encodedUrl = URLEncoder.encode(url, "UTF-8")
                                val encodedTitle = URLEncoder.encode(title, "UTF-8")
                                val encodedServer = URLEncoder.encode(server ?: "", "UTF-8")
                                val encodedWebsite = URLEncoder.encode(website ?: "", "UTF-8")
                                navController.navigate("player?mediaId=$seriesId&isMovie=false&title=$encodedTitle&url=$encodedUrl&server=$encodedServer&website=$encodedWebsite")
                            }
                        }
"""
content = re.sub(r'onPlay = \{ title, url ->[\s\S]*?navController\.navigate\("player\?mediaId=\$seriesId[^\n]*\n\s*\}\n\s*\}', onplay_series_patch.strip(), content)

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'w') as f:
    f.write(content)

