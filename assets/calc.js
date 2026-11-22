/* Market Plus calculators: tiny shared helpers (no libraries, nothing leaves the browser). */
(function (w) {
  "use strict";
  var MP = w.MPCalc = {};
  MP.$ = function (id) { return document.getElementById(id); };
  MP.num = function (id, d) { var e = MP.$(id); if (!e) return d || 0; var v = parseFloat(String(e.value).replace(/[, ]/g, "")); return isFinite(v) ? v : (d || 0); };
  MP.money = function (v, dec) {
    if (!isFinite(v)) return "—";
    var s = v < 0 ? "-" : ""; v = Math.abs(v);
    return s + "$" + v.toLocaleString("en-US", { minimumFractionDigits: dec || 0, maximumFractionDigits: dec || 0 });
  };
  MP.n = function (v, dec) { return isFinite(v) ? v.toLocaleString("en-US", { minimumFractionDigits: dec || 0, maximumFractionDigits: dec || 0 }) : "—"; };
  MP.pct = function (v, dec) { return isFinite(v) ? (v * 100).toFixed(dec == null ? 1 : dec) + "%" : "—"; };
  // "5:30" -> 330 s, "1:05:00" -> 3900 s, "5.5" -> 330 s (minutes)
  MP.secs = function (str) {
    str = String(str || "").trim(); if (!str) return 0;
    if (str.indexOf(":") < 0) { var m = parseFloat(str.replace(",", ".")); return isFinite(m) ? Math.round(m * 60) : 0; }
    var p = str.split(":").map(function (x) { return parseFloat(x) || 0; }), s = 0;
    for (var i = 0; i < p.length; i++) s = s * 60 + p[i];
    return Math.round(s);
  };
  MP.clock = function (s, forceH) {
    if (!isFinite(s)) return "—";
    s = Math.max(0, Math.round(s));
    var h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60), x = s % 60;
    var mm = (h || forceH ? (m < 10 ? "0" : "") : "") + m;
    return (h || forceH ? h + ":" : "") + mm + ":" + (x < 10 ? "0" : "") + x;
  };
  MP.set = function (id, v) { var e = MP.$(id); if (e) e.textContent = v; };
  MP.esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  // Saves inputs only in this browser (localStorage), so a return visit picks up where you left off.
  MP.persist = function (key, root) {
    var k = "mp_tool_" + key, els = root.querySelectorAll("input[id],select[id]");
    try { var saved = JSON.parse(localStorage.getItem(k) || "null"); if (saved) Array.prototype.forEach.call(els, function (e) { if (saved[e.id] != null) e.value = saved[e.id]; }); } catch (e) {}
    return function () {
      var o = {}; Array.prototype.forEach.call(root.querySelectorAll("input[id],select[id]"), function (e) { o[e.id] = e.value; });
      try { localStorage.setItem(k, JSON.stringify(o)); } catch (e) {}
    };
  };
  MP.saveJSON = function (key, v) { try { localStorage.setItem("mp_tool_" + key, JSON.stringify(v)); } catch (e) {} };
  MP.loadJSON = function (key) { try { return JSON.parse(localStorage.getItem("mp_tool_" + key) || "null"); } catch (e) { return null; } };
  MP.live = function (root, fn) { root.addEventListener("input", fn); root.addEventListener("change", fn); fn(); };
  MP.bars = function (el, rows, max) { // rows: [label, value, text, cls]
    max = max || Math.max.apply(null, rows.map(function (r) { return r[1]; }).concat([1e-9]));
    el.innerHTML = rows.map(function (r) {
      var w = Math.max(0, Math.min(100, r[1] / max * 100));
      return '<div class="brow"><span>' + MP.esc(r[0]) + '</span><span class="bt"><i class="' + (r[3] || "") + '" style="width:' + w.toFixed(1) + '%"></i></span><span>' + MP.esc(r[2]) + "</span></div>";
    }).join("");
  };
  MP.reset = function (key) { try { localStorage.removeItem("mp_tool_" + key); } catch (e) {} location.reload(); };
})(window);
