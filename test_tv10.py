import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

title = "the runner"
url = f"https://tv10.egydead.live/page/1/?s={urllib.parse.quote(title)}"

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.select('a.postBlock, section.main-section ul.posts-list li.movieItem a, .movieItem a, .postBlock a,  ul.pm-ul-browse-videos li a, ul.movie__blocks__ul li a.movie__block, ul.series__ul li a, div.media-block a.image, div.owl-animes a.overlay, div.embla__slide a, .movie-card a, .anime-card a, .item-list a, article a, .post a, .thumb a, .Blocks-Area a.Block-Item, .ep-card a, .episode-card a, .box-item a, .hover-content a, .anime-list-content a, .half-post a, .Block-Item, a.header-featured-item, a.movie-item__link, .pm-video-thumb a, .lucodeia-slider-slide-item, a.overlay, a.absolute.inset-0')
    print(f"Found {len(results)} results")
    if results:
        print("First result:", results[0].get('href'))
except Exception as e:
    print(f"Error: {e}")
