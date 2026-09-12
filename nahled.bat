@echo off
chcp 1250 >nul
setlocal
title Hradcany - lokalni nahled webu

cd /d "C:\Users\pepam\OneDrive\Stamps\Claude-Hradcany-website"

set PORT=8765
set "URL=http://localhost:%PORT%/15h/assets/cancel_map.html"

echo.
echo ======================================================
echo  Lokalni nahled webu Hradcany
echo.
echo  Mapa potrebuje, aby stranka bezela pres http://,
echo  ne pres file:// - OpenStreetMap bez hlavicky Referer
echo  vraci dlazdice "Access blocked".
echo ======================================================
echo.

set "SRV="
py -3 -c "import sys" >nul 2>&1 && set "SRV=py -3 -m http.server %PORT%"
if not defined SRV python -c "import sys" >nul 2>&1 && set "SRV=python -m http.server %PORT%"
if not defined SRV (
  where npx >nul 2>&1 && set "SRV=npx --yes http-server -p %PORT% -c-1"
)

if not defined SRV (
  echo !!! Nenasel jsem ani Python, ani Node/npx.
  echo     Nejjednodussi je nainstalovat Python z Microsoft Store
  echo     ^(hledej "Python 3"^) a pak tenhle soubor spustit znovu.
  echo.
  echo     Do te doby si mapu proklikni na zverejnenem webu -
  echo     tam dlazdice funguji, protoze se stranka servíruje pres https.
  goto konec
)

echo Spoustim server:  %SRV%
echo Adresa:           %URL%
echo.
echo Okno NECHEJ OTEVRENE - zavrenim se server vypne.
echo Ukonceni: Ctrl+C nebo zavrit toto okno.
echo.

start "" "%URL%"
%SRV%

:konec
echo.
pause
