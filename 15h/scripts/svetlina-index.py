# -*- coding: utf-8 -*-
"""
Index světliny pro jedno známkové pole.

Měří, kolik barvy chybí ve sledovaném ohnisku, a normalizuje to týmž prvkem
kresby jinde na TÉŽE známce. Díky tomu nevadí rozdílná sytost tisku ani jiný
sken: index 1,0 = v ohnisku je barvy stejně jako v kontrolní ploše, nižší
hodnota = barva v ohnisku chybí.

Použití:
    python svetlina-index.py <složka se skeny> [--ohnisko roh-pd] [--rada rada.jpg]

Složka = jedna pozice z training knihovny, např. training_15h/TD5_pos020.
Skeny musí být jednotlivé známky, kresba orientovaná nastojato.

Ohniska jsou definovaná zlomky výšky/šířky kresby, ne pixely, takže jsou
nezávislá na rozlišení skenu. Nové ohnisko se přidá do tabulky OHNISKA.
"""
import sys, os, glob, argparse
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 1010          # společná mřížka, na kterou se kresba natáhne

# ohnisko a kontrolní plochy jako (x0,x1,y0,y1) ve zlomcích kresby
OHNISKA = {
    # vnější roh rámu vpravo dole; kontrola = táž rámová linka jinde
    'roh-pd': dict(
        ohnisko=(0.962, 1.000, 0.955, 1.000),
        kontrola=[(0.45, 0.90, 0.955, 1.000),      # spodní linka vlevo od rohu
                  (0.962, 1.000, 0.45, 0.90)],     # pravá linka nad rohem
    ),
    'roh-ld': dict(
        ohnisko=(0.000, 0.038, 0.955, 1.000),
        kontrola=[(0.10, 0.55, 0.955, 1.000), (0.000, 0.038, 0.45, 0.90)],
    ),
}


def kresba(cesta, prah=60):
    """Ořízne sken na kresbu (bez perforace a okraje) a natáhne na mřížku."""
    im = Image.open(cesta).convert('RGB')
    a = np.asarray(im).astype(int)
    m = (a[:, :, 0] - (a[:, :, 1] + a[:, :, 2]) / 2) > prah
    xs = np.where(m.sum(0) > m.shape[0] * 0.35)[0]
    ys = np.where(m.sum(1) > m.shape[1] * 0.35)[0]
    if len(xs) < 10 or len(ys) < 10:
        raise ValueError('kresba nenalezena')
    im = im.crop((xs[0], ys[0], xs[-1], ys[-1])).resize((W, H), Image.LANCZOS)
    a = np.asarray(im).astype(float)
    return im, np.clip(a[:, :, 0] - (a[:, :, 1] + a[:, :, 2]) / 2, 0, None)


def _plocha(k, r):
    x0, x1, y0, y1 = r
    return k[int(H * y0):int(H * y1), int(W * x0):int(W * x1)]


def index(k, ohnisko):
    o = OHNISKA[ohnisko]
    barva = _plocha(k, o['ohnisko']).mean()
    ctrl = np.mean([_plocha(k, r).mean() for r in o['kontrola']])
    return barva / max(ctrl, 1e-6)


def vyrez(im, ohnisko, sirka=260):
    """Těsný výřez okolo ohniska pro vývojovou řadu."""
    x0, x1, y0, y1 = OHNISKA[ohnisko]['ohnisko']
    cx0 = max(0, int(W * (x0 - 0.075))); cy0 = max(0, int(H * (y0 - 0.075)))
    cx1 = min(W, int(W * (x1 + 0.035))); cy1 = min(H, int(H * (y1 + 0.045)))
    c = im.crop((cx0, cy0, cx1, cy1))
    return c.resize((sirka, int(sirka * c.height / c.width)), Image.LANCZOS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('slozka')
    ap.add_argument('--ohnisko', default='roh-pd', choices=sorted(OHNISKA))
    ap.add_argument('--rada', help='soubor pro obrázek vývojové řady')
    ap.add_argument('--sloupcu', type=int, default=6)
    ap.add_argument('--sirka', type=int, default=260, help='šířka jednoho výřezu v px')
    ap.add_argument('--mezera', type=int, default=18, help='mezera mezi výřezy v px')
    a = ap.parse_args()

    radky = []
    for f in sorted(glob.glob(os.path.join(a.slozka, '*.png')) +
                    glob.glob(os.path.join(a.slozka, '*.jpg'))):
        try:
            im, k = kresba(f)
        except Exception as e:
            print('  přeskočeno %s (%s)' % (os.path.basename(f), e), file=sys.stderr)
            continue
        radky.append((index(k, a.ohnisko), os.path.basename(f), im))
    if not radky:
        sys.exit('ve složce nejsou použitelné skeny')
    radky.sort(key=lambda r: r[0])

    print('%-34s %s' % ('soubor', 'index'))
    for v, n, _ in radky:
        print('%-34s %.2f  %s' % (n, v, '#' * int(v * 30)))
    h = [v for v, _, _ in radky]
    print('\n%d kusů, index %.2f – %.2f, medián %.2f' %
          (len(h), min(h), max(h), float(np.median(h))))

    if a.rada:
        ts = [(v, vyrez(im, a.ohnisko, sirka=a.sirka)) for v, _, im in radky]
        tw = ts[0][1].width
        th = max(t.height for _, t in ts)
        pis = int(tw / 12)
        font = None
        for f in ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
                  'C:/Windows/Fonts/arial.ttf'):
            if os.path.exists(f):
                font = ImageFont.truetype(f, pis); break
        ram = 1                       # tenká linka kolem výřezu
        popis = int(pis * 1.6)        # pruh na index pod výřezem
        mez = a.mezera                # mezera mezi buňkami
        bw = tw + 2 * ram             # buňka i s rámečkem
        bh = th + 2 * ram + popis
        cols = a.sloupcu; rows = (len(ts) + cols - 1) // cols
        s = Image.new('RGB', (cols * bw + (cols + 1) * mez,
                              rows * bh + (rows + 1) * mez), (255, 255, 255))
        d = ImageDraw.Draw(s)
        for i, (v, t) in enumerate(ts):
            x = mez + (i % cols) * (bw + mez)
            y = mez + (i // cols) * (bh + mez)
            d.rectangle([x, y, x + bw - 1, y + th + 2 * ram - 1], outline=(214, 205, 198))
            s.paste(t, (x + ram, y + ram))
            d.text((x + ram, y + th + 2 * ram + int(pis * 0.25)),
                   ('%.2f' % v).replace('.', ','), fill=(90, 80, 73), font=font)
        s.save(a.rada, quality=92)
        print('vývojová řada: %s' % a.rada)


if __name__ == '__main__':
    main()
