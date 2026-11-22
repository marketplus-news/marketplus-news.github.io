PRODUCTS = {
 "hyrox": dict(name="Hyrox Race-Prep System", price="$24.99", img="/assets/crypto/hyrox.webp",
   text="A 16-week Hyrox training plan with a split calculator, station drills and race-day pacing sheets. Excel and Google Sheets, instant download.",
   buttons=[("Buy with USDC", "https://shieldz.cash/unlock/IHv1_Lk0eVEkufyZogaB", "gold"), ("View on Etsy", "https://www.etsy.com/listing/4617717547", "ghost")]),
 "str": dict(name="STR Host System", price="from $49", img="/assets/crypto/str-complete.webp",
   text="Spreadsheets for Airbnb and VRBO hosts: bookings, cleaning schedule, pricing calendar and a monthly profit dashboard. BASIC ($49) or COMPLETE ($119) with every tool and template.",
   buttons=[("BASIC on Etsy", "https://www.etsy.com/listing/4617676139", "gold"), ("COMPLETE on Etsy", "https://www.etsy.com/listing/4617675743", "ghost"), ("Pay with USDC", "/shop-crypto.html", "ghost")]),
 "debt": dict(name="Debt Snowball & Sinking Funds Tracker", price="$7.49", img="/assets/products/4613052251.webp",
   text="Snowball or avalanche: a month-by-month payoff plan, your debt-free date and interest saved, plus sinking funds for irregular costs. Google Sheets and Excel.",
   buttons=[("Buy on Etsy", "https://www.etsy.com/listing/4613052251", "gold")]),
 "savings": dict(name="2027 New Year Financial Reset", price="$8", img="/assets/products/4607126260.webp",
   text="Net worth tracker, annual money goals and a 2027 budget planner, so your savings plan has numbers behind it. Google Sheets and Excel.",
   buttons=[("Buy on Etsy", "https://www.etsy.com/listing/4607126260", "gold"), ("Couples budget", "https://www.etsy.com/listing/4606791663", "ghost")]),
 "trading": dict(name="Trading Journal Pro", price="$14", img="/assets/products/4603971549.webp",
   text="Day trading journal for forex, gold, stocks and crypto: log each trade with its planned risk, then review P&L, win rate and mistakes on a dashboard.",
   buttons=[("Buy on Etsy", "https://www.etsy.com/listing/4603971549", "gold"), ("Kalshi journal", "https://www.etsy.com/listing/4607416314", "ghost")]),
 "xmas": dict(name="Christmas Budget & Gift List 2026", price="$4", img="/assets/products/4603973045.webp",
   text="Gift list with a budget per person, holiday spending by category and a dashboard. Want everything? The Christmas Planner Bundle adds dinner, Secret Santa and a New Year reset.",
   buttons=[("Buy on Etsy", "https://www.etsy.com/listing/4603973045", "gold"), ("Bundle ($12)", "https://www.etsy.com/listing/4607125622", "ghost")]),
}
def pcta(key, lead="Want the full system?"):
    p = PRODUCTS[key]
    btns = "".join('<a class="btn btn-%s" href="%s"%s>%s</a>' % (c, u, ' target="_blank" rel="noopener"' if u.startswith("http") else "", t) for t, u, c in p["buttons"])
    return (f'<aside class="pcta"><div class="pimg"><img src="{p["img"]}" alt="{p["name"]}" loading="lazy" width="480" height="320"></div>'
            f'<div class="pb"><span class="kicker">{lead}</span><p class="cta-h">{p["name"]}</p><span class="price">{p["price"]}</span>'
            f'<p>{p["text"]}</p><div class="cta">{btns}</div></div></aside>')
