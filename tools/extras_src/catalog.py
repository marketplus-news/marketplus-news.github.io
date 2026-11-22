# Active MarketPulseStudio Etsy listings shown on the site (source: shop listing snapshot of 21 Nov 2026 in /workspace/etsy).
# Excluded: listings hidden on 14 Nov, Scholarship Tracker (off-season), Thanksgiving (season ends 26 Nov), Black Friday (ends 30 Nov).
L = "https://www.etsy.com/listing/"
CATS = [("featured", "Best sellers"), ("money", "Money & budgeting"), ("trading", "Trading & investing"), ("life", "Family & life admin"),
        ("business", "Small business"), ("hobby", "Mahjong"), ("holiday", "Christmas & holidays"), ("free", "Free")]
P = [
 # featured: USDC + Etsy (kept as before)
 dict(cat="featured", title="Hyrox Race-Prep System", price="$24.99", img="assets/crypto/hyrox.webp", desc="16-week Hyrox training plan + split calculator from 700k+ real results. Excel & Google Sheets. Pay with USDC, instant download.", ctaText="Buy with USDC", url="https://shieldz.cash/unlock/IHv1_Lk0eVEkufyZogaB", etsy=L+"4617717547"),
 dict(cat="featured", title="STR Host System BASIC", price="$49", img="assets/crypto/str-basic.webp", desc="Short-term rental host trackers: bookings, cleaning, pricing, profit. Pay with USDC, instant download.", ctaText="Buy with USDC", url="https://shieldz.cash/unlock/l-pGBrh81vxVTKfJnw9s", etsy=L+"4617676139"),
 dict(cat="featured", title="STR Host System COMPLETE", price="$119", img="assets/crypto/str-complete.webp", desc="Full Airbnb/VRBO host business system with all tools and templates. Pay with USDC, instant download.", ctaText="Buy with USDC", url="https://shieldz.cash/unlock/XzBTsw1X2X5DqlllbNny", etsy=L+"4617675743"),
 # money
 dict(cat="money", id=4613052251, title="Debt Snowball & Sinking Funds Tracker", price="$7.49", desc="Snowball or avalanche payoff plan, debt-free date calculator and sinking funds in one Google Sheets / Excel file."),
 dict(cat="money", id=4607126260, title="2027 New Year Financial Reset", price="$8", desc="Net worth tracker, annual money goals and a 2027 budget planner. Google Sheets and Excel."),
 dict(cat="money", id=4606791663, title="Couples Budget Spreadsheet", price="$9", desc="Fair-share income split, joint budget for two, shared expenses and savings goals. Sheets and Excel."),
 dict(cat="money", id=4617703590, title="2027 Open Enrollment Health Plan Comparison", price="$14.99", desc="Compare health plans side by side: HSA vs PPO cost calculator and FSA tracker. Excel and Sheets."),
 # trading
 dict(cat="trading", id=4607416314, title="Kalshi & Polymarket Trading Journal", price="$14.99", desc="Prediction-market position log with fees, settlements, real P&L and calibration. Sheets and Excel."),
 dict(cat="trading", id=4603971549, title="Trading Journal Pro", price="$14", desc="Day trading journal for forex, gold, stocks and crypto: P&L dashboard and risk calculator."),
 dict(cat="trading", id=4603995046, title="Dividend Calendar & Portfolio Tracker", price="$13", desc="Monthly dividend calendar, DRIP income and stock portfolio tracker. Google Sheets and Excel."),
 # life
 dict(cat="life", id=4617000139, title="Co-Parenting Planner", price="$16.99", desc="Custody calendar, holiday custody schedule and child support / shared expense tracker."),
 dict(cat="life", id=4617673160, title="New Baby Paperwork Kit", price="$14.99", desc="Maternity leave letter templates, newborn paperwork checklist and deadline tracker. Word and Sheets."),
 dict(cat="life", id=4617143757, title="What To Do When Someone Dies: US Checklist Kit", price="$14.99", desc="Step-by-step after-death checklist, notification letters and executor tracker. Editable Word and Excel."),
 dict(cat="life", id=4603995270, title="2027 Notion Goal & Life Planner", price="$13", desc="Notion template: yearly vision, quarterly goals dashboard and habit tracker."),
 # business
 dict(cat="business", id=4617123204, title="Esthetician Business Tracker", price="$16.99", desc="Booth rent and income tracker, client log, service profit and tax set-aside. Sheets and Excel."),
 dict(cat="business", id=4615485293, title="Sheet Doctor: Formula Backup & Repair", price="$9.99", desc="Google Sheets script that backs up formulas and repairs overwritten cells and #REF! errors."),
 # hobby
 dict(cat="hobby", id=4622334386, title="Mahjong Teacher & Club Kit", price="$59.99", desc="American mahjong lesson plans, class slides, club and league spreadsheet, instructor workbook."),
 dict(cat="hobby", id=4622465150, title="American Mahjong Player Academy", price="$39.99", desc="Learn American mahjong: beginner workbook, practice drills and cheat sheet. Printable."),
 # holiday
 dict(cat="holiday", id=4603973045, title="Christmas Budget & Gift List 2026", price="$4", desc="Gift list with budget per person, holiday spending by category and a dashboard. Sheets and Excel."),
 dict(cat="holiday", id=4607125622, title="Christmas Planner Bundle 2026", price="$12", desc="Budget, gift list, dinner planner, Secret Santa and New Year reset spreadsheets in one bundle."),
 dict(cat="holiday", id=4607094884, title="Secret Santa Generator with Exclusions", price="$4", desc="Private name draw in Google Sheets with exclusions and wish lists, no emails needed."),
 dict(cat="holiday", id=4607125058, title="Christmas Dinner Planner", price="$6", desc="Holiday menu, guest list, grocery list and a cooking timeline worked back from serving time."),
 dict(cat="holiday", id=4607441866, title="Christmas Cookie Exchange Planner", price="$3.99", desc="Cookie swap sign-up sheet, baking plan, recipe cards, labels and gift tags. Printable + Sheets."),
 dict(cat="holiday", id=4615643781, title="Office Christmas Party Games", price="$7.99", desc="Office Christmas quiz with answers, holiday trivia and bingo. TV / Zoom slides and printables."),
 dict(cat="holiday", id=4615480047, title="Christmas Trivia & Bingo for Adults", price="$7.99", desc="Adult Christmas trivia quiz with answers and bingo for a holiday party night. Printable."),
 dict(cat="holiday", id=4615478485, title="Christmas Quiz & Bingo for Kids", price="$7.99", desc="Family Christmas quiz and bingo for ages 4-6, 7-9 and 10-12. Phone, TV and printable."),
 dict(cat="holiday", id=4615378417, title="Hogmanay Party Games", price="$6.99", desc="Scottish New Year's Eve quiz with answers, bingo and a Scots word game. Printable."),
 dict(cat="holiday", id=4615476511, title="Burns Night Party Games", price="$6.99", desc="Burns Supper quiz with answers, bingo and a Scots word game. Letter and A4."),
 # free (real links, not Etsy)
 dict(cat="free", t="p11.t", d="p11.d", free=True, cta="prod.get", img="assets/goal-planner-2027-lite.webp", url="https://viridian-question-22d.notion.site/2027-Goal-Life-Planner-Lite-40418c614944812e8d68c49b3f754ff6"),
 dict(cat="free", t="p6.t", d="p6.d", free=True, cta="prod.github", img="assets/ai-skills.webp", url="https://github.com/aiskillsdrop/ai-skills-for-business"),
]
for p in P:
    if "id" in p:
        p["url"] = L + str(p.pop("id")); p["img"] = "assets/products/" + p["url"].rsplit("/", 1)[1] + ".webp"; p["etsyOnly"] = True
