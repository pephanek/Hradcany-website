# Sbírám Hradčany — moderní responzivní web

Statický web (HTML/CSS/JS) postavený znovu z obsahu webu
[hradcany-stamps.com](https://www.hradcany-stamps.com/). Obsahuje hlavní stránky původního webu
v moderním, plně responzivním designu (mobil, tablet, desktop).

## Struktura

```
Hradcany Website/
├── index.html              Úvod (domovská stránka)
├── novinky.html            Novinky
├── znamky-emise.html       Známky emise (přehled)
│   ├── prvni-kresba.html   1. kresba (3h–40h)
│   ├── druha-kresba.html   2. kresba (100h–400h)
│   ├── treti-kresba.html   3. kresba (1h, 50h)
│   ├── ctvrta-kresba.html  4. kresba (60h–1000h)
│   └── pata-kresba.html    5. kresba (5h–500h)
├── clanky.html             Články
├── tiskove-desky.html      Kompletní tiskové desky
├── typy-pate-kresby.html   Typy páté kresby
├── deskove-vady.html       Deskové vady
├── shanim-a-nabizim.html   Sháním a nabízím
├── odkazy.html             Odkazy
├── kniha-navstev.html      Kniha návštěv (kontaktní formulář)
├── ke-stazeni.html         Ke stažení (albové listy)
├── sitemap.html            Mapa stránek
├── css/style.css           Styl, responzivní layout
├── js/main.js              Mobilní menu, lightbox, fallback obrázků
├── assets/images/          Lokální obrázky (naplní download skript)
└── scripts/                Skripty pro stažení obrázků + manifest
```

## Obrázky

Stránky odkazují na **lokální** obrázky ve složce `assets/images/`. Dokud nejsou staženy, web se
automaticky přepne na původní obrázky z CDN, takže se zobrazí správně i hned po otevření.

Pro plně offline / samostatný web stáhněte obrázky lokálně — spusťte **z kořenové složky projektu**
jeden z těchto skriptů:

```bash
# macOS / Linux
python3 scripts/download_images.py
# nebo
bash scripts/download_images.sh
```

```powershell
# Windows
powershell -ExecutionPolicy Bypass -File scripts\download_images.ps1
```

Stáhne se ~96 obrázků (loga, jednotlivé známky, tiskové desky, schémata).

## Poznámky

- Odkazy na detailní stránky, které nejsou součástí tohoto základního výběru (jednotlivá známková
  pole tiskových desek, jednotlivé články, podtypy páté kresby), směřují na původní web
  hradcany-stamps.com, takže nic není rozbité.
- Odkazy na PDF albové listy a Excel schémata vedou na původní soubory na CDN.
- Web je čistě statický — stačí otevřít `index.html` v prohlížeči, není potřeba žádný server.

© 2014–2017 Josef Matoušek. Obsah převzat z hradcany-stamps.com.

## 15h — specializovaná sekce (2026-07-06)

Nová dvojjazyčná (CZ/EN) sekce věnovaná hodnotě 15h: `15h/index.html`.
- 16 stránek: přehled, barvy, tiskové desky, galerie pozic (7×100 polí), typy, zoubkování, statistiky (Chart.js), články, poštovní provoz.
- Galerie: 1 400 obrazů (náhled + plné rozlišení) v `15h/assets/library/TDn/`, generováno z knihovny `Claude-Hradcany-agent/Hradcany/library_15h`.
- Data: hradcany-stamps.com, Hradcany_15h GENERAL.xlsx, REPORT_15h_all_plates.md.
- Přepínač jazyka ukládá volbu do localStorage; galerie má lightbox s klávesovým listováním a filtr pozice.
