# -*- coding: utf-8 -*-
import io

PATH = "15h/vyrobni-vady.html"
with io.open(PATH, encoding="utf-8") as f:
    s = f.read()

def must_replace(s, old, new, expect=1):
    n = s.count(old)
    assert n == expect, f"expected {expect} occurrences, found {n}: {old[:150]!r}"
    return s.replace(old, new, expect)

# 1) insert new card after item 23
anchor = 'the perforated gutter between them — further evidence that the creasing was already there in the sheet.</span></p></div>\n  </div>'
new_card = '<div class="tg-card"><div class="cell" data-pos="24" data-full="assets/img/zvrasneni/full/zvrasneni-24.jpg" data-cap="&lt;span class=\'cs\'&gt;Kus 24 — Svislá vráska při levém okraji, na kusu s přetiskem SO 1920 (pole 92/I).&lt;/span&gt;&lt;span class=\'en\'&gt;Item 24 — A vertical crease along the left edge, on a copy with the SO 1920 overprint (field 92/I).&lt;/span&gt;" data-tags=""><img src="assets/img/zvrasneni/thumb/zvrasneni-24.jpg" alt="Zvrásnění papíru — kus 24" loading="lazy"><span class="pos">24</span></div><p class="tg-cap"><span class="cs">Svislá vráska při levém okraji, na kusu s přetiskem SO 1920 (pole 92/I).</span><span class="en">A vertical crease along the left edge, on a copy with the SO 1920 overprint (field 92/I).</span></p></div>\n'
new = anchor.replace('\n  </div>', '\n' + new_card + '  </div>')
s = must_replace(s, anchor, new)

# 2) bump the intro "23 kusech" / "23 items" count in the section note
s = must_replace(s,
  '<span class="cs">Pětadvacet známek na dvaceti třech kusech — dvacet jedna jednotlivých, jeden nezoubkovaný vodorovný pár (kus 1) a jeden svislý pár (kus 23). Kliknutím se ukázka zvětší.</span><span class="en">Twenty-five stamps on twenty-three items — twenty-one singles, one imperforate horizontal pair (item 1) and one vertical pair (item 23). Click a specimen to enlarge it.</span>',
  '<span class="cs">Šestadvacet známek na dvaceti čtyřech kusech — dvacet dva jednotlivých, jeden nezoubkovaný vodorovný pár (kus 1) a jeden svislý pár (kus 23). Kliknutím se ukázka zvětší.</span><span class="en">Twenty-six stamps on twenty-four items — twenty-two singles, one imperforate horizontal pair (item 1) and one vertical pair (item 23). Click a specimen to enlarge it.</span>')

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(s)

print("OK, new size", len(s))
