#!/usr/bin/env python3
"""Stahne obrazky clanku z hradcany-stamps.com (Webnode CDN) do 15h/assets/img/."""
import os, time, urllib.request, pathlib
here = pathlib.Path(__file__).resolve().parent
dst = here.parent / "assets" / "img"
dst.mkdir(parents=True, exist_ok=True)
for i, line in enumerate(open(here/"manifest.txt", encoding="utf-8"), 1):
    if "\t" not in line: continue
    url, name = line.rstrip("\n").split("\t")
    out = dst / name
    if out.exists():
        print(f"[{i}] skip  {name}"); continue
    try:
        urllib.request.urlretrieve(url, out)
        print(f"[{i}] OK    {name}")
    except Exception as e:
        print(f"[{i}] CHYBA {url}: {e}")
    time.sleep(0.15)
print("Hotovo:", dst)
