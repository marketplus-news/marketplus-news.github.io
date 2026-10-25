#!/usr/bin/env python3
"""Fetch market quotes from Yahoo Finance's public chart endpoint (no API key) and write data/quotes.json.

Run by .github/workflows/update-quotes.yml every 15 minutes. The browser never calls Yahoo
(Yahoo sends no CORS headers); the page reads the same-origin data/quotes.json instead.
The file is rewritten only when a price or the chart changes, so closed markets create no commits.
On any failure the previous values are kept (per symbol), and the page shows the last good data.
"""
import http.cookiejar, json, os, sys, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "quotes.json")
UA = "Mozilla/5.0"  # Yahoo returns 429 for full browser UA strings and for python/curl defaults
# id, Yahoo symbol, decimals. XAUUSD=X does not exist on Yahoo (404) -> COMEX gold futures GC=F, labelled as futures.
SYMBOLS = [
    ("gold", "GC=F", 2), ("eurusd", "EURUSD=X", 4),  # UAH=X left out: Yahoo returns a stale previous close (0.00% change) and jumpy data
    ("wti", "CL=F", 2), ("brent", "BZ=F", 2), ("spx", "^GSPC", 2), ("ndx", "^IXIC", 2),
]
SPARK_POINTS = 48

jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
opener.addheaders = [("User-Agent", UA), ("Accept", "application/json,text/html;q=0.9,*/*;q=0.8")]


def get(url, timeout=15):
    with opener.open(url, timeout=timeout) as r:
        return r.read()


def warm_cookie():
    # Yahoo answers 429 without its consent cookie (A3); fc.yahoo.com sets it (the response itself is a 404).
    try:
        get("https://fc.yahoo.com/")
    except Exception:
        pass


def chart(sym, rng, interval):
    q = urllib.parse.quote(sym, safe="")
    last = None
    for host in ("query1", "query2"):
        try:
            d = json.loads(get(f"https://{host}.finance.yahoo.com/v8/finance/chart/{q}?range={rng}&interval={interval}"))
            res = (d.get("chart") or {}).get("result")
            if res:
                return res[0]
            last = (d.get("chart") or {}).get("error")
        except Exception as e:  # 429 / network: try the other host
            last = str(e)
        time.sleep(0.4)
    raise RuntimeError(f"{sym}: {last}")


def spark(res):
    ts = res.get("timestamp") or []
    cl = ((res.get("indicators") or {}).get("quote") or [{}])[0].get("close") or []
    pts = [(t, c) for t, c in zip(ts, cl) if c is not None]
    if len(pts) > SPARK_POINTS:
        step = len(pts) / SPARK_POINTS
        pts = [pts[int(i * step)] for i in range(SPARK_POINTS - 1)] + [pts[-1]]
    return pts


def fetch_one(sym, dec):
    r = chart(sym, "1d", "5m")
    m = r["meta"]
    price, prev = m.get("regularMarketPrice"), m.get("chartPreviousClose") or m.get("previousClose")
    if price is None or not prev:
        raise RuntimeError(f"{sym}: no price")
    pts = spark(r)
    if len(pts) < 3:  # weekend / before the open: draw the last trading session instead
        r5 = chart(sym, "5d", "15m")
        allp = [(t, c) for t, c in zip(r5.get("timestamp") or [], ((r5.get("indicators") or {}).get("quote") or [{}])[0].get("close") or []) if c is not None]
        if allp:
            day = time.strftime("%Y-%m-%d", time.gmtime(allp[-1][0] + (m.get("gmtoffset") or 0)))
            pts = [p for p in allp if time.strftime("%Y-%m-%d", time.gmtime(p[0] + (m.get("gmtoffset") or 0))) == day]
            pts = spark({"timestamp": [p[0] for p in pts], "indicators": {"quote": [{"close": [p[1] for p in pts]}]}})
    ch = price - prev
    return {
        "sym": sym, "price": round(price, dec), "prev": round(prev, dec), "ch": round(ch, dec),
        "pct": round(ch / prev * 100, 2), "dec": dec, "cur": m.get("currency"), "ex": m.get("exchangeName"),
        "time": m.get("regularMarketTime"), "spark": [round(c, dec) for _, c in pts],
    }


def main():
    try:
        prev = json.load(open(OUT, encoding="utf-8"))
    except Exception:
        prev = {"q": {}}
    warm_cookie()
    out, errors = {}, []
    for qid, sym, dec in SYMBOLS:
        try:
            out[qid] = fetch_one(sym, dec)
        except Exception as e:
            errors.append(str(e)[:160])
            if qid in prev.get("q", {}):
                out[qid] = prev["q"][qid]  # keep last good value
        time.sleep(0.5)
    if not out:
        print("no quotes fetched:", errors)
        return 1
    times = [v["time"] for v in out.values() if v.get("time")]
    doc = {"source": "Yahoo Finance (delayed)", "order": [s[0] for s in SYMBOLS], "asof": max(times) if times else None, "q": out}
    if json.dumps(doc.get("q"), sort_keys=True) == json.dumps(prev.get("q"), sort_keys=True):
        print("unchanged", "errors:", errors)
        return 0
    doc["generated"] = int(time.time())
    if errors:
        doc["errors"] = errors
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, separators=(",", ":"))
    print("written", {k: (v["price"], v["ch"], v["pct"], len(v["spark"])) for k, v in out.items()}, "errors:", errors)
    return 0


if __name__ == "__main__":
    import urllib.parse
    sys.exit(main())
