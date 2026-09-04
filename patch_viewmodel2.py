import re

with open('app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt', 'r') as f:
    content = f.read()

old_lists = """        val animeSites = listOf("WitAnime", "Anime4up", "AnimeBlkom", "Animeat", "Arabanime", "AnimeLuxe")
        val movieSites = listOf("EgyDead TV10", "QFilm", "TopCinema", "ArabSeed", "ArabSeed Wine", "CimaLight", "Egy Best", "Stardima", "Brstej")
        val seriesSites = listOf("TopCinema", "EgyDead TV10", "Egy Best", "ArabSeed Wine", "QFilm", "ArabSeed", "CimaLight", "Stardima", "Brstej")"""

new_lists = """        val animeSites = listOf("WitAnime", "Anime4up", "AnimeBlkom", "Animeat", "Arabanime", "AnimeLuxe")
        val movieSites = listOf("EgyDead TV10", "QFilm", "TopCinema", "Laaroza", "Almeshkah", "ArabSeed", "ArabSeed Wine", "CimaLight", "Egy Best", "Stardima", "Brstej")
        val seriesSites = listOf("TopCinema", "EgyDead TV10", "Egy Best", "ArabSeed Wine", "Almeshkah", "QFilm", "ArabSeed", "CimaLight", "Stardima", "Brstej")"""

content = content.replace(old_lists, new_lists)

with open('app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt', 'w') as f:
    f.write(content)
print("Patched PlayerViewModel.kt sites")
