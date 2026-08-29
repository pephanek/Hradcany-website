# -*- coding: utf-8 -*-
"""
Generator jazykovych mutaci webu Sbiram Hradcany.

Zdroj (master) = dvojjazycne HTML v korenu projektu (cestina + angl. ve
znackach <span class="cs">/<span class="en">). Preklady do dalsich jazyku
jsou v i18n/catalog.json.

Spusteni:   python build-jazyky.py
Vysledek:   slozky en/ fr/ de/ es/ s kompletni kopii webu v danem jazyce.
            Korenove soubory zustavaji ceske a needituje je.

Obrazky, CSS a JS se nekopiruji - jazykove stranky na ne odkazuji o uroven
vys (../), takze existuji na disku jen jednou.
"""
import os,re,sys,json,shutil,hashlib

ROOT=os.path.dirname(os.path.abspath(__file__))
LANGS=['en','fr','de','es']
ALL=['cs']+LANGS
LABEL={'cs':'CZ','en':'EN','fr':'FR','de':'DE','es':'ES'}
SKIP=set(LANGS)|{'_backups','i18n','.git'}
ASSET_DIRS={'assets','css','js','img','images','downloads','fonts'}

def key(s): return hashlib.sha1(s.strip().encode('utf-8')).hexdigest()[:10]

# ---------------------------------------------------------------- soubory
def html_files():
    out=[]
    for dp,dn,fn in os.walk(ROOT):
        dn[:]=[d for d in dn if d not in SKIP and not d.startswith('.')]
        rel=os.path.relpath(dp,ROOT)
        for f in sorted(fn):
            if f.endswith('.html'):
                p=os.path.normpath(os.path.join(rel,f)).replace('\\','/')
                if not is_asset(p): out.append(p)
    return sorted(out)

def is_asset(url):
    parts=[p for p in url.split('/') if p not in ('.','')]
    i=0
    while i<len(parts) and parts[i]=='..': i+=1
    rest=parts[i:]
    if not rest: return False
    return rest[0] in ASSET_DIRS or (len(rest)>1 and rest[1] in ASSET_DIRS)

# ------------------------------------------------- parove bloky se zanorenim
def _close(s,i,tag):
    depth=1; pat=re.compile(r'</?%s\b'%tag)
    while True:
        m=pat.search(s,i)
        if not m: raise ValueError('nevyvazeny <%s>'%tag)
        if m.group(0).startswith('</'):
            depth-=1
            if depth==0: return m.start()
        else: depth+=1
        i=m.end()

def find_pairs(s,tag='span'):
    op=re.compile(r'<%s class="cs">'%tag); out=[]; pos=0
    while True:
        m=op.search(s,pos)
        if not m: break
        try: c1=_close(s,m.end(),tag)
        except ValueError: pos=m.end(); continue
        m2=re.compile(r'\s*<%s class="en">'%tag).match(s,c1+len(tag)+3)
        if not m2: pos=m.end(); continue
        try: c2=_close(s,m2.end(),tag)
        except ValueError: pos=m.end(); continue
        end=c2+len(tag)+3
        out.append((m.start(),end,s[m.end():c1],s[m2.end():c2]))
        pos=end
    return out

def collapse(raw,lang,tag='span'):
    idx=0 if lang=='cs' else 1
    while True:
        ps=find_pairs(raw,tag)
        if not ps: return raw
        buf=[]; last=0
        for st,en,a,b in ps:
            buf.append(raw[last:st]); buf.append(a if idx==0 else b); last=en
        buf.append(raw[last:]); raw=''.join(buf)

# ---------------------------------------------------------------- preklad
FORM=re.compile(r'^(ZP\s*\d+(\s*/+\s*(TD\s*)?[IVX]+)?|\d+\s*/+\s*[IVX]+|TD\s*[IVX]+)$')
def formula(cs,lang):
    """Oznaceni poli a desek: v cizich jazycich se drzi ceska zkratka ZP/TD,
    jen anglictina je rozepisuje. Ciste ciselne popisky se nepreklada."""
    t=cs.strip()
    if not re.search(r'[A-Za-zÀ-ž]',re.sub(r'<[^>]+>|&[a-zA-Z#0-9]+;','',t)):
        return cs
    if not FORM.match(t): return None
    W={'en':('field','plate'),'fr':('position','planche'),
       'de':('Feld','Platte'),'es':('posición','plancha')}
    if lang not in W: return cs          # cestina drzi zkratky ZP/TD
    zp,td=W[lang]
    t=re.sub(r'\bZP\s*(\d+)',zp+r' \1',cs)
    return re.sub(r'\bTD\s*([IVX]+)',td+r' \1',t)

class Cat:
    def __init__(self):
        self.d=json.load(open(os.path.join(ROOT,'i18n','catalog.json'),encoding='utf-8'))
        self.miss=[]
    def get(self,cs,lang,where=''):
        e=self.d.get(key(cs))
        if e and e.get(lang): return e[lang]
        f=formula(cs,lang)
        if f is not None: return f
        self.miss.append((where,cs))
        return cs

def swap_pairs(s,lang,cat,where):
    for tag in ('div','span'):
        while True:
            ps=find_pairs(s,tag)
            if not ps: break
            buf=[]; last=0
            for st,en,a,b in ps:
                buf.append(s[last:st])
                buf.append(cat.get(collapse(a,'cs',tag),lang,where))
                last=en
            buf.append(s[last:]); s=''.join(buf)
    return s

# ------------------------------------------------------------------- cesty
def fix_paths(s,page,lang):
    """Prepocita relativni cesty na soubory, ktere zustavaji v korenu
    (obrazky, css, js). Stranky odkazuji uvnitr jazykove slozky, takze
    se nemeni."""
    outdir=os.path.dirname(os.path.join(lang,page)) or '.'
    srcdir=os.path.dirname(page) or '.'
    def rep(m):
        attr,url=m.group(1),m.group(2)
        if re.match(r'^(https?:|mailto:|tel:|data:|#|//)',url): return m.group(0)
        if not is_asset(url): return m.group(0)
        head,sep,tail=url.partition('#')
        head,q,query=head.partition('?')
        target=os.path.normpath(os.path.join(srcdir,head)).replace('\\','/')
        new=os.path.relpath(target,outdir).replace('\\','/')
        return '%s="%s%s%s%s%s"'%(attr,new,q,query,sep,tail)
    return re.sub(r'\b(href|src|data-full|data-thumb|poster|action)="([^"]*)"',rep,s)

# --------------------------------------------------------------- prepinac
def switcher(page,lang):
    up='../'*(page.count('/')+(1 if lang!='cs' else 0))
    out=['<div class="lang-switch">']
    for L in ALL:
        if L==lang: out.append('<span class="active">%s</span>'%LABEL[L])
        else:
            tgt=up+page if L=='cs' else up+L+'/'+page
            out.append('<a href="%s" hreflang="%s">%s</a>'%(tgt,L,LABEL[L]))
    out.append('</div>')
    return ''.join(out)

def alternates(page,lang):
    """<link rel="alternate" hreflang> pro vyhledavace."""
    up='../'*(page.count('/')+(1 if lang!='cs' else 0))
    out=[]
    for L in ALL:
        tgt=up+page if L=='cs' else up+L+'/'+page
        out.append('<link rel="alternate" hreflang="%s" href="%s">'%(L,tgt))
    out.append('<link rel="alternate" hreflang="x-default" href="%s">'%(up+page))
    return '\n'.join(out)

SW=re.compile(r'<div class="lang-switch">.*?</div>',re.S)

# ------------------------------------------------------- specialni fixupy
def komparator_js(s,lang,cat):
    """Komparator sklada dvojjazycne popisky v JavaScriptu."""
    lbl={'Is':'Is — otevřená spirála','IIp':'IIp — dlouhá příčka','IIap':'IIap — podtyp příčky',
         'crack':'prasklá deska','spot':'skvrna / závoj','frame':'poškozený rám'}
    tr={k:cat.get(v,lang,'komparator LBL') for k,v in lbl.items()}
    block='var LBL={'+','.join("%s:%s"%(k,json.dumps(v,ensure_ascii=False)) for k,v in tr.items())+'};'
    s2=re.sub(r'var LBL=\{.*?\};',lambda m:block,s,count=1,flags=re.S)
    assert s2!=s,'komparator: LBL nenalezeno'
    subs=[
      ("'<span class=\"badge '+CLS[k]+'\"><span class=\"cs\">'+LBL[k][0]+'</span><span class=\"en\">'+LBL[k][1]+'</span></span>'",
       "'<span class=\"badge '+CLS[k]+'\">'+LBL[k]+'</span>'"),
      ("<span class=\"cs\">TD '+ROM[td]+'</span><span class=\"en\">Plate '+ROM[td]+'</span>",
       cat.get('Deska',lang,'komparator TD')+" '+ROM[td]+'"),
      ("<span class=\"cs\">ZP '+pos+'</span><span class=\"en\">field '+pos+'</span>",
       cat.get('Známkové pole',lang,'komparator ZP')+" '+pos+'"),
    ]
    for a,b in subs:
        assert a in s2,'komparator: nenalezeno %r'%a[:50]
        s2=s2.replace(a,b)
    return s2

def mapa_js(s,page,lang):
    a="var l = document.body.classList.contains('lang-en') ? 'en' : 'cs';"
    assert a in s,'mapa: prepinac jazyka nenalezen'
    s=s.replace(a,"var l = %s;"%json.dumps(lang))
    # cesta k mape je v JS retezci, obecny prepocet cest ji nevidi
    outdir=os.path.dirname(os.path.join(lang,page)) or '.'
    srcdir=os.path.dirname(page) or '.'
    target=os.path.normpath(os.path.join(srcdir,'assets/cancel_map.html')).replace('\\','/')
    rel=os.path.relpath(target,outdir).replace('\\','/')
    b="var src = 'assets/cancel_map.html?lang=' + l;"
    assert b in s,'mapa: cesta k cancel_map nenalezena'
    return s.replace(b,"var src = '%s?lang=' + l;"%rel)

# ------------------------------------------------------------------ stranka
META=[('<title data-cs="','"',' data-en="'),]
def build_page(page,lang,cat):
    src=open(os.path.join(ROOT,page),encoding='utf-8').read()
    where='%s [%s]'%(page,lang)
    s=src
    if page=='15h/komparator.html': s=komparator_js(s,lang,cat)
    if page=='15h/mapa.html':       s=mapa_js(s,page,lang)
    s=swap_pairs(s,lang,cat,where)
    # titulek
    def t(m):
        return '<title>%s</title>'%cat.get(m.group(1),lang,where)
    s=re.sub(r'<title data-cs="([^"]*)" data-en="[^"]*">.*?</title>',t,s,flags=re.S)
    # meta
    for name in ('og:title','og:description'):
        s=re.sub(r'(<meta property="%s" content=")([^"]*)(")'%re.escape(name),
                 lambda m:m.group(1)+cat.get(m.group(2),lang,where)+m.group(3),s)
    s=re.sub(r'(<meta name="description" content=")([^"]*)(")',
             lambda m:m.group(1)+cat.get(m.group(2),lang,where)+m.group(3),s)
    # data-tags: escapovane jazykove spany v atributu
    def dattr(m):
        import html as _h
        name=m.group(1); inner=_h.unescape(m.group(2))
        sq="class='cs'" in inner
        if sq: inner=inner.replace("class='cs'",'class="cs"').replace("class='en'",'class="en"')
        inner=swap_pairs(inner,lang,cat,where)
        return '%s="%s"'%(name,_h.escape(inner,quote=True))
    s=re.sub(r'\b(data-tags|data-cap)="([^"]*)"',dattr,s)
    # parove <text> uvnitr SVG (schemata se dvema jazyky)
    def tpair(m):
        cls=m.group(1).strip(); txt=m.group(2)
        return '<text class="%s">%s</text>'%(cls,cat.get(txt,lang,where))
    s=re.sub(r'<text class="cs([^"]*)">(.*?)</text>\s*<text class="en[^"]*">.*?</text>',
             tpair,s,flags=re.S)
    # texty uvnitr SVG (schemata)
    def opt(t):
        e=cat.d.get(key(t))
        return e[lang] if e and e.get(lang) else t
    def svg(m):
        blk=m.group(0)
        blk=re.sub(r'(<text\b[^>]*>)([^<]+)(</text>)',
                   lambda t:t.group(1)+opt(t.group(2))+t.group(3),blk)
        blk=re.sub(r'(<title\b[^>]*>)([^<]+)(</title>)',
                   lambda t:t.group(1)+opt(t.group(2))+t.group(3),blk)
        return blk
    s=re.sub(r'<svg\b.*?</svg>',svg,s,flags=re.S)
    # popisky obrazku (jen ty, ktere jsou v katalogu)
    def figcap(m):
        inner=re.sub(r'(^|>)([^<>]+)(?=<|$)',lambda t:t.group(1)+opt(t.group(2)),m.group(2))
        return m.group(1)+inner+m.group(3)
    s=re.sub(r'(<figcaption[^>]*>)(.*?)(</figcaption>)',figcap,s,flags=re.S)
    s=re.sub(r'alt="([^"]*)"',lambda m:'alt="%s"'%opt(m.group(1)),s)
    # znacka webu
    s=re.sub(r'(<span class="title">)([^<]*)(</span>)',
             lambda m:m.group(1)+cat.get(m.group(2),lang,where)+m.group(3),s)
    s=s.replace('alt="Sbírám Hradčany"','alt="%s"'%cat.get('Sbírám Hradčany',lang,where))
    # alternativni jazykove verze pro vyhledavace (nejprve zahodit ty z masteru)
    s=re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?','',s)
    s=re.sub(r'(</head>)',lambda m:alternates(page,lang)+'\n'+m.group(1),s,count=1)
    # jazyk dokumentu
    s=s.replace('<html lang="cs">','<html lang="%s">'%lang,1)
    s=re.sub(r'(<body[^>]*class=")lang-cs',r'\1lang-'+lang,s,count=1)
    # prepinac + cesty
    s=SW.sub(lambda m:switcher(page,lang),s,count=1)
    s=fix_paths(s,page,lang)
    return s

def build_master_switcher(cat):
    """Do korenovych (ceskych) stranek doplni odkazy na jazykove mutace."""
    n=0
    for page in html_files():
        p=os.path.join(ROOT,page); s=open(p,encoding='utf-8').read()
        new=SW.sub(lambda m:switcher(page,'cs'),s,count=1)
        new=re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?','',new)
        new=re.sub(r'(</head>)',lambda m:alternates(page,'cs')+'\n'+m.group(1),new,count=1)
        if new!=s: open(p,'w',encoding='utf-8').write(new); n+=1
    return n

def main():
    cat=Cat(); pages=html_files()
    # Soubory se prepisuji na miste. Mazani celych slozek se neosvedcilo —
    # pripojena slozka casto zapoved dava jen cteni a zapis, ne mazani.
    for L in LANGS:
        for page in pages:
            out=os.path.join(ROOT,L,page)
            os.makedirs(os.path.dirname(out),exist_ok=True)
            open(out,'w',encoding='utf-8').write(build_page(page,L,cat))
        print('%s: %d stranek'%(L,len(pages)))
        zbyle=[]
        for dp,dn,fn in os.walk(os.path.join(ROOT,L)):
            for f in fn:
                if not f.endswith('.html'): continue
                rel=os.path.relpath(os.path.join(dp,f),os.path.join(ROOT,L)).replace('\\','/')
                if rel not in pages: zbyle.append(rel)
        if zbyle:
            print('   pozor: %s/ obsahuje %d stranek, ktere uz v masteru nejsou: %s'
                  %(L,len(zbyle),', '.join(sorted(zbyle)[:5])))
    n=build_master_switcher(cat)
    print('prepinac doplnen do %d ceskych stranek'%n)
    if cat.miss:
        seen=set(); uniq=[]
        for w,c in cat.miss:
            if c not in seen: seen.add(c); uniq.append((w,c))
        print('\nCHYBEJICI PREKLADY: %d vyskytu / %d unikatnich'%(len(cat.miss),len(uniq)))
        with open(os.path.join(ROOT,'i18n','chybejici.txt'),'w',encoding='utf-8') as fh:
            for w,c in uniq: fh.write('%s\t%s\n'%(w,c))
        print('  seznam: i18n/chybejici.txt')
        for w,c in uniq[:15]: print('  %-40s %s'%(w[:40],c))
    else:
        print('\nvsechny retezce prelozeny')

if __name__=='__main__': main()
