# Builds guides/*.html and sitemap.xml from the article bodies in this folder: python3 tools/guides_src/build.py
import json, re, html, os
SITE="https://marketplus-news.github.io"
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT=os.path.join(ROOT,"guides")
SRC=os.path.dirname(os.path.abspath(__file__))
DATE="2026-10-25"; DATE_H="October 25, 2026"
os.makedirs(OUT, exist_ok=True)
P=lambda s:"https://www.patreon.com/DmitryZhuk/posts/"+s
G=[
 dict(slug="how-to-plan-christmas-budget-2026", src="christmas.html",
  title="How to Plan a Christmas Budget in 2026: Step by Step",
  h1="How to Plan a Christmas Budget in 2026 (Step by Step)",
  desc="Plan a Christmas budget for 2026 step by step: set a total you can afford, per-person gift limits, hidden costs, an example table and tracking tips.",
  card="Set a total, gift limits per person, cover hidden costs and track spending, with an example $800 budget.",
  img="christmas-budget-2026.webp",
  cta=("Track your Christmas budget in a ready-made sheet",
       "The Christmas Budget &amp; Gift Tracker 2026 for Excel and Google Sheets has a gift list with budget vs actual, holiday spending by category and a dashboard with charts. Just need a gift list? The free version tracks budget, actual price and bought / wrapped status for each gift.",
       [("Christmas Budget &amp; Gift Tracker 2026 ($4)",P("christmas-budget-173352149"),1),("Free Christmas Gift List",P("free-christmas-173352318"),0)])),
 dict(slug="savings-challenges-2027", src="savings.html",
  title="16 Savings Challenges for 2027 (With Real Totals)",
  h1="16 Savings Challenges for 2027: How Each Works and the Real Totals",
  desc="16 savings challenges for 2027 explained: 52-week ($1,378), 100 envelope ($5,050), 26-week, penny challenge and more, with exact yearly totals.",
  card="52-week, 100 envelope, 26-week, penny and 12 more challenges, with exact totals and a summary table.",
  img="savings-challenge-2027.webp",
  cta=("Print your challenge and colour it in",
       "The 2027 Savings Challenge Pack includes 16 printable savings challenges (52-week, 100-envelope, $10,000 and more) in A6, A4 and US Letter sizes, plus an Excel tracker with automatic totals.",
       [("2027 Savings Challenge Pack ($4)",P("2027-savings-16-173352268"),1)])),
 dict(slug="how-to-set-goals-2027", src="goals.html",
  title="How to Set Goals for 2027 You Actually Keep",
  h1="How to Set Goals for 2027 That You Actually Keep",
  desc="A simple goal system for 2027: a yearly vision by life area, 3 to 5 goals, quarterly OKRs, weekly actions and a monthly review checklist.",
  card="Yearly vision, 3 to 5 goals, quarterly OKRs with a worked example, weekly actions and a monthly review.",
  img="goal-planner-2027-pro.webp",
  cta=("Run this system in Notion",
       "The 2027 Goal &amp; Life Planner Pro for Notion connects goals to quarterly OKRs, projects and money goals so progress updates automatically, with habit stats and weekly, monthly and year-end reviews. Want to start free? The Lite version has a year vision, goals with progress bars, a weekly habit tracker and a monthly review.",
       [("2027 Goal &amp; Life Planner Pro ($9)",P("2027-goal-life-173353268"),1),("Free Lite version for Notion","https://viridian-question-22d.notion.site/2027-Goal-Life-Planner-Lite-40418c614944812e8d68c49b3f754ff6",0)])),
 dict(slug="how-to-keep-a-trading-journal", src="trading.html",
  title="How to Keep a Trading Journal: What to Log and Why",
  h1="How to Keep a Trading Journal: What to Log and Why",
  desc="What to record in a trading journal and why: trade fields, R-multiple, win rate, expectancy and drawdown, explained simply. Educational only.",
  card="The fields to log for every trade, how to calculate R, and the review metrics that matter. Educational only.",
  img="trading-journal.webp",
  cta=("Use a ready-made journal template",
       "Trading Journal Pro for Google Sheets and Excel calculates win rate, R-multiple and P&amp;L automatically, with a dashboard and mistake analysis. The free Lite version is a lightweight way to start logging today. Templates are record-keeping tools, not trading advice.",
       [("Trading Journal Pro",P("trading-journal-173290193"),1),("Free Trading Journal Lite",P("free-trading-173292664"),0)])),
 dict(slug="simple-monthly-budget-for-beginners", src="budget.html",
  title="Simple Monthly Budget for Beginners: 50/30/20 & Zero-Based",
  h1="Simple Monthly Budget for Beginners: 50/30/20 and Zero-Based Budgeting",
  desc="Build a simple monthly budget: work out take-home pay, try the 50/30/20 rule or zero-based budgeting with $3,000 examples, and plan sinking funds.",
  card="Take-home pay, fixed bills, the 50/30/20 rule and zero-based budgeting with worked $3,000 examples.",
  img="budget-tracker.webp",
  cta=("Start with a budget template",
       "The Budget &amp; Expense Tracker covers income, expenses by category, savings goals and clear monthly charts. If you prefer to start simple, Budget Lite is free: income, expenses and balance in one sheet.",
       [("Budget &amp; Expense Tracker",P("budget-expense-173290094"),1),("Free Budget Lite",P("free-budget-lite-173292612"),0)])),
]


# Other languages: same slugs, same numbers, same product links. Texts live in <lang>/meta.json, bodies in <lang>/*.html
LANGS=["en","ru","uk","fr","de","zh"]
INFO={ # html lang, hreflang, og:locale, langCur label, reading speed (words/min; zh: chars/min)
 "en":("en","en","en_US","EN",220), "ru":("ru","ru","ru_RU","RU",180), "uk":("uk","uk","uk_UA","UK",180),
 "fr":("fr","fr","fr_FR","FR",200), "de":("de","de","de_DE","DE",180), "zh":("zh-CN","zh-Hans","zh_CN","中文",400)}
def FMT(lang, s):
    """native number typography: non-breaking thousands/currency/percent spaces"""
    if lang in ("ru","uk"):
        return re.sub(r'(\$\d{1,3}) (\d{3})', '\\1\u00a0\\2', s)
    if lang=="fr":
        s=re.sub(r'(?<![\d,.])(\d{1,3})[ \u00a0\u202f](\d{3})(?=(?:,\d+)?[ \u00a0]?(?:\$|%|€))', '\\1\u202f\\2', s)
    if lang in ("fr","de"):
        s=re.sub(r'(\d) (\$|%)', '\\1\u00a0\\2', s)
    return s
EN_META=dict(glabel="Guides", more="More guides", upd="Updated {d} · {m} min read", date=DATE_H, nav=["News","Products","Guides"],
  foot=["Not investment advice.","All content is for informational purposes only. Trading in financial markets involves risk of loss.","All rights reserved.","Terms of Use","No trackers, no forms, no data collection."],
  crumbs="Breadcrumb", cta_label="Template",
  index=dict(title="Guides: Budgeting, Saving & Goal Planning | Market Plus",
    desc="Free step-by-step guides: Christmas budget 2026, 16 savings challenges for 2027, goal setting with OKRs, a beginner budget and trading journals.",
    h1="Guides: budgeting, saving, goals and trading journals", upd=f"Practical, plain-English guides. Updated {DATE_H}.",
    intro="Step-by-step guides to planning your money and your year: a Christmas budget, savings challenges with real totals, a goal system for 2027, a beginner's monthly budget and how to keep a trading journal. Everything here is general education, not financial advice.",
    outro='Looking for ready-made templates? See all <a href="../#products">products</a> or visit <a href="https://www.patreon.com/DmitryZhuk" target="_blank" rel="noopener">Patreon</a>.'))
def fmt_all(lang, o):
    if isinstance(o,str): return FMT(lang,o)
    if isinstance(o,list): return [fmt_all(lang,x) for x in o]
    if isinstance(o,dict): return {k:fmt_all(lang,v) for k,v in o.items()}
    return o
L10N={"en":dict(EN_META, dir="", up="../")}
for lang in LANGS[1:]:
    m=fmt_all(lang, json.load(open(os.path.join(SRC,lang,"meta.json"))))
    L10N[lang]=dict(m, dir=lang+"/", up="../../")
# <html lang> before first paint. EN guide pages: the visitor's language (?lang= > saved choice > browser) other than EN
# goes to the same guide in that language. Other guide pages keep their language unless ?lang= asks for another one.
def head_script(lang, alt):
    A=json.dumps(alt, separators=(",",":"))
    if lang=="en":
        return f'''<script>/* set <html lang> before first paint: ?lang= > saved choice > browser language; non-English visitors get the guide in their language */
(function(){{var L={{uk:"uk",en:"en",fr:"fr",de:"de",zh:"zh-CN",ru:"ru"}},A={A},c=null;
try{{c=new URLSearchParams(location.search).get("lang")}}catch(e){{}}
if(!L[c]){{try{{c=localStorage.getItem("mp_lang")}}catch(e){{}}}}
if(!L[c]){{var n=(navigator.languages||[navigator.language||"en"]);for(var i=0;i<n.length;i++){{var x=String(n[i]||"").toLowerCase().split("-")[0];if(x==="ua")x="uk";if(L[x]){{c=x;break}}}}}}
if(c&&A[c]){{try{{location.replace(A[c]+location.search+location.hash)}}catch(e){{}}}}
document.documentElement.lang=L[c]||"en";}})();</script>'''
    return f'''<script>/* {lang} guide page: this language unless ?lang= asks for another one (then that language's page) */
(function(){{var A={A},c=null;
try{{c=new URLSearchParams(location.search).get("lang")}}catch(e){{}}
if(c&&A[c]){{try{{location.replace(A[c]+"?lang="+c+location.hash)}}catch(e){{}}}}
document.documentElement.lang="{INFO[lang][0]}";}})();</script>'''
idx=open(os.path.join(ROOT,"index.html")).read()
GLOBE=re.search(r'<button type="button" class="lang-btn".*?</button>', idx, re.S).group(0)
XSVG=re.search(r'(<a class="xbtn".*?</a>)', idx, re.S).group(1)
def header(lang):
    l=L10N[lang]; up=l["up"]; n=l["nav"]; s=INFO[lang][3]
    g=GLOBE if lang=="en" else GLOBE.replace('<span id="langCur">EN</span>',f'<span id="langCur" lang="{"en" if re.search("[A-Za-z]",s) else INFO[lang][0]}" translate="no">{s}</span>')
    return f'''<header class="top"><div class="wrap">
  <div class="brand">
    <a class="logo" href="{up}"><img src="{up}favicon.svg" alt="" width="30" height="30"><span lang="en" translate="no">Market <b>Plus</b></span></a>
    <div class="lang-dd" id="langDD">
      {g}
      <ul class="lang-menu" id="langMenu" role="menu" hidden></ul>
    </div>
  </div>
  <nav class="main" aria-label="Main" data-i18n-aria="nav.aria">
    <a class="hide-xs" href="{up}#news" data-i18n="nav.news">{n[0]}</a>
    <a class="hide-sm" href="{up}#products" data-i18n="nav.products">{n[1]}</a>
    <a href="./" data-i18n="nav.guides">{n[2]}</a>
    {XSVG}
  </nav>
</div></header>'''
def foot(lang):
    l=L10N[lang]; up=l["up"]; f=l["foot"]
    return f'''<footer><div class="wrap">
  <p class="disc"><b data-i18n="foot.na">{f[0]}</b> <span data-i18n="foot.disc">{f[1]}</span></p>
  <div class="flinks" lang="en" translate="no"><a href="https://x.com/MarketPulseGold" target="_blank" rel="noopener">X</a><a href="https://www.patreon.com/DmitryZhuk" target="_blank" rel="noopener">Patreon</a><a href="https://github.com/aiskillsdrop/ai-skills-for-business" target="_blank" rel="noopener">GitHub</a></div>
  <div class="fcopy">© <span id="yr">2026</span> <span lang="en" translate="no">Market Plus</span>. <span data-i18n="foot.rights">{f[2]}</span> · <a href="./" data-i18n="nav.guides">{l["nav"][2]}</a> · <a href="{up}terms.html" data-i18n="foot.terms">{f[3]}</a></div>
  <div class="fpriv" data-i18n="foot.priv">{f[4]}</div>
</div></footer>
<script src="{up}app.js?v=1792944444" defer></script>'''
def page(lang, title, desc, urls, img, body, jsonld, ogtype="article"):
    """urls: {lang: absolute URL} of this page in every language"""
    l=L10N[lang]; up=l["up"]; url=urls[lang]
    t=html.escape(title, quote=True); d=html.escape(desc, quote=True)
    hl="\n".join(f'<link rel="alternate" hreflang="{INFO[x][1]}" href="{urls[x]}">' for x in LANGS)+f'\n<link rel="alternate" hreflang="x-default" href="{urls["en"]}">'
    ogalt="\n".join(f'<meta property="og:locale:alternate" content="{INFO[x][2]}">' for x in LANGS if x!=lang)
    alt={x:urlpath(urls[x]) for x in LANGS if x!=lang}
    dalt=" ".join(f'data-alt-{x}="{urlpath(urls[x])}"' for x in LANGS)
    return f'''<!doctype html>
<html lang="{INFO[lang][0]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<link rel="canonical" href="{url}">
{hl}
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#0b0b0d">
<meta name="color-scheme" content="dark">
<link rel="icon" href="{up}favicon.svg" type="image/svg+xml">
<meta property="og:type" content="{ogtype}">
<meta property="og:site_name" content="Market Plus">
<meta property="og:locale" content="{INFO[lang][2]}">
{ogalt}
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="800">
<meta property="og:image:height" content="450">
{'<meta property="article:published_time" content="'+DATE+'">' if ogtype=="article" else ''}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{img}">
<meta name="twitter:site" content="@MarketPulseGold">
<link rel="stylesheet" href="{up}style.css?v=8">
{head_script(lang, alt)}
<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>
</head>
<body data-static-meta data-page-lang="{lang}" {dalt}>
{header(lang)}

<main id="top" lang="{INFO[lang][0]}">
{body}
</main>

{foot(lang)}
</body>
</html>
'''
def urlpath(u): return u[len(SITE):]
PUB={"@type":"Organization","name":"Market Plus","url":SITE+"/","logo":{"@type":"ImageObject","url":SITE+"/favicon.svg"}}
def crumbs(items):
    return {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":u} for i,(n,u) in enumerate(items)]}
def ctabox(c, lang):
    h,p,links=c
    btns="".join(f'<a class="btn {"btn-gold" if gold else "btn-ghost"}" href="{u}" target="_blank" rel="noopener">{n}</a>' for n,u,gold in links)
    return f'<aside class="cta-box" aria-label="{L10N[lang]["cta_label"]}"><p class="cta-h">{h}</p><p>{p}</p><div class="cta">{btns}</div></aside>'
def wrap_tables(b):
    b=re.sub(r'<div class="tbl">\s*(<table>.*?</table>)\s*</div>', r'\1', b, flags=re.S)
    return re.sub(r'(<table>.*?</table>)', r'<div class="tbl">\1</div>', b, flags=re.S)
def words(s, lang):
    t=re.sub(r'<[^>]+>',' ',s)
    if lang=="zh": return len(re.findall(r'[\u4e00-\u9fff]', t))+len(re.findall(r'[A-Za-z0-9]+', t))
    return len(t.split())
def loc(g, lang):
    """guide fields in a language; translations reuse the EN product URLs and button styles"""
    if lang=="en": return g
    r=L10N[lang]["guides"][g["slug"]]; names=r["buttons"]
    assert len(names)==len(g["cta"][2]), (lang, g["slug"])
    return dict(g, title=r["title"], h1=r["h1"], desc=r["desc"], card=r["card"], src=lang+"/"+g["src"],
                cta=(r["cta_h"], r["cta_p"], [(nm,u,gold) for nm,(_,u,gold) in zip(names, g["cta"][2])]))
def gurl(lang, slug=None): return f"{SITE}/guides/{L10N[lang]['dir']}" + (f"{slug}.html" if slug else "")
smap=[]; idxmap=[]
for lang in LANGS:
    l=L10N[lang]; os.makedirs(os.path.join(OUT, l["dir"]), exist_ok=True)
    GL=[loc(g,lang) for g in G]
    for g in GL:
        urls={x:gurl(x,g['slug']) for x in LANGS}; url=urls[lang]; img=f"{SITE}/assets/{g['img']}"
        body=FMT(lang, open(os.path.join(SRC,g['src'])).read())
        body=re.sub(r'<div class="cta-box" data-cta="\d"></div>', lambda m: ctabox(g['cta'],lang), body)
        body=wrap_tables(body)
        wc=words(body, lang); mins=max(1,round(wc/INFO[lang][4]))
        rel=[o for o in GL if o["slug"]!=g["slug"]]
        related=f'<section class="related"><h2>{l["more"]}</h2><ul class="glist">'+"".join(f'<li><a class="gcard" href="{o["slug"]}.html"><b>{html.escape(o["h1"])}</b><span>{html.escape(o["card"])}</span></a></li>' for o in rel)+'</ul></section>'
        art=f'''<article class="wrap guide">
  <nav class="crumbs" aria-label="{l["crumbs"]}"><a href="{l["up"]}" lang="en" translate="no">Market Plus</a> › <a href="./">{l["glabel"]}</a></nav>
  <h1>{html.escape(g['h1'])}</h1>
  <p class="upd">{l["upd"].format(d=l["date"], m=mins)}</p>
{body}
{related}
</article>'''
        ld={"@context":"https://schema.org","@graph":[{"@type":"Article","headline":g['title'],"description":g['desc'],"image":[img],
            "datePublished":DATE,"dateModified":DATE,"inLanguage":INFO[lang][0],"wordCount":wc,"mainEntityOfPage":{"@type":"WebPage","@id":url},
            "author":{"@type":"Organization","name":"Market Plus","url":SITE+"/"},"publisher":PUB},
            crumbs([("Market Plus",SITE+"/"),(l["glabel"],gurl(lang)),(g['h1'],url)])]}
        open(os.path.join(OUT, l["dir"], g['slug']+".html"),"w").write(page(lang,g['title'],g['desc'],urls,img,art,ld))
        smap.append((url,"monthly","0.7",urls))
        print(lang, g['slug'], wc, mins, len(g['title']), len(g['desc']))
    # index
    urls={x:gurl(x) for x in LANGS}; url=urls[lang]; ix=l["index"]
    cards="".join(f'<li><a class="gcard" href="{g["slug"]}.html"><b>{html.escape(g["h1"])}</b><span>{html.escape(g["card"])}</span></a></li>' for g in GL)
    body=f'''<article class="wrap guide">
  <nav class="crumbs" aria-label="{l["crumbs"]}"><a href="{l["up"]}" lang="en" translate="no">Market Plus</a> › {l["glabel"]}</nav>
  <h1>{ix["h1"]}</h1>
  <p class="upd">{ix["upd"]}</p>
  <p>{ix["intro"]}</p>
  <ul class="glist">{cards}</ul>
  <p style="margin-top:28px">{ix["outro"]}</p>
</article>'''
    ld={"@context":"https://schema.org","@graph":[{"@type":"CollectionPage","name":l["glabel"]+" — Market Plus","url":url,"description":ix["desc"],"inLanguage":INFO[lang][0],"publisher":PUB,
        "mainEntity":{"@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"url":gurl(lang,g['slug']),"name":g['h1']} for i,g in enumerate(GL)]}},
        crumbs([("Market Plus",SITE+"/"),(l["glabel"],url)])]}
    open(os.path.join(OUT, l["dir"], "index.html"),"w").write(page(lang,ix["title"],ix["desc"],urls,SITE+"/assets/budget-tracker.webp",body,ld,ogtype="website"))
    idxmap.append((url,"weekly","0.8",urls))
    print(lang,"index",len(ix["title"]),len(ix["desc"]))
# sitemap with hreflang alternates for every language version
def alts(a):
    if not a: return ""
    return "".join(f'\n    <xhtml:link rel="alternate" hreflang="{INFO[x][1]}" href="{a[x]}"/>' for x in LANGS)+f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{a["en"]}"/>\n  '
urls=[(SITE+"/","daily","1.0",None)]+idxmap+smap+[(SITE+"/terms.html","yearly","0.2",None)]
sm=('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
    +"".join(f"  <url><loc>{u}</loc><lastmod>{DATE}</lastmod><changefreq>{c}</changefreq><priority>{p}</priority>{alts(a)}</url>\n" for u,c,p,a in urls)+"</urlset>\n")
open(os.path.join(ROOT,"sitemap.xml"),"w").write(sm)
