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
})();
