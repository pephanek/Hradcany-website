# -*- coding: utf-8 -*-
import io

PATH = "assets/cancel_map.html"
with io.open(PATH, encoding="utf-8") as f:
    s = f.read()

def rep(s, old, new, expect=1):
    n = s.count(old)
    assert n == expect, f"expected {expect}, got {n}: {old[:150]!r}"
    return s.replace(old, new, expect)

# 1. Add TD7 group to existing "Praha 1" location (92-VII, 13-VII, strip 23/33-VII — all no/illegible date)
old = '"name": "Praha 1", "lat": 50.087, "lon": 14.4207, "g": {"G":'
new = ('"name": "Praha 1", "lat": 50.087, "lon": 14.4207, "g": {'
       '"TD7": {"n": 4, "rows": [["", "spec_92_VII_01", ""], ["", "spec_13_VII_01", ""], '
       '["", "spec_23_VII_01", ""], ["", "spec_33_VII_01", ""]]}, "G":')
s = rep(s, old, new)

# 2. Add new "Karlova Studánka" location (71-VII, 5.9.1919) before "Karlovy Vary"
old2 = '{"name": "Karlovy Vary", "lat": 50.2306, "lon": 12.8702,'
new2 = ('{"name": "Karlova Studánka", "lat": 50.0731, "lon": 17.3062, "g": {"TD7": {"n": 1, '
        '"rows": [["5.9.1919", "spec_71_VII_01", ""]]}}}, '
        '{"name": "Karlovy Vary", "lat": 50.2306, "lon": 12.8702,')
s = rep(s, old2, new2)

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(s)

print("OK, new size", len(s))
