#!/usr/bin/env bash
# Stáhne všechny obrázky do assets/images/. Spusťte: bash scripts/download_images.sh
set -u
BASE="https://900cfd8a63.clvaw-cdnwnd.com/9c4605a2643780500ef1c2ac87facbb9"
DIR="$(cd "$(dirname "$0")/.." && pwd)/assets/images"
mkdir -p "$DIR"
ok=0; fail=0
while IFS='|' read -r path local; do
  [ -z "${path:-}" ] && continue
  if curl -fsSL --max-time 30 "$BASE/$path" -o "$DIR/$local"; then
    ok=$((ok+1)); echo "OK   $local"
  else
    fail=$((fail+1)); echo "FAIL $local" >&2
  fi
done < "$(dirname "$0")/manifest.txt"
echo "Hotovo: $ok stazeno, $fail chyb."
