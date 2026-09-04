import re

with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'r') as f:
    content = f.read()

old_script = "var serverList = document.querySelectorAll('ul.servers li, .server-list li, .serversList li, .watch-servers li, .list-servers li, .servers-list li, .mob-servers ul li, .servers-container li, .btn-server');"
new_script = "var serverList = document.querySelectorAll('ul.servers li, .server-list li, .serversList li, .watch-servers li, .list-servers li, .servers-list li, .mob-servers ul li, #servers li, .server_list li, .watch-btn, .DownloadServers li, ul#episode-servers li, ul.NavTabs li, .server-list a, .watch-servers a, .servers-container li, .btn-server, .servers a, .item-server, .server-item');"

if old_script in content:
    content = content.replace(old_script, new_script)
    with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'w') as f:
        f.write(content)
    print("Patched VideoExtractor selector")
else:
    print("Old script not found in VideoExtractor selector")

