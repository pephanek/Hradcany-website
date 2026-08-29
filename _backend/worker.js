/**
 * Hradčany — vrátný pro knihu návštěv a anketu.
 *
 * Cloudflare Worker. Sám nic neukládá: co projde kontrolou, zapíše
 * commitem do GitHub repozitáře webu (data/kniha.json, data/anketa.json).
 * Web ta data čte přímo jako statické soubory, takže čtení Worker vůbec
 * nezatěžuje.
 *
 * Tajné proměnné (npx wrangler secret put NAZEV):
 *   GH_TOKEN     – GitHub token s právem Contents: write na repozitář webu
 *   TAJNY_KLIC   – náhodný řetězec, podepisuje formulářové tokeny
 *   TURNSTILE    – tajný klíč Cloudflare Turnstile (volitelné, další vrstva)
 *
 * Běžné proměnné (vars v wrangler.toml):
 *   GH_REPO      – "pephanek/Hradcany-website"
 *   GH_VETEV     – "main"
 *   POVOLENY_WEB – čárkou oddělené originy webu
 */

const VYCHOZI_ORIGINY = [
  'https://www.hradcany-stamps.com',
  'https://hradcany-stamps.com',
];

/* ------------------------------------------------------------ pomocné */
const enc = new TextEncoder();
const b64u = (b) => btoa(String.fromCharCode(...new Uint8Array(b)))
  .replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');

async function hmac(secret, msg) {
  const k = await crypto.subtle.importKey('raw', enc.encode(secret),
    { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  return b64u(await crypto.subtle.sign('HMAC', k, enc.encode(msg)));
}
async function sha(msg) {
  return b64u(await crypto.subtle.digest('SHA-256', enc.encode(msg)));
}

function odpoved(data, status, origin) {
  return new Response(JSON.stringify(data), {
    status: status || 200,
    headers: {
      'content-type': 'application/json; charset=utf-8',
      'cache-control': 'no-store',
      'access-control-allow-origin': origin,
      'access-control-allow-headers': 'content-type',
      'access-control-allow-methods': 'GET,POST,OPTIONS',
      'vary': 'origin',
    },
  });
}

/** Malá písmena, bez diakritiky a interpunkce — pro porovnávání. */
const norm = (s) => (s || '').normalize('NFD').replace(/\p{M}/gu, '')
  .toLowerCase().replace(/[^a-z0-9]+/g, '');

/* ------------------------------------------- krátkodobá paměť (bez KV)
 * Cache API drží jen pomocné značky s krátkou platností. Do repozitáře
 * se nikdy nezapisuje nic, podle čeho by šel návštěvník identifikovat. */
async function znackaJe(klic) {
  const r = await caches.default.match(new Request('https://znacka.local/' + klic));
  return !!r;
}
async function znackaDej(klic, sekund) {
  await caches.default.put(
    new Request('https://znacka.local/' + klic),
    new Response('1', { headers: { 'cache-control': 'max-age=' + sekund } })
  );
}
async function otisk(req, secret) {
  const ip = req.headers.get('cf-connecting-ip') || '0';
  return (await sha(secret + '|' + ip)).slice(0, 24);
}

/* --------------------------------------------- antispam: znalostní otázka */
const OTAZKY = [
  { id: 'rok', a: ['1918'], q: {
      cs: 'V kterém roce vyšly první známky emise Hradčany? (čtyři číslice)',
      en: 'In which year did the first Hradčany stamps appear? (four digits)',
      fr: 'En quelle année sont parus les premiers timbres Hradčany ? (quatre chiffres)',
      de: 'In welchem Jahr erschienen die ersten Hradschin-Marken? (vier Ziffern)',
      es: '¿En qué año aparecieron los primeros sellos Hradčany? (cuatro cifras)' } },
  { id: 'autor', a: ['mucha', 'alfonsmucha', 'alphonsemucha'], q: {
      cs: 'Kdo emisi Hradčany navrhl? (příjmení)',
      en: 'Who designed the Hradčany issue? (surname)',
      fr: 'Qui a dessiné l’émission Hradčany ? (nom de famille)',
      de: 'Wer entwarf die Hradschin-Ausgabe? (Nachname)',
      es: '¿Quién diseñó la emisión Hradčany? (apellido)' } },
  { id: 'mesto', a: ['praha', 'prague', 'prag', 'praga'], q: {
      cs: 'Které město je na známkách vyobrazeno? (jedno slovo)',
      en: 'Which city is depicted on the stamps? (one word)',
      fr: 'Quelle ville figure sur les timbres ? (un mot)',
      de: 'Welche Stadt zeigen die Marken? (ein Wort)',
      es: '¿Qué ciudad aparece en los sellos? (una palabra)' } },
  { id: 'poli', a: ['100', 'sto', 'hundred', 'onehundred', 'cent', 'einhundert', 'hundert', 'cien', 'ciento'], q: {
      cs: 'Kolik známkových polí má jedna tisková deska Hradčan?',
      en: 'How many stamp fields does one Hradčany printing plate have?',
      fr: 'Combien de positions compte une planche d’impression Hradčany ?',
      de: 'Wie viele Markenfelder hat eine Hradschin-Druckplatte?',
      es: '¿Cuántas posiciones tiene una plancha de impresión Hradčany?' } },
];

/* ------------------------------------------------- antispam: obsah zprávy */
const BLOKOVANA = /\b(casino|viagra|cialis|porn|escort|payday|loan|crypto|bitcoin|forex|backlink|betting|kamagra|replica\s*watch|xxx|sex\s*cam)\b/i;
const ODKAZ = /(https?:\/\/|www\.|\b[a-z0-9-]{2,}\.(com|net|org|ru|cn|xyz|top|info|biz|online|site|shop|club|link|store|icu)\b)/i;

function podilCiziAbecedy(t) {
  const pismena = (t.match(/\p{L}/gu) || []).length;
  if (pismena < 12) return 0;
  const cizi = (t.match(/[Ѐ-ӿ؀-ۿ一-鿿぀-ヿ฀-๿]/gu) || []).length;
  return cizi / pismena;
}

function zkontrolujObsah(jmeno, text) {
  const j = (jmeno || '').trim(), t = (text || '').trim();
  if (j.length < 2 || j.length > 40) return 'jmeno';
  if (t.length < 10 || t.length > 1500) return 'delka';
  if (ODKAZ.test(t) || ODKAZ.test(j)) return 'odkaz';
  if (BLOKOVANA.test(t) || BLOKOVANA.test(j)) return 'blokovano';
  if (podilCiziAbecedy(t) > 0.3) return 'pismo';
  if (/(.)\1{9,}/.test(t)) return 'opakovani';
  const slova = t.split(/\s+/);
  if (slova.length > 6 && new Set(slova.map(norm)).size / slova.length < 0.35) return 'opakovani';
  if (/[<>]|&#|javascript:/i.test(t)) return 'znacky';
  return null;
}

async function turnstileOk(env, token, ip) {
  if (!env.TURNSTILE) return true;
  if (!token) return false;
  const r = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
    method: 'POST', headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ secret: env.TURNSTILE, response: token, remoteip: ip }),
  });
  return !!(await r.json().catch(() => ({}))).success;
}

/* ==================================================== GitHub jako úložiště */
const GH = 'https://api.github.com';

function ghHlavicky(env) {
  return {
    authorization: 'Bearer ' + env.GH_TOKEN,
    accept: 'application/vnd.github+json',
    'user-agent': 'hradcany-vratny',
    'content-type': 'application/json',
  };
}

async function ghNacti(env, cesta) {
  const u = `${GH}/repos/${env.GH_REPO}/contents/${cesta}?ref=${env.GH_VETEV || 'main'}`;
  const r = await fetch(u, { headers: ghHlavicky(env) });
  if (r.status === 404) return { data: null, sha: null };
  if (!r.ok) throw new Error('github-cteni-' + r.status);
  const j = await r.json();
  const text = new TextDecoder().decode(
    Uint8Array.from(atob(j.content.replace(/\n/g, '')), c => c.charCodeAt(0)));
  return { data: JSON.parse(text), sha: j.sha };
}

async function ghZapis(env, cesta, data, sha, zprava) {
  const obsah = JSON.stringify(data, null, 1);
  const bytes = new TextEncoder().encode(obsah);
  const b64 = btoa(String.fromCharCode(...bytes));
  const r = await fetch(`${GH}/repos/${env.GH_REPO}/contents/${cesta}`, {
    method: 'PUT',
    headers: ghHlavicky(env),
    body: JSON.stringify({
      message: zprava,
      content: b64,
      sha: sha || undefined,
      branch: env.GH_VETEV || 'main',
    }),
  });
  if (r.status === 409 || r.status === 422) return false;   // mezitím se změnil
  if (!r.ok) throw new Error('github-zapis-' + r.status + ' ' + (await r.text()).slice(0, 120));
  return true;
}

/** Načti → uprav → zapiš, s opakováním při souběžné změně. */
async function uprav(env, cesta, vychozi, zprava, upravFn) {
  for (let pokus = 0; pokus < 4; pokus++) {
    const { data, sha } = await ghNacti(env, cesta);
    const stav = data || vychozi;
    const vysledek = upravFn(stav);
    if (vysledek && vysledek.chyba) return vysledek;
    if (await ghZapis(env, cesta, stav, sha, zprava)) return vysledek || { ok: true };
    await new Promise(r => setTimeout(r, 150 * (pokus + 1)));
  }
  return { chyba: 'soubeh' };
}

/* ================================================================ router */
export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    const povolene = (env.POVOLENY_WEB || VYCHOZI_ORIGINY.join(',')).split(',').map(s => s.trim());
    const zdroj = req.headers.get('origin') || '';
    const origin = povolene.includes(zdroj) ? zdroj : povolene[0];

    if (req.method === 'OPTIONS') return odpoved({}, 204, origin);
    if (zdroj && !povolene.includes(zdroj)) return odpoved({ chyba: 'origin' }, 403, origin);

    const cesta = url.pathname.replace(/^\/+|\/+$/g, '').replace(/^api\//, '');
    try {
      if (cesta === 'formular') return await formular(env, origin);
      if (cesta === 'kniha')    return await kniha(req, env, origin);
      if (cesta === 'anketa')   return await anketa(req, env, origin);
      return odpoved({ chyba: 'neznama-cesta' }, 404, origin);
    } catch (e) {
      return odpoved({ chyba: 'server', detail: String((e && e.message) || e) }, 500, origin);
    }
  },
};

/* -------- GET /formular: podepsaný token + náhodná znalostní otázka ----- */
async function formular(env, origin) {
  const o = OTAZKY[Math.floor(Math.random() * OTAZKY.length)];
  const telo = `${Date.now()}.${o.id}`;
  return odpoved({
    token: `${telo}.${await hmac(env.TAJNY_KLIC, telo)}`,
    otazka: o.q,
    turnstile: !!env.TURNSTILE,
  }, 200, origin);
}

/* -------------------------------- POST /kniha: nový zápis do knihy ------ */
async function kniha(req, env, origin) {
  if (req.method !== 'POST') return odpoved({ chyba: 'metoda' }, 405, origin);
  const d = await req.json().catch(() => ({}));
  const ip = req.headers.get('cf-connecting-ip') || '0';

  // 1) past na roboty — skryté pole musí zůstat prázdné
  if (d.web) return odpoved({ ok: true }, 200, origin);

  // 2) podepsaný token a stáří formuláře
  const c = String(d.token || '').split('.');
  if (c.length !== 3) return odpoved({ chyba: 'token' }, 400, origin);
  if (await hmac(env.TAJNY_KLIC, `${c[0]}.${c[1]}`) !== c[2])
    return odpoved({ chyba: 'token' }, 400, origin);
  const stari = Date.now() - Number(c[0]);
  if (stari < 8000) return odpoved({ chyba: 'rychle' }, 429, origin);
  if (stari > 3 * 3600e3) return odpoved({ chyba: 'stary-formular' }, 400, origin);

  // 3) znalostní otázka
  const otazka = OTAZKY.find(o => o.id === c[1]);
  if (!otazka || !otazka.a.includes(norm(d.odpoved)))
    return odpoved({ chyba: 'odpoved' }, 400, origin);

  // 4) Turnstile, pokud je zapnutý
  if (!(await turnstileOk(env, d.turnstile, ip)))
    return odpoved({ chyba: 'turnstile' }, 400, origin);

  // 5) obsah zprávy
  const duvod = zkontrolujObsah(d.jmeno, d.text);
  if (duvod) return odpoved({ chyba: duvod }, 400, origin);

  // 6) krátkodobý limit na IP (jen v cache, nikam se neukládá)
  const o = await otisk(req, env.TAJNY_KLIC);
  if (await znackaJe('k' + o)) return odpoved({ chyba: 'limit' }, 429, origin);

  const zaznam = {
    jmeno: String(d.jmeno).trim().slice(0, 40),
    mesto: String(d.mesto || '').trim().slice(0, 40),
    text: String(d.text).trim().slice(0, 1500),
    ts: new Date().toISOString(),
    lang: String(d.lang || 'cs').slice(0, 2),
  };

  const vysledek = await uprav(env, 'data/kniha.json',
    { verze: 1, zaznamy: [] },
    `Kniha návštěv: ${zaznam.jmeno}`,
    (stav) => {
      // 7) duplicita proti již uloženým zápisům
      const otiskTextu = norm(zaznam.text).slice(0, 120);
      if (stav.zaznamy.some(z => norm(z.text).slice(0, 120) === otiskTextu))
        return { chyba: 'duplicita' };
      zaznam.id = 'z' + Date.now().toString(36);
      stav.zaznamy.unshift(zaznam);
      if (stav.zaznamy.length > 500) stav.zaznamy.length = 500;
      return { ok: true, zaznam };
    });

  if (vysledek.chyba) return odpoved(vysledek, 400, origin);
  await znackaDej('k' + o, 900);        // 15 minut mezi zápisy
  return odpoved(vysledek, 200, origin);
}

/* --------------------------------------- POST /anketa: hlas v anketě ---- */
async function anketa(req, env, origin) {
  if (req.method !== 'POST') return odpoved({ chyba: 'metoda' }, 405, origin);
  const d = await req.json().catch(() => ({}));
  const volba = String(d.volba || '').slice(0, 24);
  if (!/^[a-z0-9-]+$/.test(volba)) return odpoved({ chyba: 'volba' }, 400, origin);

  const o = await otisk(req, env.TAJNY_KLIC);
  if (await znackaJe('a' + o)) return odpoved({ chyba: 'uz-hlasoval' }, 429, origin);

  const vysledek = await uprav(env, 'data/anketa.json',
    { verze: 1, pocty: {}, celkem: 0 },
    'Anketa: hlas',
    (stav) => {
      stav.pocty[volba] = (stav.pocty[volba] || 0) + 1;
      stav.celkem = (stav.celkem || 0) + 1;
      stav.zmeneno = new Date().toISOString();
      return { ok: true, pocty: stav.pocty, celkem: stav.celkem };
    });

  if (vysledek.chyba) return odpoved(vysledek, 400, origin);
  await znackaDej('a' + o, 30 * 86400);   // jeden hlas na 30 dní
  return odpoved(vysledek, 200, origin);
}
