# -*- coding: utf-8 -*-
import json, hashlib, io

PATH = "i18n/catalog.json"
with io.open(PATH, encoding="utf-8") as f:
    cat = json.load(f)

def key(s):
    return hashlib.sha1(s.strip().encode("utf-8")).hexdigest()[:10]

# remove orphaned entries (my earlier guess, not actually used in the live file)
orphan1 = "Plná skvrna v ploše oblohy vpravo od věží Hradčan."
orphan2 = "Kus 14 — Plná skvrna v ploše oblohy vpravo od věží Hradčan."
removed = 0
for o in (orphan1, orphan2):
    k = key(o)
    if k in cat:
        del cat[k]
        removed += 1

FILE = "15h/vyrobni-vady.html"
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

add(
 "Kroužek s tmavým jádrem a světlým dvorcem — při pravém okraji kresby, v porostu vpravo od kostelních věží, těsně nad lištou s nápisem.",
 "A ring with a dark core and a light halo — at the right edge of the design, in the foliage right of the church towers, just above the inscription band.",
 "Un anneau au centre sombre et au halo clair — au bord droit du dessin, dans le feuillage à droite des tours de l'église, juste au-dessus du bandeau de l'inscription.",
 "Ein Ring mit dunklem Kern und hellem Hof — am rechten Rand der Zeichnung, im Blattwerk rechts der Kirchtürme, unmittelbar über dem Schriftband.",
 "Un anillo con núcleo oscuro y halo claro — en el borde derecho del dibujo, entre el follaje a la derecha de las torres de la iglesia, justo encima de la franja de la inscripción.",
)
add(
 "Kus 14 — Kroužek s tmavým jádrem a světlým dvorcem — při pravém okraji kresby, v porostu vpravo od kostelních věží, těsně nad lištou s nápisem.",
 "Item 14 — A ring with a dark core and a light halo — at the right edge of the design, in the foliage right of the church towers, just above the inscription band.",
 "Pièce 14 — Un anneau au centre sombre et au halo clair — au bord droit du dessin, dans le feuillage à droite des tours de l'église, juste au-dessus du bandeau de l'inscription.",
 "Stück 14 — Ein Ring mit dunklem Kern und hellem Hof — am rechten Rand der Zeichnung, im Blattwerk rechts der Kirchtürme, unmittelbar über dem Schriftband.",
 "Pieza 14 — Un anillo con núcleo oscuro y halo claro — en el borde derecho del dibujo, entre el follaje a la derecha de las torres de la iglesia, justo encima de la franja de la inscripción.",
)

with io.open(PATH, "w", encoding="utf-8") as f:
    json.dump(cat, f, ensure_ascii=False, indent=1, sort_keys=True)

print("removed orphans:", removed, "added", added, "skipped(existing)", skipped, "total", len(cat))
