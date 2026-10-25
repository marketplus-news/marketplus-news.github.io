# Market Plus

Static site for **Market Plus** — market and world news.
Plain HTML/CSS/vanilla JS, no build step, no trackers, no forms.

## Files
- `index.html` — main page
- `terms.html` — Terms of Use (6 languages via `app.js`)
- `style.css` — all CSS (shared by both pages)
- `app.js` — translations (UK, EN, FR, DE, 中文, RU), language dropdown, product cards, news feed renderer
- `data/news.json` — the feed shown on the page (RSS headlines by section + @MarketPulseGold posts)
- `data/posts.json` — last good copy of @MarketPulseGold posts
- `tools/build_news.py` — fetches open RSS feeds (+ X posts if a keyless public source works), machine-translates new headlines/posts into UK/EN/FR/DE/ZH/RU (free keyless endpoints, cached per url/post id, capped per run, falls back to the original) and writes `data/news.json`
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

## Language tagging and name spelling (v3)
- `<html lang>` follows the UI language (set early in `<head>` from `?lang=`, saved choice or browser language, then by `app.js` on every switch); `og:locale` and `hreflang` alternates (`?lang=uk|en|fr|de|zh|ru`) are provided.
- Every headline carries the `lang` of the text actually shown; Latin brand/source/person names inside Ukrainian, Russian or Chinese text are wrapped in `<span lang="en" translate="no">`, so screen readers and read-aloud don't pronounce them with Cyrillic rules.
- `tools/build_news.py` normalizes names with a small glossary: Russian translations get Russian spellings (Зеленский, Сырский, Ермак, Киев, Харьков, Уиткофф, Бёрнем), Ukrainian ones get Ukrainian spellings (Зеленський, Сирський, Єрмак, Київ, Харків, Віткофф, Бернем). A translation in the wrong alphabet (і/ї/є/ґ in Russian, ы/э/ё/ъ in Ukrainian) is dropped and re-translated.

## Quotes strip (v4)
- A compact strip under the hero shows gold (COMEX futures `GC=F` — Yahoo has no `XAUUSD=X` spot symbol), EUR/USD, WTI, Brent, S&P 500 and Nasdaq: price, daily change in points and %, and an intraday sparkline.
- `.github/workflows/update-quotes.yml` runs `tools/update_quotes.py` every 15 minutes: it reads Yahoo Finance's public chart endpoint (no key) and commits `data/quotes.json` only when prices change (no commits while markets are closed).
- The page re-reads the same-origin `data/quotes.json` every 60 seconds without reloading (the browser cannot call Yahoo directly: no CORS headers). Data is delayed — exchange delay plus up to ~15 min schedule plus GitHub's scheduling lag — and the strip says so, with the "as of" time.
- If the file is missing the strip hides itself; on a failed refresh the last values stay.
