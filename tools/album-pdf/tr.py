# -*- coding: utf-8 -*-
"""Preklad textu albovych listu Hradcany (cs -> en/de/fr/es). tr(text, lang) ; untranslated() vraci radky, ktere prosly beze zmeny."""
import re

MISS = set()

COL = {  # feminine adjective forms (barva znamky), order: longest first at use
 'purpurověfialová': ('purple-violet', 'purpurviolett', 'violet pourpre', 'violeta púrpura'),
 'tmavě žlutoolivová': ('dark yellow-olive', 'dunkel gelboliv', 'olive jaune foncé', 'oliva amarillento oscuro'),
 'žlutě olivová': ('yellow-olive', 'gelboliv', 'olive jaune', 'oliva amarillento'),
 'stříbřitě šedá': ('silver-grey', 'silbergrau', 'gris argenté', 'gris plateado'),
 'cihlově červená': ('brick red', 'ziegelrot', 'rouge brique', 'rojo ladrillo'),
 'tm. modrozelená': ('dk. blue-green', 'dkl. blaugrün', 'bleu-vert fcé', 'azul verdoso osc.'),
 'tmavě modrozelená': ('dark blue-green', 'dunkelblaugrün', 'bleu-vert foncé', 'azul verdoso oscuro'),
 'světle zelená': ('light green', 'hellgrün', 'vert clair', 'verde claro'),
 'sytě zelená': ('deep green', 'sattgrün', 'vert intense', 'verde intenso'),
 'tmavě zelená': ('dark green', 'dunkelgrün', 'vert foncé', 'verde oscuro'),
 'žlutozelená': ('yellow-green', 'gelbgrün', 'vert jaunâtre', 'verde amarillento'),
 'zelenošedá': ('green-grey', 'grüngrau', 'gris verdâtre', 'gris verdoso'),
 'šedozelená': ('grey-green', 'graugrün', 'vert grisâtre', 'verde grisáceo'),
 'modrozelená': ('blue-green', 'blaugrün', 'bleu-vert', 'azul verdoso'),
 'tmavě červená': ('dark red', 'dunkelrot', 'rouge foncé', 'rojo oscuro'),
 'hnědočervená': ('brown-red', 'braunrot', 'rouge brunâtre', 'rojo pardo'),
 'červenooranžová': ('red-orange', 'rotorange', 'orange rougeâtre', 'naranja rojizo'),
 'žlutooranžová': ('yellow-orange', 'gelborange', 'orange jaunâtre', 'naranja amarillento'),
 'světle modrá': ('light blue', 'hellblau', 'bleu clair', 'azul claro'),
 'tmavě modrá': ('dark blue', 'dunkelblau', 'bleu foncé', 'azul oscuro'),
 'ultramarínová': ('ultramarine', 'ultramarin', 'outremer', 'ultramar'),
 'modrofialová': ('blue-violet', 'blauviolett', 'violet bleuâtre', 'violeta azulado'),
 'světle fialová': ('light violet', 'hellviolett', 'violet clair', 'violeta claro'),
 'tmavě fialová': ('dark violet', 'dunkelviolett', 'violet foncé', 'violeta oscuro'),
 'černofialová': ('black-violet', 'schwarzviolett', 'violet noirâtre', 'violeta negruzco'),
 'světle hnědá': ('light brown', 'hellbraun', 'brun clair', 'marrón claro'),
 'tmavě hnědá': ('dark brown', 'dunkelbraun', 'brun foncé', 'marrón oscuro'),
 'černohnědá': ('black-brown', 'schwarzbraun', 'brun noirâtre', 'marrón negruzco'),
 'světle šedá': ('light grey', 'hellgrau', 'gris clair', 'gris claro'),
 'černošedá': ('black-grey', 'schwarzgrau', 'gris noirâtre', 'gris negruzco'),
 'červenohnědá': ('red-brown', 'rotbraun', 'brun rougeâtre', 'marrón rojizo'),
 'červenofialová': ('red-violet', 'rotviolett', 'violet rougeâtre', 'violeta rojizo'),
 'karmínová': ('carmine', 'karmin', 'carmin', 'carmín'),
 'rumělková': ('vermilion', 'zinnober', 'vermillon', 'bermellón'),
 'oranžová': ('orange', 'orange', 'orange', 'naranja'),
 'olivová': ('olive', 'oliv', 'olive', 'oliva'),
 'fialová': ('violet', 'violett', 'violet', 'violeta'),
 'červená': ('red', 'rot', 'rouge', 'rojo'),
 'zelená': ('green', 'grün', 'vert', 'verde'),
 'modrá': ('blue', 'blau', 'bleu', 'azul'),
 'hnědá': ('brown', 'braun', 'brun', 'marrón'),
 'žlutá': ('yellow', 'gelb', 'jaune', 'amarillo'),
 'růžová': ('pink', 'rosa', 'rose', 'rosa'),
 'šedá': ('grey', 'grau', 'gris', 'gris'),
 # masculine (pretisk)
 'červenohnědý': ('red-brown', 'rotbraun', 'brun rougeâtre', 'marrón rojizo'),
 'fialový': ('violet', 'violett', 'violet', 'violeta'),
 'zelený': ('green', 'grün', 'vert', 'verde'),
 'modrý': ('blue', 'blau', 'bleu', 'azul'),
}
MON = {'ledna': ('January', 'Januar', 'janvier', 'enero'), 'února': ('February', 'Februar', 'février', 'febrero'), 'března': ('March', 'März', 'mars', 'marzo'),
       'dubna': ('April', 'April', 'avril', 'abril'), 'května': ('May', 'Mai', 'mai', 'mayo'), 'června': ('June', 'Juni', 'juin', 'junio'), 'července': ('July', 'Juli', 'juillet', 'julio'),
       'srpna': ('August', 'August', 'août', 'agosto'), 'září': ('September', 'September', 'septembre', 'septiembre'), 'října': ('October', 'Oktober', 'octobre', 'octubre'),
       'listopadu': ('November', 'November', 'novembre', 'noviembre'), 'prosince': ('December', 'Dezember', 'décembre', 'diciembre')}
ORD = {'První': ('First', 'Erste', 'Premier', 'Primer'), 'Druhá': ('Second', 'Zweite', 'Deuxième', 'Segundo'), 'Třetí': ('Third', 'Dritte', 'Troisième', 'Tercer'),
       'Čtvrtá': ('Fourth', 'Vierte', 'Quatrième', 'Cuarto'), 'Pátá': ('Fifth', 'Fünfte', 'Cinquième', 'Quinto')}
W = {  # whole-string or token translations, applied after patterns (longest first)
 'CZECHOSLOVAKIA': ('CZECHOSLOVAKIA', 'TSCHECHOSLOWAKEI', 'TCHÉCOSLOVAQUIE', 'CHECOSLOVAQUIA'),
 'Alfons Mucha, Knihtisk': ('Alfons Mucha, letterpress', 'Alfons Mucha, Buchdruck', 'Alfons Mucha, typographie', 'Alfons Mucha, tipografía'),
 'den vydání': ('date of issue', 'Ausgabetag', "date d'émission", 'fecha de emisión'),
 'náklad:': ('print run:', 'Auflage:', 'tirage :', 'tirada:'),
 'Náklad:': ('Print run:', 'Auflage:', 'Tirage :', 'Tirada:'),
 'nezjištěno , nevydaná': ('not known, unissued', 'nicht bekannt, nicht ausgegeben', 'inconnu, non émis', 'desconocida, no emitido'),
 ', nevydaná': (', unissued', ', nicht ausgegeben', ', non émis', ', no emitido'),
 'nezoubkovaných a zoubkovaných': ('imperforate and perforated', 'ungezähnt und gezähnt', 'non dentelés et dentelés', 'sin dentar y dentados'),
 'nezoubkované': ('imperforate', 'ungezähnt', 'non dentelés', 'sin dentar'),
 'Nezoubkované': ('Imperforate', 'Ungezähnt', 'Non dentelés', 'Sin dentar'),
 'zoubkované': ('perforated', 'gezähnt', 'dentelés', 'dentados'),
 'Zoubkované': ('Perforated', 'Gezähnt', 'Dentelés', 'Dentados'),
 'kresba': ('design', 'Zeichnung', 'dessin', 'dibujo'),
 'přetisk:': ('overprint:', 'Aufdruck:', 'surcharge :', 'sobrecarga:'),
 'p:': ('ovpt:', 'Aufdr.:', 'surch. :', 'sobrec.:'),
 'I. typ': ('type I', 'Typ I', 'type I', 'tipo I'),
 'II. typ': ('type II', 'Typ II', 'type II', 'tipo II'),
 'Typy spirály:': ('Spiral types:', 'Spiraltypen:', 'Types de spirale :', 'Tipos de espiral:'),
 'Typy příčky:': ('Bar types:', 'Typen des Querstrichs:', 'Types de barre :', 'Tipos de barra:'),
 'Typy rámečku:': ('Frame types:', 'Rahmentypen:', 'Types de cadre :', 'Tipos de marco:'),
 'Spirála otevřená - typ Is': ('Open spiral – type Is', 'Offene Spirale – Typ Is', 'Spirale ouverte – type Is', 'Espiral abierta – tipo Is'),
 'Spirála zavřená - typ IIs': ('Closed spiral – type IIs', 'Geschlossene Spirale – Typ IIs', 'Spirale fermée – type IIs', 'Espiral cerrada – tipo IIs'),
 'Příčka krátká - typ Ip': ('Short bar – type Ip', 'Kurzer Querstrich – Typ Ip', 'Barre courte – type Ip', 'Barra corta – tipo Ip'),
 'Příčka dlouhá - typ IIp': ('Long bar – type IIp', 'Langer Querstrich – Typ IIp', 'Barre longue – type IIp', 'Barra larga – tipo IIp'),
 'Příčka nedotažená - typ IIap': ('Incomplete bar – type IIap', 'Unvollständiger Querstrich – Typ IIap', 'Barre incomplète – type IIap', 'Barra incompleta – tipo IIap'),
 'Rámeček přerušený - typ Ir': ('Broken frame – type Ir', 'Unterbrochener Rahmen – Typ Ir', 'Cadre interrompu – type Ir', 'Marco interrumpido – tipo Ir'),
 'Rámeček nepřerušený - typ IIr': ('Unbroken frame – type IIr', 'Durchgehender Rahmen – Typ IIr', 'Cadre continu – type IIr', 'Marco continuo – tipo IIr'),
 'Výpotřební vydání Doplatní známky': ('provisional issue – postage due stamps', 'Aufbrauchausgabe – Portomarken', 'émission provisoire – timbres-taxe', 'emisión provisional – sellos de tasa'),
 'První letecké provizorium': ('First airmail provisional', 'Erstes Flugpost-Provisorium', 'Premier provisoire de poste aérienne', 'Primer provisional de correo aéreo'),
 'Přípravné kresby, černý knihtisk': ('Preparatory designs, black letterpress', 'Vorentwürfe, schwarzer Buchdruck', 'Dessins préparatoires, typographie noire', 'Dibujos preparatorios, tipografía negra'),
 'HZ': ('comb', 'KZ', 'peigne', 'peine'),
 'ŘZ': ('line', 'LZ', 'ligne', 'línea'),
}
PARA = {
 'Kolem prvních československých známek často vzkvétají neuvěřitelné, dokonce i přehnané historky a nejasné informace. Uplynulo již přez 90 let od vzniku prvních československých známek, zkusme zde shrnout některé informace:':
 ('Incredible, even exaggerated stories and vague information often flourish around the first Czechoslovak stamps. More than 90 years have passed since the first Czechoslovak stamps appeared; let us try to summarise some facts here:',
  'Um die ersten tschechoslowakischen Briefmarken ranken sich oft unglaubliche, sogar übertriebene Geschichten und unklare Angaben. Seit dem Erscheinen der ersten tschechoslowakischen Marken sind mehr als 90 Jahre vergangen; versuchen wir hier, einige Fakten zusammenzufassen:',
  "Autour des premiers timbres tchécoslovaques fleurissent souvent des histoires incroyables, voire exagérées, et des informations imprécises. Plus de 90 ans se sont écoulés depuis l'apparition des premiers timbres tchécoslovaques ; essayons d'en résumer ici quelques faits :",
  'En torno a los primeros sellos checoslovacos florecen a menudo historias increíbles, incluso exageradas, e informaciones imprecisas. Han pasado ya más de 90 años desde la aparición de los primeros sellos checoslovacos; intentemos resumir aquí algunos datos:'),
 'Snad prvním iniciátorem k přípravě nových československých známek byl předseda KČF, ing. Jaroslav Šula, který prý již 20. 10. 1918 dopisem vyzval Alfonse Muchu aby připravil návrhy pro příští českou vládu.':
 ('Perhaps the first to initiate the preparation of new Czechoslovak stamps was the chairman of the KČF (Club of Czech Philatelists), Ing. Jaroslav Šula, who reportedly wrote to Alfons Mucha as early as 20 October 1918, asking him to prepare designs for the future Czech government.',
  'Der vielleicht erste Initiator der neuen tschechoslowakischen Briefmarken war der Vorsitzende des KČF (Klub tschechischer Philatelisten), Ing. Jaroslav Šula, der angeblich schon am 20. 10. 1918 Alfons Mucha brieflich aufforderte, Entwürfe für die künftige tschechische Regierung vorzubereiten.',
  "Le premier à avoir pris l'initiative de nouveaux timbres tchécoslovaques fut sans doute le président du KČF (Club des philatélistes tchèques), l'ingénieur Jaroslav Šula, qui aurait écrit dès le 20 octobre 1918 à Alfons Mucha pour lui demander de préparer des projets pour le futur gouvernement tchèque.",
  'Quizá el primer iniciador de la preparación de nuevos sellos checoslovacos fue el presidente del KČF (Club de Filatelistas Checos), el ingeniero Jaroslav Šula, quien, según se dice, ya el 20 de octubre de 1918 pidió por carta a Alfons Mucha que preparara diseños para el futuro gobierno checo.'),
 'Dle záznamů KČF, 8. 11. 1918 se vedení KČF obrátilo na profesora Alfonse Muchu aby vypracoval návrhy na první ČSR známky...':
 ('According to the records of the KČF, on 8 November 1918 the club management approached Professor Alfons Mucha to work out designs for the first Czechoslovak stamps...',
  'Laut den Aufzeichnungen des KČF wandte sich die Vereinsleitung am 8. 11. 1918 an Professor Alfons Mucha, um Entwürfe für die ersten tschechoslowakischen Marken auszuarbeiten...',
  "D'après les archives du KČF, le 8 novembre 1918 la direction du club s'adressa au professeur Alfons Mucha pour qu'il élabore des projets pour les premiers timbres tchécoslovaques...",
  'Según los registros del KČF, el 8 de noviembre de 1918 la dirección del club se dirigió al profesor Alfons Mucha para que elaborara diseños para los primeros sellos checoslovacos...'),
 'Navíce, dle vzpomínek vrchního poštovního oficiála Jaroslava Lešetického, dne 29. 10. 1918 byl poštovním ředitelem Maxmiliánem Fatkou osobně pověřen úkolem, aby postaral kresbu přetisku "Zatímní vláda 28. 10. 1918" pro rakouské známky. Tento návrh byl odmítnutý a od přetisku oficiálního opuštěno. Den nato byl J. Lešetický pověřen druhým posláním - sehnat návrhy na zatimní známky.':
 ('Moreover, according to the recollections of the senior postal official Jaroslav Lešetický, on 29 October 1918 he was personally charged by the postal director Maxmilián Fatka with obtaining a design for the overprint "Zatímní vláda 28. 10. 1918" (Provisional Government) for Austrian stamps. This proposal was rejected and the official overprint was abandoned. The next day J. Lešetický was given a second task – to obtain designs for provisional stamps.',
  'Außerdem wurde laut den Erinnerungen des Oberpostoffizials Jaroslav Lešetický dieser am 29. 10. 1918 vom Postdirektor Maxmilián Fatka persönlich beauftragt, eine Zeichnung für den Aufdruck „Zatímní vláda 28. 10. 1918“ (Provisorische Regierung) auf österreichischen Marken zu besorgen. Dieser Vorschlag wurde abgelehnt und der amtliche Aufdruck aufgegeben. Am nächsten Tag erhielt J. Lešetický einen zweiten Auftrag – Entwürfe für provisorische Marken zu beschaffen.',
  "De plus, selon les souvenirs de l'officier supérieur des postes Jaroslav Lešetický, le 29 octobre 1918 le directeur des postes Maxmilián Fatka le chargea personnellement de procurer un dessin pour la surcharge « Zatímní vláda 28. 10. 1918 » (Gouvernement provisoire) destinée aux timbres autrichiens. Ce projet fut rejeté et la surcharge officielle abandonnée. Le lendemain, J. Lešetický reçut une seconde mission : trouver des projets de timbres provisoires.",
  'Además, según los recuerdos del oficial superior de correos Jaroslav Lešetický, el 29 de octubre de 1918 el director de correos Maxmilián Fatka le encargó personalmente conseguir un dibujo para la sobrecarga «Zatímní vláda 28. 10. 1918» (Gobierno provisional) destinada a los sellos austriacos. Esta propuesta fue rechazada y se abandonó la sobrecarga oficial. Al día siguiente, J. Lešetický recibió un segundo encargo: conseguir diseños para sellos provisionales.'),
 'Dne 1. listopadu 1918, na procházce z tiskárny Unie, navrhnul ministerský rada Viliam Elias, Jaroslavu Lešetickému, Hradčany jako motiv prvních známek.':
 ('On 1 November 1918, on a walk back from the Unie printing works, the ministerial councillor Viliam Elias suggested to Jaroslav Lešetický the Hradčany (Prague Castle) as the motif of the first stamps.',
  'Am 1. November 1918 schlug der Ministerialrat Viliam Elias auf dem Rückweg von der Druckerei Unie Jaroslav Lešetický den Hradschin als Motiv der ersten Marken vor.',
  "Le 1er novembre 1918, en revenant à pied de l'imprimerie Unie, le conseiller ministériel Viliam Elias proposa à Jaroslav Lešetický le Hradčany (château de Prague) comme motif des premiers timbres.",
  'El 1 de noviembre de 1918, al volver a pie de la imprenta Unie, el consejero ministerial Viliam Elias propuso a Jaroslav Lešetický el Hradčany (castillo de Praga) como motivo de los primeros sellos.'),
 'Tento návrh byl schválen u poštovního presidia a následující den bylo zadáno A. Muchovi aby též vykreslil Hradčany.':
 ('This proposal was approved by the postal presidium and the next day A. Mucha was commissioned to draw the Hradčany as well.',
  'Dieser Vorschlag wurde vom Postpräsidium gebilligt, und am folgenden Tag wurde A. Mucha beauftragt, auch den Hradschin zu zeichnen.',
  'Cette proposition fut approuvée par la présidence des postes et, le lendemain, A. Mucha fut chargé de dessiner également le Hradčany.',
  'Esta propuesta fue aprobada por la presidencia de correos y al día siguiente se encargó a A. Mucha que dibujara también el Hradčany.'),
 'Zhotovením prvních poštovních známek byla pověřena tiskárna České grafické unie v Praze. Tento podnik vznikl roku 1903 sloučením České grafické společnosti Unie s reprodukční dílnou Jana Vilíma.':
 ('The printing of the first postage stamps was entrusted to the printing works of the Česká grafická unie in Prague. This company was formed in 1903 by the merger of the Česká grafická společnost Unie with the reproduction workshop of Jan Vilím.',
  'Mit der Herstellung der ersten Briefmarken wurde die Druckerei Česká grafická unie in Prag betraut. Dieses Unternehmen entstand 1903 durch die Fusion der Česká grafická společnost Unie mit der Reproduktionswerkstatt von Jan Vilím.',
  "La fabrication des premiers timbres-poste fut confiée à l'imprimerie Česká grafická unie de Prague. Cette entreprise était née en 1903 de la fusion de la Česká grafická společnost Unie avec l'atelier de reproduction de Jan Vilím.",
  'La fabricación de los primeros sellos de correos se confió a la imprenta Česká grafická unie de Praga. Esta empresa surgió en 1903 de la fusión de la Česká grafická společnost Unie con el taller de reproducción de Jan Vilím.'),
 'Dne 3. listopadu odevzdal Alfons Mucha návrhy s obrazem Hradčan, s Husitou, se sokolem a s dívkou v kroji.':
 ('On 3 November Alfons Mucha delivered designs showing the Hradčany, a Hussite, a falcon and a girl in folk costume.',
  'Am 3. November lieferte Alfons Mucha Entwürfe mit dem Hradschin, einem Hussiten, einem Falken und einem Mädchen in Tracht ab.',
  'Le 3 novembre, Alfons Mucha remit des projets représentant le Hradčany, un hussite, un faucon et une jeune fille en costume traditionnel.',
  'El 3 de noviembre, Alfons Mucha entregó diseños con el Hradčany, un husita, un halcón y una muchacha en traje popular.'),
 'První hradčanské známky, hodnota 5 h světle zelená a 10 h červená, byly vydané 18. prosince 1918. Tento den se stal pamětním dnem čs. filatelie.':
 ('The first Hradčany stamps, the 5 h light green and the 10 h red, were issued on 18 December 1918. This day became the commemorative day of Czechoslovak philately.',
  'Die ersten Hradschin-Marken, die 5 h hellgrün und die 10 h rot, erschienen am 18. Dezember 1918. Dieser Tag wurde zum Gedenktag der tschechoslowakischen Philatelie.',
  'Les premiers timbres Hradčany, le 5 h vert clair et le 10 h rouge, furent émis le 18 décembre 1918. Ce jour devint la journée commémorative de la philatélie tchécoslovaque.',
  'Los primeros sellos Hradčany, el 5 h verde claro y el 10 h rojo, se emitieron el 18 de diciembre de 1918. Ese día se convirtió en el día conmemorativo de la filatelia checoslovaca.'),
 'Hradčanské známky nevycházely v pořadí podle hodnot, ale napřeskáčku. Poslední 30 h světle fialová vyšla až 12. dubna 1920':
 ('The Hradčany stamps were not issued in order of value but haphazardly. The last one, the 30 h light violet, did not appear until 12 April 1920.',
  'Die Hradschin-Marken erschienen nicht in der Reihenfolge der Werte, sondern durcheinander. Die letzte, die 30 h hellviolett, kam erst am 12. April 1920 heraus.',
  "Les timbres Hradčany ne parurent pas dans l'ordre des valeurs, mais en désordre. Le dernier, le 30 h violet clair, ne sortit que le 12 avril 1920.",
  'Los sellos Hradčany no se emitieron por orden de valor, sino de forma desordenada. El último, el 30 h violeta claro, no apareció hasta el 12 de abril de 1920.'),
 'Emise Hradčany spočívá z pěti různých kreseb, z 26 hodnot z nichž 14 hodnot bylo též vydáno v perforované úpravě.':
 ('The Hradčany issue consists of five different designs and 26 values, 14 of which were also issued perforated.',
  'Die Hradschin-Ausgabe besteht aus fünf verschiedenen Zeichnungen und 26 Werten, von denen 14 auch gezähnt erschienen.',
  "L'émission Hradčany comprend cinq dessins différents et 26 valeurs, dont 14 furent également émises dentelées.",
  'La emisión Hradčany consta de cinco dibujos diferentes y 26 valores, 14 de los cuales se emitieron también dentados.'),
 'Výroba prvních československých známek je poznamenaná poválečným chaosem. Tiskárna „Česká grafická unie“ v Praze, na výrobu známek nebyla připravená. Stroje pro knihtisk byly zastaralé, tím vzniklo množství tiskových vad, odchylek a tím i ráj pro specialisty.':
 ('The production of the first Czechoslovak stamps bears the marks of post-war chaos. The printing works "Česká grafická unie" in Prague was not prepared for stamp production. The letterpress machines were outdated, which gave rise to a multitude of printing flaws and varieties – and thus a paradise for specialists.',
  'Die Herstellung der ersten tschechoslowakischen Marken ist vom Nachkriegschaos geprägt. Die Druckerei „Česká grafická unie“ in Prag war auf die Markenproduktion nicht vorbereitet. Die Buchdruckmaschinen waren veraltet, wodurch zahlreiche Druckfehler und Abweichungen entstanden – und damit ein Paradies für Spezialisten.',
  "La fabrication des premiers timbres tchécoslovaques porte la marque du chaos d'après-guerre. L'imprimerie « Česká grafická unie » de Prague n'était pas préparée à produire des timbres. Les machines typographiques étaient vétustes, d'où une multitude de défauts d'impression et de variétés – et donc un paradis pour les spécialistes.",
  'La fabricación de los primeros sellos checoslovacos lleva la huella del caos de posguerra. La imprenta «Česká grafická unie» de Praga no estaba preparada para producir sellos. Las máquinas tipográficas estaban anticuadas, lo que originó multitud de defectos de impresión y variedades, y con ello un paraíso para los especialistas.'),
 'Druhý návrh o velikosti 68 x 68 mm. Holubice umístěné čelem k oválnému místu pro umístění hodnoty.':
 ('Second design, 68 × 68 mm. The doves face the oval space intended for the value.',
  'Zweiter Entwurf, 68 × 68 mm. Die Tauben sind dem ovalen Feld für die Wertangabe zugewandt.',
  "Deuxième projet, 68 × 68 mm. Les colombes font face à l'ovale destiné à la valeur.",
  'Segundo diseño, 68 × 68 mm. Las palomas miran hacia el óvalo destinado al valor.'),
 'Malý bílý nápis na barevném podkladu, se sluncem a keřem.':
 ('Small white inscription on a coloured ground, with sun and bush.', 'Kleine weiße Inschrift auf farbigem Grund, mit Sonne und Strauch.', 'Petite inscription blanche sur fond coloré, avec soleil et buisson.', 'Pequeña inscripción blanca sobre fondo de color, con sol y arbusto.'),
 'Malý barevný nápis na bílém podkladu, se sluncem a keřem.':
 ('Small coloured inscription on a white ground, with sun and bush.', 'Kleine farbige Inschrift auf weißem Grund, mit Sonne und Strauch.', 'Petite inscription colorée sur fond blanc, avec soleil et buisson.', 'Pequeña inscripción de color sobre fondo blanco, con sol y arbusto.'),
 'Velký bílý nápis na barevném podkladu, se sluncem a bílým keřem.':
 ('Large white inscription on a coloured ground, with sun and white bush.', 'Große weiße Inschrift auf farbigem Grund, mit Sonne und weißem Strauch.', 'Grande inscription blanche sur fond coloré, avec soleil et buisson blanc.', 'Gran inscripción blanca sobre fondo de color, con sol y arbusto blanco.'),
 'Velký bílý nápis na barevném podkladu, se šrafovaným keřem, bez slunce.':
 ('Large white inscription on a coloured ground, with hatched bush, without sun.', 'Große weiße Inschrift auf farbigem Grund, mit schraffiertem Strauch, ohne Sonne.', 'Grande inscription blanche sur fond coloré, avec buisson hachuré, sans soleil.', 'Gran inscripción blanca sobre fondo de color, con arbusto rayado, sin sol.'),
 'Velký bílý nápis na barevném podkladu, bez keře a slunce. Větší kresba chrámu svatého Mikuláše, odlišná kresba ornamentu v orámování obrazu.':
 ('Large white inscription on a coloured ground, without bush and sun. Larger drawing of St. Nicholas Church, different ornament in the frame of the picture.',
  'Große weiße Inschrift auf farbigem Grund, ohne Strauch und Sonne. Größere Zeichnung der St.-Nikolaus-Kirche, abweichendes Ornament in der Bildumrahmung.',
  "Grande inscription blanche sur fond coloré, sans buisson ni soleil. Dessin plus grand de l'église Saint-Nicolas, ornement différent dans l'encadrement de l'image.",
  'Gran inscripción blanca sobre fondo de color, sin arbusto ni sol. Dibujo mayor de la iglesia de San Nicolás, ornamento diferente en el marco de la imagen.'),
 '1920 - První letecké provizorium Náklad: L1: 1 620 000, L2: 1 720 000, L3: 860 000 nezoubkovaných a zoubkovaných Nevyprodaná část nákladu bylo po roce 1933 úředně zničena. Přesný konečný náklad tedy není znám.':
 ('1920 – First airmail provisional. Print run: L1: 1 620 000, L2: 1 720 000, L3: 860 000 imperforate and perforated. The unsold part of the printing was officially destroyed after 1933, so the exact final quantity is not known.',
  '1920 – Erstes Flugpost-Provisorium. Auflage: L1: 1 620 000, L2: 1 720 000, L3: 860 000 ungezähnt und gezähnt. Der unverkaufte Teil der Auflage wurde nach 1933 amtlich vernichtet; die genaue Endauflage ist daher nicht bekannt.',
  "1920 – Premier provisoire de poste aérienne. Tirage : L1 : 1 620 000, L2 : 1 720 000, L3 : 860 000 non dentelés et dentelés. La partie invendue du tirage fut officiellement détruite après 1933 ; le tirage final exact n'est donc pas connu.",
  '1920 – Primer provisional de correo aéreo. Tirada: L1: 1 620 000, L2: 1 720 000, L3: 860 000 sin dentar y dentados. La parte no vendida de la tirada fue destruida oficialmente después de 1933, por lo que no se conoce la tirada final exacta.'),
}
LI = {'en': 0, 'de': 1, 'fr': 2, 'es': 3}

def tr(t, lang):
    i = LI[lang]; s = t.strip()
    if not s: return t
    if s in PARA: return PARA[s][i]
    if s in W: return W[s][i]
    o = s
    # header "1919, Hradčany - Pátá kresba, zoubkované" / "1922, Hradčany - Výpotřební vydání Doplatní známky"
    m = re.match(r'^(\d{4}(?:-\d\d)?), Hradčany - (\S+) kresba, (nezoubkované|zoubkované)$', s)
    if m:
        yr, ordn, z = m.groups(); zz = W[z][i]
        return {'en': f'{yr}, Hradčany – {ORD[ordn][0]} design, {zz}', 'de': f'{yr}, Hradčany – {ORD[ordn][1]} Zeichnung, {zz}',
                'fr': f'{yr}, Hradčany – {ORD[ordn][2]} dessin, {zz}', 'es': f'{yr}, Hradčany – {ORD[ordn][3]} dibujo, {zz}'}[lang]
    m = re.match(r'^(\d{4}), Hradčany - Výpotřební vydání Doplatní známky$', s)
    if m: return f"{m.group(1)}, Hradčany – {W['Výpotřební vydání Doplatní známky'][i]}"
    # date: "den vydání 18. prosince 1918"
    def dat(mm):
        dd, mon, yr = mm.group(1), mm.group(2), mm.group(3); M = MON[mon][i]
        return {'en': f'{W["den vydání"][0]} {dd} {M} {yr}', 'de': f'{W["den vydání"][1]} {dd}. {M} {yr}', 'fr': f'{W["den vydání"][2]} {dd} {M} {yr}', 'es': f'{W["den vydání"][3]} {dd} de {M} de {yr}'}[lang]
    s = re.sub(r'den vydání (\d{1,2})\. (\w+) (\d{4})', dat, s)
    s = s.replace(' - ', ' – ')
    # colours (longest first), masculine for pretisk
    for k in sorted(COL, key=len, reverse=True):
        s = re.sub(r'(?<![\wěščřžýáíéúůóťď])' + re.escape(k) + r'(?![\wěščřžýáíéúůóťď])', COL[k][i], s)
    for k in sorted(W, key=len, reverse=True):
        if k in ('HZ', 'ŘZ'):
            s = re.sub(r'\b' + k + r'\b', W[k][i], s)
        elif k == 'p:':
            s = re.sub(r'^p:', W[k][i], s)
        else:
            s = s.replace(k, W[k][i])
    s = re.sub(r'\bkreseb\b', {'en': 'designs', 'de': 'Zeichnungen', 'fr': 'dessins', 'es': 'dibujos'}[lang], s)
    if s == o and re.search(r'[ěščřžýáíéúůóťďĚŠČŘŽÝÁÍÉÚŮ]', s): MISS.add(o)
    return s

if __name__ == '__main__':
    import json, sys
    L = json.load(open('lines_cs.json', encoding='utf-8'))
    for t, n in L:
        for lg in ('en', 'de', 'fr', 'es'): tr(t, lg)
    print('MISS', len(MISS)); [print(repr(m)) for m in sorted(MISS)]
