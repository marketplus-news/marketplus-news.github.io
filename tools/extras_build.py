# Builds the free tools section (/tools/), the tool-paired guides, home-page strips and "what next" blocks.
#   python3 tools/extras_build.py      (idempotent; safe to re-run)
import glob, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "extras_src"))
import layout
from icons import icon, art
from products import pcta
from guides_new import GUIDES
import tool_hyrox, tool_str, tool_debt, tool_compound, tool_position, tool_holiday
TOOLS = [m.T for m in (tool_hyrox, tool_str, tool_debt, tool_compound, tool_position, tool_holiday)]
TBY = {t["slug"]: t for t in TOOLS}; GBY = {g["slug"]: g for g in GUIDES}
SITE = "https://marketplus-news.github.io"; DATE = "2026-11-22"; APPV = "1792960000"; CSSV = "3"
PUB = {"@type": "Organization", "name": "Market Plus", "url": SITE + "/"}
def rd(p): return open(os.path.join(ROOT, p), encoding="utf-8").read()
def wr(p, s):
    os.makedirs(os.path.dirname(os.path.join(ROOT, p)) or ROOT, exist_ok=True)
    open(os.path.join(ROOT, p), "w", encoding="utf-8").write(s)
LANGJS = rd("analysis/what-moves-gold-prices.html").split("<script>/* set <html lang>", 1)[1].split("</script>", 1)[0]
LANGJS = "<script>/* set <html lang>" + LANGJS + "</script>"
def esc(s): return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")

def page(path, title, desc, main, active, ld, otype="website", scripts=""):
    url = SITE + "/" + (path[:-10] if path.endswith("index.html") else path)
    head = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#0b0b0d">
<meta name="color-scheme" content="dark">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="{otype}">
<meta property="og:site_name" content="Market Plus">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{SITE}/assets/og-image.jpg">
<link rel="stylesheet" href="/style.css?v=9">
<link rel="preload" href="/assets/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/site.css?v=2">
<link rel="stylesheet" href="/assets/tools.css?v={CSSV}">
{layout.HEAD_JS}
{LANGJS}
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body data-nav="{active}" data-static-meta>
{layout.header("", "en", active)}

<main id="top">
<div class="read-progress" aria-hidden="true"><span></span></div>
{main}
</main>

{layout.footer("", "en")}
<script src="/app.js?v={APPV}" defer></script>
<script src="/assets/site.js?v=1" defer></script>
{scripts}
</body>
</html>
'''
    wr(path, head)

def crumbs(items):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items)]}

def tcard(t, h="h3"):
    return (f'<a class="tcard" href="/tools/{t["slug"]}.html"><span class="free">Free</span><span class="ticon">{icon(t["icon"], 22)}</span>'
            f'<{h}>{t["h1"].replace(" Calculator", "").replace("Airbnb & Short-Term Rental", "Airbnb / STR") if False else t["h1"]}</{h}><p>{t["card"]}</p><span class="mlink">Open the tool →</span></a>')

def ntile_tool(t): return f'<a class="ntile" href="/tools/{t["slug"]}.html"><span class="kicker">Free tool</span><b>{t["h1"]}</b><span>{t["card"]}</span></a>'
def ntile_guide(g): return f'<a class="ntile" href="/guides/{g["slug"]}.html"><span class="kicker">Guide · {g["mins"]} min</span><b>{g["h1"]}</b><span>{g["dek"]}</span></a>'
def ntile_x(u, k, b, s): return f'<a class="ntile" href="{u}"><span class="kicker">{k}</span><b>{b}</b><span>{s}</span></a>'

def next_block(tools=(), guides=(), extra=(), title="What next?"):
    tiles = [ntile_tool(TBY[s]) for s in tools] + [ntile_guide(GBY[s]) for s in guides] + [ntile_x(*e) for e in extra]
    return f'<!--mp:next--><section class="next"><div class="wrap"><h2>{title}</h2><p class="sub">Free tools and guides that go with what you just read.</p><div class="ntiles">{"".join(tiles[:4])}</div></div></section><!--/mp:next-->'

def faq_html(faq):
    return '<h2 id="faq">Frequently asked questions</h2><div class="faq">' + "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faq) + "</div>"

# ---------- tool pages ----------
for i, t in enumerate(TOOLS):
    path = f'tools/{t["slug"]}.html'
    main = f'''<section class="phead thead"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="/" translate="no">Market Plus</a> › <a href="/tools/">Tools</a></nav>
  <div class="thero"><div><span class="kicker">{t["kicker"]} · free tool</span><h1>{t["h1"]}</h1><p class="lead">{t["dek"]}</p>
  <div class="tbadges"><span>Runs in your browser</span><span>No sign-up</span><span>Nothing is sent anywhere</span></div></div>
  <div class="hart-wrap">{art(t["icon"], t["h1"], i + 3)}</div></div>
</div></section>
<section class="psec" style="padding-top:6px"><div class="wrap">{t["calc"]}</div></section>
<article class="wrap guide article" lang="en">
  <div class="art-body">{t["body"]}{faq_html(t["faq"])}</div>
  {pcta(t["product"])}
</article>
{next_block(t["related_tools"], t["related_guides"])}'''
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebApplication", "name": t["h1"], "url": SITE + "/" + path, "description": t["desc"], "applicationCategory": "FinanceApplication" if t["icon"] != "hyrox" else "HealthApplication",
         "operatingSystem": "Any (web browser)", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "publisher": PUB},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]]},
        crumbs([("Market Plus", "/"), ("Tools", "/tools/"), (t["h1"], "/" + path)])]}
    page(path, t["title"], t["desc"], main, "tools", ld, scripts=f'<script src="/assets/calc.js?v={CSSV}"></script>\n<script>{t["js"]}</script>')

# ---------- tools index ----------
cards = "".join(tcard(t) for t in TOOLS)
main = f'''<section class="phead thead"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="/" translate="no">Market Plus</a> › Tools</nav>
  <div class="thero"><div><span class="kicker">Free · no sign-up</span><h1>Free calculators and planners</h1>
  <p class="lead">Six practical tools for money, trading, short-term rentals and Hyrox racing. They run entirely in your browser: no account, no tracking, and nothing you type is sent anywhere.</p>
  <div class="tbadges"><span>6 tools</span><span>Mobile-friendly</span><span>Remembers your inputs on this device</span></div></div>
  <div class="hart-wrap">{art("spark", "Free tools", 2)}</div></div>
</div></section>
<section class="psec"><div class="wrap"><div class="tstrip grid">{cards}</div></div></section>
<section class="psec"><div class="wrap"><div class="shead"><div><h2>Guides that go with the tools</h2><p class="sub">The reasoning behind the numbers, in plain English.</p></div><a class="more" href="/guides/">All guides →</a></div>
<div class="ntiles">{"".join(ntile_guide(g) for g in GUIDES)}</div></div></section>
<section class="psec"><div class="wrap"><div class="etsy"><div><span class="kicker">Templates</span><h2>Want the full spreadsheet?</h2><p>Each tool has a matching Excel and Google Sheets template in the MarketPulseStudio shop: trackers, dashboards and planners you keep.</p></div>
<div class="cta"><a class="btn btn-gold" href="https://marketpulsestudio.etsy.com" target="_blank" rel="noopener">Etsy shop</a><a class="btn btn-ghost" href="/shop-crypto.html">Pay with USDC</a></div></div></div></section>'''
ld = {"@context": "https://schema.org", "@graph": [{"@type": "CollectionPage", "name": "Free calculators and planners — Market Plus", "url": SITE + "/tools/", "publisher": PUB,
      "hasPart": [{"@type": "WebApplication", "name": t["h1"], "url": f'{SITE}/tools/{t["slug"]}.html'} for t in TOOLS]}, crumbs([("Market Plus", "/"), ("Tools", "/tools/")])]}
page("tools/index.html", "Free Calculators: Debt, Savings, Airbnb, Hyrox, Position Size | Market Plus",
     "Free online calculators that run in your browser: debt snowball vs avalanche, compound interest, Airbnb profit, Hyrox finish time, forex and gold position size, and a holiday budget planner.", main, "tools", ld)

# ---------- new guides ----------
for i, g in enumerate(GUIDES):
    path = f'guides/{g["slug"]}.html'; t = TBY[g["tool"]]
    others = [x["slug"] for x in GUIDES if x["slug"] != g["slug"]][:2]
    main = f'''<article class="wrap guide article" lang="en">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="/" translate="no">Market Plus</a> › <a href="/guides/">Guides</a></nav>
  <div class="hart-wrap ghead">{art(g["icon"], g["h1"], i + 11)}</div>
  <span class="kicker">{g["kicker"]}</span>
  <h1>{g["h1"]}</h1>
  <p class="dek">{g["dek"]}</p>
  <p class="upd">Published November 22, 2026 · {g["mins"]} min read</p>
  <a class="tryit" href="/tools/{t["slug"]}.html"><span class="ticon">{icon(t["icon"], 20)}</span><span><b>Try it with your numbers:</b> {t["h1"]} (free)</span><span aria-hidden="true">→</span></a>
  <div class="art-body">{g["body"]}</div>
  {pcta(g["product"], "Ready-made template")}
</article>
{next_block([g["tool"]] + [x for x in ("compound-interest-calculator", "debt-payoff-calculator") if x != g["tool"]][:1], others)}'''
    ld = {"@context": "https://schema.org", "@graph": [{"@type": "Article", "headline": g["h1"], "description": g["desc"], "datePublished": DATE, "dateModified": DATE, "inLanguage": "en",
          "mainEntityOfPage": SITE + "/" + path, "author": PUB, "publisher": PUB, "image": SITE + "/assets/og-image.jpg"}, crumbs([("Market Plus", "/"), ("Guides", "/guides/"), (g["h1"], "/" + path)])]}
    page(path, g["title"], g["desc"], main, "guides", ld, otype="article")

# ---------- "what next" on existing articles and guides ----------
MAP = {"what-moves-gold-prices": (["position-size-calculator", "compound-interest-calculator"], ["position-sizing-explained"]),
       "how-forex-quotes-work": (["position-size-calculator"], ["position-sizing-explained", "debt-snowball-vs-avalanche"]),
       "crypto-market-basics": (["position-size-calculator", "compound-interest-calculator"], ["position-sizing-explained"]),
       "how-stock-indices-work": (["compound-interest-calculator", "position-size-calculator"], ["position-sizing-explained"]),
       "how-to-keep-a-trading-journal": (["position-size-calculator", "compound-interest-calculator"], ["position-sizing-explained"]),
       "how-to-plan-christmas-budget-2026": (["holiday-budget-planner", "debt-payoff-calculator"], ["debt-snowball-vs-avalanche"]),
       "savings-challenges-2027": (["compound-interest-calculator", "holiday-budget-planner"], ["debt-snowball-vs-avalanche"]),
       "how-to-set-goals-2027": (["compound-interest-calculator", "hyrox-finish-time-calculator"], ["hyrox-pacing-strategy"]),
       "simple-monthly-budget-for-beginners": (["debt-payoff-calculator", "compound-interest-calculator"], ["debt-snowball-vs-avalanche"])}
for p in glob.glob(os.path.join(ROOT, "analysis", "*.html")) + glob.glob(os.path.join(ROOT, "guides", "**", "*.html"), recursive=True):
    slug = os.path.basename(p)[:-5]
    if slug not in MAP: continue
    r = os.path.relpath(p, ROOT); s = rd(r)
    s = re.sub(r"<!--mp:next-->.*?<!--/mp:next-->\n?", "", s, flags=re.S)
    tl, gl = MAP[slug]
    s = s.replace("</main>", next_block(tl, gl, title="Try a free tool") + "\n</main>", 1)
    wr(r, s)


# ---------- shop and planners: free tools before buying ----------
for r, tl, gl in [("shop-crypto.html", ["hyrox-finish-time-calculator", "airbnb-rental-profit-calculator"], ["hyrox-pacing-strategy", "how-to-price-airbnb"]),
                  ("planners/index.html", ["debt-payoff-calculator", "holiday-budget-planner", "compound-interest-calculator"], ["debt-snowball-vs-avalanche"])]:
    s = re.sub(r"<!--mp:next-->.*?<!--/mp:next-->\n?", "", rd(r), flags=re.S)
    wr(r, s.replace("</main>", next_block(tl, gl, title="Try before you buy: free tools") + "\n</main>", 1))

# ---------- guides index (English): add the new guides ----------
gi = rd("guides/index.html")
gi = re.sub(r"<!--mp:gnew-->.*?<!--/mp:gnew-->", "", gi, flags=re.S)
new = "".join(f'<li><a class="gcard" href="{g["slug"]}.html"><b>{g["h1"]}</b><span>{g["dek"]}</span></a></li>' for g in GUIDES)
gi = gi.replace('<ul class="glist">', '<ul class="glist"><!--mp:gnew-->' + new + '<!--/mp:gnew-->', 1)
gi = gi.replace("or visit .</p>", 'or visit the <a href="https://marketpulsestudio.etsy.com" target="_blank" rel="noopener">Etsy shop</a>. Prefer numbers? Try the <a href="/tools/">free calculators</a>.</p>')
wr("guides/index.html", gi)

# ---------- home page ----------
idx = rd("index.html")
for m in ("tools", "start", "keep"):
    idx = re.sub(r"<!--mp:%s-->.*?<!--/mp:%s-->\n*" % (m, m), "", idx, flags=re.S)
tools_strip = (f'<!--mp:tools--><section id="tools" class="tools-home"><div class="wrap"><div class="shead"><div><h2 data-i18n="home.tools.h">Free tools</h2>'
    f'<p class="sub" data-i18n="home.tools.sub">Calculators that run in your browser. Nothing is sent anywhere.</p></div><a class="more" href="/tools/" data-i18n="tools.all">All tools →</a></div>'
    f'<div class="tstrip">{cards}</div></div></section><!--/mp:tools-->\n\n')
start = ('<!--mp:start--><section id="start" class="start-home"><div class="wrap"><h2 data-i18n="home.start.h">Start here: most popular</h2>'
    '<p class="sub">Our best-selling systems and the free tools that go with them.</p><div class="start">'
    '<a class="spick" href="/tools/hyrox-finish-time-calculator.html"><div class="pimg"><img src="/assets/crypto/hyrox.webp" alt="Hyrox Race-Prep System" loading="lazy" width="900" height="900"></div><div class="pb"><span class="rank">#1 · Fitness</span><h3>Hyrox Race-Prep System</h3><p>16-week plan and split calculator. Predict your finish time free, then get the full system.</p><span class="mlink">Predict my time →</span></div></a>'
    '<a class="spick" href="/tools/airbnb-rental-profit-calculator.html"><div class="pimg"><img src="/assets/crypto/str-complete.webp" alt="STR Host System" loading="lazy" width="900" height="720"></div><div class="pb"><span class="rank">#2 · Short-term rental</span><h3>STR Host System</h3><p>Is your Airbnb profitable? Check break-even occupancy free, then run it with the host system.</p><span class="mlink">Check my numbers →</span></div></a>'
    '<a class="spick" href="/tools/debt-payoff-calculator.html"><div class="pimg"><img src="/assets/debt-snowball-tracker.webp" alt="Debt snowball tracker" loading="lazy" width="900" height="600"></div><div class="pb"><span class="rank">#3 · Money</span><h3>Debt-free date planner</h3><p>Snowball or avalanche? Compare both with your own debts in under a minute.</p><span class="mlink">Find my date →</span></div></a>'
    '</div></div></section><!--/mp:start-->\n\n')
keep = ('<!--mp:keep--><section id="keep" class="next"><div class="wrap"><h2 data-i18n="home.next.h">Keep reading</h2><p class="sub">New practical guides, each paired with a free tool.</p><div class="ntiles">'
    + "".join(ntile_guide(g) for g in GUIDES) + '</div></div></section><!--/mp:keep-->\n\n')
idx = idx.replace('<!--mp:latest-->', tools_strip + start + '<!--mp:latest-->', 1)
idx = idx.replace('<section id="about">', keep + '<section id="about">', 1)
wr("index.html", idx)

# ---------- sitemap ----------
sm = rd("sitemap.xml")
urls = [("/tools/", "weekly", "0.9")] + [(f'/tools/{t["slug"]}.html', "monthly", "0.8") for t in TOOLS] + [(f'/guides/{g["slug"]}.html', "monthly", "0.7") for g in GUIDES]
for u, c, pr in urls:
    sm = re.sub(r"  <url><loc>%s</loc>.*?</url>\n" % re.escape(SITE + u), "", sm, flags=re.S)
add = "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{DATE}</lastmod><changefreq>{c}</changefreq><priority>{pr}</priority></url>\n" for u, c, pr in urls)
sm = sm.replace("</urlset>", add + "</urlset>")
wr("sitemap.xml", sm)
print("tools:", len(TOOLS), "guides:", len(GUIDES))
