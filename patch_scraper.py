import re

with open('app/src/main/java/com/example/data/repository/ScraperRepository.kt', 'r') as f:
    content = f.read()

new_sites = """                "Anime4up", "w1.anime4up.rest" -> {
                    val doc = connect("https://w1.anime4up.rest/?s=$encodedQuery").get()
                    val link = doc.select("div.anime-grid div.anime-card-themex div.anime-card-poster a.overlay, div.anime-card-title a").first()?.attr("href")
                    if (link == null) return@withContext null
                    if (isMovie) return@withContext link
                    val seriesDoc = connect(link).get()
                    val episodeLinks = seriesDoc.select("div.ep_num a, a.overlay")
                    for (epLink in episodeLinks) {
                        if (epLink.text().replace("\\D+".toRegex(), "") == episode.toString()) return@withContext epLink.attr("href")
                    }
                    return@withContext episodeLinks.first()?.attr("href")
                }
                "AnimeBlkom", "animeblkom.net" -> {
                    val doc = connect("https://animeblkom.net/search?query=$encodedQuery").get()
                    val link = doc.select("div.content div.poster a").first()?.attr("href")
                    if (link == null) return@withContext null
                    if (isMovie) return@withContext "https://animeblkom.net/watch/${link.substringAfterLast("/")}/1"
                    val seriesDoc = connect("https://animeblkom.net" + (if(link.startsWith("/")) link else "/$link")).get()
                    val episodeLinks = seriesDoc.select("ul.episodes-links li.episode-link a")
                    for (epLink in episodeLinks) {
                        if (epLink.text().replace("\\D+".toRegex(), "") == episode.toString()) return@withContext "https://animeblkom.net" + epLink.attr("href")
                    }
                    return@withContext "https://animeblkom.net" + (episodeLinks.first()?.attr("href") ?: "")
                }
                "TopCinema", "topcinema.io" -> {
                    val doc = connect("https://topcinema.io/search/?query=$encodedQuery").get()
                    val link = doc.select("div.Small--Box a").first()?.attr("href")
                    if (link == null) return@withContext null
                    if (isMovie) return@withContext link
                    val seriesDoc = connect(link).get()
                    val episodeLinks = seriesDoc.select("div.row a")
                    for (epLink in episodeLinks) {
                        if (epLink.selectFirst(".epnum")?.text()?.replace("\\D+".toRegex(), "") == episode.toString()) return@withContext epLink.attr("href")
                    }
                    return@withContext episodeLinks.first()?.attr("href")
                }
                "Laaroza", "laaroza.space" -> {
                    val doc = connect("https://laaroza.space/search.php?keywords=$encodedQuery").get()
                    val link = doc.select("ul.pm-ul-browse-videos li div.thumbnail a").first()?.attr("href")
                    if (link == null) return@withContext null
                    // Laaroza is mostly for movies/single episodes.
                    return@withContext link
                }
                "Almeshkah", "z1.almeshkah.net" -> {
                    val doc = connect("https://z1.almeshkah.net/search.php?keywords=$encodedQuery").get()
                    val link = doc.select("ul.pm-ul-browse-videos li div.thumbnail a").first()?.attr("href")
                    if (link == null) return@withContext null
                    if (isMovie) return@withContext link
                    val seriesDoc = connect(link).get()
                    val episodeLinks = seriesDoc.select("div.tabcontent a")
                    for (epLink in episodeLinks) {
                        if (epLink.text().replace("\\D+".toRegex(), "") == episode.toString()) return@withContext epLink.attr("href")
                    }
                    return@withContext episodeLinks.first()?.attr("href")
                }"""

# Insert the new sites right after `when (website) {`
insert_idx = content.find('when (website) {') + len('when (website) {')
content = content[:insert_idx] + '\n' + new_sites + content[insert_idx:]

with open('app/src/main/java/com/example/data/repository/ScraperRepository.kt', 'w') as f:
    f.write(content)
print("Patched ScraperRepository.kt")
