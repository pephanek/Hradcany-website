# -*- coding: utf-8 -*-
import io

PATH = "15h/statistiky.html"
with io.open(PATH, encoding="utf-8") as f:
    s = f.read()

def must_replace(s, old, new, expect=1):
    n = s.count(old)
    assert n == expect, f"expected {expect} occurrences, found {n}: {old[:150]!r}"
    return s.replace(old, new, expect)

# 1) intro paragraph
s = must_replace(s, '<strong>21 331 určených známek</strong>, z toho <strong>6 476 s čitelně datovaným razítkem</strong>',
                     '<strong>21 332 určených známek</strong>, z toho <strong>6 477 s čitelně datovaným razítkem</strong>')
s = must_replace(s, '<strong>21,331 attributed stamps</strong>, of which <strong>6,476 carry a legibly dated cancellation</strong>',
                     '<strong>21,332 attributed stamps</strong>, of which <strong>6,477 carry a legibly dated cancellation</strong>')

# 2) KPI cards
s = must_replace(s, '<span class="num">21&nbsp;331</span>', '<span class="num">21&nbsp;332</span>')
s = must_replace(s, '<span class="num">6&nbsp;474</span>', '<span class="num">6&nbsp;477</span>')

# 3) matrix table row "A"
old_row_a = "<tr><td><strong><span class=\"cs\">A — 13¾:13½ hřeb.</span><span class=\"en\">A — 13¾:13½ comb</span></strong></td><td class='num'>2&nbsp;178</td><td class='num'>410</td><td class='num'>322</td><td class='num'>501</td><td class='num'>17</td><td class='num'><strong>3&nbsp;428</strong></td><td class='num'><span class=\"cs\">16,1&nbsp;%</span><span class=\"en\">16.1&nbsp;%</span></td></tr>"
new_row_a = "<tr><td><strong><span class=\"cs\">A — 13¾:13½ hřeb.</span><span class=\"en\">A — 13¾:13½ comb</span></strong></td><td class='num'>2&nbsp;179</td><td class='num'>410</td><td class='num'>322</td><td class='num'>501</td><td class='num'>17</td><td class='num'><strong>3&nbsp;429</strong></td><td class='num'><span class=\"cs\">16,1&nbsp;%</span><span class=\"en\">16.1&nbsp;%</span></td></tr>"
s = must_replace(s, old_row_a, new_row_a)

# 4) group sum row
old_row_sum = "<tr><td><strong><span class=\"cs\">Součet skupin</span><span class=\"en\">Group sum</span></strong></td><td class='num'><strong>9&nbsp;990</strong></td><td class='num'><strong>667</strong></td><td class='num'><strong>800</strong></td><td class='num'><strong>9&nbsp;823</strong></td><td class='num'><strong>51</strong></td><td class='num'><strong>21&nbsp;331</strong></td><td class='num'>100&nbsp;%</td></tr>"
new_row_sum = "<tr><td><strong><span class=\"cs\">Součet skupin</span><span class=\"en\">Group sum</span></strong></td><td class='num'><strong>9&nbsp;991</strong></td><td class='num'><strong>667</strong></td><td class='num'><strong>800</strong></td><td class='num'><strong>9&nbsp;823</strong></td><td class='num'><strong>51</strong></td><td class='num'><strong>21&nbsp;332</strong></td><td class='num'>100&nbsp;%</td></tr>"
s = must_replace(s, old_row_sum, new_row_sum)

# 5) MATRIX
s = must_replace(s, '"A": [2178, 410, 322, 501, 17]', '"A": [2179, 410, 322, 501, 17]')

# 6) U.groups "A 1-2"
s = must_replace(s,
  '"A 1-2": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]',
  '"A 1-2": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]')

# 7) total_series
s = must_replace(s,
  '"total_series": [3, 97, 159, 186, 191, 185, 174, 116, 180, 411, 1123, 1257, 620, 529, 239, 174, 135, 87, 92, 79, 66, 127, 246]',
  '"total_series": [3, 97, 159, 186, 191, 185, 174, 116, 180, 411, 1123, 1257, 621, 529, 239, 174, 135, 87, 92, 79, 66, 127, 246]')

# 8) comparison labels
s = must_replace(s, "Josef (21 331 ks)", "Josef (21 332 ks)")
s = must_replace(s, "Josef (21,331 pcs)", "Josef (21,332 pcs)")
s = must_replace(s, "Josef (21 331 ex.)", "Josef (21 332 ex.)")
s = must_replace(s, "Josef (21 331 St.)", "Josef (21 332 St.)")
s = must_replace(s, "Josef (21 331 ej.)", "Josef (21 332 ej.)")

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(s)

print("OK, new size", len(s))
