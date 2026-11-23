#!/usr/bin/env python3
"""Final SEO pass for Market Plus. Run LAST (extras_build.py calls it at the end).
Idempotent: normalises asset versions and head tags, fixes canonical/hreflang on home and terms,
adds JSON-LD (WebSite/Organization, Product offers, FAQPage), and rewrites robots.txt and sitemap.xml
from the indexable HTML files. No trackers, no forms."""
import glob, html as H, json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "extras_src"))
from catalog import P as CATALOG
SITE = "https://marketplus-news.github.io"
APPV = "1792970000"; CSSV = "4"; SITEJS = "1"
TODAY = os.environ.get("SEO_DATE") or subprocess.run(["date", "+%Y-%m-%d"], capture_output=True, text=True).stdout.strip()
OGIMG = SITE + "/assets/og-image.jpg"
ORG = {"@type": "Organization", "@id": SITE + "/#org", "name": "Market Plus", "url": SITE + "/",
       "logo": {"@type": "ImageObject", "url": SITE + "/favicon.svg"},
       "sameAs": ["https://marketpulsestudio.etsy.com", "https://github.com/aiskillsdrop/ai-skills-for-business"]}
SKIP = re.compile(r"^(tools/(guides_src|site_src|extras_src)/|node_modules/|googlea|404\.html)")
# pages whose head is not produced by a Python builder: title, description (<=60 / <=155)
META = {
 "index.html": ("Market Plus: Market News, Free Money Calculators & Guides",
   "Live market and world news plus free calculators and plain-English guides: Christmas budget, debt payoff, savings, Airbnb profit, Hyrox and position size."),
 "terms.html": ("Terms of Use | Market Plus",
   "Terms of use for Market Plus: informational content only, not investment advice, third-party links and digital template purchases."),
 "shop-crypto.html": ("Buy Templates with USDC (Crypto) | Market Plus",
   "Buy the Hyrox Race-Prep System and STR Host System templates with USDC on Base. Instant download after payment, or buy the same templates on Etsy."),
}

def rd(p): return open(os.path.join(ROOT, p), encoding="utf-8").read()
def wr(p, s):
    fp = os.path.join(ROOT, p)
    if open(fp, encoding="utf-8").read() != s:
        open(fp, "w", encoding="utf-8").write(s)
def esc(s): return H.escape(H.unescape(s), quote=True).replace("&#x27;", "'")
def pages():
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True)):
        r = os.path.relpath(f, ROOT)
        if not SKIP.match(r): out.append(r)
    return out
def url_of(r): return SITE + "/" + (r[:-10] if r.endswith("index.html") else r)

def set_meta(s, attr, key, val):
    tag = f'<meta {attr}="{key}" content="{esc(val)}">'
    pat = re.compile(r'<meta %s="%s" content="[^"]*">' % (attr, re.escape(key)))
    return pat.sub(lambda m: tag, s, count=1) if pat.search(s) else s.replace("</title>", "</title>\n" + tag, 1)

def dedupe(s, attr, key):
    pat = re.compile(r'\n?<meta %s="%s" content="[^"]*">' % (attr, re.escape(key)))
    seen = [0]
    def f(m):
        seen[0] += 1
        return m.group(0) if seen[0] == 1 else ""
    return pat.sub(f, s)

def set_ld(s, key, obj):
    """one managed JSON-LD block per key, placed before </head>"""
    s = re.sub(r'\n?<script type="application/ld\+json" data-seo="%s">.*?</script>' % key, "", s, flags=re.S)
    if obj is None: return s
    blk = f'<script type="application/ld+json" data-seo="{key}">{json.dumps(obj, ensure_ascii=False)}</script>'
    return s.replace("</head>", blk + "\n</head>", 1)

def strip_tags(x): return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", "", x))).strip()

FAQ_H = re.compile(r"<h2[^>]*>\s*(FAQ|Frequently asked questions|Questions fréquentes|Häufige Fragen|Частые вопросы|Часті запитання|常见问题|常见问答)\s*</h2>(.*?)(?=<h2|</section>|</article>|<div class=\"cta-box|<section|<div class=\"next|<!--mp:next)", re.S | re.I)
def faq_ld(s, r):
    if '"FAQPage"' in re.sub(r'<script type="application/ld\+json" data-seo="faq">.*?</script>', "", s, flags=re.S):
        return set_ld(s, "faq", None)  # page already has its own FAQPage (tools)
    m = FAQ_H.search(s)
    if not m: return set_ld(s, "faq", None)
    qa = re.findall(r"<h3[^>]*>(.*?)</h3>\s*((?:<p[^>]*>.*?</p>\s*|<ul>.*?</ul>\s*|<ol>.*?</ol>\s*)+)", m.group(2), re.S)
    if len(qa) < 2: return set_ld(s, "faq", None)
    lang = (re.search(r'<html lang="([^"]+)"', s) or [None, "en"])[1]
    return set_ld(s, "faq", {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": lang, "url": url_of(r),
        "mainEntity": [{"@type": "Question", "name": strip_tags(q), "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in qa]})

def price(p): return re.sub(r"[^0-9.]", "", p)
def product(name, desc, img, p, url, sku=None):
    o = {"@type": "Product", "name": name, "description": desc, "image": SITE + "/" + img.lstrip("/"),
         "brand": {"@type": "Brand", "name": "MarketPulseStudio"}, "category": "Digital template",
         "offers": {"@type": "Offer", "price": price(p), "priceCurrency": "USD", "availability": "https://schema.org/InStock", "url": url,
                    "itemCondition": "https://schema.org/NewCondition"}}
    if sku: o["sku"] = str(sku)
    return o
def crumbs(items):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items)]}

def common(s, r):
    # asset versions (one source of truth) and tools.css everywhere the shared layout is used
    s = re.sub(r'(app\.js)\?v=\d+', r'\1?v=' + APPV, s)
    s = re.sub(r'(/assets/site\.js)\?v=\d+', r'\1?v=' + SITEJS, s)
    s = re.sub(r'(/assets/tools\.css)\?v=\d+', r'\1?v=' + CSSV, s)
    if "/assets/site.css" in s and "/assets/tools.css" not in s:
        s = re.sub(r'(<link rel="stylesheet" href="/assets/site\.css\?v=\d+">)', r'\1' + f'\n<link rel="stylesheet" href="/assets/tools.css?v={CSSV}">', s, count=1)
    # one og:image / size / twitter:image (earlier passes left duplicates on guides)
    for a, k in (("property", "og:image"), ("property", "og:image:width"), ("property", "og:image:height"), ("name", "twitter:image")):
        s = dedupe(s, a, k)
    og = re.search(r'<meta property="og:image" content="([^"]+)">', s)
    if og and og.group(1) == OGIMG:
        s = re.sub(r'<meta property="og:image:width" content="\d+">', '<meta property="og:image:width" content="1200">', s)
        s = re.sub(r'<meta property="og:image:height" content="\d+">', '<meta property="og:image:height" content="630">', s)
        if "og:image:width" not in s:
            s = s.replace(og.group(0), og.group(0) + '\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n<meta property="og:image:alt" content="Market Plus">', 1)
        s = set_meta(s, "name", "twitter:image", OGIMG)
    if 'name="twitter:card"' not in s and og:
        s = s.replace(og.group(0), og.group(0) + '\n<meta name="twitter:card" content="summary_large_image">', 1)
    return s

def apply_meta(s, r, title, desc):
    s = re.sub(r"<title>.*?</title>", "<title>" + esc(title) + "</title>", s, count=1, flags=re.S)
    s = set_meta(s, "name", "description", desc)
    for a, k, v in (("property", "og:title", title), ("property", "og:description", desc), ("name", "twitter:title", title), ("name", "twitter:description", desc), ("property", "og:url", url_of(r))):
        s = set_meta(s, a, k, v)
    return s

def canon_only(s, r):
    """client-side ?lang= variants are not separate pages: self canonical, no hreflang to ?lang URLs"""
    s = re.sub(r'\n?<link rel="alternate" hreflang="[^"]+" href="[^"]*\?lang=[^"]*">', "", s)
    s = re.sub(r'\n?<link rel="alternate" hreflang="x-default" href="[^"]*">', "", s) if "hreflang=\"en\"" not in s else s
    if 'rel="canonical"' not in s:
        s = re.sub(r'(<meta name="description" content="[^"]*">)', r'\1' + f'\n<link rel="canonical" href="{url_of(r)}">', s, count=1)
    return s

USDC_BTN = '    <a class="pbtn" href="/shop-crypto.html" lang="en" translate="no">Buy with USDC</a>\n'
def page_specific(s, r):
    if r in META: s = apply_meta(s, r, *META[r])
    if r == "index.html":
        s = canon_only(s, r)
        if 'href="/shop-crypto.html" lang="en" translate="no">Buy with USDC' not in s:
            s = re.sub(r'(    <a class="pbtn" href="https://marketpulsestudio\.etsy\.com")', lambda m: USDC_BTN + m.group(1), s, count=1)
        s = set_ld(s, "site", {"@context": "https://schema.org", "@graph": [
            {"@type": "WebSite", "@id": SITE + "/#website", "name": "Market Plus", "url": SITE + "/", "inLanguage": ["en", "ru", "uk", "fr", "de", "zh-Hans"],
             "description": META[r][1], "publisher": {"@id": SITE + "/#org"}}, ORG]})
    elif r == "terms.html":
        s = canon_only(s, r)
        s = re.sub(r"<body(?![^>]*data-static-meta)([^>]*)>", r"<body\1 data-static-meta>", s, count=1)
        s = set_ld(s, "page", {"@context": "https://schema.org", "@graph": [{"@type": "WebPage", "name": META[r][0], "url": url_of(r), "publisher": {"@id": SITE + "/#org"}},
                   crumbs([("Market Plus", "/"), ("Terms of Use", "/terms.html")])]})
    elif r == "shop-crypto.html":
        s = re.sub(r"<body(?![^>]*data-static-meta)([^>]*)>", r"<body\1 data-static-meta>", s, count=1)
        feat = [p for p in CATALOG if p.get("cat") == "featured"]
        s = set_ld(s, "page", {"@context": "https://schema.org", "@graph": [
            {"@type": "CollectionPage", "name": META[r][0], "url": url_of(r), "publisher": {"@id": SITE + "/#org"},
             "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": product(p["title"], p["desc"], p["img"], p["price"], url_of(r))} for i, p in enumerate(feat)]}},
            crumbs([("Market Plus", "/"), ("Crypto Shop", "/shop-crypto.html")])]})
    elif r == "planners/index.html":
        items = [p for p in CATALOG if not p.get("free") and p.get("price")]
        lst = []
        for p in items:
            url = p.get("etsy") or ("https://www.etsy.com/listing/%s" % p["id"]) if p.get("id") or p.get("etsy") else p["url"]
            img = p.get("img") or "assets/products/%s.webp" % p["id"]
            lst.append(product(p["title"], p["desc"], img, p["price"], url, p.get("id")))
        s = set_ld(s, "page", {"@context": "https://schema.org", "@type": "ItemList", "name": "MarketPulseStudio templates", "numberOfItems": len(lst),
                   "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": o} for i, o in enumerate(lst)]})
    return s

# ---------- run over pages ----------
changed = []
for r in pages():
    s0 = rd(r); s = common(s0, r); s = page_specific(s, r)
    if r.startswith(("guides/", "analysis/")): s = faq_ld(s, r)
    if s != s0: wr(r, s); changed.append(r)

# ---------- robots.txt ----------
wr_robots = """User-agent: *
Allow: /
Disallow: /tools/guides_src/
Disallow: /tools/site_src/
Disallow: /tools/extras_src/
Disallow: /tools/*.py$

Sitemap: https://marketplus-news.github.io/sitemap.xml
"""
open(os.path.join(ROOT, "robots.txt"), "w").write(wr_robots)

# ---------- sitemap.xml: every indexable page, lastmod, language alternates ----------
def lastmod(r):
    st = subprocess.run(["git", "status", "--porcelain", "--", r], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    if st: return TODAY
    d = subprocess.run(["git", "log", "-1", "--format=%cs", "--", r], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    return d or TODAY
def prio(r):
    if r == "index.html": return "1.0", "hourly"
    if r == "news/index.html": return "0.9", "hourly"
    if r.startswith("tools/"): return ("0.9" if r == "tools/index.html" else "0.8"), "monthly"
    if r == "guides/how-to-plan-christmas-budget-2026.html": return "0.9", "weekly"
    if r.endswith("index.html"): return "0.8", "weekly"
    if r in ("about/index.html", "terms.html"): return "0.3", "yearly"
    return "0.7", "monthly"
prev = {}
for m in re.finditer(r"<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>", rd("sitemap.xml")):
    prev[m.group(1)] = m.group(2)
rows = []
for r in pages():
    s = rd(r)
    if re.search(r'<meta name="robots" content="[^"]*noindex', s): continue
    can = re.search(r'<link rel="canonical" href="([^"]+)">', s)
    if not can or can.group(1) != url_of(r): continue
    alts = re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)">', s)
    pr, cf = prio(r)
    if r in ("about/index.html", "terms.html"): pr, cf = "0.3", "yearly"
    x = f"  <url>\n    <loc>{url_of(r)}</loc>\n    <lastmod>{lastmod(r)}</lastmod>\n    <changefreq>{cf}</changefreq>\n    <priority>{pr}</priority>\n"
    x += "".join(f'    <xhtml:link rel="alternate" hreflang="{h}" href="{u}"/>\n' for h, u in alts)
    rows.append(x + "  </url>\n")
sm = ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
      + "".join(rows) + "</urlset>\n")
open(os.path.join(ROOT, "sitemap.xml"), "w").write(sm)
print("seo: pages changed", len(changed), "| sitemap urls", len(rows))
