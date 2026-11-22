ES = "https://www.etsy.com/shop/MarketPulseStudio?search_query="
PRODUCTS = {
 "hyrox": dict(name="Hyrox Race-Prep System", price="$24.99", img="/assets/crypto/hyrox.webp",
   text="A 16-week Hyrox training plan with a split calculator, station drills and race-day pacing sheets. Excel and Google Sheets, instant download.",
   buttons=[("Buy with USDC", "https://shieldz.cash/unlock/IHv1_Lk0eVEkufyZogaB", "gold"), ("View on Etsy", "https://www.etsy.com/listing/4617717547", "ghost")]),
 "str": dict(name="STR Host System", price="from $49", img="/assets/crypto/str-complete.webp",
   text="Spreadsheets for Airbnb and VRBO hosts: bookings, cleaning schedule, pricing calendar and a monthly profit dashboard. BASIC ($49) or COMPLETE ($119) with every tool and template.",
   buttons=[("BASIC on Etsy", "https://www.etsy.com/listing/4617676139", "gold"), ("COMPLETE on Etsy", "https://www.etsy.com/listing/4617675743", "ghost"), ("Pay with USDC", "/shop-crypto.html", "ghost")]),
 "debt": dict(name="Debt Snowball & Avalanche Payoff Tracker", price="$4", img="/assets/debt-snowball-tracker.webp",
   text="Up to 15 debts, Snowball or Avalanche: a month-by-month payoff plan, your debt-free date and interest saved, plus a printable debt-free thermometer. Excel and Google Sheets, no macros.",
   buttons=[("Get it on Etsy", ES + "debt+snowball", "gold")]),
 "savings": dict(name="2027 Savings Challenge Pack", price="$4", img="/assets/savings-challenge-2027.webp",
   text="16 printable savings challenges (52-week, 100-envelope, $10,000 and more) plus an Excel tracker with automatic totals.",
   buttons=[("Get it on Etsy", ES + "savings+challenge", "gold"), ("Budget tracker", ES + "budget", "ghost")]),
 "trading": dict(name="Trading Journal Pro", price="$14", img="/assets/trading-journal.webp",
   text="Log every trade with its risk and result: win rate, R-multiple, P&L dashboard and mistake analysis. Google Sheets and Excel.",
   buttons=[("Get it on Etsy", ES + "trading+journal", "gold")]),
 "xmas": dict(name="Christmas Budget & Gift Tracker 2026", price="$4", img="/assets/christmas-budget-2026.webp",
   text="Gift list with budget vs actual, holiday spending by category, a chart dashboard, card and party lists and a countdown. Excel and Google Sheets, no macros.",
   buttons=[("Get it on Etsy", ES + "christmas+budget", "gold")]),
}
def pcta(key, lead="Want the full system?"):
    p = PRODUCTS[key]
    btns = "".join('<a class="btn btn-%s" href="%s"%s>%s</a>' % (c, u, ' target="_blank" rel="noopener"' if u.startswith("http") else "", t) for t, u, c in p["buttons"])
    return (f'<aside class="pcta"><div class="pimg"><img src="{p["img"]}" alt="{p["name"]}" loading="lazy" width="480" height="320"></div>'
            f'<div class="pb"><span class="kicker">{lead}</span><p class="cta-h">{p["name"]}</p><span class="price">{p["price"]}</span>'
            f'<p>{p["text"]}</p><div class="cta">{btns}</div></div></aside>')
