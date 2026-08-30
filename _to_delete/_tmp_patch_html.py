import io

PATH = "15h/vyrobni-vady.html"
with io.open(PATH, encoding="utf-8") as f:
    s = f.read()

bk_gallery = io.open("_tmp_bk_gallery.html", encoding="utf-8").read().strip()
z_gallery = io.open("_tmp_z_gallery.html", encoding="utf-8").read().strip()

def must_replace(s, old, new, expect=1):
    n = s.count(old)
    assert n == expect, f"expected {expect} occurrences, found {n}: {old[:80]!r}"
    return s.replace(old, new, expect)

# ---------- bludne-krouzky ----------

old_prehled_bk = '  <figure><img src="assets/img/bludne-krouzky/bludne-krouzky-prehled.jpg" alt="12 kusu se znacenymi bludnymi krouzky a skvrnami / 12 copies with wandering rings and spots marked" loading="lazy"><figcaption><span class="cs">Dvanáct kusů se zaznamenaným výskytem vady — polohy jsou na každém kuse jinde, kroužky vyznačují místo skvrny.</span><span class="en">Twelve copies with the flaw recorded — the position differs on every copy; the circles mark where the spot sits.</span></figcaption></figure>\n'
s = must_replace(s, old_prehled_bk, '')

anchor_bk_detail = '  <div class="gallery loose vada-gal">\n<figure><img src="assets/img/bludne-krouzky/bludne-krouzky-detail-skvrna.jpg"'
new_anchor_bk = bk_gallery + '\n  <div class="gallery loose vada-gal">\n<figure><img src="assets/img/bludne-krouzky/bludne-krouzky-detail-skvrna.jpg"'
s = must_replace(s, anchor_bk_detail, new_anchor_bk)

# ---------- zavoje ----------

old_prehled_z1 = '  <figure><img src="assets/img/zavoje/zavoje-prehled-1.jpg" alt="12 kusu se znacenymi zavoji / 12 copies with smears marked" loading="lazy"><figcaption><span class="cs">Dvanáct kusů se zaznamenaným závojem — kroužky vyznačují místo, žádný z nich není ostře ohraničený.</span><span class="en">Twelve copies with a recorded smear — the circles mark the spot; none of them is sharply bounded.</span></figcaption></figure>\n'
s = must_replace(s, old_prehled_z1, '')

detail_gallery_z = '''  <div class="gallery loose vada-gal">
<figure><img src="assets/img/zavoje/zavoje-detail-1.jpg" alt="detail zavoje vytekajiciho z ornamentu / detail of a smear spilling from an ornament" loading="lazy"><figcaption><span class="cs">Barva vytéká z hustého květinového ornamentu do sousední bílé plochy — okraj je měkký, ne ostrý.</span><span class="en">Ink spills from a dense floral ornament into the neighbouring white area — the edge is soft, not sharp.</span></figcaption></figure>
<figure><img src="assets/img/zavoje/zavoje-detail-2.jpg" alt="detail zavoje pod napisem CESKO / detail of a smear under the inscription CESKO" loading="lazy"><figcaption><span class="cs">Závoj stéká z nápisu na srdíčkovou ozdobu pod ním — barva plynule slábne, žádná ostrá hranice.</span><span class="en">A smear runs down from the inscription onto the little heart ornament below it — the ink fades gradually, with no sharp boundary.</span></figcaption></figure>
  </div>
'''
s = must_replace(s, detail_gallery_z, '')

old_prehled_z2 = '  <figure><img src="assets/img/zavoje/zavoje-prehled-2.jpg" alt="dva kusy se zavojem, pole 35/V / two copies with a smear, field 35/V" loading="lazy"><figcaption><span class="cs">Dva kusy se závojem pod hodnotovým oválem — na kartě vpravo je odkaz na pole 35/V.</span><span class="en">Two copies with a smear below the value oval — the card on the right references field 35/V.</span></figcaption></figure>\n'
old_prehled_z3 = '  <figure><img src="assets/img/zavoje/zavoje-prehled-3.jpg" alt="dalsi tri kusy se zavojem / three further copies with a smear" loading="lazy"><figcaption><span class="cs">Tři další doložené kusy — stejný vzorec: barva se line podél tištěné linky nebo z hustého ornamentu.</span><span class="en">Three further recorded copies — the same pattern: the ink runs along a printed line or out of a dense ornament.</span></figcaption></figure>\n'
old_both = old_prehled_z2 + old_prehled_z3
new_both = z_gallery + '\n' + detail_gallery_z
s = must_replace(s, old_both, new_both)

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(s)

print("OK, new size", len(s))
