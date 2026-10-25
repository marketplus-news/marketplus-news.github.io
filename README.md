# Market Plus

Static landing page for **Market Plus** — markets, gold, forex & macro news without the fluff.
Plain HTML/CSS/vanilla JS, no build step, no trackers, no forms.

## Files
- `index.html` — page + all CSS
- `app.js` — translations (UK, EN, FR, DE, 中文, RU), one-click language switcher, product cards, news feed renderer
- `data/news.json` — the feed shown on the page (RSS headlines by section + @MarketPulseGold posts)
- `data/posts.json` — last good copy of @MarketPulseGold posts
- `tools/build_news.py` — fetches open RSS feeds (+ X posts if a keyless public source works) and writes `data/news.json`
- `tools/update_posts.py` — refresh X posts from a JSON list (`id,text,created_at`), commit + push only if changed
- `.github/workflows/update-news.yml` — runs `build_news.py` every 30 min and commits only when the data changed
- `favicon.svg` — gold "M+" icon
- `assets/` — compressed product covers (WebP)

## Deploy on GitHub Pages
1. Create a public repo and upload the contents of this folder to the repo root (Add file → Upload files).
2. Settings → Pages → Source: *Deploy from a branch*, Branch: `main` / `(root)` → Save.
3. The site appears at `https://<username>.github.io/<repo>/` within a minute or two.

## Editing
- Products: edit the `PRODUCTS` array in `app.js` (title, price, image, link).
- Texts: edit the `T` dictionary in `app.js` (one block per language).
- News: no X scripts or widgets. The page loads same-origin `data/news.json` and renders it with plain JS
  (tabs: All / Markets / World / Politics / Ukraine / X @MarketPulseGold). Every item links to the original.
  Sources: Reuters & AP (via Google News RSS), BBC, Al Jazeera, The Guardian, DW, France 24, NPR, CNBC,
  MarketWatch, Investing.com, The Kyiv Independent, Ukrainska Pravda, Ukrinform. Edit `FEEDS` in `tools/build_news.py`.

Not investment advice.
