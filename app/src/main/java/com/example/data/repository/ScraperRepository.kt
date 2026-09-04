package com.example.data.repository

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.jsoup.Jsoup
import java.net.URLEncoder


import android.webkit.CookieManager

object ScraperRepository {

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

        val encodedQuery = URLEncoder.encode(query, "UTF-8")
        
        fun connect(url: String): org.jsoup.Connection {
            var conn = Jsoup.connect(url)
                .userAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
                .header("Accept-Language", "ar,en-US;q=0.9,en;q=0.8")
                .referrer("https://google.com/")
                .timeout(10000)
            
            val cookies = CookieManager.getInstance().getCookie(url)
            if (cookies != null) {
                val cookieMap = mutableMapOf<String, String>()
                val pairs = cookies.split(";")
                for (pair in pairs) {
                    val parts = pair.trim().split("=", limit = 2)
                    if (parts.size == 2) {
                        cookieMap[parts[0]] = parts[1]
                    }
                }
                conn = conn.cookies(cookieMap)
            }
            return conn
        }

            
        try {
            when (website) {
                "Anime4up", "w1.anime4up.rest" -> {
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
                }
                "EgyDead TV10", "tv10.egydead.live" -> {
                    val doc = connect("https://tv10.egydead.live/page/1/?s=$encodedQuery").get()
                    val link = doc.select("section.main-section ul.posts-list li.movieItem a, div.pin-posts-list ul li.movieItem a").first()?.attr("href")
                    if (link == null) return@withContext null
                    if (isMovie) return@withContext link
                    val seriesDoc = connect(link).get()
                    val seasonItems = seriesDoc.select("div.seasons-list ul li.movieItem a")
                    val seasonLink = if (seasonItems.size >= season) seasonItems[season - 1].attr("href") else link
                    val episodesDoc = if (seasonLink != link) connect(seasonLink).get() else seriesDoc
                    val episodeLinks = episodesDoc.select("div.EpsList li a")
                    for (epLink in episodeLinks) {
                        if (epLink.text().replace("\\D+".toRegex(), "") == episode.toString()) return@withContext epLink.attr("href")
                    }
                    return@withContext episodeLinks.first()?.attr("href")
                }
                "QFilm", "a.qfilm.tv" -> {
                    val doc = connect("https://a.qfilm.tv/search.php?keywords=$encodedQuery").get()
                    return@withContext doc.select("ul.pm-ul-browse-videos li a[href*='watch.php']").first()?.attr("href")
                }
                "Animeat", "animeat.net" -> {
                    return@withContext "https://animeat.net/?search=$encodedQuery"
                }
                "Arabanime", "arabanime.net" -> {
                    return@withContext "https://www.arabanime.net/?s=$encodedQuery"
                }
                "ArabSeed", "arabseed-tv.com" -> {
                    val doc = connect("https://arabseed-tv.com/page/1/?s=$encodedQuery").get()
                    val link = doc.select("ul.movie__blocks__ul li a.movie__block, ul.series__ul li a").first()?.attr("href")
                    if (link == null) return@withContext null
                    if (isMovie) return@withContext link
                    val seriesDoc = connect(link).get()
                    val episodeLinks = seriesDoc.select("ul.episodes__list li a, ul.episodes__blocks__holder a.episode__item")
                    for (ep in episodeLinks) {
                        if (ep.select("div.epi__num b, div.episode__title em").text() == episode.toString()) return@withContext ep.attr("href")
                    }
                    return@withContext episodeLinks.first()?.attr("href")
                }
                "ArabSeed Wine", "arabseed.wine" -> {
                    val doc = connect("https://www.arabseed.wine/page/1/?s=$encodedQuery").get()
                    val link = doc.select("ul.movie__blocks__ul li a.movie__block, ul.series__ul li a").first()?.attr("href")
                    if (link == null) return@withContext null
                    if (isMovie) return@withContext link
                    val seriesDoc = connect(link).get()
                    val episodeLinks = seriesDoc.select("ul.episodes__list li a, ul.episodes__blocks__holder a.episode__item")
                    for (ep in episodeLinks) {
                        if (ep.select("div.epi__num b, div.episode__title em").text() == episode.toString()) return@withContext ep.attr("href")
                    }
                    return@withContext episodeLinks.first()?.attr("href")
                }
                "Animerco", "det.animerco.org" -> {
                    val doc = connect("https://det.animerco.org/?s=$encodedQuery&page=1").get()
                    val link = doc.select("div.media-section div.row div.box-5x1.media-block a.image").first()?.attr("href")
                    if (link == null) return@withContext null
                    if (isMovie) return@withContext link
                    val seriesDoc = connect(link).get()
                    val episodeLinks = seriesDoc.select("ul.episodes-list li a")
                    for (ep in episodeLinks) {
                        if (ep.text().replace("\\D+".toRegex(), "") == episode.toString()) return@withContext ep.attr("href")
                    }
                    return@withContext episodeLinks.first()?.attr("href")
                }
                "CimaLight", "e.cimalight.co" -> {
                    val doc = connect("https://e.cimalight.co/search.php?keywords=$encodedQuery").get()
                    return@withContext doc.select("ul.row.pm-ul-browse-videos li a[href*='watch.php?vid=']").first()?.attr("href")
                }
                "Egy Best", "egybests.live" -> {
                    val doc = connect("https://egybests.live/?s=$encodedQuery&page=1").get()
                    val link = doc.select("a.postBlock").first()?.attr("href")
                    if (link == null) return@withContext null
                    if (isMovie) return@withContext link
                    val seriesDoc = connect(link).get()
                    val episodeLinks = seriesDoc.select("div.all-episodes a, div.EpisodesList a")
                    for (ep in episodeLinks) {
                        if (ep.text().filter { it.isDigit() } == episode.toString()) return@withContext ep.attr("href")
                    }
                    return@withContext episodeLinks.first()?.attr("href")
                }
                "Stardima", "stardima.com" -> {
                    val doc = connect("https://www.stardima.com/search?query=$encodedQuery&page=1").get()
                    val link = doc.select("div.embla__slide a[href^='/tvshow/']").first()?.attr("href")
                    if (link == null) return@withContext null
                    val fullLink = if (link.startsWith("/")) "https://www.stardima.com$link" else link
                    if (isMovie) return@withContext fullLink
                    val seriesDoc = connect(fullLink).get()
                    val episodeLinks = seriesDoc.select("ul#episodes-list-container li.episode-list-item a")
                    for (ep in episodeLinks) {
                        if (ep.text().contains(episode.toString())) return@withContext ep.attr("href")
                    }
                    return@withContext episodeLinks.first()?.attr("href")
                }
                "Brstej", "uo.brstej.com" -> {
                    val doc = connect("https://uo.brstej.com/search.php?keywords=$encodedQuery").get()
                    val link = doc.select("ul.pm-ul-browse-videos li div.pm-video-thumb a").first()?.attr("href")
                    if (link == null) return@withContext null
                    if (isMovie) return@withContext link
                    val seriesDoc = connect(link).get()
                    val episodeLinks = seriesDoc.select("div.SeasonsEpisodes a")
                    for (ep in episodeLinks) {
                        if (ep.select("em").text() == episode.toString()) return@withContext ep.attr("href")
                    }
                    return@withContext episodeLinks.first()?.attr("href")
                }
                "AnimeLuxe", "vip.animeluxe.org" -> {
                    val doc = connect("https://vip.animeluxe.org/anime?s=$encodedQuery&page=1").get()
                    val link = doc.select("div.media-section div.row div.box-5x1.media-block a.image").first()?.attr("href")
                    if (link == null) return@withContext null
                    if (isMovie) return@withContext link
                    val seriesDoc = connect(link).get()
                    val episodeLinks = seriesDoc.select("ul.episodes-lists li a[href*='/episodes/']")
                    for (ep in episodeLinks) {
                        val numText = (ep.selectFirst("h3")?.text() ?: ep.ownText()).replace("\\D+".toRegex(), "")
                        if (numText == episode.toString()) return@withContext ep.attr("href")
                    }
                    return@withContext episodeLinks.first()?.attr("href")
                }
                "Watch Stardima", "watch.stardima.com" -> {
                    val doc = connect("https://watch.stardima.com/watch/search_gcse-2/?s=$encodedQuery&page=1").get()
                    val link = doc.select("article.item div.data h3 a, article.item div.poster a").first()?.attr("href")
                    if (link == null) return@withContext null
                    if (isMovie) return@withContext link
                    val seriesDoc = connect(link).get()
                    val episodeLinks = seriesDoc.select("ul.all-episodes-list li.episode-list-item a")
                    for (ep in episodeLinks) {
                        if (ep.text().contains(episode.toString())) return@withContext ep.attr("href")
                    }
                    return@withContext episodeLinks.first()?.attr("href")
                }
                "WitAnime", "witanime.you", "witanime.com" -> {
                    val doc = connect("https://witanime.com/?search_param=animes&s=$encodedQuery").get()
                    val link = doc.select("div.owl-animes .anime-card-container a.overlay, div.episodes-card-container a.overlay").first()?.attr("href")
                    if (link == null) return@withContext null
                    if (isMovie) return@withContext link
                    val seriesDoc = connect(link).get()
                    val episodeLinks = seriesDoc.select("ul.all-episodes-list li a")
                    for (ep in episodeLinks) {
                        if (ep.text().replace("\\D+".toRegex(), "") == episode.toString()) return@withContext ep.attr("href")
                    }
                    return@withContext episodeLinks.first()?.attr("href")
                }
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
        return@withContext null
    }
}
