/* Hradčany — kniha návštěv a anketa.
 *
 * Zápis jde přes Worker (adresa v API níže), čtení přímo ze statických
 * souborů data/*.json. Skript si sám odvodí, kde je kořen webu, takže
 * funguje stejně v češtině i v jazykových složkách en/ fr/ de/ es/.
 */
(function () {
  'use strict';

  // ---- NASTAVENÍ ------------------------------------------------------
  // Adresu vypíše `npx wrangler deploy`. Dokud sem nepřijde, formulář
  // se nezobrazí a stránka jen slušně oznámí, že zápis zatím neběží.
  var API = 'https://hradcany-vratny.pepa-matousek.workers.dev';
  var TURNSTILE_KEY = '';       // volitelné, site key z Cloudflare Turnstile
  // ---------------------------------------------------------------------

  var me = document.currentScript || (function () {
    var s = document.getElementsByTagName('script');
    return s[s.length - 1];
  })();
  var KOREN = me.src.replace(/js\/komunita\.js.*$/, '');
  var LANG = (document.documentElement.lang || 'cs').slice(0, 2);

  var T = {
    cs: { jmeno:'Jméno', mesto:'Město (nepovinné)', zprava:'Vzkaz', odeslat:'Odeslat',
          odesilam:'Odesílám…', diky:'Děkuji za vzkaz! Ostatním se ukáže během chvilky.',
          prazdno:'Zatím tu není žádný vzkaz. Můžete být první.',
          nacitam:'Načítám…', nedostupne:'Kniha návštěv se právě nedaří načíst.',
          zapisVypnut:'Zápis do knihy zatím není spuštěný.',
          hlasovat:'Hlasovat', hlasu:'hlasů', hlas:'hlas', hlasy:'hlasy',
          dikyHlas:'Děkuji za hlas.', vysledky:'Zobrazit výsledky',
          uzHlasoval:'V této anketě jste už hlasoval.', bezHlasu:'Zatím nikdo nehlasoval.',
          chyby:{ jmeno:'Vyplňte prosím jméno (2–40 znaků).',
                  delka:'Vzkaz musí mít 10 až 1500 znaků.',
                  odkaz:'Vzkaz nesmí obsahovat odkaz.',
                  odpoved:'Odpověď na kontrolní otázku nesouhlasí.',
                  rychle:'Chviličku — formulář byl odeslán příliš rychle.',
                  limit:'Z této adresy už jeden vzkaz přišel. Zkuste to za chvíli.',
                  duplicita:'Tenhle text už v knize je.',
                  'uz-hlasoval':'V této anketě jste už hlasoval.',
                  jine:'Vzkaz se nepodařilo uložit. Zkuste to prosím znovu.' } },
    en: { jmeno:'Name', mesto:'Town (optional)', zprava:'Message', odeslat:'Send',
          odesilam:'Sending…', diky:'Thank you! Your message will appear for others shortly.',
          prazdno:'No messages yet. You could be the first.',
          nacitam:'Loading…', nedostupne:'The guestbook cannot be loaded right now.',
          zapisVypnut:'The guestbook is not accepting messages yet.',
          hlasovat:'Vote', hlasu:'votes', hlas:'vote', hlasy:'votes',
          dikyHlas:'Thank you for voting.', vysledky:'Show results',
          uzHlasoval:'You have already voted in this poll.', bezHlasu:'No votes yet.',
          chyby:{ jmeno:'Please enter a name (2–40 characters).',
                  delka:'The message must be 10 to 1500 characters.',
                  odkaz:'The message may not contain a link.',
                  odpoved:'The answer to the check question is not right.',
                  rychle:'One moment — the form was sent too quickly.',
                  limit:'A message from this address has just arrived. Please try later.',
                  duplicita:'That text is already in the guestbook.',
                  'uz-hlasoval':'You have already voted in this poll.',
                  jine:'The message could not be saved. Please try again.' } },
    fr: { jmeno:'Nom', mesto:'Ville (facultatif)', zprava:'Message', odeslat:'Envoyer',
          odesilam:'Envoi…', diky:'Merci ! Votre message apparaîtra sous peu.',
          prazdno:'Aucun message pour l’instant. Vous pouvez être le premier.',
          nacitam:'Chargement…', nedostupne:'Le livre d’or ne peut pas être chargé.',
          zapisVypnut:'Le livre d’or n’accepte pas encore de messages.',
          hlasovat:'Voter', hlasu:'voix', hlas:'voix', hlasy:'voix',
          dikyHlas:'Merci de votre vote.', vysledky:'Afficher les résultats',
          uzHlasoval:'Vous avez déjà voté.', bezHlasu:'Aucun vote pour l’instant.',
          chyby:{ jmeno:'Indiquez un nom (2 à 40 caractères).',
                  delka:'Le message doit faire de 10 à 1500 caractères.',
                  odkaz:'Le message ne peut pas contenir de lien.',
                  odpoved:'La réponse à la question de contrôle est incorrecte.',
                  rychle:'Un instant — le formulaire a été envoyé trop vite.',
                  limit:'Un message vient déjà d’arriver de cette adresse. Réessayez plus tard.',
                  duplicita:'Ce texte figure déjà dans le livre d’or.',
                  'uz-hlasoval':'Vous avez déjà voté.',
                  jine:'Le message n’a pas pu être enregistré. Réessayez.' } },
    de: { jmeno:'Name', mesto:'Ort (optional)', zprava:'Nachricht', odeslat:'Senden',
          odesilam:'Wird gesendet…', diky:'Danke! Ihre Nachricht erscheint in Kürze.',
          prazdno:'Noch keine Einträge. Sie können der erste sein.',
          nacitam:'Wird geladen…', nedostupne:'Das Gästebuch lässt sich gerade nicht laden.',
          zapisVypnut:'Das Gästebuch nimmt noch keine Einträge an.',
          hlasovat:'Abstimmen', hlasu:'Stimmen', hlas:'Stimme', hlasy:'Stimmen',
          dikyHlas:'Danke für Ihre Stimme.', vysledky:'Ergebnisse anzeigen',
          uzHlasoval:'Sie haben bereits abgestimmt.', bezHlasu:'Noch keine Stimmen.',
          chyby:{ jmeno:'Bitte geben Sie einen Namen an (2–40 Zeichen).',
                  delka:'Die Nachricht muss 10 bis 1500 Zeichen haben.',
                  odkaz:'Die Nachricht darf keinen Link enthalten.',
                  odpoved:'Die Antwort auf die Kontrollfrage stimmt nicht.',
                  rychle:'Einen Moment — das Formular wurde zu schnell abgeschickt.',
                  limit:'Von dieser Adresse kam soeben schon eine Nachricht. Bitte später erneut.',
                  duplicita:'Dieser Text steht bereits im Gästebuch.',
                  'uz-hlasoval':'Sie haben bereits abgestimmt.',
                  jine:'Die Nachricht konnte nicht gespeichert werden. Bitte erneut versuchen.' } },
    es: { jmeno:'Nombre', mesto:'Ciudad (opcional)', zprava:'Mensaje', odeslat:'Enviar',
          odesilam:'Enviando…', diky:'¡Gracias! Su mensaje aparecerá en breve.',
          prazdno:'Aún no hay mensajes. Puede ser el primero.',
          nacitam:'Cargando…', nedostupne:'El libro de visitas no se puede cargar ahora.',
          zapisVypnut:'El libro de visitas aún no admite mensajes.',
          hlasovat:'Votar', hlasu:'votos', hlas:'voto', hlasy:'votos',
          dikyHlas:'Gracias por su voto.', vysledky:'Ver resultados',
          uzHlasoval:'Ya ha votado en esta encuesta.', bezHlasu:'Aún no hay votos.',
          chyby:{ jmeno:'Indique un nombre (2 a 40 caracteres).',
                  delka:'El mensaje debe tener de 10 a 1500 caracteres.',
                  odkaz:'El mensaje no puede contener enlaces.',
                  odpoved:'La respuesta a la pregunta de control no es correcta.',
                  rychle:'Un momento: el formulario se envió demasiado rápido.',
                  limit:'Acaba de llegar un mensaje desde esta dirección. Inténtelo más tarde.',
                  duplicita:'Ese texto ya está en el libro de visitas.',
                  'uz-hlasoval':'Ya ha votado en esta encuesta.',
                  jine:'No se pudo guardar el mensaje. Inténtelo de nuevo.' } },
  }[LANG] || null;
  if (!T) return;

  var esc = function (s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;' }[c];
    });
  };
  var datum = function (iso) {
    try { return new Date(iso).toLocaleDateString(LANG, { year:'numeric', month:'long', day:'numeric' }); }
    catch (e) { return (iso || '').slice(0, 10); }
  };
  var pocetSlovem = function (n) {
    if (LANG !== 'cs') return n === 1 ? T.hlas : T.hlasu;
    if (n === 1) return 'hlas';
    if (n >= 2 && n <= 4) return 'hlasy';
    return 'hlasů';
  };
  var post = function (cesta, telo) {
    return fetch(API.replace(/\/+$/, '') + cesta, {
      method: 'POST', headers: { 'content-type': 'application/json' },
      body: JSON.stringify(telo),
    }).then(function (r) { return r.json().catch(function () { return { chyba: 'jine' }; }); });
  };

  /* ==================================================== KNIHA NÁVŠTĚV */
  var kniha = document.getElementById('kniha');
  if (kniha) (function () {
    var vypis = kniha.querySelector('.kn-vypis');
    var misto = kniha.querySelector('.kn-formular');

    // --- výpis: statický soubor, žádné volání na server ---------------
    vypis.innerHTML = '<p class="muted">' + esc(T.nacitam) + '</p>';
    fetch(KOREN + 'data/kniha.json', { cache: 'no-cache' })
      .then(function (r) { return r.json(); })
      .then(function (d) { vykresli(d.zaznamy || []); })
      .catch(function () { vypis.innerHTML = '<p class="muted">' + esc(T.nedostupne) + '</p>'; });

    function vykresli(z) {
      if (!z.length) { vypis.innerHTML = '<p class="muted">' + esc(T.prazdno) + '</p>'; return; }
      vypis.innerHTML = z.map(function (v) {
        return '<article class="kn-zaznam"><header><strong>' + esc(v.jmeno) + '</strong>' +
          (v.mesto ? ' <span class="kn-mesto">' + esc(v.mesto) + '</span>' : '') +
          '<time>' + esc(datum(v.ts)) + '</time></header><p>' +
          esc(v.text).replace(/\n+/g, '<br>') + '</p></article>';
      }).join('');
    }

    // --- formulář: až po načtení tokenu od vrátného -------------------
    if (!API) { misto.innerHTML = '<p class="muted">' + esc(T.zapisVypnut) + '</p>'; return; }

    fetch(API.replace(/\/+$/, '') + '/formular')
      .then(function (r) {
        return r.json().catch(function () { return { chyba: 'html', stav: r.status }; })
                .then(function (d) { d.stav = r.status; return d; });
      })
      .then(function (f) {
        if (!f || !f.otazka) {
          // ať je z webu poznat, co přesně vázne — bez toho se to hádá naslepo
          var proc = f && f.chyba ? f.chyba : 'bez odpovědi';
          misto.innerHTML = '<p class="muted">' + esc(T.nedostupne) +
            ' <span class="kn-detail">(' + esc(proc) + ', HTTP ' + esc(f && f.stav || '?') + ')</span></p>';
          return;
        }
        postavFormular(f);
      })
      .catch(function (e) {
        // sem se to dostane, když prohlížeč spojení vůbec nepustí — typicky CORS
        misto.innerHTML = '<p class="muted">' + esc(T.nedostupne) +
          ' <span class="kn-detail">(spojení zamítnuto — zkontrolujte POVOLENY_WEB)</span></p>';
      });

    function postavFormular(f) {
      misto.innerHTML =
        '<form class="kn-form" novalidate>' +
          '<div class="kn-radek">' +
            '<label>' + esc(T.jmeno) + ' <input name="jmeno" maxlength="40" required></label>' +
            '<label>' + esc(T.mesto) + ' <input name="mesto" maxlength="40"></label>' +
          '</div>' +
          '<label class="kn-blok">' + esc(T.zprava) +
            ' <textarea name="text" rows="5" maxlength="1500" required></textarea></label>' +
          '<label class="kn-blok kn-otazka">' + esc(f.otazka[LANG] || f.otazka.cs) +
            ' <input name="odpoved" autocomplete="off" required></label>' +
          '<div class="kn-past" aria-hidden="true">' +
            '<label>Web <input name="web" tabindex="-1" autocomplete="off"></label></div>' +
          (f.turnstile && TURNSTILE_KEY ? '<div class="cf-turnstile" data-sitekey="' + TURNSTILE_KEY + '"></div>' : '') +
          '<div class="kn-akce"><button type="submit" class="kn-btn">' + esc(T.odeslat) + '</button>' +
            '<span class="kn-stav" role="status"></span></div>' +
        '</form>';

      if (f.turnstile && TURNSTILE_KEY && !window.turnstile) {
        var s = document.createElement('script');
        s.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js';
        s.async = true; s.defer = true; document.head.appendChild(s);
      }

      var form = misto.querySelector('form');
      var stav = misto.querySelector('.kn-stav');
      var btn = misto.querySelector('.kn-btn');

      form.addEventListener('submit', function (e) {
        e.preventDefault();
        var d = {
          token: f.token, lang: LANG,
          jmeno: form.jmeno.value, mesto: form.mesto.value,
          text: form.text.value, odpoved: form.odpoved.value, web: form.web.value,
        };
        if (window.turnstile) {
          var t = form.querySelector('[name="cf-turnstile-response"]');
          if (t) d.turnstile = t.value;
        }
        btn.disabled = true;
        stav.className = 'kn-stav';
        stav.textContent = T.odesilam;

        post('/kniha', d).then(function (r) {
          if (r && r.ok) {
            stav.className = 'kn-stav kn-ok';
            stav.textContent = T.diky;
            form.reset();
            if (r.zaznam) {
              var p = document.createElement('div');
              p.innerHTML = '<article class="kn-zaznam kn-novy"><header><strong>' +
                esc(r.zaznam.jmeno) + '</strong>' +
                (r.zaznam.mesto ? ' <span class="kn-mesto">' + esc(r.zaznam.mesto) + '</span>' : '') +
                '<time>' + esc(datum(r.zaznam.ts)) + '</time></header><p>' +
                esc(r.zaznam.text).replace(/\n+/g, '<br>') + '</p></article>';
              if (vypis.querySelector('.muted')) vypis.innerHTML = '';
              vypis.insertBefore(p.firstChild, vypis.firstChild);
            }
          } else {
            stav.className = 'kn-stav kn-chyba';
            var kod = r && r.chyba;
            if (T.chyby[kod]) {
              stav.textContent = T.chyby[kod];
            } else {
              // neznámý kód = závada na straně vrátného; ať je vidět, která
              stav.innerHTML = esc(T.chyby.jine) +
                ' <span class="kn-detail">(' + esc(kod || 'bez kódu') +
                (r && r.detail ? ': ' + esc(String(r.detail).slice(0, 120)) : '') + ')</span>';
            }
            btn.disabled = false;
          }
        }).catch(function () {
          stav.className = 'kn-stav kn-chyba';
          stav.textContent = T.chyby.jine;
          btn.disabled = false;
        });
      });
    }
  })();

  /* ============================================================ ANKETA */
  var anketa = document.getElementById('anketa');
  if (anketa) (function () {
    var moznosti = [].slice.call(anketa.querySelectorAll('.an-moznost'));
    var vysledky = anketa.querySelector('.an-vysledky');
    var akce = anketa.querySelector('.an-akce');
    var stav = anketa.querySelector('.an-stav');
    var KLIC = 'hradcany-anketa';
    var uzHlasoval = false;
    try { uzHlasoval = !!localStorage.getItem(KLIC); } catch (e) {}

    var data = null;
    fetch(KOREN + 'data/anketa.json', { cache: 'no-cache' })
      .then(function (r) { return r.json(); })
      .then(function (d) { data = d; if (uzHlasoval) ukazVysledky(); })
      .catch(function () { data = { pocty: {}, celkem: 0 }; });

    if (uzHlasoval) {
      anketa.classList.add('an-hotovo');
      stav.textContent = T.uzHlasoval;
    }

    moznosti.forEach(function (m) {
      m.addEventListener('click', function () {
        if (anketa.classList.contains('an-hotovo')) { ukazVysledky(); return; }
        moznosti.forEach(function (x) { x.classList.remove('vybrano'); });
        m.classList.add('vybrano');
        akce.querySelector('.an-btn').disabled = false;
      });
    });

    var odkazVysledky = akce.querySelector('.an-odkaz');
    if (odkazVysledky) odkazVysledky.addEventListener('click', function (e) {
      e.preventDefault(); ukazVysledky();
    });

    akce.querySelector('.an-btn').addEventListener('click', function () {
      var v = anketa.querySelector('.an-moznost.vybrano');
      if (!v) return;
      if (!API) { stav.textContent = T.zapisVypnut; return; }
      var btn = this;
      btn.disabled = true;
      stav.className = 'an-stav';
      stav.textContent = T.odesilam;
      post('/anketa', { volba: v.dataset.id }).then(function (r) {
        if (r && r.ok) {
          try { localStorage.setItem(KLIC, v.dataset.id); } catch (e) {}
          data = { pocty: r.pocty, celkem: r.celkem };
          anketa.classList.add('an-hotovo');
          stav.className = 'an-stav an-ok';
          stav.textContent = T.dikyHlas;
          ukazVysledky();
        } else {
          stav.className = 'an-stav an-chyba';
          stav.textContent = T.chyby[(r && r.chyba)] || T.chyby.jine;
          if (r && r.chyba === 'uz-hlasoval') {
            try { localStorage.setItem(KLIC, '1'); } catch (e) {}
            anketa.classList.add('an-hotovo'); ukazVysledky();
          } else { btn.disabled = false; }
        }
      }).catch(function () {
        stav.className = 'an-stav an-chyba';
        stav.textContent = T.chyby.jine;
        btn.disabled = false;
      });
    });

    function ukazVysledky() {
      if (!data) return;
      var celkem = data.celkem || 0;
      vysledky.hidden = false;
      if (!celkem) { vysledky.innerHTML = '<p class="muted">' + esc(T.bezHlasu) + '</p>'; return; }
      var moje = null;
      try { moje = localStorage.getItem(KLIC); } catch (e) {}
      var radky = moznosti.map(function (m) {
        var n = data.pocty[m.dataset.id] || 0;
        // innerText bere jen viditelný text — v české verzi jsou anglické
        // varianty skryté přes CSS a nesmí se do popisku připlést
        var vid = function (el) { return el ? (el.innerText || el.textContent || '') : ''; };
        var popis = (vid(m.querySelector('.an-pv')) + ' ' + vid(m.querySelector('.an-pt')))
                      .replace(/\s+/g, ' ').trim() || m.dataset.popis || m.dataset.id;
        return { id: m.dataset.id, popis: popis, n: n };
      }).sort(function (a, b) { return b.n - a.n; });
      vysledky.innerHTML =
        '<p class="an-celkem">' + celkem + '&nbsp;' + esc(pocetSlovem(celkem)) + '</p>' +
        radky.map(function (r) {
          var pct = celkem ? Math.round(r.n / celkem * 1000) / 10 : 0;
          return '<div class="an-radek' + (r.id === moje ? ' an-moje' : '') + '">' +
            '<span class="an-jmeno">' + esc(r.popis) + '</span>' +
            '<span class="an-pruh"><span style="width:' + pct + '%"></span></span>' +
            '<span class="an-cislo">' + r.n + '</span></div>';
        }).join('');
    }
  })();
})();
