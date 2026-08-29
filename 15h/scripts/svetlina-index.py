# -*- coding: utf-8 -*-
"""
Index světliny pro jedno známkové pole.

Měří, kolik barvy chybí ve sledovaném ohnisku, a normalizuje to týmž prvkem
kresby jinde na TÉŽE známce. Díky tomu nevadí rozdílná sytost tisku ani jiný
sken: index 1,0 = v ohnisku je barvy stejně jako v kontrolní ploše, nižší
hodnota = barva v ohnisku chybí.

Skeny se před měřením srovnají na společnou soustavu:
  1. narovnají se podle spodní hrany kresby (nakloněný sken jinak posune
     všechno, co se počítá od okraje),
  2. zakotví se na STŘEDNICE čtyř rámových linek, ne na obalový obdélník
     barvy — obalový obdélník ujede vždy, když linka v rohu chybí nebo je
     otisk na kraji slabý.
Souřadnice 0 a 1 tedy leží na střednicích rámu; vnější roh rámu je v (1, 1).

Použití:
    python svetlina-index.py <složka se skeny> [--ohnisko roh-pd] [--rada rada.jpg]

Složka = jedna pozice z training knihovny, např. training_15h/TD5_pos020.
Skeny musí být jednotlivé známky, kresba orientovaná nastojato.
"""
import sys, os, glob, argparse
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 1010          # společná mřížka mezi střednicemi rámu

# Ohniska. Roh = průsečík dvou rámových linek; okno kolem něj i kontrolní pásy
# se odvozují od NAMĚŘENÉ tloušťky linky, ne od pevného zlomku kresby — okno
# široké proti lince by měřilo hlavně papír a index by nesl jen nepřesnost
# zarovnání. `kotvy` říkají, které dvě linky se protínají, `pas` rozsah
# kontrolního pásu podél každé z nich (ve zlomcích strany kresby).
OHNISKA = {
    'roh-pd': dict(kotvy=('prava', 'dolni'), pas=(0.45, 0.90),
                   vyrez=(0.80, 1.075, 0.75, 1.09)),
    'roh-ld': dict(kotvy=('leva', 'dolni'), pas=(0.10, 0.55),
                   vyrez=(-0.075, 0.20, 0.75, 1.09)),
}


def _barva(im):
    a = np.asarray(im.convert('RGB')).astype(float)
    return np.clip(a[:, :, 0] - (a[:, :, 1] + a[:, :, 2]) / 2, 0, None)


def _hruby_ram(k, prah=60):
    m = k > prah
    xs = np.where(m.sum(0) > m.shape[0] * 0.35)[0]
    ys = np.where(m.sum(1) > m.shape[1] * 0.35)[0]
    if len(xs) < 10 or len(ys) < 10:
        raise ValueError('kresba nenalezena')
    return xs[0], ys[0], xs[-1], ys[-1]


def sklon(k, prah=60):
    """Náklon skenu ve stupních, měřený na spodní hraně kresby."""
    m = k > prah
    h, w = m.shape
    xs, ys = [], []
    for x in range(int(w * 0.15), int(w * 0.85), 4):
        col = np.where(m[:, x])[0]
        if len(col):
            xs.append(x); ys.append(col[-1])
    if len(xs) < 20:
        return 0.0
    xs = np.array(xs, float); ys = np.array(ys, float)
    for _ in range(3):                      # odlehlé body (razítko, vada) pryč
        a, b = np.polyfit(xs, ys, 1)
        r = ys - (a * xs + b)
        ok = np.abs(r) < max(3 * r.std(), 2.0)
        if ok.sum() < 20:
            break
        xs, ys = xs[ok], ys[ok]
    a, _ = np.polyfit(xs, ys, 1)
    return float(np.degrees(np.arctan(a)))


def _strednice(k, od, do, osa, kolmo):
    """Řádek (nebo sloupec) s nejvíc barvou v zadaném pásu = střed rámové linky."""
    a, b = kolmo
    if osa == 'y':
        pas = k[od:do, a:b].mean(axis=1)
    else:
        pas = k[a:b, od:do].mean(axis=0)
    return od + int(np.argmax(pas))


def ram(k):
    """Střednice čtyř rámových linek: (x_levá, y_horní, x_pravá, y_dolní)."""
    x0, y0, x1, y1 = _hruby_ram(k)
    w, h = x1 - x0, y1 - y0
    dx, dy = int(w * 0.10), int(h * 0.10)
    ax, bx = x0 + int(w * 0.25), x0 + int(w * 0.75)
    ay, by = y0 + int(h * 0.25), y0 + int(h * 0.75)
    return (_strednice(k, max(0, x0 - dx // 2), x0 + dx, 'x', (ay, by)),
            _strednice(k, max(0, y0 - dy // 2), y0 + dy, 'y', (ax, bx)),
            _strednice(k, x1 - dx, min(k.shape[1], x1 + dx // 2), 'x', (ay, by)),
            _strednice(k, y1 - dy, min(k.shape[0], y1 + dy // 2), 'y', (ax, bx)))


def srovnej(cesta):
    """Načte sken, narovná ho a vrátí (obrázek, mapa barvy) v soustavě rámu.

    Mřížka je o 12 % větší na každou stranu, aby se vešel i vnější okraj rámu;
    kresba mezi střednicemi leží na (0,0)-(W,H) po odečtení okraje.
    """
    im = Image.open(cesta).convert('RGB')
    uhel = sklon(_barva(im))
    if abs(uhel) > 0.05:
        im = im.rotate(uhel, resample=Image.BICUBIC, fillcolor=(255, 255, 255))
    k = _barva(im)
    lx, ty, px, dy = ram(k)
    w, h = px - lx, dy - ty
    okr = 0.12
    box = (lx - w * okr, ty - h * okr, px + w * okr, dy + h * okr)
    velikost = (int(W * (1 + 2 * okr)), int(H * (1 + 2 * okr)))
    im = im.crop([int(round(v)) for v in box]).resize(velikost, Image.LANCZOS)
    return im, _barva(im), okr


def _obdelnik(r, okr):
    """(x0,x1,y0,y1) v soustavě rámu -> pixely na mřížce s okrajem."""
    x0, x1, y0, y1 = r
    px = lambda v: int(round((v + okr) / (1 + 2 * okr) * W * (1 + 2 * okr)))
    py = lambda v: int(round((v + okr) / (1 + 2 * okr) * H * (1 + 2 * okr)))
    return px(x0), px(x1), py(y0), py(y1)


def _tloustka(pas, stred):
    """Tloušťka linky v pixelech: šířka profilu v polovině jeho výšky."""
    if pas.max() <= 0:
        return 3
    prah = pas.max() / 2.0
    i = j = int(np.clip(stred, 0, len(pas) - 1))
    while i > 0 and pas[i - 1] >= prah: i -= 1
    while j < len(pas) - 1 and pas[j + 1] >= prah: j += 1
    return max(3, j - i + 1)


def _linky(k, okr):
    """Střednice a tloušťky čtyř rámových linek na srovnané mřížce."""
    hh, ww = k.shape
    px = lambda v: (v + okr) / (1 + 2 * okr) * ww
    py = lambda v: (v + okr) / (1 + 2 * okr) * hh
    a, b = int(py(0.25)), int(py(0.75))
    c, d = int(px(0.25)), int(px(0.75))
    out = {}
    for jm, osa, stred in (('leva', 'x', px(0)), ('prava', 'x', px(1)),
                           ('horni', 'y', py(0)), ('dolni', 'y', py(1))):
        s0 = int(stred - (ww if osa == 'x' else hh) * 0.03)
        s1 = int(stred + (ww if osa == 'x' else hh) * 0.03)
        s0, s1 = max(0, s0), min(ww if osa == 'x' else hh, s1)
        pas = k[a:b, s0:s1].mean(axis=0) if osa == 'x' else k[s0:s1, c:d].mean(axis=1)
        i = int(np.argmax(pas))
        out[jm] = (s0 + i, _tloustka(pas, i))
    return out, px, py


def index(k, okr, ohnisko):
    """Barva v rohu rámu / barva v týchž linkách dál od rohu."""
    o = OHNISKA[ohnisko]
    L, px, py = _linky(k, okr)
    jm_x, jm_y = o['kotvy']
    cx, tx = L[jm_x]; cy, ty = L[jm_y]
    def pruh(x0, x1, y0, y1):
        return k[int(y0):int(y1), int(x0):int(x1)].mean()
    roh = pruh(cx - tx, cx + tx + 1, cy - ty, cy + ty + 1)
    p0, p1 = o['pas']
    vodo = pruh(px(p0), px(p1), cy - ty, cy + ty + 1)
    svis = pruh(cx - tx, cx + tx + 1, py(p0), py(p1))
    return roh / max((vodo + svis) / 2, 1e-6)


def cizi_tma(im, k, okr, ohnisko):
    """Podíl skutečně tmavých bodů v ohnisku — okraj skenu, pásek sousední
    známky apod. Taková plocha není barva ani papír a měření by zkreslila."""
    o = OHNISKA[ohnisko]
    L, px, py = _linky(k, okr)
    cx, tx = L[o['kotvy'][0]]; cy, ty = L[o['kotvy'][1]]
    a = np.asarray(im).astype(int)
    okno = a[int(cy - ty):int(cy + ty + 1), int(cx - tx):int(cx + tx + 1)]
    if okno.size == 0:
        return 1.0
    return float((okno.max(axis=2) < 70).mean())


def vyrez(im, okr, ohnisko, sirka=260):
    x0, x1, y0, y1 = _obdelnik(OHNISKA[ohnisko]['vyrez'], okr)
    c = im.crop((x0, y0, x1, y1))
    return c.resize((sirka, int(sirka * c.height / c.width)), Image.LANCZOS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('slozka')
    ap.add_argument('--ohnisko', default='roh-pd', choices=sorted(OHNISKA))
    ap.add_argument('--rada', help='soubor pro obrázek vývojové řady')
    ap.add_argument('--sloupcu', type=int, default=6)
    ap.add_argument('--sirka', type=int, default=260, help='šířka jednoho výřezu v px')
    ap.add_argument('--mezera', type=int, default=18, help='mezera mezi výřezy v px')
    ap.add_argument('--tma', type=float, default=0.03,
                    help='max. podíl cizí tmavé plochy v ohnisku, jinak se kus vynechá')
    a = ap.parse_args()

    radky = []
    for f in sorted(glob.glob(os.path.join(a.slozka, '*.png')) +
                    glob.glob(os.path.join(a.slozka, '*.jpg'))):
        try:
            im, k, okr = srovnej(f)
            t = cizi_tma(im, k, okr, a.ohnisko)
            if t > a.tma:
                print('  vynecháno %s (v ohnisku %.0f %% cizí tmavé plochy)'
                      % (os.path.basename(f), t * 100), file=sys.stderr)
                continue
            radky.append((index(k, okr, a.ohnisko), os.path.basename(f),
                          vyrez(im, okr, a.ohnisko, a.sirka)))
        except Exception as e:
            print('  přeskočeno %s (%s)' % (os.path.basename(f), e), file=sys.stderr)
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
        tw = radky[0][2].width
        th = max(r[2].height for r in radky)
        pis = max(9, int(tw / 12))
        font = None
        for f in ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
                  'C:/Windows/Fonts/arial.ttf'):
            if os.path.exists(f):
                font = ImageFont.truetype(f, pis); break
        ram_, popis, mez = 1, int(pis * 1.6), a.mezera
        bw, bh = tw + 2 * ram_, th + 2 * ram_ + popis
        cols = a.sloupcu; rows = (len(radky) + cols - 1) // cols
        s = Image.new('RGB', (cols * bw + (cols + 1) * mez,
                              rows * bh + (rows + 1) * mez), (255, 255, 255))
        d = ImageDraw.Draw(s)
        for i, (v, _, t) in enumerate(radky):
            x = mez + (i % cols) * (bw + mez)
            y = mez + (i // cols) * (bh + mez)
            d.rectangle([x, y, x + bw - 1, y + th + 2 * ram_ - 1], outline=(214, 205, 198))
            s.paste(t, (x + ram_, y + ram_))
            d.text((x + ram_, y + th + 2 * ram_ + int(pis * 0.25)),
                   ('%.2f' % v).replace('.', ','), fill=(90, 80, 73), font=font)
        s.save(a.rada, quality=92)
        print('vývojová řada: %s' % a.rada)


if __name__ == '__main__':
    main()
