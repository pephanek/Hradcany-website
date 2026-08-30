# -*- coding: utf-8 -*-
import io

def must_replace(s, old, new, expect=1):
    n = s.count(old)
    assert n == expect, f"expected {expect} occurrences, found {n}: {old[:150]!r}"
    return s.replace(old, new, expect)

PATH2 = "15h/statistiky.html"
with io.open(PATH2, encoding="utf-8") as f:
    s = f.read()

s = must_replace(s, '<strong>21 333 určených známek</strong>, z toho <strong>6 477 s čitelně datovaným razítkem</strong>',
                     '<strong>21 334 určených známek</strong>, z toho <strong>6 478 s čitelně datovaným razítkem</strong>')
s = must_replace(s, '<strong>21,333 attributed stamps</strong>, of which <strong>6,477 carry a legibly dated cancellation</strong>',
                     '<strong>21,334 attributed stamps</strong>, of which <strong>6,478 carry a legibly dated cancellation</strong>')
s = must_replace(s, '<span class="num">21&nbsp;333</span>', '<span class="num">21&nbsp;334</span>')
s = must_replace(s, '<span class="num">6&nbsp;477</span>', '<span class="num">6&nbsp;478</span>')

old_row_imperf = "<tr><td><strong><span class=\"cs\">nezoubkovaná</span><span class=\"en\">imperforate</span></strong></td><td class='num'>4&nbsp;475</td><td class='num'>–</td><td class='num'>–</td><td class='num'>16</td><td class='num'>34</td><td class='num'><strong>4&nbsp;525</strong></td><td class='num'><span class=\"cs\">21,2&nbsp;%</span><span class=\"en\">21.2&nbsp;%</span></td></tr>"
new_row_imperf = "<tr><td><strong><span class=\"cs\">nezoubkovaná</span><span class=\"en\">imperforate</span></strong></td><td class='num'>4&nbsp;476</td><td class='num'>–</td><td class='num'>–</td><td class='num'>16</td><td class='num'>34</td><td class='num'><strong>4&nbsp;526</strong></td><td class='num'><span class=\"cs\">21,2&nbsp;%</span><span class=\"en\">21.2&nbsp;%</span></td></tr>"
s = must_replace(s, old_row_imperf, new_row_imperf)

old_row_sum = "<tr><td><strong><span class=\"cs\">Součet skupin</span><span class=\"en\">Group sum</span></strong></td><td class='num'><strong>9&nbsp;992</strong></td><td class='num'><strong>667</strong></td><td class='num'><strong>800</strong></td><td class='num'><strong>9&nbsp;823</strong></td><td class='num'><strong>51</strong></td><td class='num'><strong>21&nbsp;333</strong></td><td class='num'>100&nbsp;%</td></tr>"
new_row_sum = "<tr><td><strong><span class=\"cs\">Součet skupin</span><span class=\"en\">Group sum</span></strong></td><td class='num'><strong>9&nbsp;993</strong></td><td class='num'><strong>667</strong></td><td class='num'><strong>800</strong></td><td class='num'><strong>9&nbsp;823</strong></td><td class='num'><strong>51</strong></td><td class='num'><strong>21&nbsp;334</strong></td><td class='num'>100&nbsp;%</td></tr>"
s = must_replace(s, old_row_sum, new_row_sum)

s = must_replace(s, '"IMPERF": [4475, 0, 0, 16, 34]', '"IMPERF": [4476, 0, 0, 16, 34]')

s = must_replace(s,
  '"IMPERF 1-2": [2, 25, 27, 27, 36, 31, 42, 14, 24, 31, 26, 31, 7, 1, 1, 4, 9, 2, 0, 0, 0, 0, 1]',
  '"IMPERF 1-2": [2, 25, 27, 27, 36, 31, 42, 14, 25, 31, 26, 31, 7, 1, 1, 4, 9, 2, 0, 0, 0, 0, 1]')

s = must_replace(s,
  '"total_series": [3, 97, 159, 186, 191, 185, 174, 116, 180, 411, 1123, 1257, 621, 529, 239, 174, 135, 87, 92, 79, 66, 127, 246]',
  '"total_series": [3, 97, 159, 186, 191, 185, 174, 116, 181, 411, 1123, 1257, 621, 529, 239, 174, 135, 87, 92, 79, 66, 127, 246]')

s = must_replace(s, "Josef (21 333 ks)", "Josef (21 334 ks)")
s = must_replace(s, "Josef (21,333 pcs)", "Josef (21,334 pcs)")
s = must_replace(s, "Josef (21 333 ex.)", "Josef (21 334 ex.)")
s = must_replace(s, "Josef (21 333 St.)", "Josef (21 334 St.)")
s = must_replace(s, "Josef (21 333 ej.)", "Josef (21 334 ej.)")

with io.open(PATH2, "w", encoding="utf-8") as f:
    f.write(s)
print("statistiky.html OK", len(s))

# zoubkovani.html dated total 6477 -> 6478
PATH3 = "15h/zoubkovani.html"
with io.open(PATH3, encoding="utf-8") as f:
    s3 = f.read()
s3 = must_replace(s3, 'Z 6 477 čitelně datovaných razítek.', 'Z 6 478 čitelně datovaných razítek.')
s3 = must_replace(s3, 'From 6,477 legibly dated cancellations.', 'From 6,478 legibly dated cancellations.')
with io.open(PATH3, "w", encoding="utf-8") as f:
    f.write(s3)
print("zoubkovani.html OK", len(s3))
