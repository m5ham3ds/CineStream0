import re

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

old_script = """                                        var serverList = document.querySelectorAll('ul.servers li, .server-list li, .serversList li, .watch-servers li, .list-servers li, .servers-list li, .mob-servers ul li, #servers li, .server_list li, .watch-btn, .DownloadServers li, ul#episode-servers li, ul.NavTabs li, .server-list a, .watch-servers a, .servers-container li, .btn-server');
                                        var hasServers = serverList && serverList.length > 0;
                                        var iframes = document.querySelectorAll('iframe');
                                        var hasIframe = false;
                                        for(var i=0; i<iframes.length; i++) {
                                            if(iframes[i].src && !iframes[i].src.includes('cloudflare') && !iframes[i].src.includes('facebook') && !iframes[i].src.includes('twitter')) {
                                                hasIframe = true; break;
                                            }
                                        }

                                        if (!isMovie && !hasServers && !hasIframe) {
                                            var epLinks = document.querySelectorAll('.episodes__list li a, .EpsList li a, .episodes-list li a, .all-episodes-list li a, .SeasonsEpisodes a, .episodelist a, .episodes a, .ListEp a, ul.episodes li a, .ep-card a, .episode-card a, .List-Episodes a, .list-episodes a, .EpisodesList a, .eplist a, .episode-list a');
                                            if (epLinks.length > 0) {
                                                clearInterval(intervalId);
                                                var targetEp = null;
                                                for(var i=0; i<epLinks.length; i++) {
                                                    var text = epLinks[i].innerText || "";
                                                    if(text.trim() === epNum.toString() || text.includes(" " + epNum.toString() + " ") || text.includes("حلقة " + epNum) || text.includes("الحلقة " + epNum)) {
                                                        targetEp = epLinks[i];
                                                        break;
                                                    }
                                                }
                                                if(targetEp) {
                                                    window.location.href = targetEp.href;
                                                } else {
                                                    // Fallback to first episode if matching fails, or the one that has the number somewhere
                                                    for(var i=0; i<epLinks.length; i++) {
                                                        if((epLinks[i].innerText || "").includes(epNum.toString())) {
                                                            targetEp = epLinks[i]; break;
                                                        }
                                                    }
                                                    window.location.href = targetEp ? targetEp.href : epLinks[0].href;
                                                }
                                                return;
                                            }
                                        }
                                        
                                        // 3. Extract Servers on Watch Page
                                        if (hasServers || hasIframe) {
                                            var serverNames = [];
                                            if (hasServers) {
                                                for(var i=0; i<serverList.length; i++) {
                                                    var serverName = serverList[i].innerText.trim();
                                                    // Filter out qualities
                                                    if (serverName && !serverName.includes('1080') && !serverName.includes('720') && !serverName.includes('480') && !serverName.includes('360') && !serverName.includes('240')) {
                                                        serverNames.push(serverName);
                                                    }
                                                }
                                            }
                                            if (serverNames.length === 0 && hasIframe) {
                                                serverNames.push("السيرفر الرئيسي");
                                            }
                                            
                                            if (serverNames.length > 0) {
                                                // Make unique
                                                var uniqueServers = [...new Set(serverNames)];
                                                clearInterval(intervalId);
                                                if (typeof AndroidBridge !== 'undefined') {
                                                    AndroidBridge.sendServers(uniqueServers.join(','), window.location.href);
                                                }
                                                return;
                                            }
                                        }"""

new_script = """                                        var serverList = document.querySelectorAll('ul.servers li, .server-list li, .serversList li, .watch-servers li, .list-servers li, .servers-list li, .mob-servers ul li, #servers li, .server_list li, .watch-btn, .DownloadServers li, ul#episode-servers li, ul.NavTabs li, .server-list a, .watch-servers a, .servers-container li, .btn-server, .servers a, .item-server, .server-item');
                                        var hasServers = serverList && serverList.length > 0;
                                        
                                        // Click play buttons to reveal iframe if hidden
                                        var playBtn = document.querySelector('.play-button, .jw-icon-display, video, .vjs-big-play-button, .play-icon, #play-video, .btn-play');
                                        if (playBtn) playBtn.click();
                                        
                                        var iframes = document.querySelectorAll('iframe');
                                        var hasIframe = false;
                                        for(var i=0; i<iframes.length; i++) {
                                            if(iframes[i].src && !iframes[i].src.includes('cloudflare') && !iframes[i].src.includes('facebook') && !iframes[i].src.includes('twitter')) {
                                                hasIframe = true; break;
                                            }
                                        }

                                        var videoTags = document.querySelectorAll('video');
                                        var hasVideo = videoTags.length > 0;

                                        if (!isMovie && !hasServers && !hasIframe && !hasVideo) {
                                            var epLinks = document.querySelectorAll('.episodes__list li a, .EpsList li a, .episodes-list li a, .all-episodes-list li a, .SeasonsEpisodes a, .episodelist a, .episodes a, .ListEp a, ul.episodes li a, .ep-card a, .episode-card a, .List-Episodes a, .list-episodes a, .EpisodesList a, .eplist a, .episode-list a');
                                            if (epLinks.length > 0) {
                                                clearInterval(intervalId);
                                                var targetEp = null;
                                                for(var i=0; i<epLinks.length; i++) {
                                                    var text = epLinks[i].innerText || "";
                                                    if(text.trim() === epNum.toString() || text.includes(" " + epNum.toString() + " ") || text.includes("حلقة " + epNum) || text.includes("الحلقة " + epNum)) {
                                                        targetEp = epLinks[i];
                                                        break;
                                                    }
                                                }
                                                if(targetEp) {
                                                    window.location.href = targetEp.href;
                                                } else {
                                                    for(var i=0; i<epLinks.length; i++) {
                                                        if((epLinks[i].innerText || "").includes(epNum.toString())) {
                                                            targetEp = epLinks[i]; break;
                                                        }
                                                    }
                                                    window.location.href = targetEp ? targetEp.href : epLinks[0].href;
                                                }
                                                return;
                                            }
                                        }
                                        
                                        // 3. Extract Servers on Watch Page
                                        if (hasServers || hasIframe || hasVideo) {
                                            var serverNames = [];
                                            if (hasServers) {
                                                for(var i=0; i<serverList.length; i++) {
                                                    var serverName = serverList[i].innerText.trim();
                                                    if (serverName) {
                                                        // Strip quality terms from the server name
                                                        serverName = serverName.replace(/1080p|720p|480p|360p|240p|1080|720|480|360|240/gi, '').trim();
                                                        // If after stripping it's empty, or it was just "جودة عالية" etc, skip it or give it a default name
                                                        if (serverName.length > 0 && !serverName.includes('جودة') && !serverName.includes('FHD') && !serverName.includes('HD') && !serverName.includes('SD')) {
                                                            serverNames.push(serverName);
                                                        } else if (serverNames.length === 0) {
                                                            // If we only have qualities, maybe just call it server + index
                                                            serverNames.push("سيرفر " + (i+1));
                                                        }
                                                    }
                                                }
                                            }
                                            if (serverNames.length === 0 && (hasIframe || hasVideo)) {
                                                serverNames.push("السيرفر الرئيسي");
                                            }
                                            
                                            if (serverNames.length > 0) {
                                                // Make unique
                                                var uniqueServers = [...new Set(serverNames)];
                                                clearInterval(intervalId);
                                                if (typeof AndroidBridge !== 'undefined') {
                                                    AndroidBridge.sendServers(uniqueServers.join(','), window.location.href);
                                                }
                                                return;
                                            }
                                        }"""

if old_script in content:
    content = content.replace(old_script, new_script)
    with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
        f.write(content)
    print("Patched successfully")
else:
    print("Old script not found")
