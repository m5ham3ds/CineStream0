import re

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

# Update result selectors
content = content.replace("var result = document.querySelector('a.postBlock, section.main-section ul.posts-list li.movieItem a, ul.pm-ul-browse-videos li a, ul.movie__blocks__ul li a.movie__block, ul.series__ul li a, div.media-block a.image, div.owl-animes a.overlay, div.embla__slide a, .movie-card a, .anime-card a, .item-list a, article a, .post a, .thumb a');", 
"var result = document.querySelector('a.postBlock, section.main-section ul.posts-list li.movieItem a, ul.pm-ul-browse-videos li a, ul.movie__blocks__ul li a.movie__block, ul.series__ul li a, div.media-block a.image, div.owl-animes a.overlay, div.embla__slide a, .movie-card a, .anime-card a, .item-list a, article a, .post a, .thumb a, .Blocks-Area a.Block-Item, .ep-card a, .episode-card a, .box-item a, .hover-content a, .anime-list-content a');")

# Update episode selectors
content = content.replace("var epLinks = document.querySelectorAll('.episodes__list li a, .EpsList li a, .episodes-list li a, .all-episodes-list li a, .SeasonsEpisodes a, .episodelist a, .episodes a, .ListEp a, ul.episodes li a');",
"var epLinks = document.querySelectorAll('.episodes__list li a, .EpsList li a, .episodes-list li a, .all-episodes-list li a, .SeasonsEpisodes a, .episodelist a, .episodes a, .ListEp a, ul.episodes li a, .ep-card a, .episode-card a, .List-Episodes a, .list-episodes a, .EpisodesList a');")

# Update server selectors
content = content.replace("var serverList = document.querySelectorAll('ul.servers li, .server-list li, .serversList li, .watch-servers li, .list-servers li, .servers-list li, .mob-servers ul li, #servers li, .server_list li');",
"var serverList = document.querySelectorAll('ul.servers li, .server-list li, .serversList li, .watch-servers li, .list-servers li, .servers-list li, .mob-servers ul li, #servers li, .server_list li, .watch-btn, .DownloadServers li, .quality-list li, ul#episode-servers li, ul.NavTabs li, .server-list a, .watch-servers a');")

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
    f.write(content)

