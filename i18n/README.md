# Jazykové verze webu

Web běží v pěti jazycích: **čeština, angličtina, francouzština, němčina, španělština**.

## Jak je to uspořádané

```
/                 čeština — ZDE SE EDITUJE
/en/ /fr/ /de/ /es/   generované kopie, needitovat
/i18n/catalog.json    překladová paměť (1 339 textů × 5 jazyků)
/i18n/glosar.md       závazná odborná terminologie
/assets/ /css/ /js/   obrázky a styly — existují jen jednou, jazykové
                      stránky na ně odkazují o úroveň výš
```

Obrázky se nekopírují. 284 vygenerovaných stránek zabírá jen text.

## Když měníte obsah

Editujete **jen soubory v kořeni**, přesně jako dosud — česky a anglicky
ve dvojicích `<span class="cs">…</span><span class="en">…</span>`.
Potom spustíte:

```
python build-jazyky.py
```

Skript projde všechny stránky, poskládá z katalogu FR/DE/ES verze
a přepíše složky `en/ fr/ de/ es/`. Trvá pár vteřin.

Pokud napíšete nový text, který v katalogu ještě není, skript ho
**nezahodí ani nepřeloží špatně** — nechá tam češtinu a vypíše seznam
do `i18n/chybejici.txt`. Ten stačí poslat k doplnění.

## Co se překládá

Kromě běžného textu i:

* titulky stránek a `meta description` (kvůli vyhledávačům),
* popisky obrázků (`alt`, `figcaption`),
* texty ve schématech (SVG) — včetně obrázku typů páté kresby,
  který má vlastní anglickou verzi `pata-kresba-schema-en.png`,
* popisky v galeriích uložené v atributech `data-cap` a `data-tags`,
* popisky v komparátoru polí a v mapě razítek (JavaScript).

Nepřekládají se vlastní jména (Hradčany, Košice, Česká grafická Unie,
jména sběratelů), označení polí a desek (ZP 34/VI, TD VII), katalogová
čísla a nápisy vytištěné na známkách (ČESKO-SLOVENSKA, DOPLATIT 40 h).
Zkratky **ZP** a **TD** zůstávají zkratkami **jen v češtině**; všechny
ostatní jazyky je rozepisují (field/plate, position/planche,
Feld/Platte, posición/plancha) — podrobnosti v glosáři. Název emise je
v němčině **Hradschin**, jinde **Hradčany**.

Grafy na stránce Statistiky a mapa razítek mají vlastní tabulku popisků
přímo v HTML (`TT = {cs:…, en:…, fr:…, de:…, es:…}`) — včetně názvů
měsíců. Jazyk si berou z `<html lang>`, takže po přidání jazyka je
potřeba doplnit i tyto tabulky.

## Přepínání jazyka

V hlavičce je pět odkazů (CZ EN FR DE ES). Každý vede na **tutéž
stránku** v jiném jazyce. V `<head>` jsou navíc značky
`<link rel="alternate" hreflang>`, aby si vyhledávače jazykové verze
správně spárovaly.

## Terminologie

`glosar.md` je závazný. Když v některém jazyce narazíte na termín, který
odborníci v dané zemi říkají jinak, opravte ho v glosáři a dejte vědět —
katalog se podle něj sjednotí.
