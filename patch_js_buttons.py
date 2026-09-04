import re

# PATCH ServerSelectionDialog.kt
with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

old_click = """                                        // Click play buttons to reveal iframe if hidden
                                        var playBtn = document.querySelector('.play-button, .jw-icon-display, video, .vjs-big-play-button, .play-icon, #play-video, .btn-play');
                                        if (playBtn) playBtn.click();"""

new_click = """                                        // Click play buttons or watch forms to reveal iframe if hidden
                                        var playBtn = document.querySelector('.play-button, .jw-icon-display, video, .vjs-big-play-button, .play-icon, #play-video, .btn-play');
                                        if (playBtn) playBtn.click();
                                        
                                        var watchNowBtn = document.querySelector('.watchNow button, .watchNow form button, .watch-btn, #watch-btn');
                                        if (watchNowBtn && !hasServers && !hasIframe && !hasVideo) {
                                            watchNowBtn.click();
                                            return;
                                        }"""

if old_click in content:
    content = content.replace(old_click, new_click)
    with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
        f.write(content)
    print("Patched ServerSelectionDialog.kt")
else:
    print("Could not find old_click in ServerSelectionDialog.kt")

# PATCH VideoExtractor.kt
with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'r') as f:
    content = f.read()

old_watch = """                                    // Some sites need us to click a watch button first
                                    var watchBtn = document.querySelector('.watch-btn, #watch-btn, a.watch, .btn-watch, .play-btn');
                                    if(watchBtn && !loc.includes('watch')) watchBtn.click();"""

new_watch = """                                    // Some sites need us to click a watch button or submit a form first
                                    var watchBtn = document.querySelector('.watch-btn, #watch-btn, a.watch, .btn-watch, .play-btn, .watchNow button, .watchNow form button');
                                    if(watchBtn) watchBtn.click();"""

if old_watch in content:
    content = content.replace(old_watch, new_watch)
    with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'w') as f:
        f.write(content)
    print("Patched VideoExtractor.kt")
else:
    print("Could not find old_watch in VideoExtractor.kt")

