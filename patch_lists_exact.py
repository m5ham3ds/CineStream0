import re

files_to_patch = [
    'app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt',
    'app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt'
]

# EXACT user request:
# Movies: tv10 (EgyDead TV10), qfilm (QFilm), topcinema (TopCinema)
# Series: topcinema (TopCinema), tv10 (EgyDead TV10), egybests (Egy Best), arabseed.wine (ArabSeed Wine)
# Anime: witanime (WitAnime), anime4up (Anime4up), animeblkom (AnimeBlkom)

anime_replacement = 'val animeSites = listOf("WitAnime", "Anime4up", "AnimeBlkom")'
movie_replacement = 'val movieSites = listOf("EgyDead TV10", "QFilm", "TopCinema")'
series_replacement = 'val seriesSites = listOf("TopCinema", "EgyDead TV10", "Egy Best", "ArabSeed Wine")'

for filepath in files_to_patch:
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        content = re.sub(r'val animeSites = listOf\(.*?\)', anime_replacement, content)
        content = re.sub(r'val movieSites = listOf\(.*?\)', movie_replacement, content)
        content = re.sub(r'val seriesSites = listOf\(.*?\)', series_replacement, content)
        
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Patched {filepath} to exact requested short lists")
    except FileNotFoundError:
        print(f"Not found: {filepath}")
