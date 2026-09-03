import re

with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'r') as f:
    content = f.read()

new_js = """
                                // 1. Auto-Play Players (MegaMax, VidSrc, etc)
                                setInterval(function() {
                                    var iframes = document.getElementsByTagName('iframe');
                                    for (var i = 0; i < iframes.length; i++) {
                                        try {
                                            var playBtn = iframes[i].contentWindow.document.querySelector('.play-button, .jw-icon-display, video, .vjs-big-play-button');
                                            if (playBtn) playBtn.click();
                                        } catch(e) {}
                                    }
                                    var localPlay = document.querySelector('.play-button, .jw-icon-display, video, .vjs-big-play-button');
                                    if (localPlay) localPlay.click();
                                    
                                    // Some sites need us to click a watch button first
                                    var watchBtn = document.querySelector('.watch-btn, #watch-btn, a.watch, .btn-watch, .play-btn');
                                    if(watchBtn && !loc.includes('watch')) watchBtn.click();
                                    
                                    // Some sites use servers list to load iframe
                                    var serverList = document.querySelectorAll('ul.servers li, .server-list li, .serversList li, .watch-servers li, .list-servers li, .servers-list li, .mob-servers ul li');
                                    var clickedTarget = false;
                                    if (serverList && serverList.length > 0) {
                                        if (targetServer !== "") {
                                            for(var i=0; i<serverList.length; i++) {
                                                if(serverList[i].innerText.trim() === targetServer) {
                                                    serverList[i].click();
                                                    clickedTarget = true;
                                                    break;
                                                }
                                            }
                                        }
                                        if (!clickedTarget && document.getElementsByTagName('iframe').length === 0) {
                                            serverList[0].click();
                                        }
                                    }
                                    
                                    // Send servers back to Kotlin
                                    if (serverList && serverList.length > 0 && typeof AndroidBridge !== 'undefined') {
                                        var serverNames = [];
                                        for(var i=0; i<serverList.length; i++) {
                                            serverNames.push(serverList[i].innerText.trim());
                                        }
                                        AndroidBridge.sendServers(serverNames.join(','));
                                    }
                                    
                                }, 1500);
"""

# replace between // 1. Auto-Click Search Results and // Send servers back to Kotlin
# using regex
content = re.sub(r'// 1\. Auto-Click Search Results.*AndroidBridge\.sendServers\(serverNames\.join\(\',\',\)\);\s*\}\s*\}, 1500\);', new_js, content, flags=re.DOTALL | re.MULTILINE)

# wait, the regex above has a comma typo in the join string. let's just do an index based replace

start_idx = content.find('// 1. Auto-Click Search Results')
end_idx = content.find('}, 1500);', start_idx) + 9

content = content[:start_idx] + new_js.strip() + content[end_idx:]

with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'w') as f:
    f.write(content)

