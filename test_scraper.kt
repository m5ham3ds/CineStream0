import com.example.data.repository.ScraperRepository
import kotlinx.coroutines.runBlocking

fun main() = runBlocking {
    val res = ScraperRepository.getWatchUrl("EgyDead TV10", "batman", true, 1, 1)
    println("Result: $res")
}
