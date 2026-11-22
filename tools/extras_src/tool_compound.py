T = dict(slug="compound-interest-calculator", icon="grow", product="savings", kicker="Saving · Investing",
 title="Compound Interest & Savings Goal Calculator | Market Plus",
 h1="Compound Interest & Savings Goal Calculator",
 desc="Free compound interest calculator: see how a starting amount and monthly deposits grow over time, the share that comes from growth, the value after inflation, and the monthly saving needed to reach a goal.",
 card="See your savings grow year by year, or find the monthly amount to hit a goal.",
 dek="Watch a starting amount and regular monthly deposits grow, see how much is your money and how much is growth, and find the monthly saving needed for a target.",
 related_guides=["debt-snowball-vs-avalanche", "position-sizing-explained"], related_tools=["debt-payoff-calculator", "holiday-budget-planner"])
F = lambda i, l, v, s="": f'<div class="fld"><label for="{i}">{l}</label><input id="{i}" inputmode="decimal" value="{v}" autocomplete="off">{"<small>"+s+"</small>" if s else ""}</div>'
T["calc"] = f'''<div class="calc" id="calc">
<div>
 <h2>Your plan</h2>
 <div class="fgrid2">
  {F("p0","Starting amount ($)","1000")}
  {F("pm","Monthly deposit ($)","200")}
  {F("rate","Annual return (%)","5","An assumption, not a promise. Try several.")}
  {F("yrs","Years","15")}
  {F("inc","Raise deposits each year by (%)","0")}
  {F("inf","Inflation for 'today's money' (%)","2.5")}
 </div>
 <h2 style="margin-top:18px">Savings goal</h2>
 <div class="fgrid2">{F("goal","Target amount ($)","50000","Uses the starting amount, return and years above.")}</div>
 <p class="privacy">Saved only in this browser.</p>
</div>
<div>
 <h2>Result</h2>
 <div class="kpis">
  <div class="kpi hi"><b id="oFV">—</b><span id="oFVL">Balance at the end</span></div>
  <div class="kpi"><b id="oIn">—</b><span>Total you deposited</span></div>
  <div class="kpi pos"><b id="oGr">—</b><span>Growth (interest earned)</span></div>
  <div class="kpi"><b id="oReal">—</b><span>Ending balance in today's money</span></div>
  <div class="kpi hi" style="grid-column:1/-1"><b id="oNeed">—</b><span id="oNeedL">Monthly deposit needed for your goal</span></div>
 </div>
 <svg class="chart" id="chart" viewBox="0 0 520 220" role="img" aria-label="Balance by year"></svg>
 <div class="legend"><span><i style="background:#d4af37"></i>Balance</span><span><i style="background:#3fb8af"></i>Your deposits</span></div>
 <div class="tscroll"><table class="ttable" id="tab"><thead><tr><th>Year</th><th>Deposited</th><th>Growth</th><th>Balance</th></tr></thead><tbody></tbody></table></div>
</div>
</div>'''
T["js"] = r'''(function(){var M=MPCalc,root=M.$("calc"),save=M.persist("compound",root);
function grow(p0,pm,r,y,inc){var b=p0,dep=p0,rows=[[0,dep,b]],m=r/1200;for(var k=1;k<=y;k++){for(var i=0;i<12;i++){b=b*(1+m)+pm;dep+=pm}rows.push([k,dep,b]);pm*=1+inc/100}return rows}
function run(){var p0=M.num("p0"),pm=M.num("pm"),r=M.num("rate"),y=Math.max(1,Math.min(60,Math.round(M.num("yrs",1)))),inc=M.num("inc"),inf=M.num("inf"),g=M.num("goal");
var rows=grow(p0,pm,r,y,inc),L=rows[y],fv=L[2];M.set("oFV",M.money(fv));M.set("oFVL","Balance after "+y+" years");M.set("oIn",M.money(L[1]));M.set("oGr",M.money(fv-L[1]));M.set("oReal",M.money(fv/Math.pow(1+inf/100,y)));
var m=r/1200,n=y*12,need=m?(g-p0*Math.pow(1+m,n))*m/(Math.pow(1+m,n)-1):(g-p0)/n;
if(need<=0){M.set("oNeed","$0");M.set("oNeedL","Your starting amount alone reaches the goal")}else{M.set("oNeed",M.money(need,2)+" / month");M.set("oNeedL","Monthly deposit needed for "+M.money(g)+" in "+y+" years (flat deposits)")}
var W=520,H=220,P=34,max=Math.max(fv,1),sx=function(k){return P+(W-P-8)*k/y},sy=function(v){return H-22-(H-34)*v/max};
var bal=rows.map(function(r){return sx(r[0]).toFixed(1)+","+sy(r[2]).toFixed(1)}).join(" "),dep=rows.map(function(r){return sx(r[0]).toFixed(1)+","+sy(r[1]).toFixed(1)}).join(" ");
var grid="";for(var t=0;t<=4;t++){var v=max*t/4,yy=sy(v);grid+='<line x1="'+P+'" x2="'+W+'" y1="'+yy+'" y2="'+yy+'" stroke="#26262e"/><text x="2" y="'+(yy+4)+'">'+(v>=1e6?(v/1e6).toFixed(1)+"M":Math.round(v/1e3)+"k")+"</text>"}
var step=Math.max(1,Math.ceil(y/6));for(var k=0;k<=y;k+=step)grid+='<text x="'+(sx(k)-4)+'" y="'+(H-6)+'">'+k+"</text>";
M.$("chart").innerHTML=grid+'<polygon points="'+sx(0)+","+sy(0)+" "+bal+" "+sx(y)+","+sy(0)+'" fill="rgba(212,175,55,.16)"/><polyline points="'+bal+'" fill="none" stroke="#d4af37" stroke-width="2.5"/><polyline points="'+dep+'" fill="none" stroke="#3fb8af" stroke-width="2" stroke-dasharray="5 4"/>';
M.$("tab").tBodies[0].innerHTML=rows.slice(1).map(function(r){return"<tr><td>"+r[0]+"</td><td>"+M.money(r[1])+"</td><td>"+M.money(r[2]-r[1])+"</td><td>"+M.money(r[2])+"</td></tr>"}).join("");save();}
M.live(root,run);})();'''
T["body"] = '''
<h2>What compound interest is</h2>
<p>Compound interest means you earn a return not only on the money you put in, but also on the returns you have already earned. In the first years most of the balance is your own deposits; over longer periods the growth line pulls away from the deposits line in the chart above, because each year's growth is calculated on a larger base. Time and consistency usually matter more than the size of any single deposit.</p>
<h2>How this calculator works</h2>
<p>It assumes deposits at the end of each month and monthly compounding at the annual rate ÷ 12. Each year you can raise the deposit by a percentage, for example to match pay rises. The <strong>today's money</strong> figure divides the ending balance by the inflation you enter for every year, which shows what the balance would buy at today's prices. That number is often a useful reality check on large long-term totals.</p>
<p>The <strong>savings goal</strong> box works backwards with the standard future-value formula: given your starting amount, the return and the number of years, it finds the flat monthly deposit that reaches the target.</p>
<h2>Choosing a realistic return</h2>
<ul>
<li><strong>Savings accounts and deposits</strong> pay a stated rate that changes with central bank rates; use the rate your bank actually offers.</li>
<li><strong>Investments</strong> such as stock funds do not have a fixed return. Results vary from year to year and can be negative. Run the calculator with a cautious, a middle and an optimistic rate rather than relying on one number.</li>
<li><strong>Fees and taxes</strong> reduce your real return. Subtract them from the rate for a more honest picture.</li>
</ul>
<p>If you carry high-interest debt, paying it off is often the best guaranteed "return" available. Compare with our <a href="/tools/debt-payoff-calculator.html">debt payoff calculator</a>.</p>
<p class="note-box">For education and planning only. Past or assumed returns do not guarantee future results; this is not investment advice.</p>
'''
T["faq"] = [
 ("How often does interest compound in this calculator?", "Monthly, at the annual rate divided by 12, with deposits added at the end of each month. Accounts that compound daily give very slightly higher results."),
 ("What return should I use?", "For a savings account, its current interest rate. For investments there is no guaranteed rate, so compare a few scenarios and treat the results as a range, not a forecast."),
 ("What does 'today's money' mean?", "It is the ending balance adjusted for the inflation rate you entered, so you can see roughly what it would buy at today's prices."),
 ("How is the monthly amount for a goal calculated?", "With the standard future-value-of-an-annuity formula: the target minus the grown starting amount, divided by the growth factor of a series of monthly deposits."),
 ("Does the calculator store my numbers?", "Only in your own browser, so they are there next time. Nothing is sent anywhere."),
]
