# -*- coding: utf-8 -*-
"""frag.py : rozdeli text PDF na fragmenty (spany oddelene mezerou > GAP) a sloucene popisky (id N/M + navazujici radky ve stejnem sloupci).
items(page) -> list of dict(kind='cap'|'line', text, rect, size, font, flags, color, lines=[(text, origin, rect)])"""
import fitz, re
GAP = 14
def fragments(page):
    out = []
    for b in page.get_text('dict')['blocks']:
        if b['type'] != 0: continue
        for l in b['lines']:
            cur = []
            for s in l['spans']:
                if not s['text'].strip():
                    continue
                if cur and s['bbox'][0] - cur[-1]['bbox'][2] > GAP:
                    out.append(cur); cur = []
                cur.append(s)
            if cur: out.append(cur)
    frs = []
    for spans in out:
        r = fitz.Rect(spans[0]['bbox'])
        for s in spans[1:]: r |= fitz.Rect(s['bbox'])
        t = ''.join(s['text'] for s in spans).strip()
        s0 = spans[0]
        frs.append(dict(text=t, rect=r, size=s0['size'], font=s0['font'], flags=s0['flags'], color=s0['color'], origin=s0['origin']))
    return frs

ID = re.compile(r'^\d+/\d+[a-z]?(\s|$)')
def items(page):
    frs = fragments(page); used = [False] * len(frs); res = []
    order = sorted(range(len(frs)), key=lambda i: (frs[i]['rect'].y0, frs[i]['rect'].x0))
    for i in order:
        if used[i]: continue
        f = frs[i]
        if ID.match(f['text']):
            grp = [i]; used[i] = True; last = f
            while True:
                nxt = None
                for j in order:
                    if used[j]: continue
                    g = frs[j]
                    if ID.match(g['text']): continue
                    dy = g['rect'].y0 - last['rect'].y1
                    cx = (g['rect'].x0 + g['rect'].x1) / 2; lx = (last['rect'].x0 + last['rect'].x1) / 2
                    if -2 <= dy <= 6 and abs(cx - lx) < 40 and abs(g['size'] - last['size']) < 0.5:
                        nxt = j; break
                if nxt is None: break
                used[nxt] = True; grp.append(nxt); last = frs[nxt]
            r = fitz.Rect(frs[grp[0]]['rect'])
            for j in grp[1:]: r |= frs[j]['rect']
            res.append(dict(kind='cap', text=' '.join(frs[j]['text'] for j in grp), rect=r, size=f['size'], font=f['font'], flags=f['flags'], color=f['color'],
                            lines=[(frs[j]['text'], frs[j]['origin'], frs[j]['rect']) for j in grp]))
        else:
            used[i] = True
            res.append(dict(kind='line', text=f['text'], rect=f['rect'], size=f['size'], font=f['font'], flags=f['flags'], color=f['color'], lines=[(f['text'], f['origin'], f['rect'])]))
    return res

if __name__ == '__main__':
    import sys, json, collections
    d = fitz.open(sys.argv[1]); caps = collections.Counter(); lines = collections.Counter()
    for p in d:
        for it in items(p):
            (caps if it['kind'] == 'cap' else lines)[it['text']] += 1
    json.dump(dict(caps=sorted(caps), lines=sorted(lines.items(), key=lambda x: -x[1])), open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print(len(caps), 'caps', len(lines), 'lines')
