/* Market Plus — vanilla JS, no trackers, no build */
(function () {
  "use strict";

  var X_URL = "https://x.com/MarketPulseGold";

  // ---------- Translations ----------
  var LANGS = [
    { code: "en", short: "EN", name: "English", html: "en", x: "en" },
    { code: "ru", short: "RU", name: "Русский", html: "ru", x: "ru" },
    { code: "uk", short: "UK", name: "Українська", html: "uk", x: "uk" },
    { code: "fr", short: "FR", name: "Français", html: "fr", x: "fr" },
    { code: "de", short: "DE", name: "Deutsch", html: "de", x: "de" },
    { code: "zh", short: "中文", name: "中文（简体）", html: "zh-CN", x: "zh-cn" }
  ];

  var T = {
    en: {
      title: "Market Plus — markets, gold, forex & macro news without the fluff",
      desc: "Market Plus: concise news on markets, gold, forex, oil and macroeconomics. Live feed from X, trading and finance tools.",
      lang: "Language",
      "nav.news": "News", "nav.products": "Products", "nav.about": "About",
      "hero.badge": "● Market Plus · live news from X",
      "hero.h1a": "Markets, gold, forex & macro news",
      "hero.h1b": "without the fluff",
      "hero.lead": "Market Plus covers the events that actually move markets — briefly and to the point: what happened and how it may affect gold, the dollar, oil and risk assets.",
      "hero.cta": "Follow on X", "hero.cta2": "Latest news", "hero.cta3": "Products",
      "stat.1": "gold & currencies", "stat.2b": "Macro", "stat.2": "Fed, inflation, oil", "stat.3b": "Live", "stat.3": "news feed from X",
      "about.h": "About",
      "about.sub": "Market Plus is a markets news project for people who want the signal, not the noise.",
      "about.t1h": "Only what matters", "about.t1p": "Geopolitics, central bank decisions, inflation and jobs data — the things that move gold and currencies.",
      "about.t2h": "With context", "about.t2p": "Every headline comes with a short takeaway: how the event may affect the market and why.",
      "about.t3h": "Source included", "about.t3p": "Reuters, Bloomberg, official statements — the original is always one tap away.",
      "news.h": "Latest news",
      "news.sub": "Live feed from our X account — new posts appear here automatically.",
      "news.live": "Live", "news.loading": "Loading posts from X…",
      "fb.h": "Latest posts on X",
      "fb.p": "The live feed couldn't load in your browser — X sometimes limits embeds for visitors who aren't signed in, or a privacy blocker is on. All posts are available on X.",
      "fb.btn": "Open @MarketPulseGold on X",
      "news.hint": "Feed empty? Some browsers and extensions block X embeds.",
      "prod.h": "Products",
      "prod.sub": "Tools for trading, personal finance and business. Payment and download on Patreon.",
      "prod.note": "Buttons open Patreon or GitHub pages. This site does not collect or store any data.",
      "prod.buy": "Buy on Patreon", "prod.get": "Get it free", "prod.github": "Open on GitHub", "prod.free": "Free",
      "p1.d": "10 ready-made AI skills for Claude & ChatGPT: marketing, sales, support, SEO, HR and a content calendar. PDF guide included.",
      "p2.d": "Trade journal with automatic stats: win rate, R-multiple, P&L, dashboard and mistake analysis. Google Sheets and Excel.",
      "p3.d": "Personal budget spreadsheet for 2026: income, expenses by category, savings goals and clear monthly charts.",
      "p4.d": "Free lightweight version of the trading journal — start tracking your trade stats today.",
      "p5.d": "Free simple budget tracker: income, expenses and balance in one sheet.",
      "p6.t": "3 free AI skills for business",
      "p6.d": "Three free AI skills from the pack in an open GitHub repository. Try them before buying the full version.",
      "foot.na": "Not investment advice.",
      "foot.disc": "All content is for informational purposes only. Trading in financial markets involves risk of loss.",
      "foot.priv": "No trackers, no forms, no data collection."
    },
    ru: {
      title: "Market Plus — рынки, золото, форекс и макро без воды",
      desc: "Market Plus: короткие новости о рынках, золоте, форексе, нефти и макроэкономике. Живая лента из X, инструменты для трейдинга и финансов.",
      lang: "Язык",
      "nav.news": "Новости", "nav.products": "Продукты", "nav.about": "О проекте",
      "hero.badge": "● Market Plus · живая лента из X",
      "hero.h1a": "Рынки, золото, форекс и макро",
      "hero.h1b": "без воды",
      "hero.lead": "Market Plus — о событиях, которые действительно двигают рынок, коротко и по делу: что произошло и как это может повлиять на золото, доллар, нефть и рисковые активы.",
      "hero.cta": "Читать в X", "hero.cta2": "Последние новости", "hero.cta3": "Продукты",
      "stat.1": "золото и валюты", "stat.2b": "Макро", "stat.2": "ФРС, инфляция, нефть", "stat.3b": "Онлайн", "stat.3": "лента новостей из X",
      "about.h": "О проекте",
      "about.sub": "Market Plus — новостной проект о рынках для тех, кому нужна суть, а не шум.",
      "about.t1h": "Только важное", "about.t1p": "Геополитика, решения центробанков, данные по инфляции и занятости — всё, что двигает золото и валюты.",
      "about.t2h": "С контекстом", "about.t2p": "К каждой новости — короткий вывод: как событие может отразиться на рынке и почему.",
      "about.t3h": "Со ссылкой на источник", "about.t3p": "Reuters, Bloomberg, официальные заявления — оригинал всегда в одно касание.",
      "news.h": "Последние новости",
      "news.sub": "Живая лента нашего аккаунта в X — новые посты появляются здесь автоматически.",
      "news.live": "Онлайн", "news.loading": "Загружаем посты из X…",
      "fb.h": "Свежие посты в X",
      "fb.p": "Лента не загрузилась в вашем браузере — X иногда ограничивает встраивание для гостей без входа в аккаунт, либо включён блокировщик. Все посты доступны в X.",
      "fb.btn": "Открыть @MarketPulseGold в X",
      "news.hint": "Лента пустая? Некоторые браузеры и расширения блокируют виджеты X.",
      "prod.h": "Продукты",
      "prod.sub": "Инструменты для трейдинга, личных финансов и бизнеса. Оплата и скачивание — на Patreon.",
      "prod.note": "Кнопки ведут на страницы Patreon или GitHub. Сайт не собирает и не хранит никаких данных.",
      "prod.buy": "Купить на Patreon", "prod.get": "Скачать бесплатно", "prod.github": "Открыть на GitHub", "prod.free": "Бесплатно",
      "p1.d": "10 готовых AI-навыков для Claude и ChatGPT: маркетинг, продажи, поддержка, SEO, HR и контент-календарь. PDF-гайд в комплекте.",
      "p2.d": "Журнал сделок с автоматической статистикой: win rate, R-multiple, P&L, дашборд и разбор ошибок. Google Sheets и Excel.",
      "p3.d": "Таблица личного бюджета на 2026 год: доходы, расходы по категориям, цели накоплений и наглядные графики по месяцам.",
      "p4.d": "Бесплатная облегчённая версия журнала трейдера — начните вести статистику сделок уже сегодня.",
      "p5.d": "Бесплатный простой трекер бюджета: доходы, расходы и остаток в одной таблице.",
      "p6.t": "3 бесплатных AI-навыка для бизнеса",
      "p6.d": "Три бесплатных AI-навыка из пакета в открытом репозитории на GitHub. Попробуйте перед покупкой полной версии.",
      "foot.na": "Не является инвестиционной рекомендацией.",
      "foot.disc": "Все материалы носят исключительно ознакомительный характер. Торговля на финансовых рынках связана с риском потери средств.",
      "foot.priv": "Без трекеров, без форм, без сбора данных."
    },
    uk: {
      title: "Market Plus — ринки, золото, форекс і макро без води",
      desc: "Market Plus: стислі новини про ринки, золото, форекс, нафту та макроекономіку. Жива стрічка з X, інструменти для трейдингу й фінансів.",
      lang: "Мова",
      "nav.news": "Новини", "nav.products": "Продукти", "nav.about": "Про проєкт",
      "hero.badge": "● Market Plus · жива стрічка з X",
      "hero.h1a": "Ринки, золото, форекс і макро",
      "hero.h1b": "без води",
      "hero.lead": "Market Plus — про події, які справді рухають ринок, коротко й по суті: що сталося і як це може вплинути на золото, долар, нафту та ризикові активи.",
      "hero.cta": "Читати в X", "hero.cta2": "Останні новини", "hero.cta3": "Продукти",
      "stat.1": "золото й валюти", "stat.2b": "Макро", "stat.2": "ФРС, інфляція, нафта", "stat.3b": "Онлайн", "stat.3": "стрічка новин з X",
      "about.h": "Про проєкт",
      "about.sub": "Market Plus — новинний проєкт про ринки для тих, кому потрібна суть, а не шум.",
      "about.t1h": "Лише важливе", "about.t1p": "Геополітика, рішення центробанків, дані щодо інфляції та зайнятості — усе, що рухає золото й валюти.",
      "about.t2h": "З контекстом", "about.t2p": "До кожної новини — короткий висновок: як подія може позначитися на ринку і чому.",
      "about.t3h": "З посиланням на джерело", "about.t3p": "Reuters, Bloomberg, офіційні заяви — оригінал завжди в один дотик.",
      "news.h": "Останні новини",
      "news.sub": "Жива стрічка нашого акаунта в X — нові пости з'являються тут автоматично.",
      "news.live": "Онлайн", "news.loading": "Завантажуємо пости з X…",
      "fb.h": "Свіжі пости в X",
      "fb.p": "Стрічка не завантажилася у вашому браузері — X іноді обмежує вбудовування для гостей без входу в акаунт, або ввімкнено блокувальник. Усі пости доступні в X.",
      "fb.btn": "Відкрити @MarketPulseGold в X",
      "news.hint": "Стрічка порожня? Деякі браузери та розширення блокують віджети X.",
      "prod.h": "Продукти",
      "prod.sub": "Інструменти для трейдингу, особистих фінансів і бізнесу. Оплата та завантаження — на Patreon.",
      "prod.note": "Кнопки ведуть на сторінки Patreon або GitHub. Сайт не збирає й не зберігає жодних даних.",
      "prod.buy": "Купити на Patreon", "prod.get": "Завантажити безкоштовно", "prod.github": "Відкрити на GitHub", "prod.free": "Безкоштовно",
      "p1.d": "10 готових AI-навичок для Claude і ChatGPT: маркетинг, продажі, підтримка, SEO, HR і контент-календар. PDF-посібник у комплекті.",
      "p2.d": "Журнал угод з автоматичною статистикою: win rate, R-multiple, P&L, дашборд і розбір помилок. Google Sheets та Excel.",
      "p3.d": "Таблиця особистого бюджету на 2026 рік: доходи, витрати за категоріями, цілі заощаджень і наочні графіки по місяцях.",
      "p4.d": "Безкоштовна полегшена версія журналу трейдера — почніть вести статистику угод уже сьогодні.",
      "p5.d": "Безкоштовний простий трекер бюджету: доходи, витрати й залишок в одній таблиці.",
      "p6.t": "3 безкоштовні AI-навички для бізнесу",
      "p6.d": "Три безкоштовні AI-навички з пакета у відкритому репозиторії на GitHub. Спробуйте перед купівлею повної версії.",
      "foot.na": "Не є інвестиційною порадою.",
      "foot.disc": "Усі матеріали мають виключно ознайомчий характер. Торгівля на фінансових ринках пов'язана з ризиком втрати коштів.",
      "foot.priv": "Без трекерів, без форм, без збору даних."
    },
    fr: {
      title: "Market Plus — marchés, or, forex et macro, sans blabla",
      desc: "Market Plus : l'essentiel de l'actualité des marchés, de l'or, du forex, du pétrole et de la macroéconomie. Fil en direct depuis X, outils de trading et de finances.",
      lang: "Langue",
      "nav.news": "Actus", "nav.products": "Produits", "nav.about": "À propos",
      "hero.badge": "● Market Plus · l'actu en direct depuis X",
      "hero.h1a": "Marchés, or, forex et macro",
      "hero.h1b": "sans blabla",
      "hero.lead": "Market Plus suit les événements qui font vraiment bouger les marchés, en bref et sans détour : ce qui s'est passé et l'impact possible sur l'or, le dollar, le pétrole et les actifs risqués.",
      "hero.cta": "Suivre sur X", "hero.cta2": "Dernières actus", "hero.cta3": "Produits",
      "stat.1": "or et devises", "stat.2b": "Macro", "stat.2": "Fed, inflation, pétrole", "stat.3b": "Direct", "stat.3": "fil d'actu depuis X",
      "about.h": "À propos",
      "about.sub": "Market Plus est un projet d'actualité des marchés pour ceux qui veulent l'essentiel, pas le bruit.",
      "about.t1h": "L'essentiel uniquement", "about.t1p": "Géopolitique, décisions des banques centrales, chiffres de l'inflation et de l'emploi — ce qui fait bouger l'or et les devises.",
      "about.t2h": "Avec du contexte", "about.t2p": "Chaque info s'accompagne d'une courte analyse : l'impact possible sur le marché, et pourquoi.",
      "about.t3h": "Source à l'appui", "about.t3p": "Reuters, Bloomberg, communiqués officiels — l'original est toujours à portée de clic.",
      "news.h": "Dernières actus",
      "news.sub": "Fil en direct de notre compte X — les nouveaux posts s'affichent ici automatiquement.",
      "news.live": "Direct", "news.loading": "Chargement des posts depuis X…",
      "fb.h": "Derniers posts sur X",
      "fb.p": "Le fil n'a pas pu se charger dans votre navigateur — X limite parfois les intégrations pour les visiteurs non connectés, ou un bloqueur est actif. Tous les posts sont disponibles sur X.",
      "fb.btn": "Ouvrir @MarketPulseGold sur X",
      "news.hint": "Fil vide ? Certains navigateurs et extensions bloquent les intégrations X.",
      "prod.h": "Produits",
      "prod.sub": "Des outils pour le trading, les finances personnelles et l'entreprise. Paiement et téléchargement sur Patreon.",
      "prod.note": "Les boutons ouvrent des pages Patreon ou GitHub. Ce site ne collecte ni ne stocke aucune donnée.",
      "prod.buy": "Acheter sur Patreon", "prod.get": "Obtenir gratuitement", "prod.github": "Ouvrir sur GitHub", "prod.free": "Gratuit",
      "p1.d": "10 compétences IA prêtes à l'emploi pour Claude et ChatGPT : marketing, ventes, support, SEO, RH et calendrier éditorial. Guide PDF inclus.",
      "p2.d": "Journal de trading avec statistiques automatiques : taux de réussite, R-multiple, P&L, tableau de bord et analyse des erreurs. Google Sheets et Excel.",
      "p3.d": "Tableur de budget personnel 2026 : revenus, dépenses par catégorie, objectifs d'épargne et graphiques mensuels clairs.",
      "p4.d": "Version allégée et gratuite du journal de trading — commencez à suivre vos statistiques dès aujourd'hui.",
      "p5.d": "Suivi de budget simple et gratuit : revenus, dépenses et solde sur une seule feuille.",
      "p6.t": "3 compétences IA gratuites pour l'entreprise",
      "p6.d": "Trois compétences IA gratuites du pack, dans un dépôt GitHub public. Essayez-les avant d'acheter la version complète.",
      "foot.na": "Ceci n'est pas un conseil en investissement.",
      "foot.disc": "Tous les contenus sont fournis à titre informatif uniquement. Le trading sur les marchés financiers comporte un risque de perte.",
      "foot.priv": "Aucun traceur, aucun formulaire, aucune collecte de données."
    },
    de: {
      title: "Market Plus — Märkte, Gold, Forex & Makro ohne Schnickschnack",
      desc: "Market Plus: kompakte News zu Märkten, Gold, Forex, Öl und Makroökonomie. Live-Feed von X, Tools für Trading und Finanzen.",
      lang: "Sprache",
      "nav.news": "News", "nav.products": "Produkte", "nav.about": "Über uns",
      "hero.badge": "● Market Plus · Live-News von X",
      "hero.h1a": "Märkte, Gold, Forex & Makro",
      "hero.h1b": "ohne Schnickschnack",
      "hero.lead": "Market Plus berichtet über die Ereignisse, die die Märkte wirklich bewegen — kurz und auf den Punkt: was passiert ist und wie es sich auf Gold, Dollar, Öl und Risikoanlagen auswirken kann.",
      "hero.cta": "Auf X folgen", "hero.cta2": "Aktuelle News", "hero.cta3": "Produkte",
      "stat.1": "Gold & Währungen", "stat.2b": "Makro", "stat.2": "Fed, Inflation, Öl", "stat.3b": "Live", "stat.3": "News-Feed von X",
      "about.h": "Über uns",
      "about.sub": "Market Plus ist ein Marktnachrichten-Projekt für alle, die das Signal statt des Rauschens wollen.",
      "about.t1h": "Nur das Wichtige", "about.t1p": "Geopolitik, Zentralbankentscheidungen, Inflations- und Arbeitsmarktdaten — alles, was Gold und Währungen bewegt.",
      "about.t2h": "Mit Kontext", "about.t2p": "Zu jeder Meldung ein kurzes Fazit: wie das Ereignis den Markt beeinflussen kann und warum.",
      "about.t3h": "Mit Quelle", "about.t3p": "Reuters, Bloomberg, offizielle Mitteilungen — das Original ist immer nur einen Klick entfernt.",
      "news.h": "Aktuelle News",
      "news.sub": "Live-Feed unseres X-Accounts — neue Posts erscheinen hier automatisch.",
      "news.live": "Live", "news.loading": "Posts von X werden geladen…",
      "fb.h": "Neueste Posts auf X",
      "fb.p": "Der Live-Feed konnte in deinem Browser nicht geladen werden — X schränkt Einbettungen für nicht angemeldete Besucher manchmal ein, oder ein Tracking-Blocker ist aktiv. Alle Posts findest du auf X.",
      "fb.btn": "@MarketPulseGold auf X öffnen",
      "news.hint": "Feed leer? Manche Browser und Erweiterungen blockieren X-Einbettungen.",
      "prod.h": "Produkte",
      "prod.sub": "Tools für Trading, private Finanzen und Business. Bezahlung und Download über Patreon.",
      "prod.note": "Die Buttons öffnen Seiten auf Patreon oder GitHub. Diese Website erhebt und speichert keinerlei Daten.",
      "prod.buy": "Auf Patreon kaufen", "prod.get": "Kostenlos holen", "prod.github": "Auf GitHub öffnen", "prod.free": "Kostenlos",
      "p1.d": "10 fertige KI-Skills für Claude & ChatGPT: Marketing, Vertrieb, Support, SEO, HR und Content-Kalender. Inklusive PDF-Anleitung.",
      "p2.d": "Trading-Journal mit automatischer Statistik: Trefferquote, R-Multiple, P&L, Dashboard und Fehleranalyse. Google Sheets und Excel.",
      "p3.d": "Tabelle fürs private Budget 2026: Einnahmen, Ausgaben nach Kategorien, Sparziele und übersichtliche Monatsdiagramme.",
      "p4.d": "Kostenlose Light-Version des Trading-Journals — starte noch heute mit der Statistik deiner Trades.",
      "p5.d": "Kostenloser, einfacher Budget-Tracker: Einnahmen, Ausgaben und Saldo in einer Tabelle.",
      "p6.t": "3 kostenlose KI-Skills fürs Business",
      "p6.d": "Drei kostenlose KI-Skills aus dem Paket in einem öffentlichen GitHub-Repository. Teste sie vor dem Kauf der Vollversion.",
      "foot.na": "Keine Anlageberatung.",
      "foot.disc": "Alle Inhalte dienen ausschließlich Informationszwecken. Der Handel an Finanzmärkten ist mit Verlustrisiken verbunden.",
      "foot.priv": "Keine Tracker, keine Formulare, keine Datenerhebung."
    },
    zh: {
      title: "Market Plus — 市场、黄金、外汇与宏观资讯，只讲干货",
      desc: "Market Plus：简明的市场、黄金、外汇、原油与宏观经济资讯。来自 X 的实时动态，以及交易和理财工具。",
      lang: "语言",
      "nav.news": "资讯", "nav.products": "产品", "nav.about": "关于",
      "hero.badge": "● Market Plus · 来自 X 的实时资讯",
      "hero.h1a": "市场、黄金、外汇与宏观资讯",
      "hero.h1b": "只讲干货",
      "hero.lead": "Market Plus 聚焦真正推动市场的事件，简明扼要：发生了什么，以及它可能如何影响黄金、美元、原油和风险资产。",
      "hero.cta": "在 X 上关注", "hero.cta2": "最新资讯", "hero.cta3": "产品",
      "stat.1": "黄金与外汇", "stat.2b": "宏观", "stat.2": "美联储、通胀、原油", "stat.3b": "实时", "stat.3": "来自 X 的资讯流",
      "about.h": "关于我们",
      "about.sub": "Market Plus 是一个市场资讯项目，为只想要关键信息、不要噪音的人而做。",
      "about.t1h": "只看重点", "about.t1p": "地缘政治、央行决议、通胀与就业数据——这些才是推动黄金和汇率的因素。",
      "about.t2h": "附带背景", "about.t2p": "每条资讯都配有简短解读：事件可能如何影响市场，以及原因。",
      "about.t3h": "注明来源", "about.t3p": "路透社、彭博社、官方声明——原文随时一键可查。",
      "news.h": "最新资讯",
      "news.sub": "我们 X 账号的实时动态——新帖子会自动显示在这里。",
      "news.live": "实时", "news.loading": "正在从 X 加载帖子…",
      "fb.h": "X 上的最新帖子",
      "fb.p": "实时动态未能在您的浏览器中加载——X 有时会限制未登录访客查看嵌入内容，或者您开启了隐私拦截插件。所有帖子均可在 X 上查看。",
      "fb.btn": "在 X 上打开 @MarketPulseGold",
      "news.hint": "动态为空？部分浏览器和扩展会拦截 X 的嵌入内容。",
      "prod.h": "产品",
      "prod.sub": "面向交易、个人理财和企业的实用工具。在 Patreon 上付款和下载。",
      "prod.note": "按钮将打开 Patreon 或 GitHub 页面。本网站不收集、不存储任何数据。",
      "prod.buy": "在 Patreon 购买", "prod.get": "免费获取", "prod.github": "在 GitHub 打开", "prod.free": "免费",
      "p1.d": "10 个适用于 Claude 和 ChatGPT 的现成 AI 技能：营销、销售、客服、SEO、人力资源和内容日历。附 PDF 指南。",
      "p2.d": "交易日志，自动统计胜率、R 倍数、盈亏，附仪表盘和错误分析。支持 Google Sheets 和 Excel。",
      "p3.d": "2026 年个人预算表：收入、分类支出、储蓄目标和清晰的月度图表。",
      "p4.d": "免费精简版交易日志——今天就开始记录你的交易数据。",
      "p5.d": "免费简易预算表：收入、支出和余额尽在一张表中。",
      "p6.t": "3 个免费的商业 AI 技能",
      "p6.d": "来自技能包的三个免费 AI 技能，托管在公开的 GitHub 仓库中。购买完整版前先试用。",
      "foot.na": "不构成投资建议。",
      "foot.disc": "所有内容仅供参考。金融市场交易存在亏损风险。",
      "foot.priv": "无追踪器、无表单、不收集数据。"
    }
  };

  // ---------- Products (edit here) ----------
  var PRODUCTS = [
    { title: "AI Skills Pack for Business", price: "$8", img: "assets/ai-skills.webp", d: "p1.d",
      url: "https://www.patreon.com/DmitryZhuk/posts/ai-skills-pack-173304384" },
    { title: "Trading Journal Pro (Google Sheets & Excel)", price: "$12", img: "assets/trading-journal.webp", d: "p2.d",
      url: "https://www.patreon.com/DmitryZhuk/posts/trading-journal-173290193" },
    { title: "Budget & Expense Tracker 2026", price: "$9", img: "assets/budget-tracker.webp", d: "p3.d",
      url: "https://www.patreon.com/DmitryZhuk/posts/budget-expense-173290094" },
    { title: "Trading Journal Lite", free: true, img: "assets/trading-journal.webp", d: "p4.d", cta: "prod.get",
      url: "https://www.patreon.com/DmitryZhuk/posts/free-trading-173292664" },
    { title: "Budget Lite", free: true, img: "assets/budget-tracker.webp", d: "p5.d", cta: "prod.get",
      url: "https://www.patreon.com/DmitryZhuk/posts/free-budget-lite-173292612" },
    { t: "p6.t", free: true, img: "assets/ai-skills.webp", d: "p6.d", cta: "prod.github",
      url: "https://github.com/aiskillsdrop/ai-skills-for-business" }
  ];

  var $ = function (id) { return document.getElementById(id); };
  var cur = "en";
  function tr(k) { return (T[cur] && T[cur][k]) || T.en[k] || ""; }
  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }
  var yr = $("yr"); if (yr) yr.textContent = new Date().getFullYear();

  // ---------- Products render ----------
  var pl = $("productList");
  PRODUCTS.forEach(function (p) {
    var card = el("article", "prod");
    var imgBox = el("div", "img");
    var im = new Image(); im.src = p.img; im.loading = "lazy"; im.decoding = "async"; im.width = 960; im.height = 540;
    im.alt = p.title || ""; if (p.t) im.setAttribute("data-i18n-alt", p.t);
    imgBox.appendChild(im);
    if (p.free) { var tag = el("span", "tag"); tag.setAttribute("data-i18n", "prod.free"); imgBox.appendChild(tag); }
    var body = el("div", "body");
    var h = el("h3", null, p.title || ""); if (p.t) h.setAttribute("data-i18n", p.t);
    var d = el("p"); d.setAttribute("data-i18n", p.d);
    body.appendChild(h); body.appendChild(d);
    var row = el("div", "row");
    var pr = el("span", p.free ? "price free" : "price", p.free ? "" : p.price);
    if (p.free) pr.setAttribute("data-i18n", "prod.free");
    row.appendChild(pr);
    var a = el("a", "btn " + (p.free ? "btn-ghost" : "btn-gold"));
    a.setAttribute("data-i18n", p.cta || "prod.buy");
    a.href = p.url; a.target = "_blank"; a.rel = "noopener";
    row.appendChild(a);
    body.appendChild(row);
    card.appendChild(imgBox); card.appendChild(body);
    pl.appendChild(card);
  });

  // ---------- i18n ----------
  function setMeta(sel, val) { var m = document.querySelector(sel); if (m) m.setAttribute("content", val); }
  function apply(code) {
    if (!T[code]) code = "en";
    cur = code;
    var L = LANGS.filter(function (l) { return l.code === code; })[0];
    document.documentElement.lang = L.html;
    document.title = tr("title");
    setMeta('meta[name="description"]', tr("desc"));
    setMeta('meta[property="og:title"]', tr("title"));
    setMeta('meta[property="og:description"]', tr("desc"));
    Array.prototype.forEach.call(document.querySelectorAll("[data-i18n]"), function (n) {
      n.textContent = tr(n.getAttribute("data-i18n"));
    });
    Array.prototype.forEach.call(document.querySelectorAll("[data-i18n-alt]"), function (n) {
      n.alt = tr(n.getAttribute("data-i18n-alt"));
    });
    $("langCur").textContent = L.short;
    $("langBtn").setAttribute("aria-label", tr("lang") + ": " + L.name);
    Array.prototype.forEach.call($("langMenu").querySelectorAll("button"), function (b) {
      b.setAttribute("aria-selected", b.getAttribute("data-lang") === code ? "true" : "false");
    });
    try { localStorage.setItem("mp_lang", code); } catch (e) {}
  }
  function detect() {
    try { var s = localStorage.getItem("mp_lang"); if (s && T[s]) return s; } catch (e) {}
    var list = (navigator.languages && navigator.languages.length) ? navigator.languages : [navigator.language || "en"];
    for (var i = 0; i < list.length; i++) {
      var c = String(list[i] || "").toLowerCase().split("-")[0];
      if (c === "ua") c = "uk";
      if (T[c]) return c;
    }
    return "en";
  }

  // ---------- Language dropdown ----------
  var btn = $("langBtn"), menu = $("langMenu");
  LANGS.forEach(function (l) {
    var li = el("li"); li.setAttribute("role", "none");
    var b = el("button"); b.type = "button"; b.setAttribute("role", "option"); b.setAttribute("data-lang", l.code);
    b.setAttribute("lang", l.html);
    b.appendChild(document.createTextNode(l.name)); b.appendChild(el("span", null, l.short));
    b.addEventListener("click", function () { apply(l.code); closeMenu(); btn.focus(); });
    li.appendChild(b); menu.appendChild(li);
  });
  function openMenu() {
    menu.hidden = false; btn.setAttribute("aria-expanded", "true");
    var sel = menu.querySelector('[aria-selected="true"]') || menu.querySelector("button");
    if (sel) sel.focus();
  }
  function closeMenu() { menu.hidden = true; btn.setAttribute("aria-expanded", "false"); }
  btn.addEventListener("click", function (e) { e.stopPropagation(); menu.hidden ? openMenu() : closeMenu(); });
  document.addEventListener("click", function (e) { if (!menu.hidden && !menu.contains(e.target)) closeMenu(); });
  document.addEventListener("keydown", function (e) {
    if (menu.hidden) return;
    var items = Array.prototype.slice.call(menu.querySelectorAll("button"));
    var i = items.indexOf(document.activeElement);
    if (e.key === "Escape") { closeMenu(); btn.focus(); }
    else if (e.key === "ArrowDown") { e.preventDefault(); items[(i + 1) % items.length].focus(); }
    else if (e.key === "ArrowUp") { e.preventDefault(); items[(i - 1 + items.length) % items.length].focus(); }
  });

  apply(detect());

  // ---------- X timeline: lazy-load + fallback ----------
  var box = $("xbox"), feed = $("feed"), skel = $("xskel"), fb = $("xfallback"), tl = $("xtl");
  var started = false, ok = false, timer = null;
  function rendered() {
    var f = box.querySelector("iframe");
    return !!(f && f.offsetHeight > 80);
  }
  function showOk() {
    if (ok) return; ok = true;
    clearTimeout(timer);
    skel.hidden = true; skel.style.display = "none"; fb.hidden = true; feed.classList.remove("failed"); $("news").classList.remove("xfail");
  }
  function showFallback() {
    if (ok) return;
    skel.style.display = "none"; fb.hidden = false; feed.classList.add("failed"); $("news").classList.add("xfail");
  }
  function startX() {
    if (started) return; started = true;
    var L = LANGS.filter(function (l) { return l.code === cur; })[0];
    tl.setAttribute("data-lang", L ? L.x : "en");
    tl.setAttribute("data-height", String(Math.max(420, box.clientHeight || 620)));
    var s = document.createElement("script");
    s.src = "https://platform.twitter.com/widgets.js"; s.async = true; s.charset = "utf-8";
    s.onerror = showFallback;
    s.onload = function () {
      if (window.twttr && twttr.events && twttr.events.bind) {
        twttr.events.bind("rendered", function () { setTimeout(function () { if (rendered()) showOk(); }, 300); });
      }
    };
    document.body.appendChild(s);
    // Poll the DOM too (works even if the events API is unavailable)
    var tries = 0;
    var poll = setInterval(function () {
      tries++;
      if (rendered()) { clearInterval(poll); showOk(); }
      else if (tries > 60) clearInterval(poll);
    }, 500);
    timer = setTimeout(function () { if (!rendered()) showFallback(); }, 6000);
  }
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (en) {
      if (en.some(function (x) { return x.isIntersecting; })) { io.disconnect(); startX(); }
    }, { rootMargin: "600px 0px" });
    io.observe($("news"));
  } else {
    window.addEventListener("load", startX);
  }
})();
