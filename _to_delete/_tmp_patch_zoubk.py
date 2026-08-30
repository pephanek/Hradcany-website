# -*- coding: utf-8 -*-
import io

PATH = "15h/zoubkovani.html"
with io.open(PATH, encoding="utf-8") as f:
    s = f.read()

def must_replace(s, old, new, expect=1):
    n = s.count(old)
    assert n == expect, f"expected {expect} occurrences, found {n}: {old[:150]!r}"
    return s.replace(old, new, expect)

# 1) intro count for the earliest-usages section
s = must_replace(s, 'Z 6 474 čitelně datovaných razítek.', 'Z 6 477 čitelně datovaných razítek.')
s = must_replace(s, 'From 6,474 legibly dated cancellations.', 'From 6,477 legibly dated cancellations.')

# 2) insert new row "A (TD 1-2)" 1.6.1920, between A(TD3) 4.5.1920 and A(TD4) 8.6.1920
anchor = '<tr><td><span class="cs">A (TD 3)</span><span class="en">A (plate 3)</span></td><td>4. 5. 1920</td></tr><tr><td><span class="cs">A (TD 4)</span><span class="en">A (plate 4)</span></td><td>8. 6. 1920</td></tr>'
new_mid = '<tr><td><span class="cs">A (TD 3)</span><span class="en">A (plate 3)</span></td><td>4. 5. 1920</td></tr><tr><td><span class="cs">A (TD 1–2)</span><span class="en">A (plates 1–2)</span></td><td>1. 6. 1920</td></tr><tr><td><span class="cs">A (TD 4)</span><span class="en">A (plate 4)</span></td><td>8. 6. 1920</td></tr>'
s = must_replace(s, anchor, new_mid)

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(s)

print("OK, new size", len(s))
