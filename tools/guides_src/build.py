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
       [("Christmas Budget &amp; Gift Tracker 2026 ($3)",P("christmas-budget-173352149"),1),("Free Christmas Gift List",P("free-christmas-173352318"),0)])),
 dict(slug="savings-challenges-2027", src="savings.html",
  title="16 Savings Challenges for 2027 (With Real Totals)",
  h1="16 Savings Challenges for 2027: How Each Works and the Real Totals",
  desc="16 savings challenges for 2027 explained: 52-week ($1,378), 100 envelope ($5,050), 26-week, penny challenge and more, with exact yearly totals.",
  card="52-week, 100 envelope, 26-week, penny and 12 more challenges, with exact totals and a summary table.",
  img="savings-challenge-2027.webp",
  cta=("Print your challenge and colour it in",
       "The 2027 Savings Challenge Pack includes 16 printable savings challenges (52-week, 100-envelope, $10,000 and more) in A6, A4 and US Letter sizes, plus an Excel tracker with automatic totals.",
       [("2027 Savings Challenge Pack ($3.50)",P("2027-savings-16-173352268"),1)])),
 dict(slug="how-to-set-goals-2027", src="goals.html",
  title="How to Set Goals for 2027 You Actually Keep",
  h1="How to Set Goals for 2027 That You Actually Keep",
  desc="A simple goal system for 2027: a yearly vision by life area, 3 to 5 goals, quarterly OKRs, weekly actions and a monthly review checklist.",
  card="Yearly vision, 3 to 5 goals, quarterly OKRs with a worked example, weekly actions and a monthly review.",
  img="goal-planner-2027-pro.webp",
  cta=("Run this system in Notion",
       "The 2027 Goal &amp; Life Planner Pro for Notion connects goals to quarterly OKRs, projects and money goals so progress updates automatically, with habit stats and weekly, monthly and year-end reviews. Want to start free? The Lite version has a year vision, goals with progress bars, a weekly habit tracker and a monthly review.",
       [("2027 Goal &amp; Life Planner Pro ($4.50)",P("2027-goal-life-173353268"),1),("Free Lite version for Notion","https://viridian-question-22d.notion.site/2027-Goal-Life-Planner-Lite-40418c614944812e8d68c49b3f754ff6",0)])),
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
HEAD_SCRIPT='''<script>/* set <html lang> before first paint: ?lang= > saved choice > browser language */
(function(){var L={uk:"uk",en:"en",fr:"fr",de:"de",zh:"zh-CN",ru:"ru"},c=null;
try{c=new URLSearchParams(location.search).get("lang")}catch(e){}
if(!L[c]){try{c=localStorage.getItem("mp_lang")}catch(e){}}
if(!L[c]){var n=(navigator.languages||[navigator.language||"en"]);for(var i=0;i<n.length;i++){var x=String(n[i]||"").toLowerCase().split("-")[0];if(x==="ua")x="uk";if(L[x]){c=x;break}}}
document.documentElement.lang=L[c]||"en";})();</script>'''
idx=open(os.path.join(ROOT,"index.html")).read()
GLOBE=re.search(r'<button type="button" class="lang-btn".*?</button>', idx, re.S).group(0)
XSVG=re.search(r'(<a class="xbtn".*?</a>)', idx, re.S).group(1)
def header():
    return f'''<header class="top"><div class="wrap">
  <div class="brand">
    <a class="logo" href="../"><img src="../favicon.svg" alt="" width="30" height="30"><span lang="en" translate="no">Market <b>Plus</b></span></a>
    <div class="lang-dd" id="langDD">
      {GLOBE}
      <ul class="lang-menu" id="langMenu" role="menu" hidden></ul>
    </div>
  </div>
  <nav class="main" aria-label="Main">
    <a class="hide-xs" href="../#news" data-i18n="nav.news">News</a>
    <a class="hide-sm" href="../#products" data-i18n="nav.products">Products</a>
    <a href="./" data-i18n="nav.guides">Guides</a>
    {XSVG}
  </nav>
</div></header>'''
FOOT='''<footer><div class="wrap">
  <p class="disc"><b data-i18n="foot.na">Not investment advice.</b> <span data-i18n="foot.disc">All content is for informational purposes only. Trading in financial markets involves risk of loss.</span></p>
  <div class="flinks" lang="en" translate="no"><a href="https://x.com/MarketPulseGold" target="_blank" rel="noopener">X</a><a href="https://www.patreon.com/DmitryZhuk" target="_blank" rel="noopener">Patreon</a><a href="https://github.com/aiskillsdrop/ai-skills-for-business" target="_blank" rel="noopener">GitHub</a></div>
  <div class="fcopy">© <span id="yr">2026</span> <span lang="en" translate="no">Market Plus</span>. <span data-i18n="foot.rights">All rights reserved.</span> · <a href="./" data-i18n="nav.guides">Guides</a> · <a href="../terms.html" data-i18n="foot.terms">Terms of Use</a></div>
  <div class="fpriv" data-i18n="foot.priv">No trackers, no forms, no data collection.</div>
</div></footer>
<script src="../app.js?v=1792933332" defer></script>'''
def page(title, desc, url, img, body, jsonld, ogtype="article"):
    t=html.escape(title, quote=True); d=html.escape(desc, quote=True)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#0b0b0d">
<meta name="color-scheme" content="dark">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<meta property="og:type" content="{ogtype}">
<meta property="og:site_name" content="Market Plus">
<meta property="og:locale" content="en_US">
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
<link rel="stylesheet" href="../style.css?v=8">
{HEAD_SCRIPT}
<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>
</head>
<body data-static-meta>
{header()}

<main id="top" lang="en">
{body}
</main>

{FOOT}
</body>
</html>
'''
PUB={"@type":"Organization","name":"Market Plus","url":SITE+"/","logo":{"@type":"ImageObject","url":SITE+"/favicon.svg"}}
def crumbs(items):
    return {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":u} for i,(n,u) in enumerate(items)]}
def ctabox(c):
    h,p,links=c
    btns="".join(f'<a class="btn {"btn-gold" if gold else "btn-ghost"}" href="{u}" target="_blank" rel="noopener">{n}</a>' for n,u,gold in links)
    return f'<aside class="cta-box" aria-label="Template"><p class="cta-h">{h}</p><p>{p}</p><div class="cta">{btns}</div></aside>'
def wrap_tables(b):
    b=re.sub(r'<div class="tbl">\s*(<table>.*?</table>)\s*</div>', r'\1', b, flags=re.S)
    return re.sub(r'(<table>.*?</table>)', r'<div class="tbl">\1</div>', b, flags=re.S)
def words(s): return len(re.sub(r'<[^>]+>',' ',s).split())
for g in G:
    url=f"{SITE}/guides/{g['slug']}.html"; img=f"{SITE}/assets/{g['img']}"
    body=open(os.path.join(SRC,g['src'])).read()
    body=re.sub(r'<div class="cta-box" data-cta="\d"></div>', ctabox(g['cta']), body)
    body=wrap_tables(body)
    wc=words(body); mins=max(1,round(wc/220))
    rel=[o for o in G if o is not g]
    related='<section class="related"><h2>More guides</h2><ul class="glist">'+"".join(f'<li><a class="gcard" href="{o["slug"]}.html"><b>{html.escape(o["h1"])}</b><span>{html.escape(o["card"])}</span></a></li>' for o in rel)+'</ul></section>'
    art=f'''<article class="wrap guide">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="../">Market Plus</a> › <a href="./">Guides</a></nav>
  <h1>{html.escape(g['h1'])}</h1>
  <p class="upd">Updated {DATE_H} · {mins} min read</p>
{body}
{related}
</article>'''
    ld={"@context":"https://schema.org","@graph":[{"@type":"Article","headline":g['title'],"description":g['desc'],"image":[img],
        "datePublished":DATE,"dateModified":DATE,"inLanguage":"en","wordCount":wc,"mainEntityOfPage":{"@type":"WebPage","@id":url},
        "author":{"@type":"Organization","name":"Market Plus","url":SITE+"/"},"publisher":PUB},
        crumbs([("Market Plus",SITE+"/"),("Guides",SITE+"/guides/"),(g['h1'],url)])]}
    open(f"{OUT}/{g['slug']}.html","w").write(page(g['title'],g['desc'],url,img,art,ld))
    print(g['slug'], wc, len(g['title']), len(g['desc']))
# index
url=SITE+"/guides/"
cards="".join(f'<li><a class="gcard" href="{g["slug"]}.html"><b>{html.escape(g["h1"])}</b><span>{html.escape(g["card"])}</span></a></li>' for g in G)
body=f'''<article class="wrap guide">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="../">Market Plus</a> › Guides</nav>
  <h1>Guides: budgeting, saving, goals and trading journals</h1>
  <p class="upd">Practical, plain-English guides. Updated {DATE_H}.</p>
  <p>Step-by-step guides to planning your money and your year: a Christmas budget, savings challenges with real totals, a goal system for 2027, a beginner's monthly budget and how to keep a trading journal. Everything here is general education, not financial advice.</p>
  <ul class="glist">{cards}</ul>
  <p style="margin-top:28px">Looking for ready-made templates? See all <a href="../#products">products</a> or visit <a href="https://www.patreon.com/DmitryZhuk" target="_blank" rel="noopener">Patreon</a>.</p>
</article>'''
ld={"@context":"https://schema.org","@graph":[{"@type":"CollectionPage","name":"Guides — Market Plus","url":url,"description":"","inLanguage":"en","publisher":PUB,
    "mainEntity":{"@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"url":f"{SITE}/guides/{g['slug']}.html","name":g['h1']} for i,g in enumerate(G)]}},
    crumbs([("Market Plus",SITE+"/"),("Guides",url)])]}
T="Guides: Budgeting, Saving & Goal Planning | Market Plus"
D="Free step-by-step guides: Christmas budget 2026, 16 savings challenges for 2027, goal setting with OKRs, a beginner budget and trading journals."
ld["@graph"][0]["description"]=D
open(f"{OUT}/index.html","w").write(page(T,D,url,SITE+"/assets/budget-tracker.webp",body,ld,ogtype="website"))
print("index",len(T),len(D))
# sitemap
urls=[(SITE+"/","daily","1.0"),(SITE+"/guides/","weekly","0.8")]+[(f"{SITE}/guides/{g['slug']}.html","monthly","0.7") for g in G]+[(SITE+"/terms.html","yearly","0.2")]
sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join(f"  <url><loc>{u}</loc><lastmod>{DATE}</lastmod><changefreq>{c}</changefreq><priority>{p}</priority></url>\n" for u,c,p in urls)+"</urlset>\n"
open(os.path.join(ROOT,"sitemap.xml"),"w").write(sm)
