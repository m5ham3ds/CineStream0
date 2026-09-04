import re

with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'r') as f:
    content = f.read()

old_script = """                                    // Send servers back to Kotlin
                                    if (serverList && serverList.length > 0 && typeof AndroidBridge !== 'undefined') {
                                        var serverNames = [];
                                        for(var i=0; i<serverList.length; i++) {
                                            serverNames.push(serverList[i].innerText.trim());
                                        }
                                        AndroidBridge.sendServers(serverNames.join(','));
                                    }"""

new_script = """                                    // Send servers back to Kotlin
                                    if (typeof AndroidBridge !== 'undefined') {
                                        var serverNames = [];
                                        if (serverList && serverList.length > 0) {
                                            for(var i=0; i<serverList.length; i++) {
                                                var sName = serverList[i].innerText.trim().replace(/1080p|720p|480p|360p|240p|1080|720|480|360|240/gi, '').trim();
                                                if (sName === "" && !sName.includes('جودة') && !sName.includes('FHD') && !sName.includes('HD') && !sName.includes('SD')) {
                                                    sName = "سيرفر " + (i+1);
                                                }
                                                if (sName.length > 0) serverNames.push(sName);
                                            }
                                        }
                                        if (serverNames.length === 0 && (document.getElementsByTagName('iframe').length > 0 || document.querySelectorAll('video').length > 0)) {
                                            serverNames.push("السيرفر الرئيسي");
                                        }
                                        var uniqueServers = [...new Set(serverNames)];
                                        if (uniqueServers.length > 0) {
                                            AndroidBridge.sendServers(uniqueServers.join(','));
                                        }
                                    }"""

if old_script in content:
    content = content.replace(old_script, new_script)
    with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'w') as f:
        f.write(content)
    print("Patched VideoExtractor sendServers")
else:
    print("Old script not found in VideoExtractor sendServers")

