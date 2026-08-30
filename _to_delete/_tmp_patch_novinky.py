# -*- coding: utf-8 -*-
import io

PATH = "novinky.html"
with io.open(PATH, encoding="utf-8") as f:
    s = f.read()

def must_replace(s, old, new, expect=1):
    n = s.count(old)
    assert n == expect, f"expected {expect} occurrences, found {n}: {old[:150]!r}"
    return s.replace(old, new, expect)

anchor = '<ul class="news">\n'
new_li = '<li><span class="date">30.&nbsp;8.&nbsp;2026</span> <span class="cs">Nový přírůstek: kus s <strong>částečně zdvojeným tiskem</strong> (zoubkování&nbsp;A, TD&nbsp;1 nebo&nbsp;2), s datovaným razítkem <strong>1.&nbsp;VI.&nbsp;1920</strong>; poštovní úřad není čitelný — jde o vůbec první doložený datovaný kus tohoto zoubkování na deskách 1–2. Nově na stránce <a href="15h/vyrobni-vady.html#zdvojeny-tisk"><strong>Výrobní vady</strong></a> a v <a href="15h/statistiky.html"><strong>statistikách</strong></a> (6&nbsp;477 datovaných razítek).</span><span class="en">New acquisition: a piece with <strong>partially doubled printing</strong> (perforation&nbsp;A, plate&nbsp;1 or&nbsp;2), with a dated cancellation of <strong>1&nbsp;June&nbsp;1920</strong>; the post office is not legible — this is the first documented dated example of this perforation on plates&nbsp;1–2. Now featured on the <a href="15h/vyrobni-vady.html#zdvojeny-tisk"><strong>Production flaws</strong></a> page and in the <a href="15h/statistiky.html"><strong>statistics</strong></a> (6,477 dated cancellations).</span></li>\n'
new = anchor + new_li
s = must_replace(s, anchor, new)

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(s)

print("OK, new size", len(s))
