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

add(
 "Plná skvrna v ploše oblohy vpravo od věží Hradčan.",
 "A solid spot in the sky, to the right of the towers of Hradčany.",
 "Une tache pleine dans le ciel, à droite des tours du Hradčany.",
 "Ein voller Fleck am Himmel, rechts von den Türmen des Hradschin.",
 "Una mancha maciza en el cielo, a la derecha de las torres del Hradčany.",
)
add(
 "Kus 14 — Plná skvrna v ploše oblohy vpravo od věží Hradčan.",
 "Item 14 — A solid spot in the sky, to the right of the towers of Hradčany.",
 "Pièce 14 — Une tache pleine dans le ciel, à droite des tours du Hradčany.",
 "Stück 14 — Ein voller Fleck am Himmel, rechts von den Türmen des Hradschin.",
 "Pieza 14 — Una mancha maciza en el cielo, a la derecha de las torres del Hradčany.",
)

with io.open(PATH, "w", encoding="utf-8") as f:
    json.dump(cat, f, ensure_ascii=False, indent=1, sort_keys=True)

print("added", added, "skipped(existing)", skipped, "total", len(cat))
