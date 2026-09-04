import re

files_to_patch = [
    'app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt',
    'app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt'
]

anime_replacement = 'val animeSites = listOf("WitAnime", "Anime4up", "AnimeBlkom", "Animeat", "Arabanime", "AnimeLuxe")'
movie_replacement = 'val movieSites = listOf("EgyDead TV10", "QFilm", "TopCinema", "Laaroza", "Almeshkah", "ArabSeed", "ArabSeed Wine", "CimaLight", "Egy Best", "Stardima", "Brstej")'
series_replacement = 'val seriesSites = listOf("TopCinema", "EgyDead TV10", "Egy Best", "ArabSeed Wine", "Almeshkah", "QFilm", "ArabSeed", "CimaLight", "Stardima", "Brstej")'


for filepath in files_to_patch:
    with open(filepath, 'r') as f:
        content = f.read()
    
    content = re.sub(r'val animeSites = listOf\(.*?\)', anime_replacement, content)
    content = re.sub(r'val movieSites = listOf\(.*?\)', movie_replacement, content)
    content = re.sub(r'val seriesSites = listOf\(.*?\)', series_replacement, content)
    
    with open(filepath, 'w') as f:
        f.write(content)

print("Patched lists in both files")
