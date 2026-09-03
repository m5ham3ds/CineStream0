import os

repo_template = """package com.example.data.repository

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.jsoup.Jsoup
import java.net.URLEncoder
import android.util.Base64

object ScraperRepository {

    suspend fun getExtractionUrls(website: String, query: String, isMovie: Boolean, season: Int, episode: Int): List<String> = withContext(Dispatchers.IO) {
        val urls = mutableListOf<String>()
        val encodedQuery = URLEncoder.encode(query, "UTF-8")
        
        try {
            when (website) {
                "QFilm" -> {
                    val doc = Jsoup.connect("https://a.qfilm.tv/search.php?keywords=$encodedQuery").get()
                    val link = doc.select("ul.pm-ul-browse-videos li a[href*='watch.php']").first()?.attr("href")
                    if (link != null) urls.add(link)
                }
                "Animeat" -> {
                    // Not supported search directly via GET easily without workarounds
                    // fallback to webview
                }
                "Arabanime" -> {}
                "ArabSeed" -> {
                    val doc = Jsoup.connect("https://arabseed-tv.com/page/1/?s=$encodedQuery").get()
                    val link = doc.select("ul.movie__blocks__ul li a.movie__block, ul.series__ul li a").first()?.attr("href")
                    if (link != null) urls.add(link)
                }
                "ArabSeed Wine" -> {
                    val doc = Jsoup.connect("https://www.arabseed.wine/page/1/?s=$encodedQuery").get()
                    val link = doc.select("ul.movie__blocks__ul li a.movie__block, ul.series__ul li a").first()?.attr("href")
                    if (link != null) urls.add(link)
                }
                "Animerco" -> {
                    val doc = Jsoup.connect("https://det.animerco.org/?s=$encodedQuery&page=1").get()
                    val link = doc.select("div.media-section div.row div.box-5x1.media-block a.image").first()?.attr("href")
                    if (link != null) urls.add(link)
                }
                "CimaLight" -> {
                    val doc = Jsoup.connect("https://e.cimalight.co/search.php?keywords=$encodedQuery").get()
                    val link = doc.select("ul.row.pm-ul-browse-videos li a[href*='watch.php?vid=']").first()?.attr("href")
                    if (link != null) urls.add(link)
                }
                "Egy Best" -> {
                    val doc = Jsoup.connect("https://egybests.live/?s=$encodedQuery&page=1").get()
                    val link = doc.select("a.postBlock").first()?.attr("href")
                    if (link != null) urls.add(link)
                }
                "Stardima" -> {
                    val doc = Jsoup.connect("https://www.stardima.com/search?query=$encodedQuery&page=1").get()
                    val link = doc.select("div.embla__slide a[href^='/tvshow/']").first()?.attr("href")
                    if (link != null) {
                        urls.add(link)
                        // Stardima URL is relative usually
                        if (link.startsWith("/")) {
                            urls.add("https://www.stardima.com$link")
                        }
                    }
                }
                "EgyDead TV10" -> {
                    val doc = Jsoup.connect("https://tv10.egydead.live/page/1/?s=$encodedQuery").get()
                    val link = doc.select("section.main-section ul.posts-list li.movieItem a, div.pin-posts-list ul li.movieItem a").first()?.attr("href")
                    if (link != null) urls.add(link)
                }
                "Brstej" -> {
                    val doc = Jsoup.connect("https://uo.brstej.com/search.php?keywords=$encodedQuery").get()
                    val link = doc.select("ul.pm-ul-browse-videos li div.pm-video-thumb a").first()?.attr("href")
                    if (link != null) urls.add(link)
                }
                "AnimeLuxe" -> {
                    val doc = Jsoup.connect("https://vip.animeluxe.org/anime?s=$encodedQuery&page=1").get()
                    val link = doc.select("div.media-section div.row div.box-5x1.media-block a.image").first()?.attr("href")
                    if (link != null) urls.add(link)
                }
                "Watch Stardima" -> {
                    val doc = Jsoup.connect("https://watch.stardima.com/watch/search_gcse-2/?s=$encodedQuery&page=1").get()
                    val link = doc.select("article.item div.data h3 a, article.item div.poster a").first()?.attr("href")
                    if (link != null) urls.add(link)
                }
                "WitAnime" -> {
                    val doc = Jsoup.connect("https://witanime.you/?s=$encodedQuery").get()
                    val link = doc.select("div.owl-animes .anime-card-container a.overlay, div.episodes-card-container a.overlay").first()?.attr("href")
                    if (link != null) urls.add(link)
                }
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
        
        return@withContext urls
    }
}
"""

with open('app/src/main/java/com/example/data/repository/ScraperRepository.kt', 'w') as f:
    f.write(repo_template)

