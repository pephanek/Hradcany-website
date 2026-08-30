import importlib.util, json

spec = importlib.util.spec_from_file_location('bj', 'build-jazyky.py')
bj = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bj)

content = open('novinky.html', encoding='utf-8').read()
pairs = bj.find_pairs(content, tag='span')

target = None
for start, end, cs, en in pairs:
    if cs.startswith('Stránka <a href="15h/vyrobni-vady.html">'):
        target = (cs, en)
        break

if target is None:
    raise SystemExit("NOT FOUND")

cs, en = target
k = bj.key(cs)

fr = '''La page <a href="15h/vyrobni-vady.html"><strong>Défauts de fabrication</strong></a> propose désormais une vue d’ensemble complète des défauts d’impression et de papier : <strong>Impression partiellement doublée</strong> (5 pièces), <strong>Anneaux errants</strong> (14 pièces), <strong>Voiles</strong> (19 pièces) et <strong>Taches blanches</strong> (4 pièces) dans la section Défauts d’impression ; <strong>Pli de papier</strong> (24 pièces) et <strong>Éclats de bois dans le papier</strong> (3 pièces) dans la section Défauts du papier. Sous <a href="15h/vyrobni-vady.html#deska"><strong>Endommagement de la planche d’impression</strong></a>, les deux articles – la planche fissurée à 11/II et le cadre endommagé à 60/VI – figurent désormais directement sur la page au lieu d’un simple lien. Le sommaire en haut de page mène directement à chaque sous-catégorie, et la <a href="15h/mapa.html"><strong>carte des oblitérations</strong></a>, désormais corrigée, affiche correctement les lieux même sous les filtres de planches individuels, et pas seulement sous « plusieurs groupes ».'''

de = '''Die Seite <a href="15h/vyrobni-vady.html"><strong>Herstellungsfehler</strong></a> bietet jetzt einen vollständigen Überblick über Druck- und Papierfehler: <strong>Teilweiser Doppeldruck</strong> (5 Stück), <strong>Wandernde Ringe</strong> (14 Stück), <strong>Schleier</strong> (19 Stück) und <strong>Weiße Flecken</strong> (4 Stück) im Abschnitt Druckfehler; <strong>Papierfaltung</strong> (24 Stück) und <strong>Holzsplitter im Papier</strong> (3 Stück) im Abschnitt Papierfehler. Bei <a href="15h/vyrobni-vady.html#deska"><strong>Beschädigung der Druckplatte</strong></a> stehen jetzt beide Artikel – die gesprungene Platte bei 11/II und der beschädigte Rahmen bei 60/VI – direkt auf der Seite statt nur verlinkt. Das Inhaltsverzeichnis oben führt direkt zu jeder Unterkategorie, und die korrigierte <a href="15h/mapa.html"><strong>Stempelkarte</strong></a> zeigt Orte jetzt auch unter den einzelnen Plattenfiltern korrekt an, nicht nur unter „mehrere Gruppen“.'''

es = '''La página <a href="15h/vyrobni-vady.html"><strong>Defectos de fabricación</strong></a> ofrece ahora una visión completa de los defectos de impresión y de papel: <strong>Impresión parcialmente duplicada</strong> (5 ejemplares), <strong>Anillos errantes</strong> (14 ejemplares), <strong>Velos</strong> (19 ejemplares) y <strong>Manchas blancas</strong> (4 ejemplares) en la sección Defectos de impresión; <strong>Arruga del papel</strong> (24 ejemplares) y <strong>Astillas en el papel</strong> (3 ejemplares) en la sección Defectos del papel. En <a href="15h/vyrobni-vady.html#deska"><strong>Daños de la plancha de impresión</strong></a>, ambos artículos –la plancha agrietada en 11/II y el marco dañado en 60/VI– aparecen ahora directamente en la página en lugar de un simple enlace. El índice de arriba lleva directamente a cada subcategoría, y el <a href="15h/mapa.html"><strong>mapa de matasellos</strong></a>, ya corregido, muestra ahora correctamente los lugares también bajo los filtros de cada plancha, no solo bajo «varios grupos».'''

cat = json.load(open('i18n/catalog.json', encoding='utf-8'))
if k in cat:
    print("ALREADY EXISTS, aborting to avoid overwrite:", k)
else:
    cat[k] = {
        'cs': cs,
        'en': en,
        'fr': fr,
        'de': de,
        'es': es,
        'files': ['novinky.html'],
        'tag': 'span',
    }
    with open('i18n/catalog.json', 'w', encoding='utf-8') as f:
        json.dump(cat, f, ensure_ascii=False, indent=2, sort_keys=True)
    print("ADDED KEY:", k)
