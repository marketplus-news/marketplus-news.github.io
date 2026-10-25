#!/usr/bin/env python3
"""Refresh @MarketPulseGold posts from a JSON list and publish.

Usage:  python3 tools/update_posts.py posts.json      (or JSON on stdin)
Input:  [{"id": "...", "text": "...", "created_at": "2026-10-24T21:21:22.000Z"}, ...]
        or {"data": [...]} (X API shape). Retweets (text starting "RT @") are skipped.
Writes data/posts.json (merged, newest 15), rebuilds data/news.json from the cached
RSS items + posts (no network), then git commit + push only if something changed.
Flags: --no-push (write files only), --no-git.
"""
import json, os, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_news as B

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    raw = open(args[0], encoding="utf-8").read() if args else sys.stdin.read()
    data = json.loads(raw)
    if isinstance(data, dict):
        data = data.get("data") or data.get("posts") or []
    data = [p for p in data if not str(p.get("text", "")).startswith("RT @")
            and not any(r.get("type") == "retweeted" for r in (p.get("referenced_tweets") or []))]
    new = B.normalize_posts(data)
    if not new:
        sys.exit("no valid posts in input")
    old = B.load(B.POSTS, {"posts": []}).get("posts", [])
    merged = {p["id"]: p for p in old}
    merged.update({p["id"]: p for p in new})
    posts = B.normalize_posts(list(merged.values()))[:15]
    ch1 = B.write_if_changed(B.POSTS, {"handle": B.X_HANDLE, "source": "manual",
                                       "updated": int(time.time()), "posts": posts}, ignore=("updated", "source"))
    news = B.load(B.NEWS, {"items": [], "status": []})
    prev_news = json.loads(json.dumps(news))
    news["x"] = [{"id": p["id"], "text": p["text"], "ts": p["ts"], "url": p["url"]} for p in posts]
    tlog = []
    B.attach_translations(news.get("items", []), news["x"], prev_news, tlog)  # cached; only new posts hit the network
    print("translate:", json.dumps(tlog, ensure_ascii=False))
    news["x_source"] = "manual"
    news["updated"] = int(time.time())
    ch2 = B.write_if_changed(B.NEWS, news, ignore=("updated", "status", "x_source"))
    print("posts: %d, newest %s, posts.json changed=%s, news.json changed=%s"
          % (len(posts), posts[0]["created_at"], ch1, ch2))
    if not (ch1 or ch2) or "--no-git" in flags:
        return
    g = lambda *a: subprocess.run(["git", "-C", B.ROOT] + list(a), check=True)
    g("add", "data/posts.json", "data/news.json")
    if subprocess.run(["git", "-C", B.ROOT, "diff", "--cached", "--quiet"]).returncode == 0:
        print("nothing to commit"); return
    g("commit", "-m", "Update @MarketPulseGold posts")
    if "--no-push" not in flags:
        g("pull", "--rebase", "--autostash")
        g("push")

if __name__ == "__main__":
    main()
