# Překlad albových listů (album-hradcany.pdf) do EN/DE/FR/ES

Postup: `python3 build.py <lang> [out.pdf] [stránky]` nad `album_cs.pdf` (= assets/downloads/album-hradcany.pdf, 47 str., export z Visia 2016).
- `tr.py` – slovník (barvy, měsíce, pořadové číslovky, tokeny ŘZ/HZ, náklad, den vydání, typy spirál/příček/rámečků) + ručně přeložené odstavce; `python3 tr.py` vypíše řádky bez překladu.
- `build.py` – PyMuPDF: každý textový řádek/odstavec redaktuje (obrázky a kresby zůstávají) a vloží překlad fontem Carlito (metrika Calibri) nebo Liberation Serif; řádky centruje na rámeček známky resp. stránku, při přetečení zmenší písmo (min. 7 pt), odstavce justify.
- Potřebuje `pip install pymupdf` a fonty Carlito + Liberation (Linux: fonts-crosextra-carlito, fonts-liberation).
- Značka zoubkování (symbolový glyf) se nepřekresluje – řádek s ŘZ/HZ stojí o pár bodů vlevo od středu rámečku.
- `build-jazyky.py` přepíše pro cizí jazyky odkaz `assets/downloads/X.pdf` na `X-<lang>.pdf`, existuje-li.
