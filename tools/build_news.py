#!/usr/bin/env python3
"""Market Plus news builder (stdlib only).

Fetches free, open RSS feeds (+ @MarketPulseGold posts from a keyless public
source when one works), assigns sections, dedups and writes data/news.json.
X posts are also kept in data/posts.json (last good copy is reused when every
keyless X source fails, and tools/update_posts.py can refresh it manually).
If a feed fails, its items from the previous news.json are kept.

Headlines (and X posts) are machine-translated into the site languages at build
time with free, keyless public endpoints (Google "dict-chrome-ex"/"gtx" web
clients, MyMemory as last resort). Translations are stored per item as
item["t"] = {"uk": ..., "ru": ...} and cached by url / post id, so each run only
translates new headlines. Failures never break the build: the frontend simply
shows the original title.
"""
import email.utils, html, json, os, re, sys, time, urllib.request, urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEWS = os.path.join(ROOT, "data", "news.json")
POSTS = os.path.join(ROOT, "data", "posts.json")
UA = "Mozilla/5.0 (compatible; MarketPlusNews/1.0; +https://marketplus-news.github.io/)"
X_HANDLE = "MarketPulseGold"
PER_SECTION = 30
PER_SOURCE_IN_SECTION = 8
MAX_AGE_H = 72

def gn(q):
    return "https://news.google.com/rss/search?" + urllib.parse.urlencode(
        {"q": q, "hl": "en-US", "gl": "US", "ceid": "US:en"})

# key, display name, url, default section(s), use keyword fallback
FEEDS = [
    ("cnbc_markets", "CNBC", "https://www.cnbc.com/id/10000664/device/rss/rss.html", ["market"], False),
    ("cnbc_top", "CNBC", "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114", ["market"], True),
    ("mw_top", "MarketWatch", "https://feeds.content.dowjones.io/public/rss/mw_topstories", ["market"], False),
    ("investing", "Investing.com", "https://www.investing.com/rss/news.rss", ["market"], False),
    ("investing_comm", "Investing.com", "https://www.investing.com/rss/news_11.rss", ["market"], False),
    ("bbc_business", "BBC", "https://feeds.bbci.co.uk/news/business/rss.xml", ["market"], False),
    ("guardian_business", "The Guardian", "https://www.theguardian.com/uk/business/rss", ["market"], False),
    ("dw_business", "DW", "https://rss.dw.com/rdf/rss-en-bus", ["market"], False),
    ("npr_business", "NPR", "https://feeds.npr.org/1006/rss.xml", ["market"], False),
    ("reuters_markets", "Reuters", gn("site:reuters.com/markets when:2d"), ["market"], False),
    ("reuters_business", "Reuters", gn("site:reuters.com/business when:2d"), ["market"], False),
    ("reuters_world", "Reuters", gn("site:reuters.com/world when:2d"), ["world"], True),
    ("ap", "AP News", gn("site:apnews.com when:2d"), ["world"], True),
    ("bbc_world", "BBC", "https://feeds.bbci.co.uk/news/world/rss.xml", ["world"], True),
    ("aljazeera", "Al Jazeera", "https://www.aljazeera.com/xml/rss/all.xml", ["world"], True),
    ("guardian_world", "The Guardian", "https://www.theguardian.com/world/rss", ["world"], True),
    ("dw_world", "DW", "https://rss.dw.com/rdf/rss-en-world", ["world"], True),
    ("france24", "France 24", "https://www.france24.com/en/rss", ["world"], True),
    ("npr_world", "NPR", "https://feeds.npr.org/1004/rss.xml", ["world"], True),
    ("bbc_politics", "BBC", "https://feeds.bbci.co.uk/news/politics/rss.xml", ["politics"], False),
    ("guardian_politics", "The Guardian", "https://www.theguardian.com/politics/rss", ["politics"], False),
    ("npr_politics", "NPR", "https://feeds.npr.org/1014/rss.xml", ["politics"], False),
    ("kyiv_independent", "The Kyiv Independent", "https://kyivindependent.com/news-archive/rss/", ["ukraine"], False),
    ("pravda_en", "Ukrainska Pravda", "https://www.pravda.com.ua/eng/rss/", ["ukraine"], False),
    ("ukrinform", "Ukrinform", "https://www.ukrinform.net/rss/block-lastnews", ["ukraine"], False),
    ("guardian_ukraine", "The Guardian", "https://www.theguardian.com/world/ukraine/rss", ["ukraine"], False),
]

KW = {
    "ukraine": r"\b(ukrain\w*|kyiv|kiev|zelensk\w*|kharkiv|odesa|odessa|donbas\w*|donetsk|zaporizh\w*|crimea\w*|kherson)\b",
    "market": r"\b(stocks?|shares|markets?|wall street|s&p|nasdaq|dow|oil|crude|brent|gold|silver|bitcoin|crypto\w*|fed|federal reserve|ecb|central bank|interest rates?|rate cut|inflation|cpi|gdp|recession|bonds?|yields?|treasur\w+|dollar|euro|yen|currenc\w+|earnings|profit|tariffs?|economy|economic|opec)\b",
    "politics": r"\b(elections?|vote[sd]?|voting|parliament\w*|senate|congress|lawmakers?|prime minister|president\w*|minister|government|cabinet|party|campaign|referendum|white house|kremlin|downing street|supreme court|impeach\w*|coalition)\b",
}
KWC = {k: re.compile(v, re.I) for k, v in KW.items()}

def fetch(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/rss+xml, application/xml, text/xml, */*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()

def clean(s):
    s = html.unescape(re.sub(r"<[^>]+>", " ", s or ""))
    return re.sub(r"\s+", " ", s).strip()

def parse_date(s):
    if not s:
        return None
    s = s.strip()
    try:
        d = email.utils.parsedate_to_datetime(s)
    except Exception:
        d = None
        for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d %H:%M:%S"):
            try:
                d = datetime.strptime(s.replace("Z", "+00:00") if "%z" in fmt else s, fmt); break
            except Exception:
                pass
    if d is None:
        return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)
    return int(d.timestamp())

def local(tag):
    return tag.rsplit("}", 1)[-1].lower()

def parse_feed(raw):
    root = ET.fromstring(raw)
    out = []
    for node in root.iter():
        if local(node.tag) not in ("item", "entry"):
            continue
        f = {}
        for ch in node:
            n = local(ch.tag)
            if n == "link":
                href = ch.attrib.get("href")
                if href and ch.attrib.get("rel", "alternate") == "alternate":
                    f.setdefault("link", href)
                elif (ch.text or "").strip():
                    f.setdefault("link", ch.text.strip())
            elif n in ("title", "pubdate", "date", "published", "updated", "guid"):
                f.setdefault(n, (ch.text or "").strip())
        title = clean(f.get("title"))
        link = f.get("link") or (f.get("guid") if (f.get("guid") or "").startswith("http") else "")
        ts = parse_date(f.get("pubdate") or f.get("published") or f.get("date") or f.get("updated"))
        if title and link.startswith(("http://", "https://")):
            out.append({"title": title, "url": link, "ts": ts})
    return out

def norm_title(t):
    return re.sub(r"[^a-z0-9а-яіїєґ]+", " ", t.lower()).strip()[:90]

def sections_for(item, defaults, kw):
    secs = list(defaults)
    if kw:
        t = item["title"]
        for k in ("ukraine", "market", "politics"):
            if k not in secs and KWC[k].search(t):
                secs.append(k)
    elif "ukraine" not in secs and KWC["ukraine"].search(item["title"]):
        secs.append("ukraine")
    return secs

# ---------- X (keyless public sources) ----------
def x_from_syndication():
    url = "https://syndication.twitter.com/srv/timeline-profile/screen-name/" + X_HANDLE
    raw = fetch(url).decode("utf-8", "replace")
    m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', raw, re.S)
    if not m:
        raise ValueError("no __NEXT_DATA__")
    data = json.loads(m.group(1))
    entries = data["props"]["pageProps"]["timeline"]["entries"]
    posts = []
    for e in entries:
        t = (e.get("content") or {}).get("tweet")
        if not t or t.get("retweeted_status"):
            continue
        if (t.get("user") or {}).get("screen_name", "").lower() != X_HANDLE.lower():
            continue
        text = t.get("full_text") or t.get("text") or ""
        posts.append({"id": t["id_str"], "text": html.unescape(text), "created_at": t.get("created_at")})
    if not posts:
        raise ValueError("empty timeline")
    return posts

def x_from_nitter(base):
    raw = fetch(base.rstrip("/") + "/" + X_HANDLE + "/rss")
    root = ET.fromstring(raw)
    posts = []
    for it in root.iter("item"):
        title = (it.findtext("title") or "")
        if title.startswith("RT by "):
            continue
        link = it.findtext("link") or ""
        m = re.search(r"/status/(\d+)", link)
        if not m:
            continue
        desc = clean(it.findtext("description") or title)
        posts.append({"id": m.group(1), "text": desc or title, "created_at": it.findtext("pubDate")})
    if not posts:
        raise ValueError("empty rss")
    return posts

X_SOURCES = [("syndication.twitter.com", x_from_syndication)] + [
    (b, (lambda b=b: x_from_nitter("https://" + b))) for b in
    ("nitter.net", "xcancel.com", "nitter.poast.org", "nitter.privacydev.net", "nitter.tiekoetter.com")]

def normalize_posts(posts):
    out, seen = [], set()
    for p in posts:
        pid = str(p.get("id") or "").strip()
        if not pid.isdigit() or pid in seen:
            continue
        seen.add(pid)
        ts = p.get("ts") or parse_date(p.get("created_at") or "")
        text = html.unescape(str(p.get("text") or ""))
        # drop Telegram promo lines (site policy: no Telegram links)
        text = re.sub(r"(?im)^[^\n]*telegram[^\n]*$", "", text)
        text = re.sub(r"\n{3,}", "\n\n", text).strip()
        if not text:
            continue
        out.append({"id": pid, "text": text, "ts": ts,
                    "created_at": datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") if ts else p.get("created_at"),
                    "url": "https://x.com/%s/status/%s" % (X_HANDLE, pid)})
    out.sort(key=lambda p: (p["ts"] or 0, int(p["id"])), reverse=True)
    return out

def load(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def write_if_changed(path, obj, ignore=("updated",)):
    old = load(path, None)
    strip = lambda o: {k: v for k, v in o.items() if k not in ignore} if isinstance(o, dict) else o
    if old is not None and strip(old) == strip(obj):
        return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write("\n")
    os.replace(tmp, path)
    return True

def update_x(log):
    posts_doc = load(POSTS, {"handle": X_HANDLE, "posts": []})
    for name, fn in X_SOURCES:
        try:
            got = normalize_posts(fn())
            log.append({"source": "x:" + name, "ok": True, "items": len(got)})
            # merge with known posts (keeps posts the public source dropped), newest 15
            merged = {p["id"]: p for p in posts_doc.get("posts", [])}
            for p in got:
                merged[p["id"]] = p
            posts = normalize_posts(list(merged.values()))[:15]
            write_if_changed(POSTS, {"handle": X_HANDLE, "source": name,
                                     "updated": int(time.time()), "posts": posts})
            return posts, name
        except Exception as e:
            log.append({"source": "x:" + name, "ok": False, "error": str(e)[:120]})
    return posts_doc.get("posts", []), posts_doc.get("source", "cache")

# ---------- Translation (free, keyless, cached) ----------
TR_LANGS = {"uk": "uk", "en": "en", "fr": "fr", "de": "de", "zh": "zh-CN", "ru": "ru"}
TR_BATCH = 20            # texts per request
TR_MAX_REQUESTS = 80     # hard cap per run (keeps volume small)
TR_DELAY = 0.6           # seconds between requests
TR_MAX_CHARS = 4500      # per batch request

class _Budget:
    def __init__(self, n):
        self.left = n
    def take(self):
        if self.left <= 0:
            return False
        self.left -= 1
        time.sleep(TR_DELAY)
        return True

def _http_json(url, data=None, timeout=20):
    req = urllib.request.Request(url, data=data, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))

def tr_batch_dict(texts, tl):
    """Many texts in one request -> [(translation, src_lang)]."""
    url = "https://clients5.google.com/translate_a/t?" + urllib.parse.urlencode(
        {"client": "dict-chrome-ex", "sl": "auto", "tl": tl})
    data = urllib.parse.urlencode([("q", t) for t in texts]).encode()
    r = _http_json(url, data)
    if len(texts) == 1 and r and isinstance(r[0], str):
        r = [r]
    if not isinstance(r, list) or len(r) != len(texts):
        raise ValueError("batch size mismatch")
    out = []
    for x in r:
        if isinstance(x, list):
            out.append((str(x[0]), str(x[1]) if len(x) > 1 else None))
        else:
            out.append((str(x), None))
    return out

def tr_one_gtx(text, tl):
    url = "https://translate.googleapis.com/translate_a/single?" + urllib.parse.urlencode(
        {"client": "gtx", "sl": "auto", "tl": tl, "dt": "t"})
    r = _http_json(url, urllib.parse.urlencode({"q": text}).encode())
    return "".join(seg[0] for seg in r[0] if seg and seg[0]), r[2] if len(r) > 2 else None

def tr_one_mymemory(text, tl, sl):
    if len(text) > 480:
        raise ValueError("too long for MyMemory")
    url = "https://api.mymemory.translated.net/get?" + urllib.parse.urlencode(
        {"q": text, "langpair": "%s|%s" % (sl, tl)})
    r = _http_json(url)
    if r.get("responseStatus") != 200 or r.get("quotaFinished"):
        raise ValueError("mymemory: %s" % r.get("responseDetails"))
    return html.unescape(r["responseData"]["translatedText"]), sl

def _guess_src(text):
    return "ru" if re.search(r"[а-яё]", text, re.I) and not re.search(r"[іїєґ]", text, re.I) else (
        "uk" if re.search(r"[іїєґ]", text, re.I) else "en")

def _good(orig, tr):
    if not tr or not tr.strip():
        return False
    if len(tr) > 4 * len(orig) + 40:
        return False
    return True

def translate_entries(entries, log):
    """entries: list of dicts with "text" and "t" (dict, filled in place) and "src" (detected).
    Translates only missing languages; respects TR_MAX_REQUESTS."""
    budget = _Budget(TR_MAX_REQUESTS)
    stats = {"requests": 0, "translated": 0, "failed": 0, "method": {}}
    for code, tl in TR_LANGS.items():
        todo = [e for e in entries if code not in e["t"] and e.get("src") != code]
        i = 0
        while i < len(todo):
            # build a batch within size limits
            batch, chars = [], 0
            while i < len(todo) and len(batch) < TR_BATCH and (not batch or chars + len(todo[i]["text"]) <= TR_MAX_CHARS):
                batch.append(todo[i]); chars += len(todo[i]["text"]); i += 1
            res = None
            if budget.take():
                stats["requests"] += 1
                try:
                    res = tr_batch_dict([e["text"] for e in batch], tl)
                    stats["method"]["dict"] = stats["method"].get("dict", 0) + 1
                except Exception as ex:
                    log_err = str(ex)[:80]
                    stats.setdefault("errors", []).append("dict/%s: %s" % (code, log_err))
            if res is None:
                # per-item fallbacks (gtx, then MyMemory), still within the budget
                res = []
                for e in batch:
                    got = None
                    for name, fn in (("gtx", lambda e=e: tr_one_gtx(e["text"], tl)),
                                     ("mymemory", lambda e=e: tr_one_mymemory(e["text"], tl if code != "zh" else "zh-CN", e.get("src") or _guess_src(e["text"])))):
                        if not budget.take():
                            break
                        stats["requests"] += 1
                        try:
                            got = fn()
                            stats["method"][name] = stats["method"].get(name, 0) + 1
                            break
                        except Exception:
                            continue
                    res.append(got or (None, None))
            for e, (txt, src) in zip(batch, res):
                if src and not e.get("src"):
                    e["src"] = src.split("-")[0].lower()
                if e.get("src") == code:
                    continue  # original already in this language
                if txt and _good(e["text"], txt):
                    if txt.strip() != e["text"].strip():
                        e["t"][code] = txt.strip()
                    else:
                        e["t"][code] = None  # same as original: mark done
                    stats["translated"] += 1
                else:
                    stats["failed"] += 1
    if budget.left <= 0:
        stats["capped"] = True
    log.append({"source": "translate", "ok": stats["failed"] == 0 and not stats.get("errors"), **{k: v for k, v in stats.items() if v}})
    return stats

# ---------- Name / place glossary (post-translation normalization) ----------
# Machine translation sometimes mixes Ukrainian and Russian spellings or renders a
# name differently from item to item. Each language gets its own standard spelling:
# RU text -> Russian forms (Зеленский, Сырский, Ермак, Киев, Харьков),
# UK text -> Ukrainian forms (Зеленський, Сирський, Єрмак, Київ, Харків).
# Stems are replaced so case endings are kept. Applied on every build (idempotent,
# no network), so cached translations are fixed too.
GLOSSARY = {
    "ru": [
        # people
        (r"Зеленськ", "Зеленск"), (r"Сирськ|Сирск", "Сырск"), (r"Єрмак", "Ермак"),
        (r"Сибіг", "Сибиг"), (r"Шмигал", "Шмыгал"), (r"Умєров", "Умеров"),
        (r"Свириденк", "Свириденк"), (r"Пауелл", "Пауэлл"), (r"\bЕрдоган", "Эрдоган"),
        (r"Сі Цзіньпін", "Си Цзиньпин"), (r"\bВенс\b", "Вэнс"), (r"Віткофф|Виткофф", "Уиткофф"),
        (r"Бёрнэм|Бернем|Бёрнхэм|Бернхэм", "Бёрнем"), (r"Рубіо", "Рубио"),
        (r"Кім Чен Ин", "Ким Чен Ын"), (r"Дмитро Жук", "Дмитрий Жук"), (r"Ердоган", "Эрдоган"),
        # places (specific case forms first, then stems)
        (r"Києві", "Киеве"), (r"Київськ", "Киевск"), (r"Київ\b", "Киев"), (r"Києв", "Киев"),
        (r"Харкові", "Харькове"), (r"Харківськ", "Харьковск"), (r"Харків\b", "Харьков"), (r"Харков(?!ь)", "Харьков"),
        (r"Одес(?!с)", "Одесс"), (r"Дніпрі", "Днепре"), (r"Дніпр", "Днепр"),
        (r"Запоріжж[яі]", "Запорожье"), (r"Запорізьк", "Запорожск"),
        (r"Львові", "Львове"), (r"Львів\b", "Львов"),
        (r"Миколаївщин", "Николаевщин"), (r"Миколаївськ", "Николаевск"), (r"Миколаєві", "Николаеве"),
        (r"Миколаїв\b", "Николаев"), (r"Миколаєв", "Николаев"),
        (r"Донецьк", "Донецк"), (r"Луганськ", "Луганск"), (r"Чернігові", "Чернигове"), (r"Чернігів\b", "Чернигов"), (r"Чернігов", "Чернигов"),
        (r"Вінниц", "Винниц"), (r"Кривий Ріг", "Кривой Рог"), (r"Покровськ", "Покровск"), (r"Костянтинівк", "Константиновк"),
        (r"Куп[ʼ'’]янськ", "Купянск"),
    ],
    "uk": [
        (r"Зеленск", "Зеленськ"), (r"Сырск", "Сирськ"), (r"\bЕрмак", "Єрмак"), (r"Сибиг", "Сибіг"),
        (r"Шмыгал", "Шмигал"), (r"Умеров", "Умєров"), (r"Пауэлл", "Пауелл"), (r"Эрдоган", "Ердоган"),
        (r"Си Цзиньпин", "Сі Цзіньпін"), (r"Вэнс", "Венс"), (r"Уиткофф|Виткофф", "Віткофф"),
        (r"Бернхем|Бернгем|Бёрнем|Бьорнем", "Бернем"), (r"Рубио", "Рубіо"), (r"Ким Чен Ын", "Кім Чен Ин"),
        (r"Дмитрий Жук", "Дмитро Жук"),
        (r"Киеве", "Києві"), (r"Киевск", "Київськ"), (r"Киев\b", "Київ"), (r"Киев(?=[а-я])", "Києв"),
        (r"Харькове", "Харкові"), (r"Харьковск", "Харківськ"), (r"Харьков\b", "Харків"), (r"Харьков(?=[а-я])", "Харков"),
        (r"Одесс", "Одес"), (r"Днепре", "Дніпрі"), (r"Днепр", "Дніпр"),
        (r"Львове", "Львові"), (r"Львов\b", "Львів"),
        (r"Николаеве", "Миколаєві"), (r"Николаевщин", "Миколаївщин"), (r"Николаев\b", "Миколаїв"), (r"Николаев(?=[а-я])", "Миколаєв"),
        (r"Донецк(?!ь)", "Донецьк"), (r"Луганск(?!ь)", "Луганськ"),
    ],
}
GLOSSARY_C = {k: [(re.compile(a), b) for a, b in v] for k, v in GLOSSARY.items()}
UK_ONLY = re.compile(r"[ІіЇїЄєҐґ]")
RU_ONLY = re.compile(r"[ЫыЭэЁёЪъ]")

def normalize_names(text, lang):
    for rx, rep in GLOSSARY_C.get(lang, []):
        text = rx.sub(rep, text)
    return text

def normalize_entry_t(obj, log_stats):
    """Apply the glossary to obj["t"]; drop translations that are in the wrong
    language (Ukrainian letters in RU text or Russian letters in UK text) so they
    get re-translated."""
    t = obj.get("t") or {}
    for lang in ("ru", "uk"):
        v = t.get(lang)
        if not v:
            continue
        nv = normalize_names(v, lang)
        if nv != v:
            log_stats["normalized"] = log_stats.get("normalized", 0) + 1
            t[lang] = nv
        if (lang == "ru" and UK_ONLY.search(nv)) or (lang == "uk" and RU_ONLY.search(nv)):
            log_stats["wrong_script"] = log_stats.get("wrong_script", 0) + 1
            t.pop(lang, None)
            miss = t.setdefault("_miss", [])
            if lang not in miss:
                miss.append(lang)
    obj["t"] = t

def _clean_t(t):
    return {k: v for k, v in (t or {}).items() if v and k in TR_LANGS}

def attach_translations(items, xposts, prev, log):
    """Fill item["t"] / post["t"], reusing cached translations from the previous news.json."""
    cache = {}
    for it in prev.get("items", []):
        if it.get("t") is not None:
            cache[("u", it.get("url"), it.get("title"))] = (it.get("t"), it.get("lang"))
    for p in prev.get("x", []):
        if p.get("t") is not None:
            cache[("x", p.get("id"), p.get("text"))] = (p.get("t"), p.get("lang"))
    entries = []
    for kind, key, txtkey, obj in [("u", i["url"], "title", i) for i in items] + [("x", p["id"], "text", p) for p in xposts]:
        hit = cache.get((kind, key, obj[txtkey]))
        t, src = (dict(hit[0]), hit[1]) if hit else ({}, None)
        # cached entries: languages stored as missing were "same as original"/done
        done = dict(t)
        if hit:
            for c in TR_LANGS:
                done.setdefault(c, None)
            # retry languages that previously failed (recorded in "_miss")
            for c in (hit[0].get("_miss") or []):
                done.pop(c, None)
            done.pop("_miss", None)
        entries.append({"obj": obj, "text": obj[txtkey], "t": done, "src": src})
    try:
        translate_entries(entries, log)
    except Exception as ex:  # never break the build
        log.append({"source": "translate", "ok": False, "error": str(ex)[:120]})
    gstats = {}
    for e in entries:
        t = _clean_t(e["t"])
        miss = [c for c in TR_LANGS if c not in e["t"] and c != e.get("src")]
        if miss:
            t["_miss"] = miss
        e["obj"]["t"] = t
        if e.get("src"):
            e["obj"]["lang"] = e["src"]
        normalize_entry_t(e["obj"], gstats)
    log.append({"source": "glossary", "ok": not gstats.get("wrong_script"), **gstats})

def main():
    now = int(time.time())
    prev = load(NEWS, {})
    prev_by_feed = {}
    for it in prev.get("items", []):
        prev_by_feed.setdefault(it.get("feed"), []).append(it)
    log, items = [], []
    for key, name, url, defaults, kw in FEEDS:
        try:
            got = parse_feed(fetch(url))
            if not got:
                raise ValueError("no items")
            n = 0
            for g in got[:40]:
                title, link = g["title"], g["url"]
                if key.startswith(("reuters", "ap")):
                    title = re.sub(r"\s+-\s+(Reuters|AP News|The Associated Press)$", "", title)
                if re.search(r"Stock Price (&|and) Latest News|^\([A-Z0-9.]+\)\s*\|", title):
                    continue  # quote pages, not news
                ts = g["ts"] or now
                if ts < now - MAX_AGE_H * 3600 or ts > now + 3600:
                    continue
                items.append({"feed": key, "source": name, "title": title[:300], "url": link, "ts": ts,
                              "sec": sections_for({"title": title}, defaults, kw)})
                n += 1
            log.append({"source": key, "ok": True, "items": n})
        except Exception as e:
            kept = [i for i in prev_by_feed.get(key, []) if i.get("ts", 0) >= now - MAX_AGE_H * 3600]
            items.extend(kept)
            log.append({"source": key, "ok": False, "error": str(e)[:120], "kept": len(kept)})
    # dedup by url and by normalized title (keep earliest-listed = more specific feed)
    seen_u, seen_t, uniq = set(), set(), []
    for it in sorted(items, key=lambda i: -i["ts"]):
        nt = norm_title(it["title"])
        if it["url"] in seen_u or nt in seen_t:
            continue
        seen_u.add(it["url"]); seen_t.add(nt); uniq.append(it)
    # cap per section: native feed items first (source-diverse), keyword matches fill up to 1/3
    keep = set()
    for sec in ("market", "world", "politics", "ukraine"):
        per_src, nat, kwn = {}, 0, 0
        cap = PER_SECTION_SOURCE_CAP(sec)
        for i, it in enumerate(uniq):
            if sec not in it["sec"] or per_src.get(it["source"], 0) >= cap:
                continue
            native = sec == it["sec"][0]
            if native and nat < PER_SECTION:
                nat += 1
            elif not native and kwn < PER_SECTION // 3:
                kwn += 1
            else:
                continue
            per_src[it["source"]] = per_src.get(it["source"], 0) + 1
            keep.add(i)
    final = [it for i, it in enumerate(uniq) if i in keep]
    for it in final:
        it["sec"] = [s for s in it["sec"] if s in ("market", "world", "politics", "ukraine")]
    xposts, xsrc = update_x(log)
    xout = [{"id": p["id"], "text": p["text"], "ts": p["ts"], "url": p["url"]} for p in xposts]
    attach_translations(final, xout, prev, log)
    doc = {"updated": now, "x_handle": X_HANDLE, "x_source": xsrc, "x": xout,
           "items": final, "status": log}
    changed = write_if_changed(NEWS, doc, ignore=("updated", "status"))
    ok = sum(1 for l in log if l["ok"])
    print("feeds ok %d/%d, items %d, x posts %d (%s), changed=%s" % (ok, len(log), len(final), len(xposts), xsrc, changed))
    for l in log:
        print("  ", json.dumps(l, ensure_ascii=False))
    if not final and not prev.get("items"):
        sys.exit(1)

def PER_SECTION_SOURCE_CAP(sec):
    return PER_SECTION_SOURCE_CAP_MAP.get(sec, PER_SOURCE_IN_SECTION)
PER_SECTION_SOURCE_CAP_MAP = {"politics": 12, "ukraine": 12}

if __name__ == "__main__":
    main()
