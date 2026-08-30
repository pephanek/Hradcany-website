# -*- coding: utf-8 -*-
import io

PATH = "vyrobni-vady.html"
with io.open(PATH, encoding="utf-8") as f:
    s = f.read()

def must_replace(s, old, new, expect=1):
    n = s.count(old)
    assert n == expect, f"expected {expect} occurrences, found {n}: {old[:150]!r}"
    return s.replace(old, new, expect)

anchor = '<div class="tg-card"><div class="cell" data-pos="13" data-full="assets/img/bludne-krouzky/full/bludne-krouzky-13.jpg" data-cap="&lt;span class=\'cs\'&gt;Kus 13 — V levé části siluety Hradčan.&lt;/span&gt;&lt;span class=\'en\'&gt;Item 13 — In the left part of the Hradčany skyline.&lt;/span&gt;" data-tags=""><img src="assets/img/bludne-krouzky/thumb/bludne-krouzky-13.jpg" alt="Bludné kroužky — kus 13" loading="lazy"><span class="pos">13</span></div><p class="tg-cap"><span class="cs">V levé části siluety Hradčan.</span><span class="en">In the left part of the Hradčany skyline.</span></p></div>\n</div>'

new_card = '<div class="tg-card"><div class="cell" data-pos="14" data-full="assets/img/bludne-krouzky/full/bludne-krouzky-14.jpg" data-cap="&lt;span class=\'cs\'&gt;Kus 14 — Plná skvrna v ploše oblohy vpravo od věží Hradčan.&lt;/span&gt;&lt;span class=\'en\'&gt;Item 14 — A solid spot in the sky, to the right of the towers of Hradčany.&lt;/span&gt;" data-tags=""><img src="assets/img/bludne-krouzky/thumb/bludne-krouzky-14.jpg" alt="Bludné kroužky — kus 14" loading="lazy"><span class="pos">14</span></div><p class="tg-cap"><span class="cs">Plná skvrna v ploše oblohy vpravo od věží Hradčan.</span><span class="en">A solid spot in the sky, to the right of the towers of Hradčany.</span></p></div>\n'

new = anchor.replace('</p></div>\n</div>', '</p></div>\n' + new_card + '</div>')
s = must_replace(s, anchor, new)

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(s)

print("OK, new size", len(s))
