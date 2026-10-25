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

# Russian versions: same slugs, same numbers, same product links (pages in guides/ru/)
RU={
 "how-to-plan-christmas-budget-2026": dict(
  title="Как спланировать бюджет на Рождество 2026: пошагово",
  h1="Как спланировать рождественский бюджет на 2026 год (пошагово)",
  desc="Рождественский бюджет на 2026 год шаг за шагом: общая сумма по средствам, лимиты на подарки, скрытые расходы, пример таблицы и советы по учёту трат.",
  card="Общая сумма, лимит на подарок каждому, скрытые расходы и учёт трат — с примером бюджета на $800.",
  cta=("Ведите рождественский бюджет в готовой таблице",
       "Таблица «Бюджет и список подарков на Рождество 2026» для Excel и Google Sheets включает список подарков с планом и фактом, праздничные траты по категориям и панель с диаграммами. Нужен только список подарков? Бесплатная версия отслеживает бюджет, фактическую цену и статус «куплен / упакован» для каждого подарка.",
       ["Бюджет и список подарков на Рождество 2026 ($4)","Бесплатный список подарков на Рождество"])),
 "savings-challenges-2027": dict(
  title="16 челленджей накоплений на 2027 год (с реальными итогами)",
  h1="16 челленджей накоплений на 2027 год: как работает каждый и реальные итоги",
  desc="16 челленджей накоплений на 2027 год: 52 недели ($1 378), 100 конвертов ($5 050), 26 недель, челлендж по центу и другие — с точными годовыми итогами.",
  card="52 недели, 100 конвертов, 26 недель, по центу и ещё 12 челленджей — с точными итогами и сводной таблицей.",
  cta=("Распечатайте свой челлендж и закрашивайте клеточки",
       "«Набор челленджей накоплений 2027» — это 16 челленджей для печати (52 недели, 100 конвертов, $10 000 и другие) в форматах A6, A4 и US Letter, а также трекер Excel с автоматическими итогами.",
       ["Набор челленджей накоплений 2027 ($4)"])),
 "how-to-set-goals-2027": dict(
  title="Как ставить цели на 2027 год и не бросать их",
  h1="Как ставить цели на 2027 год, которых вы действительно будете придерживаться",
  desc="Простая система целей на 2027 год: видение года по сферам жизни, 3–5 целей, квартальные OKR, еженедельные действия и чек-лист ежемесячного обзора.",
  card="Видение года, 3–5 целей, квартальные OKR с разобранным примером, еженедельные действия и ежемесячный обзор.",
  cta=("Ведите эту систему в Notion",
       "«Планировщик целей и жизни 2027 Pro» для Notion связывает цели с квартальными OKR, проектами и финансовыми целями, так что прогресс обновляется автоматически; в нём есть статистика привычек и еженедельные, ежемесячные и годовые обзоры. Хотите начать бесплатно? В версии Lite есть видение года, цели с индикаторами прогресса, недельный трекер привычек и ежемесячный обзор.",
       ["Планировщик целей и жизни 2027 Pro ($9)","Бесплатная версия Lite для Notion"])),
 "how-to-keep-a-trading-journal": dict(
  title="Как вести журнал трейдера: что записывать и зачем",
  h1="Как вести журнал трейдера: что записывать и зачем",
  desc="Что записывать в журнал трейдера и зачем: поля сделки, R-мультипликатор, доля прибыльных сделок, матожидание и просадка — простыми словами. Только для обучения.",
  card="Какие поля записывать по каждой сделке, как считать R и какие метрики важны при разборе. Только для обучения.",
  cta=("Возьмите готовый шаблон журнала",
       "Trading Journal Pro для Google Sheets и Excel автоматически считает долю прибыльных сделок, R-мультипликатор и P&amp;L, а также включает дашборд и разбор ошибок. Бесплатная версия Lite — простой способ начать вести записи уже сегодня. Шаблоны — это инструменты учёта, а не торговые рекомендации.",
       ["Trading Journal Pro","Бесплатный Trading Journal Lite"])),
 "simple-monthly-budget-for-beginners": dict(
  title="Простой месячный бюджет для начинающих: 50/30/20 и нулевой баланс",
  h1="Простой месячный бюджет для начинающих: правило 50/30/20 и бюджет с нулевым балансом",
  desc="Составьте простой месячный бюджет: посчитайте чистый доход, попробуйте правило 50/30/20 или бюджет с нулевым балансом на примерах с $3 000 и спланируйте целевые фонды.",
  card="Чистый доход, обязательные платежи, правило 50/30/20 и бюджет с нулевым балансом на разобранных примерах с $3 000.",
  cta=("Начните с шаблона бюджета",
       "Budget &amp; Expense Tracker охватывает доходы, расходы по категориям, цели накоплений и наглядные графики по месяцам. Если хотите начать с простого, Budget Lite бесплатен: доходы, расходы и остаток в одной таблице.",
       ["Budget &amp; Expense Tracker","Бесплатный Budget Lite"])),
}
NB=lambda s: re.sub(r'(\$\d{1,3}) (\d{3})', '\\1\u00a0\\2', s)  # "$1 378" -> non-breaking thousands space
L10N={
 "en": dict(dir="", up="../", og="en_US", guides="Guides", more="More guides", upd="Updated {d} · {m} min read",
            date=DATE_H, nav=("News","Products","Guides"),
            foot=("Not investment advice.","All content is for informational purposes only. Trading in financial markets involves risk of loss.","All rights reserved.","Terms of Use","No trackers, no forms, no data collection."),
            crumbs="Breadcrumb", cta_label="Template"),
 "ru": dict(dir="ru/", up="../../", og="ru_RU", guides="Гайды", more="Другие гайды", upd="Обновлено {d} · {m} мин чтения",
            date="25 октября 2026 г.", nav=("Новости","Продукты","Гайды"),
            foot=("Не является инвестиционной рекомендацией.","Все материалы носят исключительно ознакомительный характер. Торговля на финансовых рынках связана с риском потери средств.","Все права защищены.","Условия использования","Без трекеров, без форм, без сбора данных."),
            crumbs="Навигация", cta_label="Шаблон"),
}
# <html lang> before first paint. EN guide pages: if the visitor's language (?lang= > saved choice > browser) is RU,
# go to the Russian version of the same page. RU guide pages: an explicit ?lang= other than ru goes to the English page.
def head_script(lang, alt):
    if lang=="en":
        go=f'if(c==="ru"){{try{{location.replace("{alt}"+location.hash)}}catch(e){{}}}}'
        return f'''<script>/* set <html lang> before first paint: ?lang= > saved choice > browser language; RU visitors get the Russian guide */
(function(){{var L={{uk:"uk",en:"en",fr:"fr",de:"de",zh:"zh-CN",ru:"ru"}},c=null;
try{{c=new URLSearchParams(location.search).get("lang")}}catch(e){{}}
if(!L[c]){{try{{c=localStorage.getItem("mp_lang")}}catch(e){{}}}}
if(!L[c]){{var n=(navigator.languages||[navigator.language||"en"]);for(var i=0;i<n.length;i++){{var x=String(n[i]||"").toLowerCase().split("-")[0];if(x==="ua")x="uk";if(L[x]){{c=x;break}}}}}}
{go}
document.documentElement.lang=L[c]||"en";}})();</script>'''
    return f'''<script>/* Russian guide page: Russian UI unless ?lang= asks for another language (then the English page) */
(function(){{var L={{uk:1,en:1,fr:1,de:1,zh:1}},c=null;
try{{c=new URLSearchParams(location.search).get("lang")}}catch(e){{}}
if(L[c]){{try{{location.replace("{alt}?lang="+c+location.hash)}}catch(e){{}}}}
document.documentElement.lang="ru";}})();</script>'''
idx=open(os.path.join(ROOT,"index.html")).read()
GLOBE=re.search(r'<button type="button" class="lang-btn".*?</button>', idx, re.S).group(0)
XSVG=re.search(r'(<a class="xbtn".*?</a>)', idx, re.S).group(1)
def header(lang):
    l=L10N[lang]; up=l["up"]; n=l["nav"]
    g=GLOBE if lang=="en" else GLOBE.replace('<span id="langCur">EN</span>','<span id="langCur" lang="en" translate="no">RU</span>')
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
<script src="{up}app.js?v=1792933333" defer></script>'''
def page(lang, title, desc, url, alt, img, body, jsonld, ogtype="article"):
    l=L10N[lang]; up=l["up"]
    t=html.escape(title, quote=True); d=html.escape(desc, quote=True)
    en_url, ru_url = (url, alt) if lang=="en" else (alt, url)
    alt_rel = os.path.relpath(urlpath(alt), os.path.dirname(urlpath(url)) if not url.endswith("/") else urlpath(url))
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="ru" href="{ru_url}">
<link rel="alternate" hreflang="x-default" href="{en_url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#0b0b0d">
<meta name="color-scheme" content="dark">
<link rel="icon" href="{up}favicon.svg" type="image/svg+xml">
<meta property="og:type" content="{ogtype}">
<meta property="og:site_name" content="Market Plus">
<meta property="og:locale" content="{l["og"]}">
<meta property="og:locale:alternate" content="{L10N["ru" if lang=="en" else "en"]["og"]}">
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
{head_script(lang, alt_rel if alt_rel.endswith(".html") else alt_rel.rstrip("/")+"/")}
<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>
</head>
<body data-static-meta data-page-lang="{lang}" data-alt-en="{urlpath(en_url)}" data-alt-ru="{urlpath(ru_url)}">
{header(lang)}

<main id="top" lang="{lang}">
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
def words(s): return len(re.sub(r'<[^>]+>',' ',s).split())
def loc(g, lang):
    """guide fields in a language; RU reuses the EN product URLs and button styles"""
    if lang=="en": return g
    r=RU[g["slug"]]; h,p,names=r["cta"]
    assert len(names)==len(g["cta"][2])
    return dict(g, title=NB(r["title"]), h1=NB(r["h1"]), desc=NB(r["desc"]), card=NB(r["card"]), src="ru/"+g["src"],
                cta=(NB(h), NB(p), [(NB(nm),u,gold) for nm,(_,u,gold) in zip(names, g["cta"][2])]))
def gurl(lang, slug=None): return f"{SITE}/guides/{L10N[lang]['dir']}" + (f"{slug}.html" if slug else "")
smap=[]
for lang in ("en","ru"):
    l=L10N[lang]; os.makedirs(os.path.join(OUT, l["dir"]), exist_ok=True)
    GL=[loc(g,lang) for g in G]
    for g in GL:
        other="ru" if lang=="en" else "en"
        url=gurl(lang,g['slug']); alt=gurl(other,g['slug']); img=f"{SITE}/assets/{g['img']}"
        body=open(os.path.join(SRC,g['src'])).read()
        if lang=="ru": body=NB(body)
        body=re.sub(r'<div class="cta-box" data-cta="\d"></div>', ctabox(g['cta'],lang), body)
        body=wrap_tables(body)
        wc=words(body); mins=max(1,round(wc/(220 if lang=="en" else 180)))
        rel=[o for o in GL if o["slug"]!=g["slug"]]
        related=f'<section class="related"><h2>{l["more"]}</h2><ul class="glist">'+"".join(f'<li><a class="gcard" href="{o["slug"]}.html"><b>{html.escape(o["h1"])}</b><span>{html.escape(o["card"])}</span></a></li>' for o in rel)+'</ul></section>'
        art=f'''<article class="wrap guide">
  <nav class="crumbs" aria-label="{l["crumbs"]}"><a href="{l["up"]}" lang="en" translate="no">Market Plus</a> › <a href="./">{l["guides"]}</a></nav>
  <h1>{html.escape(g['h1'])}</h1>
  <p class="upd">{l["upd"].format(d=l["date"], m=mins)}</p>
{body}
{related}
</article>'''
        ld={"@context":"https://schema.org","@graph":[{"@type":"Article","headline":g['title'],"description":g['desc'],"image":[img],
            "datePublished":DATE,"dateModified":DATE,"inLanguage":lang,"wordCount":wc,"mainEntityOfPage":{"@type":"WebPage","@id":url},
            "author":{"@type":"Organization","name":"Market Plus","url":SITE+"/"},"publisher":PUB},
            crumbs([("Market Plus",SITE+"/"),(l["guides"],gurl(lang)),(g['h1'],url)])]}
        open(os.path.join(OUT, l["dir"], g['slug']+".html"),"w").write(page(lang,g['title'],g['desc'],url,alt,img,art,ld))
        smap.append((url,"monthly","0.7",alt))
        print(lang, g['slug'], wc, len(g['title']), len(g['desc']))
    # index
    url=gurl(lang); alt=gurl("ru" if lang=="en" else "en")
    cards="".join(f'<li><a class="gcard" href="{g["slug"]}.html"><b>{html.escape(g["h1"])}</b><span>{html.escape(g["card"])}</span></a></li>' for g in GL)
    if lang=="en":
        H1="Guides: budgeting, saving, goals and trading journals"
        UPD=f"Practical, plain-English guides. Updated {DATE_H}."
        INTRO="Step-by-step guides to planning your money and your year: a Christmas budget, savings challenges with real totals, a goal system for 2027, a beginner's monthly budget and how to keep a trading journal. Everything here is general education, not financial advice."
        OUTRO='Looking for ready-made templates? See all <a href="../#products">products</a> or visit <a href="https://www.patreon.com/DmitryZhuk" target="_blank" rel="noopener">Patreon</a>.'
        T="Guides: Budgeting, Saving & Goal Planning | Market Plus"
        D="Free step-by-step guides: Christmas budget 2026, 16 savings challenges for 2027, goal setting with OKRs, a beginner budget and trading journals."
    else:
        H1="Гайды: бюджет, накопления, цели и журнал трейдера"
        UPD="Практичные руководства простым языком. Обновлено 25 октября 2026 г."
        INTRO="Пошаговые руководства по планированию денег и года: рождественский бюджет, челленджи накоплений с реальными итогами, система целей на 2027 год, месячный бюджет для начинающих и ведение журнала трейдера. Всё здесь — общая образовательная информация, а не финансовая рекомендация."
        OUTRO='Ищете готовые шаблоны? Смотрите все <a href="../../#products">продукты</a> или загляните на <a href="https://www.patreon.com/DmitryZhuk" target="_blank" rel="noopener" lang="en" translate="no">Patreon</a>.'
        T="Гайды: бюджет, накопления и планирование целей | Market Plus"
        D="Бесплатные пошаговые гайды: рождественский бюджет 2026, 16 челленджей накоплений на 2027 год, постановка целей с OKR, бюджет для начинающих и журнал трейдера."
    body=f'''<article class="wrap guide">
  <nav class="crumbs" aria-label="{l["crumbs"]}"><a href="{l["up"]}" lang="en" translate="no">Market Plus</a> › {l["guides"]}</nav>
  <h1>{H1}</h1>
  <p class="upd">{UPD}</p>
  <p>{INTRO}</p>
  <ul class="glist">{cards}</ul>
  <p style="margin-top:28px">{OUTRO}</p>
</article>'''
    ld={"@context":"https://schema.org","@graph":[{"@type":"CollectionPage","name":l["guides"]+" — Market Plus","url":url,"description":D,"inLanguage":lang,"publisher":PUB,
        "mainEntity":{"@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"url":gurl(lang,g['slug']),"name":g['h1']} for i,g in enumerate(GL)]}},
        crumbs([("Market Plus",SITE+"/"),(l["guides"],url)])]}
    open(os.path.join(OUT, l["dir"], "index.html"),"w").write(page(lang,T,D,url,alt,SITE+"/assets/budget-tracker.webp",body,ld,ogtype="website"))
    smap.insert(0 if lang=="en" else 1,(url,"weekly","0.8",alt))
    print(lang,"index",len(T),len(D))
# sitemap with hreflang alternates for the EN/RU guide pairs
def alts(u,a):
    if not a: return ""
    en,ru=(u,a) if "/guides/ru/" not in u else (a,u)
    return (f'\n    <xhtml:link rel="alternate" hreflang="en" href="{en}"/>\n    <xhtml:link rel="alternate" hreflang="ru" href="{ru}"/>'
            f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{en}"/>\n  ')
urls=[(SITE+"/","daily","1.0",None)]+smap+[(SITE+"/terms.html","yearly","0.2",None)]
sm=('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
    +"".join(f"  <url><loc>{u}</loc><lastmod>{DATE}</lastmod><changefreq>{c}</changefreq><priority>{p}</priority>{alts(u,a)}</url>\n" for u,c,p,a in urls)+"</urlset>\n")
open(os.path.join(ROOT,"sitemap.xml"),"w").write(sm)
