# -*- coding: utf-8 -*-
"""
Měření návštěvnosti (Cloudflare Web Analytics).

Zajistí, že každá HTML stránka webu má těsně před </head> měřicí skript.
Spouští se samo na začátku build-jazyky.py a před každou automatickou
publikací. Ručně:  python _backend/analytics.py

Vynechává složky začínající podtržítkem (_backups, _tmp_upload, _backend…)
a složky assets/ (mapa razítek v iframe a její zálohy by se jinak
započítávaly jako samostatné návštěvy).
Statistiky: Cloudflare → Web Analytics → www.hradcany-stamps.com
"""
import os

SNIPPET = ("<!-- Cloudflare Web Analytics --><script type='module' "
           "src='https://static.cloudflareinsights.com/beacon.min.js' "
           "data-cf-beacon='{\"token\": \"b3238fffc2414045a9fa85609c50e8e4\"}'>"
           "</script><!-- End Cloudflare Web Analytics -->")
MARK = 'static.cloudflareinsights.com/beacon.min.js'
SKIP_DIRS = {'assets', 'i18n', 'scripts', 'node_modules'}

KOREN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def stranky(root=KOREN):
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in SKIP_DIRS
                 and not d.startswith('.') and not d.startswith('_')]
        for f in sorted(fn):
            if f.endswith('.html'):
                yield os.path.join(dp, f)


def ensure(root=KOREN, verbose=True):
    doplneno, spatne, celkem = [], [], 0
    for p in stranky(root):
        celkem += 1
        with open(p, 'rb') as fh:
            s = fh.read().decode('utf-8')
        if MARK in s:
            continue
        if s.count('</head>') != 1:
            spatne.append(p)
            continue
        nl = '\r\n' if '\r\n' in s else '\n'
        s = s.replace('</head>', SNIPPET + nl + '</head>', 1)
        with open(p, 'wb') as fh:
            fh.write(s.encode('utf-8'))
        doplneno.append(os.path.relpath(p, root).replace('\\', '/'))
    if verbose:
        print('analytics: %d stranek, skript doplnen do %d' % (celkem, len(doplneno)))
        for a in doplneno[:20]:
            print('   +', a)
        for b in spatne:
            print('   POZOR: nema prave jedno </head>, preskoceno:',
                  os.path.relpath(b, root).replace('\\', '/'))
    return doplneno, spatne


if __name__ == '__main__':
    ensure()
