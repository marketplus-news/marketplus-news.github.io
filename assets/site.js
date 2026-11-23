/* Market Plus: scroll reveal, hero gold particles, reading progress, header state. Vanilla, no deps. */
(function () {
  "use strict";
  var d = document, w = window, h = d.documentElement;
  var still = w.matchMedia && w.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var hdr = d.querySelector("header.top");
  var bar = d.querySelector(".read-progress span"), art = d.querySelector("article.guide");
  if (!bar && art && d.querySelector(".related")) { // guide pages: add a progress bar
    var rp = d.createElement("div"); rp.className = "read-progress"; rp.setAttribute("aria-hidden", "true");
    rp.appendChild(bar = d.createElement("span")); d.body.insertBefore(rp, d.body.firstChild);
  }
  var tick = false;
  function onScroll() {
    if (tick) return; tick = true;
    w.requestAnimationFrame(function () {
      tick = false;
      if (hdr) hdr.classList.toggle("scrolled", w.pageYOffset > 8);
      if (bar && art) {
        var r = art.getBoundingClientRect(), t = r.height - w.innerHeight;
        bar.style.transform = "scaleX(" + Math.min(1, Math.max(0, t > 0 ? -r.top / t : 1)).toFixed(4) + ")";
      }
    });
  }
  w.addEventListener("scroll", onScroll, { passive: true }); onScroll();

  // ---- scroll reveal: only elements below the fold are hidden (no flash, no hidden content if JS fails) ----
  if (!still && "IntersectionObserver" in w) {
    var SEL = ".phead .wrap>*,section>.wrap>h2,section>.wrap>.sub,.shead,.acard,.scard,.mcard,.etsy,.tile,.feed,.products,.quotes .wrap,.guide>h2,.cta-box,.related>h2,footer .fgrid>*";
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -6% 0px", threshold: 0 });
    var vh = w.innerHeight;
    Array.prototype.forEach.call(d.querySelectorAll(SEL), function (el) {
      if (el.getBoundingClientRect().top < vh * 0.95) return;
      var p = el.parentNode, i = p ? Array.prototype.indexOf.call(p.children, el) : 0;
      el.style.setProperty("--d", (Math.min(i, 5) % 3) * 0.08 + "s"); // stagger cards in a row
      el.classList.add("rv"); io.observe(el);
    });
  }

  // ---- hero: light gold/teal particles on a canvas (pauses off-screen and in background tabs) ----
  var cv = d.querySelector(".hero-fx");
  if (cv && !still && cv.getContext) {
    var cx = cv.getContext("2d"), P = [], W = 0, H = 0, dpr = 1, run = false, vis = true, raf = 0, mx = 0, my = 0;
    var size = function () {
      var r = cv.getBoundingClientRect(); dpr = Math.min(2, w.devicePixelRatio || 1);
      W = r.width; H = r.height; cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
      cx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var n = Math.round(Math.min(56, Math.max(18, W / 26)));
      while (P.length < n) P.push(mk(true)); P.length = n;
    };
    var mk = function (any) {
      return { x: Math.random() * W, y: any ? Math.random() * H : H + 10, r: 0.6 + Math.random() * 1.9,
        vy: 0.08 + Math.random() * 0.32, vx: (Math.random() - 0.5) * 0.12, a: 0.25 + Math.random() * 0.55,
        ph: Math.random() * 6.28, teal: Math.random() < 0.18 };
    };
    var draw = function (t) {
      cx.clearRect(0, 0, W, H);
      for (var i = 0; i < P.length; i++) {
        var p = P[i]; p.y -= p.vy; p.x += p.vx + Math.sin(t / 2400 + p.ph) * 0.06;
        if (p.y < -10 || p.x < -10 || p.x > W + 10) { P[i] = p = mk(false); }
        var k = p.r / 2.5, x = p.x + mx * k * 14, y = p.y + my * k * 10;
        var al = p.a * (0.55 + 0.45 * Math.sin(t / 900 + p.ph)) * Math.min(1, p.y / (H * 0.35));
        var c = p.teal ? "63,184,175," : "242,215,122,";
        cx.fillStyle = "rgba(" + c + (al * 0.16).toFixed(3) + ")"; cx.beginPath(); cx.arc(x, y, p.r * 4, 0, 6.283); cx.fill();
        cx.fillStyle = "rgba(" + c + al.toFixed(3) + ")"; cx.beginPath(); cx.arc(x, y, p.r, 0, 6.283); cx.fill();
      }
      raf = run ? w.requestAnimationFrame(draw) : 0;
    };
    var go = function () { var on = vis && !d.hidden; if (on && !run) { run = true; raf = w.requestAnimationFrame(draw); } else if (!on) { run = false; w.cancelAnimationFrame(raf); } };
    size();
    var rz; w.addEventListener("resize", function () { clearTimeout(rz); rz = setTimeout(size, 150); });
    d.addEventListener("visibilitychange", go);
    if ("IntersectionObserver" in w) new IntersectionObserver(function (e) { vis = e[0].isIntersecting; go(); }).observe(cv);
    cv.parentNode.addEventListener("pointermove", function (e) { // subtle parallax
      var r = cv.getBoundingClientRect(); mx = (e.clientX - r.left) / r.width - 0.5; my = (e.clientY - r.top) / r.height - 0.5;
    }, { passive: true });
    go();
  }

  // ---- owner-only stats badge (?owner=<key> sets a localStorage flag; ?owner=off clears it) ----
  var OWNER_KEY = "PJxFR2FoNufS";
  var OWNER_FLAG = "mp_owner";
  var GC_HOST = "https://marketplus.goatcounter.com";
  var isOwner = false;
  try {
    var oq = new URLSearchParams(w.location.search).get("owner");
    if (oq === "off") {
      localStorage.removeItem(OWNER_FLAG);
      localStorage.removeItem("skipgc");
    } else if (oq === OWNER_KEY) {
      localStorage.setItem(OWNER_FLAG, "1");
      localStorage.setItem("skipgc", "t");
    }
    if (localStorage.getItem(OWNER_FLAG)) {
      localStorage.setItem("skipgc", "t");
      w.goatcounter = w.goatcounter || {};
      w.goatcounter.no_onload = true;
      isOwner = true;
    }
  } catch (err) {}

  // Anonymous, cookie-free visit stats (GoatCounter). Skip if the page already has the tag.
  // Owner mode is applied first so count.js honors no_onload / skipgc.
  if (!d.querySelector("script[data-goatcounter]")) {
    var gc = d.createElement("script");
    gc.setAttribute("data-goatcounter", "https://marketplus.goatcounter.com/count");
    gc.async = true;
    gc.src = "https://gc.zgo.at/count.js";
    (d.head || d.body || d.documentElement).appendChild(gc);
  }

  if (isOwner) {
    try {
      var ou = new URL(w.location.href);
      if (ou.searchParams.has("owner")) {
        ou.searchParams.delete("owner");
        w.history.replaceState(null, "", ou.pathname + (ou.search ? ou.search : "") + ou.hash);
      }
    } catch (err) {}
    showOwnerBadge();
  }

  function ymdKiev(ts) {
    return new Intl.DateTimeFormat("en-CA", { timeZone: "Europe/Kiev", year: "numeric", month: "2-digit", day: "2-digit" }).format(ts);
  }
  function addDaysYmd(ymd, days) {
    var p = ymd.split("-");
    var dt = new Date(Date.UTC(+p[0], +p[1] - 1, +p[2] + days));
    return dt.toISOString().slice(0, 10);
  }
  function gcCount(data) {
    if (!data || data.count == null || data.count === "") return null;
    return String(data.count);
  }
  function gcPath() {
    var p = (w.location && w.location.pathname) ? w.location.pathname : "/";
    if (p.length > 11 && p.slice(-11) === "/index.html") p = p.slice(0, -10);
    if (!p) p = "/";
    return p;
  }
  function fetchCounter(path, query) {
    var url = GC_HOST + "/counter/" + encodeURIComponent(path) + ".json" + (query || "");
    return fetch(url, { credentials: "omit" }).then(function (res) {
      if (!res.ok) return null;
      return res.json().then(gcCount).catch(function () { return null; });
    }).catch(function () { return null; });
  }
  function showOwnerBadge() {
    if (d.getElementById("mp-owner-stats")) return;
    var box = d.createElement("aside");
    box.id = "mp-owner-stats";
    box.className = "mp-owner";
    box.setAttribute("aria-label", "Your visit stats");
    box.innerHTML = '<div class="mp-owner-rows">' +
      '<div><span>Page</span> <b data-k="page">…</b></div>' +
      '<div><span>Today</span> <b data-k="today">…</b></div>' +
      '<div><span>All</span> <b data-k="all">…</b></div>' +
      '</div><a href="' + GC_HOST + '/" target="_blank" rel="noopener">Stats</a>';
    (d.body || d.documentElement).appendChild(box);
    var set = function (k, v) {
      var el = box.querySelector('[data-k="' + k + '"]');
      if (el) el.textContent = v == null ? "—" : v;
    };
    var today = ymdKiev(new Date());
    var tmrw = addDaysYmd(today, 1);
    var path = gcPath();
    Promise.all([
      fetchCounter(path),
      fetchCounter("TOTAL", "?start=" + today + "&end=" + tmrw),
      fetchCounter("TOTAL")
    ]).then(function (vals) {
      var page = vals[0], day = vals[1], all = vals[2];
      if (page == null && day == null && all == null) {
        box.classList.add("mp-owner-na");
        box.querySelector(".mp-owner-rows").innerHTML = "<div><span>Counts unavailable — open the dashboard</span></div>";
        return;
      }
      set("page", page);
      set("today", day);
      set("all", all);
    });
  }
})();
