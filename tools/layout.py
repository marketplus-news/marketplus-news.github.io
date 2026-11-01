# Shared Market Plus layout: sticky header with sections + mobile menu, footer, site.css/site.js.
# apply_layout(html) is idempotent and is used by tools/site_build.py and tools/guides_src/build.py.
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
TX = json.load(open(os.path.join(HERE, "site_src", "i18n_extra.json"), encoding="utf-8"))
ASSET_V = "1"
X_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M18.2 2.3h3.4l-7.4 8.4 8.7 11.5h-6.8l-5.3-7-6.1 7H1.3l7.9-9L.9 2.3h7l4.8 6.4 5.5-6.4Zm-1.2 17.9h1.9L7 4.2H5Z"/></svg>'
# extra/sections pages listed in sitemap.xml (path, changefreq, priority)
EXTRA_URLS = [("/news/", "hourly", "0.9"), ("/analysis/", "weekly", "0.8"), ("/markets/", "daily", "0.8"),
              ("/planners/", "weekly", "0.8"), ("/about/", "yearly", "0.4"),
              ("/analysis/what-moves-gold-prices.html", "monthly", "0.7"), ("/analysis/how-forex-quotes-work.html", "monthly", "0.7"),
              ("/analysis/crypto-market-basics.html", "monthly", "0.7"), ("/analysis/how-stock-indices-work.html", "monthly", "0.7")]
HEAD_JS = ('<script>/* js flag + mobile menu (works even if site.js fails) */(function(d){var h=d.documentElement;h.classList.add("js");'
  'function s(o){h.classList.toggle("nav-open",o);var m=d.getElementById("menuBtn");if(m)m.setAttribute("aria-expanded",o?"true":"false")}'
  'd.addEventListener("click",function(e){var t=e.target;if(!t.closest)return;if(t.closest("#menuBtn")){s(!h.classList.contains("nav-open"))}'
  'else if(h.classList.contains("nav-open")&&(t.closest("#mainNav a")||!t.closest("header.top")))s(false)});'
  'd.addEventListener("keydown",function(e){if(e.key==="Escape"&&h.classList.contains("nav-open"))s(false)})})(document)</script>')
NAV = [("news", "/news/", "nav.news"), ("analysis", "/analysis/", "nav.analysis"), ("markets", "/markets/", "nav.markets"),
       ("planners", "/planners/", "nav.planners"), ("guides", "/guides/", "nav.guides"), ("about", "/about/", "nav.about")]
BASE_LABELS = {"nav.news": "News", "nav.guides": "Guides", "nav.about": "About", "nav.products": "Products",
               "foot.na": "Not investment advice.", "foot.disc": "All content is for informational purposes only. Trading in financial markets involves risk of loss.",
               "foot.rights": "All rights reserved.", "foot.terms": "Terms of Use", "foot.priv": "No trackers, no forms, no data collection."}

def _grab(html, key, default):
    m = re.search(r'data-i18n="%s"[^>]*>([^<]*)<' % re.escape(key), html)
    return m.group(1) if m else default

def _lang(html):
    m = re.search(r'data-page-lang="([a-z]+)"', html)
    return m.group(1) if m else "en"

ABOUT = {"en": "About", "ru": "О проекте", "uk": "Про проєкт", "fr": "À propos", "de": "Über uns", "zh": "关于"}
def label(html, lang, k):
    v = _grab(html, k, None)
    if v: return v
    if k == "nav.about": return ABOUT.get(lang, "About")
    return TX.get(lang, TX["en"]).get(k) or TX["en"].get(k) or BASE_LABELS.get(k, k)

def header(html, lang, active):
    t = lambda k: label(html, lang, k)
    lab = {k: t(k) for _, _, k in NAV}
    m = re.search(r'<div class="lang-dd" id="langDD">.*?</ul>\s*</div>', html, re.S)
    if not m:  # new pages: same language dropdown as the home page
        m = re.search(r'<div class="lang-dd" id="langDD">.*?</ul>\s*</div>', open(os.path.join(os.path.dirname(HERE), "index.html"), encoding="utf-8").read(), re.S)
    dd = m.group(0) if m else ""
    guides_href = "/guides/" if lang == "en" else "/guides/%s/" % lang
    links = "\n".join('    <a href="%s" data-nav="%s" data-i18n="%s"%s>%s</a>' % (
        guides_href if n == "guides" else h, n, k, ' aria-current="page"' if n == active else "", lab[k]) for n, h, k in NAV)
    return f'''<header class="top"><div class="wrap">
  <div class="brand">
    <a class="logo" href="/"><img src="/favicon.svg" alt="" width="30" height="30"><span lang="en" translate="no">Market <b>Plus</b></span></a>
    {dd}
  </div>
  <button type="button" class="menu-btn" id="menuBtn" aria-controls="mainNav" aria-expanded="false"><span class="bars" aria-hidden="true"></span><span class="sr-only" data-i18n="nav.menu">{t("nav.menu")}</span></button>
  <nav class="main" id="mainNav" aria-label="Main" data-i18n-aria="nav.aria">
{links}
    <a class="pbtn" href="https://www.patreon.com/DmitryZhuk" target="_blank" rel="noopener" lang="en" translate="no">Patreon</a>
    <a class="xbtn" href="https://x.com/MarketPulseGold" target="_blank" rel="noopener" aria-label="X">{X_SVG}</a>
  </nav>
</div></header>'''

def footer(html, lang):
    g = lambda k: _grab(html, k, BASE_LABELS[k])
    t = lab = lambda k: label(html, lang, k)
    guides_href = "/guides/" if lang == "en" else "/guides/%s/" % lang
    return f'''<footer><div class="wrap">
  <div class="fgrid">
    <div class="fbrand"><a class="logo" href="/"><img src="/favicon.svg" alt="" width="26" height="26"><span lang="en" translate="no">Market <b>Plus</b></span></a>
      <p class="disc"><b data-i18n="foot.na">{g("foot.na")}</b> <span data-i18n="foot.disc">{g("foot.disc")}</span></p></div>
    <nav class="fcol" aria-label="Sections"><a href="/news/" data-i18n="nav.news">{lab("nav.news")}</a><a href="/analysis/" data-i18n="nav.analysis">{t("nav.analysis")}</a><a href="/markets/" data-i18n="nav.markets">{t("nav.markets")}</a><a href="/planners/" data-i18n="nav.planners">{t("nav.planners")}</a><a href="{guides_href}" data-i18n="nav.guides">{lab("nav.guides")}</a><a href="/about/" data-i18n="nav.about">{lab("nav.about")}</a></nav>
    <div class="flinks" lang="en" translate="no"><a href="https://x.com/MarketPulseGold" target="_blank" rel="noopener">X</a><a href="https://www.patreon.com/DmitryZhuk" target="_blank" rel="noopener">Patreon</a><a href="https://marketpulsestudio.etsy.com" target="_blank" rel="noopener">Etsy</a><a href="https://github.com/aiskillsdrop/ai-skills-for-business" target="_blank" rel="noopener">GitHub</a></div>
  </div>
  <div class="fcopy">© <span id="yr">2026</span> <span lang="en" translate="no">Market Plus</span>. <span data-i18n="foot.rights">{g("foot.rights")}</span> · <a href="/terms.html" data-i18n="foot.terms">{g("foot.terms")}</a></div>
  <div class="fpriv" data-i18n="foot.priv">{g("foot.priv")}</div>
</div></footer>'''

def apply_layout(html, active=None):
    lang = _lang(html)
    html = re.sub(r'<header class="top">.*?</header>', lambda m: header(html, lang, active), html, count=1, flags=re.S)
    html = re.sub(r'<footer>.*?</footer>', lambda m: footer(html, lang), html, count=1, flags=re.S)
    if "/assets/site.css" not in html:
        html = re.sub(r'(<link rel="stylesheet" href="[^"]*style\.css[^"]*">)',
                      lambda m: m.group(1) + f'\n<link rel="preload" href="/assets/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>\n<link rel="stylesheet" href="/assets/site.css?v={ASSET_V}">\n' + HEAD_JS, html, count=1)
    if "/assets/site.js" not in html:
        html = re.sub(r'(<script src="[^"]*app\.js[^"]*" defer></script>)', lambda m: m.group(1) + f'\n<script src="/assets/site.js?v={ASSET_V}" defer></script>', html, count=1)
    if active:
        html = re.sub(r'<body(?![^>]*data-nav=)', f'<body data-nav="{active}"', html, count=1)
    return html
