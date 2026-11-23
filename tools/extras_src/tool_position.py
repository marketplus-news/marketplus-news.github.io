T = dict(slug="position-size-calculator", icon="risk", product="trading", kicker="Forex · Gold",
 title="Position Size Calculator for Forex & Gold (XAU/USD)",
 h1="Position Size & Pip Value Calculator",
 desc="Free position size calculator for forex and gold: balance, risk % and stop-loss in; lot size, units, pip value and money at risk out.",
 card="Lot size from your risk % and stop loss, with pip value for forex and gold.",
 dek="Decide how big a trade should be before you place it: enter your account size, the percentage you are willing to risk and your stop-loss distance.",
 related_guides=["position-sizing-explained"], related_tools=["compound-interest-calculator", "debt-payoff-calculator"])
F = lambda i, l, v, s="": f'<div class="fld"><label for="{i}" id="{i}L">{l}</label><input id="{i}" inputmode="decimal" value="{v}" autocomplete="off">{"<small id=" + chr(34) + i + "S" + chr(34) + ">"+s+"</small>" if s else ""}</div>'
T["calc"] = f'''<div class="calc" id="calc">
<div>
 <h2>Trade setup</h2>
 <div class="fgrid2">
  <div class="fld full"><label for="sym">Instrument (USD account)</label><select id="sym">
   <option value="xxxusd">EUR/USD, GBP/USD, AUD/USD, NZD/USD</option>
   <option value="usdjpy">USD/JPY</option>
   <option value="usdxxx">USD/CHF, USD/CAD</option>
   <option value="xau">XAU/USD (gold, 100 oz per lot)</option>
   <option value="custom">Other: I know the pip value per lot</option></select></div>
  {F("bal","Account balance ($)","5000")}
  {F("risk","Risk per trade (%)","1","Many traders keep this small; it is your choice.")}
  {F("sl","Stop-loss distance (pips)","25")}
  {F("tp","Take-profit distance (pips, optional)","50")}
  {F("px","Current price","150.00","Needed to convert the pip value to USD.")}
  {F("pv","Pip value per 1 standard lot ($)","10")}
 </div>
 <p class="privacy">Standard lot = 100,000 units of the base currency (forex) or 100 oz (gold). Check your broker's contract size.</p>
</div>
<div>
 <h2>Position size</h2>
 <div class="kpis">
  <div class="kpi hi"><b id="oLots">—</b><span>Standard lots (rounded down to 0.01)</span></div>
  <div class="kpi"><b id="oRisk">—</b><span>Money at risk (your limit)</span></div>
  <div class="kpi"><b id="oUnits">—</b><span id="oUnitsL">Units</span></div>
  <div class="kpi"><b id="oPip">—</b><span>Value of 1 pip at this size</span></div>
  <div class="kpi neg"><b id="oLoss">—</b><span>Loss if the stop is hit</span></div>
  <div class="kpi pos"><b id="oWin">—</b><span id="oWinL">Gain at take-profit</span></div>
 </div>
 <div class="tscroll"><table class="ttable" id="alt"><thead><tr><th>Risk %</th><th>Lots</th><th>Loss at stop</th></tr></thead><tbody></tbody></table></div>
 <p class="rnote" id="oNote"></p>
</div>
</div>'''
T["js"] = r'''(function(){var M=MPCalc,root=M.$("calc"),save=M.persist("position",root);
function show(id,on){var f=M.$(id).closest(".fld");f.style.display=on?"":"none"}
function pipLot(sym,px){if(sym==="xxxusd")return 10;if(sym==="usdjpy")return px>0?1000/px:NaN;if(sym==="usdxxx")return px>0?10/px:NaN;if(sym==="xau")return 10;return M.num("pv")}
function run(){var sym=M.$("sym").value,px=M.num("px");show("px",sym==="usdjpy"||sym==="usdxxx");show("pv",sym==="custom");
M.set("slL",sym==="xau"?"Stop-loss distance (pips of $0.10)":"Stop-loss distance (pips)");
M.set("pxS",sym==="usdjpy"?"USD/JPY price, e.g. 150.00. 1 pip = 0.01.":"Pair price, e.g. 0.8800. 1 pip = 0.0001.");
var bal=M.num("bal"),rp=M.num("risk"),sl=M.num("sl"),tp=M.num("tp"),pv=pipLot(sym,px),cash=bal*rp/100;
function lotsFor(c){return sl>0&&pv>0?Math.floor(c/(sl*pv)*100+1e-9)/100:NaN}
var lots=lotsFor(cash),units=lots*(sym==="xau"?100:100000);
M.set("oLots",isFinite(lots)?lots.toFixed(2):"—");M.set("oRisk",M.money(cash,2));
M.set("oUnits",isFinite(units)?M.n(units):"—");M.set("oUnitsL",sym==="xau"?"Ounces of gold":"Units of base currency");
M.set("oPip",isFinite(lots)?M.money(lots*pv,2):"—");M.set("oLoss",isFinite(lots)?M.money(lots*pv*sl,2):"—");
M.set("oWin",tp>0&&isFinite(lots)?M.money(lots*pv*tp,2):"—");M.set("oWinL",tp>0&&sl>0?"Gain at take-profit (reward:risk "+(tp/sl).toFixed(2)+")":"Gain at take-profit");
M.$("alt").tBodies[0].innerHTML=[0.25,0.5,1,2,3].map(function(r){var l=lotsFor(bal*r/100);return"<tr"+(r===rp?' class="best"':"")+"><td>"+r+"%</td><td>"+(isFinite(l)?l.toFixed(2):"—")+"</td><td>"+(isFinite(l)?M.money(l*pv*sl,2):"—")+"</td></tr>"}).join("");
M.set("oNote",lots===0?"Your risk budget is smaller than 0.01 lot at this stop. Use a smaller stop, a larger account or a broker that offers smaller sizes.":"Pip value per standard lot used: "+(isFinite(pv)?M.money(pv,2):"—")+". Rounding down keeps the real loss at or under your limit. Spreads, commissions and slippage are not included.");save();}
M.live(root,run);})();'''
T["body"] = '''
<h2>Why position size matters more than entry</h2>
<p>Position sizing decides how much you lose when a trade goes wrong. The idea is simple: decide in advance the maximum amount of your account you are willing to lose on one trade, decide where your stop-loss goes based on the chart, and then let those two numbers set the trade size. The stop is placed where the trade idea is proven wrong; the size is adjusted so that being wrong costs only what you planned.</p>
<p>The formula is: <strong>position size = money at risk ÷ (stop distance × value per pip per lot)</strong>. With a $5,000 account and 1% risk, the money at risk is $50. On EUR/USD a standard lot moves about $10 per pip, so a 25-pip stop costs $250 per lot, and $50 ÷ $250 = 0.20 lots.</p>
<h2>Pip value for different instruments</h2>
<ul>
<li><strong>Pairs quoted in USD</strong> (EUR/USD, GBP/USD, AUD/USD, NZD/USD): one pip is 0.0001, and for a 100,000-unit lot that is $10 per pip.</li>
<li><strong>USD/JPY:</strong> one pip is 0.01 yen, so a lot moves 1,000 yen per pip. Converted to dollars that is 1,000 ÷ the current USD/JPY price.</li>
<li><strong>USD/CHF, USD/CAD:</strong> one pip is 0.0001 of the quote currency, so the USD value is 10 ÷ the current price.</li>
<li><strong>XAU/USD:</strong> conventions differ between brokers. This calculator assumes 100 oz per lot and a pip of $0.10, so a lot moves $10 per pip ($100 per $1 move in gold). Check your platform's contract specification.</li>
</ul>
<p>Mini (0.10) and micro (0.01) lots scale the pip value by the same factor. The calculator rounds down to 0.01 lot so the real loss never exceeds your limit.</p>
<h2>Using the table</h2>
<p>The risk table shows the same trade at several risk levels. It makes the trade-off visible: doubling the risk percentage doubles both the size and the loss at the stop. A sequence of losses at a high risk percentage can take a large share of an account, which is why many traders choose a small fixed percentage. Read more in <a href="/guides/position-sizing-explained.html">How position sizing works</a>.</p>
<p class="note-box">Educational tool, not investment advice. Leveraged trading in forex and gold carries a high risk of loss. Spreads, commissions, swaps and slippage are not included.</p>
'''
T["faq"] = [
 ("How do I calculate lot size from risk?", "Divide the money you are willing to lose by the stop-loss distance in pips multiplied by the pip value of one lot. For example, $50 ÷ (25 pips × $10) = 0.20 lots."),
 ("What is the pip value of EUR/USD?", "For a standard lot of 100,000 euros, one pip (0.0001) is worth $10. A mini lot is $1 and a micro lot $0.10 per pip."),
 ("How is a pip defined for gold?", "It varies by broker. Many use $0.01 or $0.10 as a pip for XAU/USD. This calculator uses $0.10 and 100 oz per lot; if your broker differs, choose 'Other' and enter its pip value per lot."),
 ("Why does the calculator round down?", "Brokers usually accept sizes in steps of 0.01 lot. Rounding down keeps the loss at the stop at or below the amount you chose to risk."),
 ("Are spreads and commissions included?", "No. They add to the cost of every trade, so on tight stops your real loss can be a little larger than shown."),
]
