# -*- coding: utf-8 -*-
import json, hashlib, io

PATH = "i18n/catalog.json"
with io.open(PATH, encoding="utf-8") as f:
    cat = json.load(f)

FILE = "15h/zoubkovani.html"

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
 "Z 6 478 čitelně datovaných razítek. Pořadí ukazuje, jak výroba postupovala od řádkových zoubkování D/E/F na raných deskách k hřebenovým A/B na deskách pozdějších.",
 "From 6,478 legibly dated cancellations. The sequence shows production moving from line perforations D/E/F on the early plates to comb perforations A/B on the later ones.",
 "Sur la base de 6 478 oblitérations lisiblement datées. La séquence montre la production passer des dentelures en lignes D/E/F sur les planches précoces aux dentelures en peigne A/B sur les planches plus tardives.",
 "Von 6.478 lesbar datierten Stempeln. Die Reihenfolge zeigt, wie die Produktion von den Linienzähnungen D/E/F auf den frühen Platten zu den Kammzähnungen A/B auf den späteren Platten überging.",
 "De 6478 matasellos legiblemente fechados. La secuencia muestra cómo la producción avanzó de los dentados en línea D/E/F en las planchas tempranas a los dentados en peine A/B en las planchas posteriores.",
)

with io.open(PATH, "w", encoding="utf-8") as f:
    json.dump(cat, f, ensure_ascii=False, indent=1, sort_keys=True)

print("added", added, "skipped(existing)", skipped, "total", len(cat))
