import re

with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'r') as f:
    content = f.read()

old_script = """                                    if (targetServer === "السيرفر الرئيسي") {
                                        clickedTarget = true;
                                    } else if (serverList && serverList.length > 0) {
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
                                    }"""

new_script = """                                    if (targetServer === "السيرفر الرئيسي") {
                                        clickedTarget = true;
                                    } else if (serverList && serverList.length > 0) {
                                        if (targetServer !== "") {
                                            for(var i=0; i<serverList.length; i++) {
                                                var sName = serverList[i].innerText.trim().replace(/1080p|720p|480p|360p|240p|1080|720|480|360|240/gi, '').trim();
                                                if (sName === "" && !sName.includes('جودة') && !sName.includes('FHD') && !sName.includes('HD') && !sName.includes('SD')) {
                                                    sName = "سيرفر " + (i+1);
                                                }
                                                if(sName === targetServer || serverList[i].innerText.trim() === targetServer) {
                                                    serverList[i].click();
                                                    clickedTarget = true;
                                                    break;
                                                }
                                            }
                                        }
                                        if (!clickedTarget && document.getElementsByTagName('iframe').length === 0 && document.querySelectorAll('video').length === 0) {
                                            serverList[0].click();
                                        }
                                    }"""

if old_script in content:
    content = content.replace(old_script, new_script)
    with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'w') as f:
        f.write(content)
    print("Patched VideoExtractor")
else:
    print("Old script not found in VideoExtractor")

