import re

with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'r') as f:
    content = f.read()

old_code = """                                    // Some sites need us to click a watch button or submit a form first
                                    var watchBtn = document.querySelector('.watch-btn, #watch-btn, a.watch, .btn-watch, .play-btn, .watchNow button, .watchNow form button');
                                    if(watchBtn) watchBtn.click();
                                    
                                    // Some sites use servers list to load iframe
                                    var serverList = document.querySelectorAll('ul.servers li, .server-list li, .serversList li, .watch-servers li, .list-servers li, .servers-list li, .mob-servers ul li, #servers li, .server_list li, .watch-btn, .DownloadServers li, ul#episode-servers li, ul.NavTabs li, .server-list a, .watch-servers a, .servers-container li, .btn-server, .servers a, .item-server, .server-item, .server-btn, .server-link, a.server-link, ul.donwload-servers-list li, .servers-container button');"""

new_code = """                                    // Some sites use servers list to load iframe
                                    var serverList = document.querySelectorAll('ul.servers li, .server-list li, .serversList li, .watch-servers li, .list-servers li, .servers-list li, .mob-servers ul li, #servers li, .server_list li, .watch-btn, .DownloadServers li, ul#episode-servers li, ul.NavTabs li, .server-list a, .watch-servers a, .servers-container li, .btn-server, .servers a, .item-server, .server-item, .server-btn, .server-link, a.server-link, ul.donwload-servers-list li, .servers-container button');
                                    
                                    // Some sites need us to click a watch button or submit a form first
                                    var watchBtn = document.querySelector('.watch-btn, #watch-btn, a.watch, .btn-watch, .play-btn, .watchNow button, .watchNow form button');
                                    if(watchBtn && (!serverList || serverList.length === 0)) {
                                        watchBtn.click();
                                    }"""

if old_code in content:
    content = content.replace(old_code, new_code)
    with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'w') as f:
        f.write(content)
    print("Patched watchBtn logic in VideoExtractor.kt")
else:
    print("Could not find old_code in VideoExtractor.kt")
