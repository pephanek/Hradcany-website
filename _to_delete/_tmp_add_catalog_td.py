# -*- coding: utf-8 -*-
import json, hashlib, io

PATH = "i18n/catalog.json"
with io.open(PATH, encoding="utf-8") as f:
    cat = json.load(f)

FILE = "15h/zkusebni-tisky.html"

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
 "Vedle jednotlivých zkušebních tisků se dochoval i celý arch (10×10 polí) POFIS 7 (15h) vytištěný celý v černé barvě, nezoubkovaný — stejný účel jako u ostatních zkušebních tisků, tentokrát ale na úrovni celého archu místo jediného pole. Rozmezí let 1918–1920 odpovídá období, kdy se na arších tohoto vydání tiskla takzvaná kontrolní čísla. Podle stavebního znaku na poli 11 — barevná spojnice mezi hodnotovým oválem a spodním rámečkem, kterou má na tomto poli každá deska kromě III — jde o tiskovou desku VI.",
 "Besides the individual proofs, a full pane (10×10 fields) of POFIS 7 (the 15h) has also survived, printed entirely in black and imperforate — the same purpose as the other proofs, but at the level of a whole pane rather than a single field. The span 1918–1920 corresponds to the period in which this issue's sheets carried what are called control numbers. A structural marker at field 11 — a coloured line joining the value oval to the bottom frame, present on every plate except III — identifies this as printing plate VI.",
 "Outre les épreuves individuelles, une feuille complète (10×10 champs) de POFIS 7 (le 15h) a également été conservée, imprimée entièrement en noir et non dentelée — le même objectif que pour les autres épreuves, mais cette fois à l'échelle d'une feuille entière plutôt que d'un seul champ. La période 1918–1920 correspond à l'époque où les feuilles de cette émission portaient ce que l'on appelle les chiffres de contrôle. Une marque structurelle au champ 11 — un trait coloré reliant l'ovale de valeur au cadre inférieur, présent sur toutes les planches sauf la III — permet d'identifier ici la planche d'impression VI.",
 "Neben den einzelnen Probedrucken ist auch ein vollständiger Bogen (10×10 Felder) von POFIS 7 (der 15h) erhalten geblieben, vollständig in Schwarz gedruckt und ungezähnt — derselbe Zweck wie bei den übrigen Probedrucken, diesmal jedoch auf der Ebene eines ganzen Bogens statt eines einzelnen Feldes. Der Zeitraum 1918–1920 entspricht der Periode, in der die Bögen dieser Ausgabe die sogenannten Kontrollzahlen trugen. Ein Strukturmerkmal an Feld 11 — eine farbige Linie, die das Wertoval mit dem unteren Rahmen verbindet und auf jeder Platte außer III vorhanden ist — identifiziert dies als Druckplatte VI.",
 "Además de las pruebas individuales, también se ha conservado una hoja completa (10×10 campos) de POFIS 7 (el 15h), impresa enteramente en negro y sin dentar — el mismo propósito que las demás pruebas, pero esta vez a escala de una hoja entera en lugar de un solo campo. El período 1918–1920 corresponde a la época en que las hojas de esta emisión llevaban las llamadas cifras de control. Una marca estructural en el campo 11 — una línea coloreada que une el óvalo de valor con el marco inferior, presente en todas las planchas excepto la III — identifica esta como la plancha de impresión VI.",
)
add("Tisková deska", "Printing plate", "Planche d'impression", "Druckplatte", "Plancha de impresión")
add("VI", "VI", "VI", "VI", "VI")

with io.open(PATH, "w", encoding="utf-8") as f:
    json.dump(cat, f, ensure_ascii=False, indent=1, sort_keys=True)

print("added", added, "skipped(existing)", skipped, "total", len(cat))
