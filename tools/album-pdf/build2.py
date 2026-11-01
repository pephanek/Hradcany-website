# -*- coding: utf-8 -*-
"""build2.py <src.pdf> <lang> <out.pdf> <dict.json> [pages]
Preklad PDF z Bullzip (Calibri/Times): fragmenty a sdruzene popisky (frag.py), prekladovy slovnik popisku (dict.json: cs -> [en,de,fr,es]),
ostatni radky pres tr.tr (barvy, hlavicky, 'den vydani', ...). Zachova obrazky a kresby."""
import sys, re, json, fitz
import tr as TR, frag
src, lang, out, dpath = sys.argv[1:5]
only = set(int(x) for x in sys.argv[5].split(',')) if len(sys.argv) > 5 else None
D = json.load(open(dpath, encoding='utf-8')); LI = TR.LI[lang]
FD = '/usr/share/fonts/truetype/'
FONTS = {'cr': FD + 'crosextra/Carlito-Regular.ttf', 'cb': FD + 'crosextra/Carlito-Bold.ttf', 'ci': FD + 'crosextra/Carlito-Italic.ttf',
         'cbi': FD + 'crosextra/Carlito-BoldItalic.ttf', 'tsr': FD + 'liberation/LiberationSerif-Regular.ttf'}
FOBJ = {k: fitz.Font(fontfile=v) for k, v in FONTS.items()}
def fkey(font, flags):
    if 'Times' in font: return 'tsr'
    b = 'Bold' in font or bool(flags & 16); i = 'Italic' in font or bool(flags & 2)
    return 'cbi' if b and i else 'cb' if b else 'ci' if i else 'cr'
def width(t, fk, s): return FOBJ[fk].text_length(t, fontsize=s)
def col(c): return ((c >> 16) & 255) / 255, ((c >> 8) & 255) / 255, (c & 255) / 255
MISS = set()

def tr_line(t):
    """nepopiskove radky: hlavicky 'YYYY-YY, Hradčany - Deskové vady (n. část)', 'Nh barva - Tisková deska k', 'Nh barva', barvy, atd."""
    s = t.strip()
    m = re.match(r'^(\d{4}(?:-\d\d)?), Hradčany - Deskové vady\s*\((\d+)\. část\)$', s)
    if m:
        y, n = m.groups()
        return {'en': f'{y}, Hradčany – Plate varieties (part {n})', 'de': f'{y}, Hradčany – Plattenfehler (Teil {n})',
                'fr': f'{y}, Hradčany – Variétés de planche ({n}e partie)', 'es': f'{y}, Hradčany – Variedades de plancha (parte {n})'}[lang]
    m = re.match(r'^(\d+h) (.+?) - Tisková deska (\d+)$', s)
    if m:
        v, c, k = m.groups(); cc = TR.tr(c, lang)
        return {'en': f'{v} {cc} – printing plate {k}', 'de': f'{v} {cc} – Druckplatte {k}', 'fr': f'{v} {cc} – planche {k}', 'es': f'{v} {cc} – plancha {k}'}[lang]
    if s in D: return D[s][LI]
    r = TR.tr(s, lang)
    if r == s and re.search(r'[ěščřžýáíéúůóťďĚŠČŘŽÝÁÍÉÚŮ]', s) and s not in ('ČESKOSLOVENSKO 1918 – 1939',): MISS.add(s)
    return r

def tr_cap(t):
    m = re.match(r'^(\d+/\d+[a-z]?)\s*(.*)$', t.strip(), re.S)
    cid, body = m.group(1), re.sub(r'\s+', ' ', m.group(2)).strip()
    if body in D: return cid + ' ' + D[body][LI]
    r = TR.tr(body, lang)
    if r != body: return cid + ' ' + r
    MISS.add(body); return t

def wrap(t, fk, fs, maxw):
    words = t.split(' '); lines = []; cur = ''
    for w in words:
        c = (cur + ' ' + w).strip()
        if width(c, fk, fs) <= maxw or not cur: cur = c
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

doc = fitz.open(src); PW = doc[0].rect.width
for pn, page in enumerate(doc):
    if only and pn + 1 not in only: continue
    items = frag.items(page); jobs = []
    for it in items:
        fk = fkey(it['font'], it['flags']); fs = it['size']; c = col(it['color']); r = it['rect']
        if it['kind'] == 'cap':
            new = tr_cap(it['text'])
            if new == it['text']: continue
            cx = (r.x0 + r.x1) / 2; nl = len(it['lines']); lh = (it['lines'][1][1][1] - it['lines'][0][1][1]) if nl > 1 else fs * 1.2
            others = [abs((o['rect'].x0 + o['rect'].x1) / 2 - cx) for o in items if o is not it and o['kind'] == 'cap' and abs(o['rect'].y0 - r.y0) < 30]
            others = [d for d in others if d > 20]
            maxw = (min(others) - 10) if others else 125; f = fs
            while True:
                ls = wrap(new, fk, f, maxw)
                if len(ls) <= 3 or f <= fs * 0.75: break
                f -= 0.25
            y0 = it['lines'][0][1][1]
            page.add_redact_annot(fitz.Rect(r.x0 - 1, r.y0 - 1, r.x1 + 1, r.y1 + 1))
            for k, l in enumerate(ls):
                w = width(l, fk, f); jobs.append((fitz.Point(cx - w / 2, y0 + k * lh * (f / fs)), l, fk, f, c))
        else:
            new = tr_line(it['text'])
            if new == it['text']: continue
            cx = (r.x0 + r.x1) / 2; x0, y = it['lines'][0][1]
            center = abs(cx - PW / 2) < 12 or r.width > 60
            f = fs; w = width(new, fk, f); avail = (PW - 90) if abs(cx - PW / 2) < 12 else max(r.width + 24, 90)
            while w > avail and f > fs * 0.7: f -= 0.25; w = width(new, fk, f)
            x = cx - w / 2 if center else x0
            page.add_redact_annot(fitz.Rect(r.x0 - 1, r.y0 - 1, r.x1 + 1, r.y1 + 1)); jobs.append((fitz.Point(x, y), new, fk, f, c))
    page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_NONE)
    for p, t, fk, f, c in jobs: page.insert_text(p, t, fontsize=f, fontname=fk, fontfile=FONTS[fk], color=c)
    if (pn + 1) % 10 == 0: print('page', pn + 1, 'jobs', len(jobs))
if only: doc.select([p - 1 for p in sorted(only)])
doc.save(out, garbage=3, deflate=True); print('saved', out, 'MISS', len(MISS))
for m in sorted(MISS)[:40]: print('  MISS', repr(m))
