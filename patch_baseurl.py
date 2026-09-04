with open('app/src/main/java/com/example/data/repository/ScraperRepository.kt', 'r') as f:
    content = f.read()

replacement = """
    fun getBaseUrl(website: String): String {
        return when(website) {
            "Anime4up", "w1.anime4up.rest" -> "https://w1.anime4up.rest/"
            "AnimeBlkom", "animeblkom.net" -> "https://animeblkom.net/"
            "TopCinema", "topcinema.io" -> "https://topcinema.io/"
            "Laaroza", "laaroza.space" -> "https://laaroza.space/"
            "Almeshkah", "z1.almeshkah.net" -> "https://z1.almeshkah.net/"
            "EgyDead TV10", "tv10.egydead.live" -> "https://tv10.egydead.live/"
            "QFilm", "a.qfilm.tv" -> "https://a.qfilm.tv/"
            "Animeat", "animeat.net" -> "https://animeat.net/"
            "Arabanime", "arabanime.net" -> "https://arabanime.net/"
            "ArabSeed", "arabseed-tv.com" -> "https://arabseed-tv.com/"
            "ArabSeed Wine", "arabseed.wine" -> "https://www.arabseed.wine/"
            "Animerco", "det.animerco.org" -> "https://det.animerco.org/"
            "CimaLight", "e.cimalight.co" -> "https://e.cimalight.co/"
            "Egy Best", "egybests.live" -> "https://egybests.live/"
            "Stardima", "stardima.com" -> "https://stardima.com/"
            "Brstej", "uo.brstej.com" -> "https://uo.brstej.com/"
            "AnimeLuxe", "vip.animeluxe.org" -> "https://vip.animeluxe.org/"
            "Watch Stardima", "watch.stardima.com" -> "https://watch.stardima.com/"
            "WitAnime", "witanime.you", "witanime.com" -> "https://witanime.you/"
            else -> ""
        }
    }

    suspend fun getWatchUrl(website: String, query: String, isMovie: Boolean, season: Int, episode: Int): String? = withContext(Dispatchers.IO) {
"""

content = content.replace("    suspend fun getWatchUrl(website: String, query: String, isMovie: Boolean, season: Int, episode: Int): String? = withContext(Dispatchers.IO) {", replacement)

with open('app/src/main/java/com/example/data/repository/ScraperRepository.kt', 'w') as f:
    f.write(content)
print("Patched getBaseUrl into ScraperRepository")
