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

# --- section 68-I ---
add(
 "ZP 68/I — černý zkušební tisk, definitivní stav kresby",
 "Field 68/I — a black proof, the design's final state",
 "Champ 68/I — une épreuve noire, l'état définitif du dessin",
 "Feld 68/I — ein schwarzer Probedruck, der endgültige Zustand der Zeichnung",
 "Campo 68/I — una prueba en negro, el estado definitivo del dibujo",
)
add(
 "Zkušební tisk 15h v černé barvě, nezoubkovaný. Známkové pole 68 první tiskové desky.",
 "A proof of the 15h in black, imperforate. Stamp field 68 of the first printing plate.",
 "Une épreuve du 15h en noir, non dentelée. Champ 68 de la première planche.",
 "Ein Probedruck der 15h in Schwarz, ungezähnt. Markenfeld 68 der ersten Druckplatte.",
 "Una prueba del 15h en negro, sin dentar. Campo 68 de la primera plancha.",
)
add(
 "černá — barva, ve které známka nikdy nevyšla",
 "black — a colour in which the stamp never appeared",
 "noir — une couleur dans laquelle le timbre n'a jamais paru",
 "schwarz — eine Farbe, in der die Marke nie erschienen ist",
 "negro — un color en el que el sello nunca se emitió",
)
add(
 "krémový, jemně strukturovaný",
 "cream, finely textured",
 "crème, à grain fin",
 "cremefarben, fein strukturiert",
 "crema, de grano fino",
)
add(
 "68 / TD I",
 "68 / plate I",
 "68 / planche I",
 "68 / Platte I",
 "68 / plancha I",
)
add(
 "shoduje se s produkčním tiskem — žádná pozdější úprava kresby",
 "matches the production printing — no later alteration to the design",
 "correspond à l'impression de production — aucune modification ultérieure du dessin",
 "stimmt mit dem Produktionsdruck überein — keine spätere Änderung der Zeichnung",
 "coincide con la impresión de producción — sin alteración posterior del dibujo",
)
add(
 "Na rozdíl od pole 96/I je tohle pole opačným příkladem. Ve srovnání s produkčním otiskem téhož pole (evidenční sada pozic desky I) je kresba shodná do posledního detailu — včetně drobné nepravidelnosti v levém horním rohu rámečku, kterou má pole 68 jako svůj identifikační znak na všech tiskových deskách. Ta je vidět stejně na zkušebním tisku i na produkčním kuse, takže tu mezi oběma otisky k žádnému zásahu do formy nedošlo.",
 "Unlike field 96/I, this field is the opposite case. Set beside the production impression of the same field (from the reference set of plate I positions), the drawing matches down to the last detail — including a small irregularity in the top left corner of the frame that field 68 carries as its identifying mark on every printing plate. It appears identically on both the proof and the production copy, so no alteration was made to the forme between the two impressions.",
 "Contrairement au champ 96/I, ce champ constitue le cas inverse. Comparé à l'impression de production du même champ (série de référence des positions de la planche I), le dessin correspond jusqu'au moindre détail — y compris une petite irrégularité dans le coin supérieur gauche du cadre, que le champ 68 porte comme marque d'identification sur toutes les planches d'impression. Elle apparaît de façon identique sur l'épreuve comme sur l'exemplaire de production : aucune intervention sur la forme n'a donc eu lieu entre les deux tirages.",
 "Im Gegensatz zu Feld 96/I ist dieses Feld der umgekehrte Fall. Im Vergleich mit dem Produktionsabdruck desselben Feldes (aus der Referenzsammlung der Positionen von Platte I) stimmt die Zeichnung bis ins letzte Detail überein — einschließlich einer kleinen Unregelmäßigkeit in der oberen linken Ecke des Rahmens, die Feld 68 als sein Erkennungsmerkmal auf allen Druckplatten trägt. Sie erscheint auf dem Probedruck ebenso wie auf dem Produktionsstück, sodass zwischen den beiden Abdrucken kein Eingriff in die Druckform erfolgte.",
 "A diferencia del campo 96/I, este campo es el caso contrario. Comparado con la impresión de producción del mismo campo (del conjunto de referencia de posiciones de la plancha I), el dibujo coincide hasta el último detalle, incluida una pequeña irregularidad en la esquina superior izquierda del marco que el campo 68 lleva como su marca identificativa en todas las planchas de impresión. Aparece de forma idéntica tanto en la prueba como en el ejemplar de producción, por lo que no se realizó ninguna intervención en la forma entre ambas impresiones.",
)
add(
 "zkušební tisk vedle produkčního ZP 68/I / the proof beside the production field 68/I",
 "zkušební tisk vedle produkčního ZP 68/I / the proof beside the production field 68/I",
 "zkušební tisk vedle produkčního ZP 68/I / the proof beside the production field 68/I",
 "zkušební tisk vedle produkčního ZP 68/I / the proof beside the production field 68/I",
 "zkušební tisk vedle produkčního ZP 68/I / the proof beside the production field 68/I",
 tag="alt",
)
add(
 "Vlevo zkušební tisk v černé barvě, vpravo produkční pole 68/I ve stejném měřítku. Kresba, včetně drobných detailů rámečku, je totožná.",
 "The proof in black on the left, the production field 68/I at the same scale on the right. The drawing, including the small details of the frame, is identical.",
 "L'épreuve en noir à gauche, le champ de production 68/I à la même échelle à droite. Le dessin, y compris les petits détails du cadre, est identique.",
 "Der Probedruck in Schwarz links, das Produktionsfeld 68/I im gleichen Maßstab rechts. Die Zeichnung, einschließlich der kleinen Rahmendetails, ist identisch.",
 "La prueba en negro a la izquierda, el campo de producción 68/I a la misma escala a la derecha. El dibujo, incluidos los pequeños detalles del marco, es idéntico.",
)
add(
 "Pole 68/I tak doplňuje pole 96/I z opačné strany: na 96/I zkušební tisk zachytil formu ještě před dvěma úpravami, na 68/I byla forma v době tohoto otisku už definitivní. Ne všechna pole desky I se tedy v době zkušebních tisků nacházela ve stejném stavu rozpracování.",
 "Field 68/I complements field 96/I from the opposite side: on 96/I the proof caught the forme before two alterations, on 68/I the forme was already definitive at the time of this impression. Not every field of plate I, then, was at the same stage of completion when the proofs were pulled.",
 "Le champ 68/I complète ainsi le champ 96/I depuis l'autre côté : sur 96/I l'épreuve a saisi la forme avant deux modifications, sur 68/I la forme était déjà définitive au moment de ce tirage. Tous les champs de la planche I n'étaient donc pas au même stade d'achèvement lors du tirage des épreuves.",
 "Feld 68/I ergänzt somit Feld 96/I von der anderen Seite: Bei 96/I hielt der Probedruck die Druckform noch vor zwei Änderungen fest, bei 68/I war die Druckform zum Zeitpunkt dieses Abdrucks bereits endgültig. Nicht alle Felder der Platte I befanden sich also zum Zeitpunkt der Probedrucke im selben Fertigstellungsstadium.",
 "El campo 68/I complementa así al campo 96/I desde el lado opuesto: en 96/I la prueba capturó la forma antes de dos modificaciones, en 68/I la forma ya era definitiva en el momento de esta impresión. No todos los campos de la plancha I se encontraban, pues, en la misma fase de acabado cuando se tiraron las pruebas.",
)

# --- section arch-cerny ---
add(
 "Celý arch v černé barvě — kontrolní čísla",
 "A full black pane — the control numbers",
 "Une feuille complète en noir — les chiffres de contrôle",
 "Ein vollständiger schwarzer Bogen — die Kontrollzahlen",
 "Una hoja completa en negro — las cifras de control",
)
add(
 "Vedle jednotlivých zkušebních tisků se dochoval i celý arch (10×10 polí) POFIS 7 (15h) vytištěný celý v černé barvě, nezoubkovaný — stejný účel jako u ostatních zkušebních tisků, tentokrát ale na úrovni celého archu místo jediného pole. Rozmezí let 1918–1920 odpovídá období, kdy se na arších tohoto vydání tiskla takzvaná kontrolní čísla.",
 "Besides the individual proofs, a full pane (10×10 fields) of POFIS 7 (the 15h) has also survived, printed entirely in black and imperforate — the same purpose as the other proofs, but at the level of a whole pane rather than a single field. The span 1918–1920 corresponds to the period in which this issue's sheets carried what are called control numbers.",
 "Outre les épreuves individuelles, une feuille complète (10×10 champs) de POFIS 7 (le 15h) a également été conservée, imprimée entièrement en noir et non dentelée — le même objectif que pour les autres épreuves, mais cette fois à l'échelle d'une feuille entière plutôt que d'un seul champ. La période 1918–1920 correspond à l'époque où les feuilles de cette émission portaient ce que l'on appelle les chiffres de contrôle.",
 "Neben den einzelnen Probedrucken ist auch ein vollständiger Bogen (10×10 Felder) von POFIS 7 (der 15h) erhalten geblieben, vollständig in Schwarz gedruckt und ungezähnt — derselbe Zweck wie bei den übrigen Probedrucken, diesmal jedoch auf der Ebene eines ganzen Bogens statt eines einzelnen Feldes. Der Zeitraum 1918–1920 entspricht der Periode, in der die Bögen dieser Ausgabe die sogenannten Kontrollzahlen trugen.",
 "Además de las pruebas individuales, también se ha conservado una hoja completa (10×10 campos) de POFIS 7 (el 15h), impresa enteramente en negro y sin dentar — el mismo propósito que las demás pruebas, pero esta vez a escala de una hoja entera en lugar de un solo campo. El período 1918–1920 corresponde a la época en que las hojas de esta emisión llevaban las llamadas cifras de control.",
)
add(
 "celý arch 15h v černé barvě, nezoubkovaný / a full pane of the 15h in black, imperforate",
 "celý arch 15h v černé barvě, nezoubkovaný / a full pane of the 15h in black, imperforate",
 "celý arch 15h v černé barvě, nezoubkovaný / a full pane of the 15h in black, imperforate",
 "celý arch 15h v černé barvě, nezoubkovaný / a full pane of the 15h in black, imperforate",
 "celý arch 15h v černé barvě, nezoubkovaný / a full pane of the 15h in black, imperforate",
 tag="alt",
)
add(
 "Celý arch zkušebního tisku 15h v černé barvě. V dolní části archu jsou vytištěna kontrolní čísla.",
 "A full pane of the 15h proof in black. Along the bottom of the sheet the control numbers are printed.",
 "Feuille complète de l'épreuve du 15h en noir. Les chiffres de contrôle sont imprimés dans la partie inférieure de la feuille.",
 "Vollständiger Bogen des Probedrucks der 15h in Schwarz. Im unteren Teil des Bogens sind die Kontrollzahlen aufgedruckt.",
 "Hoja completa de la prueba del 15h en negro. En la parte inferior de la hoja están impresas las cifras de control.",
)
add(
 "Kontrolní čísla jsou postupně rostoucí částky vytištěné pod každým sloupcem deseti známek — 1.50, 3.-, 4.50, 6.-, 7.50, 9.-, 10.50, 12.-, 13.50, až 15.- Kč za celý arch (10 × 15 h = 1,50 Kč na sloupec). Poštovní úředník tak mohl ověřit, že v archu nechybí žádná známka, jen porovnáním posledního vytištěného čísla s cenou celého archu, bez nutnosti počítat jednotlivé kusy.",
 "The control numbers are running totals printed beneath each column of ten stamps — 1.50, 3.-, 4.50, 6.-, 7.50, 9.-, 10.50, 12.-, 13.50, up to 15.- Kč for the whole pane (10 × 15h = 1.50 Kč per column). A post-office clerk could therefore confirm that no stamp was missing from the sheet simply by checking the last printed figure against the price of the full pane, without having to count the individual stamps.",
 "Les chiffres de contrôle sont des totaux cumulés imprimés sous chaque colonne de dix timbres — 1.50, 3.-, 4.50, 6.-, 7.50, 9.-, 10.50, 12.-, 13.50, jusqu'à 15.- Kč pour la feuille entière (10 × 15h = 1,50 Kč par colonne). Un employé des postes pouvait ainsi vérifier qu'il ne manquait aucun timbre dans la feuille en comparant simplement le dernier chiffre imprimé au prix de la feuille complète, sans avoir à compter les timbres un par un.",
 "Die Kontrollzahlen sind fortlaufend steigende Summen, die unter jeder Spalte von zehn Marken aufgedruckt sind — 1.50, 3.-, 4.50, 6.-, 7.50, 9.-, 10.50, 12.-, 13.50, bis 15.- Kč für den gesamten Bogen (10 × 15h = 1,50 Kč pro Spalte). Ein Postbeamter konnte so überprüfen, dass im Bogen keine Marke fehlte, indem er lediglich die zuletzt aufgedruckte Zahl mit dem Preis des gesamten Bogens verglich, ohne die einzelnen Marken zählen zu müssen.",
 "Las cifras de control son totales acumulados impresos bajo cada columna de diez sellos — 1.50, 3.-, 4.50, 6.-, 7.50, 9.-, 10.50, 12.-, 13.50, hasta 15.- Kč para la hoja completa (10 × 15h = 1,50 Kč por columna). Un funcionario de correos podía así comprobar que no faltaba ningún sello en la hoja simplemente comparando la última cifra impresa con el precio de la hoja completa, sin necesidad de contar los sellos uno a uno.",
)
add(
 "detail kontrolních čísel v dolním okraji archu / detail of the control numbers along the bottom margin",
 "detail kontrolních čísel v dolním okraji archu / detail of the control numbers along the bottom margin",
 "detail kontrolních čísel v dolním okraji archu / detail of the control numbers along the bottom margin",
 "detail kontrolních čísel v dolním okraji archu / detail of the control numbers along the bottom margin",
 "detail kontrolních čísel v dolním okraji archu / detail of the control numbers along the bottom margin",
 tag="alt",
)
add(
 "Detail dolního okraje archu: poslední řada známek a pod ní kontrolní čísla rostoucí po 1,50 Kč na každých deset známek.",
 "Detail of the sheet's bottom margin: the last row of stamps and, beneath it, the control numbers rising by 1.50 Kč for every ten stamps.",
 "Détail du bas de la feuille : la dernière rangée de timbres et, en dessous, les chiffres de contrôle augmentant de 1,50 Kč tous les dix timbres.",
 "Detail des unteren Bogenrands: die letzte Markenreihe und darunter die Kontrollzahlen, die je zehn Marken um 1,50 Kč ansteigen.",
 "Detalle del margen inferior de la hoja: la última fila de sellos y, debajo, las cifras de control que aumentan en 1,50 Kč cada diez sellos.",
)
add(
 "POFIS 7 (15h)",
 "POFIS 7 (the 15h)",
 "POFIS 7 (le 15h)",
 "POFIS 7 (die 15h)",
 "POFIS 7 (el 15h)",
)
add(
 "nezoubkovaný arch, 10×10 polí",
 "imperforate pane, 10×10 fields",
 "feuille non dentelée, 10×10 champs",
 "ungezähnter Bogen, 10×10 Felder",
 "hoja sin dentar, 10×10 campos",
)

with io.open(PATH, "w", encoding="utf-8") as f:
    json.dump(cat, f, ensure_ascii=False, indent=1, sort_keys=True)

print("added", added, "skipped(existing)", skipped, "total", len(cat))
