"""Emit the disclosure-gap reference page with data embedded inline."""
import json

SRC = "/Users/armaan/code/katalysis/research/coverage_tools/by_metric.json"
OUT = "/Users/armaan/code/katalysis/research/coverage_tools/disclosure_gaps.html"

data = json.load(open(SRC))

# Compact payload: bank name, year-suffix list, window length.
payload = {}
for sheet, banks in data.items():
    payload[sheet] = [[b["bank"],
                       [int(y[2:]) for y in b["missing"]],
                       [int(y[2:]) for y in b["ever"]]] for b in banks]

js = json.dumps(payload, separators=(",", ":"))

HTML = """<title>Disclosure Gap Register</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700&family=Source+Sans+3:wght@400;600&display=swap">
<style>
:root{
  --paper:#f6f7f5; --card:#ffffff; --ink:#141d24; --muted:#63717b;
  --rule:#dfe3df; --rule-soft:#ecefec;
  --accent:#0e5f5c; --accent-soft:#e2eeec;
  --s1:#cfe0de; --s2:#a3c7c4; --s3:#6ea9a5; --s4:#3a8683; --s5:#0e5f5c;
  --warn:#8a5a14;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --paper:#10171c; --card:#162026; --ink:#e6eceb; --muted:#8fa0a8;
    --rule:#26333a; --rule-soft:#1c272d;
    --accent:#5fbdb7; --accent-soft:#14312f;
    --s1:#1f3a39; --s2:#2c5c58; --s3:#3f807c; --s4:#57a9a3; --s5:#7fd0c9;
    --warn:#d2a24e;
  }
}
:root[data-theme="dark"]{
  --paper:#10171c; --card:#162026; --ink:#e6eceb; --muted:#8fa0a8;
  --rule:#26333a; --rule-soft:#1c272d;
  --accent:#5fbdb7; --accent-soft:#14312f;
  --s1:#1f3a39; --s2:#2c5c58; --s3:#3f807c; --s4:#57a9a3; --s5:#7fd0c9;
  --warn:#d2a24e;
}
*{box-sizing:border-box}
body{
  margin:0; background:var(--paper); color:var(--ink);
  font-family:"Source Sans 3",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  font-size:15px; line-height:1.5; font-variant-numeric:tabular-nums;
}
.wrap{max-width:1080px; margin:0 auto; padding:40px 24px 80px}
header{border-bottom:2px solid var(--ink); padding-bottom:18px; margin-bottom:8px}
h1{
  font-family:Archivo,sans-serif; font-weight:700; font-size:30px;
  letter-spacing:-.015em; margin:0 0 6px; text-wrap:balance;
}
.sub{color:var(--muted); max-width:62ch; margin:0}
.meta{
  display:flex; flex-wrap:wrap; gap:22px; margin-top:16px;
  font-size:13px; color:var(--muted);
}
.meta b{font-family:Archivo,sans-serif; color:var(--ink); font-size:19px; font-weight:600; display:block}

.controls{
  display:flex; flex-wrap:wrap; gap:10px; align-items:center;
  margin:26px 0 18px; padding:12px 0; border-bottom:1px solid var(--rule);
  position:sticky; top:0; background:var(--paper); z-index:5;
}
.seg{display:flex; border:1px solid var(--rule); border-radius:2px; overflow:hidden}
.seg button{
  font:inherit; font-size:13px; padding:6px 13px; border:0; cursor:pointer;
  background:transparent; color:var(--muted); border-right:1px solid var(--rule);
}
.seg button:last-child{border-right:0}
.seg button[aria-pressed="true"]{background:var(--accent); color:#fff}
input[type=search]{
  font:inherit; font-size:13px; padding:6px 11px; flex:1; min-width:180px;
  border:1px solid var(--rule); border-radius:2px;
  background:var(--card); color:var(--ink);
}
input[type=search]:focus-visible,.seg button:focus-visible,summary:focus-visible{
  outline:2px solid var(--accent); outline-offset:1px;
}

.chart{margin:8px 0 34px}
.row{
  display:grid; grid-template-columns:150px 1fr 96px; gap:12px;
  align-items:center; padding:5px 0; cursor:pointer;
  border-bottom:1px solid var(--rule-soft);
}
.row:hover .lbl{color:var(--accent)}
.lbl{font-family:Archivo,sans-serif; font-weight:600; font-size:13px}
.bar{height:16px; background:var(--rule-soft); position:relative}
.bar i{display:block; height:100%; background:var(--accent)}
.bar em{
  position:absolute; inset:0; display:block; font-style:normal;
  background:var(--warn); opacity:.85;
}
.num{font-size:13px; color:var(--muted); text-align:right}
.num b{color:var(--ink); font-weight:600}

details{
  background:var(--card); border:1px solid var(--rule);
  border-radius:2px; margin-bottom:8px;
}
summary{
  cursor:pointer; padding:11px 14px; list-style:none;
  display:flex; align-items:baseline; gap:12px;
}
summary::-webkit-details-marker{display:none}
summary::before{
  content:"+"; font-family:Archivo,sans-serif; color:var(--accent);
  font-weight:700; width:12px;
}
details[open] summary::before{content:"\\2212"}
details[open] summary{border-bottom:1px solid var(--rule)}
.mname{font-family:Archivo,sans-serif; font-weight:600; flex:1}
.mcount{font-size:13px; color:var(--muted)}
.banks{padding:4px 14px 14px}
.bank{
  display:grid; grid-template-columns:1fr auto auto; gap:14px;
  align-items:center; padding:6px 0; border-bottom:1px solid var(--rule-soft);
  font-size:14px;
}
.bank:last-child{border-bottom:0}
.bn{display:flex; flex-direction:column; gap:1px}
.has{font-size:12px; color:var(--muted)}
.has.none{color:var(--warn)}
.yrs{display:flex; gap:3px}
.yr{
  font-size:11px; padding:1px 5px; border-radius:2px;
  background:var(--accent-soft); color:var(--accent); font-weight:600;
}
.pill{
  font-size:11px; font-weight:600; padding:2px 7px; border-radius:2px;
  white-space:nowrap;
}
.p5{background:var(--s5); color:#fff}
.p1{background:var(--s1); color:var(--ink)}
.empty{color:var(--muted); font-size:13px; padding:10px 0}
footer{
  margin-top:44px; padding-top:16px; border-top:1px solid var(--rule);
  font-size:13px; color:var(--muted); max-width:70ch;
}
footer p{margin:0 0 8px}
@media (max-width:640px){
  .row{grid-template-columns:110px 1fr 64px; gap:8px}
  .bank{grid-template-columns:1fr; gap:4px}
}
</style>

<div class="wrap">
<header>
  <h1>Disclosure Gap Register</h1>
  <p class="sub">Which Pillar 3 metrics are missing, for which UK PRA-authorised banks, across each bank's last five reported financial years.</p>
  <div class="meta">
    <span><b>145</b>banks covered</span>
    <span><b>944</b>open cells</span>
    <span><b>86.6%</b>coverage, MREL excluded</span>
    <span><b>15 Sep 2026</b>generated</span>
  </div>
</header>

<div class="controls">
  <div class="seg" role="group" aria-label="Filter scope">
    <button data-f="all" aria-pressed="true">All gaps</button>
    <button data-f="proven" aria-pressed="false">Disclosed before</button>
    <button data-f="persistent" aria-pressed="false">Never disclosed</button>
    <button data-f="latest" aria-pressed="false">Latest year only</button>
  </div>
  <input type="search" id="q" placeholder="Filter by bank name...">
</div>

<div class="chart" id="chart"></div>
<div id="list"></div>

<footer>
  <p><b>Disclosed before</b> is the cohort that matters most: the bank has published this metric in at least one year, so the missing years are far more likely to be a sourcing miss than a real absence. Each row shows what the bank does disclose, so a gap sitting between two disclosed years stands out. <b>Never disclosed</b> means absent in all five reported years — usually a bank publishing no Pillar 3 at all, or disclosing only at group level. <b>Latest year only</b> is most often publication lag, which resolves itself with time.</p>
  <p>MREL is excluded throughout: only UK resolution entities carry an MREL requirement, so its absence is structural for roughly 130 of the 145 banks. Pre-2022 NSFR blanks are likewise structural — the UK had no NSFR requirement or disclosure template before 1 January 2022 (PRA PS17/21).</p>
  <p>Years a bank could not have reported — before it held a banking licence, or before the metric existed as a requirement — now leave the denominator rather than counting as gaps, and are marked in the workbooks themselves so they read as settled rather than as work nobody has done. 79 such cells sit inside the five-year windows. An earlier version of this page counted them, which overstated the remaining work and sent researchers after figures that can never exist.</p>
</footer>
</div>

<script>
const DATA = __DATA__;
const ORDER = ["NSFR","RWA Breakdown","Leverage Ratio","LCR","Total RWAs","Tier 1 Ratio","Total Capital Ratio","CET1 Ratio","Tier 1 Capital","CET1 Capital","Total Capital"];
let filter = "all", query = "";

function rows(sheet){
  let r = DATA[sheet] || [];
  if (filter === "proven") r = r.filter(b => (b[2] || []).length > 0);
  if (filter === "persistent") r = r.filter(b => b[1].length >= 5);
  if (filter === "latest") r = r.filter(b => b[1].length === 1);
  if (query) r = r.filter(b => b[0].toLowerCase().includes(query));
  return r;
}

function drawChart(){
  const counts = ORDER.map(s => {
    const all = rows(s);
    return {s, n: all.length, persistent: all.filter(b => b[1].length >= 5).length,
            cells: all.reduce((a,b) => a + b[1].length, 0)};
  });
  const max = Math.max(1, ...counts.map(c => c.n));
  document.getElementById("chart").innerHTML = counts.map(c => `
    <div class="row" data-go="${c.s.replace(/"/g,'&quot;')}">
      <span class="lbl">${c.s}</span>
      <span class="bar" title="${c.n} banks, ${c.persistent} never disclosing">
        <i style="width:${c.n/max*100}%"></i>
        <em style="width:${c.persistent/max*100}%"></em>
      </span>
      <span class="num"><b>${c.n}</b> banks</span>
    </div>`).join("");
  document.querySelectorAll("[data-go]").forEach(el => el.onclick = () => {
    const d = document.getElementById("d-" + el.dataset.go.replace(/\\s/g,"_"));
    if (d){ d.open = true; d.scrollIntoView({behavior:"smooth", block:"start"}); }
  });
}

function drawList(){
  document.getElementById("list").innerHTML = ORDER.map(s => {
    const r = rows(s);
    const cells = r.reduce((a,b) => a + b[1].length, 0);
    const body = r.length ? r.map(b => {
      const persistent = b[1].length >= 5, ever = b[2] || [];
      const has = ever.length
        ? `<span class="has">discloses ${ever.slice(0,4).map(y => "FY"+y).join(", ")}${ever.length>4 ? " +"+(ever.length-4) : ""}</span>`
        : `<span class="has none">no year on record</span>`;
      return `<div class="bank">
        <span class="bn">${b[0]}${has}</span>
        <span class="yrs">${b[1].map(y => `<span class="yr">FY${y}</span>`).join("")}</span>
        <span class="pill ${persistent ? "p5" : "p1"}">${persistent ? "never" : b[1].length + "y"}</span>
      </div>`;
    }).join("") : `<div class="empty">No banks match this filter.</div>`;
    return `<details id="d-${s.replace(/\\s/g,"_")}">
      <summary><span class="mname">${s}</span><span class="mcount">${r.length} banks &middot; ${cells} cells</span></summary>
      <div class="banks">${body}</div>
    </details>`;
  }).join("");
}

function render(){ drawChart(); drawList(); }

document.querySelectorAll(".seg button").forEach(btn => btn.onclick = () => {
  filter = btn.dataset.f;
  document.querySelectorAll(".seg button").forEach(b =>
    b.setAttribute("aria-pressed", String(b === btn)));
  render();
});
document.getElementById("q").oninput = e => { query = e.target.value.toLowerCase().trim(); render(); };
render();
</script>
"""

open(OUT, "w").write(HTML.replace("__DATA__", js))
print("wrote", OUT, len(HTML.replace("__DATA__", js)), "bytes")
