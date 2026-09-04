import re

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

old_sites = """    val animeSites = listOf("witanime.cyou", "anime4up.cam", "animeat.net", "vip.animeluxe.org", "det.animerco.org", "stardima.com", "watch.stardima.com")
    val movieSites = listOf("egydead.plus", "arabseed.show", "qfilm.tv", "cima4u.skin", "faselhd.wtf", "tv10.egydead.live", "a.qfilm.tv", "arabseed.wine", "egybests.live")
    val prioritySites = if (isAnime) animeSites else movieSites"""

new_sites = """    val animeSites = listOf("witanime.cyou", "anime4up.cam", "animeat.net", "vip.animeluxe.org", "det.animerco.org", "stardima.com", "watch.stardima.com", "tv10.egydead.live")
    val movieSites = listOf("egydead.plus", "arabseed.show", "qfilm.tv", "cima4u.skin", "faselhd.wtf", "a.qfilm.tv", "arabseed.wine", "egybests.live", "tv10.egydead.live")
    val prioritySites = if (isAnime) animeSites else movieSites"""

content = content.replace(old_sites, new_sites)

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
    f.write(content)
print("Patched sites list")
