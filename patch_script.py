with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

replacement = """                                (function() {
                                    var isMovie = $isMovieStr;
                                    var season = $season;
                                    var epNum = $episode;
                                    var loc = window.location.href.toLowerCase();
                                    
                                    var intervalId = setInterval(function() {
                                        // Bypass Cloudflare
                                        var cf = document.querySelector('.cf-turnstile-wrapper, #challenge-stage, input[type="checkbox"], #challenge-form, .mark-as-human');
                                        if (cf) { cf.click(); return; }
                                        
                                        var isJustAMoment = document.title.includes('Just a moment') || document.title.includes('Cloudflare') || document.title.includes('Attention Required');
                                        var isCloudflare = cf || isJustAMoment;

                                        // 1. Search Results -> Click item
                                        if (loc.includes('?s=') || loc.includes('search') || loc.includes('query=')) {
                                            var result = document.querySelector('a.postBlock, section.main-section ul.posts-list li.movieItem a, ul.pm-ul-browse-videos li a, ul.movie__blocks__ul li a.movie__block, ul.series__ul li a, div.media-block a.image, div.owl-animes a.overlay, div.embla__slide a, .movie-card a, .anime-card a, .item-list a, article a, .post a, .thumb a');
                                            if (result) { 
                                                clearInterval(intervalId);
                                                window.location.href = result.href; 
                                                return; 
                                            }
                                        }
                                        
                                        // 2. Series Page -> Click Season/Episode
                                        if (!isMovie && !loc.includes('episode') && !loc.includes('ep-') && !loc.includes('watch') && !loc.includes('episodes')) {
                                            var epLinks = document.querySelectorAll('.episodes__list li a, .EpsList li a, .episodes-list li a, .all-episodes-list li a, .SeasonsEpisodes a, .episodelist a, .episodes a, .ListEp a, ul.episodes li a');
                                            if (epLinks.length > 0) {
                                                clearInterval(intervalId);
                                                for(var i=0; i<epLinks.length; i++) {
                                                    var text = epLinks[i].innerText || "";
                                                    if(text.includes(epNum.toString())) {
                                                        window.location.href = epLinks[i].href;
                                                        return;
                                                    }
                                                }
                                                // Fallback to first episode
                                                window.location.href = epLinks[0].href;
                                                return;
                                            }
                                        }
                                        
                                        // 3. Extract Servers on Watch Page
                                        var serverList = document.querySelectorAll('ul.servers li, .server-list li, .serversList li, .watch-servers li, .list-servers li, .servers-list li, .mob-servers ul li, #servers li, .server_list li');
                                        if (serverList && serverList.length > 0) {
                                            var serverNames = [];
                                            for(var i=0; i<serverList.length; i++) {
                                                var serverName = serverList[i].innerText.trim();
                                                if (serverName) serverNames.push(serverName);
                                            }
                                            if (serverNames.length > 0) {
                                                clearInterval(intervalId);
                                                if (typeof AndroidBridge !== 'undefined') {
                                                    AndroidBridge.sendServers(serverNames.join(','), window.location.href);
                                                }
                                                return;
                                            }
                                        }
                                        
                                        // 4. Fast Fail (if no search results or servers found after loading)
                                        if (!isCloudflare && document.readyState === 'complete') {
                                            window._failCount = (window._failCount || 0) + 1;
                                            if (window._failCount >= 4) {
                                                clearInterval(intervalId);
                                                if (typeof AndroidBridge !== 'undefined') AndroidBridge.sendFailed();
                                            }
                                        }
                                    }, 1500);
                                })();"""

content = content.replace("""                                (function() {
                                    var isMovie = $isMovieStr;
                                    var season = $season;
                                    var epNum = $episode;
                                    var loc = window.location.href.toLowerCase();
                                    
                                    setInterval(function() {
                                        // Bypass Cloudflare
                                        var cf = document.querySelector('.cf-turnstile-wrapper, #challenge-stage, input[type="checkbox"], #challenge-form, .mark-as-human');
                                        if (cf) { cf.click(); return; }
                                        
                                        var isJustAMoment = document.title.includes('Just a moment') || document.title.includes('Cloudflare');
                                        var isCloudflare = cf || isJustAMoment;

                                        // 1. Search Results -> Click item
                                        if (loc.includes('?s=') || loc.includes('search') || loc.includes('query=')) {
                                            var result = document.querySelector('a.postBlock, section.main-section ul.posts-list li.movieItem a, ul.pm-ul-browse-videos li a, ul.movie__blocks__ul li a.movie__block, ul.series__ul li a, div.media-block a.image, div.owl-animes a.overlay, div.embla__slide a');
                                            if (result) { window.location.href = result.href; return; }
                                        }
                                        
                                        // 2. Series Page -> Click Season/Episode
                                        if (!isMovie && !loc.includes('episode') && !loc.includes('ep-') && !loc.includes('watch')) {
                                            var epLinks = document.querySelectorAll('.episodes__list li a, .EpsList li a, .episodes-list li a, .all-episodes-list li a, .SeasonsEpisodes a');
                                            if (epLinks.length > 0) {
                                                for(var i=0; i<epLinks.length; i++) {
                                                    var text = epLinks[i].innerText || "";
                                                    if(text.includes(epNum.toString())) {
                                                        window.location.href = epLinks[i].href;
                                                        return;
                                                    }
                                                }
                                                // Fallback to first episode
                                                window.location.href = epLinks[0].href;
                                                return;
                                            }
                                        }
                                        
                                        // 3. Extract Servers on Watch Page
                                        var serverList = document.querySelectorAll('ul.servers li, .server-list li, .serversList li, .watch-servers li, .list-servers li, .servers-list li, .mob-servers ul li');
                                        if (serverList && serverList.length > 0) {
                                            var serverNames = [];
                                            for(var i=0; i<serverList.length; i++) {
                                                serverNames.push(serverList[i].innerText.trim());
                                            }
                                            if (typeof AndroidBridge !== 'undefined') {
                                                AndroidBridge.sendServers(serverNames.join(','), window.location.href);
                                            }
                                            return;
                                        }
                                        
                                        // 4. Fast Fail
                                        if (!isCloudflare && document.readyState === 'complete') {
                                            window._failCount = (window._failCount || 0) + 1;
                                            if (window._failCount >= 4) {
                                                if (typeof AndroidBridge !== 'undefined') AndroidBridge.sendFailed();
                                            }
                                        }
                                    }, 1500);
                                })();""", replacement)

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
    f.write(content)
