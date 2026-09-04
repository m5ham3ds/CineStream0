import re

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

old_sites = """    val animeSites = listOf("witanime.cyou", "anime4up.cam", "animeat.net", "vip.animeluxe.org", "det.animerco.org", "stardima.com", "watch.stardima.com", "tv10.egydead.live")
    val movieSites = listOf("egydead.plus", "arabseed.show", "qfilm.tv", "cima4u.skin", "faselhd.wtf", "a.qfilm.tv", "arabseed.wine", "egybests.live", "tv10.egydead.live")"""

new_sites = """    val animeSites = listOf("tv10.egydead.live", "witanime.cyou", "anime4up.cam", "animeat.net", "vip.animeluxe.org", "det.animerco.org", "stardima.com", "watch.stardima.com")
    val movieSites = listOf("tv10.egydead.live", "egydead.plus", "arabseed.show", "qfilm.tv", "cima4u.skin", "faselhd.wtf", "a.qfilm.tv", "arabseed.wine", "egybests.live")"""

content = content.replace(old_sites, new_sites)

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
    f.write(content)
print("Patched sites list order")
