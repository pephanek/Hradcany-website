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
        # ensure file listed
        if FILE not in cat[k].get("files", []):
            cat[k]["files"].append(FILE)
        skipped += 1
        return
    cat[k] = {"cs": cs, "en": en, "fr": fr, "de": de, "es": es, "files": [FILE], "tag": tag}
    added += 1

add(
 "V horní části kresby při pravém okraji, poblíž nápisu „POŠTA“.",
 "In the upper part of the design, right of the “POŠTA” inscription.",
 "Dans la partie supérieure du dessin, à droite de l'inscription « POŠTA ».",
 "Im oberen Teil der Zeichnung, rechts von der Inschrift „POŠTA“.",
 "En la parte superior del dibujo, a la derecha de la inscripción «POŠTA».",
)
add(
 "V levé části siluety Hradčan.",
 "In the left part of the Hradčany skyline.",
 "Dans la partie gauche de la silhouette de Hradčany.",
 "Im linken Teil der Hradschin-Silhouette.",
 "En la parte izquierda de la silueta de Hradčany.",
)
add(
 "Uprostřed siluety Hradčan.",
 "In the middle of the Hradčany skyline.",
 "Au milieu de la silhouette de Hradčany.",
 "In der Mitte der Hradschin-Silhouette.",
 "En el centro de la silueta de Hradčany.",
)
add(
 "V pravé části siluety Hradčan.",
 "In the right part of the Hradčany skyline.",
 "Dans la partie droite de la silhouette de Hradčany.",
 "Im rechten Teil der Hradschin-Silhouette.",
 "En la parte derecha de la silueta de Hradčany.",
)
add(
 "Pod siluetou hradu při levém okraji.",
 "Below the castle skyline, near the left edge.",
 "Sous la silhouette du château, près du bord gauche.",
 "Unterhalb der Burgsilhouette, nahe dem linken Rand.",
 "Bajo la silueta del castillo, cerca del borde izquierdo.",
)
add(
 "V nápisu „ČESKO-SLOVENSKO“ vlevo.",
 "In the “ČESKO-SLOVENSKO” inscription, on the left.",
 "Dans l'inscription « ČESKO-SLOVENSKO », à gauche.",
 "In der Inschrift „ČESKO-SLOVENSKO“, links.",
 "En la inscripción «ČESKO-SLOVENSKO», a la izquierda.",
)
add(
 "V dolní ozdobě rámu vlevo od hodnotového oválu.",
 "In the lower ornament of the frame, left of the value oval.",
 "Dans l'ornement inférieur du cadre, à gauche de l'ovale de valeur.",
 "In der unteren Rahmenverzierung, links vom Wertoval.",
 "En el ornamento inferior del marco, a la izquierda del óvalo de valor.",
)
add(
 "U hodnotového oválu s číslicí 15.",
 "Near the value oval with the figure 15.",
 "Près de l'ovale de valeur portant le chiffre 15.",
 "Beim Wertoval mit der Ziffer 15.",
 "Junto al óvalo de valor con la cifra 15.",
)
add(
 "V dolní ozdobě rámu vpravo od hodnotového oválu.",
 "In the lower ornament of the frame, right of the value oval.",
 "Dans l'ornement inférieur du cadre, à droite de l'ovale de valeur.",
 "In der unteren Rahmenverzierung, rechts vom Wertoval.",
 "En el ornamento inferior del marco, a la derecha del óvalo de valor.",
)
add(
 "Skutečný prstýnek v mezeře pod siluetou hradu — viz detail níže.",
 "A genuine ring below the castle skyline — see the detail below.",
 "Un véritable petit anneau sous la silhouette du château — voir le détail ci-dessous.",
 "Ein echter Ring unterhalb der Burgsilhouette — siehe Detail unten.",
 "Un anillo genuino bajo la silueta del castillo — véase el detalle más abajo.",
)
add(
 "Plná skvrna v mezeře mezi věžemi — viz detail níže.",
 "A solid spot in the gap between the towers — see the detail below.",
 "Une tache pleine dans l'interstice entre les tours — voir le détail ci-dessous.",
 "Ein voller Fleck in der Lücke zwischen den Türmen — siehe Detail unten.",
 "Una mancha maciza en el hueco entre las torres — véase el detalle más abajo.",
)

with io.open(PATH, "w", encoding="utf-8") as f:
    json.dump(cat, f, ensure_ascii=False, indent=1, sort_keys=True)

print("added", added, "skipped(existing)", skipped, "total", len(cat))
