import io

PATH = "15h/zkusebni-tisky.html"
with io.open(PATH, encoding="utf-8") as f:
    s = f.read()

def must_replace(s, old, new, expect=1):
    n = s.count(old)
    assert n == expect, f"expected {expect} occurrences, found {n}: {old[:120]!r}"
    return s.replace(old, new, expect)

old = ' Podle stavebního znaku na poli 11 — barevná spojnice mezi hodnotovým oválem a spodním rámečkem, kterou má na tomto poli každá deska kromě III — jde o tiskovou desku VI.</span><span class="en">Besides the individual proofs, a full pane (10×10 fields) of POFIS 7 (the 15h) has also survived, printed entirely in black and imperforate — the same purpose as the other proofs, but at the level of a whole pane rather than a single field. The span 1918–1920 corresponds to the period in which this issue\'s sheets carried what are called control numbers. A structural marker at field 11 — a coloured line joining the value oval to the bottom frame, present on every plate except III — identifies this as printing plate VI.</span>'
new = '</span><span class="en">Besides the individual proofs, a full pane (10×10 fields) of POFIS 7 (the 15h) has also survived, printed entirely in black and imperforate — the same purpose as the other proofs, but at the level of a whole pane rather than a single field. The span 1918–1920 corresponds to the period in which this issue\'s sheets carried what are called control numbers.</span>'
s = must_replace(s, old, new)

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(s)

print("OK, new size", len(s))
