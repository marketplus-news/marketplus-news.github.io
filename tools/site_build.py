# Builds the multi-page portal around the existing site (no build step needed to serve it):
#   python3 tools/site_build.py
# - section pages: news/, analysis/, markets/, planners/, about/ and analysis articles (tools/site_src/analysis/*.html)
# - home page blocks (latest articles, sections), shared header/footer on every page (tools/layout.py)
# - extra UI translations injected into app.js, new URLs added to sitemap.xml. Idempotent.
import glob, html, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout import apply_layout, TX, EXTRA_URLS
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "tools", "site_src")
SITE = "https://marketplus-news.github.io"
DATE = "2026-11-01"; DATE_H = "November 1, 2026"
rd = lambda p: open(os.path.join(ROOT, p), encoding="utf-8").read()
def wr(p, s):
    p = os.path.join(ROOT, p); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(s)
esc = lambda s: html.escape(s, quote=True)

# ---------- content index ----------
EXPL = [
 dict(slug="what-moves-gold-prices", src="gold.html", kicker="Gold · XAU/USD", cover="gold", sym="XAU",
      title="What Moves the Gold Price? XAU/USD Explained",
      h1="What Moves the Gold Price? A Plain-English Guide to XAU/USD",
      desc="What drives gold prices: real interest rates, the US dollar, inflation fears, safe-haven demand, central banks and physical demand. Educational explainer.",
      card="Real yields, the dollar, safe-haven demand and central bank buying: the forces behind XAU/USD."),
 dict(slug="how-forex-quotes-work", src="forex.html", kicker="Forex", cover="fx", sym="FX",
      title="How Forex Quotes Work: Pairs, Pips and Spreads",
      h1="How Forex Quotes Work: Currency Pairs, Pips and Spreads",
      desc="How to read a currency pair, what bid, ask, spread, pips and lots mean, and what moves exchange rates. A plain-English forex explainer.",
      card="Base and quote currencies, bid and ask, pips and lots, and what moves exchange rates."),
 dict(slug="crypto-market-basics", src="crypto.html", kicker="Crypto", cover="crypto", sym="BTC",
      title="Crypto Market Basics: Bitcoin, Stablecoins and Market Cap",
      h1="Crypto Market Basics: Bitcoin, Altcoins, Stablecoins and Market Cap",
      desc="A plain-English crypto explainer: Bitcoin, Ether, altcoins and stablecoins, what market cap measures, why prices swing and how custody works.",
      card="Bitcoin, altcoins and stablecoins, what market cap really measures and the main risks."),
 dict(slug="how-stock-indices-work", src="stocks.html", kicker="Stocks", cover="stocks", sym="SPX",
      title="How Stock Indices Work: S&P 500, Nasdaq and Dow",
      h1="How Stock Market Indices Work: S&P 500, Nasdaq and the Dow",
      desc="How the S&P 500, Nasdaq and Dow Jones are built, how index weighting works, index funds such as VTI, and what moves an index.",
      card="How the S&P 500, Nasdaq and Dow are built, why weighting matters, and what moves an index."),
]
def words(s): return len(re.sub(r"<[^>]+>", " ", s).split())
for e in EXPL:
    e["body"] = open(os.path.join(SRC, "analysis", e["src"]), encoding="utf-8").read()
    e["mins"] = max(1, round(words(e["body"]) / 220)); e["url"] = f"/analysis/{e['slug']}.html"; e["date"] = DATE_H
# existing English guides (titles/cards/covers from tools/guides_src/build.py, reading time from the built page)
bsrc = rd("tools/guides_src/build.py")
GUIDES = []
for m in re.finditer(r'dict\(slug="([^"]+)".*?h1="([^"]+)".*?card="([^"]+)".*?img="([^"]+)"', bsrc, re.S):
    slug, h1, card, img = m.groups()
    page = rd(f"guides/{slug}.html"); mm = re.search(r'· (\d+) min read', page)
    kick = {"how-to-keep-a-trading-journal": "Trading", "how-to-plan-christmas-budget-2026": "Budgeting",
            "savings-challenges-2027": "Saving", "how-to-set-goals-2027": "Planning", "simple-monthly-budget-for-beginners": "Budgeting"}.get(slug, "Guide")
    GUIDES.append(dict(slug=slug, h1=html.unescape(h1), card=html.unescape(card), img=img, mins=int(mm.group(1)) if mm else 5,
                       url=f"/guides/{slug}.html", kicker="Guide · " + kick, date="October 25, 2026"))
ALL = EXPL + GUIDES

def card(a, lvl="h3"):
    if a.get("img"):
        cov = f'<div class="acard-img"><img src="/assets/{a["img"]}" alt="" loading="lazy" decoding="async" width="800" height="450"></div>'
    else:
        cov = f'<div class="acard-img cover cover-{a["cover"]}" aria-hidden="true"><span lang="en" translate="no">{a["sym"]}</span></div>'
    return (f'<article class="acard" lang="en"><a class="acard-link" href="{a["url"]}">{cov}<div class="acard-body">'
            f'<span class="kicker">{esc(a["kicker"])}</span><{lvl}>{esc(a["h1"])}</{lvl}><p>{esc(a["card"])}</p>'
            f'<span class="ameta">{a["date"]} · {a["mins"]} min read</span></div></a></article>')
def grid(items, cls=""): return f'<div class="agrid {cls}">' + "".join(card(a) for a in items) + "</div>"
T_EN = TX["en"]
def k(key, tag="span", cls=None, attrs=""):  # translatable element with English fallback text
    c = f' class="{cls}"' if cls else ""
    return f'<{tag}{c} data-i18n="{key}"{attrs}>{esc(T_EN[key]) if key in T_EN else ""}</{tag}>'

# ---------- page shell ----------
HEAD_LANG = re.search(r'<script>/\* set <html lang> before first paint.*?</script>', rd("index.html"), re.S).group(0)
def shell(path, title, desc, body, active, ogtype="website", jsonld=None, img=SITE + "/assets/og-image.jpg", extra=""):
    url = SITE + path; ld = f'\n<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    t, d = esc(title), esc(desc)
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
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="{ogtype}">
<meta property="og:site_name" content="Market Plus">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{img}">
<meta name="twitter:site" content="@MarketPulseGold">{extra}
<link rel="stylesheet" href="/style.css?v=8">
{HEAD_LANG}{ld}
</head>
<body data-static-meta>
<header class="top"></header>

<main id="top">
{body}
</main>

<footer></footer>
<script src="/app.js?v=1792944444" defer></script>
</body>
</html>
'''
PUB = {"@type": "Organization", "name": "Market Plus", "url": SITE + "/", "logo": {"@type": "ImageObject", "url": SITE + "/favicon.svg"}}
def crumbs_ld(items): return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items)]}
def page_head(key_h, h_en, key_sub, kicker_key=None):
    return (f'<section class="phead"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="/" lang="en" translate="no">Market Plus</a> › '
            f'{k(kicker_key) if kicker_key else ""}</nav><h1 data-i18n="{key_h}">{esc(h_en)}</h1>{k(key_sub, "p", "lead")}</div></section>')
FEED = rd("index.html"); FEED = re.search(r'<div class="feed" id="feed">.*?</div>\s*<div class="feed-actions">.*?</div>', FEED, re.S).group(0)
QUOTES = re.search(r'<section id="quotes".*?</section>', rd("index.html"), re.S).group(0)
out = {}

# news/
out["news/index.html"] = shell("/news/", "Latest market and world news | Market Plus",
  "Live headlines on markets, gold, forex, world, politics and Ukraine from open news sources and @MarketPulseGold, updated every 30 minutes.",
  page_head("news.h", "Latest news", "news.sub", "nav.news") + "\n" + QUOTES + f'\n<section class="pfeed"><div class="wrap">\n  {FEED}\n</div></section>', "news",
  jsonld={"@context": "https://schema.org", "@graph": [{"@type": "CollectionPage", "name": "News — Market Plus", "url": SITE + "/news/", "publisher": PUB}, crumbs_ld([("Market Plus", "/"), ("News", "/news/")])]})

# analysis/
rel_guide = [g for g in GUIDES if g["slug"] == "how-to-keep-a-trading-journal"]
out["analysis/index.html"] = shell("/analysis/", "Market analysis and explainers: gold, forex, crypto, stocks | Market Plus",
  "Plain-language explainers on what moves gold, how forex quotes work, crypto market basics and how stock indices are built. Educational only.",
  page_head("pg.analysis.h", T_EN["pg.analysis.h"], "pg.analysis.sub", "nav.analysis") +
  f'\n<section class="psec"><div class="wrap">{grid(EXPL[:1], "feature")}{grid(EXPL[1:] + rel_guide)}</div></section>', "analysis",
  jsonld={"@context": "https://schema.org", "@graph": [{"@type": "CollectionPage", "name": "Analysis — Market Plus", "url": SITE + "/analysis/", "publisher": PUB,
    "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": SITE + a["url"], "name": a["h1"]} for i, a in enumerate(EXPL + rel_guide)]}},
    crumbs_ld([("Market Plus", "/"), ("Analysis", "/analysis/")])]})

# analysis articles
for e in EXPL:
    rel = [o for o in EXPL if o is not e][:2] + rel_guide
    art = f'''<div class="read-progress" aria-hidden="true"><span></span></div>
<article class="wrap guide article" lang="en">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="/" translate="no">Market Plus</a> › <a href="/analysis/">Analysis</a></nav>
  <span class="kicker">{esc(e["kicker"])}</span>
  <h1>{esc(e["h1"])}</h1>
  <p class="dek">{esc(e["card"])}</p>
  <p class="upd">Published {DATE_H} · {e["mins"]} min read</p>
  <div class="art-body">
{e["body"]}
  </div>
  <aside class="cta-box"><p class="cta-h">Follow the headlines</p><p>Market Plus collects headlines on gold, currencies, oil and macro from open sources, with the original one tap away.</p><div class="cta"><a class="btn btn-gold" href="/markets/">Markets</a><a class="btn btn-ghost" href="/news/">Latest news</a></div></aside>
</article>
<section class="related wrap"><h2>Related articles</h2>{grid(rel)}</section>'''
    ld = {"@context": "https://schema.org", "@graph": [{"@type": "Article", "headline": e["title"], "description": e["desc"], "datePublished": DATE, "dateModified": DATE,
          "inLanguage": "en", "wordCount": words(e["body"]), "mainEntityOfPage": {"@type": "WebPage", "@id": SITE + e["url"]},
          "author": {"@type": "Organization", "name": "Market Plus", "url": SITE + "/"}, "publisher": PUB},
          crumbs_ld([("Market Plus", "/"), ("Analysis", "/analysis/"), (e["h1"], e["url"])])]}
    out[e["url"].lstrip("/")] = shell(e["url"], e["title"] + " | Market Plus", e["desc"], art, "analysis", "article", ld,
                                      extra=f'\n<meta property="article:published_time" content="{DATE}">')

# markets/
MK = [("gold", "mk.gold.h", "mk.gold.p", EXPL[0]), ("forex", "mk.fx.h", "mk.fx.p", EXPL[1]), ("crypto", "mk.crypto.h", "mk.crypto.p", EXPL[2]), ("stocks", "mk.stocks.h", "mk.stocks.p", EXPL[3])]
mk = "".join(f'<article class="mcard" id="{i}"><span class="msym" lang="en" translate="no">{e["sym"]}</span><h2 data-i18n="{h}">{esc(T_EN[h])}</h2>{k(p, "p")}'
             f'<a class="mlink" href="{e["url"]}" data-i18n="mk.read">{esc(T_EN["mk.read"])}</a></article>' for i, h, p, e in MK)
feed_m = FEED.replace('<div class="nlist" id="newsList"', '<div class="nlist" id="newsList" data-tab="market"')
out["markets/index.html"] = shell("/markets/", "Markets: gold (XAU/USD), forex, crypto and stocks | Market Plus",
  "Gold (XAU/USD), forex, crypto and stocks on Market Plus: a quotes strip, market headlines from open sources and plain-English explainers.",
  page_head("nav.markets", "Markets", "pg.markets.sub", "nav.markets") + "\n" + QUOTES +
  f'\n<section class="psec"><div class="wrap"><div class="mgrid">{mk}</div></div></section>'
  f'\n<section class="pfeed" id="headlines"><div class="wrap"><h2 data-i18n="mk.news.h">{T_EN["mk.news.h"]}</h2>\n  {feed_m}\n</div></section>', "markets",
  jsonld={"@context": "https://schema.org", "@graph": [{"@type": "CollectionPage", "name": "Markets — Market Plus", "url": SITE + "/markets/", "publisher": PUB}, crumbs_ld([("Market Plus", "/"), ("Markets", "/markets/")])]})

# planners/
plan_g = [g for g in GUIDES if g["slug"] != "how-to-keep-a-trading-journal"]
out["planners/index.html"] = shell("/planners/", "Digital planners and templates by MarketPulseStudio | Market Plus",
  "Digital planners and templates for budgets, goals, savings and trading journals: the MarketPulseStudio shop on Etsy and templates on Patreon.",
  page_head("pg.planners.h", T_EN["pg.planners.h"], "pg.planners.sub", "nav.planners") +
  f'''\n<section class="psec"><div class="wrap"><div class="etsy">
  <div><span class="kicker" lang="en" translate="no">Etsy · MarketPulseStudio</span><h2 data-i18n="pl.etsy.h">{T_EN["pl.etsy.h"]}</h2>{k("pl.etsy.p", "p")}</div>
  <a class="btn btn-gold" href="https://marketpulsestudio.etsy.com" target="_blank" rel="noopener" data-i18n="pl.etsy.btn">{T_EN["pl.etsy.btn"]}</a>
</div></div></section>
<section id="products"><div class="wrap">
  <h2 data-i18n="pl.more.h">{T_EN["pl.more.h"]}</h2>
  <p class="sub" data-i18n="prod.sub">Tools for trading, personal finance and business. Payment and download on Patreon.</p>
  <div class="products" id="productList"></div>
  <p class="note" data-i18n="prod.note">Buttons open Patreon or GitHub pages. This site does not collect or store any data.</p>
</div></section>
<section class="psec"><div class="wrap"><h2 data-i18n="nav.guides">Guides</h2>{grid(plan_g)}</div></section>''', "planners",
  jsonld={"@context": "https://schema.org", "@graph": [{"@type": "CollectionPage", "name": "Planners — Market Plus", "url": SITE + "/planners/", "publisher": PUB}, crumbs_ld([("Market Plus", "/"), ("Planners", "/planners/")])]})

# about/
about_tiles = re.search(r'<div class="about">.*?</div>\s*</div>\s*</div>', rd("index.html"), re.S)
out["about/index.html"] = shell("/about/", "About Market Plus and contact | Market Plus",
  "About Market Plus: market and world news with context, explainers and planning templates. Contact Market Plus on X @MarketPulseGold.",
  page_head("pg.about.h", T_EN["pg.about.h"], "about.sub", "nav.about").replace('data-i18n="about.sub">', 'data-i18n="about.sub">Market Plus is a markets news project for people who want the signal, not the noise.', 1) +
  f'''\n<section class="psec"><div class="wrap">{about_tiles.group(0) if about_tiles else ""}</div></section>
<section class="psec"><div class="wrap"><div class="etsy contact">
  <div><h2 data-i18n="ab.contact.h">{T_EN["ab.contact.h"]}</h2>{k("ab.contact.p", "p")}<p class="fpriv" data-i18n="foot.priv">No trackers, no forms, no data collection.</p></div>
  <a class="btn btn-gold" href="https://x.com/MarketPulseGold" target="_blank" rel="noopener"><span data-i18n="ab.contact.btn">{T_EN["ab.contact.btn"]}</span> <span lang="en" translate="no">@MarketPulseGold</span></a>
</div></div></section>''', "about",
  jsonld={"@context": "https://schema.org", "@graph": [{"@type": "AboutPage", "name": "About — Market Plus", "url": SITE + "/about/", "publisher": PUB}, crumbs_ld([("Market Plus", "/"), ("About", "/about/")])]})

for p, s in out.items():  # shared header/footer, active section in the nav
    wr(p, apply_layout(s, p.split("/")[0]))

# ---------- home page blocks ----------
idx = rd("index.html")
latest = (f'<!--mp:latest--><section id="latest" class="latest"><div class="wrap"><div class="shead"><div><h2 data-i18n="home.lat.h">{T_EN["home.lat.h"]}</h2>'
          f'{k("home.lat.sub", "p", "sub")}</div><a class="more" href="/analysis/" data-i18n="art.all">{T_EN["art.all"]}</a></div>'
          f'{grid(EXPL[:1] + GUIDES[:1], "feature2")}{grid(EXPL[1:] + GUIDES[1:4])}</div></section><!--/mp:latest-->')
SEC = [("/news/", "nav.news", "News", "sec.news.d", "N"), ("/analysis/", "nav.analysis", "Analysis", "sec.analysis.d", "A"),
       ("/markets/", "nav.markets", "Markets", "sec.markets.d", "M"), ("/planners/", "nav.planners", "Planners", "sec.planners.d", "P")]
secs = "".join(f'<a class="scard" href="{u}"><span class="sicon" aria-hidden="true">{ic}</span><h3 data-i18n="{h}">{T_EN.get(h, he)}</h3>{k(d, "p")}<span class="mlink" data-i18n="sec.open">{T_EN["sec.open"]}</span></a>' for u, h, he, d, ic in SEC)
sections = (f'<!--mp:sections--><section id="sections" class="sections"><div class="wrap"><h2 data-i18n="home.sec.h">{T_EN["home.sec.h"]}</h2>'
            f'{k("home.sec.sub", "p", "sub")}<div class="sgrid">{secs}</div></div></section><!--/mp:sections-->')
idx = re.sub(r'<!--mp:latest-->.*?<!--/mp:latest-->\n*', '', idx, flags=re.S)
idx = re.sub(r'<!--mp:sections-->.*?<!--/mp:sections-->\n*', '', idx, flags=re.S)
idx = idx.replace('<section id="news">', latest + '\n\n<section id="news">', 1)
idx = idx.replace('<section id="products">', sections + '\n\n<section id="products">', 1)
if 'class="hero-fx"' not in idx:
    idx = idx.replace('<section class="hero"><div class="wrap">', '<section class="hero"><canvas class="hero-fx" aria-hidden="true"></canvas><div class="wrap">', 1)
idx = re.sub(r"\n{3,}", "\n\n", idx)
wr("index.html", apply_layout(idx, "home"))
for p in ["terms.html", "404.html"]:
    wr(p, apply_layout(rd(p)))
for p in glob.glob(os.path.join(ROOT, "guides", "**", "*.html"), recursive=True):
    r = os.path.relpath(p, ROOT); wr(r, apply_layout(rd(r), "guides"))

# ---------- app.js: extra translations ----------
app = rd("app.js")
blk = "  /*TX-START*/ var TX = " + json.dumps(TX, ensure_ascii=False, separators=(",", ":")) + ";\n  Object.keys(TX).forEach(function (l) { if (T[l]) for (var k in TX[l]) T[l][k] = TX[l][k]; }); /*TX-END*/\n"
app = re.sub(r"  /\*TX-START\*/.*?/\*TX-END\*/\n", "", app, flags=re.S)
app = app.replace("\n  var PRODUCTS = [", "\n" + blk + "  var PRODUCTS = [", 1)
wr("app.js", app)

# ---------- sitemap ----------
sm = rd("sitemap.xml")
add = "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{DATE}</lastmod><changefreq>{c}</changefreq><priority>{pr}</priority></url>\n"
              for u, c, pr in EXTRA_URLS if f"<loc>{SITE}{u}</loc>" not in sm)
wr("sitemap.xml", sm.replace("</urlset>", add + "</urlset>"))
print("pages:", len(out), "| articles:", len(EXPL), "| guides:", len(GUIDES))
