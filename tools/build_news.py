#!/usr/bin/env python3
"""Market Plus news builder (stdlib only).

Fetches free, open RSS feeds (+ @MarketPulseGold posts from a keyless public
source when one works), assigns sections, dedups and writes data/news.json.
X posts are also kept in data/posts.json (last good copy is reused when every
keyless X source fails, and tools/update_posts.py can refresh it manually).
If a feed fails, its items from the previous news.json are kept.
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
    doc = {"updated": now, "x_handle": X_HANDLE, "x_source": xsrc,
           "x": [{"id": p["id"], "text": p["text"], "ts": p["ts"], "url": p["url"]} for p in xposts],
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
