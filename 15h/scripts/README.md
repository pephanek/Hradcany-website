# Nástroje k 15h

## svetlina-index.py

Měří sílu světliny na jednom známkovém poli a kreslí vývojovou řadu.

```
python svetlina-index.py <složka se skeny> [--ohnisko roh-pd] [--rada rada.jpg]
                         [--sloupcu 5] [--sirka 320] [--mezera 22] [--tma 0.03]
```

Složka = jedna pozice ze studijní knihovny, například `training_15h/TD5_pos020`.
Skeny musí být jednotlivé známky, kresba nastojato.

**Co skript dělá.** Každý sken nejdřív narovná podle spodní hrany kresby a
zakotví se na střednice čtyř rámových linek — ne na obalový obdélník barvy,
který u nakloněného skenu ujede. Linku hledá jako první výrazný vrchol profilu
při pohledu zvenčí dovnitř; maximum v pásu by uteklo na ornamentální pásku,
která má v průměru barvy víc než tenká rámová linka.

**Index** = barva v ohnisku / barva v týchž linkách dál od rohu. Okno ohniska i
kontrolní pásy mají šířku podle naměřené tloušťky linky. Normalizace probíhá
uvnitř jednoho kusu, takže nevadí rozdílná sytost tisku ani jiný sken. Nižší
hodnota = v ohnisku chybí barva.

**Kontroly.** Kus, kterému do ohniska zasahuje cizí tmavá plocha (okraj skenu,
tužkou psaná poznámka), se vynechá — práh se nastavuje přepínačem `--tma`.
Rozteč rámových linek by měla u všech kusů vyjít stejná (u 15h kolem 1,18);
větší rozptyl znamená, že detekce linky někde selhala.

**Nové ohnisko** se přidá do tabulky `OHNISKA` v hlavičce skriptu: stačí říct,
které dvě rámové linky se protínají, a rozsah kontrolního pásu.

## Publikace webu

Změny ve složce se na GitHub dostávají skriptem `publikuj.bat` v kořeni
repozitáře (spouští ho Plánovač úloh přes `publikuj-skryte.vbs`, aby neblikalo
okno konzole). Skript uklidí zámky po spadlém běhu, zjistí, jestli je co
publikovat, srovná se se vzdáleným repozitářem — zapisuje do něj i vrátný knihy
návštěv — a teprve pak pushne. Průběh je v `publikuj.log`.

Oba skripty jsou v `.gitignore`, protože patří k tomuhle počítači, ne na web.
