import re

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

start_idx = content.find("// 1. Search Results -> Click item")
end_idx = content.find("// 2. Series Page -> Click Season/Episode")

if start_idx != -1 and end_idx != -1:
    new_search = """// 1. Search Results -> Click item
                                        if (loc.includes('?s=') || loc.includes('search') || loc.includes('query=')) {
                                            var results = document.querySelectorAll('a.postBlock, section.main-section ul.posts-list li.movieItem a, .movieItem a, .postBlock a,  ul.pm-ul-browse-videos li a, ul.movie__blocks__ul li a.movie__block, ul.series__ul li a, div.media-block a.image, div.owl-animes a.overlay, div.embla__slide a, .movie-card a, .anime-card a, .item-list a, article a, .post a, .thumb a, .Blocks-Area a.Block-Item, .ep-card a, .episode-card a, .box-item a, .hover-content a, .anime-list-content a, .half-post a, .Block-Item, a.header-featured-item, a.movie-item__link, .pm-video-thumb a, .lucodeia-slider-slide-item, a.overlay, a.absolute.inset-0');
                                            if (results && results.length > 0) {
                                                clearInterval(intervalId);
                                                var targetResult = results[0];
                                                if (!isMovie) {
                                                    var e = epNum.toString();
                                                    for (var i=0; i<results.length; i++) {
                                                        var txt = decodeURIComponent(results[i].href || "").toLowerCase() + " " + (results[i].innerText || results[i].title || results[i].getAttribute('title') || "").toLowerCase();
                                                        if (txt.includes('حلقة ' + e) || txt.includes('حلقه ' + e) || txt.includes('-' + e + '-') || txt.includes('ep ' + e) || txt.includes('episode ' + e) || txt.includes(' ' + e + ' ')) {
                                                            targetResult = results[i];
                                                            break;
                                                        }
                                                    }
                                                }
                                                window.location.href = targetResult.href;
                                                return;
                                            }
                                        }
                                        
                                        """
    content = content[:start_idx] + new_search + content[end_idx:]
    with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
        f.write(content)
    print("Patched search result logic in ServerSelectionDialog.kt")
else:
    print("Could not find start or end index.")
