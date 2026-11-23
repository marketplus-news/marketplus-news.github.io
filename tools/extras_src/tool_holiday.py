T = dict(slug="holiday-budget-planner", icon="gift", product="xmas", kicker="Christmas · Holidays",
 title="Christmas Budget Calculator 2026: Gifts & Savings",
 h1="Christmas & Holiday Budget Planner",
 desc="Free Christmas budget calculator: list gifts per person, food, decor and travel, see what is left and how much to save each week until Christmas.",
 card="Gift list, holiday costs and how much to set aside each week until the day.",
 dek="Set one total, list who you are buying for, add the costs people forget, and see what is left and how much to put aside each week until the holiday.",
 related_guides=["debt-snowball-vs-avalanche"], related_tools=["compound-interest-calculator", "debt-payoff-calculator"])
F = lambda i, l, v, s="": f'<div class="fld"><label for="{i}">{l}</label><input id="{i}" inputmode="decimal" value="{v}" autocomplete="off">{"<small>"+s+"</small>" if s else ""}</div>'
T["calc"] = f'''<div class="calc" id="calc">
<div>
 <h2>Budget</h2>
 <div class="fgrid2">
  {F("total","Total holiday budget ($)","900")}
  {F("saved","Already set aside ($)","150")}
  <div class="fld full"><label for="day">Holiday date</label><input id="day" type="date"></div>
 </div>
 <h2 style="margin-top:18px">Gifts</h2>
 <div class="rhead g"><span>Person</span><span>Amount ($)</span><span></span></div>
 <div class="rows" id="rows"></div>
 <button type="button" class="addb" id="add">+ Add a person</button>
 <h2 style="margin-top:18px">Everything else</h2>
 <div class="fgrid2">
  {F("food","Food & drinks ($)","150")}
  {F("deco","Decorations & tree ($)","40")}
  {F("wrap","Wrapping, cards & postage ($)","30")}
  {F("travel","Travel ($)","80")}
  {F("events","Parties & going out ($)","50")}
  {F("misc","Charity & other ($)","20")}
 </div>
 <p class="privacy">Example list; replace it with yours. Saved only in this browser. <button type="button" class="addb" id="reset" style="margin:0 0 0 6px;min-height:30px">Reset</button></p>
</div>
<div>
 <h2>Your plan</h2>
 <div class="kpis">
  <div class="kpi hi" id="leftBox"><b id="oLeft">—</b><span id="oLeftL">Left to allocate</span></div>
  <div class="kpi"><b id="oPlan">—</b><span>Planned spending</span></div>
  <div class="kpi"><b id="oWeek">—</b><span id="oWeekL">Save per week</span></div>
  <div class="kpi"><b id="oDays">—</b><span>Days to go</span></div>
 </div>
 <div class="bars" id="bars"></div>
 <p class="rnote" id="oNote"></p>
</div>
</div>'''
T["js"] = r'''(function(){var M=MPCalc,root=M.$("calc"),box=M.$("rows");
var DEF=[["Partner",120],["Mum",60],["Dad",60],["Kids",150],["Friends & colleagues",60]];
var st=M.loadJSON("holiday");var save=M.persist("holiday-f",root);
function xmas(){var d=new Date(),y=d.getFullYear(),c=new Date(y,11,25);if(d>c)c=new Date(y+1,11,25);return c.getFullYear()+"-12-25"}
if(!M.$("day").value)M.$("day").value=xmas();
function rowHTML(r){return'<div class="drow g"><input aria-label="Person" value="'+M.esc(r[0])+'"><input aria-label="Amount" inputmode="decimal" value="'+r[1]+'"><button type="button" class="rmb" aria-label="Remove">×</button></div>'}
function draw(rows){box.innerHTML=rows.map(rowHTML).join("")}draw(st||DEF);
function read(){return Array.prototype.map.call(box.querySelectorAll(".drow"),function(d){var i=d.querySelectorAll("input");return[i[0].value||"Gift",parseFloat(i[1].value)||0]})}
function run(){var g=read();M.saveJSON("holiday",g);save();
var gifts=g.reduce(function(a,x){return a+x[1]},0),cats=[["Gifts",gifts],["Food & drinks",M.num("food")],["Decorations",M.num("deco")],["Wrapping & cards",M.num("wrap")],["Travel",M.num("travel")],["Parties",M.num("events")],["Charity & other",M.num("misc")]];
var plan=cats.reduce(function(a,x){return a+x[1]},0),tot=M.num("total"),left=tot-plan,saved=M.num("saved");
M.set("oPlan",M.money(plan));M.set("oLeft",M.money(Math.abs(left)));M.set("oLeftL",left>=0?"Left to allocate":"Over budget");M.$("leftBox").className="kpi hi "+(left<0?"neg":"");
var d=new Date(M.$("day").value+"T00:00:00"),now=new Date();now.setHours(0,0,0,0);var days=Math.round((d-now)/864e5);
M.set("oDays",isFinite(days)?(days>=0?days:"passed"):"—");
var need=Math.max(0,plan-saved),weeks=Math.max(1,Math.ceil(days/7));
M.set("oWeek",days>0?M.money(need/weeks,2):"—");M.set("oWeekL","Save per week for "+weeks+" week"+(weeks>1?"s":"")+" ("+M.money(need)+" still to find)");
M.bars(M.$("bars"),cats.map(function(c){return[c[0],c[1],M.money(c[1])+" · "+(plan?Math.round(c[1]/plan*100):0)+"%"]}));
var top=g.slice().sort(function(a,b){return b[1]-a[1]})[0];
M.set("oNote",g.length?g.length+" people on the gift list, average "+M.money(gifts/g.length)+" each"+(top?"; largest: "+top[0]+" ("+M.money(top[1])+").":"."):"Add the people you are buying for.");}
root.addEventListener("click",function(e){if(e.target.closest(".rmb")){e.target.closest(".drow").remove();run()}});
M.$("add").addEventListener("click",function(){box.insertAdjacentHTML("beforeend",rowHTML(["Name",30]));run()});
M.$("reset").addEventListener("click",function(){M.saveJSON("holiday",null);M.reset("holiday-f")});
M.live(root,run);})();'''
T["body"] = '''
<h2>Start with one number</h2>
<p>The most effective holiday budget starts with a single total that you can pay from savings and this month's income, without a card balance that lingers into the new year. Everything else is a way of dividing that number. Set the total first, then fill in the gifts and the other categories, and adjust until <em>Left to allocate</em> is zero or positive.</p>
<h2>The costs people forget</h2>
<p>Gifts are the obvious part, but the extras are often what pushes a holiday over budget: food and drinks for several days, the tree and decorations, wrapping paper, cards and postage, travel to family, parties and office collections, and charity donations. Listing them separately makes them visible early, while there is still time to cut back.</p>
<h2>Setting gift amounts</h2>
<ul>
<li>Decide the <strong>gift total</strong> before choosing individual gifts, then divide it per person.</li>
<li>Agree on a <strong>limit or a Secret Santa</strong> with large families or groups of friends.</li>
<li>Track what you actually spend against each amount. A planner that shows budget against actual makes overspending obvious.</li>
</ul>
<h2>Saving week by week</h2>
<p>The planner counts the days until the date you choose (Christmas Day by default) and divides what you still need by the remaining weeks. Setting that amount aside each week, for example by moving it to a separate savings pot on payday, spreads the cost and avoids a January surprise. If the weekly amount looks too high, lower the total now rather than borrowing later. Our <a href="/guides/how-to-plan-christmas-budget-2026.html">Christmas budget guide</a> walks through a full example.</p>
<p class="note-box">The planner runs entirely in your browser and stores your list only on this device.</p>
'''
T["faq"] = [
 ("How much should I spend on Christmas?", "There is no universal right amount. A practical rule is to spend only what you can cover from savings and current income without carrying a credit card balance into the new year."),
 ("How do I avoid overspending on gifts?", "Set a total gift budget first, give each person a limit, keep a list and record what you actually spend. Group agreements such as a Secret Santa also help."),
 ("Can I use this for other holidays?", "Yes. Change the holiday date and rename the gift list; the categories work for birthdays, Eid, Hanukkah, Diwali or a family trip."),
 ("How is the weekly saving calculated?", "Planned spending minus what you have already set aside, divided by the number of weeks left until the holiday date (rounded up)."),
 ("Is my gift list private?", "Yes. It is saved only in your browser's local storage on this device. Nothing is sent to Market Plus."),
]
