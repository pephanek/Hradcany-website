# -*- coding: utf-8 -*-
import io

def must_replace(s, old, new, expect=1):
    n = s.count(old)
    assert n == expect, f"expected {expect} occurrences, found {n}: {old[:150]!r}"
    return s.replace(old, new, expect)

# --- posta.html ---
PATH1 = "15h/posta.html"
with io.open(PATH1, encoding="utf-8") as f:
    s = f.read()
s = must_replace(s, "<li>Karlovy Vary</li><li>Klatovy</li>", "<li>Karlovy Vary (2×)</li><li>Klatovy</li>")
with io.open(PATH1, "w", encoding="utf-8") as f:
    f.write(s)
print("posta.html OK", len(s))

# --- statistiky.html ---
PATH2 = "15h/statistiky.html"
with io.open(PATH2, encoding="utf-8") as f:
    s = f.read()

s = must_replace(s, '<strong>21 332 určených známek</strong>, z toho <strong>6 477 s čitelně datovaným razítkem</strong>',
                     '<strong>21 333 určených známek</strong>, z toho <strong>6 477 s čitelně datovaným razítkem</strong>')
s = must_replace(s, '<strong>21,332 attributed stamps</strong>, of which <strong>6,477 carry a legibly dated cancellation</strong>',
                     '<strong>21,333 attributed stamps</strong>, of which <strong>6,477 carry a legibly dated cancellation</strong>')
s = must_replace(s, '<span class="num">21&nbsp;332</span>', '<span class="num">21&nbsp;333</span>')

old_row_b = "<tr><td><strong><span class=\"cs\">B — 11¾ hřeb.</span><span class=\"en\">B — 11¾ comb</span></strong></td><td class='num'>144</td><td class='num'>257</td><td class='num'>478</td><td class='num'>4&nbsp;597</td><td class='num'>–</td><td class='num'><strong>5&nbsp;476</strong></td><td class='num'><span class=\"cs\">25,7&nbsp;%</span><span class=\"en\">25.7&nbsp;%</span></td></tr>"
new_row_b = "<tr><td><strong><span class=\"cs\">B — 11¾ hřeb.</span><span class=\"en\">B — 11¾ comb</span></strong></td><td class='num'>145</td><td class='num'>257</td><td class='num'>478</td><td class='num'>4&nbsp;597</td><td class='num'>–</td><td class='num'><strong>5&nbsp;477</strong></td><td class='num'><span class=\"cs\">25,7&nbsp;%</span><span class=\"en\">25.7&nbsp;%</span></td></tr>"
s = must_replace(s, old_row_b, new_row_b)

old_row_sum = "<tr><td><strong><span class=\"cs\">Součet skupin</span><span class=\"en\">Group sum</span></strong></td><td class='num'><strong>9&nbsp;991</strong></td><td class='num'><strong>667</strong></td><td class='num'><strong>800</strong></td><td class='num'><strong>9&nbsp;823</strong></td><td class='num'><strong>51</strong></td><td class='num'><strong>21&nbsp;332</strong></td><td class='num'>100&nbsp;%</td></tr>"
new_row_sum = "<tr><td><strong><span class=\"cs\">Součet skupin</span><span class=\"en\">Group sum</span></strong></td><td class='num'><strong>9&nbsp;992</strong></td><td class='num'><strong>667</strong></td><td class='num'><strong>800</strong></td><td class='num'><strong>9&nbsp;823</strong></td><td class='num'><strong>51</strong></td><td class='num'><strong>21&nbsp;333</strong></td><td class='num'>100&nbsp;%</td></tr>"
s = must_replace(s, old_row_sum, new_row_sum)

s = must_replace(s, '"B": [144, 257, 478, 4597, 0]', '"B": [145, 257, 478, 4597, 0]')

s = must_replace(s, "Josef (21 332 ks)", "Josef (21 333 ks)")
s = must_replace(s, "Josef (21,332 pcs)", "Josef (21,333 pcs)")
s = must_replace(s, "Josef (21 332 ex.)", "Josef (21 333 ex.)")
s = must_replace(s, "Josef (21 332 St.)", "Josef (21 333 St.)")
s = must_replace(s, "Josef (21 332 ej.)", "Josef (21 333 ej.)")

with io.open(PATH2, "w", encoding="utf-8") as f:
    f.write(s)
print("statistiky.html OK", len(s))
