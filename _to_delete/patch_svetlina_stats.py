# -*- coding: utf-8 -*-
import io

PATH = "statistiky.html"
with io.open(PATH, encoding="utf-8") as f:
    s = f.read()

def rep(s, old, new, expect=1):
    n = s.count(old)
    assert n == expect, f"expected {expect}, got {n}: {old[:150]!r}"
    return s.replace(old, new, expect)

# Intro paragraph
s = rep(s, "<strong>21 340 určených známek</strong>, z toho <strong>6 479 s čitelně datovaným razítkem</strong>",
            "<strong>21 341 určených známek</strong>, z toho <strong>6 480 s čitelně datovaným razítkem</strong>")
s = rep(s, "<strong>21,340 attributed stamps</strong>, of which <strong>6,479 carry a legibly dated cancellation</strong>",
            "<strong>21,341 attributed stamps</strong>, of which <strong>6,480 carry a legibly dated cancellation</strong>")

# KPI cards
s = rep(s, '<span class="num">21&nbsp;340</span>', '<span class="num">21&nbsp;341</span>')
s = rep(s, '<span class="num">6&nbsp;479</span>', '<span class="num">6&nbsp;480</span>')

# Main matrix: nezoubkovana row TD1-2 col + Celkem
s = rep(s, "<td class='num'>4&nbsp;476</td><td class='num'>–</td><td class='num'>–</td><td class='num'>16</td><td class='num'>37</td><td class='num'><strong>4&nbsp;529</strong></td>",
            "<td class='num'>4&nbsp;477</td><td class='num'>–</td><td class='num'>–</td><td class='num'>16</td><td class='num'>37</td><td class='num'><strong>4&nbsp;530</strong></td>")

# Soucet skupin row: TD1-2 col + Celkem
s = rep(s, "<td class='num'><strong>9&nbsp;993</strong></td><td class='num'><strong>667</strong></td><td class='num'><strong>800</strong></td><td class='num'><strong>9&nbsp;823</strong></td><td class='num'><strong>57</strong></td><td class='num'><strong>21&nbsp;340</strong></td><td class='num'>100&nbsp;%</td>",
            "<td class='num'><strong>9&nbsp;994</strong></td><td class='num'><strong>667</strong></td><td class='num'><strong>800</strong></td><td class='num'><strong>9&nbsp;823</strong></td><td class='num'><strong>57</strong></td><td class='num'><strong>21&nbsp;341</strong></td><td class='num'>100&nbsp;%</td>")

# earliest-usage table: nezoubk 1-2 (342 -> 343)
s = rep(s, "<td class='num'>342</td><td>24.&nbsp;6.&nbsp;1919</td>",
            "<td class='num'>343</td><td>24.&nbsp;6.&nbsp;1919</td>")

# earliest-usage table Celkem (6478 -> 6479)
s = rep(s, "<td class='num'><strong>6478</strong></td>",
            "<td class='num'><strong>6479</strong></td>")

# JS U object
s = rep(s, '"IMPERF 1-2": [2, 25, 27, 27, 36, 31, 42, 14, 25, 31, 26, 31, 7, 1, 1, 4, 9, 2, 0, 0, 0, 0, 1]',
            '"IMPERF 1-2": [2, 25, 27, 27, 36, 32, 42, 14, 25, 31, 26, 31, 7, 1, 1, 4, 9, 2, 0, 0, 0, 0, 1]')
s = rep(s, '"total_series": [3, 97, 159, 187, 191, 185, 174, 116, 181, 411, 1123, 1257, 621, 529, 239, 174, 135, 87, 92, 79, 66, 127, 246]',
            '"total_series": [3, 97, 159, 187, 191, 186, 174, 116, 181, 411, 1123, 1257, 621, 529, 239, 174, 135, 87, 92, 79, 66, 127, 246]')

# MATRIX object
s = rep(s, '"IMPERF": [4476, 0, 0, 16, 37]', '"IMPERF": [4477, 0, 0, 16, 37]')

# Josef labels
s = rep(s, "j:'Josef (21 340 ks)'", "j:'Josef (21 341 ks)'")
s = rep(s, "j:'Josef (21,340 pcs)'", "j:'Josef (21,341 pcs)'")
s = rep(s, "j:'Josef (21 340 ex.)'", "j:'Josef (21 341 ex.)'")
s = rep(s, "j:'Josef (21 340 St.)'", "j:'Josef (21 341 St.)'")
s = rep(s, "j:'Josef (21 340 ej.)'", "j:'Josef (21 341 ej.)'")

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(s)

print("OK, new size", len(s))
