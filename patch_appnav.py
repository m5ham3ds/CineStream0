import re

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'r') as f:
    content = f.read()

# For MovieDetailsScreen
old_movie_onplay = """onPlay = { title, url, server, website -> 
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
                        }"""

new_movie_onplay = """onPlay = { title, url, server, website, season, episode -> 
                            if (url?.startsWith("trailer:") == true) {
                                val trailerId = url.removePrefix("trailer:")
                                navController.navigate("trailer/$trailerId")
                            } else {
                                val encodedUrl = if (!url.isNullOrEmpty()) URLEncoder.encode(url, "UTF-8") else ""
                                val encodedTitle = URLEncoder.encode(title, "UTF-8")
                                val encodedServer = if (!server.isNullOrEmpty()) URLEncoder.encode(server, "UTF-8") else ""
                                val encodedWebsite = if (!website.isNullOrEmpty()) URLEncoder.encode(website, "UTF-8") else ""
                                navController.navigate("player?mediaId=$movieId&isMovie=true&title=$encodedTitle&url=$encodedUrl&server=$encodedServer&website=$encodedWebsite&season=$season&episode=$episode")
                            }
                        }"""

content = content.replace(old_movie_onplay, new_movie_onplay)

# For SeriesDetailsScreen
old_series_onplay = """onPlay = { title, url, server, website -> 
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
                        }"""

new_series_onplay = """onPlay = { title, url, server, website, season, episode -> 
                            if (url?.startsWith("trailer:") == true) {
                                val trailerId = url.removePrefix("trailer:")
                                navController.navigate("trailer/$trailerId")
                            } else {
                                val encodedUrl = if (!url.isNullOrEmpty()) URLEncoder.encode(url, "UTF-8") else ""
                                val encodedTitle = URLEncoder.encode(title, "UTF-8")
                                val encodedServer = if (!server.isNullOrEmpty()) URLEncoder.encode(server, "UTF-8") else ""
                                val encodedWebsite = if (!website.isNullOrEmpty()) URLEncoder.encode(website, "UTF-8") else ""
                                navController.navigate("player?mediaId=$seriesId&isMovie=false&title=$encodedTitle&url=$encodedUrl&server=$encodedServer&website=$encodedWebsite&season=$season&episode=$episode")
                            }
                        }"""

content = content.replace(old_series_onplay, new_series_onplay)

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'w') as f:
    f.write(content)
print("Patched AppNavigation.kt")

