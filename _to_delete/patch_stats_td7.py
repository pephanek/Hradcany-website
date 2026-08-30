# -*- coding: utf-8 -*-
import io, re

PATH = "statistiky.html"
with io.open(PATH, encoding="utf-8") as f:
    s = f.read()

def rep(s, old, new, expect=1):
    n = s.count(old)
    assert n == expect, f"expected {expect}, got {n}: {old[:120]!r}"
    return s.replace(old, new, expect)

# 1. Intro paragraph
s = rep(s, "<strong>21 334 určených známek</strong>, z toho <strong>6 478 s čitelně datovaným razítkem</strong>",
            "<strong>21 340 určených známek</strong>, z toho <strong>6 479 s čitelně datovaným razítkem</strong>")
s = rep(s, "<strong>21,334 attributed stamps</strong>, of which <strong>6,478 carry a legibly dated cancellation</strong>",
            "<strong>21,340 attributed stamps</strong>, of which <strong>6,479 carry a legibly dated cancellation</strong>")

# 2/3. KPI cards
s = rep(s, '<span class="num">21&nbsp;334</span>', '<span class="num">21&nbsp;340</span>')
s = rep(s, '<span class="num">6&nbsp;478</span>', '<span class="num">6&nbsp;479</span>')

# 4. Main matrix: nezoubkovana row TD7 + Celkem
s = rep(s, "<td class='num'>16</td><td class='num'>34</td><td class='num'><strong>4&nbsp;526</strong></td>",
            "<td class='num'>16</td><td class='num'>37</td><td class='num'><strong>4&nbsp;529</strong></td>")

# 5. Main matrix: A row TD7 + Celkem
s = rep(s, "<td class='num'>501</td><td class='num'>17</td><td class='num'><strong>3&nbsp;429</strong></td>",
            "<td class='num'>501</td><td class='num'>20</td><td class='num'><strong>3&nbsp;432</strong></td>")

# 6. Soucet skupin row: TD7 + Celkem
s = rep(s, "<td class='num'><strong>9&nbsp;823</strong></td><td class='num'><strong>51</strong></td><td class='num'><strong>21&nbsp;334</strong></td><td class='num'>100&nbsp;%</td>",
            "<td class='num'><strong>9&nbsp;823</strong></td><td class='num'><strong>57</strong></td><td class='num'><strong>21&nbsp;340</strong></td><td class='num'>100&nbsp;%</td>")

# 7a. earliest-usage table: fix stale nezoubk 1-2 (341->342, bugfix missed during 52-II edit)
s = rep(s, "<td class='num'>341</td><td>24.&nbsp;6.&nbsp;1919</td>",
            "<td class='num'>342</td><td>24.&nbsp;6.&nbsp;1919</td>")

# 7b. earliest-usage table: nezoubk 7 (22->23)
s = rep(s, "<td class='num'>22</td><td>17.&nbsp;7.&nbsp;1919</td>",
            "<td class='num'>23</td><td>17.&nbsp;7.&nbsp;1919</td>")

# 7c. earliest-usage table Celkem (6476 -> 6478)
s = rep(s, "<td class='num'><strong>6476</strong></td>",
            "<td class='num'><strong>6478</strong></td>")

# 8. JS U object: IMPERF 7 series index3 (SEP1919) 3->4; total_series index3 186->187
s = rep(s, '"IMPERF 7": [0, 3, 4, 3, 2, 7, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}',
            '"IMPERF 7": [0, 3, 4, 4, 2, 7, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}')
s = rep(s, '"total_series": [3, 97, 159, 186, 191, 185, 174, 116, 181, 411, 1123, 1257, 621, 529, 239, 174, 135, 87, 92, 79, 66, 127, 246]',
            '"total_series": [3, 97, 159, 187, 191, 185, 174, 116, 181, 411, 1123, 1257, 621, 529, 239, 174, 135, 87, 92, 79, 66, 127, 246]')

# 9. MATRIX object
s = rep(s, '"IMPERF": [4476, 0, 0, 16, 34]', '"IMPERF": [4476, 0, 0, 16, 37]')
s = rep(s, '"A": [2179, 410, 322, 501, 17]', '"A": [2179, 410, 322, 501, 20]')

# 10. Josef comparison labels (5x, one per language)
s = rep(s, "j:'Josef (21 334 ks)'", "j:'Josef (21 340 ks)'")
s = rep(s, "j:'Josef (21,334 pcs)'", "j:'Josef (21 340 pcs)'".replace("21 340","21,340"))
s = rep(s, "j:'Josef (21 334 ex.)'", "j:'Josef (21 340 ex.)'")
s = rep(s, "j:'Josef (21 334 St.)'", "j:'Josef (21 340 St.)'")
s = rep(s, "j:'Josef (21 334 ej.)'", "j:'Josef (21 340 ej.)'")

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(s)

print("OK, new size", len(s))
