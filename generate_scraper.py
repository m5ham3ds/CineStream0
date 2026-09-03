import re

sites = [
    ("QFilm", "a.qfilm.tv"),
    ("Animeat", "animeat.net"),
    ("Arabanime", "arabanime.net"),
    ("ArabSeed", "arabseed-tv.com"),
    ("ArabSeed Wine", "arabseed.wine"),
    ("Animerco", "det.animerco.org"),
    ("CimaLight", "e.cimalight.co"),
    ("Egy Best", "egybests.live"),
    ("Stardima", "stardima.com"),
    ("EgyDead TV10", "tv10.egydead.live"),
    ("Brstej", "uo.brstej.com"),
    ("AnimeLuxe", "vip.animeluxe.org"),
    ("Watch Stardima", "watch.stardima.com"),
    ("WitAnime", "witanime.you")
]

print("val availableWebsites: List<String> = listOf(")
for name, domain in sites:
    print(f'    "{name}",')
print(")")

