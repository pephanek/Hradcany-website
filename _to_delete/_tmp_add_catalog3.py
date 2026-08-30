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
 'Kus 1 — V nápisu „ČESKO-SLOVENSKO“ vlevo.',
 'Item 1 — In the “ČESKO-SLOVENSKO” inscription, on the left.',
 "Pièce 1 — Dans l'inscription « ČESKO-SLOVENSKO », à gauche.",
 'Stück 1 — In der Inschrift „ČESKO-SLOVENSKO“, links.',
 'Ejemplar 1 — En la inscripción «ČESKO-SLOVENSKO», a la izquierda.',
)
add(
 'Kus 2 — V levé části siluety Hradčan.',
 'Item 2 — In the left part of the Hradčany skyline.',
 'Pièce 2 — Dans la partie gauche de la silhouette de Hradčany.',
 'Stück 2 — Im linken Teil der Hradschin-Silhouette.',
 'Ejemplar 2 — En la parte izquierda de la silueta de Hradčany.',
)
add(
 'Kus 3 — V levé části siluety Hradčan.',
 'Item 3 — In the left part of the Hradčany skyline.',
 'Pièce 3 — Dans la partie gauche de la silhouette de Hradčany.',
 'Stück 3 — Im linken Teil der Hradschin-Silhouette.',
 'Ejemplar 3 — En la parte izquierda de la silueta de Hradčany.',
)
add(
 'Kus 4 — Uprostřed siluety Hradčan.',
 'Item 4 — In the middle of the Hradčany skyline.',
 'Pièce 4 — Au milieu de la silhouette de Hradčany.',
 'Stück 4 — In der Mitte der Hradschin-Silhouette.',
 'Ejemplar 4 — En el centro de la silueta de Hradčany.',
)
add(
 'Kus 5 — V levé části siluety Hradčan.',
 'Item 5 — In the left part of the Hradčany skyline.',
 'Pièce 5 — Dans la partie gauche de la silhouette de Hradčany.',
 'Stück 5 — Im linken Teil der Hradschin-Silhouette.',
 'Ejemplar 5 — En la parte izquierda de la silueta de Hradčany.',
)
add(
 'Kus 6 — V levé části siluety Hradčan.',
 'Item 6 — In the left part of the Hradčany skyline.',
 'Pièce 6 — Dans la partie gauche de la silhouette de Hradčany.',
 'Stück 6 — Im linken Teil der Hradschin-Silhouette.',
 'Ejemplar 6 — En la parte izquierda de la silueta de Hradčany.',
)
add(
 'Kus 7 — Skutečný prstýnek v mezeře pod siluetou hradu — viz detail níže.',
 'Item 7 — A genuine ring below the castle skyline — see the detail below.',
 'Pièce 7 — Un véritable petit anneau sous la silhouette du château — voir le détail ci-dessous.',
 'Stück 7 — Ein echter Ring unterhalb der Burgsilhouette — siehe Detail unten.',
 'Ejemplar 7 — Un anillo genuino bajo la silueta del castillo — véase el detalle más abajo.',
)
add(
 'Kus 8 — Plná skvrna v mezeře mezi věžemi — viz detail níže.',
 'Item 8 — A solid spot in the gap between the towers — see the detail below.',
 "Pièce 8 — Une tache pleine dans l'interstice entre les tours — voir le détail ci-dessous.",
 'Stück 8 — Ein voller Fleck in der Lücke zwischen den Türmen — siehe Detail unten.',
 'Ejemplar 8 — Una mancha maciza en el hueco entre las torres — véase el detalle más abajo.',
)
add(
 'Kus 9 — V dolní ozdobě rámu vpravo od hodnotového oválu.',
 'Item 9 — In the lower ornament of the frame, right of the value oval.',
 "Pièce 9 — Dans l'ornement inférieur du cadre, à droite de l'ovale de valeur.",
 'Stück 9 — In der unteren Rahmenverzierung, rechts vom Wertoval.',
 'Ejemplar 9 — En el ornamento inferior del marco, a la derecha del óvalo de valor.',
)
add(
 'Kus 10 — V dolní ozdobě rámu vlevo od hodnotového oválu.',
 'Item 10 — In the lower ornament of the frame, left of the value oval.',
 "Pièce 10 — Dans l'ornement inférieur du cadre, à gauche de l'ovale de valeur.",
 'Stück 10 — In der unteren Rahmenverzierung, links vom Wertoval.',
 'Ejemplar 10 — En el ornamento inferior del marco, a la izquierda del óvalo de valor.',
)
add(
 'Kus 11 — V horní části kresby při pravém okraji, poblíž nápisu „POŠTA“.',
 'Item 11 — In the upper part of the design, right of the “POŠTA” inscription.',
 "Pièce 11 — Dans la partie supérieure du dessin, à droite de l'inscription « POŠTA ».",
 'Stück 11 — Im oberen Teil der Zeichnung, rechts von der Inschrift „POŠTA“.',
 'Ejemplar 11 — En la parte superior del dibujo, a la derecha de la inscripción «POŠTA».',
)
add(
 'Kus 12 — V levé části siluety Hradčan.',
 'Item 12 — In the left part of the Hradčany skyline.',
 'Pièce 12 — Dans la partie gauche de la silhouette de Hradčany.',
 'Stück 12 — Im linken Teil der Hradschin-Silhouette.',
 'Ejemplar 12 — En la parte izquierda de la silueta de Hradčany.',
)
add(
 'Kus 13 — V levé části siluety Hradčan.',
 'Item 13 — In the left part of the Hradčany skyline.',
 'Pièce 13 — Dans la partie gauche de la silhouette de Hradčany.',
 'Stück 13 — Im linken Teil der Hradschin-Silhouette.',
 'Ejemplar 13 — En la parte izquierda de la silueta de Hradčany.',
)
add(
 'Kus 1 — V dolní ozdobě rámu vpravo od hodnotového oválu.',
 'Item 1 — In the lower ornament of the frame, right of the value oval.',
 "Pièce 1 — Dans l'ornement inférieur du cadre, à droite de l'ovale de valeur.",
 'Stück 1 — In der unteren Rahmenverzierung, rechts vom Wertoval.',
 'Ejemplar 1 — En el ornamento inferior del marco, a la derecha del óvalo de valor.',
)
add(
 'Kus 2 — Pod siluetou hradu při levém okraji.',
 'Item 2 — Below the castle skyline, near the left edge.',
 'Pièce 2 — Sous la silhouette du château, près du bord gauche.',
 'Stück 2 — Unterhalb der Burgsilhouette, nahe dem linken Rand.',
 'Ejemplar 2 — Bajo la silueta del castillo, cerca del borde izquierdo.',
)
add(
 'Kus 3 — Uprostřed siluety Hradčan.',
 'Item 3 — In the middle of the Hradčany skyline.',
 'Pièce 3 — Au milieu de la silhouette de Hradčany.',
 'Stück 3 — In der Mitte der Hradschin-Silhouette.',
 'Ejemplar 3 — En el centro de la silueta de Hradčany.',
)
add(
 'Kus 4 — Uprostřed siluety Hradčan.',
 'Item 4 — In the middle of the Hradčany skyline.',
 'Pièce 4 — Au milieu de la silhouette de Hradčany.',
 'Stück 4 — In der Mitte der Hradschin-Silhouette.',
 'Ejemplar 4 — En el centro de la silueta de Hradčany.',
)
add(
 'Kus 5 — Uprostřed siluety Hradčan.',
 'Item 5 — In the middle of the Hradčany skyline.',
 'Pièce 5 — Au milieu de la silhouette de Hradčany.',
 'Stück 5 — In der Mitte der Hradschin-Silhouette.',
 'Ejemplar 5 — En el centro de la silueta de Hradčany.',
)
add(
 'Kus 6 — Uprostřed siluety Hradčan.',
 'Item 6 — In the middle of the Hradčany skyline.',
 'Pièce 6 — Au milieu de la silhouette de Hradčany.',
 'Stück 6 — In der Mitte der Hradschin-Silhouette.',
 'Ejemplar 6 — En el centro de la silueta de Hradčany.',
)
add(
 'Kus 7 — U hodnotového oválu s číslicí 15.',
 'Item 7 — Near the value oval with the figure 15.',
 "Pièce 7 — Près de l'ovale de valeur portant le chiffre 15.",
 'Stück 7 — Beim Wertoval mit der Ziffer 15.',
 'Ejemplar 7 — Junto al óvalo de valor con la cifra 15.',
)
add(
 'Kus 8 — V pravé části siluety Hradčan.',
 'Item 8 — In the right part of the Hradčany skyline.',
 'Pièce 8 — Dans la partie droite de la silhouette de Hradčany.',
 'Stück 8 — Im rechten Teil der Hradschin-Silhouette.',
 'Ejemplar 8 — En la parte derecha de la silueta de Hradčany.',
)
add(
 'Kus 9 — Uprostřed siluety Hradčan.',
 'Item 9 — In the middle of the Hradčany skyline.',
 'Pièce 9 — Au milieu de la silhouette de Hradčany.',
 'Stück 9 — In der Mitte der Hradschin-Silhouette.',
 'Ejemplar 9 — En el centro de la silueta de Hradčany.',
)
add(
 'Kus 10 — V levé části siluety Hradčan.',
 'Item 10 — In the left part of the Hradčany skyline.',
 'Pièce 10 — Dans la partie gauche de la silhouette de Hradčany.',
 'Stück 10 — Im linken Teil der Hradschin-Silhouette.',
 'Ejemplar 10 — En la parte izquierda de la silueta de Hradčany.',
)
add(
 'Kus 11 — Uprostřed siluety Hradčan.',
 'Item 11 — In the middle of the Hradčany skyline.',
 'Pièce 11 — Au milieu de la silhouette de Hradčany.',
 'Stück 11 — In der Mitte der Hradschin-Silhouette.',
 'Ejemplar 11 — En el centro de la silueta de Hradčany.',
)
add(
 'Kus 12 — V nápisu „ČESKO-SLOVENSKO“ vlevo.',
 'Item 12 — In the “ČESKO-SLOVENSKO” inscription, on the left.',
 "Pièce 12 — Dans l'inscription « ČESKO-SLOVENSKO », à gauche.",
 'Stück 12 — In der Inschrift „ČESKO-SLOVENSKO“, links.',
 'Ejemplar 12 — En la inscripción «ČESKO-SLOVENSKO», a la izquierda.',
)
add(
 'Kus 13 — Uprostřed siluety Hradčan.',
 'Item 13 — In the middle of the Hradčany skyline.',
 'Pièce 13 — Au milieu de la silhouette de Hradčany.',
 'Stück 13 — In der Mitte der Hradschin-Silhouette.',
 'Ejemplar 13 — En el centro de la silueta de Hradčany.',
)
add(
 'Kus 14 — V levé části siluety Hradčan.',
 'Item 14 — In the left part of the Hradčany skyline.',
 'Pièce 14 — Dans la partie gauche de la silhouette de Hradčany.',
 'Stück 14 — Im linken Teil der Hradschin-Silhouette.',
 'Ejemplar 14 — En la parte izquierda de la silueta de Hradčany.',
)
add(
 'Kus 15 — U hodnotového oválu s číslicí 15.',
 'Item 15 — Near the value oval with the figure 15.',
 "Pièce 15 — Près de l'ovale de valeur portant le chiffre 15.",
 'Stück 15 — Beim Wertoval mit der Ziffer 15.',
 'Ejemplar 15 — Junto al óvalo de valor con la cifra 15.',
)
add(
 'Kus 16 — U hodnotového oválu s číslicí 15.',
 'Item 16 — Near the value oval with the figure 15.',
 "Pièce 16 — Près de l'ovale de valeur portant le chiffre 15.",
 'Stück 16 — Beim Wertoval mit der Ziffer 15.',
 'Ejemplar 16 — Junto al óvalo de valor con la cifra 15.',
)
add(
 'Kus 17 — V nápisu „ČESKO-SLOVENSKO“ vlevo.',
 'Item 17 — In the “ČESKO-SLOVENSKO” inscription, on the left.',
 "Pièce 17 — Dans l'inscription « ČESKO-SLOVENSKO », à gauche.",
 'Stück 17 — In der Inschrift „ČESKO-SLOVENSKO“, links.',
 'Ejemplar 17 — En la inscripción «ČESKO-SLOVENSKO», a la izquierda.',
)
add(
 'Kus 18 — Uprostřed siluety Hradčan.',
 'Item 18 — In the middle of the Hradčany skyline.',
 'Pièce 18 — Au milieu de la silhouette de Hradčany.',
 'Stück 18 — In der Mitte der Hradschin-Silhouette.',
 'Ejemplar 18 — En el centro de la silueta de Hradčany.',
)
add(
 'Kus 19 — Uprostřed siluety Hradčan.',
 'Item 19 — In the middle of the Hradčany skyline.',
 'Pièce 19 — Au milieu de la silhouette de Hradčany.',
 'Stück 19 — In der Mitte der Hradschin-Silhouette.',
 'Ejemplar 19 — En el centro de la silueta de Hradčany.',
)

with io.open(PATH, "w", encoding="utf-8") as f:
    json.dump(cat, f, ensure_ascii=False, indent=1, sort_keys=True)

print("added", added, "skipped(existing)", skipped, "total", len(cat))