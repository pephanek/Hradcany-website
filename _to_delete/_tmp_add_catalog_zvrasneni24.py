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
 "Svislá vráska při levém okraji, na kusu s přetiskem SO 1920 (pole 92/I).",
 "A vertical crease along the left edge, on a copy with the SO 1920 overprint (field 92/I).",
 "Pli vertical le long du bord gauche, sur un exemplaire portant la surcharge SO 1920 (champ 92/I).",
 "Senkrechte Knickfalte am linken Rand, auf einem Stück mit dem Aufdruck SO 1920 (Feld 92/I).",
 "Un pliegue vertical junto al margen izquierdo, en un ejemplar con la sobrecarga SO 1920 (campo 92/I).",
)
add(
 "Kus 24 — Svislá vráska při levém okraji, na kusu s přetiskem SO 1920 (pole 92/I).",
 "Item 24 — A vertical crease along the left edge, on a copy with the SO 1920 overprint (field 92/I).",
 "Pièce 24 — Pli vertical le long du bord gauche, sur un exemplaire portant la surcharge SO 1920 (champ 92/I).",
 "Stück 24 — Senkrechte Knickfalte am linken Rand, auf einem Stück mit dem Aufdruck SO 1920 (Feld 92/I).",
 "Pieza 24 — Un pliegue vertical junto al margen izquierdo, en un ejemplar con la sobrecarga SO 1920 (campo 92/I).",
)
add(
 "Šestadvacet známek na dvaceti čtyřech kusech — dvacet dva jednotlivých, jeden nezoubkovaný vodorovný pár (kus 1) a jeden svislý pár (kus 23). Kliknutím se ukázka zvětší.",
 "Twenty-six stamps on twenty-four items — twenty-two singles, one imperforate horizontal pair (item 1) and one vertical pair (item 23). Click a specimen to enlarge it.",
 "Vingt-six timbres sur vingt-quatre pièces — vingt-deux isolés, une paire horizontale non dentelée (pièce 1) et une paire verticale (pièce 23). Cliquez sur un exemplaire pour l'agrandir.",
 "Sechsundzwanzig Marken auf vierundzwanzig Stücken — zweiundzwanzig Einzelstücke, ein ungezähntes waagerechtes Paar (Stück 1) und ein senkrechtes Paar (Stück 23). Klicken Sie auf ein Stück, um es zu vergrößern.",
 "Veintiséis sellos en veinticuatro piezas — veintidós individuales, una pareja horizontal sin dentar (pieza 1) y una pareja vertical (pieza 23). Haga clic en un ejemplar para ampliarlo.",
)

with io.open(PATH, "w", encoding="utf-8") as f:
    json.dump(cat, f, ensure_ascii=False, indent=1, sort_keys=True)

print("added", added, "skipped(existing)", skipped, "total", len(cat))
