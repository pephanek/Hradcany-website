import io

PATH = "15h/vyrobni-vady.html"
with io.open(PATH, encoding="utf-8") as f:
    s = f.read()

block = io.open("_tmp_bile_skvrny_block.html", encoding="utf-8").read().strip()

def must_replace(s, old, new, expect=1):
    n = s.count(old)
    assert n == expect, f"expected {expect} occurrences, found {n}: {old[:100]!r}"
    return s.replace(old, new, expect)

anchor = '    <div class="soon-card"><strong><span class="cs">Slitý tisk</span><span class="en">Blurred print</span></strong><span class="note"><span class="cs">Připravuje se.</span><span class="en">In preparation.</span></span></div>\n    \n  </div>\n</div>\n\n<div class="section" id="deska">'
new = '    <div class="soon-card"><strong><span class="cs">Slitý tisk</span><span class="en">Blurred print</span></strong><span class="note"><span class="cs">Připravuje se.</span><span class="en">In preparation.</span></span></div>\n    \n  </div>\n</div>\n\n' + block + '\n\n<div class="section" id="deska">'
s = must_replace(s, anchor, new)

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(s)

print("OK, new size", len(s))
