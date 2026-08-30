# -*- coding: utf-8 -*-
import io

PATH = "15h/vyrobni-vady.html"
with io.open(PATH, encoding="utf-8") as f:
    s = f.read()

def must_replace(s, old, new, expect=1):
    n = s.count(old)
    assert n == expect, f"expected {expect} occurrences, found {n}: {old[:150]!r}"
    return s.replace(old, new, expect)

anchor = 'Item 4 — The clearest item of the group. The straight boundary crosses the whole stamp and continues into the side margins; below it the outlines are doubled. The detail above is taken from this copy.</span></p></div>\n  </div>'

new_card = '<div class="tg-card"><div class="cell" data-pos="05" data-full="assets/img/zdvojeny/full/zdvojeny-05.jpg" data-cap="&lt;span class=\'cs\'&gt;Kus 5 — Kus s čitelným razítkem 1. VI. 1920. Hranice probíhá těsně pod obloukem, ve výši horních věží Hradčan.&lt;/span&gt;&lt;span class=\'en\'&gt;Item 5 — A copy with a legible cancel of 1 June 1920. The boundary runs just below the arch, at the level of the upper towers of Hradčany.&lt;/span&gt;" data-tags=""><img src="assets/img/zdvojeny/thumb/zdvojeny-05.jpg" alt="Částečně zdvojený tisk — kus 5" loading="lazy"><span class="pos">5</span></div><p class="tg-cap"><span class="cs">Kus s čitelným razítkem 1. VI. 1920. Hranice probíhá těsně pod obloukem, ve výši horních věží Hradčan.</span><span class="en">A copy with a legible cancel of 1 June 1920. The boundary runs just below the arch, at the level of the upper towers of Hradčany.</span></p></div>\n'

new = anchor.replace('\n  </div>', '\n' + new_card + '  </div>')
s = must_replace(s, anchor, new)

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(s)

print("OK, new size", len(s))
