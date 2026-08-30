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

# --- h3 title ---
add(
 "Bílé skvrny",
 "Blank spots",
 "Taches blanches",
 "Weiße Flecken",
 "Manchas blancas",
)

# --- intro paragraph ---
add(
 "Na místě, kde měl být normální sytý tisk, chybí barva úplně — bílá skvrna má ostrou hranici a nenavazuje na žádnou tištěnou linku ani vyvýšený prvek kresby, jak je tomu u závoje. Poloha, velikost i tvar se u jednotlivých kusů liší a neváže se na jedno známkové pole.",
 "Where the print should be solidly inked, the colour is missing altogether — a blank spot has a sharp boundary and does not run on from any printed line or raised design element, the way a smear (závoj) does. Its position, size and shape differ from copy to copy and are not tied to one stamp field.",
 "Là où l'impression aurait dû être pleine et dense, la couleur manque entièrement — une tache blanche a un contour net et ne prolonge aucune ligne imprimée ni aucun élément en relief du dessin, contrairement au voile (závoj). Sa position, sa taille et sa forme varient d'un exemplaire à l'autre et ne sont liées à aucun champ précis de la planche.",
 "Dort, wo ein normaler, satter Druck sein sollte, fehlt die Farbe vollständig — ein weißer Fleck hat eine scharfe Kontur und schließt sich nicht an eine gedruckte Linie oder ein erhabenes Zeichnungselement an, wie es beim Schleier (závoj) der Fall ist. Lage, Größe und Form unterscheiden sich von Stück zu Stück und sind an kein bestimmtes Markenfeld gebunden.",
 "Donde debería haber una impresión normal y densa, falta el color por completo — una mancha blanca tiene un límite nítido y no continúa ninguna línea impresa ni ningún elemento en relieve del dibujo, como ocurre con el velo (závoj). Su posición, tamaño y forma varían de una pieza a otra y no están ligados a un campo concreto de la plancha.",
)

# --- h4: Jak vada vznikla ---
add(
 "Jak vada vznikla",
 "How the flaw arose",
 "Comment le défaut est apparu",
 "Wie der Fehler entstand",
 "Cómo se originó el defecto",
)

add(
 "Mezi obarvení formy a přítisk papíru se na už natřenou barvu položil cizí objekt — smítko prachu, vlákno, drobný odštěpek nebo třeba vlásek. Objekt je nenasákavý a sedí nad barvou o zlomek milimetru výš, takže se v tom místě papír s barvou vůbec nedotkne. Zbytek tisku zůstává beze změny; jakmile se objekt při dalším tisku posunul nebo setřel, mizí spolu s ním i vada — proto se skvrna neopakuje na stejném místě a u dalších kusů se objeví jinde, nebo vůbec.",
 "Between the inking of the forme and the impression of the paper, a foreign object settled on top of the already-applied ink — a speck of dust, a fibre, a small chip, or perhaps a hair. Being non-absorbent, the object sits a fraction of a millimetre above the ink, so at that one point the paper never actually touches it. The rest of the impression is unaffected; once the object shifted or was brushed away before the next impression, the flaw disappears with it — which is why the spot never repeats at the same place and turns up differently, or not at all, on other copies.",
 "Entre l'encrage de la forme et le passage du papier, un corps étranger s'est déposé sur l'encre déjà appliquée — un grain de poussière, une fibre, un petit éclat, voire un cheveu. N'étant pas absorbant, l'objet repose à une fraction de millimètre au-dessus de l'encre, si bien qu'à cet endroit précis le papier ne la touche jamais. Le reste de l'impression n'est pas affecté ; dès que l'objet s'est déplacé ou a été balayé avant le tirage suivant, le défaut disparaît avec lui — c'est pourquoi la tache ne se reproduit jamais au même endroit et apparaît ailleurs, ou pas du tout, sur d'autres exemplaires.",
 "Zwischen dem Einfärben der Druckform und dem Abdruck auf dem Papier setzte sich ein Fremdkörper auf die bereits aufgetragene Farbe — ein Staubkorn, eine Faser, ein kleiner Span oder sogar ein Haar. Da der Gegenstand nicht saugfähig ist, liegt er einen Bruchteil eines Millimeters über der Farbe, sodass das Papier sie an dieser Stelle nie berührt. Der Rest des Abdrucks bleibt unverändert; sobald sich der Gegenstand vor dem nächsten Druck verschob oder abgewischt wurde, verschwand der Fehler mit ihm — deshalb wiederholt sich der Fleck nie an derselben Stelle und tritt bei anderen Stücken anders oder gar nicht auf.",
 "Entre el entintado de la forma y la impresión del papel, un cuerpo extraño se posó sobre la tinta ya aplicada: una mota de polvo, una fibra, una pequeña astilla o incluso un cabello. Al no ser absorbente, el objeto queda una fracción de milímetro por encima de la tinta, de modo que en ese punto el papel nunca llega a tocarla. El resto de la impresión no se ve afectado; en cuanto el objeto se desplazó o fue retirado antes de la siguiente impresión, el defecto desapareció con él, por lo que la mancha nunca se repite en el mismo lugar y aparece de forma distinta, o no aparece, en otras piezas.",
)

# --- diagram texts ---
add(
 "cizí objekt (smítko, vlásek)",
 "foreign object (speck, hair)",
 "corps étranger (grain, cheveu)",
 "Fremdkörper (Staubkorn, Haar)",
 "objeto extraño (mota, cabello)",
)
add(
 "usadil se až na už nanesené barvě",
 "settled on top of the already-applied ink",
 "s'est déposé sur l'encre déjà appliquée",
 "setzte sich auf die bereits aufgetragene Farbe",
 "se posó sobre la tinta ya aplicada",
)
add(
 "→ bílá skvrna",
 "→ blank spot",
 "→ tache blanche",
 "→ weißer Fleck",
 "→ mancha blanca",
)
add(
 "jinde barva přejde beze změny",
 "elsewhere the ink transfers unchanged",
 "ailleurs, l'encre se transfère sans changement",
 "anderswo überträgt sich die Farbe unverändert",
 "en otras zonas la tinta se transfiere sin cambios",
)
add(
 "→ ostrá skvrna bez barvy",
 "→ a sharp spot with no ink",
 "→ une tache nette sans encre",
 "→ ein scharfer Fleck ohne Farbe",
 "→ una mancha nítida sin tinta",
)

# --- diagram figcaption ---
add(
 "Mezi obarvením formy a přítiskem papíru se na už nanesenou barvu položil cizí objekt — v místě, kde sedí, se papír s barvou vůbec nedotkne. Zbytek tisku zůstává beze změny.",
 "Between the inking of the forme and the impression of the paper, a foreign object settled on top of the already-applied ink — where it sits, the paper never actually touches the ink. The rest of the impression is unaffected.",
 "Entre l'encrage de la forme et le passage du papier, un corps étranger s'est déposé sur l'encre déjà appliquée — à l'endroit où il repose, le papier ne touche jamais l'encre. Le reste de l'impression n'est pas affecté.",
 "Zwischen dem Einfärben der Druckform und dem Abdruck auf dem Papier setzte sich ein Fremdkörper auf die bereits aufgetragene Farbe — dort, wo er liegt, berührt das Papier die Farbe nie. Der Rest des Abdrucks bleibt unverändert.",
 "Entre el entintado de la forma y la impresión del papel, un cuerpo extraño se posó sobre la tinta ya aplicada — donde se encuentra, el papel nunca llega a tocar la tinta. El resto de la impresión no se ve afectado.",
)

# --- h4: Proc to neni svetlina ---
add(
 "Proč to není světlina",
 "Why this is not a white spot (světlina)",
 "Pourquoi ce n'est pas une éclaircie (světlina)",
 "Warum dies keine Lichtstelle (světlina) ist",
 "Por qué esto no es una clara (světlina)",
)
add(
 "Světlina vzniká trvalým poškozením nebo zanesením konkrétního místa desky a vrací se proto na stejném známkovém poli při každém tisku — hranice je navíc měkká, protože ubývání barvy se vyvíjí postupně. Bílá skvrna je naopak jednorázová: způsobil ji volný předmět, který mezi tisky zmizel, hranice je proto ostrá a poloha se u jednotlivých kusů mění.",
 "A světlina arises from permanent damage or clogging at one specific point of the plate, so it recurs at the same stamp field on every impression — and its edge is soft, because the loss of ink develops gradually. A blank spot, by contrast, is a one-off: it was caused by a loose object that was gone by the next impression, so its edge is sharp and its position changes from copy to copy.",
 "Une éclaircie (světlina) résulte d'une dégradation permanente ou d'un encrassement à un point précis de la planche, et revient donc au même champ de la planche à chaque tirage — son contour est en outre flou, car la perte d'encre se développe progressivement. La tache blanche, elle, est ponctuelle : elle a été causée par un objet mobile disparu avant le tirage suivant, son contour est donc net et sa position change d'un exemplaire à l'autre.",
 "Eine Lichtstelle (světlina) entsteht durch dauerhafte Beschädigung oder Verstopfung an einer bestimmten Stelle der Platte und kehrt daher bei jedem Druck am selben Markenfeld wieder — ihr Rand ist zudem weich, da der Farbverlust sich allmählich entwickelt. Ein weißer Fleck dagegen ist einmalig: Er wurde durch ein loses Objekt verursacht, das beim nächsten Druck schon verschwunden war, sein Rand ist daher scharf und seine Position ändert sich von Stück zu Stück.",
 "Una clara (světlina) surge de un daño permanente o de una obstrucción en un punto concreto de la plancha, por lo que reaparece en el mismo campo en cada impresión, y además su borde es difuso, porque la pérdida de tinta se desarrolla de forma gradual. La mancha blanca, en cambio, es un hecho puntual: la causó un objeto suelto que ya no estaba en la siguiente impresión, por lo que su borde es nítido y su posición cambia de una pieza a otra.",
)

# --- h4: Proc to neni zvrasneni ---
add(
 "Proč to není zvrásnění",
 "Why this is not creasing",
 "Pourquoi ce n'est pas un plissement",
 "Warum dies keine Faltenbildung ist",
 "Por qué esto no es un plegado",
)
add(
 "Zvrásnění vzniká přeložením vlhkého papíru ještě před tiskem: v ohybu chybí barva, ale hlavně se kresba na obou stranách přeložení navzájem posune a nenavazuje na sebe, protože se papír po rozložení „roztáhl\". U bílé skvrny je papír zcela v pořádku — žádná rýha, žádné posunutí kresby, chybí jen barva na jednom ohraničeném místě.",
 "Creasing arises from a fold in the damp paper before printing: ink is missing in the fold, but above all the design is displaced on the two sides of the fold and fails to line up, because the paper \"stretched\" once it was unfolded. With a blank spot the paper is entirely sound — no crease, no displacement of the design; only the ink is missing at one bounded spot.",
 "Le plissement provient d'un pli dans le papier humide avant l'impression : l'encre manque dans le pli, mais surtout le dessin se décale de part et d'autre du pli et ne se raccorde plus, car le papier s'est « étiré » une fois déplié. Avec une tache blanche, le papier est parfaitement intact — aucun pli, aucun décalage du dessin ; seule l'encre manque à un endroit délimité.",
 "Faltenbildung entsteht durch eine Faltung des feuchten Papiers noch vor dem Druck: In der Falte fehlt Farbe, vor allem aber verschiebt sich die Zeichnung auf beiden Seiten der Falte gegeneinander und passt nicht mehr zusammen, weil sich das Papier nach dem Entfalten „gedehnt\" hat. Beim weißen Fleck ist das Papier völlig unversehrt — keine Rille, keine Verschiebung der Zeichnung; es fehlt nur die Farbe an einer begrenzten Stelle.",
 "El plegado se produce por un doblez en el papel húmedo antes de la impresión: falta tinta en el pliegue, pero sobre todo el dibujo se desplaza a ambos lados del pliegue y deja de coincidir, porque el papel se \"estiró\" al desdoblarse. En la mancha blanca el papel está perfectamente intacto — sin ninguna raya, sin desplazamiento del dibujo; solo falta la tinta en un punto delimitado.",
)

# --- h4: Proc to neni drivko/smitko ---
add(
 "Proč to není dřívko nebo smítko",
 "Why this is not a splinter or a speck",
 "Pourquoi ce n'est pas une esquille ou une impureté",
 "Warum dies kein Holzsplitter oder Fremdkörper im Papier ist",
 "Por qué esto no es una astilla o una mota incrustada",
)
add(
 "Dřívko i smítko jsou cizí objekty zalisované přímo v papíru už při jeho výrobě, a proto jsou vidět z obou stran známky — na líci narušují tisk, na rubu je znát jejich obrys. Objekt, který způsobil bílou skvrnu, ležel jen na tiskové formě: rub je proto úplně čistý, bez jakékoli stopy.",
 "A splinter or a speck is a foreign object pressed directly into the paper while it was being made, so it shows on both sides of the stamp — on the face it disturbs the print, on the back its outline is visible. The object that caused a blank spot lay only on the printing forme: the back is therefore completely clean, without any trace at all.",
 "Une esquille comme une impureté sont des corps étrangers incorporés directement dans le papier lors de sa fabrication, et sont donc visibles des deux côtés du timbre — au recto ils perturbent l'impression, au verso leur contour est visible. L'objet à l'origine de la tache blanche ne se trouvait que sur la forme d'impression : le verso est donc parfaitement propre, sans aucune trace.",
 "Sowohl Holzsplitter als auch Fremdkörper sind Objekte, die bereits bei der Papierherstellung direkt ins Papier eingepresst wurden, und sind daher auf beiden Seiten der Marke sichtbar — auf der Vorderseite stören sie den Druck, auf der Rückseite ist ihr Umriss erkennbar. Das Objekt, das den weißen Fleck verursachte, lag nur auf der Druckform: Die Rückseite ist daher völlig sauber, ohne jede Spur.",
 "Tanto la astilla como la mota son cuerpos extraños incrustados directamente en el papel durante su fabricación, por lo que se ven en ambas caras del sello: en el anverso alteran la impresión, en el reverso se aprecia su contorno. El objeto que causó la mancha blanca se encontraba solo sobre la forma de impresión: el reverso está, por tanto, completamente limpio, sin rastro alguno.",
)

# --- h4: Ukazky ze sbirky (likely already exists from other sections, but ensure) ---
add(
 "Ukázky ze sbírky",
 "Specimens from the collection",
 "Exemplaires de la collection",
 "Beispiele aus der Sammlung",
 "Ejemplares de la colección",
)

# --- gallery item captions (bare) ---
add(
 "Velká skvrna v levém dolním rohu, pod nápisem ČESKO-SLOVENSKA — nejvýraznější doložený kus.",
 "A large spot in the bottom left corner, below the ČESKO-SLOVENSKA inscription — the most pronounced copy recorded.",
 "Une grande tache dans le coin inférieur gauche, sous l'inscription ČESKO-SLOVENSKA — l'exemplaire le plus marqué recensé.",
 "Ein großer Fleck in der unteren linken Ecke, unterhalb der Inschrift ČESKO-SLOVENSKA — das am stärksten ausgeprägte belegte Stück.",
 "Una gran mancha en la esquina inferior izquierda, bajo la inscripción ČESKO-SLOVENSKA — el ejemplar más marcado documentado.",
)
add(
 "Velmi jemná, sotva znatelná skvrna v nápisu SLOVENSKO a v ozdobě vedle hodnotového oválu — nejslabší doložený případ.",
 "A very faint, barely visible spot in the SLOVENSKO inscription and in the ornament beside the value oval — the faintest copy recorded.",
 "Une tache très légère, à peine perceptible, dans l'inscription SLOVENSKO et dans l'ornement près de l'ovale de valeur — le cas le plus discret recensé.",
 "Ein sehr feiner, kaum wahrnehmbarer Fleck in der Inschrift SLOVENSKO und in der Verzierung neben dem Wertoval — der schwächste belegte Fall.",
 "Una mancha muy tenue, apenas perceptible, en la inscripción SLOVENSKO y en el ornamento junto al óvalo de valor — el caso más leve documentado.",
)
add(
 "Ostře ohraničená skvrna přes patu hradu a písmeno L v nápisu ČESKO-SLOVENSKA — písmeno úplně mizí.",
 "A sharply bounded spot across the base of the castle and the letter L of the ČESKO-SLOVENSKA inscription — the letter disappears completely.",
 "Une tache aux contours nets traversant la base du château et la lettre L de l'inscription ČESKO-SLOVENSKA — la lettre disparaît complètement.",
 "Ein scharf begrenzter Fleck über dem Burgsockel und dem Buchstaben L der Inschrift ČESKO-SLOVENSKA — der Buchstabe verschwindet vollständig.",
 "Una mancha de bordes nítidos que atraviesa la base del castillo y la letra L de la inscripción ČESKO-SLOVENSKA — la letra desaparece por completo.",
)
add(
 "Šikmá skvrna přes věže, nápis i hodnotový ovál, z části skrytá pod razítkem.",
 "A diagonal spot across the towers, the inscription and the value oval, partly hidden under the cancel.",
 "Une tache oblique traversant les tours, l'inscription et l'ovale de valeur, en partie masquée par l'oblitération.",
 "Ein diagonaler Fleck über den Türmen, der Inschrift und dem Wertoval, teilweise unter dem Stempel verborgen.",
 "Una mancha diagonal que atraviesa las torres, la inscripción y el óvalo de valor, parcialmente oculta bajo el matasellos.",
)

# --- gallery item captions (numbered "Kus N -"/"Item N -" variants) ---
add(
 "Kus 1 — Velká skvrna v levém dolním rohu, pod nápisem ČESKO-SLOVENSKA — nejvýraznější doložený kus.",
 "Item 1 — A large spot in the bottom left corner, below the ČESKO-SLOVENSKA inscription — the most pronounced copy recorded.",
 "Pièce 1 — Une grande tache dans le coin inférieur gauche, sous l'inscription ČESKO-SLOVENSKA — l'exemplaire le plus marqué recensé.",
 "Stück 1 — Ein großer Fleck in der unteren linken Ecke, unterhalb der Inschrift ČESKO-SLOVENSKA — das am stärksten ausgeprägte belegte Stück.",
 "Pieza 1 — Una gran mancha en la esquina inferior izquierda, bajo la inscripción ČESKO-SLOVENSKA — el ejemplar más marcado documentado.",
)
add(
 "Kus 2 — Velmi jemná, sotva znatelná skvrna v nápisu SLOVENSKO a v ozdobě vedle hodnotového oválu — nejslabší doložený případ.",
 "Item 2 — A very faint, barely visible spot in the SLOVENSKO inscription and in the ornament beside the value oval — the faintest copy recorded.",
 "Pièce 2 — Une tache très légère, à peine perceptible, dans l'inscription SLOVENSKO et dans l'ornement près de l'ovale de valeur — le cas le plus discret recensé.",
 "Stück 2 — Ein sehr feiner, kaum wahrnehmbarer Fleck in der Inschrift SLOVENSKO und in der Verzierung neben dem Wertoval — der schwächste belegte Fall.",
 "Pieza 2 — Una mancha muy tenue, apenas perceptible, en la inscripción SLOVENSKO y en el ornamento junto al óvalo de valor — el caso más leve documentado.",
)
add(
 "Kus 3 — Ostře ohraničená skvrna přes patu hradu a písmeno L v nápisu ČESKO-SLOVENSKA — písmeno úplně mizí.",
 "Item 3 — A sharply bounded spot across the base of the castle and the letter L of the ČESKO-SLOVENSKA inscription — the letter disappears completely.",
 "Pièce 3 — Une tache aux contours nets traversant la base du château et la lettre L de l'inscription ČESKO-SLOVENSKA — la lettre disparaît complètement.",
 "Stück 3 — Ein scharf begrenzter Fleck über dem Burgsockel und dem Buchstaben L der Inschrift ČESKO-SLOVENSKA — der Buchstabe verschwindet vollständig.",
 "Pieza 3 — Una mancha de bordes nítidos que atraviesa la base del castillo y la letra L de la inscripción ČESKO-SLOVENSKA — la letra desaparece por completo.",
)
add(
 "Kus 4 — Šikmá skvrna přes věže, nápis i hodnotový ovál, z části skrytá pod razítkem.",
 "Item 4 — A diagonal spot across the towers, the inscription and the value oval, partly hidden under the cancel.",
 "Pièce 4 — Une tache oblique traversant les tours, l'inscription et l'ovale de valeur, en partie masquée par l'oblitération.",
 "Stück 4 — Ein diagonaler Fleck über den Türmen, der Inschrift und dem Wertoval, teilweise unter dem Stempel verborgen.",
 "Pieza 4 — Una mancha diagonal que atraviesa las torres, la inscripción y el óvalo de valor, parcialmente oculta bajo el matasellos.",
)

# --- detail figure captions ---
add(
 "Detail kusu 3 — skvrna úplně vymazává písmeno L a zasahuje i do paty hradu. Hranice je ostrá po celém obvodu.",
 "Detail of item 3 — the spot completely erases the letter L and reaches into the base of the castle. The boundary is sharp all the way round.",
 "Détail de la pièce 3 — la tache efface complètement la lettre L et empiète sur la base du château. Le contour est net sur tout le pourtour.",
 "Detail von Stück 3 — der Fleck löscht den Buchstaben L vollständig aus und reicht bis in den Burgsockel hinein. Die Kontur ist rundum scharf.",
 "Detalle de la pieza 3 — la mancha borra por completo la letra L y alcanza también la base del castillo. El borde es nítido en todo su contorno.",
)
add(
 "Detail kusu 1 — v ploše skvrny přežily jen dvě drobné ostrůvky barvy, jinak je hranice čistá a nepřechází plynule do bílé.",
 "Detail of item 1 — only two tiny islands of ink survive within the spot; otherwise the boundary is clean and does not fade gradually into white.",
 "Détail de la pièce 1 — seuls deux minuscules îlots d'encre subsistent dans la tache ; le contour est par ailleurs net et ne s'estompe pas progressivement vers le blanc.",
 "Detail von Stück 1 — innerhalb des Flecks überleben nur zwei winzige Farbinseln; ansonsten ist die Kontur sauber und geht nicht allmählich ins Weiß über.",
 "Detalle de la pieza 1 — dentro de la mancha solo sobreviven dos pequeñas islas de tinta; por lo demás, el borde es limpio y no se difumina gradualmente hacia el blanco.",
)

with io.open(PATH, "w", encoding="utf-8") as f:
    json.dump(cat, f, ensure_ascii=False, indent=1, sort_keys=True)

print("added", added, "skipped(existing)", skipped, "total", len(cat))
