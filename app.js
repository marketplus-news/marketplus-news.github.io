/* Market Plus — vanilla JS, no trackers, no build */
(function () {
  "use strict";

  var X_URL = "https://x.com/MarketPulseGold";

  // ---------- Translations ----------
  var LANGS = [
    { code: "uk", short: "UK", name: "Українська", html: "uk", x: "uk" },
    { code: "en", short: "EN", name: "English", html: "en", x: "en" },
    { code: "fr", short: "FR", name: "Français", html: "fr", x: "fr" },
    { code: "de", short: "DE", name: "Deutsch", html: "de", x: "de" },
    { code: "zh", short: "中文", name: "中文（简体）", html: "zh-CN", x: "zh-cn" },
    { code: "ru", short: "RU", name: "Русский", html: "ru", x: "ru" }
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
      "news.sub": "Headlines on markets, world, politics and Ukraine from open news sources, plus our posts on X. Updated automatically every 30 minutes.",
      "news.live": "Live", "news.loading": "Loading news…",
      "news.hint": "Tap a headline to open the original in a new tab. Headlines appear in their original language.",
      "news.empty": "No news in this section yet — check back soon.",
      "news.error": "Couldn't load the news feed. Please refresh the page.",
      "news.updated": "Updated",
      "news.xsrc": "Post on X",
      "news.posts": "Latest posts",
      "news.tabs": "News sections",
      "tab.all": "All",
      "tab.market": "Markets",
      "tab.world": "World",
      "tab.politics": "Politics",
      "tab.ukraine": "Ukraine",
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
      "news.sub": "Заголовки о рынках, мире, политике и Украине из открытых новостных источников и наши посты в X. Обновляется автоматически каждые 30 минут.",
      "news.live": "Онлайн", "news.loading": "Загружаем новости…",
      "news.hint": "Нажмите на заголовок, чтобы открыть оригинал в новой вкладке. Заголовки — на языке источника.",
      "news.empty": "В этом разделе пока нет новостей — загляните позже.",
      "news.error": "Не удалось загрузить ленту. Обновите страницу.",
      "news.updated": "Обновлено",
      "news.xsrc": "Пост в X",
      "news.posts": "Свежие посты",
      "news.tabs": "Разделы новостей",
      "tab.all": "Все",
      "tab.market": "Рынки",
      "tab.world": "Мир",
      "tab.politics": "Политика",
      "tab.ukraine": "Украина",
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
      "news.sub": "Заголовки про ринки, світ, політику та Україну з відкритих новинних джерел і наші пости в X. Оновлюється автоматично кожні 30 хвилин.",
      "news.live": "Онлайн", "news.loading": "Завантажуємо новини…",
      "news.hint": "Натисніть на заголовок, щоб відкрити оригінал у новій вкладці. Заголовки — мовою джерела.",
      "news.empty": "У цьому розділі поки немає новин — зазирніть пізніше.",
      "news.error": "Не вдалося завантажити стрічку. Оновіть сторінку.",
      "news.updated": "Оновлено",
      "news.xsrc": "Пост в X",
      "news.posts": "Свіжі пости",
      "news.tabs": "Розділи новин",
      "tab.all": "Усі",
      "tab.market": "Ринки",
      "tab.world": "Світ",
      "tab.politics": "Політика",
      "tab.ukraine": "Україна",
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
      "news.sub": "Les titres marchés, monde, politique et Ukraine issus de sources d'information ouvertes, plus nos posts sur X. Mise à jour automatique toutes les 30 minutes.",
      "news.live": "Direct", "news.loading": "Chargement des actus…",
      "news.hint": "Touchez un titre pour ouvrir l'original dans un nouvel onglet. Les titres restent dans leur langue d'origine.",
      "news.empty": "Pas encore d'actus dans cette rubrique — revenez bientôt.",
      "news.error": "Impossible de charger le fil. Actualisez la page.",
      "news.updated": "Mis à jour",
      "news.xsrc": "Post sur X",
      "news.posts": "Derniers posts",
      "news.tabs": "Rubriques",
      "tab.all": "Tout",
      "tab.market": "Marchés",
      "tab.world": "Monde",
      "tab.politics": "Politique",
      "tab.ukraine": "Ukraine",
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
      "news.sub": "Schlagzeilen zu Märkten, Welt, Politik und Ukraine aus offenen Nachrichtenquellen sowie unsere Posts auf X. Automatische Aktualisierung alle 30 Minuten.",
      "news.live": "Live", "news.loading": "News werden geladen…",
      "news.hint": "Tippe auf eine Schlagzeile, um das Original in einem neuen Tab zu öffnen. Schlagzeilen erscheinen in der Originalsprache.",
      "news.empty": "In dieser Rubrik gibt es noch keine News — schau bald wieder vorbei.",
      "news.error": "Der News-Feed konnte nicht geladen werden. Bitte lade die Seite neu.",
      "news.updated": "Aktualisiert",
      "news.xsrc": "Post auf X",
      "news.posts": "Neueste Posts",
      "news.tabs": "Rubriken",
      "tab.all": "Alle",
      "tab.market": "Märkte",
      "tab.world": "Welt",
      "tab.politics": "Politik",
      "tab.ukraine": "Ukraine",
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
      "news.sub": "来自公开新闻源的市场、国际、政治和乌克兰新闻标题，以及我们在 X 上的帖子。每 30 分钟自动更新。",
      "news.live": "实时", "news.loading": "正在加载新闻…",
      "news.hint": "点击标题即可在新标签页中打开原文。标题保持原文语言。",
      "news.empty": "该栏目暂无新闻，请稍后再来。",
      "news.error": "无法加载新闻，请刷新页面。",
      "news.updated": "更新于",
      "news.xsrc": "X 上的帖子",
      "news.posts": "最新帖子",
      "news.tabs": "新闻栏目",
      "tab.all": "全部",
      "tab.market": "市场",
      "tab.world": "国际",
      "tab.politics": "政治",
      "tab.ukraine": "乌克兰",
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

  // ---------- Products render (whole card links to Patreon / GitHub) ----------
  var pl = $("productList");
  PRODUCTS.forEach(function (p) {
    var card = el("article", "prod");
    var imgBox = el("a", "img");
    imgBox.href = p.url; imgBox.target = "_blank"; imgBox.rel = "noopener noreferrer"; imgBox.tabIndex = -1;
    imgBox.setAttribute("aria-hidden", "true");
    var im = new Image(); im.src = p.img; im.loading = "lazy"; im.decoding = "async"; im.width = 960; im.height = 540;
    im.alt = p.title || ""; if (p.t) im.setAttribute("data-i18n-alt", p.t);
    imgBox.appendChild(im);
    if (p.free) { var tag = el("span", "tag"); tag.setAttribute("data-i18n", "prod.free"); imgBox.appendChild(tag); }
    var body = el("div", "body");
    var h = el("h3");
    var ha = el("a", "plink", p.title || ""); if (p.t) ha.setAttribute("data-i18n", p.t);
    ha.href = p.url; ha.target = "_blank"; ha.rel = "noopener noreferrer";
    h.appendChild(ha);
    var d = el("p"); d.setAttribute("data-i18n", p.d);
    body.appendChild(h); body.appendChild(d);
    var row = el("div", "row");
    var pr = el("span", p.free ? "price free" : "price", p.free ? "" : p.price);
    if (p.free) pr.setAttribute("data-i18n", "prod.free");
    row.appendChild(pr);
    var a = el("a", "btn " + (p.free ? "btn-ghost" : "btn-gold"));
    a.setAttribute("data-i18n", p.cta || "prod.buy");
    a.href = p.url; a.target = "_blank"; a.rel = "noopener noreferrer";
    row.appendChild(a);
    body.appendChild(row);
    card.appendChild(imgBox); card.appendChild(body);
    pl.appendChild(card);
  });

  // ---------- i18n ----------
  var onLang = [];
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
    var bar = $("langBar");
    bar.setAttribute("aria-label", tr("lang"));
    Array.prototype.forEach.call(bar.querySelectorAll("button"), function (b) {
      b.setAttribute("aria-pressed", b.getAttribute("data-lang") === code ? "true" : "false");
    });
    try { localStorage.setItem("mp_lang", code); } catch (e) {}
    onLang.forEach(function (f) { f(); });
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

  // ---------- Language switcher: one-click buttons in the header (order = LANGS) ----------
  var langBar = $("langBar");
  LANGS.forEach(function (l) {
    var b = el("button", "lb", l.short); b.type = "button";
    b.setAttribute("data-lang", l.code); b.setAttribute("lang", l.html); b.title = l.name;
    b.setAttribute("aria-label", l.name);
    b.addEventListener("click", function () { apply(l.code); });
    langBar.appendChild(b);
  });

  // ---------- News feed (same-origin data/news.json, no third-party scripts) ----------
  var SECS = ["all", "market", "world", "politics", "ukraine", "x"];
  var MAX_PER_TAB = 30;
  var newsData = null, curTab = "all", loadState = "loading";
  var listEl = $("newsList"), tabsEl = $("newsTabs"), updEl = $("newsUpdated");
  try { var st = sessionStorage.getItem("mp_tab"); if (st && SECS.indexOf(st) >= 0) curTab = st; } catch (e) {}

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
  function shortUrl(u) { return u.replace(/^https?:\/\/(www\.)?/i, "").replace(/^(.{0,60}).*$/, function (m, a) { return m.length > 60 ? a + "…" : a; }); }

  function itemsFor(tab) {
    if (!newsData) return [];
    var x = (newsData.x || []).map(function (p) { return { kind: "x", title: p.text, url: p.url, ts: p.ts, source: "@" + (newsData.x_handle || "MarketPulseGold") }; });
    var rss = (newsData.items || []).map(function (i) { return { kind: "rss", title: i.title, url: i.url, ts: i.ts, source: i.source, sec: i.sec || [] }; });
    var out;
    if (tab === "x") out = x;
    else if (tab === "all") out = x.concat(rss);
    else out = rss.filter(function (i) { return i.sec.indexOf(tab) >= 0; });
    out = out.filter(function (i) { return safeUrl(i.url) && i.title; });
    out.sort(function (a, b) { return (b.ts || 0) - (a.ts || 0); });
    return out.slice(0, tab === "all" ? 40 : MAX_PER_TAB);
  }

  function card(it) {
    var a = el("a", "ni" + (it.kind === "x" ? " ni-x" : ""));
    a.href = safeUrl(it.url); a.target = "_blank"; a.rel = "noopener noreferrer";
    var meta = el("span", "ni-meta");
    meta.appendChild(el("b", "ni-src", it.kind === "x" ? it.source + " · X" : it.source));
    if (it.ts) {
      meta.appendChild(document.createTextNode(" · "));
      var t = el("time", null, rel(it.ts)); t.dateTime = new Date(it.ts * 1000).toISOString(); t.title = absDate(it.ts);
      meta.appendChild(t);
    }
    a.appendChild(meta);
    a.appendChild(el("span", "ni-t", it.title));
    if (it.kind === "x") a.appendChild(el("span", "ni-link", shortUrl(it.url)));
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
    if (s === "x") b.textContent = "X @MarketPulseGold"; else b.setAttribute("data-i18n", "tab." + s);
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

  apply(detect());

  function load() {
    var bucket = Math.floor(Date.now() / 300000); // refresh at most every 5 min (cache-busting)
    fetch("data/news.json?v=" + bucket, { cache: "no-cache" })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (d) { newsData = d; loadState = "ok"; render(); })
      .catch(function () { if (!newsData) { loadState = "error"; render(); } });
  }
  load();
  setInterval(load, 10 * 60 * 1000);
  setInterval(function () { if (loadState === "ok") render(); }, 60 * 1000);
})();
