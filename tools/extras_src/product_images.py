# One-off: copy MarketPulseStudio listing covers from /workspace/etsy into assets/products/<listing id>.webp (720px wide).
import os
from PIL import Image
E = "/workspace/etsy/"
M = {
4613052251:'debt_snowball_sinking_2026-11-09/images/01-thumbnail.jpg', 4606791663:'covers_2026-11-07/4606791663_couples-budget/01-cover.jpg',
4607126260:'holiday_2026-10-31/new-year-2027-financial-reset/images/01-new-year-financial-reset-hero.jpg', 4617703590:'openenroll2027/images/01-cover.png',
4603995046:'listings/dividend-portfolio-tracker/images/01-thumbnail.jpg', 4607416314:'kalshi_journal_2026-10-31/images/01-prediction-market-trading-journal.jpg',
4603971549:'listings/trading-journal-pro/images/01-thumbnail.jpg', 4617000139:'coparenting/images/01-cover.png', 4617673160:'newbaby/images/01-cover.png',
4617143757:'afterdeath/images/01-cover.png', 4617123204:'esthetician/images/01-cover.png', 4615485293:'sheet_doctor_product/images/01.png',
4603995270:'listings/goal-life-planner-2027-notion/images/01-thumbnail.jpg', 4622334386:'mahjong/images/01_main.png', 4622465150:'mahjong_player/images/01_main.png',
4603973045:'covers_2026-11-07/4603973045_christmas-budget/01-cover.jpg', 4607094884:'covers_2026-11-07/4607094884_secret-santa/01-cover.jpg',
4607125058:'holiday_2026-10-31/christmas-dinner-party-planner/images/01-christmas-dinner-planner-hero.jpg',
4607125622:'holiday_2026-10-31/holiday-planner-bundle/images/01-holiday-planner-bundle-hero.jpg', 4607441866:'covers_2026-11-07/4607441866_cookie-exchange/01-cover.jpg',
4615478485:'christmas_kids/images/01.png', 4615480047:'christmas_adults/images/01.png', 4615643781:'office_christmas/images/01.png',
4615378417:'hogmanay/images/01.png', 4615476511:'burns_night/images/01.png'}
if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "products")
    os.makedirs(out, exist_ok=True)
    for i, p in M.items():
        im = Image.open(E + p).convert("RGB"); w, h = im.size
        im = im.resize((720, round(720 * h / w)), Image.LANCZOS)
        f = f"{out}/{i}.webp"; im.save(f, "WEBP", quality=80, method=6)
        print(i, im.size, os.path.getsize(f) // 1024, "KB")
