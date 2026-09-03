package com.example.data.repository

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.jsoup.Jsoup
import java.net.URLEncoder

object ScraperRepository {

    suspend fun getWatchUrl(website: String, query: String, isMovie: Boolean, season: Int, episode: Int): String? = withContext(Dispatchers.IO) {
        val encodedQuery = URLEncoder.encode(query, "UTF-8")
        
        try {
            when (website) {
                "EgyDead TV10" -> {
                    // 1. Search
                    val doc = Jsoup.connect("https://tv10.egydead.live/page/1/?s=$encodedQuery").userAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36").header("Accept-Language", "ar,en-US;q=0.9,en;q=0.8").header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8").referrer("https://google.com/").get()
                    val link = doc.select("section.main-section ul.posts-list li.movieItem a, div.pin-posts-list ul li.movieItem a").first()?.attr("href")
                    if (link == null) return@withContext null
                    
                    if (isMovie) {
                        return@withContext link
                    } else {
                        // Navigate to series page
                        val seriesDoc = Jsoup.connect(link).userAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36").header("Accept-Language", "ar,en-US;q=0.9,en;q=0.8").header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8").referrer("https://google.com/").get()
                        
                        // Check for seasons
                        val seasonItems = seriesDoc.select("div.seasons-list ul li.movieItem a")
                        val seasonLink = if (seasonItems.size >= season) {
                            seasonItems[season - 1].attr("href")
                        } else {
                            link // Try using current page
                        }
                        
                        val episodesDoc = if (seasonLink != link) Jsoup.connect(seasonLink).userAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36").header("Accept-Language", "ar,en-US;q=0.9,en;q=0.8").header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8").referrer("https://google.com/").get() else seriesDoc
                        
                        // Find episode
                        val episodeLinks = episodesDoc.select("div.EpsList li a")
                        for (epLink in episodeLinks) {
                            val epNumStr = epLink.text().replace("\\D+".toRegex(), "")
                            if (epNumStr.isNotEmpty() && epNumStr.toIntOrNull() == episode) {
                                return@withContext epLink.attr("href")
                            }
                        }
                        
                        // Fallback: first episode
                        return@withContext episodeLinks.first()?.attr("href")
                    }
                }
                "QFilm" -> {
                    val doc = Jsoup.connect("https://a.qfilm.tv/search.php?keywords=$encodedQuery").userAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36").header("Accept-Language", "ar,en-US;q=0.9,en;q=0.8").header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8").referrer("https://google.com/").get()
                    return@withContext doc.select("ul.pm-ul-browse-videos li a[href*='watch.php']").first()?.attr("href")
                }
                "Animeat" -> {
                    // SPA, fallback to returning base url + query for webview search
                    return@withContext "https://animeat.net"
                }
                "Arabanime" -> {
                    return@withContext "https://www.arabanime.net"
                }
                "ArabSeed" -> {
                    val doc = Jsoup.connect("https://arabseed-tv.com/page/1/?s=$encodedQuery").userAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36").header("Accept-Language", "ar,en-US;q=0.9,en;q=0.8").header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8").referrer("https://google.com/").get()
                    val link = doc.select("ul.movie__blocks__ul li a.movie__block, ul.series__ul li a").first()?.attr("href")
                    if (link == null) return@withContext null
                    
                    if (isMovie) return@withContext link
                    
                    val seriesDoc = Jsoup.connect(link).userAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36").header("Accept-Language", "ar,en-US;q=0.9,en;q=0.8").header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8").referrer("https://google.com/").get()
                    val episodeLinks = seriesDoc.select("ul.episodes__list li a, ul.episodes__blocks__holder a.episode__item")
                    for (ep in episodeLinks) {
                        val numText = ep.select("div.epi__num b, div.episode__title em").text()
                        if (numText == episode.toString()) {
                            return@withContext ep.attr("href")
                        }
                    }
                    return@withContext episodeLinks.first()?.attr("href")
                }
                "ArabSeed Wine" -> {
                    val doc = Jsoup.connect("https://www.arabseed.wine/page/1/?s=$encodedQuery").userAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36").header("Accept-Language", "ar,en-US;q=0.9,en;q=0.8").header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8").referrer("https://google.com/").get()
                    val link = doc.select("ul.movie__blocks__ul li a.movie__block, ul.series__ul li a").first()?.attr("href")
                    if (link == null) return@withContext null
                    
                    if (isMovie) return@withContext link
                    
                    val seriesDoc = Jsoup.connect(link).userAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36").header("Accept-Language", "ar,en-US;q=0.9,en;q=0.8").header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8").referrer("https://google.com/").get()
                    val episodeLinks = seriesDoc.select("ul.episodes__list li a, ul.episodes__blocks__holder a.episode__item")
                    for (ep in episodeLinks) {
                        val numText = ep.select("div.epi__num b, div.episode__title em").text()
                        if (numText == episode.toString()) {
                            return@withContext ep.attr("href")
                        }
                    }
                    return@withContext episodeLinks.first()?.attr("href")
                }
                "Animerco" -> {
                    val doc = Jsoup.connect("https://det.animerco.org/?s=$encodedQuery&page=1").userAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36").header("Accept-Language", "ar,en-US;q=0.9,en;q=0.8").header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8").referrer("https://google.com/").get()
                    val link = doc.select("div.media-section div.row div.box-5x1.media-block a.image").first()?.attr("href")
                    if (link == null) return@withContext null
                    
                    if (isMovie) return@withContext link
                    
                    val seriesDoc = Jsoup.connect(link).userAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36").header("Accept-Language", "ar,en-US;q=0.9,en;q=0.8").header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8").referrer("https://google.com/").get()
                    val episodeLinks = seriesDoc.select("ul.episodes-list li a")
                    for (ep in episodeLinks) {
                        val numText = ep.text().replace("\\D+".toRegex(), "")
                        if (numText == episode.toString()) {
                            return@withContext ep.attr("href")
                        }
                    }
                    return@withContext episodeLinks.first()?.attr("href")
                }
                "CimaLight" -> {
                    val doc = Jsoup.connect("https://e.cimalight.co/search.php?keywords=$encodedQuery").userAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36").header("Accept-Language", "ar,en-US;q=0.9,en;q=0.8").header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8").referrer("https://google.com/").get()
                    val link = doc.select("ul.row.pm-ul-browse-videos li a[href*='watch.php?vid=']").first()?.attr("href")
                    if (link == null) return@withContext null
                    // CimaLight handles series on the same page with seasons
                    return@withContext link
                }
                "Egy Best" -> {
                    val doc = Jsoup.connect("https://egybests.live/?s=$encodedQuery&page=1").userAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36").header("Accept-Language", "ar,en-US;q=0.9,en;q=0.8").header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8").referrer("https://google.com/").get()
                    val link = doc.select("a.postBlock").first()?.attr("href")
                    if (link == null) return@withContext null
                    
                    if (isMovie) return@withContext link
                    
                    val seriesDoc = Jsoup.connect(link).userAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36").header("Accept-Language", "ar,en-US;q=0.9,en;q=0.8").header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8").referrer("https://google.com/").get()
                    val episodeLinks = seriesDoc.select("div.all-episodes a, div.EpisodesList a")
                    for (ep in episodeLinks) {
                        val numText = ep.text().filter { it.isDigit() }
                        if (numText == episode.toString()) return@withContext ep.attr("href")
                    }
                    return@withContext episodeLinks.first()?.attr("href")
                }
                "Stardima" -> {
                    val doc = Jsoup.connect("https://www.stardima.com/search?query=$encodedQuery&page=1").userAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36").header("Accept-Language", "ar,en-US;q=0.9,en;q=0.8").header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8").referrer("https://google.com/").get()
                    val link = doc.select("div.embla__slide a[href^='/tvshow/']").first()?.attr("href")
                    if (link == null) return@withContext null
                    
                    val fullLink = if (link.startsWith("/")) "https://www.stardima.com$link" else link
                    if (isMovie) return@withContext fullLink
                    
                    val seriesDoc = Jsoup.connect(fullLink).userAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36").header("Accept-Language", "ar,en-US;q=0.9,en;q=0.8").header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8").referrer("https://google.com/").get()
                    val episodeLinks = seriesDoc.select("ul#episodes-list-container li.episode-list-item a")
                    for (ep in episodeLinks) {
                        if (ep.text().contains(episode.toString())) return@withContext ep.attr("href")
                    }
                    return@withContext episodeLinks.first()?.attr("href")
                }
                "Brstej" -> {
                    val doc = Jsoup.connect("https://uo.brstej.com/search.php?keywords=$encodedQuery").userAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36").header("Accept-Language", "ar,en-US;q=0.9,en;q=0.8").header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8").referrer("https://google.com/").get()
                    val link = doc.select("ul.pm-ul-browse-videos li div.pm-video-thumb a").first()?.attr("href")
                    if (link == null) return@withContext null
                    
                    if (isMovie) return@withContext link
                    
                    val seriesDoc = Jsoup.connect(link).userAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36").header("Accept-Language", "ar,en-US;q=0.9,en;q=0.8").header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8").referrer("https://google.com/").get()
                    val episodeLinks = seriesDoc.select("div.SeasonsEpisodes a")
                    for (ep in episodeLinks) {
                        if (ep.select("em").text() == episode.toString()) return@withContext ep.attr("href")
                    }
                    return@withContext episodeLinks.first()?.attr("href")
                }
                "AnimeLuxe" -> {
                    val doc = Jsoup.connect("https://vip.animeluxe.org/anime?s=$encodedQuery&page=1").userAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36").header("Accept-Language", "ar,en-US;q=0.9,en;q=0.8").header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8").referrer("https://google.com/").get()
                    val link = doc.select("div.media-section div.row div.box-5x1.media-block a.image").first()?.attr("href")
                    if (link == null) return@withContext null
                    
                    if (isMovie) return@withContext link
                    
                    val seriesDoc = Jsoup.connect(link).userAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36").header("Accept-Language", "ar,en-US;q=0.9,en;q=0.8").header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8").referrer("https://google.com/").get()
                    val episodeLinks = seriesDoc.select("ul.episodes-lists li a[href*='/episodes/']")
                    for (ep in episodeLinks) {
                        val numText = (ep.selectFirst("h3")?.text() ?: ep.ownText()).replace("\\D+".toRegex(), "")
                        if (numText == episode.toString()) return@withContext ep.attr("href")
                    }
                    return@withContext episodeLinks.first()?.attr("href")
                }
                "Watch Stardima" -> {
                    val doc = Jsoup.connect("https://watch.stardima.com/watch/search_gcse-2/?s=$encodedQuery&page=1").userAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36").header("Accept-Language", "ar,en-US;q=0.9,en;q=0.8").header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8").referrer("https://google.com/").get()
                    val link = doc.select("article.item div.data h3 a, article.item div.poster a").first()?.attr("href")
                    if (link == null) return@withContext null
                    
                    if (isMovie) return@withContext link
                    
                    val seriesDoc = Jsoup.connect(link).userAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36").header("Accept-Language", "ar,en-US;q=0.9,en;q=0.8").header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8").referrer("https://google.com/").get()
                    val episodeLinks = seriesDoc.select("ul.all-episodes-list li.episode-list-item a")
                    for (ep in episodeLinks) {
                        if (ep.text().contains(episode.toString())) return@withContext ep.attr("href")
                    }
                    return@withContext episodeLinks.first()?.attr("href")
                }
                "WitAnime" -> {
                    val doc = Jsoup.connect("https://witanime.you/?s=$encodedQuery").userAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36").header("Accept-Language", "ar,en-US;q=0.9,en;q=0.8").header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8").referrer("https://google.com/").get()
                    val link = doc.select("div.owl-animes .anime-card-container a.overlay, div.episodes-card-container a.overlay").first()?.attr("href")
                    if (link == null) return@withContext null
                    
                    if (isMovie) return@withContext link
                    
                    val seriesDoc = Jsoup.connect(link).userAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36").header("Accept-Language", "ar,en-US;q=0.9,en;q=0.8").header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8").referrer("https://google.com/").get()
                    val episodeLinks = seriesDoc.select("ul.all-episodes-list li a")
                    for (ep in episodeLinks) {
                        val numText = ep.text().replace("\\D+".toRegex(), "")
                        if (numText == episode.toString()) return@withContext ep.attr("href")
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
