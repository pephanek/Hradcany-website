# -*- coding: utf-8 -*-
import json, hashlib, io

PATH = "i18n/catalog.json"
with io.open(PATH, encoding="utf-8") as f:
    cat = json.load(f)

FILE = "15h/vyrobni-vady.html"

def key(s):
    return hashlib.sha1(s.strip().encode("utf-8")).hexdigest()[:10]

added = 0
skipped = 0

def add(cs, en, fr, de, es, tag="span"):
    global added, skipped
    k = key(cs)
    if k in cat:
        if FILE not in cat[k].get("files", []):
            cat[k]["files"].append(FILE)
        skipped += 1
        return
    cat[k] = {"cs": cs, "en": en, "fr": fr, "de": de, "es": es, "files": [FILE], "tag": tag}
    added += 1

# bare description (used in <p class="tg-cap">)
add(
 "Kus s čitelným razítkem 1. VI. 1920. Hranice probíhá těsně pod obloukem, ve výši horních věží Hradčan.",
 "A copy with a legible cancel of 1 June 1920. The boundary runs just below the arch, at the level of the upper towers of Hradčany.",
 "Exemplaire avec une oblitération lisible du 1er juin 1920. La limite passe juste sous l'arc, au niveau des tours supérieures du Hradčany.",
 "Ein Exemplar mit einem lesbaren Stempel vom 1. Juni 1920. Die Grenze verläuft knapp unterhalb des Bogens, auf Höhe der oberen Türme des Hradschin.",
 "Un ejemplar con un matasellos legible del 1 de junio de 1920. El límite pasa justo debajo del arco, a la altura de las torres superiores del Hradčany.",
)

# numbered variant (used in data-cap)
add(
 "Kus 5 — Kus s čitelným razítkem 1. VI. 1920. Hranice probíhá těsně pod obloukem, ve výši horních věží Hradčan.",
 "Item 5 — A copy with a legible cancel of 1 June 1920. The boundary runs just below the arch, at the level of the upper towers of Hradčany.",
 "Pièce 5 — Exemplaire avec une oblitération lisible du 1er juin 1920. La limite passe juste sous l'arc, au niveau des tours supérieures du Hradčany.",
 "Stück 5 — Ein Exemplar mit einem lesbaren Stempel vom 1. Juni 1920. Die Grenze verläuft knapp unterhalb des Bogens, auf Höhe der oberen Türme des Hradschin.",
 "Pieza 5 — Un ejemplar con un matasellos legible del 1 de junio de 1920. El límite pasa justo debajo del arco, a la altura de las torres superiores del Hradčany.",
)

with io.open(PATH, "w", encoding="utf-8") as f:
    json.dump(cat, f, ensure_ascii=False, indent=1, sort_keys=True)

print("added", added, "skipped(existing)", skipped, "total", len(cat))
