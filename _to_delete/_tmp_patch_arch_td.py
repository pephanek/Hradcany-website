import io

PATH = "15h/zkusebni-tisky.html"
with io.open(PATH, encoding="utf-8") as f:
    s = f.read()

def must_replace(s, old, new, expect=1):
    n = s.count(old)
    assert n == expect, f"expected {expect} occurrences, found {n}: {old[:120]!r}"
    return s.replace(old, new, expect)

# 1) extend the intro paragraph with the plate identification
old_p = 'Rozmezí let 1918–1920 odpovídá období, kdy se na arších tohoto vydání tiskla takzvaná kontrolní čísla.</span><span class="en">Besides the individual proofs, a full pane (10×10 fields) of POFIS 7 (the 15h) has also survived, printed entirely in black and imperforate — the same purpose as the other proofs, but at the level of a whole pane rather than a single field. The span 1918–1920 corresponds to the period in which this issue\'s sheets carried what are called control numbers.</span></p>'
new_p = 'Rozmezí let 1918–1920 odpovídá období, kdy se na arších tohoto vydání tiskla takzvaná kontrolní čísla. Podle stavebního znaku na poli 11 — barevná spojnice mezi hodnotovým oválem a spodním rámečkem, kterou má na tomto poli každá deska kromě III — jde o tiskovou desku VI.</span><span class="en">Besides the individual proofs, a full pane (10×10 fields) of POFIS 7 (the 15h) has also survived, printed entirely in black and imperforate — the same purpose as the other proofs, but at the level of a whole pane rather than a single field. The span 1918–1920 corresponds to the period in which this issue\'s sheets carried what are called control numbers. A structural marker at field 11 — a coloured line joining the value oval to the bottom frame, present on every plate except III — identifies this as printing plate VI.</span></p>'
s = must_replace(s, old_p, new_p)

# 2) add a "Tiskova deska" row to the facts table, right after "Katalog"
old_row = '<tr><th><span class="cs">Katalog</span><span class="en">Catalogue</span></th><td><span class="cs">POFIS 7 (15h)</span><span class="en">POFIS 7 (the 15h)</span></td></tr>\n    <tr><th><span class="cs">Období</span><span class="en">Period</span></th><td>1918–1920</td></tr>'
new_row = '<tr><th><span class="cs">Katalog</span><span class="en">Catalogue</span></th><td><span class="cs">POFIS 7 (15h)</span><span class="en">POFIS 7 (the 15h)</span></td></tr>\n    <tr><th><span class="cs">Tisková deska</span><span class="en">Printing plate</span></th><td><span class="cs">VI</span><span class="en">VI</span></td></tr>\n    <tr><th><span class="cs">Období</span><span class="en">Period</span></th><td>1918–1920</td></tr>'
s = must_replace(s, old_row, new_row)

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(s)

print("OK, new size", len(s))
