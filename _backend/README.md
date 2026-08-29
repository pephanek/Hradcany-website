# Vrátný pro knihu návštěv a anketu

Web běží na GitHub Pages, které umí jen statické soubory — nedokáže tedy
přijmout odeslaný formulář. Tenhle Worker je jediná dynamická část celého
webu. Sám nic neukládá: co projde kontrolou, **zapíše commitem do
repozitáře webu**. Data tak zůstávají na GitHubu, verzovaná, s historií.

```
návštěvník → Worker (kontrola) → commit do repa → GitHub Pages → web
                                                        ↑
                              stránka čte data/*.json přímo odsud
```

Čtení Worker vůbec nezatěžuje — stránka si `data/kniha.json`
a `data/anketa.json` načte jako obyčejný statický soubor.

## Co je potřeba jednou nastavit

**1. GitHub token.** Na GitHubu → Settings → Developer settings →
Personal access tokens → Fine-grained tokens → Generate new token.
Přístup omezte na jediný repozitář `Hradcany-website`, oprávnění
**Contents: Read and write**. Nic víc. Token si zkopírujte.

**2. Cloudflare účet** (zdarma) a v něm:

```
npm install -g wrangler
cd _backend
npx wrangler login
npx wrangler secret put GH_TOKEN      # vložte token z kroku 1
npx wrangler secret put TAJNY_KLIC    # libovolný náhodný řetězec, 30+ znaků
npx wrangler deploy
```

Wrangler vypíše adresu ve tvaru
`https://hradcany-vratny.<váš-účet>.workers.dev`.

**3. Adresu vložte do webu.** V souboru `js/komunita.js` je hned nahoře

```js
var API = '';                 // sem přijde adresa vrátného
```

Doplňte adresu z předchozího kroku. Přegenerovávat nic není potřeba —
`js/komunita.js` existuje jen jednou a používají ho všechny jazykové verze.
Dokud je řetězec prázdný, kniha návštěv se jen zobrazuje a formulář
slušně oznámí, že zápis zatím neběží.

## Vlastní token pro vrátného

Token pro Worker vyrobte **samostatně**, nepoužívejte ten, kterým se
publikuje web. Kdyby bylo někdy potřeba jeden z nich zneplatnit,
druhá věc pojede dál. Publikační token je uložený jinde
(`.deploy/github_token.txt`) a mění se skriptem `_backend/vymen-token.py`.

## Doporučeno: vlastní doména místo workers.dev

Hezčí a odolnější je pověsit Worker na `api.hradcany-stamps.com`.
V Cloudflare → Workers → váš worker → Settings → Domains & Routes →
Add custom domain. Doména musí být v Cloudflare DNS.

## Volitelně: Turnstile

Turnstile je bezplatná obdoba CAPTCHy od Cloudflare, která ve většině
případů nic nezobrazí a jen tiše ověří prohlížeč. Zapíná se takto:

1. Cloudflare → Turnstile → Add site, doména `hradcany-stamps.com`.
2. `npx wrangler secret put TURNSTILE` a vložte **secret key**.
3. Do `js/komunita.js` doplňte **site key** do proměnné `TURNSTILE_KEY`.

Bez těchto kroků Worker Turnstile přeskočí a spoléhá na ostatní vrstvy.

## Jak se maže nevhodný příspěvek

Data jsou obyčejný JSON v repozitáři. Otevřete na GitHubu
`data/kniha.json`, smažte příslušný blok a uložte — Pages se přestaví
a příspěvek zmizí. Historie commitů zůstane, takže je vždy vidět,
co se kdy stalo.

## Pozor: jen přes http(s)

Kniha i anketa načítají data přes `fetch`, což prohlížeč u souborů
otevřených jako `file://` blokuje. Když si web prohlížíte lokálně
dvojklikem, výpis vzkazů zůstane prázdný — na doméně funguje normálně.

## Vrstvy proti spamu

| vrstva | co dělá |
|---|---|
| skryté pole | robot ho vyplní, člověk ne — takový zápis se tiše zahodí |
| podepsaný token | formulář musí být opravdu načtený z webu; token je podepsaný HMAC |
| časová past | odeslání dřív než za 8 s nebo později než za 3 h se odmítne |
| znalostní otázka | náhodně jedna ze čtyř otázek k emisi, kontrola na serveru |
| zákaz odkazů | jakýkoli odkaz ve jméně nebo textu = odmítnuto |
| slovník | běžná spamová slova |
| cizí písmo | přes 30 % znaků mimo latinku (web je v pěti evropských jazycích) |
| opakování | jeden znak 10× za sebou nebo text složený z pár stále dokola opakovaných slov |
| limit | jeden zápis z jedné adresy za 15 minut, jeden hlas za 30 dní |
| duplicita | shodný text už v knize je |
| Turnstile | volitelně, viz výše |

O návštěvnících se **nikde neukládá nic**, podle čeho by šli
identifikovat — krátkodobé značky pro limit žijí jen v paměti Cloudflare
a samy vyprší. Do repozitáře se zapisuje jen jméno, město a text, tedy
to, co člověk sám vyplnil.

## Když spam přesto projde

Vrstvy výše zastaví roboty. Placeného člověka, který spam rozesílá ručně,
nezastaví nic kromě schvalování. Pokud by k tomu došlo, řekněte — přepnutí
na režim „nic se nezveřejní bez schválení“ je úprava na pár řádků.
