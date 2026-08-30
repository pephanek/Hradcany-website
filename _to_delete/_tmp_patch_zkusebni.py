import io

PATH = "15h/zkusebni-tisky.html"
with io.open(PATH, encoding="utf-8") as f:
    s = f.read()

block = io.open("_tmp_zt_new_sections.html", encoding="utf-8").read().strip()

def must_replace(s, old, new, expect=1):
    n = s.count(old)
    assert n == expect, f"expected {expect} occurrences, found {n}: {old[:120]!r}"
    return s.replace(old, new, expect)

anchor = '</div>\n\n<div class="section" id="proc">'
new = '</div>\n\n' + block + '\n\n<div class="section" id="proc">'
s = must_replace(s, anchor, new)

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(s)

print("OK, new size", len(s))
