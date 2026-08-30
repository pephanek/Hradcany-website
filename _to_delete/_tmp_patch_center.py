import io

PATH = "15h/vyrobni-vady.html"
with io.open(PATH, encoding="utf-8") as f:
    s = f.read()

def must_replace(s, old, new, expect=1):
    n = s.count(old)
    assert n == expect, f"expected {expect} occurrences, found {n}: {old[:100]!r}"
    return s.replace(old, new, expect)

# --- bludne-krouzky: unwrap the two detail figures from the flex gallery div ---
old_open_bk = '  <div class="gallery loose vada-gal">\n<figure><img src="assets/img/bludne-krouzky/bludne-krouzky-detail-skvrna.jpg"'
new_open_bk = '<figure><img src="assets/img/bludne-krouzky/bludne-krouzky-detail-skvrna.jpg"'
s = must_replace(s, old_open_bk, new_open_bk)

old_close_bk = 'A genuine ring inside a letter of the inscription POŠTA — only the rim of the speck printed, the centre stayed light.</span></figcaption></figure>\n  </div>\n</div>\n\n<div class="vada" id="zavoje">'
new_close_bk = 'A genuine ring inside a letter of the inscription POŠTA — only the rim of the speck printed, the centre stayed light.</span></figcaption></figure>\n</div>\n\n<div class="vada" id="zavoje">'
s = must_replace(s, old_close_bk, new_close_bk)

# --- zavoje: same treatment ---
old_open_z = '  <div class="gallery loose vada-gal">\n<figure><img src="assets/img/zavoje/zavoje-detail-1.jpg"'
new_open_z = '<figure><img src="assets/img/zavoje/zavoje-detail-1.jpg"'
s = must_replace(s, old_open_z, new_open_z)

old_close_z = 'A smear runs down from the inscription onto the little heart ornament below it — the ink fades gradually, with no sharp boundary.</span></figcaption></figure>\n  </div>\n</div>\n\n  <div class="soon">'
new_close_z = 'A smear runs down from the inscription onto the little heart ornament below it — the ink fades gradually, with no sharp boundary.</span></figcaption></figure>\n</div>\n\n  <div class="soon">'
s = must_replace(s, old_close_z, new_close_z)

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(s)

print("OK, new size", len(s))
