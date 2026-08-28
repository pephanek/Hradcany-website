#!/usr/bin/env python3
"""Stáhne všechny obrázky webu Sbírám Hradčany do assets/images/.
Spusťte z kořenové složky projektu:  python3 scripts/download_images.py
Vyžaduje připojení k internetu (CDN clvaw-cdnwnd.com)."""
import os, sys, urllib.request

BASE = "https://900cfd8a63.clvaw-cdnwnd.com/9c4605a2643780500ef1c2ac87facbb9/"
HERE = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(os.path.dirname(HERE), "assets", "images")
os.makedirs(DEST, exist_ok=True)

ok = fail = 0
with open(os.path.join(HERE, "manifest.txt"), encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line or "|" not in line:
            continue
        path, local = line.split("|", 1)
        out = os.path.join(DEST, local)
        try:
            req = urllib.request.Request(BASE + path, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as r, open(out, "wb") as w:
                w.write(r.read())
            ok += 1
            print("OK  ", local)
        except Exception as e:
            fail += 1
            print("FAIL", local, "-", e, file=sys.stderr)
print(f"\nHotovo: {ok} staženo, {fail} chyb.")
