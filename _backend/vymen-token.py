# -*- coding: utf-8 -*-
"""
Výměna publikačního tokenu.

Přečte nový token z .deploy/github_token.txt, ověří ho proti GitHubu
a teprve když projde, zapíše ho do adresy vzdáleného repozitáře.
Starý token tím přestane být potřeba a jde ho na GitHubu zneplatnit.

Spuštění:  python _backend/vymen-token.py
"""
import os, re, subprocess, json, urllib.request, sys

KOREN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOUBOR = os.path.join(KOREN, '.deploy', 'github_token.txt')
REPO = 'pephanek/Hradcany-website'


def git(*a):
    return subprocess.run(['git', '-C', KOREN] + list(a),
                          capture_output=True, text=True).stdout.strip()


def api(cesta, token):
    req = urllib.request.Request(
        'https://api.github.com' + cesta,
        headers={'Authorization': 'Bearer ' + token,
                 'Accept': 'application/vnd.github+json',
                 'User-Agent': 'hradcany-vymena-tokenu'})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r), dict(r.headers)


def main():
    if not os.path.exists(SOUBOR):
        sys.exit('Nenalezen soubor %s' % SOUBOR)
    token = open(SOUBOR, encoding='utf-8').read().strip()
    if not token:
        sys.exit('Soubor s tokenem je prázdný.')
    if not token.startswith('github_pat_'):
        print('Varování: token nezačíná na github_pat_ — není to fine-grained token?')

    stary = git('config', '--local', '--get', 'remote.origin.url')
    if token in stary:
        print('Tento token už v adrese repozitáře je — není co měnit.')
        return

    # 1) ověřit, že token vůbec funguje a vidí správný repozitář
    try:
        data, hlavicky = api('/repos/' + REPO, token)
    except Exception as e:
        sys.exit('Token GitHub nepřijal (%s). Adresa repozitáře zůstala beze změny.' % e)
    if data.get('full_name') != REPO:
        sys.exit('Token vidí jiný repozitář: %s' % data.get('full_name'))
    if not data.get('permissions', {}).get('push'):
        sys.exit('Token nemá právo zápisu (Contents: Read and write).')

    platnost = hlavicky.get('github-authentication-token-expiration', 'neuvedena')
    print('Token ověřen: %s, právo zápisu ano, platnost do %s' % (REPO, platnost))

    # 2) teprve teď přepsat adresu repozitáře
    uzivatel = re.match(r'https://([^:]+):', stary)
    uzivatel = uzivatel.group(1) if uzivatel else 'pephanek'
    nova = 'https://%s:%s@github.com/%s.git' % (uzivatel, token, REPO)
    subprocess.run(['git', '-C', KOREN, 'remote', 'set-url', 'origin', nova], check=True)

    # 3) zkusit skutečné spojení
    r = subprocess.run(['git', '-C', KOREN, 'ls-remote', 'origin', 'HEAD'],
                       capture_output=True, text=True)
    if r.returncode != 0:
        subprocess.run(['git', '-C', KOREN, 'remote', 'set-url', 'origin', stary])
        sys.exit('Spojení s novým tokenem selhalo, vrátil jsem původní adresu.\n' + r.stderr[:300])

    print('Hotovo. Nový token je v adrese repozitáře a spojení funguje.')
    print('Teď můžete na GitHubu zneplatnit ten starý.')


if __name__ == '__main__':
    main()
