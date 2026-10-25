# Market Plus

Static landing page for **Market Plus** — markets, gold, forex & macro news without the fluff.
Plain HTML/CSS/vanilla JS, no build step, no trackers, no forms.

## Files
- `index.html` — page + all CSS
- `app.js` — translations (EN, RU, UK, FR, DE, 中文), language switcher, product cards, X feed loader
- `favicon.svg` — gold "M+" icon
- `assets/` — compressed product covers (WebP)

## Deploy on GitHub Pages
1. Create a public repo and upload the contents of this folder to the repo root (Add file → Upload files).
2. Settings → Pages → Source: *Deploy from a branch*, Branch: `main` / `(root)` → Save.
3. The site appears at `https://<username>.github.io/<repo>/` within a minute or two.

## Editing
- Products: edit the `PRODUCTS` array in `app.js` (title, price, image, link).
- Texts: edit the `T` dictionary in `app.js` (one block per language).
- News: the section embeds X's official timeline for @MarketPulseGold (loads in the visitor's browser).
  If X doesn't render it within ~6 s, a card with a link to the X profile is shown instead.

Not investment advice.
