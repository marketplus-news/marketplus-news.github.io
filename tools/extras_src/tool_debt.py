T = dict(slug="debt-payoff-calculator", icon="debt", product="debt", kicker="Debt payoff",
 title="Debt Snowball vs Avalanche Calculator: Debt-Free Date | Market Plus",
 h1="Debt Snowball vs Avalanche Calculator",
 desc="Free debt payoff calculator: list your debts, add an extra monthly payment and compare the snowball and avalanche methods side by side: debt-free date, total interest and payoff order.",
 card="Compare snowball and avalanche: debt-free date, interest paid and payoff order.",
 dek="List your debts, add what you can pay on top of the minimums, and compare both methods side by side: months to debt-free, total interest and the order your debts disappear.",
 related_guides=["debt-snowball-vs-avalanche"], related_tools=["compound-interest-calculator", "holiday-budget-planner"])
T["calc"] = '''<div class="calc" id="calc">
<div>
 <h2>Your debts</h2>
 <div class="rhead"><span>Name</span><span>Balance ($)</span><span>APR %</span><span>Min / mo ($)</span><span></span></div>
 <div class="rows" id="rows"></div>
 <button type="button" class="addb" id="add">+ Add a debt</button>
 <div class="fgrid2" style="margin-top:16px">
  <div class="fld"><label for="extra">Extra payment per month ($)</label><input id="extra" inputmode="decimal" value="200" autocomplete="off"><small>On top of all minimum payments.</small></div>
 </div>
 <p class="privacy">Example debts; replace them with yours. Saved only in this browser. <button type="button" class="addb" id="reset" style="margin:0 0 0 6px;min-height:30px">Reset</button></p>
</div>
<div>
 <h2>Results</h2>
 <div class="tscroll"><table class="ttable" id="cmp"><thead><tr><th></th><th>Snowball</th><th>Avalanche</th><th>Minimums only</th></tr></thead><tbody></tbody></table></div>
 <div class="kpis" style="margin-top:14px"><div class="kpi hi"><b id="oSave">—</b><span id="oSaveL">Interest saved by avalanche vs snowball</span></div><div class="kpi"><b id="oFirst">—</b><span id="oFirstL">First debt cleared (snowball)</span></div></div>
 <h2 style="margin-top:18px">Payoff order</h2>
 <div class="tscroll"><table class="ttable" id="ord"><thead><tr><th>#</th><th>Snowball</th><th>Avalanche</th></tr></thead><tbody></tbody></table></div>
 <p class="rnote" id="oWarn"></p>
</div>
</div>'''
T["js"] = r'''(function(){var M=MPCalc,root=M.$("calc"),box=M.$("rows");
var DEF=[["Credit card A",3200,24.9,95],["Credit card B",1200,19.9,40],["Car loan",8500,7.5,260],["Personal loan",4000,12,130]];
var st=M.loadJSON("debt")||{rows:DEF,extra:200};M.$("extra").value=st.extra;
function rowHTML(r){return'<div class="drow"><input aria-label="Name" value="'+M.esc(r[0])+'"><input aria-label="Balance" inputmode="decimal" value="'+r[1]+'"><input aria-label="APR %" inputmode="decimal" value="'+r[2]+'"><input aria-label="Minimum payment" inputmode="decimal" value="'+r[3]+'"><button type="button" class="rmb" aria-label="Remove">×</button></div>'}
function draw(rows){box.innerHTML=rows.map(rowHTML).join("")}draw(st.rows);
function read(){return Array.prototype.map.call(box.querySelectorAll(".drow"),function(d){var i=d.querySelectorAll("input");return[i[0].value||"Debt",parseFloat(i[1].value)||0,parseFloat(i[2].value)||0,parseFloat(i[3].value)||0]})}
function sim(debts,mode,extra){var d=debts.filter(function(x){return x[1]>0}).map(function(x){return{n:x[0],b:x[1],r:x[2]/1200,m:x[3]}});
var budget=d.reduce(function(a,x){return a+x.m},0)+(mode==="min"?0:extra),month=0,interest=0,order=[];
while(d.some(function(x){return x.b>0.005})&&month<1200){month++;
 d.forEach(function(x){if(x.b>0){var i=x.b*x.r;x.b+=i;interest+=i}});
 var left=mode==="min"?0:budget;
 if(mode==="min"){d.forEach(function(x){if(x.b>0){var p=Math.min(x.m,x.b);x.b-=p}})}
 else{d.forEach(function(x){if(x.b>0){var p=Math.min(x.m,x.b);x.b-=p;left-=p}});
  var act=d.filter(function(x){return x.b>0.005});act.sort(mode==="snow"?function(a,b){return a.b-b.b||b.r-a.r}:function(a,b){return b.r-a.r||a.b-b.b});
  for(var k=0;k<act.length&&left>0.005;k++){var p=Math.min(left,act[k].b);act[k].b-=p;left-=p}}
 d.forEach(function(x){if(x.b<=0.005&&!x.done){x.done=1;x.b=0;order.push([x.n,month])}});}
return{months:month,interest:interest,order:order,stuck:month>=1200}}
function when(m){var d=new Date();d.setMonth(d.getMonth()+m);return d.toLocaleDateString("en-US",{month:"short",year:"numeric"})}
function yrs(m){return Math.floor(m/12)+" y "+(m%12)+" m"}
function run(){var rows=read(),extra=M.num("extra");M.saveJSON("debt",{rows:rows,extra:extra});
var s=sim(rows,"snow",extra),a=sim(rows,"aval",extra),z=sim(rows,"min",extra);
var c=function(r){return r.stuck?"never*":yrs(r.months)};
var total=rows.reduce(function(t,x){return t+x[1]},0);
M.$("cmp").tBodies[0].innerHTML="<tr><td>Time to debt-free</td><td>"+c(s)+"</td><td>"+c(a)+"</td><td>"+c(z)+"</td></tr><tr><td>Debt-free date</td><td>"+(s.stuck?"—":when(s.months))+"</td><td>"+(a.stuck?"—":when(a.months))+"</td><td>"+(z.stuck?"—":when(z.months))+"</td></tr><tr><td>Total interest</td><td>"+M.money(s.interest)+"</td><td>"+M.money(a.interest)+"</td><td>"+(z.stuck?"—":M.money(z.interest))+"</td></tr><tr><td>Total debt today</td><td colspan=3>"+M.money(total)+"</td></tr>";
var sv=s.interest-a.interest;M.set("oSave",M.money(Math.abs(sv)));M.set("oSaveL",sv>=0?"Interest saved by avalanche vs snowball":"Snowball costs less here (equal APRs or rounding)");
M.set("oFirst",s.order.length?"Month "+s.order[0][1]:"—");M.set("oFirstL",s.order.length?"First debt cleared with snowball: "+s.order[0][0]:"First debt cleared (snowball)");
var n=Math.max(s.order.length,a.order.length),h="";for(var i=0;i<n;i++){h+="<tr><td>"+(i+1)+"</td><td>"+(s.order[i]?M.esc(s.order[i][0])+" (m "+s.order[i][1]+")":"")+"</td><td>"+(a.order[i]?M.esc(a.order[i][0])+" (m "+a.order[i][1]+")":"")+"</td></tr>"}
M.$("ord").tBodies[0].innerHTML=h;
M.set("oWarn",(z.stuck||s.stuck)?"* At least one balance never reaches zero: its minimum payment does not cover the monthly interest. Raise the payment.":"Interest is compounded monthly at APR ÷ 12. Real lenders may calculate it daily, so treat results as estimates.");}
root.addEventListener("click",function(e){if(e.target.closest(".rmb")){e.target.closest(".drow").remove();run()}});
M.$("add").addEventListener("click",function(){box.insertAdjacentHTML("beforeend",rowHTML(["New debt",1000,15,30]));run()});
M.$("reset").addEventListener("click",function(){M.saveJSON("debt",null);M.$("extra").value=200;draw(DEF);run()});
M.live(root,run);})();'''
T["body"] = '''
<h2>Snowball and avalanche in one sentence each</h2>
<p>Both methods start the same way: you keep paying the minimum on every debt and put every spare dollar on top of one target debt. When that debt is gone, its minimum payment rolls into the next target, so your payment to the target grows over time. The only difference is the order.</p>
<ul>
<li><strong>Debt snowball:</strong> target the <em>smallest balance</em> first. You clear whole debts sooner, which many people find motivating.</li>
<li><strong>Debt avalanche:</strong> target the <em>highest interest rate</em> first. Mathematically this usually costs the least interest and is never slower.</li>
</ul>
<h2>How the calculator works</h2>
<p>Each month it adds interest to every balance (APR ÷ 12), pays each minimum, and sends the rest of your total monthly budget (the sum of your minimums plus the extra amount) to the target debt. When a debt reaches zero, the money that paid it automatically flows to the next target. It repeats this until every balance is zero and records the month each debt disappears.</p>
<p>The <strong>minimums only</strong> column shows what happens if you never pay more than the required minimum on each debt and do not roll freed-up payments forward. It is usually the slowest and most expensive path, and if a minimum does not even cover the monthly interest, that balance never goes down.</p>
<h2>Which method should you choose?</h2>
<p>If the interest difference shown above is small, pick the method you are more likely to stick with; consistency matters more than the last few dollars. If the difference is large (typically when one high-rate card also has a large balance), the avalanche is worth considering. Some people use a hybrid: clear one tiny balance first for a quick win, then switch to avalanche order. We compare both in detail in <a href="/guides/debt-snowball-vs-avalanche.html">Debt snowball vs avalanche, explained</a>.</p>
<p class="note-box">The results are estimates for planning. Lenders may use daily interest, fees or promotional rates that change the numbers. This is not financial advice.</p>
'''
T["faq"] = [
 ("Is the debt avalanche always cheaper than the snowball?", "With the same total monthly payment, ordering by highest interest rate first minimises interest in almost every case. When rates are similar, the two methods give nearly identical results, and the snowball may even finish a debt or two earlier."),
 ("What should I enter as the extra payment?", "The amount you can reliably pay every month on top of all minimum payments. Even a small, steady extra amount shortens the payoff time, because it compounds through the rollover."),
 ("Why does a debt say 'never'?", "Its minimum payment is lower than the interest charged each month, so the balance grows or stays flat. Increase the payment or contact the lender about the rate."),
 ("Does it handle 0% promotional balances?", "Enter 0 as the APR. Keep in mind that when a promotion ends the rate changes, which this simple model does not track."),
 ("Where are my debts stored?", "Only in your browser's local storage on this device. Nothing is sent to us, and the Reset button clears it."),
]
