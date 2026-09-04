import re

with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'r') as f:
    content = f.read()

old_sel = "var serverList = document.querySelectorAll('ul.servers li, .server-list li, .serversList li, .watch-servers li, .list-servers li, .servers-list li, .mob-servers ul li, #servers li, .server_list li, .watch-btn, .DownloadServers li, ul#episode-servers li, ul.NavTabs li, .server-list a, .watch-servers a, .servers-container li, .btn-server, .servers a, .item-server, .server-item');"
new_sel = "var serverList = document.querySelectorAll('ul.servers li, .server-list li, .serversList li, .watch-servers li, .list-servers li, .servers-list li, .mob-servers ul li, #servers li, .server_list li, .watch-btn, .DownloadServers li, ul#episode-servers li, ul.NavTabs li, .server-list a, .watch-servers a, .servers-container li, .btn-server, .servers a, .item-server, .server-item, .server-btn, .server-link, a.server-link, ul.donwload-servers-list li, .servers-container button');"
content = content.replace(old_sel, new_sel)


old_logic1 = """                                                var sName = serverList[i].innerText.trim().replace(/1080p|720p|480p|360p|240p|1080|720|480|360|240/gi, '').trim();
                                                if (sName === "" && !sName.includes('جودة') && !sName.includes('FHD') && !sName.includes('HD') && !sName.includes('SD')) {
                                                    sName = "سيرفر " + (i+1);
                                                }
                                                if (sName.length > 0) serverNames.push(sName);"""
                                                
new_logic1 = """                                                var sName = serverList[i].innerText.trim().replace(/1080p|720p|480p|360p|240p|1080|720|480|360|240/gi, '').trim();
                                                if (sName === "" || sName.includes('جودة') || sName.includes('FHD') || sName.includes('HD') || sName.includes('SD')) {
                                                    sName = "سيرفر " + (i+1);
                                                }
                                                serverNames.push(sName);"""
content = content.replace(old_logic1, new_logic1)


old_logic2 = """            var sName = serverList[i].innerText.trim().replace(/1080p|720p|480p|360p|240p|1080|720|480|360|240/gi, '').trim();
            if (sName === "" && !sName.includes('جودة') && !sName.includes('FHD') && !sName.includes('HD') && !sName.includes('SD')) {
                sName = "سيرفر " + (i+1);
            }
            if(sName === targetServer || serverList[i].innerText.trim() === targetServer) {"""

new_logic2 = """            var sName = serverList[i].innerText.trim().replace(/1080p|720p|480p|360p|240p|1080|720|480|360|240/gi, '').trim();
            if (sName === "" || sName.includes('جودة') || sName.includes('FHD') || sName.includes('HD') || sName.includes('SD')) {
                sName = "سيرفر " + (i+1);
            }
            if(sName === targetServer || serverList[i].innerText.trim() === targetServer) {"""
content = content.replace(old_logic2, new_logic2)

with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'w') as f:
    f.write(content)
print("Patched VideoExtractor")
