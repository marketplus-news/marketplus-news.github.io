T = dict(slug="hyrox-finish-time-calculator", icon="hyrox", product="hyrox", kicker="Fitness · Hyrox",
 title="Hyrox Finish Time Calculator: Predict Your Splits | Market Plus",
 h1="Hyrox Finish Time Calculator",
 desc="Free Hyrox calculator: enter your run pace, eight station times and Roxzone to predict your finish time, see every split, or work out the run pace you need for a goal time.",
 card="Predict your finish from run pace and station times, or find the pace for a goal time.",
 dek="Enter your 1 km run pace, how long each of the eight stations takes you and your transition time. Get a predicted finish, a split sheet and the pace you need for a goal time.",
 related_guides=["hyrox-pacing-strategy"], related_tools=["compound-interest-calculator", "holiday-budget-planner"])
STATIONS = [("SkiErg 1000 m", "4:45"), ("Sled Push 50 m", "3:30"), ("Sled Pull 50 m", "4:30"), ("Burpee Broad Jumps 80 m", "5:00"),
            ("Rowing 1000 m", "4:50"), ("Farmers Carry 200 m", "2:00"), ("Sandbag Lunges 100 m", "4:30"), ("Wall Balls 100 reps", "6:00")]
st = "".join(f'<div class="fld"><label for="s{i}">{n}</label><input id="s{i}" inputmode="numeric" value="{v}" autocomplete="off"></div>' for i, (n, v) in enumerate(STATIONS))
T["calc"] = f'''<div class="calc" id="calc">
<div>
 <h2>Your inputs</h2>
 <div class="fgrid2">
  <div class="fld"><label for="pace">Average 1 km run pace (min:sec)</label><input id="pace" inputmode="numeric" value="5:30" autocomplete="off"></div>
  <div class="fld"><label for="fade">Run fade over the race: <b id="fadeV">5%</b></label><input id="fade" type="range" min="0" max="20" step="1" value="5"><small>How much slower run 8 is than run 1.</small></div>
  {st}
  <div class="fld"><label for="rox">Roxzone, total (min:sec)</label><input id="rox" inputmode="numeric" value="7:00" autocomplete="off"><small>All transitions in and out of the stations.</small></div>
  <div class="fld"><label for="goal">Goal finish time (h:mm:ss)</label><input id="goal" inputmode="numeric" value="1:25:00" autocomplete="off"></div>
 </div>
 <p class="privacy">The values above are an example, not benchmarks. Type your own times; they are saved only in this browser.</p>
</div>
<div>
 <h2>Prediction</h2>
 <div class="kpis">
  <div class="kpi hi"><b id="oTotal">—</b><span>Predicted finish</span></div>
  <div class="kpi"><b id="oRuns">—</b><span>8 × 1 km running</span></div>
  <div class="kpi"><b id="oSta">—</b><span>Stations</span></div>
  <div class="kpi"><b id="oRox">—</b><span>Roxzone</span></div>
 </div>
 <div class="kpis" style="margin-top:10px"><div class="kpi" id="goalBox"><b id="oNeed">—</b><span id="oNeedL">Avg run pace needed for your goal</span></div><div class="kpi"><b id="oShare">—</b><span>Share of race spent running</span></div></div>
 <div class="tscroll"><table class="ttable" id="splits"><thead><tr><th>Segment</th><th>Split</th><th>Elapsed</th></tr></thead><tbody></tbody></table></div>
</div>
</div>'''
T["js"] = r'''(function(){var M=MPCalc,root=M.$("calc"),save=M.persist("hyrox",root);var names=%s;
function run(){var p=M.secs(M.$("pace").value),f=M.num("fade")/100,rows=[],t=0,runs=0,sta=0;M.set("fadeV",Math.round(f*100)+"%%");
var rox=M.secs(M.$("rox").value),roxEach=rox/16;
for(var i=0;i<8;i++){var r=p*(1-f/2+f*i/7);runs+=r;t+=r+roxEach;rows.push(["Run "+(i+1),r,t]);var s=M.secs(M.$("s"+i).value);sta+=s;t+=s+roxEach;rows.push([names[i],s,t]);}
var total=runs+sta+rox;M.set("oTotal",M.clock(total,true));M.set("oRuns",M.clock(runs));M.set("oSta",M.clock(sta));M.set("oRox",M.clock(rox));M.set("oShare",total?Math.round(runs/total*100)+"%%":"—");
var g=M.secs(M.$("goal").value),need=(g-sta-rox)/8,box=M.$("goalBox");
if(g&&need>120){M.set("oNeed",M.clock(need)+" /km");M.set("oNeedL",need<p?"Avg run pace needed: "+M.clock(p-need)+" /km faster than now":"Avg run pace needed: you have "+M.clock(need-p)+" /km to spare");box.className="kpi "+(need<p?"neg":"pos");}
else{M.set("oNeed","—");M.set("oNeedL","Goal is too tight for these station times");box.className="kpi neg";}
M.$("splits").tBodies[0].innerHTML=rows.map(function(r){return"<tr><td>"+M.esc(r[0])+"</td><td>"+M.clock(r[1])+"</td><td>"+M.clock(r[2],true)+"</td></tr>"}).join("")+'<tr class="best"><td>Finish (incl. Roxzone)</td><td></td><td>'+M.clock(total,true)+"</td></tr>";save();}
M.live(root,run);})();''' % str([n for n, _ in STATIONS]).replace("'", '"')
T["body"] = '''
<h2>How the Hyrox race is built</h2>
<p>Every Hyrox race has the same format worldwide: eight 1 km runs, each followed by one functional workout station, always in the same order. The stations are the SkiErg (1000 m), Sled Push (50 m), Sled Pull (50 m), Burpee Broad Jumps (80 m), Rowing (1000 m), Farmers Carry (200 m), Sandbag Lunges (100 m) and Wall Balls (100 reps). Weights and target heights depend on the division you enter, so check the current rulebook for yours.</p>
<p>Between running and each station you pass through the <strong>Roxzone</strong>, the transition area where you enter and leave the station. Roxzone time counts towards your result, which is why this calculator asks for it separately: athletes often underestimate it, and on a crowded race day it adds up.</p>
<h2>How this calculator predicts your time</h2>
<p>Your finish time is simply the sum of eight runs, eight stations and the total Roxzone time. The calculator takes your average 1 km pace and applies a <em>run fade</em>: in most races later runs are slower than early ones, because the stations (especially the sleds and lunges) load the legs. A fade of 5% means your last run is about 5% slower than your first, while the average stays close to the pace you entered.</p>
<p>The <strong>goal</strong> field works backwards: it subtracts your station and Roxzone times from the goal and divides the rest by eight. The result is the average running pace you need. If it is faster than your current pace, the gap shows you exactly how much you need to find, either on the runs or on the stations.</p>
<h2>How to get honest inputs</h2>
<ul>
<li><strong>Run pace:</strong> use a pace you can hold for 1 km <em>repeats with hard work between them</em>, not your fresh 10 km race pace.</li>
<li><strong>Stations:</strong> time each one in training at race weight, ideally after a run, because fresh station times are optimistic.</li>
<li><strong>Roxzone:</strong> if you have raced before, take it from your official result; otherwise start with a conservative estimate and adjust.</li>
</ul>
<p>Use the split table as a race-day pacing sheet: the elapsed column tells you where you should be after each segment. If you are well ahead after the SkiErg and sleds, you probably started too fast. For a full approach to pacing, read our <a href="/guides/hyrox-pacing-strategy.html">Hyrox pacing strategy guide</a>.</p>
<p class="note-box">This tool gives an estimate from your own numbers. It is not a coaching plan or medical advice; build training load gradually.</p>
'''
T["faq"] = [
 ("How accurate is a Hyrox finish time prediction?", "It is only as good as your inputs. If your station times come from fresh efforts or your run pace from a stand-alone run, the prediction will be optimistic. Times measured in race-like conditions, with a run before each station, give a much closer estimate."),
 ("What is the Roxzone in Hyrox?", "The Roxzone is the transition area between the running track and the workout stations. The time you spend walking or jogging through it, entering and leaving each station, is included in your official finish time."),
 ("Why is there a run fade setting?", "Most athletes slow down over the eight runs because the stations tire the legs. The fade spreads that slowdown across the race so the split table looks like a real race rather than eight identical runs."),
 ("How do I use the goal time field?", "Type the finish time you want. The calculator subtracts your station and Roxzone times and shows the average 1 km pace you would need. A red result means your current pace is not enough for that goal with these station times."),
 ("Are my numbers stored anywhere?", "Only in your own browser (localStorage), so the page remembers them next time. Nothing is sent to Market Plus or anyone else."),
]
