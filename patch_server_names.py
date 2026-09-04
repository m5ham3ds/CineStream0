import re

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

# Fix the selector for serverList
old_sel = "var serverList = document.querySelectorAll('ul.servers li, .server-list li, .serversList li, .watch-servers li, .list-servers li, .servers-list li, .mob-servers ul li, #servers li, .server_list li, .watch-btn, .DownloadServers li, ul#episode-servers li, ul.NavTabs li, .server-list a, .watch-servers a, .servers-container li, .btn-server, .servers a, .item-server, .server-item');"
new_sel = "var serverList = document.querySelectorAll('ul.servers li, .server-list li, .serversList li, .watch-servers li, .list-servers li, .servers-list li, .mob-servers ul li, #servers li, .server_list li, .watch-btn, .DownloadServers li, ul#episode-servers li, ul.NavTabs li, .server-list a, .watch-servers a, .servers-container li, .btn-server, .servers a, .item-server, .server-item, .server-btn, .server-link, a.server-link, ul.donwload-servers-list li, .servers-container button');"

content = content.replace(old_sel, new_sel)

# Fix the server name logic
old_logic = """                                                        // Strip quality terms from the server name
                                                        serverName = serverName.replace(/1080p|720p|480p|360p|240p|1080|720|480|360|240/gi, '').trim();
                                                        // If after stripping it's empty, or it was just "جودة عالية" etc, skip it or give it a default name
                                                        if (serverName.length > 0 && !serverName.includes('جودة') && !serverName.includes('FHD') && !serverName.includes('HD') && !serverName.includes('SD')) {
                                                            serverNames.push(serverName);
                                                        } else if (serverNames.length === 0) {
                                                            // If we only have qualities, maybe just call it server + index
                                                            serverNames.push("سيرفر " + (i+1));
                                                        }"""

new_logic = """                                                        var sName = serverName.replace(/1080p|720p|480p|360p|240p|1080|720|480|360|240/gi, '').trim();
                                                        if (sName === "" || sName.includes('جودة') || sName.includes('FHD') || sName.includes('HD') || sName.includes('SD')) {
                                                            sName = "سيرفر " + (i+1);
                                                        }
                                                        serverNames.push(sName);"""

content = content.replace(old_logic, new_logic)

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
    f.write(content)
print("Patched ServerSelectionDialog")
