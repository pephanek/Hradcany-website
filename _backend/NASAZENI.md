# Nasazení vrátného přes prohlížeč

Příkazová řádka není potřeba. Cloudflare má v prohlížeči editor,
do kterého se kód jen vloží.

## 1. Účet

<https://dash.cloudflare.com/sign-up> — zdarma, stačí e‑mail.
Doménu tam registrovat nemusíte, web zůstává na GitHub Pages.

## 2. Vytvořit Worker

Workers & Pages → **Create** → záložka **Workers** → **Start with Hello World**
→ jméno **`hradcany-vratny`** → **Deploy**.

Vznikne prázdný Worker na adrese
`https://hradcany-vratny.<vas-ucet>.workers.dev`. Tu adresu si opište,
budeme ji potřebovat.

## 3. Vložit kód

U vytvořeného Workeru → **Edit code**. V editoru **smažte všechno**
a vložte celý obsah souboru `_backend/worker.js`. Pak **Deploy**.

## 4. Druhý GitHub token (jen pro vrátného)

Na <https://github.com/settings/personal-access-tokens> → Generate new
token → *Fine-grained*:

- Only select repositories → **Hradcany-website**
- Repository permissions → **Contents: Read and write**
- expirace třeba 1 rok

Tenhle token je **jiný** než ten publikační. Kdyby bylo potřeba jeden
zneplatnit, druhá věc pojede dál.

## 5. Proměnné

U Workeru → **Settings** → **Variables and Secrets**. Přidejte:

| jméno | typ | hodnota |
|---|---|---|
| `GH_TOKEN` | **Secret** | token z kroku 4 |
| `TAJNY_KLIC` | **Secret** | náhodný řetězec (dostanete ode mě) |
| `GH_REPO` | Text | `pephanek/Hradcany-website` |
| `GH_VETEV` | Text | `main` |
| `POVOLENY_WEB` | Text | `https://www.hradcany-stamps.com,https://hradcany-stamps.com` |

Typ **Secret** znamená, že se hodnota po uložení už nikde nezobrazí —
to je u obou tokenů správně. Nakonec **Deploy**.

## 6. Adresu poslat mně

Pošlete adresu z kroku 2. Doplním ji do `js/komunita.js`, přegeneruji
jazykové verze a rovnou vyzkouším, že kniha i anketa fungují.

## 7. Volitelně později

- **Vlastní doména** místo `workers.dev`: Settings → Domains & Routes →
  Add custom domain, `api.hradcany-stamps.com`. Vyžaduje, aby doména
  byla v Cloudflare DNS — není nutné.
- **Turnstile** jako další vrstva proti spamu: viz README.md.

## Proč to nemůžu nasadit ani vyzkoušet já

Prostředí, ve kterém pracuji, pouští ven jen vyjmenované adresy —
GitHub a npm ano, `cloudflare.com`, `workers.dev` **ani samotné
`www.hradcany-stamps.com`** ne. Není to nastavení na Vašem počítači
ani na routeru, takže s tím nejde nic udělat; Váš prohlížeč tím ale
omezený není.

Prakticky to znamená: kód napíšu, zapojím a otestuji nanečisto proti
místní napodobenině (což je hotové), ale **naostro to uvidíte až Vy
v prohlížeči**. Proto je v kroku 6 kontrolní seznam.

## 6b. Co po nasazení zkontrolovat

1. Otevřete `https://www.hradcany-stamps.com/kniha-navstev.html`.
   Místo věty „Zápis do knihy zatím není spuštěný“ se má objevit
   formulář s kontrolní otázkou k emisi.
2. Napište zkušební vzkaz a odešlete. Má se objevit poděkování
   a vzkaz hned nahoře v seznamu.
3. Do minuty se objeví commit v repozitáři (`data/kniha.json`).
4. Na homepage zkuste hlasovat v anketě — po hlasu se mají ukázat
   výsledky s pruhy.

Kdyby se místo toho objevila chybová hláška:

| hláška | příčina |
|---|---|
| „Kniha návštěv se právě nedaří načíst" | Worker neodpovídá — špatná adresa v `js/komunita.js`, nebo není nasazený |
| „Odpověď na kontrolní otázku nesouhlasí" | to je v pořádku, jen špatná odpověď |
| „Vzkaz se nepodařilo uložit" | chybí `GH_TOKEN` nebo `TAJNY_KLIC`, nebo token nemá právo zápisu |
| formulář se vůbec nenačte | `POVOLENY_WEB` neodpovídá adrese webu |
