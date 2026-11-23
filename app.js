/* Market Plus — vanilla JS, no trackers, no build */
(function () {
  "use strict";

  // ---------- Translations ----------
  var LANGS = [
    { code: "uk", short: "UK", name: "Українська", html: "uk", og: "uk_UA" },
    { code: "en", short: "EN", name: "English", html: "en", og: "en_US" },
    { code: "fr", short: "FR", name: "Français", html: "fr", og: "fr_FR" },
    { code: "de", short: "DE", name: "Deutsch", html: "de", og: "de_DE" },
    { code: "zh", short: "中文", name: "中文（简体）", html: "zh-CN", og: "zh_CN" },
    { code: "ru", short: "RU", name: "Русский", html: "ru", og: "ru_RU" }
  ];

  var T = {
    en: {
      "nav.aria": "Main", "nf.title": "Page not found — Market Plus", "nf.h": "Page not found", "nf.p": "This page doesn't exist or has moved. Try the home page or the guides.", "nf.guides": "Open the guides",
      "title": "Market Plus: Market News, Free Money Calculators & Guides",
      "desc": "Live market and world news plus free calculators and plain-English guides: Christmas budget, debt payoff, savings, Airbnb profit, Hyrox and position size.",
      "hero.h1": "market and world news",
      "news.hint": "Tap a headline to open the original in a new tab. Headlines are machine-translated into the site language; the source is in the original language.",
      "news.orig": "Original",
      "foot.rights": "All rights reserved.",
      "foot.terms": "Terms of Use",
      "terms.title": "Terms of Use — Market Plus",
      "terms.h": "Terms of Use",
      "terms.upd": "Last updated: October 25, 2026",
      "terms.back": "← Back to Market Plus",
      "terms.s1h": "1. About this site",
      "terms.s1p": "Market Plus (marketplus-news.github.io) is a free informational website with market and world news headlines and links to digital products. By using the site you agree to these terms.",
      "terms.s2h": "2. News headlines and sources",
      "terms.s2p": "News headlines are collected automatically from publicly available RSS feeds of news publishers. Headlines and articles belong to their original publishers and authors. Every headline links to its original source; we do not republish full articles. Headlines are machine-translated automatically and translations may contain errors — the original publication always prevails.",
      "terms.s3h": "3. Not financial advice",
      "terms.s3p": "All information on the site is provided for informational purposes only and is not financial, investment, legal or tax advice, nor an offer or recommendation to buy or sell any asset. Trading in financial markets involves a risk of loss. Make your own decisions and, if needed, consult a licensed professional.",
      "terms.s4h": "4. Products",
      "terms.s4p": "Paid and free products are sold and delivered via Etsy (some free materials are on GitHub or Notion). Payments, access, delivery and refunds are handled by Etsy and are subject to Etsy’s terms. The site itself does not process payments.",
      "terms.s5h": "5. Privacy",
      "terms.s5p": "The site uses anonymous, cookie-free visit stats (GoatCounter) only. There are no forms or accounts, and no personal data is collected. Your chosen language is stored only in your own browser (localStorage). External links (news sources, Etsy, GitHub, Notion) are governed by those sites’ own policies.",
      "terms.s6h": "6. No warranty",
      "terms.s6p": "The site is provided “as is”. We do our best to keep it accurate and available, but we do not guarantee the completeness, accuracy or timeliness of the information and are not liable for any losses resulting from its use.",
      "terms.s7h": "7. Contact",
      "terms.s7p": "Questions and requests (including from publishers who want a source removed): Etsy Messages (MarketPulseStudio) or Etsy.",
      "terms.s8h": "8. Changes",
      "terms.s8p": "We may update these terms from time to time. The current version is always on this page with its last-updated date.",
      lang: "Language",
      "nav.news": "News", "nav.products": "Products", "nav.about": "About", "nav.guides": "Guides",
      "hero.badge": "● Market Plus · live market news",
      "hero.lead": "Market Plus covers the events that actually move markets — briefly and to the point: what happened and how it may affect gold, the dollar, oil and risk assets.",
      "hero.cta2": "Latest news", "hero.cta3": "Products",
      "stat.1": "gold & currencies", "stat.2b": "Macro", "stat.2": "Fed, inflation, oil", "stat.3b": "Live", "stat.3": "news feed",
      "about.h": "About",
      "about.sub": "Market Plus is a markets news project for people who want the signal, not the noise.",
      "about.t1h": "Only what matters", "about.t1p": "Geopolitics, central bank decisions, inflation and jobs data — the things that move gold and currencies.",
      "about.t2h": "With context", "about.t2p": "Every headline comes with a short takeaway: how the event may affect the market and why.",
      "about.t3h": "Source included", "about.t3p": "Reuters, Bloomberg, official statements — the original is always one tap away.",
      "news.h": "Latest news",
      "news.sub": "Headlines on markets, world, politics and Ukraine from open news sources. Updated automatically every 30 minutes.",
      "news.live": "Live", "news.loading": "Loading news…",
      "news.empty": "No news in this section yet — check back soon.",
      "news.error": "Couldn't load the news feed. Please refresh the page.",
      "news.updated": "Updated",
      "q.h": "Market quotes",
      "q.gold": "Gold (COMEX futures)",
      "q.wti": "Oil WTI",
      "q.note": "Yahoo Finance data, delayed (up to ~30 min). As of",
      "q.closed": "market closed",
      "q.open": "Open on Yahoo Finance",
      "news.tabs": "News sections",
      "tab.all": "All",
      "tab.market": "Markets",
      "tab.world": "World",
      "tab.politics": "Politics",
      "tab.ukraine": "Ukraine",
      "prod.h": "Products",
      "prod.sub": "Tools for trading, personal finance and business. Pay with USDC (crypto) or buy on Etsy.",
      "prod.note": "Buttons open Etsy, GitHub or Notion pages. This site does not collect or store any data.",
      "prod.buy": "Buy on Etsy", "prod.get": "Get it free", "prod.github": "Open on GitHub", "prod.free": "Free",
      "p1.d": "10 ready-made AI skills for Claude & ChatGPT: marketing, sales, support, SEO, HR and a content calendar. PDF guide included.",
      "p2.d": "Trade journal with automatic stats: win rate, R-multiple, P&L, dashboard and mistake analysis. Google Sheets and Excel.",
      "p3.d": "Personal budget spreadsheet for 2026: income, expenses by category, savings goals and clear monthly charts.",
      "p4.d": "Free lightweight version of the trading journal — start tracking your trade stats today.",
      "p5.d": "Free simple budget tracker: income, expenses and balance in one sheet.",
      "p6.t": "3 free AI skills for business",
      "p6.d": "Three free AI skills from the pack in an open GitHub repository. Try them before buying the full version.",
      "p7.t": "Christmas Budget & Gift Tracker 2026 (Excel + Google Sheets)",
      "p7.d": "Gift list with budget vs actual, holiday spending by category, a dashboard with charts, card and party lists and a countdown. No macros.",
      "p8.t": "FREE Christmas Gift List 2026",
      "p8.d": "Simple free gift list: budget, actual price and Bought / Wrapped for each gift, with totals that update automatically. Excel and Google Sheets.",
      "p9.t": "2027 Savings Challenge Pack (16 printable challenges + Excel tracker)",
      "p9.d": "16 printable savings challenges (52-week, 100-envelope, $10,000 and more) in A6, A4 and US Letter sizes, plus an Excel tracker with automatic totals.",
      "p10.t": "2027 Goal & Life Planner Pro for Notion",
      "p10.d": "Notion planner where goals update their progress from quarterly OKRs, projects and money goals. Monthly habit stats plus weekly, monthly and year-end reviews.",
      "p11.t": "2027 Goal & Life Planner Lite for Notion",
      "p11.d": "Free Notion planner: year vision, goals with progress bars and a days-left countdown, a weekly habit tracker and a monthly review.",
      "p12.t": "Debt Snowball & Avalanche Payoff Tracker (Excel + Google Sheets)",
      "p12.d": "Up to 15 debts, Snowball or Avalanche: a month-by-month payoff plan, your debt-free date and interest saved, plus a printable debt-free thermometer. No macros.",
      "p13.t": "FREE Debt Snowball List (Lite)",
      "p13.d": "Free debt list for up to 10 debts: totals, snowball order and which debt to pay first and how much. Excel and Google Sheets.",
      "p14.t": "Dividend & Investment Portfolio Tracker (Excel + Google Sheets)",
      "p14.d": "Log buys, sells and dividends: average cost, gain/loss, yield on cost, a dividend calendar and a dashboard. A personal record-keeping tool, no investment advice.",
      "p15.t": "FREE Habit Tracker 2027 for Notion",
      "p15.d": "Free Notion habit tracker: six daily habits with one tick each, a daily score and progress bar, week and month views, plus a monthly review page.",
      "pall.t": "All products on Etsy",
      "pall.d": "See all paid and free templates in one place on the Etsy page.",
      "prod.all": "Open Etsy",
      "foot.na": "Not investment advice.",
      "foot.disc": "All content is for informational purposes only. Trading in financial markets involves risk of loss.",
      "foot.priv": "Anonymous, cookie-free visit stats only."
    },
    ru: {
      "nav.aria": "Главное меню", "nf.title": "Страница не найдена — Market Plus", "nf.h": "Страница не найдена", "nf.p": "Такой страницы нет или она переехала. Откройте главную страницу или гайды.", "nf.guides": "Открыть гайды",
      "title": "Market Plus — новости рынка и мира",
      "desc": "Market Plus — новости рынка и мира: рынки, золото, форекс, нефть, макроэкономика, политика и Украина. Заголовки из открытых источников на 6 языках и инструменты для трейдинга и финансов.",
      "hero.h1": "новости рынка и мира",
      "news.hint": "Нажмите на заголовок, чтобы открыть оригинал в новой вкладке. Заголовки автоматически переведены на язык сайта, источник — на языке оригинала.",
      "news.orig": "Оригинал",
      "foot.rights": "Все права защищены.",
      "foot.terms": "Условия использования",
      "terms.title": "Условия использования — Market Plus",
      "terms.h": "Условия использования",
      "terms.upd": "Последнее обновление: 25 октября 2026 г.",
      "terms.back": "← На главную Market Plus",
      "terms.s1h": "1. О сайте",
      "terms.s1p": "Market Plus (marketplus-news.github.io) — бесплатный информационный сайт с заголовками новостей рынка и мира и ссылками на цифровые продукты. Пользуясь сайтом, вы соглашаетесь с этими условиями.",
      "terms.s2h": "2. Заголовки новостей и источники",
      "terms.s2p": "Заголовки новостей собираются автоматически из общедоступных RSS-лент новостных изданий. Заголовки и статьи принадлежат их издателям и авторам. Каждый заголовок ведёт на первоисточник; полные тексты статей мы не публикуем. Заголовки переводятся автоматически (машинный перевод) и могут содержать неточности — приоритет всегда у оригинальной публикации.",
      "terms.s3h": "3. Не финансовая рекомендация",
      "terms.s3p": "Вся информация на сайте носит исключительно ознакомительный характер и не является финансовой, инвестиционной, юридической или налоговой рекомендацией, а также предложением купить или продать какой-либо актив. Торговля на финансовых рынках связана с риском потерь. Принимайте решения самостоятельно и при необходимости консультируйтесь с лицензированным специалистом.",
      "terms.s4h": "4. Продукты",
      "terms.s4p": "Платные и бесплатные продукты продаются и выдаются через Etsy (часть бесплатных материалов — на GitHub и в Notion). Оплата, доступ, получение и возвраты обрабатываются Etsy и регулируются его условиями. Сам сайт платежи не обрабатывает.",
      "terms.s5h": "5. Конфиденциальность",
      "terms.s5p": "На сайте используется только обезличенная статистика посещений без cookie (GoatCounter). Форм и аккаунтов нет, персональные данные не собираются. Выбранный язык хранится только в вашем браузере (localStorage). На внешние сайты (источники новостей, Etsy, GitHub, Notion) распространяются их собственные правила.",
      "terms.s6h": "6. Отказ от гарантий",
      "terms.s6p": "Сайт предоставляется «как есть». Мы стараемся поддерживать точность и доступность, но не гарантируем полноту, точность и актуальность информации и не несём ответственности за убытки, возникшие в результате её использования.",
      "terms.s7h": "7. Контакты",
      "terms.s7p": "Вопросы и запросы (в том числе от издателей, желающих убрать свой источник): сообщения Etsy (MarketPulseStudio) или Etsy.",
      "terms.s8h": "8. Изменения",
      "terms.s8p": "Мы можем время от времени обновлять эти условия. Актуальная версия всегда находится на этой странице с датой последнего обновления.",
      lang: "Язык",
      "nav.news": "Новости", "nav.products": "Продукты", "nav.about": "О проекте", "nav.guides": "Гайды",
      "hero.badge": "● Market Plus · живые новости рынка",
      "hero.lead": "Market Plus — о событиях, которые действительно двигают рынок, коротко и по делу: что произошло и как это может повлиять на золото, доллар, нефть и рисковые активы.",
      "hero.cta2": "Последние новости", "hero.cta3": "Продукты",
      "stat.1": "золото и валюты", "stat.2b": "Макро", "stat.2": "ФРС, инфляция, нефть", "stat.3b": "Онлайн", "stat.3": "лента новостей",
      "about.h": "О проекте",
      "about.sub": "Market Plus — новостной проект о рынках для тех, кому нужна суть, а не шум.",
      "about.t1h": "Только важное", "about.t1p": "Геополитика, решения центробанков, данные по инфляции и занятости — всё, что двигает золото и валюты.",
      "about.t2h": "С контекстом", "about.t2p": "К каждой новости — короткий вывод: как событие может отразиться на рынке и почему.",
      "about.t3h": "Со ссылкой на источник", "about.t3p": "Reuters, Bloomberg, официальные заявления — оригинал всегда в одно касание.",
      "news.h": "Последние новости",
      "news.sub": "Заголовки о рынках, мире, политике и Украине из открытых новостных источников. Обновляется автоматически каждые 30 минут.",
      "news.live": "Онлайн", "news.loading": "Загружаем новости…",
      "news.empty": "В этом разделе пока нет новостей — загляните позже.",
      "news.error": "Не удалось загрузить ленту. Обновите страницу.",
      "news.updated": "Обновлено",
      "q.h": "Котировки",
      "q.gold": "Золото (фьючерс COMEX)",
      "q.wti": "Нефть WTI",
      "q.note": "Данные Yahoo Finance с задержкой (до ~30 мин). На",
      "q.closed": "рынок закрыт",
      "q.open": "Открыть на Yahoo Finance",
      "news.tabs": "Разделы новостей",
      "tab.all": "Все",
      "tab.market": "Рынки",
      "tab.world": "Мир",
      "tab.politics": "Политика",
      "tab.ukraine": "Украина",
      "prod.h": "Продукты",
      "prod.sub": "Инструменты для трейдинга, личных финансов и бизнеса. Оплата и скачивание — на Etsy.",
      "prod.note": "Кнопки открывают страницы Etsy, GitHub или Notion. Этот сайт не собирает и не хранит данные.",
      "prod.buy": "Купить на Etsy", "prod.get": "Скачать бесплатно", "prod.github": "Открыть на GitHub", "prod.free": "Бесплатно",
      "p1.d": "10 готовых AI-навыков для Claude и ChatGPT: маркетинг, продажи, поддержка, SEO, HR и контент-календарь. PDF-гайд в комплекте.",
      "p2.d": "Журнал сделок с автоматической статистикой: доля прибыльных сделок, R-мультипликатор, P&L, дашборд и разбор ошибок. Google Sheets и Excel.",
      "p3.d": "Таблица личного бюджета на 2026 год: доходы, расходы по категориям, цели накоплений и наглядные графики по месяцам.",
      "p4.d": "Бесплатная облегчённая версия журнала трейдера — начните вести статистику сделок уже сегодня.",
      "p5.d": "Бесплатный простой трекер бюджета: доходы, расходы и остаток в одной таблице.",
      "p6.t": "3 бесплатных AI-навыка для бизнеса",
      "p6.d": "Три бесплатных AI-навыка из пакета в открытом репозитории на GitHub. Попробуйте перед покупкой полной версии.",
      "p7.t": "Бюджет и список подарков на Рождество 2026 (Excel + Google Sheets)",
      "p7.d": "Список подарков с бюджетом и фактическими расходами, праздничные траты по категориям, панель с диаграммами, списки открыток и вечеринок и обратный отсчёт. Без макросов.",
      "p8.t": "БЕСПЛАТНЫЙ список подарков на Рождество 2026",
      "p8.d": "Простой бесплатный список подарков: бюджет, фактическая цена и статус «Куплено / Упаковано» для каждого подарка, с автоматическим подсчётом итогов. Excel и Google Sheets.",
      "p9.t": "Набор челленджей накоплений 2027 (16 челленджей для печати + трекер Excel)",
      "p9.d": "16 челленджей накоплений для печати (52 недели, 100 конвертов, $10 000 и другие) в форматах A6, A4 и US Letter, а также трекер Excel с автоматическими итогами.",
      "p10.t": "Планировщик целей и жизни 2027 Pro для Notion",
      "p10.d": "Планировщик в Notion, где цели обновляют свой прогресс на основе квартальных OKR, проектов и финансовых целей. Ежемесячная статистика привычек, а также еженедельные, ежемесячные и годовые обзоры.",
      "p11.t": "Планировщик целей и жизни 2027 Lite для Notion",
      "p11.d": "Бесплатный планировщик в Notion: видение года, цели с индикаторами прогресса и обратным отсчётом дней, недельный трекер привычек и ежемесячный обзор.",
      "p12.t": "Трекер погашения долгов: снежный ком и лавина (Excel + Google Sheets)",
      "p12.d": "До 15 долгов, метод снежного кома или лавины: помесячный план погашения, дата освобождения от долгов и сэкономленные проценты, а также термометр для печати. Без макросов.",
      "p13.t": "Бесплатный список долгов «Снежный ком» (Lite)",
      "p13.d": "Бесплатный список до 10 долгов: итоги, порядок снежного кома и какой долг гасить первым и на какую сумму. Excel и Google Sheets.",
      "p14.t": "Трекер дивидендов и инвестиционного портфеля (Excel + Google Sheets)",
      "p14.d": "Учёт покупок, продаж и дивидендов: средняя цена, прибыль/убыток, доходность на вложенное, календарь дивидендов и панель. Инструмент для личного учёта, не инвестиционная рекомендация.",
      "p15.t": "БЕСПЛАТНЫЙ трекер привычек 2027 для Notion",
      "p15.d": "Бесплатный трекер привычек в Notion: шесть ежедневных привычек с одной галочкой, дневной балл и индикатор прогресса, виды по неделям и месяцам и страница ежемесячного обзора.",
      "pall.t": "Все продукты на Etsy",
      "pall.d": "Смотрите все платные и бесплатные шаблоны в одном месте на странице Etsy.",
      "prod.all": "Открыть Etsy",
      "foot.na": "Не является инвестиционной рекомендацией.",
      "foot.disc": "Все материалы носят исключительно ознакомительный характер. Торговля на финансовых рынках связана с риском потери средств.",
      "foot.priv": "Только обезличенная статистика посещений без cookie."
    },
    uk: {
      "nav.aria": "Головне меню", "nf.title": "Сторінку не знайдено — Market Plus", "nf.h": "Сторінку не знайдено", "nf.p": "Такої сторінки немає або її перенесено. Відкрийте головну сторінку або гайди.", "nf.guides": "Відкрити гайди",
      "title": "Market Plus — новини ринку та світу",
      "desc": "Market Plus — новини ринку та світу: ринки, золото, форекс, нафта, макроекономіка, політика й Україна. Заголовки з відкритих джерел 6 мовами та інструменти для трейдингу й фінансів.",
      "hero.h1": "новини ринку та світу",
      "news.hint": "Натисніть на заголовок, щоб відкрити оригінал у новій вкладці. Заголовки автоматично перекладені мовою сайту, джерело — мовою оригіналу.",
      "news.orig": "Оригінал",
      "foot.rights": "Усі права захищені.",
      "foot.terms": "Умови використання",
      "terms.title": "Умови використання — Market Plus",
      "terms.h": "Умови використання",
      "terms.upd": "Останнє оновлення: 25 жовтня 2026 р.",
      "terms.back": "← На головну Market Plus",
      "terms.s1h": "1. Про сайт",
      "terms.s1p": "Market Plus (marketplus-news.github.io) — безкоштовний інформаційний сайт із заголовками новин ринку та світу й посиланнями на цифрові продукти. Користуючись сайтом, ви погоджуєтеся з цими умовами.",
      "terms.s2h": "2. Заголовки новин і джерела",
      "terms.s2p": "Заголовки новин збираються автоматично із загальнодоступних RSS-стрічок новинних видань. Заголовки й статті належать їхнім видавцям і авторам. Кожен заголовок веде на першоджерело; повних текстів статей ми не публікуємо. Заголовки перекладаються автоматично (машинний переклад) і можуть містити неточності — пріоритет завжди за оригінальною публікацією.",
      "terms.s3h": "3. Не фінансова порада",
      "terms.s3p": "Уся інформація на сайті має виключно ознайомчий характер і не є фінансовою, інвестиційною, юридичною чи податковою порадою, а також пропозицією купити або продати будь-який актив. Торгівля на фінансових ринках пов’язана з ризиком втрат. Ухвалюйте рішення самостійно й за потреби консультуйтеся з ліцензованим фахівцем.",
      "terms.s4h": "4. Продукти",
      "terms.s4p": "Платні й безкоштовні продукти продаються та видаються через Etsy (частина безкоштовних матеріалів — на GitHub і в Notion). Оплата, доступ, отримання й повернення обробляються Etsy і регулюються його умовами. Сам сайт платежів не обробляє.",
      "terms.s5h": "5. Конфіденційність",
      "terms.s5p": "На сайті використовується лише знеособлена статистика відвідувань без cookie (GoatCounter). Форм і акаунтів немає, персональні дані не збираються. Обрана мова зберігається лише у вашому браузері (localStorage). На зовнішні сайти (джерела новин, Etsy, GitHub, Notion) поширюються їхні власні правила.",
      "terms.s6h": "6. Відмова від гарантій",
      "terms.s6p": "Сайт надається «як є». Ми намагаємося підтримувати точність і доступність, але не гарантуємо повноту, точність і актуальність інформації та не несемо відповідальності за збитки, що виникли внаслідок її використання.",
      "terms.s7h": "7. Контакти",
      "terms.s7p": "Питання й запити (зокрема від видавців, які бажають прибрати своє джерело): повідомлення Etsy (MarketPulseStudio) або Etsy.",
      "terms.s8h": "8. Зміни",
      "terms.s8p": "Ми можемо час від часу оновлювати ці умови. Актуальна версія завжди на цій сторінці з датою останнього оновлення.",
      lang: "Мова",
      "nav.news": "Новини", "nav.products": "Продукти", "nav.about": "Про проєкт", "nav.guides": "Гайди",
      "hero.badge": "● Market Plus · живі новини ринку",
      "hero.lead": "Market Plus — про події, які справді рухають ринок, коротко й по суті: що сталося і як це може вплинути на золото, долар, нафту та ризикові активи.",
      "hero.cta2": "Останні новини", "hero.cta3": "Продукти",
      "stat.1": "золото й валюти", "stat.2b": "Макро", "stat.2": "ФРС, інфляція, нафта", "stat.3b": "Онлайн", "stat.3": "стрічка новин",
      "about.h": "Про проєкт",
      "about.sub": "Market Plus — новинний проєкт про ринки для тих, кому потрібна суть, а не шум.",
      "about.t1h": "Лише важливе", "about.t1p": "Геополітика, рішення центробанків, дані щодо інфляції та зайнятості — усе, що рухає золото й валюти.",
      "about.t2h": "З контекстом", "about.t2p": "До кожної новини — короткий висновок: як подія може позначитися на ринку і чому.",
      "about.t3h": "З посиланням на джерело", "about.t3p": "Reuters, Bloomberg, офіційні заяви — оригінал завжди в один дотик.",
      "news.h": "Останні новини",
      "news.sub": "Заголовки про ринки, світ, політику та Україну з відкритих новинних джерел. Оновлюється автоматично кожні 30 хвилин.",
      "news.live": "Онлайн", "news.loading": "Завантажуємо новини…",
      "news.empty": "У цьому розділі поки немає новин — зазирніть пізніше.",
      "news.error": "Не вдалося завантажити стрічку. Оновіть сторінку.",
      "news.updated": "Оновлено",
      "q.h": "Котирування",
      "q.gold": "Золото (ф’ючерс COMEX)",
      "q.wti": "Нафта WTI",
      "q.note": "Дані Yahoo Finance із затримкою (до ~30 хв). Станом на",
      "q.closed": "ринок закритий",
      "q.open": "Відкрити на Yahoo Finance",
      "news.tabs": "Розділи новин",
      "tab.all": "Усі",
      "tab.market": "Ринки",
      "tab.world": "Світ",
      "tab.politics": "Політика",
      "tab.ukraine": "Україна",
      "prod.h": "Продукти",
      "prod.sub": "Інструменти для трейдингу, особистих фінансів і бізнесу. Оплата та завантаження — на Etsy.",
      "prod.note": "Кнопки відкривають сторінки Etsy, GitHub або Notion. Цей сайт не збирає і не зберігає жодних даних.",
      "prod.buy": "Купити на Etsy", "prod.get": "Завантажити безкоштовно", "prod.github": "Відкрити на GitHub", "prod.free": "Безкоштовно",
      "p1.d": "10 готових AI-навичок для Claude і ChatGPT: маркетинг, продажі, підтримка, SEO, HR і контент-календар. PDF-посібник у комплекті.",
      "p2.d": "Журнал угод з автоматичною статистикою: win rate, R-multiple, P&L, дашборд і розбір помилок. Google Sheets та Excel.",
      "p3.d": "Таблиця особистого бюджету на 2026 рік: доходи, витрати за категоріями, цілі заощаджень і наочні графіки по місяцях.",
      "p4.d": "Безкоштовна полегшена версія журналу трейдера — почніть вести статистику угод уже сьогодні.",
      "p5.d": "Безкоштовний простий трекер бюджету: доходи, витрати й залишок в одній таблиці.",
      "p6.t": "3 безкоштовні AI-навички для бізнесу",
      "p6.d": "Три безкоштовні AI-навички з пакета у відкритому репозиторії на GitHub. Спробуйте перед купівлею повної версії.",
      "p7.t": "Різдвяний бюджет і список подарунків 2026 (Excel + Google Sheets)",
      "p7.d": "Список подарунків із бюджетом і фактичними витратами, святкові витрати за категоріями, панель із діаграмами, списки листівок і вечірок та зворотний відлік. Без макросів.",
      "p8.t": "БЕЗКОШТОВНИЙ різдвяний список подарунків 2026",
      "p8.d": "Простий безкоштовний список подарунків: бюджет, фактична ціна та позначки «Куплено / Запаковано» для кожного подарунка, підсумки оновлюються автоматично. Excel і Google Sheets.",
      "p9.t": "Набір челенджів заощаджень 2027 (16 челенджів для друку + трекер Excel)",
      "p9.d": "16 челенджів заощаджень для друку (52 тижні, 100 конвертів, $10 000 та інші) у форматах A6, A4 і US Letter, а також трекер Excel з автоматичними підсумками.",
      "p10.t": "Планувальник цілей і життя 2027 Pro для Notion",
      "p10.d": "Планувальник у Notion, де цілі оновлюють свій прогрес на основі квартальних OKR, проєктів і фінансових цілей. Щомісячна статистика звичок, а також щотижневі, щомісячні та річні огляди.",
      "p11.t": "Планувальник цілей і життя 2027 Lite для Notion",
      "p11.d": "Безкоштовний планувальник у Notion: річне бачення, цілі з індикаторами прогресу та зворотним відліком днів, щотижневий трекер звичок і щомісячний огляд.",
      "p12.t": "Трекер погашення боргів: сніжна куля і лавина (Excel + Google Sheets)",
      "p12.d": "До 15 боргів, метод сніжної кулі або лавини: помісячний план погашення, дата звільнення від боргів і заощаджені відсотки, а також термометр для друку. Без макросів.",
      "p13.t": "Безкоштовний список боргів «Сніжна куля» (Lite)",
      "p13.d": "Безкоштовний список до 10 боргів: підсумки, порядок сніжної кулі та який борг гасити першим і на яку суму. Excel і Google Sheets.",
      "p14.t": "Трекер дивідендів та інвестиційного портфеля (Excel + Google Sheets)",
      "p14.d": "Облік купівель, продажів і дивідендів: середня ціна, прибуток/збиток, дохідність на вкладене, календар дивідендів і панель. Інструмент для особистого обліку, не інвестиційна порада.",
      "p15.t": "БЕЗКОШТОВНИЙ трекер звичок 2027 для Notion",
      "p15.d": "Безкоштовний трекер звичок у Notion: шість щоденних звичок з однією позначкою, денний бал та індикатор прогресу, подання за тижнями й місяцями та сторінка щомісячного огляду.",
      "pall.t": "Усі продукти на Etsy",
      "pall.d": "Перегляньте всі платні та безкоштовні шаблони в одному місці на сторінці Etsy.",
      "prod.all": "Відкрити Etsy",
      "foot.na": "Не є інвестиційною порадою.",
      "foot.disc": "Усі матеріали мають виключно ознайомчий характер. Торгівля на фінансових ринках пов'язана з ризиком втрати коштів.",
      "foot.priv": "Лише знеособлена статистика відвідувань без cookie."
    },
    fr: {
      "nav.aria": "Menu principal", "nf.title": "Page introuvable — Market Plus", "nf.h": "Page introuvable", "nf.p": "Cette page n'existe pas ou a été déplacée. Essayez la page d'accueil ou les guides.", "nf.guides": "Voir les guides",
      "title": "Market Plus — actualités des marchés et du monde",
      "desc": "Market Plus — actualités des marchés et du monde : marchés, or, forex, pétrole, macro, politique et Ukraine. Titres de sources ouvertes en 6 langues, plus des outils de trading et de finances.",
      "hero.h1": "actualités des marchés et du monde",
      "news.hint": "Touchez un titre pour ouvrir l'original dans un nouvel onglet. Les titres sont traduits automatiquement dans la langue du site ; la source reste dans sa langue d'origine.",
      "news.orig": "Original",
      "foot.rights": "Tous droits réservés.",
      "foot.terms": "Conditions d'utilisation",
      "terms.title": "Conditions d'utilisation — Market Plus",
      "terms.h": "Conditions d'utilisation",
      "terms.upd": "Dernière mise à jour : 25 octobre 2026",
      "terms.back": "← Retour à Market Plus",
      "terms.s1h": "1. À propos du site",
      "terms.s1p": "Market Plus (marketplus-news.github.io) est un site d'information gratuit proposant des titres d'actualité des marchés et du monde ainsi que des liens vers des produits numériques. En utilisant le site, vous acceptez ces conditions.",
      "terms.s2h": "2. Titres et sources",
      "terms.s2p": "Les titres sont collectés automatiquement à partir des flux RSS publics des éditeurs de presse. Les titres et articles appartiennent à leurs éditeurs et auteurs d'origine. Chaque titre renvoie à sa source originale ; nous ne republions pas les articles complets. Les titres sont traduits automatiquement et peuvent contenir des erreurs — la publication originale fait toujours foi.",
      "terms.s3h": "3. Pas un conseil financier",
      "terms.s3p": "Toutes les informations du site sont fournies à titre informatif uniquement et ne constituent pas un conseil financier, d'investissement, juridique ou fiscal, ni une offre ou recommandation d'acheter ou de vendre un actif. Le trading sur les marchés financiers comporte un risque de perte.",
      "terms.s4h": "4. Produits",
      "terms.s4p": "Les produits payants et gratuits sont vendus et livrés via Etsy (certains contenus gratuits sont sur GitHub ou Notion). Paiements, accès, livraison et remboursements sont gérés par Etsy selon ses propres conditions. Le site ne traite aucun paiement.",
      "terms.s5h": "5. Confidentialité",
      "terms.s5p": "Le site utilise uniquement des statistiques de visites anonymes, sans cookies (GoatCounter). Il n'y a ni formulaires ni comptes, et aucune donnée personnelle n'est collectée. La langue choisie est enregistrée uniquement dans votre navigateur (localStorage). Les sites externes (sources, Etsy, GitHub, Notion) ont leurs propres règles.",
      "terms.s6h": "6. Absence de garantie",
      "terms.s6p": "Le site est fourni « tel quel ». Nous faisons de notre mieux, mais ne garantissons pas l'exhaustivité, l'exactitude ou l'actualité des informations et déclinons toute responsabilité pour les pertes liées à leur utilisation.",
      "terms.s7h": "7. Contact",
      "terms.s7p": "Questions et demandes (y compris des éditeurs souhaitant retirer une source) : Etsy Messages (MarketPulseStudio) ou Etsy.",
      "terms.s8h": "8. Modifications",
      "terms.s8p": "Ces conditions peuvent être mises à jour. La version en vigueur se trouve toujours sur cette page, avec sa date de mise à jour.",
      lang: "Langue",
      "nav.news": "Actus", "nav.products": "Produits", "nav.about": "À propos", "nav.guides": "Guides",
      "hero.badge": "● Market Plus · l'actu des marchés en direct",
      "hero.lead": "Market Plus suit les événements qui font vraiment bouger les marchés, en bref et sans détour : ce qui s'est passé et l'impact possible sur l'or, le dollar, le pétrole et les actifs risqués.",
      "hero.cta2": "Dernières actus", "hero.cta3": "Produits",
      "stat.1": "or et devises", "stat.2b": "Macro", "stat.2": "Fed, inflation, pétrole", "stat.3b": "Direct", "stat.3": "fil d'actu",
      "about.h": "À propos",
      "about.sub": "Market Plus est un projet d'actualité des marchés pour ceux qui veulent l'essentiel, pas le bruit.",
      "about.t1h": "L'essentiel uniquement", "about.t1p": "Géopolitique, décisions des banques centrales, chiffres de l'inflation et de l'emploi — ce qui fait bouger l'or et les devises.",
      "about.t2h": "Avec du contexte", "about.t2p": "Chaque info s'accompagne d'une courte analyse : l'impact possible sur le marché, et pourquoi.",
      "about.t3h": "Source à l'appui", "about.t3p": "Reuters, Bloomberg, communiqués officiels — l'original est toujours à portée de clic.",
      "news.h": "Dernières actus",
      "news.sub": "Les titres marchés, monde, politique et Ukraine issus de sources d'information ouvertes. Mise à jour automatique toutes les 30 minutes.",
      "news.live": "Direct", "news.loading": "Chargement des actus…",
      "news.empty": "Pas encore d'actus dans cette rubrique — revenez bientôt.",
      "news.error": "Impossible de charger le fil. Actualisez la page.",
      "news.updated": "Mis à jour",
      "q.h": "Cours des marchés",
      "q.gold": "Or (contrat à terme COMEX)",
      "q.wti": "Pétrole WTI",
      "q.note": "Données Yahoo Finance, en différé (jusqu’à ~30 min). Au",
      "q.closed": "marché fermé",
      "q.open": "Ouvrir sur Yahoo Finance",
      "news.tabs": "Rubriques",
      "tab.all": "Tout",
      "tab.market": "Marchés",
      "tab.world": "Monde",
      "tab.politics": "Politique",
      "tab.ukraine": "Ukraine",
      "prod.h": "Produits",
      "prod.sub": "Des outils pour le trading, les finances personnelles et l'entreprise. Paiement et téléchargement sur Etsy.",
      "prod.note": "Les boutons ouvrent les pages Etsy, GitHub ou Notion. Ce site ne collecte ni ne stocke aucune donnée.",
      "prod.buy": "Acheter sur Etsy", "prod.get": "Obtenir gratuitement", "prod.github": "Ouvrir sur GitHub", "prod.free": "Gratuit",
      "p1.d": "10 compétences IA prêtes à l'emploi pour Claude et ChatGPT : marketing, ventes, support, SEO, RH et calendrier éditorial. Guide PDF inclus.",
      "p2.d": "Journal de trading avec statistiques automatiques : taux de réussite, R-multiple, P&L, tableau de bord et analyse des erreurs. Google Sheets et Excel.",
      "p3.d": "Tableur de budget personnel 2026 : revenus, dépenses par catégorie, objectifs d'épargne et graphiques mensuels clairs.",
      "p4.d": "Version allégée et gratuite du journal de trading — commencez à suivre vos statistiques dès aujourd'hui.",
      "p5.d": "Suivi de budget simple et gratuit : revenus, dépenses et solde sur une seule feuille.",
      "p6.t": "3 compétences IA gratuites pour l'entreprise",
      "p6.d": "Trois compétences IA gratuites du pack, dans un dépôt GitHub public. Essayez-les avant d'acheter la version complète.",
      "p7.t": "Suivi du budget et des cadeaux de Noël 2026 (Excel + Google Sheets)",
      "p7.d": "Liste de cadeaux avec budget vs réel, dépenses des fêtes par catégorie, tableau de bord avec graphiques, listes de cartes de vœux et de fêtes, et compte à rebours. Sans macros.",
      "p8.t": "Liste de cadeaux de Noël 2026 GRATUITE",
      "p8.d": "Liste de cadeaux simple et gratuite : budget, prix réel et Acheté / Emballé pour chaque cadeau, avec des totaux mis à jour automatiquement. Excel et Google Sheets.",
      "p9.t": "Pack de défis d'épargne 2027 (16 défis imprimables + suivi Excel)",
      "p9.d": "16 défis d'épargne imprimables (52 semaines, 100 enveloppes, 10 000 $ et plus) aux formats A6, A4 et US Letter, plus un suivi Excel avec totaux automatiques.",
      "p10.t": "Planificateur Objectifs & Vie 2027 Pro pour Notion",
      "p10.d": "Planificateur Notion où les objectifs mettent à jour leur progression à partir des OKR trimestriels, des projets et des objectifs financiers. Statistiques mensuelles d'habitudes plus revues hebdomadaires, mensuelles et de fin d'année.",
      "p11.t": "Planificateur Objectifs & Vie 2027 Lite pour Notion",
      "p11.d": "Planificateur Notion gratuit : vision annuelle, objectifs avec barres de progression et compte à rebours des jours restants, suivi hebdomadaire des habitudes et revue mensuelle.",
      "p12.t": "Suivi de remboursement des dettes : boule de neige et avalanche (Excel + Google Sheets)",
      "p12.d": "Jusqu'à 15 dettes, méthode boule de neige ou avalanche : plan de remboursement mois par mois, date de fin des dettes et intérêts économisés, plus un thermomètre à imprimer. Sans macros.",
      "p13.t": "Liste de dettes boule de neige GRATUITE (Lite)",
      "p13.d": "Liste gratuite pour 10 dettes maximum : totaux, ordre boule de neige, et quelle dette rembourser en premier et de combien. Excel et Google Sheets.",
      "p14.t": "Suivi des dividendes et du portefeuille d'investissement (Excel + Google Sheets)",
      "p14.d": "Notez achats, ventes et dividendes : prix de revient moyen, plus/moins-values, rendement sur coût, calendrier des dividendes et tableau de bord. Outil de suivi personnel, sans conseil en investissement.",
      "p15.t": "Suivi d'habitudes 2027 GRATUIT pour Notion",
      "p15.d": "Suivi d'habitudes Notion gratuit : six habitudes quotidiennes à cocher, un score du jour et une barre de progression, des vues par semaine et par mois, et une page de bilan mensuel.",
      "pall.t": "Tous les produits sur Etsy",
      "pall.d": "Voir tous les modèles payants et gratuits en un seul endroit sur la page Etsy.",
      "prod.all": "Ouvrir Etsy",
      "foot.na": "Ceci n'est pas un conseil en investissement.",
      "foot.disc": "Tous les contenus sont fournis à titre informatif uniquement. Le trading sur les marchés financiers comporte un risque de perte.",
      "foot.priv": "Uniquement des statistiques de visites anonymes, sans cookies."
    },
    de: {
      "nav.aria": "Hauptmenü", "nf.title": "Seite nicht gefunden — Market Plus", "nf.h": "Seite nicht gefunden", "nf.p": "Diese Seite existiert nicht oder wurde verschoben. Versuchen Sie die Startseite oder die Ratgeber.", "nf.guides": "Zu den Ratgebern",
      "title": "Market Plus — Markt- und Weltnachrichten",
      "desc": "Market Plus — Markt- und Weltnachrichten: Märkte, Gold, Forex, Öl, Makro, Politik und Ukraine. Schlagzeilen aus offenen Quellen in 6 Sprachen sowie Tools für Trading und Finanzen.",
      "hero.h1": "Markt- und Weltnachrichten",
      "news.hint": "Tippe auf eine Schlagzeile, um das Original in einem neuen Tab zu öffnen. Schlagzeilen werden automatisch in die Sprache der Website übersetzt; die Quelle ist in der Originalsprache.",
      "news.orig": "Original",
      "foot.rights": "Alle Rechte vorbehalten.",
      "foot.terms": "Nutzungsbedingungen",
      "terms.title": "Nutzungsbedingungen — Market Plus",
      "terms.h": "Nutzungsbedingungen",
      "terms.upd": "Zuletzt aktualisiert: 25. Oktober 2026",
      "terms.back": "← Zurück zu Market Plus",
      "terms.s1h": "1. Über diese Website",
      "terms.s1p": "Market Plus (marketplus-news.github.io) ist eine kostenlose Informationswebsite mit Schlagzeilen zu Markt- und Weltnachrichten sowie Links zu digitalen Produkten. Mit der Nutzung der Website stimmst du diesen Bedingungen zu.",
      "terms.s2h": "2. Schlagzeilen und Quellen",
      "terms.s2p": "Schlagzeilen werden automatisch aus öffentlich zugänglichen RSS-Feeds von Nachrichtenverlagen gesammelt. Schlagzeilen und Artikel gehören ihren ursprünglichen Verlagen und Autoren. Jede Schlagzeile verlinkt auf die Originalquelle; vollständige Artikel veröffentlichen wir nicht. Schlagzeilen werden maschinell übersetzt und können Fehler enthalten — maßgeblich ist stets die Originalveröffentlichung.",
      "terms.s3h": "3. Keine Finanzberatung",
      "terms.s3p": "Alle Informationen dienen ausschließlich Informationszwecken und stellen keine Finanz-, Anlage-, Rechts- oder Steuerberatung und kein Angebot oder keine Empfehlung zum Kauf oder Verkauf von Vermögenswerten dar. Der Handel an Finanzmärkten ist mit Verlustrisiken verbunden.",
      "terms.s4h": "4. Produkte",
      "terms.s4p": "Kostenpflichtige und kostenlose Produkte werden über Etsy verkauft und bereitgestellt (einige kostenlose Materialien auf GitHub oder Notion). Zahlung, Zugang, Lieferung und Erstattungen wickelt Etsy gemäß seinen eigenen Bedingungen ab. Die Website selbst verarbeitet keine Zahlungen.",
      "terms.s5h": "5. Datenschutz",
      "terms.s5p": "Die Website verwendet nur anonyme, cookiefreie Besuchszahlen (GoatCounter). Es gibt keine Formulare oder Konten, und es werden keine personenbezogenen Daten erhoben. Die gewählte Sprache wird nur in deinem Browser gespeichert (localStorage). Für externe Seiten (Nachrichtenquellen, Etsy, GitHub, Notion) gelten deren eigene Richtlinien.",
      "terms.s6h": "6. Keine Gewähr",
      "terms.s6p": "Die Website wird „wie besehen“ bereitgestellt. Wir geben unser Bestes, übernehmen aber keine Gewähr für Vollständigkeit, Richtigkeit oder Aktualität und haften nicht für Verluste aus der Nutzung der Informationen.",
      "terms.s7h": "7. Kontakt",
      "terms.s7p": "Fragen und Anliegen (auch von Verlagen, die eine Quelle entfernen lassen möchten): Etsy Messages (MarketPulseStudio) oder Etsy.",
      "terms.s8h": "8. Änderungen",
      "terms.s8p": "Wir können diese Bedingungen gelegentlich aktualisieren. Die aktuelle Fassung steht immer mit Datum auf dieser Seite.",
      lang: "Sprache",
      "nav.news": "News", "nav.products": "Produkte", "nav.about": "Über uns", "nav.guides": "Ratgeber",
      "hero.badge": "● Market Plus · Live-Marktnachrichten",
      "hero.lead": "Market Plus berichtet über die Ereignisse, die die Märkte wirklich bewegen — kurz und auf den Punkt: was passiert ist und wie es sich auf Gold, Dollar, Öl und Risikoanlagen auswirken kann.",
      "hero.cta2": "Aktuelle News", "hero.cta3": "Produkte",
      "stat.1": "Gold & Währungen", "stat.2b": "Makro", "stat.2": "Fed, Inflation, Öl", "stat.3b": "Live", "stat.3": "News-Feed",
      "about.h": "Über uns",
      "about.sub": "Market Plus ist ein Marktnachrichten-Projekt für alle, die das Signal statt des Rauschens wollen.",
      "about.t1h": "Nur das Wichtige", "about.t1p": "Geopolitik, Zentralbankentscheidungen, Inflations- und Arbeitsmarktdaten — alles, was Gold und Währungen bewegt.",
      "about.t2h": "Mit Kontext", "about.t2p": "Zu jeder Meldung ein kurzes Fazit: wie das Ereignis den Markt beeinflussen kann und warum.",
      "about.t3h": "Mit Quelle", "about.t3p": "Reuters, Bloomberg, offizielle Mitteilungen — das Original ist immer nur einen Klick entfernt.",
      "news.h": "Aktuelle News",
      "news.sub": "Schlagzeilen zu Märkten, Welt, Politik und Ukraine aus offenen Nachrichtenquellen. Automatische Aktualisierung alle 30 Minuten.",
      "news.live": "Live", "news.loading": "News werden geladen…",
      "news.empty": "In dieser Rubrik gibt es noch keine News — schau bald wieder vorbei.",
      "news.error": "Der News-Feed konnte nicht geladen werden. Bitte lade die Seite neu.",
      "news.updated": "Aktualisiert",
      "q.h": "Marktkurse",
      "q.gold": "Gold (COMEX-Future)",
      "q.wti": "Öl WTI",
      "q.note": "Daten von Yahoo Finance, verzögert (bis ~30 Min.). Stand",
      "q.closed": "Markt geschlossen",
      "q.open": "Auf Yahoo Finance öffnen",
      "news.tabs": "Rubriken",
      "tab.all": "Alle",
      "tab.market": "Märkte",
      "tab.world": "Welt",
      "tab.politics": "Politik",
      "tab.ukraine": "Ukraine",
      "prod.h": "Produkte",
      "prod.sub": "Tools für Trading, private Finanzen und Business. Bezahlung und Download über Etsy.",
      "prod.note": "Buttons öffnen Etsy-, GitHub- oder Notion-Seiten. Diese Seite sammelt oder speichert keine Daten.",
      "prod.buy": "Auf Etsy kaufen", "prod.get": "Kostenlos holen", "prod.github": "Auf GitHub öffnen", "prod.free": "Kostenlos",
      "p1.d": "10 fertige KI-Skills für Claude & ChatGPT: Marketing, Vertrieb, Support, SEO, HR und Content-Kalender. Inklusive PDF-Anleitung.",
      "p2.d": "Trading-Journal mit automatischer Statistik: Trefferquote, R-Multiple, P&L, Dashboard und Fehleranalyse. Google Sheets und Excel.",
      "p3.d": "Tabelle fürs private Budget 2026: Einnahmen, Ausgaben nach Kategorien, Sparziele und übersichtliche Monatsdiagramme.",
      "p4.d": "Kostenlose Light-Version des Trading-Journals — starte noch heute mit der Statistik deiner Trades.",
      "p5.d": "Kostenloser, einfacher Budget-Tracker: Einnahmen, Ausgaben und Saldo in einer Tabelle.",
      "p6.t": "3 kostenlose KI-Skills fürs Business",
      "p6.d": "Drei kostenlose KI-Skills aus dem Paket in einem öffentlichen GitHub-Repository. Teste sie vor dem Kauf der Vollversion.",
      "p7.t": "Weihnachtsbudget & Geschenk-Tracker 2026 (Excel + Google Sheets)",
      "p7.d": "Geschenkliste mit Budget vs. Ist, Feiertagsausgaben nach Kategorie, Dashboard mit Diagrammen, Karten- und Partylisten sowie ein Countdown. Keine Makros.",
      "p8.t": "KOSTENLOSE Weihnachts-Geschenkliste 2026",
      "p8.d": "Einfache kostenlose Geschenkliste: Budget, tatsächlicher Preis und Gekauft / Eingepackt für jedes Geschenk, mit automatisch aktualisierten Summen. Excel und Google Sheets.",
      "p9.t": "Spar-Challenge-Set 2027 (16 druckbare Challenges + Excel-Tracker)",
      "p9.d": "16 druckbare Spar-Challenges (52-Wochen-, 100-Umschlag-, $10.000- und weitere) in A6-, A4- und US-Letter-Größen, plus ein Excel-Tracker mit automatischen Summen.",
      "p10.t": "Ziel- & Lebensplaner 2027 Pro für Notion",
      "p10.d": "Notion-Planer, in dem Ziele ihren Fortschritt aus Quartals-OKRs, Projekten und Geldzielen berechnen. Monatliche Gewohnheitsstatistiken plus Wochen-, Monats- und Jahresrückblicke.",
      "p11.t": "Ziel- & Lebensplaner 2027 Lite für Notion",
      "p11.d": "Kostenloser Notion-Planer: Jahresvision, Ziele mit Fortschrittsbalken und Countdown der verbleibenden Tage, wöchentlicher Gewohnheitstracker und Monatsrückblick.",
      "p12.t": "Schulden-Tilgungstracker: Schneeball & Lawine (Excel + Google Sheets)",
      "p12.d": "Bis zu 15 Schulden, Schneeball- oder Lawinenmethode: monatlicher Tilgungsplan, Datum der Schuldenfreiheit und gesparte Zinsen, dazu ein Schuldenthermometer zum Ausdrucken. Ohne Makros.",
      "p13.t": "KOSTENLOSE Schneeball-Schuldenliste (Lite)",
      "p13.d": "Kostenlose Liste für bis zu 10 Schulden: Summen, Schneeball-Reihenfolge und welche Schuld du zuerst mit wie viel tilgst. Excel und Google Sheets.",
      "p14.t": "Dividenden- & Depot-Tracker (Excel + Google Sheets)",
      "p14.d": "Käufe, Verkäufe und Dividenden erfassen: Durchschnittskurs, Gewinn/Verlust, Yield on Cost, Dividendenkalender und Dashboard. Ein Werkzeug zur persönlichen Dokumentation, keine Anlageberatung.",
      "p15.t": "KOSTENLOSER Gewohnheitstracker 2027 für Notion",
      "p15.d": "Kostenloser Notion-Gewohnheitstracker: sechs tägliche Gewohnheiten zum Abhaken, Tagesscore und Fortschrittsbalken, Wochen- und Monatsansichten sowie eine Seite für den Monatsrückblick.",
      "pall.t": "Alle Produkte auf Etsy",
      "pall.d": "Sieh alle kostenpflichtigen und kostenlosen Vorlagen an einem Ort auf der Etsy-Seite.",
      "prod.all": "Etsy öffnen",
      "foot.na": "Keine Anlageberatung.",
      "foot.disc": "Alle Inhalte dienen ausschließlich Informationszwecken. Der Handel an Finanzmärkten ist mit Verlustrisiken verbunden.",
      "foot.priv": "Nur anonyme Besuchszahlen, ohne Cookies."
    },
    zh: {
      "nav.aria": "主导航", "nf.title": "页面未找到 — Market Plus", "nf.h": "页面未找到", "nf.p": "此页面不存在或已移动。请返回首页或查看指南。", "nf.guides": "查看指南",
      "title": "Market Plus — 市场与全球资讯",
      "desc": "Market Plus — 市场与全球资讯：市场、黄金、外汇、原油、宏观、政治与乌克兰。来自公开新闻源的标题，支持 6 种语言，并提供交易和理财工具。",
      "hero.h1": "市场与全球资讯",
      "news.hint": "点击标题即可在新标签页中打开原文。标题已自动机器翻译为网站语言，原文保持原始语言。",
      "news.orig": "原文",
      "foot.rights": "保留所有权利。",
      "foot.terms": "使用条款",
      "terms.title": "使用条款 — Market Plus",
      "terms.h": "使用条款",
      "terms.upd": "最后更新：2026 年 10 月 25 日",
      "terms.back": "← 返回 Market Plus",
      "terms.s1h": "1. 关于本网站",
      "terms.s1p": "Market Plus（marketplus-news.github.io）是一个免费的资讯网站，提供市场与全球新闻标题以及数字产品链接。使用本网站即表示您同意本条款。",
      "terms.s2h": "2. 新闻标题与来源",
      "terms.s2p": "新闻标题自动收集自新闻出版机构公开的 RSS 源。标题和文章归其原出版方和作者所有。每条标题均链接至原始来源；我们不转载文章全文。标题为自动机器翻译，可能存在错误——一切以原始报道为准。",
      "terms.s3h": "3. 不构成投资建议",
      "terms.s3p": "本网站所有信息仅供参考，不构成任何财务、投资、法律或税务建议，也不构成买卖任何资产的要约或推荐。金融市场交易存在亏损风险。",
      "terms.s4h": "4. 产品",
      "terms.s4p": "付费和免费产品均通过 Etsy 销售和交付（部分免费资料位于 GitHub 或 Notion）。付款、访问、交付和退款由 Etsy 按其条款处理。本网站不处理任何付款。",
      "terms.s5h": "5. 隐私",
      "terms.s5p": "本网站仅使用匿名、无 Cookie 的访问统计（GoatCounter）。没有表单或账户，不收集任何个人数据。您选择的语言仅保存在您自己的浏览器中（localStorage）。外部网站（新闻来源、Etsy、GitHub、Notion）适用其各自的政策。",
      "terms.s6h": "6. 免责声明",
      "terms.s6p": "本网站按“现状”提供。我们尽力保证信息准确和网站可用，但不保证信息的完整性、准确性或及时性，对因使用这些信息造成的任何损失不承担责任。",
      "terms.s7h": "7. 联系方式",
      "terms.s7p": "问题和请求（包括希望移除其来源的出版方）：Etsy Messages（MarketPulseStudio）或 Etsy。",
      "terms.s8h": "8. 条款变更",
      "terms.s8p": "我们可能会不时更新本条款。最新版本及其更新日期始终显示在本页面。",
      lang: "语言",
      "nav.news": "资讯", "nav.products": "产品", "nav.about": "关于", "nav.guides": "指南",
      "hero.badge": "● Market Plus · 实时市场资讯",
      "hero.lead": "Market Plus 聚焦真正推动市场的事件，简明扼要：发生了什么，以及它可能如何影响黄金、美元、原油和风险资产。",
      "hero.cta2": "最新资讯", "hero.cta3": "产品",
      "stat.1": "黄金与外汇", "stat.2b": "宏观", "stat.2": "美联储、通胀、原油", "stat.3b": "实时", "stat.3": "资讯流",
      "about.h": "关于我们",
      "about.sub": "Market Plus 是一个市场资讯项目，为只想要关键信息、不要噪音的人而做。",
      "about.t1h": "只看重点", "about.t1p": "地缘政治、央行决议、通胀与就业数据——这些才是推动黄金和汇率的因素。",
      "about.t2h": "附带背景", "about.t2p": "每条资讯都配有简短解读：事件可能如何影响市场，以及原因。",
      "about.t3h": "注明来源", "about.t3p": "路透社、彭博社、官方声明——原文随时一键可查。",
      "news.h": "最新资讯",
      "news.sub": "来自公开新闻源的市场、国际、政治和乌克兰新闻标题。每 30 分钟自动更新。",
      "news.live": "实时", "news.loading": "正在加载新闻…",
      "news.empty": "该栏目暂无新闻，请稍后再来。",
      "news.error": "无法加载新闻，请刷新页面。",
      "news.updated": "更新于",
      "q.h": "市场行情",
      "q.gold": "黄金（COMEX期货）",
      "q.wti": "WTI原油",
      "q.note": "数据来自 Yahoo Finance，有延迟（最多约30分钟）。截至",
      "q.closed": "休市",
      "q.open": "在 Yahoo Finance 上打开",
      "news.tabs": "新闻栏目",
      "tab.all": "全部",
      "tab.market": "市场",
      "tab.world": "国际",
      "tab.politics": "政治",
      "tab.ukraine": "乌克兰",
      "prod.h": "产品",
      "prod.sub": "面向交易、个人理财和企业的实用工具。在 Etsy 上付款和下载。",
      "prod.note": "按钮会打开 Etsy、GitHub 或 Notion 页面。本网站不收集或存储任何数据。",
      "prod.buy": "在 Etsy 购买", "prod.get": "免费获取", "prod.github": "在 GitHub 打开", "prod.free": "免费",
      "p1.d": "10 个适用于 Claude 和 ChatGPT 的现成 AI 技能：营销、销售、客服、SEO、人力资源和内容日历。附 PDF 指南。",
      "p2.d": "交易日志，自动统计胜率、R 倍数、盈亏，附仪表盘和错误分析。支持 Google Sheets 和 Excel。",
      "p3.d": "2026 年个人预算表：收入、分类支出、储蓄目标和清晰的月度图表。",
      "p4.d": "免费精简版交易日志——今天就开始记录你的交易数据。",
      "p5.d": "免费简易预算表：收入、支出和余额尽在一张表中。",
      "p6.t": "3 个免费的商业 AI 技能",
      "p6.d": "来自技能包的三个免费 AI 技能，托管在公开的 GitHub 仓库中。购买完整版前先试用。",
      "p7.t": "2026 圣诞预算与礼物追踪器（Excel + Google Sheets）",
      "p7.d": "礼物清单（预算与实际对比）、按类别统计的节日开支、带图表的仪表盘、贺卡与聚会清单以及倒计时。无宏。",
      "p8.t": "免费 2026 圣诞礼物清单",
      "p8.d": "简易免费礼物清单：每件礼物的预算、实际价格以及已购买/已包装状态，自动更新总计。Excel 和 Google Sheets。",
      "p9.t": "2027 储蓄挑战套装（16 个可打印挑战 + Excel 追踪器）",
      "p9.d": "提供 16 项可打印储蓄挑战（52 周、100 信封、$10,000 等），尺寸包括 A6、A4 和 US Letter，并附带自动累计的 Excel 追踪器。",
      "p10.t": "2027 目标与生活规划器 Pro（Notion）",
      "p10.d": "Notion 规划器：目标进度根据季度 OKR、项目和储蓄目标自动更新。提供月度习惯统计，以及每周、每月和年终回顾。",
      "p11.t": "2027 目标与生活规划器 Lite（Notion）",
      "p11.d": "免费 Notion 规划器：年度愿景、带进度条的目标和剩余天数倒计时、每周习惯追踪器以及月度回顾。",
      "p12.t": "债务雪球法与雪崩法还款追踪表（Excel + Google Sheets）",
      "p12.d": "最多 15 笔债务，可选雪球法或雪崩法：逐月还款计划、无债日期和节省的利息，另附可打印的无债温度计。无宏。",
      "p13.t": "免费债务雪球清单（Lite）",
      "p13.d": "免费清单，最多 10 笔债务：汇总、雪球顺序，以及先还哪笔、还多少。适用于 Excel 和 Google Sheets。",
      "p14.t": "股息与投资组合追踪表（Excel + Google Sheets）",
      "p14.d": "记录买入、卖出和股息：平均成本、盈亏、成本收益率、股息日历和仪表盘。个人记账工具，不提供投资建议。",
      "p15.t": "免费 2027 习惯追踪器（Notion）",
      "p15.d": "免费 Notion 习惯追踪器：六个每日习惯一键打勾，每日得分和进度条，按周和按月视图，另附月度复盘页面。",
      "pall.t": "Etsy 上的所有产品",
      "pall.d": "在 Etsy 页面一次性查看所有付费和免费模板。",
      "prod.all": "打开 Etsy",
      "foot.na": "不构成投资建议。",
      "foot.disc": "所有内容仅供参考。金融市场交易存在亏损风险。",
      "foot.priv": "仅匿名、无 Cookie 的访问统计。"
    }
  };

  // ---------- Products (edit here) ----------
  var PCATS = [["featured", "Best sellers"], ["money", "Money & budgeting"], ["trading", "Trading & investing"], ["life", "Family & life admin"], ["business", "Small business"], ["hobby", "Mahjong"], ["holiday", "Christmas & holidays"], ["free", "Free"]];
  /*TX-START*/ var TX = {"en":{"nav.analysis":"Analysis","nav.markets":"Markets","nav.planners":"Planners","nav.menu":"Menu","nav.home":"Home","home.lat.h":"Latest articles","home.lat.sub":"Explainers and practical guides on markets, money and planning.","home.sec.h":"Sections","home.sec.sub":"Everything on Market Plus, in one place.","sec.news.d":"Live headlines on markets, world, politics and Ukraine, updated every 30 minutes.","sec.analysis.d":"Evergreen explainers: what moves gold, how forex quotes work, crypto and stock index basics.","sec.markets.d":"Gold (XAU/USD), forex, crypto and stocks: quotes strip, market headlines and explainers.","sec.planners.d":"Digital planners and templates on Etsy: budgets, goals, savings and trading journals.","sec.open":"Open section →","pg.analysis.h":"Analysis & explainers","pg.analysis.sub":"Plain-language explainers on how markets work. Educational only, no signals or forecasts.","pg.markets.sub":"Gold, forex, crypto and stocks: live quotes strip, market headlines and explainers.","pg.planners.h":"Planners & templates","pg.planners.sub":"Digital planners for budgets, goals, savings and trading, made by MarketPulseStudio.","pg.about.h":"About & contact","mk.gold.h":"Gold · XAU/USD","mk.gold.p":"Real interest rates, the US dollar, central bank demand and safe-haven flows.","mk.fx.h":"Forex","mk.fx.p":"Currency pairs, pips and spreads, and the rate decisions that move them.","mk.crypto.h":"Crypto","mk.crypto.p":"Bitcoin, altcoins and stablecoins, market cap and the risks of a 24/7 market.","mk.stocks.h":"Stocks","mk.stocks.p":"How the S&P 500, Nasdaq and Dow are built and what moves an index.","mk.read":"Read the explainer →","mk.news.h":"Market headlines","pl.etsy.h":"MarketPulseStudio on Etsy","pl.etsy.p":"Printable and digital planners from MarketPulseStudio are available in the Etsy shop.","pl.etsy.btn":"Visit the Etsy shop","pl.more.h":"Templates on Etsy","ab.contact.h":"Contact","ab.contact.p":"The easiest way to reach Market Plus is a message in Etsy Messages or on Etsy.","ab.contact.btn":"Message on Etsy","art.all":"All articles →","nav.tools":"Tools","home.tools.h":"Free tools","home.tools.sub":"Calculators that run in your browser. Nothing is sent anywhere.","home.start.h":"Start here: most popular","home.next.h":"Keep reading","tools.all":"All tools →"},"ru":{"nav.analysis":"Аналитика","nav.markets":"Рынки","nav.planners":"Планеры","nav.menu":"Меню","nav.home":"Главная","home.lat.h":"Свежие статьи","home.lat.sub":"Объяснения и практические гайды о рынках, деньгах и планировании.","home.sec.h":"Разделы","home.sec.sub":"Всё на Market Plus в одном месте.","sec.news.d":"Живая лента заголовков о рынках, мире, политике и Украине, обновляется каждые 30 минут.","sec.analysis.d":"Базовые разборы: что двигает золото, как читать котировки форекс, основы крипто и фондовых индексов.","sec.markets.d":"Золото (XAU/USD), форекс, крипто и акции: котировки, рыночные новости и разборы.","sec.planners.d":"Цифровые планеры и шаблоны на Etsy: бюджет, цели, накопления и журналы сделок.","sec.open":"Открыть раздел →","pg.analysis.h":"Аналитика и разборы","pg.analysis.sub":"Простые объяснения того, как устроены рынки. Только обучение, без сигналов и прогнозов.","pg.markets.sub":"Золото, форекс, крипто и акции: котировки, рыночные новости и разборы.","pg.planners.h":"Планеры и шаблоны","pg.planners.sub":"Цифровые планеры для бюджета, целей, накоплений и трейдинга от MarketPulseStudio.","pg.about.h":"О проекте и контакты","mk.gold.h":"Золото · XAU/USD","mk.gold.p":"Реальные ставки, доллар США, спрос центробанков и бегство в защитные активы.","mk.fx.h":"Форекс","mk.fx.p":"Валютные пары, пункты и спреды — и решения по ставкам, которые их двигают.","mk.crypto.h":"Крипто","mk.crypto.p":"Биткоин, альткоины и стейблкоины, капитализация и риски рынка 24/7.","mk.stocks.h":"Акции","mk.stocks.p":"Как устроены S&P 500, Nasdaq и Dow и что двигает индекс.","mk.read":"Читать разбор →","mk.news.h":"Рыночные новости","pl.etsy.h":"MarketPulseStudio на Etsy","pl.etsy.p":"Печатные и цифровые планеры MarketPulseStudio доступны в магазине на Etsy.","pl.etsy.btn":"Открыть магазин на Etsy","pl.more.h":"Шаблоны на Etsy","ab.contact.h":"Контакты","ab.contact.p":"Проще всего связаться с Market Plus через сообщения Etsy.","ab.contact.btn":"Написать на Etsy","art.all":"Все статьи →","nav.tools":"Инструменты","home.tools.h":"Бесплатные инструменты","home.tools.sub":"Калькуляторы работают в вашем браузере. Ничего никуда не отправляется.","home.start.h":"Начните отсюда: самое популярное","home.next.h":"Читать дальше","tools.all":"Все инструменты →"},"uk":{"nav.analysis":"Аналітика","nav.markets":"Ринки","nav.planners":"Планери","nav.menu":"Меню","nav.home":"Головна","home.lat.h":"Свіжі статті","home.lat.sub":"Пояснення та практичні гайди про ринки, гроші та планування.","home.sec.h":"Розділи","home.sec.sub":"Усе на Market Plus в одному місці.","sec.news.d":"Жива стрічка заголовків про ринки, світ, політику та Україну, оновлюється кожні 30 хвилин.","sec.analysis.d":"Базові розбори: що рухає золото, як читати котирування форекс, основи крипто та фондових індексів.","sec.markets.d":"Золото (XAU/USD), форекс, крипто та акції: котирування, ринкові новини та розбори.","sec.planners.d":"Цифрові планери та шаблони на Etsy: бюджет, цілі, заощадження та журнали угод.","sec.open":"Відкрити розділ →","pg.analysis.h":"Аналітика та розбори","pg.analysis.sub":"Прості пояснення того, як працюють ринки. Лише навчання, без сигналів і прогнозів.","pg.markets.sub":"Золото, форекс, крипто та акції: котирування, ринкові новини та розбори.","pg.planners.h":"Планери та шаблони","pg.planners.sub":"Цифрові планери для бюджету, цілей, заощаджень і трейдингу від MarketPulseStudio.","pg.about.h":"Про проєкт і контакти","mk.gold.h":"Золото · XAU/USD","mk.gold.p":"Реальні ставки, долар США, попит центробанків і втеча в захисні активи.","mk.fx.h":"Форекс","mk.fx.p":"Валютні пари, пункти та спреди — і рішення щодо ставок, які їх рухають.","mk.crypto.h":"Крипто","mk.crypto.p":"Біткоїн, альткоїни та стейблкоїни, капіталізація і ризики ринку 24/7.","mk.stocks.h":"Акції","mk.stocks.p":"Як побудовані S&P 500, Nasdaq і Dow та що рухає індекс.","mk.read":"Читати розбір →","mk.news.h":"Ринкові новини","pl.etsy.h":"MarketPulseStudio на Etsy","pl.etsy.p":"Друковані та цифрові планери MarketPulseStudio доступні в магазині на Etsy.","pl.etsy.btn":"Відкрити магазин на Etsy","pl.more.h":"Шаблони на Etsy","ab.contact.h":"Контакти","ab.contact.p":"Найпростіше зв'язатися з Market Plus через повідомлення Etsy.","ab.contact.btn":"Написати на Etsy","art.all":"Усі статті →","nav.tools":"Інструменти","home.tools.h":"Безкоштовні інструменти","home.tools.sub":"Калькулятори працюють у вашому браузері. Нічого нікуди не надсилається.","home.start.h":"Почніть звідси: найпопулярніше","home.next.h":"Читати далі","tools.all":"Усі інструменти →"},"fr":{"nav.analysis":"Analyses","nav.markets":"Marchés","nav.planners":"Planners","nav.menu":"Menu","nav.home":"Accueil","home.lat.h":"Derniers articles","home.lat.sub":"Explications et guides pratiques sur les marchés, l'argent et la planification.","home.sec.h":"Rubriques","home.sec.sub":"Tout Market Plus, au même endroit.","sec.news.d":"Titres en direct sur les marchés, le monde, la politique et l'Ukraine, mis à jour toutes les 30 minutes.","sec.analysis.d":"Explications de fond : ce qui fait bouger l'or, lire une cotation forex, bases de la crypto et des indices boursiers.","sec.markets.d":"Or (XAU/USD), forex, crypto et actions : cotations, titres des marchés et explications.","sec.planners.d":"Planners numériques et modèles sur Etsy : budget, objectifs, épargne et journaux de trading.","sec.open":"Ouvrir la rubrique →","pg.analysis.h":"Analyses et explications","pg.analysis.sub":"Des explications simples sur le fonctionnement des marchés. Contenu éducatif, sans signaux ni prévisions.","pg.markets.sub":"Or, forex, crypto et actions : cotations, titres des marchés et explications.","pg.planners.h":"Planners et modèles","pg.planners.sub":"Planners numériques pour le budget, les objectifs, l'épargne et le trading, par MarketPulseStudio.","pg.about.h":"À propos et contact","mk.gold.h":"Or · XAU/USD","mk.gold.p":"Taux réels, dollar américain, achats des banques centrales et flux refuges.","mk.fx.h":"Forex","mk.fx.p":"Paires de devises, pips et spreads, et les décisions de taux qui les font bouger.","mk.crypto.h":"Crypto","mk.crypto.p":"Bitcoin, altcoins et stablecoins, capitalisation et risques d'un marché ouvert 24 h/24.","mk.stocks.h":"Actions","mk.stocks.p":"Comment sont construits le S&P 500, le Nasdaq et le Dow, et ce qui fait bouger un indice.","mk.read":"Lire l'explication →","mk.news.h":"Titres des marchés","pl.etsy.h":"MarketPulseStudio sur Etsy","pl.etsy.p":"Les planners imprimables et numériques de MarketPulseStudio sont disponibles dans la boutique Etsy.","pl.etsy.btn":"Voir la boutique Etsy","pl.more.h":"Modèles sur Etsy","ab.contact.h":"Contact","ab.contact.p":"Le plus simple pour joindre Market Plus : un message via Etsy Messages ou sur Etsy.","ab.contact.btn":"Écrire sur Etsy","art.all":"Tous les articles →","nav.tools":"Outils","home.tools.h":"Outils gratuits","home.tools.sub":"Des calculateurs qui tournent dans votre navigateur. Rien n'est envoyé.","home.start.h":"Commencez ici : les plus populaires","home.next.h":"À lire ensuite","tools.all":"Tous les outils →"},"de":{"nav.analysis":"Analysen","nav.markets":"Märkte","nav.planners":"Planer","nav.menu":"Menü","nav.home":"Startseite","home.lat.h":"Neueste Artikel","home.lat.sub":"Erklärstücke und praktische Ratgeber zu Märkten, Geld und Planung.","home.sec.h":"Rubriken","home.sec.sub":"Alles von Market Plus an einem Ort.","sec.news.d":"Live-Schlagzeilen zu Märkten, Welt, Politik und der Ukraine, alle 30 Minuten aktualisiert.","sec.analysis.d":"Grundlagen: was den Goldpreis bewegt, wie Devisenkurse funktionieren, Krypto- und Aktienindex-Basics.","sec.markets.d":"Gold (XAU/USD), Devisen, Krypto und Aktien: Kurse, Marktschlagzeilen und Erklärstücke.","sec.planners.d":"Digitale Planer und Vorlagen auf Etsy: Budget, Ziele, Sparen und Trading-Journale.","sec.open":"Rubrik öffnen →","pg.analysis.h":"Analysen und Erklärstücke","pg.analysis.sub":"Verständliche Erklärungen, wie Märkte funktionieren. Nur zur Bildung, keine Signale oder Prognosen.","pg.markets.sub":"Gold, Devisen, Krypto und Aktien: Kurse, Marktschlagzeilen und Erklärstücke.","pg.planners.h":"Planer und Vorlagen","pg.planners.sub":"Digitale Planer für Budget, Ziele, Sparen und Trading von MarketPulseStudio.","pg.about.h":"Über uns und Kontakt","mk.gold.h":"Gold · XAU/USD","mk.gold.p":"Realzinsen, US-Dollar, Nachfrage der Zentralbanken und Flucht in sichere Häfen.","mk.fx.h":"Devisen","mk.fx.p":"Währungspaare, Pips und Spreads – und die Zinsentscheide, die sie bewegen.","mk.crypto.h":"Krypto","mk.crypto.p":"Bitcoin, Altcoins und Stablecoins, Marktkapitalisierung und Risiken eines 24/7-Markts.","mk.stocks.h":"Aktien","mk.stocks.p":"Wie S&P 500, Nasdaq und Dow aufgebaut sind und was einen Index bewegt.","mk.read":"Zum Erklärstück →","mk.news.h":"Marktschlagzeilen","pl.etsy.h":"MarketPulseStudio auf Etsy","pl.etsy.p":"Druckbare und digitale Planer von MarketPulseStudio gibt es im Etsy-Shop.","pl.etsy.btn":"Zum Etsy-Shop","pl.more.h":"Vorlagen auf Etsy","ab.contact.h":"Kontakt","ab.contact.p":"Am einfachsten erreichen Sie Market Plus per Nachricht über Etsy Messages oder auf Etsy.","ab.contact.btn":"Auf Etsy schreiben","art.all":"Alle Artikel →","nav.tools":"Rechner","home.tools.h":"Kostenlose Rechner","home.tools.sub":"Rechner, die in Ihrem Browser laufen. Es wird nichts gesendet.","home.start.h":"Hier starten: am beliebtesten","home.next.h":"Weiterlesen","tools.all":"Alle Rechner →"},"zh":{"nav.analysis":"分析","nav.markets":"市场","nav.planners":"规划模板","nav.menu":"菜单","nav.home":"首页","home.lat.h":"最新文章","home.lat.sub":"关于市场、理财与规划的解读和实用指南。","home.sec.h":"栏目","home.sec.sub":"Market Plus 全部内容，一目了然。","sec.news.d":"市场、国际、政治和乌克兰实时头条，每 30 分钟更新。","sec.analysis.d":"常青解读：什么影响金价、外汇报价怎么看、加密货币与股指基础。","sec.markets.d":"黄金（XAU/USD）、外汇、加密货币和股票：行情条、市场头条与解读。","sec.planners.d":"Etsy 上的数字规划模板：预算、目标、储蓄与交易日志。","sec.open":"进入栏目 →","pg.analysis.h":"分析与解读","pg.analysis.sub":"用通俗语言解释市场如何运作。仅供学习，不含信号或预测。","pg.markets.sub":"黄金、外汇、加密货币和股票：行情条、市场头条与解读。","pg.planners.h":"规划与模板","pg.planners.sub":"MarketPulseStudio 出品的预算、目标、储蓄与交易数字规划模板。","pg.about.h":"关于与联系","mk.gold.h":"黄金 · XAU/USD","mk.gold.p":"实际利率、美元、央行购金需求与避险资金流。","mk.fx.h":"外汇","mk.fx.p":"货币对、点值与点差，以及驱动它们的利率决议。","mk.crypto.h":"加密货币","mk.crypto.p":"比特币、山寨币与稳定币、市值以及全天候市场的风险。","mk.stocks.h":"股票","mk.stocks.p":"标普 500、纳斯达克和道琼斯如何构成，以及什么推动指数涨跌。","mk.read":"阅读解读 →","mk.news.h":"市场头条","pl.etsy.h":"Etsy 上的 MarketPulseStudio","pl.etsy.p":"MarketPulseStudio 的可打印和数字规划模板在 Etsy 店铺有售。","pl.etsy.btn":"访问 Etsy 店铺","pl.more.h":"Etsy 上的模板","ab.contact.h":"联系","ab.contact.p":"联系 Market Plus 最简单的方式是通过 Etsy Messages 留言。","ab.contact.btn":"在 Etsy 上留言","art.all":"全部文章 →","nav.tools":"工具","home.tools.h":"免费工具","home.tools.sub":"在浏览器中运行的计算器，不会发送任何数据。","home.start.h":"从这里开始：最受欢迎","home.next.h":"继续阅读","tools.all":"全部工具 →"}};
  Object.keys(TX).forEach(function (l) { if (T[l]) for (var k in TX[l]) T[l][k] = TX[l][k]; }); /*TX-END*/
  var PRODUCTS = [
    {"cat": "featured", "title": "Hyrox Race-Prep System", "price": "$24.99", "img": "assets/crypto/hyrox.webp", "desc": "16-week Hyrox training plan + split calculator from 700k+ real results. Excel & Google Sheets. Pay with USDC, instant download.", "ctaText": "Buy with USDC", "url": "https://shieldz.cash/unlock/IHv1_Lk0eVEkufyZogaB", "etsy": "https://www.etsy.com/listing/4617717547"},
    {"cat": "featured", "title": "STR Host System BASIC", "price": "$49", "img": "assets/crypto/str-basic.webp", "desc": "Short-term rental host trackers: bookings, cleaning, pricing, profit. Pay with USDC, instant download.", "ctaText": "Buy with USDC", "url": "https://shieldz.cash/unlock/l-pGBrh81vxVTKfJnw9s", "etsy": "https://www.etsy.com/listing/4617676139"},
    {"cat": "featured", "title": "STR Host System COMPLETE", "price": "$119", "img": "assets/crypto/str-complete.webp", "desc": "Full Airbnb/VRBO host business system with all tools and templates. Pay with USDC, instant download.", "ctaText": "Buy with USDC", "url": "https://shieldz.cash/unlock/XzBTsw1X2X5DqlllbNny", "etsy": "https://www.etsy.com/listing/4617675743"},
    {"cat": "money", "title": "Debt Snowball & Sinking Funds Tracker", "price": "$7.49", "desc": "Snowball or avalanche payoff plan, debt-free date calculator and sinking funds in one Google Sheets / Excel file.", "url": "https://www.etsy.com/listing/4613052251", "img": "assets/products/4613052251.webp", "etsyOnly": true},
    {"cat": "money", "title": "2027 New Year Financial Reset", "price": "$8", "desc": "Net worth tracker, annual money goals and a 2027 budget planner. Google Sheets and Excel.", "url": "https://www.etsy.com/listing/4607126260", "img": "assets/products/4607126260.webp", "etsyOnly": true},
    {"cat": "money", "title": "Couples Budget Spreadsheet", "price": "$9", "desc": "Fair-share income split, joint budget for two, shared expenses and savings goals. Sheets and Excel.", "url": "https://www.etsy.com/listing/4606791663", "img": "assets/products/4606791663.webp", "etsyOnly": true},
    {"cat": "money", "title": "2027 Open Enrollment Health Plan Comparison", "price": "$14.99", "desc": "Compare health plans side by side: HSA vs PPO cost calculator and FSA tracker. Excel and Sheets.", "url": "https://www.etsy.com/listing/4617703590", "img": "assets/products/4617703590.webp", "etsyOnly": true},
    {"cat": "trading", "title": "Kalshi & Polymarket Trading Journal", "price": "$14.99", "desc": "Prediction-market position log with fees, settlements, real P&L and calibration. Sheets and Excel.", "url": "https://www.etsy.com/listing/4607416314", "img": "assets/products/4607416314.webp", "etsyOnly": true},
    {"cat": "trading", "title": "Trading Journal Pro", "price": "$14", "desc": "Day trading journal for forex, gold, stocks and crypto: P&L dashboard and risk calculator.", "url": "https://www.etsy.com/listing/4603971549", "img": "assets/products/4603971549.webp", "etsyOnly": true},
    {"cat": "trading", "title": "Dividend Calendar & Portfolio Tracker", "price": "$13", "desc": "Monthly dividend calendar, DRIP income and stock portfolio tracker. Google Sheets and Excel.", "url": "https://www.etsy.com/listing/4603995046", "img": "assets/products/4603995046.webp", "etsyOnly": true},
    {"cat": "life", "title": "Co-Parenting Planner", "price": "$16.99", "desc": "Custody calendar, holiday custody schedule and child support / shared expense tracker.", "url": "https://www.etsy.com/listing/4617000139", "img": "assets/products/4617000139.webp", "etsyOnly": true},
    {"cat": "life", "title": "New Baby Paperwork Kit", "price": "$14.99", "desc": "Maternity leave letter templates, newborn paperwork checklist and deadline tracker. Word and Sheets.", "url": "https://www.etsy.com/listing/4617673160", "img": "assets/products/4617673160.webp", "etsyOnly": true},
    {"cat": "life", "title": "What To Do When Someone Dies: US Checklist Kit", "price": "$14.99", "desc": "Step-by-step after-death checklist, notification letters and executor tracker. Editable Word and Excel.", "url": "https://www.etsy.com/listing/4617143757", "img": "assets/products/4617143757.webp", "etsyOnly": true},
    {"cat": "life", "title": "2027 Notion Goal & Life Planner", "price": "$13", "desc": "Notion template: yearly vision, quarterly goals dashboard and habit tracker.", "url": "https://www.etsy.com/listing/4603995270", "img": "assets/products/4603995270.webp", "etsyOnly": true},
    {"cat": "business", "title": "Esthetician Business Tracker", "price": "$16.99", "desc": "Booth rent and income tracker, client log, service profit and tax set-aside. Sheets and Excel.", "url": "https://www.etsy.com/listing/4617123204", "img": "assets/products/4617123204.webp", "etsyOnly": true},
    {"cat": "business", "title": "Sheet Doctor: Formula Backup & Repair", "price": "$9.99", "desc": "Google Sheets script that backs up formulas and repairs overwritten cells and #REF! errors.", "url": "https://www.etsy.com/listing/4615485293", "img": "assets/products/4615485293.webp", "etsyOnly": true},
    {"cat": "hobby", "title": "Mahjong Teacher & Club Kit", "price": "$59.99", "desc": "American mahjong lesson plans, class slides, club and league spreadsheet, instructor workbook.", "url": "https://www.etsy.com/listing/4622334386", "img": "assets/products/4622334386.webp", "etsyOnly": true},
    {"cat": "hobby", "title": "American Mahjong Player Academy", "price": "$39.99", "desc": "Learn American mahjong: beginner workbook, practice drills and cheat sheet. Printable.", "url": "https://www.etsy.com/listing/4622465150", "img": "assets/products/4622465150.webp", "etsyOnly": true},
    {"cat": "holiday", "title": "Christmas Budget & Gift List 2026", "price": "$4", "desc": "Gift list with budget per person, holiday spending by category and a dashboard. Sheets and Excel.", "url": "https://www.etsy.com/listing/4603973045", "img": "assets/products/4603973045.webp", "etsyOnly": true},
    {"cat": "holiday", "title": "Christmas Planner Bundle 2026", "price": "$12", "desc": "Budget, gift list, dinner planner, Secret Santa and New Year reset spreadsheets in one bundle.", "url": "https://www.etsy.com/listing/4607125622", "img": "assets/products/4607125622.webp", "etsyOnly": true},
    {"cat": "holiday", "title": "Secret Santa Generator with Exclusions", "price": "$4", "desc": "Private name draw in Google Sheets with exclusions and wish lists, no emails needed.", "url": "https://www.etsy.com/listing/4607094884", "img": "assets/products/4607094884.webp", "etsyOnly": true},
    {"cat": "holiday", "title": "Christmas Dinner Planner", "price": "$6", "desc": "Holiday menu, guest list, grocery list and a cooking timeline worked back from serving time.", "url": "https://www.etsy.com/listing/4607125058", "img": "assets/products/4607125058.webp", "etsyOnly": true},
    {"cat": "holiday", "title": "Christmas Cookie Exchange Planner", "price": "$3.99", "desc": "Cookie swap sign-up sheet, baking plan, recipe cards, labels and gift tags. Printable + Sheets.", "url": "https://www.etsy.com/listing/4607441866", "img": "assets/products/4607441866.webp", "etsyOnly": true},
    {"cat": "holiday", "title": "Office Christmas Party Games", "price": "$7.99", "desc": "Office Christmas quiz with answers, holiday trivia and bingo. TV / Zoom slides and printables.", "url": "https://www.etsy.com/listing/4615643781", "img": "assets/products/4615643781.webp", "etsyOnly": true},
    {"cat": "holiday", "title": "Christmas Trivia & Bingo for Adults", "price": "$7.99", "desc": "Adult Christmas trivia quiz with answers and bingo for a holiday party night. Printable.", "url": "https://www.etsy.com/listing/4615480047", "img": "assets/products/4615480047.webp", "etsyOnly": true},
    {"cat": "holiday", "title": "Christmas Quiz & Bingo for Kids", "price": "$7.99", "desc": "Family Christmas quiz and bingo for ages 4-6, 7-9 and 10-12. Phone, TV and printable.", "url": "https://www.etsy.com/listing/4615478485", "img": "assets/products/4615478485.webp", "etsyOnly": true},
    {"cat": "holiday", "title": "Hogmanay Party Games", "price": "$6.99", "desc": "Scottish New Year's Eve quiz with answers, bingo and a Scots word game. Printable.", "url": "https://www.etsy.com/listing/4615378417", "img": "assets/products/4615378417.webp", "etsyOnly": true},
    {"cat": "holiday", "title": "Burns Night Party Games", "price": "$6.99", "desc": "Burns Supper quiz with answers, bingo and a Scots word game. Letter and A4.", "url": "https://www.etsy.com/listing/4615476511", "img": "assets/products/4615476511.webp", "etsyOnly": true},
    {"cat": "free", "t": "p11.t", "d": "p11.d", "free": true, "cta": "prod.get", "img": "assets/goal-planner-2027-lite.webp", "url": "https://viridian-question-22d.notion.site/2027-Goal-Life-Planner-Lite-40418c614944812e8d68c49b3f754ff6"},
    {"cat": "free", "t": "p6.t", "d": "p6.d", "free": true, "cta": "prod.github", "img": "assets/ai-skills.webp", "url": "https://github.com/aiskillsdrop/ai-skills-for-business"}
  ];

  var $ = function (id) { return document.getElementById(id); };
  // site root (folder of app.js), so section pages in sub-folders load data/ and assets/ correctly
  var BASE = (function () { var s = document.currentScript; return s && s.src ? s.src.replace(/app\.js(\?.*)?$/, "") : ""; })();
  var cur = "en";
  function tr(k) { return (T[cur] && T[cur][k]) || T.en[k] || ""; }
  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }
  // ---------- Language tagging for correct reading (screen readers / read-aloud / TTS) ----------
  // Text is always tagged with the language it is actually written in:
  //  * <html lang> = current UI language;
  //  * in Cyrillic/Chinese UIs, Latin-script runs (brands, names, tickers: Market Plus, Etsy,
  //    Starlink, AJB) get <span lang="en" translate="no">, otherwise a
  //    Russian/Ukrainian voice spells them by Cyrillic rules;
  //  * headlines carry the lang of the text actually shown (translation or original).
  var LATIN_RUN = /[A-Za-z][A-Za-z0-9&@'’.+\-]*(?:[ \u00a0]+(?:[A-Za-z0-9][A-Za-z0-9&@'’.+\-]*))*/g;
  function scriptLang(text, hint) {
    if (/[ІіЇїЄєҐґ]/.test(text)) return "uk";
    if (/[ЫыЭэЁёЪъ]/.test(text)) return "ru";
    if (/[А-Яа-я]/.test(text)) return (hint === "uk" || hint === "ru") ? hint : "ru";
    if (/[\u4e00-\u9fff]/.test(text)) return "zh-CN";
    return hint && !/^(uk|ru|zh)/.test(hint) ? hint : "en";
  }
  function setText(node, text, textLang) {
    // textLang: BCP47 of `text`; wraps Latin runs as lang="en" when text is Cyrillic/Chinese
    node.textContent = "";
    text = text == null ? "" : String(text);
    if (!/^(uk|ru|zh)/.test(textLang || "") || !/[A-Za-z]/.test(text)) { node.textContent = text; return; }
    var last = 0, m; LATIN_RUN.lastIndex = 0;
    while ((m = LATIN_RUN.exec(text))) {
      var w = m[0].replace(/[\-.'’]+$/, "");
      if (!w) continue;
      if (m.index > last) node.appendChild(document.createTextNode(text.slice(last, m.index)));
      var sp = document.createElement("span"); sp.lang = "en"; sp.setAttribute("translate", "no"); sp.textContent = w;
      node.appendChild(sp);
      last = m.index + w.length; LATIN_RUN.lastIndex = last;
    }
    if (last < text.length) node.appendChild(document.createTextNode(text.slice(last)));
  }

  var yr = $("yr"); if (yr) yr.textContent = new Date().getFullYear();

  // ---------- Products render (whole card links to Etsy / GitHub) ----------
  var pl = $("productList");
  var lastCat = null;
  if (pl && typeof PCATS !== "undefined") { // category chips: filter the grid (all shown by default)
    var bar = el("div", "pchips"); bar.setAttribute("role", "toolbar"); bar.setAttribute("aria-label", "Product categories"); bar.lang = "en";
    [["all", "All"]].concat(PCATS).forEach(function (c) {
      var n = c[0] === "all" ? PRODUCTS.length : PRODUCTS.filter(function (p) { return p.cat === c[0]; }).length;
      if (!n) return;
      var b = el("button", "pchip"); b.type = "button"; b.setAttribute("data-cat", c[0]); b.setAttribute("aria-pressed", c[0] === "all" ? "true" : "false");
      b.appendChild(document.createTextNode(c[1] + " ")); b.appendChild(el("span", null, String(n)));
      b.addEventListener("click", function () {
        Array.prototype.forEach.call(bar.children, function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
        Array.prototype.forEach.call(pl.children, function (x) { var k = x.getAttribute("data-cat"); x.hidden = !(c[0] === "all" || k === c[0]); });
      });
      bar.appendChild(b);
    });
    pl.parentNode.insertBefore(bar, pl);
  }
  if (pl) PRODUCTS.forEach(function (p) {
    if (p.cat && p.cat !== lastCat && typeof PCATS !== "undefined") {
      lastCat = p.cat;
      var nm = PCATS.filter(function (c) { return c[0] === p.cat; })[0];
      var hd = el("h3", "pcat", nm ? nm[1] : p.cat); hd.lang = "en"; hd.setAttribute("data-cat", p.cat); pl.appendChild(hd);
    }
    var card = el("article", "prod"); if (p.cat) card.setAttribute("data-cat", p.cat);
    var imgBox = el("a", "img");
    imgBox.href = p.url; imgBox.target = "_blank"; imgBox.rel = "noopener noreferrer"; imgBox.tabIndex = -1;
    imgBox.setAttribute("aria-hidden", "true");
    if (p.more) {
      imgBox.className = "img more";
      var mk = el("span", "mark", "Etsy"); mk.lang = "en"; mk.setAttribute("translate", "no");
      imgBox.appendChild(mk);
    } else {
      var im = new Image(); im.src = BASE + p.img; im.loading = "lazy"; im.decoding = "async"; im.width = 800; im.height = 450;
      im.alt = p.title || ""; if (p.t) im.setAttribute("data-i18n-alt", p.t);
      imgBox.appendChild(im);
    }
    if (p.free) { var tag = el("span", "tag"); tag.setAttribute("data-i18n", "prod.free"); imgBox.appendChild(tag); }
    var body = el("div", "body");
    var h = el("h3");
    var ha = el("a", "plink", p.title || ""); if (p.t) ha.setAttribute("data-i18n", p.t); else { ha.lang = "en"; ha.setAttribute("translate", "no"); }
    ha.href = p.url; ha.target = "_blank"; ha.rel = "noopener noreferrer";
    h.appendChild(ha);
    var d = el("p"); if (p.desc) { d.textContent = p.desc; d.lang = "en"; } else d.setAttribute("data-i18n", p.d);
    body.appendChild(h); body.appendChild(d);
    var row = el("div", "row");
    if (!p.more) {
      var pr = el("span", p.free ? "price free" : "price", p.free ? "" : p.price);
      if (p.free) pr.setAttribute("data-i18n", "prod.free");
      row.appendChild(pr);
    }
    var a = el("a", "btn " + (p.free ? "btn-ghost" : "btn-gold"));
    if (p.etsyOnly) { a.textContent = "Buy on Etsy"; a.lang = "en"; a.setAttribute("translate", "no"); } else if (p.patreon && !p.free) { a.textContent = "Buy on Etsy"; a.lang="en"; } else if (p.patreon && p.free) { a.textContent = "Etsy"; a.lang="en"; } else if (p.ctaText) { a.textContent = p.ctaText; a.lang = "en"; a.setAttribute("translate", "no"); } else a.setAttribute("data-i18n", p.cta || "prod.buy");
    a.href = p.url; a.target = "_blank"; a.rel = "noopener noreferrer";
    row.appendChild(a);
    if (!p.more && !p.patreon && !p.etsyOnly && !p.free) {
      var ea = el("a", "btn btn-ghost", "Etsy"); ea.lang = "en"; ea.setAttribute("translate", "no");
      ea.href = p.etsy || "https://marketpulsestudio.etsy.com"; ea.target = "_blank"; ea.rel = "noopener noreferrer";
      row.appendChild(ea);
    }
    body.appendChild(row);
    card.appendChild(imgBox); card.appendChild(body);
    pl.appendChild(card);
  });

  // ---------- i18n ----------
  var onLang = [];
  function setMeta(sel, val) { var m = document.querySelector(sel); if (m) m.setAttribute("content", val); }
  var PAGE_LANG = document.body ? document.body.getAttribute("data-page-lang") : null; // guides: language of the page content
  function apply(code, noSave) {
    if (!T[code]) code = "en";
    cur = code;
    var L = LANGS.filter(function (l) { return l.code === code; })[0];
    document.documentElement.lang = L.html;
    if (!(document.body && document.body.hasAttribute("data-static-meta"))) setMeta('meta[property="og:locale"]', L.og);
    try { // keep ?lang= in the address so reload / shared links / read-aloud start in this language
      var u = new URL(location.href);
      if (u.searchParams.get("lang") !== code) { u.searchParams.set("lang", code); history.replaceState(null, "", u.pathname + u.search + u.hash); }
    } catch (e) {}
    // pages with their own static SEO title/description (guides) keep them
    if (!(document.body && document.body.hasAttribute("data-static-meta"))) {
      document.title = tr((document.body && document.body.getAttribute("data-title")) || "title");
      setMeta('meta[name="description"]', tr("desc"));
      setMeta('meta[property="og:title"]', document.title);
      setMeta('meta[property="og:description"]', tr("desc"));
    }
    Array.prototype.forEach.call(document.querySelectorAll("[data-i18n]"), function (n) {
      setText(n, tr(n.getAttribute("data-i18n")), L.html);
    });
    Array.prototype.forEach.call(document.querySelectorAll("[data-i18n-alt]"), function (n) {
      n.alt = tr(n.getAttribute("data-i18n-alt"));
    });
    Array.prototype.forEach.call(document.querySelectorAll("[data-i18n-aria]"), function (n) {
      n.setAttribute("aria-label", tr(n.getAttribute("data-i18n-aria")));
    });
    var lc = $("langCur"); if (lc) { lc.textContent = L.short; lc.lang = /[A-Za-z]/.test(L.short) ? "en" : L.html; lc.setAttribute("translate", "no"); }
    var lbtn = $("langBtn"); if (lbtn) lbtn.setAttribute("aria-label", tr("lang") + ": " + L.name);
    var menu = $("langMenu");
    if (menu) {
      menu.setAttribute("aria-label", tr("lang"));
      Array.prototype.forEach.call(menu.querySelectorAll(".lang-opt"), function (b) {
        b.setAttribute("aria-checked", b.getAttribute("data-lang") === code ? "true" : "false");
      });
    }
    // Guides links follow the language: Russian guides for RU, English guides otherwise
    Array.prototype.forEach.call(document.querySelectorAll('a[data-i18n="nav.guides"], a[data-guides-link]'), function (a) {
      a.setAttribute("href", code === "en" ? "/guides/" : "/guides/" + code + "/");
    });
    if (!noSave) { try { localStorage.setItem("mp_lang", code); } catch (e) {} }
    onLang.forEach(function (f) { f(); });
  }
  function detect() {
    try { var q = new URLSearchParams(location.search).get("lang"); if (q && T[q]) return q; } catch (e) {}
    if (PAGE_LANG && PAGE_LANG !== "en" && T[PAGE_LANG]) return PAGE_LANG; // translated guide page: its language (not saved as a preference)
    try { var s = localStorage.getItem("mp_lang"); if (s && T[s]) return s; } catch (e) {}
    var list = (navigator.languages && navigator.languages.length) ? navigator.languages : [navigator.language || "en"];
    for (var i = 0; i < list.length; i++) {
      var c = String(list[i] || "").toLowerCase().split("-")[0];
      if (c === "ua") c = "uk";
      if (T[c]) return c;
    }
    return "en";
  }

  function startLang() {
    var c = detect(), q = null;
    try { q = new URLSearchParams(location.search).get("lang"); } catch (e) {}
    apply(c, !!PAGE_LANG && PAGE_LANG !== "en" && !(q && T[q])); // landing on a translated guide doesn't overwrite the saved choice
  }

  // ---------- Language switcher: dropdown in the header (order = LANGS: UK, EN, FR, DE, 中文, RU) ----------
  var langBtn = $("langBtn"), langMenu = $("langMenu"), langDD = $("langDD");
  function opts() { return Array.prototype.slice.call(langMenu.querySelectorAll(".lang-opt")); }
  function openMenu(focusCur) {
    langMenu.hidden = false; langBtn.setAttribute("aria-expanded", "true");
    if (focusCur) { var o = opts(), c = langMenu.querySelector('[aria-checked="true"]') || o[0]; c.focus(); }
  }
  function closeMenu(refocus) {
    if (langMenu.hidden) return;
    langMenu.hidden = true; langBtn.setAttribute("aria-expanded", "false");
    if (refocus) langBtn.focus();
  }
  if (langBtn && langMenu) {
    LANGS.forEach(function (l) {
      var li = el("li"); li.setAttribute("role", "none");
      var b = el("button", "lang-opt"); b.type = "button";
      b.setAttribute("role", "menuitemradio"); b.setAttribute("data-lang", l.code); b.setAttribute("lang", l.html);
      b.appendChild(el("b", null, l.short)); b.appendChild(el("span", null, l.name));
      b.addEventListener("click", function () {
        apply(l.code); closeMenu(true);
        // guides exist in every site language: switching language opens the matching version of the same page
        var want = document.body.getAttribute("data-alt-" + l.code) ? l.code : "en";
        if (PAGE_LANG && PAGE_LANG !== want) {
          var to = document.body.getAttribute("data-alt-" + want);
          if (to) location.href = to + "?lang=" + l.code + location.hash;
        }
      });
      li.appendChild(b); langMenu.appendChild(li);
    });
    langBtn.addEventListener("click", function () { if (langMenu.hidden) openMenu(false); else closeMenu(false); });
    langBtn.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown" || e.key === "ArrowUp") { e.preventDefault(); openMenu(true); }
    });
    langMenu.addEventListener("keydown", function (e) {
      var o = opts(), i = o.indexOf(document.activeElement);
      if (e.key === "ArrowDown") { e.preventDefault(); o[(i + 1) % o.length].focus(); }
      else if (e.key === "ArrowUp") { e.preventDefault(); o[(i - 1 + o.length) % o.length].focus(); }
      else if (e.key === "Home") { e.preventDefault(); o[0].focus(); }
      else if (e.key === "End") { e.preventDefault(); o[o.length - 1].focus(); }
      else if (e.key === "Tab") { closeMenu(false); }
    });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !langMenu.hidden) closeMenu(true); });
    document.addEventListener("click", function (e) { if (!langDD.contains(e.target)) closeMenu(false); });
  }

  // ---------- News feed (same-origin data/news.json, no third-party scripts) ----------
  var SECS = ["all", "market", "world", "politics", "ukraine"];
  var MAX_PER_TAB = 30;
  var newsData = null, curTab = "all", loadState = "loading";
  var listEl = $("newsList"), tabsEl = $("newsTabs"), updEl = $("newsUpdated");
  if (!listEl || !tabsEl) { startLang(); return; } // pages without the feed (terms.html)
  try { var st = sessionStorage.getItem("mp_tab"); if (st && SECS.indexOf(st) >= 0) curTab = st; } catch (e) {}
  var dTab = listEl.getAttribute("data-tab"); if (dTab && SECS.indexOf(dTab) >= 0) curTab = dTab; // e.g. markets page opens on Markets

  function safeUrl(u) { return (typeof u === "string" && /^https?:\/\//i.test(u)) ? u : null; }
  function locale() { var L = LANGS.filter(function (l) { return l.code === cur; })[0]; return L ? L.html : "en"; }
  function rel(ts) {
    var diff = ts - Date.now() / 1000, a = Math.abs(diff);
    var u = a < 3600 ? ["minute", 60] : a < 86400 ? ["hour", 3600] : ["day", 86400];
    var v = Math.round(diff / u[1]); if (u[0] === "minute" && v === 0) v = -1;
    try { return new Intl.RelativeTimeFormat(locale(), { numeric: "auto" }).format(v, u[0]); }
    catch (e) { return new Date(ts * 1000).toLocaleString(); }
  }
  function absDate(ts) {
    try { return new Date(ts * 1000).toLocaleString(locale(), { dateStyle: "medium", timeStyle: "short" }); }
    catch (e) { return new Date(ts * 1000).toISOString(); }
  }
  function itemsFor(tab) {
    if (!newsData) return [];
    var rss = (newsData.items || []).map(function (i) { return { kind: "rss", title: i.title, t: i.t, lang: i.lang, url: i.url, ts: i.ts, source: i.source, sec: i.sec || [] }; });
    var out = (tab === "all") ? rss : rss.filter(function (i) { return i.sec.indexOf(tab) >= 0; });
    out = out.filter(function (i) { return safeUrl(i.url) && i.title; });
    out.sort(function (a, b) { return (b.ts || 0) - (a.ts || 0); });
    return out.slice(0, tab === "all" ? 40 : MAX_PER_TAB);
  }

  function card(it) {
    var a = el("a", "ni");
    a.href = safeUrl(it.url); a.target = "_blank"; a.rel = "noopener noreferrer";
    var meta = el("span", "ni-meta");
    var src = el("b", "ni-src", it.source);
    src.lang = "en"; src.setAttribute("translate", "no"); // publisher names: BBC, Reuters, The Guardian…
    meta.appendChild(src);
    if (it.ts) {
      meta.appendChild(document.createTextNode(" · "));
      var t = el("time", null, rel(it.ts)); t.dateTime = new Date(it.ts * 1000).toISOString(); t.title = absDate(it.ts);
      meta.appendChild(t);
    }
    a.appendChild(meta);
    // headline in the current site language (machine translation built into news.json), else the original
    var tt = it.t && typeof it.t[cur] === "string" && it.t[cur] ? it.t[cur] : null;
    // lang = language of the text actually shown (never inherit the UI language blindly)
    var shownLang = tt ? scriptLang(tt, locale()) : scriptLang(it.title, it.lang || "en");
    var span = el("span", "ni-t"); span.lang = shownLang;
    setText(span, tt || it.title, shownLang);
    a.appendChild(span);
    return a;
  }

  function render() {
    Array.prototype.forEach.call(tabsEl.querySelectorAll("button"), function (b) {
      var on = b.getAttribute("data-tab") === curTab;
      b.setAttribute("aria-selected", on ? "true" : "false"); b.tabIndex = on ? 0 : -1;
    });
    var keepScroll = listEl.scrollTop;
    listEl.textContent = "";
    if (loadState !== "ok") {
      listEl.appendChild(el("p", "ni-state", tr(loadState === "error" ? "news.error" : "news.loading")));
      updEl.textContent = "";
      return;
    }
    var items = itemsFor(curTab);
    if (!items.length) listEl.appendChild(el("p", "ni-state", tr("news.empty")));
    items.forEach(function (it) { listEl.appendChild(card(it)); });
    listEl.scrollTop = keepScroll;
    updEl.textContent = newsData.updated ? tr("news.updated") + " " + rel(newsData.updated) : "";
    if (newsData.updated) updEl.title = absDate(newsData.updated);
  }

  SECS.forEach(function (s) {
    var b = el("button", "tab"); b.type = "button"; b.setAttribute("role", "tab"); b.setAttribute("data-tab", s);
    b.setAttribute("aria-controls", "newsList");
    b.setAttribute("data-i18n", "tab." + s);
    b.addEventListener("click", function () {
      curTab = s; try { sessionStorage.setItem("mp_tab", s); } catch (e) {}
      render(); listEl.scrollTop = 0;
    });
    tabsEl.appendChild(b);
  });
  tabsEl.addEventListener("keydown", function (e) {
    if (e.key !== "ArrowRight" && e.key !== "ArrowLeft") return;
    var i = SECS.indexOf(curTab) + (e.key === "ArrowRight" ? 1 : -1);
    curTab = SECS[(i + SECS.length) % SECS.length]; render();
    var b = tabsEl.querySelector('[data-tab="' + curTab + '"]'); if (b) b.focus();
  });
  onLang.push(function () { tabsEl.setAttribute("aria-label", tr("news.tabs")); render(); });

  startLang();

  function load() {
    var bucket = Math.floor(Date.now() / 300000); // refresh at most every 5 min (cache-busting)
    fetch(BASE + "data/news.json?v=" + bucket, { cache: "no-cache" })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (d) { newsData = d; loadState = "ok"; render(); })
      .catch(function () { if (!newsData) { loadState = "error"; render(); } });
  }
  load();
  setInterval(load, 10 * 60 * 1000);
  setInterval(function () { if (loadState === "ok") render(); }, 60 * 1000);
  // ---------- Quotes strip (same-origin data/quotes.json written by a GitHub Action from Yahoo Finance) ----------
  var qRow = $("qRow"), qNote = $("qNote"), qSec = $("quotes"), quotes = null;
  var Q_NAMES = { gold: "q.gold", eurusd: "EUR/USD", wti: "q.wti", spx: "S&P 500", ndx: "Nasdaq", vti: "VTI" };
  function nf(v, d, sign) {
    var s = new Intl.NumberFormat(locale(), { minimumFractionDigits: d, maximumFractionDigits: d }).format(Math.abs(v));
    return (sign ? (v > 0 ? "+" : v < 0 ? "\u2212" : "") : (v < 0 ? "\u2212" : "")) + s;
  }
  function sparkSvg(pts, cls) {
    var NS = "http://www.w3.org/2000/svg", svg = document.createElementNS(NS, "svg");
    svg.setAttribute("class", "qs"); svg.setAttribute("viewBox", "0 0 56 22"); svg.setAttribute("aria-hidden", "true"); svg.setAttribute("focusable", "false");
    if (pts && pts.length > 1) {
      var mn = Math.min.apply(null, pts), mx = Math.max.apply(null, pts), rg = (mx - mn) || 1;
      var d = pts.map(function (v, i) { return (i * 56 / (pts.length - 1)).toFixed(1) + "," + (20 - (v - mn) / rg * 18).toFixed(1); }).join(" ");
      var pl = document.createElementNS(NS, "polyline");
      pl.setAttribute("points", d); pl.setAttribute("fill", "none"); pl.setAttribute("stroke-width", "1.4"); pl.setAttribute("stroke-linejoin", "round");
      pl.setAttribute("stroke", cls === "up" ? "#8cc79a" : cls === "dn" ? "#e08a7e" : "#9a978f");
      svg.appendChild(pl);
    }
    return svg;
  }
  function renderQuotes() {
    if (!qRow || !quotes) return;
    var order = (quotes.order || Object.keys(quotes.q || {})).filter(function (k) { return quotes.q[k] && typeof quotes.q[k].price === "number"; });
    if (!order.length) { if (qSec) qSec.hidden = true; return; }
    qSec.hidden = false; qRow.textContent = "";
    var now = Date.now() / 1000, allClosed = true;
    order.forEach(function (k) {
      var q = quotes.q[k], li = el("li"), a = el("a", "qi");
      a.href = "https://finance.yahoo.com/quote/" + encodeURIComponent(q.sym) + "/"; a.target = "_blank"; a.rel = "noopener noreferrer";
      var key = Q_NAMES[k] || k, name = key.indexOf("q.") === 0 ? tr(key) : key;
      var n = el("span", "qn"); setText(n, name, key.indexOf("q.") === 0 ? locale() : "en"); if (key.indexOf("q.") !== 0) { n.lang = "en"; n.setAttribute("translate", "no"); }
      var cls = q.ch > 0 ? "up" : q.ch < 0 ? "dn" : "fl";
      var p = el("span", "qp", nf(q.price, q.dec, false));
      var c = el("span", "qc " + cls, nf(q.ch, q.dec, true) + " (" + nf(q.pct, 2, true) + "%)");
      a.appendChild(n); a.appendChild(p); a.appendChild(sparkSvg(q.spark, cls)); a.appendChild(c);
      var stale = q.time && now - q.time > 3 * 3600; if (!stale) allClosed = false;
      a.title = name + ": " + nf(q.price, q.dec, false) + (q.cur ? " " + q.cur : "") + " · " + absDate(q.time) + (stale ? " · " + tr("q.closed") : "");
      a.setAttribute("aria-label", a.title + " · " + tr("q.open"));
      li.appendChild(a); qRow.appendChild(li);
    });
    qNote.textContent = "";
    var asof = quotes.asof ? new Date(quotes.asof * 1000).toLocaleString(locale(), { day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" }) : "";
    setText(qNote, tr("q.note") + " " + asof + (allClosed ? " · " + tr("q.closed") : "") + ". ", locale());
    var src = el("a", null, "finance.yahoo.com"); src.href = "https://finance.yahoo.com/markets/"; src.target = "_blank"; src.rel = "noopener noreferrer"; src.lang = "en"; src.setAttribute("translate", "no");
    qNote.appendChild(src);
  }
  function loadQuotes() {
    fetch(BASE + "data/quotes.json?t=" + Math.floor(Date.now() / 60000), { cache: "no-store" })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (d) { if (d && d.q) { quotes = d; renderQuotes(); } })
      .catch(function () { if (!quotes && qSec) qSec.hidden = true; }); // keep last values on a failed refresh
  }
  if (qRow) {
    onLang.push(renderQuotes);
    loadQuotes();
    setInterval(loadQuotes, 60 * 1000);
  }
})();
