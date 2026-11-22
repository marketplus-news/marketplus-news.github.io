T = dict(slug="airbnb-rental-profit-calculator", icon="str", product="str", kicker="Short-term rental",
 title="Airbnb Profit Calculator: STR Income, Occupancy & Break-Even | Market Plus",
 h1="Airbnb & Short-Term Rental Profit Calculator",
 desc="Free short-term rental calculator: nightly rate, occupancy, cleaning, platform fees and fixed costs in, monthly and yearly profit, break-even occupancy and break-even nightly rate out.",
 card="Monthly profit, break-even occupancy and the lowest nightly rate that still pays.",
 dek="Model one Airbnb, VRBO or Booking.com listing: revenue, fees, cleaning and fixed costs, your monthly and yearly profit, and the occupancy you need just to break even.",
 related_guides=["how-to-price-airbnb"], related_tools=["compound-interest-calculator", "debt-payoff-calculator"])
F = lambda i, l, v, s="": f'<div class="fld"><label for="{i}">{l}</label><input id="{i}" inputmode="decimal" value="{v}" autocomplete="off">{"<small>"+s+"</small>" if s else ""}</div>'
T["calc"] = f'''<div class="calc" id="calc">
<div>
 <h2>Revenue</h2>
 <div class="fgrid2">
  {F("rate","Average nightly rate ($)","140")}
  <div class="fld"><label for="occ">Occupancy: <b id="occV">65%</b></label><input id="occ" type="range" min="5" max="100" step="1" value="65"></div>
  {F("los","Average stay (nights)","3")}
  {F("cfee","Cleaning fee charged per stay ($)","60")}
 </div>
 <h2 style="margin-top:18px">Costs</h2>
 <div class="fgrid2">
  {F("pfee","Platform / payment fees (% of booking)","15","Depends on the platform and fee model you use.")}
  {F("ccost","Cleaning + laundry cost per stay ($)","55")}
  {F("sup","Supplies per stay ($)","8","Toiletries, coffee, consumables.")}
  {F("rent","Rent or mortgage per month ($)","1500")}
  {F("util","Utilities + internet per month ($)","220")}
  {F("other","Insurance, software, repairs per month ($)","150")}
 </div>
 <p class="privacy">Example values; replace them with your own. Saved only in this browser.</p>
</div>
<div>
 <h2>Monthly result</h2>
 <div class="kpis">
  <div class="kpi hi" id="netBox"><b id="oNet">—</b><span>Net profit per month</span></div>
  <div class="kpi"><b id="oYear">—</b><span>Net profit per year</span></div>
  <div class="kpi"><b id="oGross">—</b><span>Gross bookings per month</span></div>
  <div class="kpi"><b id="oMargin">—</b><span>Profit margin</span></div>
  <div class="kpi"><b id="oBeOcc">—</b><span>Break-even occupancy</span></div>
  <div class="kpi"><b id="oBeRate">—</b><span>Break-even nightly rate at this occupancy</span></div>
 </div>
 <div class="bars" id="bars"></div>
 <h2 style="margin-top:20px">Profit at other occupancy levels</h2>
 <div class="tscroll"><table class="ttable" id="sens"><thead><tr><th>Occupancy</th><th>Nights / mo</th><th>Gross</th><th>Net / mo</th></tr></thead><tbody></tbody></table></div>
 <p class="rnote" id="oNights"></p>
</div>
</div>'''
T["js"] = r'''(function(){var M=MPCalc,root=M.$("calc"),save=M.persist("str",root),D=30.4;
function model(o){var r=M.num("rate"),l=Math.max(1,M.num("los",1)),cf=M.num("cfee"),f=M.num("pfee")/100,cc=M.num("ccost"),su=M.num("sup"),fix=M.num("rent")+M.num("util")+M.num("other");
var n=D*o,s=n/l,rent=n*r,clean=s*cf,gross=rent+clean,fees=gross*f,vari=s*(cc+su),net=gross-fees-vari-fix,per=r*(1-f)+(cf*(1-f)-cc-su)/l;
return{n:n,s:s,gross:gross,fees:fees,vari:vari,fix:fix,net:net,per:per,f:f,l:l,cf:cf,cc:cc,su:su}}
function run(){var o=M.num("occ")/100;M.set("occV",Math.round(o*100)+"%");var m=model(o);
M.set("oNet",M.money(m.net));M.set("oYear",M.money(m.net*12));M.set("oGross",M.money(m.gross));M.set("oMargin",m.gross?M.pct(m.net/m.gross,0):"—");
M.$("netBox").className="kpi hi "+(m.net<0?"neg":"");
var be=m.per>0?m.fix/m.per/D:Infinity;M.set("oBeOcc",be>1?"over 100%":M.pct(be,0));
var br=m.n>0?(m.fix+m.s*(m.cc+m.su)-m.s*m.cf*(1-m.f))/(m.n*(1-m.f)):Infinity;M.set("oBeRate",isFinite(br)&&br>0?M.money(br):"—");
M.bars(M.$("bars"),[["Gross",m.gross,M.money(m.gross)],["Platform fees",m.fees,M.money(m.fees),"teal"],["Cleaning+supplies",m.vari,M.money(m.vari),"teal"],["Fixed costs",m.fix,M.money(m.fix),"teal"],["Net profit",Math.max(0,m.net),M.money(m.net)]]);
var rows="";for(var p=40;p<=90;p+=10){var x=model(p/100);rows+="<tr"+(Math.abs(p/100-o)<.05?' class="best"':"")+"><td>"+p+"%</td><td>"+M.n(x.n,1)+"</td><td>"+M.money(x.gross)+"</td><td>"+M.money(x.net)+"</td></tr>"}
M.$("sens").tBodies[0].innerHTML=rows;M.set("oNights","About "+M.n(m.n,1)+" booked nights and "+M.n(m.s,1)+" turnovers a month (a month is taken as 30.4 days).");save();}
M.live(root,run);})();'''
T["body"] = '''
<h2>What this calculator includes</h2>
<p>A short-term rental makes money on two lines: the nightly rate and the cleaning fee you charge each guest. It loses money on three: platform and payment fees, per-stay costs (cleaning, laundry, supplies) and fixed monthly costs that you pay whether the calendar is full or empty, such as rent or mortgage, utilities, internet, insurance and software.</p>
<p>The calculator turns occupancy into booked nights (occupancy × 30.4 days) and booked nights into stays (nights ÷ average length of stay). Every stay triggers one cleaning, so shorter stays mean more turnovers and more cleaning cost even at the same occupancy. That is why the average stay length matters as much as the nightly rate.</p>
<h2>Break-even occupancy and break-even rate</h2>
<p><strong>Break-even occupancy</strong> is the share of nights you need to sell just to cover fixed costs. It is calculated from the contribution of one booked night: the nightly rate after fees, plus the cleaning fee after fees minus cleaning and supply costs, spread across the nights of an average stay. Fixed costs divided by that contribution give the nights you need each month.</p>
<p><strong>Break-even nightly rate</strong> answers the opposite question: at the occupancy you entered, what is the lowest average rate that still covers everything? It is a useful floor when you set seasonal or last-minute discounts.</p>
<h2>How to use the results</h2>
<ul>
<li>Look at the <strong>occupancy table</strong>: a listing that only works at 85% occupancy is fragile, because one slow season wipes out the profit.</li>
<li>Test a <strong>longer minimum stay</strong>: fewer turnovers often add more profit than a higher nightly rate.</li>
<li>Check the <strong>fee setting</strong> against your platform's current fee structure; it differs between platforms and fee models.</li>
<li>Remember what is <strong>not</strong> included: income tax, local occupancy taxes, furniture and setup costs, and your own time.</li>
</ul>
<p>For a step-by-step approach to setting the rate itself, read <a href="/guides/how-to-price-airbnb.html">how to price an Airbnb</a>.</p>
<p class="note-box">This is a planning estimate, not tax, legal or investment advice. Check local short-term rental rules and taxes before you list.</p>
'''
T["faq"] = [
 ("What is a good occupancy rate for an Airbnb?", "It depends heavily on the market, season and listing. Rather than aiming for a number from someone else's city, use this calculator to find your break-even occupancy and make sure your realistic occupancy sits comfortably above it."),
 ("Should the cleaning fee cover the full cleaning cost?", "Many hosts set it close to the real cost, but a high cleaning fee makes short stays look expensive in search results. The calculator lets you test both: change the fee and the average stay and watch the profit and the break-even rate."),
 ("Does the calculator include taxes?", "No. Income tax and local occupancy or tourist taxes vary by country and city, and occupancy taxes are often collected from guests. Add a monthly estimate to the 'other' cost field if you want a cautious figure."),
 ("Why does a shorter stay reduce profit?", "Every stay needs a cleaning and supplies. With the same number of booked nights, shorter stays mean more turnovers, so per-stay costs rise faster than the cleaning fees you collect."),
 ("Is my data saved?", "Only in your own browser, so your numbers are still there next time. Nothing is uploaded."),
]
