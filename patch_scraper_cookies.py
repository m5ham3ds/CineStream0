with open('app/src/main/java/com/example/data/repository/ScraperRepository.kt', 'r') as f:
    content = f.read()

import re
replacement = """
import android.webkit.CookieManager

object ScraperRepository {
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
"""

content = re.sub(r'object ScraperRepository \{.*?fun connect\(url: String\) = Jsoup\.connect\(url\).*?\.timeout\(10000\)', replacement, content, flags=re.DOTALL)

with open('app/src/main/java/com/example/data/repository/ScraperRepository.kt', 'w') as f:
    f.write(content)
print("Patched ScraperRepository to use CookieManager")
