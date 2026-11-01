# -*- coding: utf-8 -*-
"""build.py <lang> [out.pdf] [pages] : prelozi album_cs.pdf (Visio -> PDF) do jazyka, zachova obrazky, ramecky a rozlozeni."""
import sys, re, fitz
import tr as TR
lang = sys.argv[1]; out = sys.argv[2] if len(sys.argv) > 2 else f'album_{lang}.pdf'
only = set(int(x) for x in sys.argv[3].split(',')) if len(sys.argv) > 3 else None
FD = '/usr/share/fonts/truetype/'
FONTS = {'cr': FD + 'crosextra/Carlito-Regular.ttf', 'cb': FD + 'crosextra/Carlito-Bold.ttf', 'ci': FD + 'crosextra/Carlito-Italic.ttf',
         'cbi': FD + 'crosextra/Carlito-BoldItalic.ttf', 'tsr': FD + 'liberation/LiberationSerif-Regular.ttf'}
FOBJ = {k: fitz.Font(fontfile=v) for k, v in FONTS.items()}
def fkey(span):
    f = span['font']; fl = span['flags']
    if f.endswith('F1'): return 'tsr'
    if fl & 16 and fl & 2: return 'cbi'
    if fl & 16: return 'cb'
    if fl & 2: return 'ci'
    return 'cr'
def width(txt, fk, size): return FOBJ[fk].text_length(txt, fontsize=size)
def col(c): return ((c >> 16) & 255) / 255, ((c >> 8) & 255) / 255, (c & 255) / 255

doc = fitz.open('album_cs.pdf'); PW = doc[0].rect.width
for pn, page in enumerate(doc):
    if only and pn + 1 not in only: continue
    rects = [d['rect'] for d in page.get_drawings() if 50 < d['rect'].width < 330 and 20 < d['rect'].height < 330]
    jobs = []; redact = []; glyphjobs = []
    for b in page.get_text('dict')['blocks']:
        if b['type'] != 0: continue
        lines = [l for l in b['lines'] if ''.join(s['text'] for s in l['spans']).strip()]
        if not lines: continue
        ptxt = ' '.join(''.join(s['text'] for s in l['spans']).strip() for l in lines)
        ptxt = re.sub(r'\s+', ' ', ptxt).strip()
        if ptxt in TR.PARA and len(lines) > 1:
            sp = lines[0]['spans'][0]; fk = fkey(sp); size = sp['size']
            r = fitz.Rect(b['bbox']); r.x1 += 2; r.y1 += 4
            redact.append(fitz.Rect(r))
            # rozsirit dolu az k dalsimu bloku (text/obrazek), aby se delsi preklad nemusel zmensovat
            nxt = [bb['bbox'][1] for bb in page.get_text('dict')['blocks'] if bb['bbox'][1] > r.y1 - 2 and bb['bbox'][2] > r.x0 and bb['bbox'][0] < r.x1]
            lim = min(nxt) - 3 if nxt else r.y1 + 20
            r.y1 = max(r.y1, min(lim, r.y1 + 60))
            jobs.append(('para', r, TR.tr(ptxt, lang), fk, size, col(sp['color'])))
            continue
        for l in lines:
            spans = [s for s in l['spans'] if s['text'].strip()]
            glyph = [s for s in spans if s['font'].endswith('F6')]
            rest = [s for s in spans if not s['font'].endswith('F6')]
            if not rest: continue
            txt = ''.join(s['text'] for s in rest).strip(); ttxt = TR.tr(txt, lang)
            if ttxt == txt: continue
            sp = rest[0]; fk = fkey(sp); size = sp['size']; c = col(sp['color'])
            r = fitz.Rect(rest[0]['bbox'])
            for s in rest[1:]: r |= fitz.Rect(s['bbox'])
            lr = fitz.Rect(l['bbox']); cx = (r.x0 + r.x1) / 2
            x0 = rest[0]['origin'][0]; y = rest[0]['origin'][1]
            w = width(ttxt, fk, size)
            if glyph:
                avail = PW - 45 - x0; mode = 'left'
            else:
                tgt = None
                cand = [q for q in rects if r.width <= q.width + 6 and q.x0 - 4 <= cx <= q.x1 + 4 and (q.y0 - 2 <= lr.y0 and lr.y1 <= q.y1 + 2 or 0 <= q.y0 - lr.y1 <= 40)]
                if abs(cx - PW / 2) < 3 or (abs(cx - PW / 2) < 12 and (r.width > 150 or not cand or min(cand, key=lambda q: q.width).width < 110)):
                    tgt = PW / 2; avail = PW - 100
                    if cand: avail = max(min(cand, key=lambda q: q.width).width + 30, 120)
                elif cand:
                    q = min(cand, key=lambda q: q.width); tgt = (q.x0 + q.x1) / 2; avail = q.width - 4
                else:
                    avail = PW - 45 - x0
                mode = 'center' if tgt is not None else 'left'
            fs = size
            while w > avail and fs > size * 0.6: fs -= 0.25; w = width(ttxt, fk, fs)
            x = (tgt - w / 2) if mode == 'center' else x0
            redact.append(r); jobs.append(('line', fitz.Point(x, y), ttxt, fk, fs, c))
            if fs < size: print(f'  shrink p{pn+1} {size}->{fs} avail {avail:.0f} w {width(ttxt, fk, size):.0f} mode {mode} :: {ttxt[:50]}')
    for r in redact: page.add_redact_annot(r)
    page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_NONE)
    for j in jobs:
        if j[0] == 'line':
            _, p, t, fk, fs, c = j; page.insert_text(p, t, fontsize=fs, fontname=fk, fontfile=FONTS[fk], color=c)
        else:
            _, r, t, fk, fs, c = j; f = fs; lh = 1.08
            while True:
                rc = page.insert_textbox(r, t, fontsize=f, fontname=fk, fontfile=FONTS[fk], color=c, align=fitz.TEXT_ALIGN_JUSTIFY if r.height > 20 else fitz.TEXT_ALIGN_LEFT, lineheight=lh)
                if rc >= 0 or f < fs * 0.6: break
                if lh > 0.98: lh -= 0.04
                else: f -= 0.25
            if f < fs: print(f'  para shrink p{pn+1} {fs:.1f}->{f:.2f} lh {lh:.2f} :: {t[:40]}')
            if rc < 0: print('  OVERFLOW page', pn + 1, t[:40])
    print('page', pn + 1, 'lines', len(jobs))
if only:
    doc.select([p - 1 for p in sorted(only)])
doc.save(out, garbage=3, deflate=True); print('saved', out)
