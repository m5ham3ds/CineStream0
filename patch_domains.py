import re

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'val animeSites = listOf("witanime.you", "animeat.net", "vip.animeluxe.org", "det.animerco.org", "stardima.com", "watch.stardima.com")',
    'val animeSites = listOf("witanime.cyou", "anime4up.cam", "animeat.net", "vip.animeluxe.org", "det.animerco.org", "stardima.com", "watch.stardima.com")'
)

content = content.replace(
    'val movieSites = listOf("tv10.egydead.live", "a.qfilm.tv", "arabseed.wine", "arabseed-tv.com", "egybests.live", "e.cimalight.co", "uo.brstej.com")',
    'val movieSites = listOf("egydead.plus", "arabseed.show", "qfilm.tv", "cima4u.skin", "faselhd.wtf", "tv10.egydead.live", "a.qfilm.tv", "arabseed.wine", "egybests.live")'
)

# Replace the specific URL generators
search_url_replacement = """    val searchUrl = when {
        currentSiteName.contains("egydead") -> "https://$currentSiteName/page/1/?s=$encodedTitle"
        currentSiteName.contains("qfilm") -> "https://$currentSiteName/search.php?keywords=$encodedTitle"
        currentSiteName.contains("arabseed") -> "https://$currentSiteName/page/1/?s=$encodedTitle"
        currentSiteName.contains("stardima") -> "https://$currentSiteName/search?query=$encodedTitle&page=1"
        currentSiteName.contains("witanime") -> "https://$currentSiteName/?search_param=animes&s=$encodedTitle"
        currentSiteName.contains("anime4up") -> "https://$currentSiteName/?search_param=animes&s=$encodedTitle"
        currentSiteName.contains("cima4u") -> "https://$currentSiteName/search.php?keywords=$encodedTitle"
        currentSiteName.contains("faselhd") -> "https://$currentSiteName/?s=$encodedTitle"
        currentSiteName == "animeat.net" -> "https://animeat.net/?search=$encodedTitle"
        currentSiteName == "det.animerco.org" -> "https://det.animerco.org/?s=$encodedTitle&page=1"
        currentSiteName == "e.cimalight.co" -> "https://e.cimalight.co/search.php?keywords=$encodedTitle"
        currentSiteName == "egybests.live" -> "https://egybests.live/?s=$encodedTitle&page=1"
        currentSiteName == "uo.brstej.com" -> "https://uo.brstej.com/search.php?keywords=$encodedTitle"
        currentSiteName == "vip.animeluxe.org" -> "https://vip.animeluxe.org/anime?s=$encodedTitle&page=1"
        else -> "https://$currentSiteName/?s=$encodedTitle"
    }"""

old_search_url = """    val searchUrl = when (currentSiteName) {
        "tv10.egydead.live" -> "https://tv10.egydead.live/page/1/?s=$encodedTitle"
        "a.qfilm.tv" -> "https://a.qfilm.tv/search.php?keywords=$encodedTitle"
        "animeat.net" -> "https://animeat.net/?search=$encodedTitle"
        "arabseed-tv.com" -> "https://arabseed-tv.com/page/1/?s=$encodedTitle"
        "arabseed.wine" -> "https://www.arabseed.wine/page/1/?s=$encodedTitle"
        "det.animerco.org" -> "https://det.animerco.org/?s=$encodedTitle&page=1"
        "e.cimalight.co" -> "https://e.cimalight.co/search.php?keywords=$encodedTitle"
        "egybests.live" -> "https://egybests.live/?s=$encodedTitle&page=1"
        "stardima.com" -> "https://www.stardima.com/search?query=$encodedTitle&page=1"
        "uo.brstej.com" -> "https://uo.brstej.com/search.php?keywords=$encodedTitle"
        "vip.animeluxe.org" -> "https://vip.animeluxe.org/anime?s=$encodedTitle&page=1"
        "watch.stardima.com" -> "https://watch.stardima.com/watch/search_gcse-2/?s=$encodedTitle&page=1"
        "witanime.you" -> "https://witanime.com/?search_param=animes&s=$encodedTitle"
        else -> "https://$currentSiteName/?s=$encodedTitle"
    }"""

content = content.replace(old_search_url, search_url_replacement)

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
    f.write(content)
