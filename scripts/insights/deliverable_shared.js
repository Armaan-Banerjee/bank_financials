// Shared helpers for the deliverable's separate HTML pages
// (comparison.html, banks.html, bank-<slug>.html). Not a framework, no
// bundler - just one <script src="deliverable_shared.js"> tag per page, per
// the user's "multiple plain HTML pages, not an SPA" instruction.

// Institutional ledger palette - muted inks rather than bright SaaS hues,
// with stage/risk colors carrying real semantic meaning (green=performing,
// amber=watch, red=default) rather than decorative variety.
// BANK_COLOR is populated per-page by assignBankColors() from BANKS_INDEX
// (whatever set of banks that page embeds) rather than hardcoded, since the
// deliverable runs against a variable-size bank list, not a fixed 4.
let BANK_COLOR = {};
function assignBankColors(banksIndex){
  // Evenly-spaced hues (golden-angle step) at fixed muted saturation/
  // lightness, so any number of banks gets visually distinct, consistently
  // "institutional" colors rather than a hand-picked palette running out.
  banksIndex.forEach((b, i) => {
    BANK_COLOR[b.name] = `hsl(${Math.round((i * 137.508) % 360)}, 38%, 34%)`;
  });
}
const STAGE_COLOR = { stage_1: "#1f6e52", stage_2: "#a6741f", stage_3: "#9c3b2e" };
const ASSET_COLOR = { cash_pct_of_assets: "#45566b", loans_pct_of_assets: "#1f6e52", treasury_investments_pct_of_assets: "#a6741f", other: "#a39a86" };
const ASSET_LABEL = { cash_pct_of_assets: "Cash & central bank balances", loans_pct_of_assets: "Customer loans", treasury_investments_pct_of_assets: "Treasury investments", other: "Other assets" };
const LIABILITY_COLOR = { customer_deposits_pct: "#1f6e52", bank_deposits_pct: "#45566b", wholesale_funding_pct: "#a6741f", other_pct: "#a39a86" };
const LIABILITY_LABEL = { customer_deposits_pct: "Customer deposits", bank_deposits_pct: "Bank deposits", wholesale_funding_pct: "Wholesale funding (debt in issue + subordinated)", other_pct: "Other liabilities" };
const LIABILITY_ORDER = ["customer_deposits_pct", "bank_deposits_pct", "wholesale_funding_pct", "other_pct"];
const OPEX_COLOR = { personnel_expense: "#1e3a5f", other_operating_expense: "#a6741f" };
const INCOME_COLOR = {
  "Net interest income": "#1e3a5f",
  "Net fee and commission income": "#1f6e52",
  "Trading & investment income": "#5b3a5c",
  "Other income": "#a39a86",
};
const INCOME_ORDER = ["Net interest income", "Net fee and commission income", "Trading & investment income", "Other income"];
// CET1/Tier 1/Total Capital ratios frequently sit on (or near) the same
// value for a bank with little AT1/T2 capital - color alone can't
// distinguish genuinely overlapping lines, so each series also gets its own
// dash pattern and point marker.
const PILLAR3_STYLE = {
  "CET1 Ratio": { color: "#1e3a5f", dash: [], point: "circle" },
  "Tier 1 Ratio": { color: "#7c3a5c", dash: [6, 3], point: "rectRot" },
  "Total Capital Ratio": { color: "#1f6e52", dash: [2, 2], point: "triangle" },
  "Leverage Ratio": { color: "#a6741f", dash: [], point: "rect" },
  "MREL Ratio": { color: "#9c3b2e", dash: [6, 3], point: "star" },
  "LCR": { color: "#5b3a5c", dash: [], point: "circle" },
  "NSFR": { color: "#8c4a2f", dash: [6, 3], point: "rectRot" },
};
const PILLAR3_LABEL = {
  "CET1 Ratio": "CET1 ratio", "Tier 1 Ratio": "Tier 1 ratio", "Total Capital Ratio": "Total capital ratio",
  "Leverage Ratio": "Leverage ratio", "LCR": "LCR", "NSFR": "NSFR", "MREL Ratio": "MREL ratio",
};
const CASHFLOW_ORDER = ["Operating activities", "Investing activities", "Financing activities", "Net change in cash"];
const CASHFLOW_COLOR = {
  "Operating activities": "#1f6e52", "Investing activities": "#1e3a5f",
  "Financing activities": "#a6741f", "Net change in cash": "#52585f",
};
function fmtK(v){ return (v<0?'-£':'£') + Math.round(Math.abs(v)).toLocaleString(); }
// Total assets spans a few million to over a trillion £ across 145 banks -
// fmtK's full-digit form is unreadable as a chart axis tick at that range,
// so balance-sheet.html's size chart abbreviates to £Xbn/£Xm instead;
// tooltips still use fmtK for the exact figure.
function fmtBn(v){
  const sign = v < 0 ? '-£' : '£', abs = Math.abs(v);
  if (abs >= 1e9) return sign + (abs / 1e9).toFixed(abs >= 1e11 ? 0 : 1) + 'bn';
  if (abs >= 1e6) return sign + (abs / 1e6).toFixed(abs >= 1e8 ? 0 : 1) + 'm';
  return fmtK(v);
}
const CATEGORICAL_PALETTE = ["#1e3a5f","#1f6e52","#a6741f","#9c3b2e","#5b3a5c","#45566b","#2b5f63","#8c4a2f","#5c6b73","#8a7f64","#3f4b3a"];
function rwaCatColor(label){
  const l = label.toLowerCase();
  if (l.includes('counterparty')) return '#5b3a5c';
  if (l.includes('securitisation')) return '#2b5f63';
  if (l.includes('market risk') || l.includes('foreign exchange')) return '#1f6e52';
  if (l.includes('operational')) return '#a6741f';
  if (l.includes('credit risk') || l.includes('credit')) return '#1e3a5f';
  return '#8a7f64';
}

function slugify(name){ return name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, ''); }
function latestYear(obj){ const years = Object.keys(obj||{}); return years.length ? years.sort().slice(-1)[0] : null; }
// The most recent year isn't always the most recent USABLE year - a bank
// can fully repay/zero out its disclosed loan book in its latest year
// (Credit Suisse UK's FY2025: every stage balance is 0), which makes
// latestYear() pick a year that renders a blank/NaN chart even though an
// earlier year has real data. Walk backwards from the most recent year to
// find one with an actual non-zero total, so the book-label, chart, and
// coverage chips all agree on the same (real) year.
function latestChartableLoanYear(comp){
  const years = Object.keys(comp.years || {}).sort().reverse();
  for (const y of years) {
    const cats = comp.years[y];
    if (comp.kind === 'stage') {
      const totals = { stage_1: 0, stage_2: 0, stage_3: 0 };
      Object.values(cats).forEach(c => Object.entries(c).forEach(([k, v]) => { if (k in totals) totals[k] += v; }));
      if (totals.stage_1 + totals.stage_2 + totals.stage_3 > 0) return y;
    } else {
      const sum = Object.values(cats).reduce((s, v) => s + (v > 0 ? v : 0), 0);
      if (sum > 0) return y;
    }
  }
  return null;
}
function shortCategoryName(cat){
  const beforeDash = cat.split(' - ')[0];
  return beforeDash.split(',')[0].replace(/^Gross\s+/i, '');
}
function latestCoverageYear(bankData){
  const years = bankData.coverage_npl.map(r => r.year);
  return years.length ? Math.max(...years) : null;
}
function distinguishingLabels(rows){
  // RWA category labels are shaped differently bank to bank: GIB UK repeats
  // its LAST segment across categories ("... - standardised approach" on
  // both Credit risk and Operational risk rows, so the category name is in
  // an EARLIER segment); Weatherbys repeats its FIRST segment ("Credit
  // risk, by exposure class (derived, see sources) - <category>", so the
  // category name is the LATER segment). Neither a fixed first- nor
  // last-segment rule works for both, so scan segment positions left to
  // right and use the first one where every row in this set has a distinct
  // value - that's the segment actually carrying the distinguishing detail.
  const segmented = rows.map(r => r.label.split(' - '));
  const maxLen = Math.max(...segmented.map(s => s.length));
  for (let i = 0; i < maxLen; i++){
    const vals = segmented.map(s => s[i] ?? s[s.length-1]);
    if (new Set(vals).size === rows.length) return vals.map(v => v.replace(/\s*\([^()]*\)\s*$/, '').trim());
  }
  return segmented.map(s => s[s.length-1].replace(/\s*\([^()]*\)\s*$/, '').trim());
}
function coverageChipShortLabel(label){
  // Coverage/NPL rows can repeat the same trailing metric name across
  // different books (e.g. GIB UK's "... - Placements with banks - ECL
  // coverage ratio" vs "... - Debt securities - ECL coverage ratio") - the
  // last segment alone is ambiguous between them, so keep the last two
  // segments when there are enough to disambiguate.
  const parts = label.split(' - ');
  return (parts.length > 2 ? parts.slice(-2) : parts.slice(-1)).join(' — ').replace(/\s*\([^()]*\)\s*$/, '');
}
function coverageNplChipsHtml(bankData, year){
  const rows = bankData.coverage_npl.filter(r => String(r.year) === String(year));
  if (!rows.length) return '<div class="empty-note">No coverage/NPL ratio disclosed this year.</div>';
  return '<div class="chip-row">' + rows.map(r => {
    const shortLabel = coverageChipShortLabel(r.label);
    const isPct = /%$/.test(r.value_raw);
    return `<span class="chip${isPct?'':' raw'}" title="${r.label}"><b>${r.value_raw}</b> ${shortLabel}</span>`;
  }).join('') + '</div>';
}
function stageTotalsForYear(comp, year){
  if (!year || comp.kind !== 'stage') return null;
  const totals = {stage_1:0, stage_2:0, stage_3:0};
  let any = false;
  Object.values(comp.years[year]).forEach(c => Object.entries(c).forEach(([k,v]) => { if (k in totals){ totals[k]+=v; any = true; } }));
  return any ? totals : null;
}

// ---- Chart.js setup ----
Chart.defaults.font.family = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif";
Chart.defaults.font.size = 11;
Chart.defaults.color = '#5b6470';
Chart.defaults.plugins.legend.display = false;

function stageCompositionMiniChart(canvas, categories){
  const totals = {stage_1:0, stage_2:0, stage_3:0};
  let any = false;
  Object.values(categories).forEach(c => Object.entries(c).forEach(([k,v]) => { if (k in totals){ totals[k]+=v; any = true; } }));
  if (!any) return false;
  const sum = totals.stage_1+totals.stage_2+totals.stage_3;
  if (!sum) return false; // all-zero year (e.g. a fully repaid book) - draw nothing rather than NaN bars
  new Chart(canvas, {
    type: 'bar',
    data: { labels: [''], datasets: [
      {label:'Stage 1', data:[totals.stage_1/sum*100], backgroundColor: STAGE_COLOR.stage_1},
      {label:'Stage 2', data:[totals.stage_2/sum*100], backgroundColor: STAGE_COLOR.stage_2},
      {label:'Stage 3', data:[totals.stage_3/sum*100], backgroundColor: STAGE_COLOR.stage_3},
    ]},
    options: {
      indexAxis: 'y', responsive: true, maintainAspectRatio: false,
      scales: { x: { stacked:true, display:false, max:100 }, y: { stacked:true, display:false } },
      plugins: { tooltip: { callbacks: { label: (ctx) => `${ctx.dataset.label}: ${ctx.raw.toFixed(1)}%` } } },
    },
  });
  return true;
}
function exposureClassMiniChart(canvas, categories){
  const entries = Object.entries(categories).filter(([,v])=>v>0).sort((a,b)=>b[1]-a[1]);
  const sum = entries.reduce((s,[,v])=>s+v,0);
  if (!sum) return false;
  new Chart(canvas, {
    type: 'bar',
    data: { labels: [''], datasets: entries.map(([name,v],i) => ({
      label: name, data: [v/sum*100], backgroundColor: CATEGORICAL_PALETTE[i % CATEGORICAL_PALETTE.length],
    })) },
    options: {
      indexAxis: 'y', responsive: true, maintainAspectRatio: false,
      scales: { x: { stacked:true, display:false, max:100 }, y: { stacked:true, display:false } },
      plugins: { tooltip: { callbacks: { label: (ctx) => `${ctx.dataset.label}: ${ctx.raw.toFixed(1)}%` } } },
    },
  });
  return true;
}
function rwaCatMiniChart(canvas, rows){
  // Normalised to this bank-year's own filtered sum (like
  // stageCompositionMiniChart/exposureClassMiniChart), so every bar fills
  // the same 100%-wide space regardless of how many risk categories a bank
  // discloses - real category coverage is consistently ~97-100%+ of Total
  // RWAs across the dataset (verified 2026-09-04, min 97.6%), so this
  // reflects genuine near-complete disclosure rather than manufacturing a
  // full bar out of partial data.
  const filtered = rows.filter(r => r.pct_of_total_rwa > 0.05);
  if (!filtered.length) return false;
  const labels = distinguishingLabels(filtered);
  const sum = filtered.reduce((s, r) => s + r.pct_of_total_rwa, 0);
  new Chart(canvas, {
    type: 'bar',
    data: { labels: [''], datasets: filtered.map((r,i) => ({
      label: labels[i], data: [r.pct_of_total_rwa / sum * 100], backgroundColor: rwaCatColor(r.label),
    })) },
    options: {
      indexAxis: 'y', responsive: true, maintainAspectRatio: false,
      scales: { x: { stacked:true, display:false, max: 100 }, y: { stacked:true, display:false } },
      plugins: { tooltip: { callbacks: { label: (ctx) => `${ctx.dataset.label}: ${ctx.raw.toFixed(1)}%` } } },
    },
  });
  return true;
}
// Fuller RWA-category chart (one horizontal bar per category, with axis
// labels/%'s shown) - used by the per-bank drilldown page, which has a full
// detail panel to draw into rather than rwaCatMiniChart's small card space.
// Resizes its own `.mini-chart-wrap` to fit however many categories this
// bank discloses.
function rwaCatChart(canvas, rows){
  if (!rows) return false;
  const filtered = rows.filter(r => r.pct_of_total_rwa > 0.05);
  if (!filtered.length) return false;
  const wrap = canvas.closest('.mini-chart-wrap');
  if (wrap) wrap.style.height = Math.max(150, filtered.length * 28) + 'px';
  new Chart(canvas, {
    type: 'bar',
    data: { labels: distinguishingLabels(filtered), datasets: [{
      data: filtered.map(r => r.pct_of_total_rwa), backgroundColor: filtered.map(r => rwaCatColor(r.label)),
    }] },
    options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false,
      scales: { x: { ticks: { callback: v => v+'%' }, grid: { color: '#edece7' } }, y: { grid: { display: false } } },
    },
  });
  return true;
}
// Same rows/threshold/coloring as rwaCatChart above - just a pie instead of
// a bar, as an alternate view (user request, 2026-09-08) toggled from the
// per-bank drilldown page rather than replacing the bar outright, since a
// stacked bar is still the easier read when one category dominates.
function rwaCatPieChart(canvas, rows){
  if (!rows) return false;
  const filtered = rows.filter(r => r.pct_of_total_rwa > 0.05);
  if (!filtered.length) return false;
  const wrap = canvas.closest('.mini-chart-wrap');
  if (wrap) wrap.style.height = '340px';
  new Chart(canvas, {
    type: 'pie',
    data: { labels: distinguishingLabels(filtered), datasets: [{
      data: filtered.map(r => r.pct_of_total_rwa), backgroundColor: filtered.map(r => rwaCatColor(r.label)),
      borderColor: '#fff', borderWidth: 1,
    }] },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: {
        legend: { display: true, position: 'right', labels: { boxWidth: 10, font: { size: 11 } } },
        tooltip: { callbacks: { label: (ctx) => `${ctx.label}: ${ctx.raw.toFixed(1)}%` } },
      },
    },
  });
  return true;
}
function rwaTrendLineChart(canvas, banks, data){
  const years = [...new Set(banks.flatMap(b => Object.keys(data[b].rwa_to_assets_pct)))].sort();
  return new Chart(canvas, {
    type: 'line',
    data: { labels: years, datasets: banks.map(b => ({
      label: b, data: years.map(y => data[b].rwa_to_assets_pct[y] ?? null),
      borderColor: BANK_COLOR[b], backgroundColor: BANK_COLOR[b], tension: 0.15, spanGaps: true, pointRadius: 3,
    })) },
    options: {
      responsive:true, maintainAspectRatio:false,
      scales: { y: { ticks: { callback: v => v+'%' }, grid:{color:'#edece7'} }, x: { grid:{display:false} } },
      plugins: {
        legend: { display:true, position:'bottom', labels:{boxWidth:10, font:{size:10}, usePointStyle:true} },
        tooltip: { callbacks: { label: (ctx) => `${ctx.dataset.label}: ${ctx.raw}%` } },
      },
    },
  });
}

// A picker of checkboxes above the RWA-density trend chart, capped at 5
// banks selected at once - with all 20+ banks plotted together the line
// chart becomes an unreadable tangle, so this keeps it comparable while
// still letting the reader choose which banks. The per-bank RWA-composition
// mini-cards below aren't affected - one card per bank scales fine as a
// grid, it's only the overlaid multi-line chart that gets crowded.
const RWA_PICKER_MAX = 5;
// The 5-year window every bank COULD have (FY2021-FY2025) - banks with real
// data across exactly these five years make the most informative default
// trend line (no gaps, and no stray extra year like Starling Bank's 2026
// data point sticking out past every other bank's line) rather than
// whichever 5 banks happen to sort first.
const RWA_FULL_COVERAGE_YEARS = ['2021', '2022', '2023', '2024', '2025'];
function defaultRwaBanks(banks, data){
  const hasFullCoverage = b => {
    const years = Object.keys(data[b].rwa_to_assets_pct).filter(y => data[b].rwa_to_assets_pct[y] != null);
    return RWA_FULL_COVERAGE_YEARS.every(y => years.includes(y))
      && years.every(y => RWA_FULL_COVERAGE_YEARS.includes(y));
  };
  const full = banks.filter(hasFullCoverage);
  if (full.length >= RWA_PICKER_MAX) return full.slice(0, RWA_PICKER_MAX);
  const rest = banks.filter(b => !hasFullCoverage(b));
  return [...full, ...rest].slice(0, RWA_PICKER_MAX);
}
function initRwaBankPicker(container, canvas, banks, data){
  let selected = new Set(defaultRwaBanks(banks, data));
  function redraw(){
    if (container._chart) container._chart.destroy();
    const chosen = banks.filter(b => selected.has(b));
    container._chart = chosen.length ? rwaTrendLineChart(canvas, chosen, data) : null;
    container.querySelectorAll('input[type=checkbox]').forEach(cb => {
      const isChecked = selected.has(cb.value);
      cb.checked = isChecked;
      cb.closest('label').classList.toggle('disabled', !isChecked && selected.size >= RWA_PICKER_MAX);
    });
  }
  container.querySelectorAll('input[type=checkbox]').forEach(cb => {
    cb.addEventListener('change', () => {
      if (cb.checked){
        if (selected.size >= RWA_PICKER_MAX) { cb.checked = false; return; }
        selected.add(cb.value);
      } else {
        selected.delete(cb.value);
      }
      redraw();
    });
  });
  redraw();
}

// ---- comparison.html: ratio trajectories (IN-052) ----
// Migrated from the old dashboard's in024 section - the only place in
// deliverable/ with a time dimension at all (every other chart here is
// "latest year with data"). Restyled onto this page's own bank-picker +
// Chart.js line-chart pattern (see rwaTrendLineChart/initRwaBankPicker
// above) rather than porting the old dashboard's bespoke hand-rolled
// SVG drag-to-zoom interaction - Chart.js's built-in hover tooltips cover
// the same "what's this point" need without that extra machinery.
//
// in024/in021's payloads key banks by their own `frn`/`bank` fields (the
// full legal entity name from canonical_bank, e.g. "MONUMENT BANK
// LIMITED"), not this page's curated short display names (e.g. "Monument
// Bank") - frnToBankName() bridges the two via the frn every bank record
// in `data` already carries, so BANK_COLOR lookups and bank-page links
// stay consistent with the rest of the site.
function frnToBankName(data){
  const map = {};
  Object.entries(data).forEach(([name, bd]) => { map[String(bd.frn)] = name; });
  return map;
}

function trajectoryLineChart(canvas, metric, banks, trends, frnName){
  const byBank = {};
  trends.metrics[metric].forEach(r => { byBank[frnName[r.frn] || r.bank] = r; });
  const years = trends.years;
  return new Chart(canvas, {
    type: 'line',
    data: { labels: years.map(y => 'FY'+y), datasets: banks.filter(b => byBank[b]).map(b => {
      const byYear = {};
      byBank[b].points.forEach(p => { byYear[p.year] = p.value; });
      return {
        label: b, data: years.map(y => byYear[y] ?? null),
        borderColor: BANK_COLOR[b], backgroundColor: BANK_COLOR[b], tension: 0.15, spanGaps: false, pointRadius: 2.5,
      };
    }) },
    options: {
      responsive:true, maintainAspectRatio:false,
      scales: { y: { ticks: { callback: v => v+'%' }, grid:{color:'#edece7'} }, x: { grid:{display:false} } },
      plugins: {
        legend: { display:true, position:'bottom', labels:{boxWidth:10, font:{size:10}, usePointStyle:true} },
        tooltip: { callbacks: { label: (ctx) => `${ctx.dataset.label}: ${ctx.raw==null?'—':ctx.raw+'%'}` } },
      },
    },
  });
}

// Same style as RWA density's default picker (see defaultRwaBanks/
// RWA_PICKER_MAX above): a 5-bank cap, and an exact match to the full
// FY2021-FY2025 window preferred over "most complete" so the default line
// never has a gap or a stray extra year (server-side curate_comparison_
// trends() already trims trends.years to just this window).
const TRAJECTORY_PICKER_MAX = 5;
function defaultTrajectoryBanks(metric, banks, trends, frnName){
  const byBank = {};
  trends.metrics[metric].forEach(r => { byBank[frnName[r.frn] || r.bank] = r; });
  const hasFullCoverage = b => {
    const rec = byBank[b];
    if (!rec) return false;
    const covered = new Set(rec.points.filter(p => p.value != null).map(p => p.year));
    return trends.years.every(y => covered.has(y)) && covered.size === trends.years.length;
  };
  const full = banks.filter(b => byBank[b] && hasFullCoverage(b));
  if (full.length >= TRAJECTORY_PICKER_MAX) return full.slice(0, TRAJECTORY_PICKER_MAX);
  const rest = banks.filter(b => byBank[b] && !hasFullCoverage(b));
  return [...full, ...rest].slice(0, TRAJECTORY_PICKER_MAX);
}

function initTrajectoryBankPicker(container, canvas, metric, banks, trends, frnName){
  let selected = new Set(defaultTrajectoryBanks(metric, banks, trends, frnName));
  function redraw(){
    if (container._chart) container._chart.destroy();
    const chosen = banks.filter(b => selected.has(b));
    container._chart = chosen.length ? trajectoryLineChart(canvas, metric, chosen, trends, frnName) : null;
    container.querySelectorAll('input[type=checkbox]').forEach(cb => {
      const isChecked = selected.has(cb.value);
      cb.checked = isChecked;
      cb.closest('label').classList.toggle('disabled', !isChecked && selected.size >= TRAJECTORY_PICKER_MAX);
    });
  }
  container.querySelectorAll('input[type=checkbox]').forEach(cb => {
    cb.addEventListener('change', () => {
      if (cb.checked){
        if (selected.size >= TRAJECTORY_PICKER_MAX) { cb.checked = false; return; }
        selected.add(cb.value);
      } else {
        selected.delete(cb.value);
      }
      redraw();
    });
  });
  redraw();
}

// A searchable, scrollable sidebar version of the plain .bank-picker
// checkbox grid (see initRwaBankPicker above) - same checkbox-driven
// overlay-chart behavior, just findable in a list of ~145 banks instead of
// scanning a flat wall of checkboxes. The returned root keeps idPrefix as
// its own id, so it's a drop-in replacement anywhere a plain .bank-picker
// checkbox container was expected (initTrajectoryBankPicker etc. just
// query `input[type=checkbox]` inside it).
function bankPickerSidebarHtml(idPrefix, banks){
  return `<div class="bank-picker-sidebar" id="${idPrefix}">
    <div class="bank-picker-search"><input type="text" placeholder="Search banks…" autocomplete="off"></div>
    <div class="bank-picker-list">
      ${banks.map(b => `<label><input type="checkbox" value="${b}"><span class="sw" style="background:${BANK_COLOR[b]}"></span><span class="n">${b}</span></label>`).join('')}
    </div>
    <div class="bank-picker-none" hidden>No banks match.</div>
  </div>`;
}
function wireBankPickerSearch(container){
  const search = container.querySelector('.bank-picker-search input');
  const none = container.querySelector('.bank-picker-none');
  if (!search) return;
  search.addEventListener('input', () => {
    const q = search.value.trim().toLowerCase();
    let anyVisible = false;
    container.querySelectorAll('.bank-picker-list label').forEach(el => {
      const match = el.querySelector('.n').textContent.toLowerCase().includes(q);
      el.style.display = match ? '' : 'none';
      if (match) anyVisible = true;
    });
    none.hidden = anyVisible;
  });
}

// ---- comparison.html: regulatory headroom trajectory (IN-052) ----
// Migrated from the old dashboard's in021 section. Filtered to `status ===
// 'screened'` only, matching this page's established convention (see the
// comment above renderComparisonPage) of showing each block only the
// records it can actually say something about - the ~150 "no regulatory
// context" and "insufficient evidence" records aren't a comparison, they're
// coverage gaps, and belong in the per-bank/QA views, not a client-facing
// screening table.
function headroomTableHtml(records){
  const screened = records.filter(r => r.status === 'screened');
  const fmt = (v, suffix) => v == null ? '—' : v.toFixed(2) + (suffix || '');
  const rows = screened.map(r => `<tr data-bank="${r.bank}" data-metric="${r.metric}" data-latest="${r.latest_year}" data-current="${r.current_value ?? ''}" data-floor="${r.regulatory_floor ?? ''}" data-headroom="${r.current_headroom ?? ''}" data-direction="${r.trend_direction || ''}" data-change="${r.trend_change ?? ''}">
    <td>${r.bank}</td><td>${r.metric}</td><td>FY${r.latest_year}</td>
    <td class="num">${fmt(r.current_value, '%')}</td><td class="num">${fmt(r.regulatory_floor, '%')}</td>
    <td class="num">${fmt(r.current_headroom, 'pp')}</td><td>${r.trend_direction || '—'}</td>
    <td class="num">${fmt(r.trend_change, 'pp')}</td>
  </tr>`).join('');
  const cols = [['bank','Bank'],['metric','Metric'],['latest','Latest'],['current','Current'],
    ['floor','Floor'],['headroom','Headroom'],['direction','Direction'],['change','Change']];
  return `<table class="bank-table headroom-table" id="headroom-table" data-sortable><thead><tr>${
    cols.map(([key,label]) => `<th><button type="button" class="sort-col" data-sort-key="${key}">${label}</button></th>`).join('')
  }</tr></thead><tbody>${rows}</tbody></table>`;
}
// ---- per-bank page: how far above the regulatory minimum this bank is,
// per metric (same in021 screening records as the comparison table above,
// filtered to this bank's own frn - user request, 2026-09-05) ----
function bankHeadroomTableHtml(records){
  const screened = (records || []).filter(r => r.status === 'screened');
  if (!screened.length) return null;
  const fmt = (v, suffix) => v == null ? '—' : v.toFixed(2) + (suffix || '');
  const rows = screened.map(r => `<tr>
    <td>${r.metric}</td><td>FY${r.latest_year}</td>
    <td class="num">${fmt(r.current_value, '%')}</td><td class="num">${fmt(r.regulatory_floor, '%')}</td>
    <td class="num">${fmt(r.current_headroom, 'pp')}</td><td>${r.trend_direction || '—'}</td>
    <td class="num">${fmt(r.trend_change, 'pp')}</td>
  </tr>`).join('');
  return `<table class="bank-table"><thead><tr>
    <th>Metric</th><th>Latest</th><th>Current</th><th>Floor</th><th>Headroom</th><th>Direction</th><th>Change</th>
  </tr></thead><tbody>${rows}</tbody></table>`;
}

// ---- comparison.html: "most extreme" (IN-052 follow-up) ----
// Reuses in009_analysis.py's detect_outliers() flags (extreme level,
// extreme year-over-year movement, or a special/non-standard disclosure)
// on each bank's latest value per core metric - no new statistical work.
function outliersTableHtml(records){
  const fmt = v => v == null ? '—' : (Math.abs(v) < 1000 ? v.toFixed(2) : v.toFixed(0));
  const rows = records.map(r => `<tr data-bank="${r.bank}" data-metric="${r.metric}" data-year="${r.fiscal_year}" data-value="${r.value ?? ''}" data-reasons="${r.reasons.length}">
    <td>${r.bank}</td><td>${r.metric}</td><td>FY${r.fiscal_year}</td>
    <td class="num">${fmt(r.value)}${typeof r.value === 'number' && Math.abs(r.value) <= 100 ? '%' : ''}</td>
    <td>${r.reasons.join('; ')}</td>
  </tr>`).join('');
  const cols = [['bank','Bank'],['metric','Metric'],['year','Latest'],['value','Value'],['reasons','Flagged for']];
  return `<table class="bank-table" data-sortable><thead><tr>${
    cols.map(([key,label]) => `<th><button type="button" class="sort-col" data-sort-key="${key}">${label}</button></th>`).join('')
  }</tr></thead><tbody>${rows}</tbody></table>`;
}

// ---- comparison.html: parent groupings (IN-052 follow-up) ----
// Reintroduces the old dashboard's parent-group dispersion/trend-agreement
// analysis - do commonly-owned legal entities report similar Pillar 3
// outcomes. Relationship between banks, not a per-bank fact, so it's kept
// as its own section rather than folded into another block.
function totalPnlLatest(groupMeta){
  const years = Object.keys(groupMeta.total_pnl_by_year || {}).sort();
  if (!years.length) return null;
  const y = years[years.length - 1];
  return { year: y, value: groupMeta.total_pnl_by_year[y] };
}

const TREND_ARROW = { '+': '▲', '-': '▼', 'mixed': '◆', 'unchanged': '▬' };

// One row per group, one column per core metric (2026-09-05 follow-up:
// was one table per metric - collapsed into a single pivoted table so a
// group's whole Pillar 3 posture reads in one line). Each cell's hover
// title carries the min/max/range/trend detail the old per-metric table
// spelled out in columns - the group's own overview page is where that
// detail earns full real estate (see groupMetricChartsHtml).
function parentGroupsTableHtml(parentGroups){
  const metrics = parentGroups.metrics, groupMeta = parentGroups.group_meta || {};
  const metricNames = Object.keys(metrics);
  const byGroup = new Map();
  metricNames.forEach(metric => {
    metrics[metric].forEach(g => {
      if (!byGroup.has(g.group)) byGroup.set(g.group, { group: g.group, member_count: g.member_count, cells: {} });
      byGroup.get(g.group).cells[metric] = g;
    });
  });
  const groups = [...byGroup.values()].sort((a, b) => a.group.localeCompare(b.group));
  const rows = groups.map(row => {
    const pnl = totalPnlLatest(groupMeta[row.group] || {});
    const pnlText = pnl ? `${fmtK(pnl.value)} <span class="hint">FY${pnl.year}</span>` : '—';
    const groupLink = `<a href="group-${slugify(row.group)}.html">${row.group}</a>`;
    const metricCells = metricNames.map(metric => {
      const g = row.cells[metric];
      if (!g) return '<td class="num">—</td>';
      const latest = g.trends.length ? g.trends[g.trends.length - 1] : null;
      const trendTitle = latest
        ? `FY${latest.start_year}→FY${latest.end_year}: ${latest.direction} (${Math.round(latest.agreement * 100)}% agree, n=${latest.n})`
        : 'not enough years to compare';
      const cellTitle = `FY${g.year} · min ${g.min.toFixed(2)}% · max ${g.max.toFixed(2)}% · range ${g.range.toFixed(2)}pp · ${trendTitle}`;
      return `<td class="num" data-${slugify(metric)}="${g.median}" title="${cellTitle}">${g.median.toFixed(2)}% <span class="trend-arrow">${TREND_ARROW[latest ? latest.direction : ''] || ''}</span></td>`;
    });
    return `<tr data-group="${row.group}" data-members="${row.member_count}"><td>${groupLink}</td><td class="num">${row.member_count}</td><td class="num">${pnlText}</td>${metricCells.join('')}</tr>`;
  }).join('');
  return `<table class="bank-table" data-sortable><thead><tr>
    <th><button type="button" class="sort-col" data-sort-key="group">Group</button></th>
    <th><button type="button" class="sort-col" data-sort-key="members">Members</button></th>
    <th>Total P&amp;L</th>
    ${metricNames.map(m => `<th><button type="button" class="sort-col" data-sort-key="${slugify(m)}">${m}</button> <span class="hint">median</span></th>`).join('')}
  </tr></thead><tbody>${rows}</tbody></table>`;
}

// group-<slug>.html: one bar chart per core metric, each bar a member
// bank's own latest comparable value (user request, 2026-09-05: "add more
// graphs, displaying the contributions from each child bank"). Distinct
// from parentGroupsTableHtml's median/range summary - this is the per-
// member breakdown behind that summary.
function groupMetricChartsHtml(metrics){
  const metricNames = Object.keys(metrics);
  if (!metricNames.length) return '<div class="empty-note">No metric has a comparable latest year across every member.</div>';
  return metricNames.map(metric => {
    const g = metrics[metric][0];
    const latest = g.trends.length ? g.trends[g.trends.length - 1] : null;
    const trendText = latest
      ? `FY${latest.start_year}→FY${latest.end_year}: ${latest.direction} (${Math.round(latest.agreement * 100)}% agree, n=${latest.n})`
      : 'not enough years to compare';
    const memberCount = Object.keys(g.values).length;
    return `<div style="margin-bottom:26px;">
      <h3 style="font-family:var(--font-serif);font-size:14px;margin:0 0 4px;">${metric}</h3>
      <span class="hint">FY${g.year} · median ${g.median.toFixed(2)}% · range ${g.range.toFixed(2)}pp · ${trendText}</span>
      <div class="mini-chart-wrap" style="height:${Math.max(90, memberCount * 32)}px;margin-top:8px;" data-group-metric-chart="${slugify(metric)}"><canvas></canvas></div>
    </div>`;
  }).join('');
}

function mountGroupMetricCharts(metrics){
  Object.keys(metrics).forEach(metric => {
    const g = metrics[metric][0];
    const canvas = document.querySelector(`[data-group-metric-chart="${slugify(metric)}"] canvas`);
    if (!canvas) return;
    const entries = Object.entries(g.values).sort((a, b) => b[1] - a[1]);
    new Chart(canvas, {
      type: 'bar',
      data: { labels: entries.map(([bank]) => bank), datasets: [{
        data: entries.map(([, v]) => v),
        backgroundColor: entries.map(([bank]) => BANK_COLOR[bank] || '#2563eb'),
      }] },
      options: {
        indexAxis: 'y', responsive: true, maintainAspectRatio: false,
        scales: { x: { ticks: { callback: v => v + '%' }, grid: { color: '#edece7' } }, y: { grid: { display: false } } },
        plugins: { legend: { display: false }, tooltip: { callbacks: { label: ctx => `${ctx.raw}%` } } },
      },
    });
  });
}

function initSortableTables(){
  document.querySelectorAll('table[data-sortable]').forEach(table => {
    let currentKey = null, ascending = true;
    table.querySelectorAll('.sort-col').forEach(btn => {
      btn.addEventListener('click', () => {
        const key = btn.dataset.sortKey;
        ascending = currentKey === key ? !ascending : true;
        currentKey = key;
        const tbody = table.querySelector('tbody');
        const rows = [...tbody.querySelectorAll('tr')];
        rows.sort((a, b) => {
          const av = a.getAttribute('data-' + key), bv = b.getAttribute('data-' + key);
          const an = parseFloat(av), bn = parseFloat(bv);
          const cmp = (!isNaN(an) && !isNaN(bn)) ? an - bn : String(av).localeCompare(String(bv));
          return ascending ? cmp : -cmp;
        });
        rows.forEach(r => tbody.appendChild(r));
      });
    });
  });
}

// Same "latest year isn't always usable" issue as loan concentration (see
// latestChartableLoanYear) - HSBC Innovation Bank's FY2023 cash/treasury
// figures are both genuinely 0 (a transition-year balance sheet), which
// made the most-recent-year chart render as "100% Other" and disappear
// even though FY2022 has a real, informative asset mix.
function latestChartableCapitalYear(cap){
  const years = Object.keys(cap || {}).sort().reverse();
  for (const y of years) {
    const mix = assetMixForYear(cap[y]);
    if (Object.entries(mix).some(([k, v]) => k !== 'other' && v != null && v > 0)) return y;
  }
  return null;
}
function assetMixForYear(capYear){
  const cash = capYear.cash_pct_of_assets, loans = capYear.loans_pct_of_assets, treasury = capYear.treasury_investments_pct_of_assets;
  const known = [cash, loans, treasury].filter(v => v != null).reduce((s,v)=>s+v, 0);
  const other = Math.max(0, 100 - known);
  return { cash_pct_of_assets: cash, loans_pct_of_assets: loans, treasury_investments_pct_of_assets: treasury, other };
}
function capitalCompositionMiniChart(canvas, capYear){
  const mix = assetMixForYear(capYear);
  const entries = Object.entries(mix).filter(([,v]) => v != null && v > 0);
  if (entries.length <= 1 && mix.other >= 99.5) return false;
  new Chart(canvas, {
    type: 'bar',
    data: { labels: [''], datasets: entries.map(([k,v]) => ({
      label: ASSET_LABEL[k], data: [v], backgroundColor: ASSET_COLOR[k],
    })) },
    options: {
      indexAxis: 'y', responsive: true, maintainAspectRatio: false,
      scales: { x: { stacked:true, display:false, max:100 }, y: { stacked:true, display:false } },
      plugins: { tooltip: { callbacks: { label: (ctx) => `${ctx.dataset.label}: ${ctx.raw.toFixed(1)}%` } } },
    },
  });
  return true;
}
const SYNTH_REVENUE_TIP = 'This bank\'s filing has no explicit "Total/Net operating income" line for this year - revenue is the sum of the Income mix categories below instead (same net basis as other years), so cost-to-income stays comparable rather than just stopping.';
const EQUITY_BALANCE_ROW_RE = /\bbalance\b/i;
const _EQUITY_BUCKET_ORDER = [
  'total_comprehensive', 'profit_loss', 'oci', 'dividend', 'share_capital',
  'share_based_payments', 'prior_year_adjustment', 'other',
];
function equityMovementsChart(canvas, equity){
  // Horizontal stacked bar, one row per fiscal year: each movement bucket
  // is a stacked segment, diverging left/right of zero (Chart.js stacks
  // positive and negative values on opposite sides of the zero baseline
  // natively) - every segment sits flush against its neighbours, so
  // nothing floats disconnected the way the old waterfall's movement bars
  // did.
  const segments = (equity && equity.waterfall) || [];
  if (!segments.length || !canvas) return false;
  const present = new Set();
  const labelFor = {};
  segments.forEach(seg => seg.bars.forEach(b => { present.add(b.bucket); labelFor[b.bucket] = b.label; }));
  const bucketKeys = _EQUITY_BUCKET_ORDER.filter(k => present.has(k));
  if (present.has('reconciling')) bucketKeys.push('reconciling');
  const colorFor = (bucket) => bucket === 'reconciling'
    ? '#a39a86'
    : CATEGORICAL_PALETTE[_EQUITY_BUCKET_ORDER.indexOf(bucket) % CATEGORICAL_PALETTE.length];
  const datasets = bucketKeys.map(k => ({
    label: labelFor[k], backgroundColor: colorFor(k),
    data: segments.map(seg => (seg.bars.find(b => b.bucket === k) || {}).value ?? 0),
  }));
  // `seg.year` is already unique and pre-formatted server-side (curate_
  // equity_waterfall in build_deliverable.py) - a plain year or year range
  // ("2013", "1999–2012") gets the usual "FY" prefix, but an archival
  // same-year checkpoint disambiguated by its own date ("Feb 1998") reads
  // fine as-is and would look broken as "FYFeb 1998".
  const rowLabels = segments.map(s => /^\d/.test(s.year) ? `FY${s.year}` : s.year);
  return new Chart(canvas, {
    type: 'bar',
    data: { labels: rowLabels, datasets },
    options: {
      indexAxis: 'y',
      responsive: true, maintainAspectRatio: false,
      scales: {
        x: { stacked: true, ticks: { callback: v => fmtK(v) }, grid: { color: '#edece7' } },
        y: { stacked: true, grid: { display: false } },
      },
      plugins: {
        legend: { display: true, position: 'bottom', labels: { boxWidth: 10, font: { size: 10 }, usePointStyle: true } },
        tooltip: {
          filter: (item) => item.raw !== 0,
          callbacks: { label: (ctx) => `${ctx.dataset.label}: ${ctx.raw >= 0 ? '+' : ''}${fmtK(ctx.raw)}` },
        },
      },
    },
  });
}
// Same "recent by default, full history behind a toggle" treatment as
// `mountHistoryChart` (capital deployment, income mix, etc.), adapted for
// a horizontal one-row-per-segment chart whose natural size axis is
// height, not width: archival segments (`start_year` before
// ARCHIVE_HISTORY_CUTOFF - Union Bancaire Privee UK's own pre-2013
// checkpoints, several of them undisclosed-movement gaps, PLUS any range
// segment that starts archival even if it closes more recently) are
// hidden by default rather than always rendered, so a bank with decades
// of history doesn't force every viewer to scroll past it to reach the
// recent years.
function mountEquityMovementsChart(id, equity){
  const host = document.getElementById(id);
  if (!host) return;
  const allSegments = (equity && equity.waterfall) || [];
  const recentSegments = allSegments.filter(s => s.start_year == null || s.start_year >= ARCHIVE_HISTORY_CUTOFF);
  const toggle = host.querySelector('[data-history-toggle]');
  const caption = host.querySelector('[data-history-caption]');
  const wrap = host.querySelector('.mini-chart-wrap');
  const canvas = host.querySelector('canvas');
  let fullHistory = false;
  let chart = null;
  function redraw(){
    const shown = fullHistory ? allSegments : recentSegments;
    wrap.style.height = `${Math.max(150, shown.length * 34 + 50)}px`;
    if (chart) chart.destroy();
    chart = equityMovementsChart(canvas, { ...equity, waterfall: shown }) || null;
    if (toggle) toggle.textContent = fullHistory ? `Show FY${ARCHIVE_HISTORY_CUTOFF} onwards` : 'Show full available history';
    if (caption) {
      const oldestYear = allSegments.length ? Math.min(...allSegments.map(s => s.start_year).filter(y => y != null)) : null;
      const newestYear = allSegments.length ? Math.max(...allSegments.map(s => s.end_year).filter(y => y != null)) : null;
      caption.textContent = fullHistory
        ? `Showing FY${oldestYear}–FY${newestYear}`
        : `Showing FY${ARCHIVE_HISTORY_CUTOFF} onwards`;
    }
  }
  if (toggle) toggle.addEventListener('click', () => { fullHistory = !fullHistory; redraw(); });
  redraw();
}
function equityMixChart(canvas, equity, years){
  const shown = years || Object.keys(equity.mix_by_year || {}).sort();
  if (!shown.length) return false;
  const comps = equity.components.filter(c => shown.some(y => c in equity.mix_by_year[y]));
  if (!comps.length) return false;
  return new Chart(canvas, {
    type: 'bar',
    data: { labels: shown, datasets: comps.map((c, i) => ({
      label: c, data: shown.map(y => equity.mix_by_year[y][c] ?? 0),
      backgroundColor: CATEGORICAL_PALETTE[i % CATEGORICAL_PALETTE.length],
    })) },
    options: {
      responsive: true, maintainAspectRatio: false,
      scales: {
        x: { stacked: true, grid: { display: false } },
        y: { stacked: true, ticks: { callback: v => fmtK(v) }, grid: { color: '#edece7' } },
      },
      plugins: {
        legend: { display: true, position: 'bottom', labels: { boxWidth: 10, font: { size: 10 }, usePointStyle: true } },
        tooltip: { callbacks: { label: (ctx) => `${ctx.dataset.label}: ${fmtK(ctx.raw)}` } },
      },
    },
  });
}
function equityChangesTableHtml(equity){
  if (!equity || !equity.rows || !equity.rows.length) {
    return '<div class="empty-note">No Statement of Changes in Equity disclosed for this bank.</div>';
  }
  const { components, rows } = equity;
  const fmtCell = v => v == null || v === '' ? '—' : (/^-?[\d,]+(\.\d+)?$/.test(v) ? Number(v.replace(/,/g,'')).toLocaleString() : v);
  const head = `<tr><th>Movement</th>${components.map(c=>`<th>${c}</th>`).join('')}</tr>`;
  const body = rows.map(r => {
    const cls = EQUITY_BALANCE_ROW_RE.test(r.label) ? ' class="total-row"' : '';
    return `<tr${cls}><td>${r.label}</td>${components.map(c=>`<td>${fmtCell(r.values[c])}</td>`).join('')}</tr>`;
  }).join('');
  return `<div class="equity-table-wrap"><table class="equity-table"><thead>${head}</thead><tbody>${body}</tbody></table></div>`;
}
function costBaseChipsHtml(costYear){
  if (!costYear) return '<div class="empty-note">No cost-base data disclosed.</div>';
  const chips = [];
  if (costYear.cost_to_income_pct != null) chips.push([costYear.cost_to_income_pct.toFixed(1)+'%', 'Cost-to-income']);
  if (costYear.revenue != null) chips.push([fmtK(costYear.revenue), 'Total revenue' + (costYear.revenue_is_synthesized ? ' <span class="kind-flag" data-tip="'+SYNTH_REVENUE_TIP+'">ⓘ derived</span>' : '')]);
  if (costYear.personnel_expense != null) chips.push([fmtK(Math.abs(costYear.personnel_expense)), 'Personnel expense']);
  if (costYear.other_operating_expense != null) chips.push([fmtK(Math.abs(costYear.other_operating_expense)), 'Other opex']);
  if (!chips.length) return '<div class="empty-note">No cost-base data disclosed.</div>';
  return '<div class="chip-row">' + chips.map(([v,l]) => `<span class="chip raw"><b>${v}</b> ${l}</span>`).join('') + '</div>';
}
const COST_TABLE_ROWS = [
  {key:'cost_to_income_pct', label:'Cost-to-income', fmt:v=>v.toFixed(1)+'%'},
  {key:'revenue', label:'Total revenue', fmt:v=>fmtK(v)},
  {key:'personnel_expense', label:'Personnel expense', fmt:v=>fmtK(Math.abs(v))},
  {key:'other_operating_expense', label:'Other opex', fmt:v=>fmtK(Math.abs(v))},
];
function costBaseTableHtml(data, banks){
  // Banks as rows, metrics as columns - with 20 banks a bank-per-column
  // layout scrolls horizontally forever, while a bank-per-row table reads
  // top to bottom like the rest of this page's bank listings (banks.html).
  let html = `<div class="card" style="padding:0;overflow-x:auto;">
    <table class="bank-table cost-table">
      <thead><tr><th>Bank</th><th>FY</th>${COST_TABLE_ROWS.map(r => `<th>${r.label}</th>`).join('')}</tr></thead>
      <tbody>`;
  banks.forEach(b => {
    const y = latestYear(data[b].cost_base);
    const cost = y ? data[b].cost_base[y] : null;
    html += `<tr><td><a href="bank-${slugify(b)}.html">${b}</a></td><td class="num">${y||'—'}</td>`;
    COST_TABLE_ROWS.forEach(r => {
      const v = cost ? cost[r.key] : null;
      const flag = (r.key === 'revenue' && cost && cost.revenue_is_synthesized)
        ? ` <span class="kind-flag" data-tip="${SYNTH_REVENUE_TIP}">ⓘ</span>` : '';
      html += `<td class="num">${v != null ? r.fmt(v) + flag : '—'}</td>`;
    });
    html += `</tr>`;
  });
  html += `</tbody></table></div>`;
  return html;
}
function incomeMixPct(yearCats){
  const total = INCOME_ORDER.reduce((s,k) => s + (yearCats[k]||0), 0);
  const mix = {};
  INCOME_ORDER.forEach(k => { if (yearCats[k] != null) mix[k] = total ? yearCats[k]/total*100 : 0; });
  return mix;
}

const PILLAR3_CAPITAL_SHEETS = ["CET1 Ratio", "Tier 1 Ratio", "Total Capital Ratio", "Leverage Ratio", "MREL Ratio"];
const PILLAR3_LIQUIDITY_SHEETS = ["LCR", "NSFR"];
// Per-bank strength scorecard (user request, 2026-09-08): a radar/spider
// chart, one point per Pillar 3 metric, plotting this bank's PERCENTILE
// RANK (0-100, pre-computed server-side by curate_radar_percentiles - see
// that function's own docstring for why raw %'s can't share one radar
// scale) rather than the raw ratio. A dashed "peer median" ring at 50 on
// every axis gives an immediate visual reference: past the ring on an axis
// is stronger than the median bank, short of it is weaker.
const RADAR_METRIC_ORDER = ["CET1 Ratio", "Leverage Ratio", "LCR", "NSFR", "MREL Ratio", "Total Capital Ratio"];
const RADAR_METRIC_SHORT_LABEL = {
  "CET1 Ratio": "CET1", "Leverage Ratio": "Leverage", "LCR": "LCR", "NSFR": "NSFR",
  "MREL Ratio": "MREL", "Total Capital Ratio": "Total cap.",
};
// Small corner card next to the headline KPIs (moved here + shrunk 2026-
// 09-08 per user feedback - a full-width 420px chart read as more
// prominent than the KPI figures themselves). No legend (no room at this
// size - a title attribute on the card's own wrapper carries the
// explanation instead) and a much lighter fill (0x14 ~= 8% alpha, down
// from 0x33 ~= 20%) so the shape reads as a light wash under the outline,
// not a solid block competing with the KPI numbers beside it.
function radarChart(canvas, radar, bank){
  const labels = RADAR_METRIC_ORDER.filter(m => radar[m]);
  const shortLabels = labels.map(m => RADAR_METRIC_SHORT_LABEL[m] || m);
  const values = labels.map(m => radar[m].percentile);
  const color = BANK_COLOR[bank] || '#2563eb';
  // BANK_COLOR values are hsl(...) strings, not hex - appending a hex alpha
  // suffix (the previous approach) produces an invalid CSS color string
  // that canvas silently ignores, rendering fully opaque instead of faint.
  // Chart.js's own bundled color parser (Chart.helpers.color) understands
  // hsl() and hex alike, so it's used here instead of string concatenation.
  const fill = Chart.helpers.color(color).alpha(0.12).rgbString();
  return new Chart(canvas, {
    type: 'radar',
    data: {
      labels: shortLabels,
      datasets: [
        {
          label: 'Peer median', data: labels.map(() => 50),
          borderColor: '#c7c2b4', backgroundColor: 'transparent', borderDash: [3, 3],
          pointRadius: 0, borderWidth: 1,
        },
        {
          label: bank, data: values,
          borderColor: color, backgroundColor: fill, pointBackgroundColor: color,
          borderWidth: 1.5, pointRadius: 2,
        },
      ],
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      layout: { padding: 4 },
      scales: {
        r: {
          min: 0, max: 100, ticks: { display: false }, backdropColor: 'transparent',
          grid: { color: '#edece7' }, angleLines: { color: '#edece7' }, pointLabels: { font: { size: 9.5 } },
        },
      },
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: (ctx) => {
          if (ctx.dataset.label === 'Peer median') return 'Peer median: 50th percentile';
          const m = labels[ctx.dataIndex];
          const info = radar[m];
          return `${bank}: ${info.value}% (${info.percentile}th percentile of ${info.n_peers} banks)`;
        } } },
      },
    },
  });
}

// Per-bank Sankey flow diagrams (user request, 2026-09-08), via the
// vendored chartjs-chart-sankey plugin (registers a 'sankey' chart type
// once loaded after Chart.js itself - see chartjs-chart-sankey.min.js's
// own script tag in every page's <head>). `centerLabels` names the pass-
// through node(s) ("Total income"/"Total assets") that get a fixed neutral
// color; every other node is colored by first-seen order from the same
// categorical palette used elsewhere in this file, so a bank's Sankey
// doesn't invent a new color language.
function sankeyNodeColorFn(links, centerLabels){
  const seen = [];
  links.forEach(l => { [l.from, l.to].forEach(n => { if (!centerLabels.includes(n) && !seen.includes(n)) seen.push(n); }); });
  const map = {};
  centerLabels.forEach(c => { map[c] = '#45566b'; });
  seen.forEach((n, i) => { map[n] = CATEGORICAL_PALETTE[i % CATEGORICAL_PALETTE.length]; });
  return (name) => map[name] || '#a39a86';
}
function sankeyChart(canvas, links, centerLabels, nodeLabels){
  if (!links || links.length < 2) return null;
  const colorFor = sankeyNodeColorFn(links, centerLabels);
  return new Chart(canvas, {
    type: 'sankey',
    data: { datasets: [{
      data: links,
      colorFrom: (c) => colorFor(c.dataset.data[c.dataIndex].from),
      colorTo: (c) => colorFor(c.dataset.data[c.dataIndex].to),
      colorMode: 'gradient',
      labels: nodeLabels || {},
    }] },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: (ctx) => {
          const p = ctx.raw;
          return `${p.from} → ${p.to}: ${fmtK(p.flow)}`;
        } } },
      },
    },
  });
}

// Derives an ordered build-up/bridge sequence from the exact same links
// data as the P&L Sankey above (curate_bank_pnl_sankey in build_deliverable.py)
// - single source of truth in Python, this is just a different lens on it:
// a step-by-step "income sources -> Total income -> Operating profit ->
// Profit for the year" bridge instead of a flow diagram. User request,
// 2026-09-08 (modeled on the classic "Apple earnings" waterfall alongside
// its Sankey counterpart).
function pnlWaterfallSteps(sankey){
  const links = sankey.links;
  const find = (from, to) => links.find(l => l.from === from && l.to === to);
  const steps = [];
  let running = 0;
  links.forEach(l => {
    if (l.to === 'Total income') {
      steps.push({ label: l.from, value: l.flow, kind: 'increase' });
      running += l.flow;
    } else if (l.from === 'Total income' && l.to.endsWith(' (net cost)')) {
      steps.push({ label: l.to.replace(/ \(net cost\)$/, ''), value: -l.flow, kind: 'decrease' });
      running -= l.flow;
    }
  });
  steps.push({ label: 'Total income', value: running, kind: 'subtotal' });

  const opex = find('Total income', 'Operating expenses');
  if (opex) {
    steps.push({ label: 'Operating expenses', value: -opex.flow, kind: 'decrease' });
    running -= opex.flow;
    steps.push({ label: 'Operating profit', value: running, kind: 'subtotal' });
    const provisions = find('Operating profit', 'Provisions & tax');
    if (provisions) {
      steps.push({ label: 'Provisions & tax', value: -provisions.flow, kind: 'decrease' });
      running -= provisions.flow;
      steps.push({ label: 'Profit for the year', value: running, kind: 'total' });
    }
  } else {
    const costs = find('Total income', 'Costs, provisions & tax');
    if (costs) {
      steps.push({ label: 'Costs, provisions & tax', value: -costs.flow, kind: 'decrease' });
      running -= costs.flow;
      steps.push({ label: 'Profit for the year', value: running, kind: 'total' });
    }
  }
  return steps;
}
// Chart.js has no native waterfall type, but a floating bar (a 'bar'
// dataset whose data points are [low, high] pairs instead of a single
// value) is a first-class, documented Chart.js feature - not a hand-rolled
// chart - and is the standard way this shape gets built with it. A
// grounded [0, value] bar marks each subtotal/total; every other bar
// floats between the running total before and after its own step.
const WATERFALL_COLOR = { increase: '#1f6e52', decrease: '#9c3b2e', subtotal: '#8a8f98', total: '#1e3a5f' };
function pnlWaterfallChart(canvas, sankey){
  const steps = pnlWaterfallSteps(sankey);
  if (!steps.length) return false;
  let running = 0;
  const ranges = steps.map(s => {
    if (s.kind === 'subtotal' || s.kind === 'total') {
      running = s.value;
      return [0, s.value];
    }
    const from = running;
    running += s.value;
    return [Math.min(from, running), Math.max(from, running)];
  });
  new Chart(canvas, {
    type: 'bar',
    data: { labels: steps.map(s => s.label), datasets: [{
      data: ranges, backgroundColor: steps.map(s => WATERFALL_COLOR[s.kind]),
    }] },
    options: {
      responsive: true, maintainAspectRatio: false,
      scales: {
        x: { grid: { display: false }, ticks: { font: { size: 10 }, maxRotation: 30, minRotation: 0 } },
        y: { ticks: { callback: v => fmtK(v) }, grid: { color: '#edece7' } },
      },
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: (ctx) => {
          const s = steps[ctx.dataIndex];
          const sign = s.kind === 'increase' ? '+' : (s.kind === 'decrease' ? '−' : '');
          return `${s.label}: ${sign}${fmtK(Math.abs(s.value))}`;
        } } },
      },
    },
  });
  return true;
}

function pillar3TrendChart(canvas, pillar3, sheetSubset, opts){
  // Capital ratios (roughly 0-60%) and liquidity ratios (LCR/NSFR, often
  // 100-1200%) share no readable scale - plotted together the capital lines
  // flatten to near-zero against LCR/NSFR's much larger range, so these are
  // always rendered as two separate charts, never one combined line chart.
  const { showLegend = true, pointRadius = 3 } = opts || {};
  const sheets = sheetSubset.filter(s => Object.keys(pillar3[s]||{}).length);
  if (!sheets.length) return false;
  const years = [...new Set(sheets.flatMap(s => Object.keys(pillar3[s])))].sort();
  new Chart(canvas, {
    type: 'line',
    data: { labels: years, datasets: sheets.map(s => ({
      label: PILLAR3_LABEL[s], data: years.map(y => pillar3[s][y] ?? null),
      borderColor: PILLAR3_STYLE[s].color, backgroundColor: PILLAR3_STYLE[s].color,
      borderDash: PILLAR3_STYLE[s].dash, pointStyle: PILLAR3_STYLE[s].point,
      tension: 0.15, spanGaps: true, pointRadius, borderWidth: 2,
    })) },
    options: {
      responsive:true, maintainAspectRatio:false,
      scales: { y: { ticks: { callback: v => v+'%' }, grid:{color:'#edece7'} }, x: { grid:{display:false} } },
      plugins: {
        legend: { display:showLegend, position:'bottom', labels:{boxWidth:10, font:{size:10}, usePointStyle:true} },
        tooltip: { callbacks: { label: (ctx) => `${ctx.dataset.label}: ${ctx.raw}%` } },
      },
    },
  });
  return true;
}

function percentile(sortedArr, p){
  if (!sortedArr.length) return 0;
  const idx = (sortedArr.length - 1) * p;
  const lo = Math.floor(idx), hi = Math.ceil(idx);
  return lo === hi ? sortedArr[lo] : sortedArr[lo] + (sortedArr[hi] - sortedArr[lo]) * (idx - lo);
}
// Cross-bank distribution, one box per year - shared by the Pillar 3
// boxplot (comparison.html), the balance-sheet composition boxplot
// (balance-sheet.html), and the P&L cost-ratio boxplot (profit-loss.html).
// The `boxplot` type comes from the vendored chartjs-chart-boxplot plugin
// (vendor/chartjs-chart-boxplot/), which self-registers on load same as
// chartjs-chart-sankey does; it computes quartiles/whiskers/outliers
// itself from a plain array of values per year. `years`/`boxes` are
// already reduced by the caller (each page's own data shape differs -
// pillar3 is keyed metric-then-year, capital_deployment/cost_base are
// keyed year-then-metric - so the reduction stays in the caller, not here).
function boxplotByYear(canvas, existingChart, years, boxes, opts){
  opts = opts || {};
  if (existingChart) existingChart.destroy();
  if (!years.length) return null;
  const color = opts.color || '#1e3a5f';
  const unit = opts.unit || '%';
  // A single small bank's freak ratio (e.g. a tiny denominator can put
  // CET1 in the hundreds of %) auto-scales the whole y-axis around it,
  // squashing every other bank's box into a sliver near zero - the same
  // shared-linear-scale problem the bubble charts above already solve
  // with a fixed axis cap. Here the cap is data-driven (95th percentile *
  // 1.6) rather than a hand-picked constant, since one selector can cover
  // several metrics with very different typical ranges (e.g. capital
  // ratios vs LCR/NSFR).
  const allValues = boxes.flat().sort((a, b) => a - b);
  const rawMax = Math.max(percentile(allValues, 0.95) * 1.6, 10);
  // Round up to a "nice" gridline step - a flat 10-unit step reads fine
  // for a 0-150% range but produces an ugly axis top like "2370%" for
  // LCR/NSFR, which can run into the thousands.
  const niceStep = rawMax < 100 ? 10 : rawMax < 1000 ? 50 : rawMax < 5000 ? 100 : 500;
  const yMax = Math.ceil(rawMax / niceStep) * niceStep;
  const clipped = allValues.filter(v => v > yMax).length;
  if (opts.noteEl) {
    opts.noteEl.textContent = clipped
      ? `Chart is capped at ${Math.round(yMax)}${unit} to keep the typical spread readable — ${clipped} bank-year value${clipped === 1 ? '' : 's'} above that are real disclosures, not errors, and sit off-chart.`
      : '';
  }
  return new Chart(canvas, {
    type: 'boxplot',
    data: { labels: years, datasets: [{
      label: opts.label || '',
      data: boxes,
      backgroundColor: color + '2e', borderColor: color, borderWidth: 1.5,
      outlierColor: '#9c3b2e', itemRadius: 2, itemStyle: 'circle', medianColor: color,
    }] },
    options: {
      responsive: true, maintainAspectRatio: false,
      scales: {
        y: { max: yMax, ticks: { callback: v => v + unit }, grid: { color: '#edece7' } },
        x: { grid: { display: false } },
      },
      plugins: { legend: { display: false } },
    },
  });
}

function pillar3BoxplotChart(canvas, existingChart, data, banks, metric, noteEl){
  const years = [...new Set(banks.flatMap(b => Object.keys(data[b].pillar3?.[metric] || {})))].sort();
  const boxes = years.map(y => banks.map(b => data[b].pillar3?.[metric]?.[y]).filter(v => v != null));
  return boxplotByYear(canvas, existingChart, years, boxes, {
    color: (PILLAR3_STYLE[metric] || {}).color, label: PILLAR3_LABEL[metric] || metric, noteEl,
  });
}

// `seriesByBank` is {bank: {year: {metric: value}}} - the shape
// capital_deployment and cost_base already use (unlike pillar3, which is
// metric-then-year), so this covers balance-sheet.html and profit-loss.html
// both without re-deriving anything server-side.
function yearMetricBoxplotChart(canvas, existingChart, seriesByBank, metric, opts){
  // Years come from whichever have data for THIS metric specifically, not
  // the union across every metric in seriesByBank - personnel/other-opex
  // expense-as-%-of-revenue only starts in 2007 while cost-to-income goes
  // back to 1997, so unioned years left the chart half-empty (real boxes
  // 2007 on, blank axis space 1997-2006) whenever the metric switched to
  // one with a shorter history.
  const allYears = [...new Set(Object.values(seriesByBank).flatMap(s => Object.keys(s)))].sort();
  const withData = allYears
    .map(y => [y, Object.values(seriesByBank).map(s => s[y]?.[metric]).filter(v => v != null)])
    .filter(([, vals]) => vals.length);
  return boxplotByYear(canvas, existingChart, withData.map(([y]) => y), withData.map(([, vals]) => vals), opts);
}

// A denser, Yahoo/Google-Finance-style read on the parent's share price
// (user request, 2026-09-09: "more of the graph you would see on Google
// or yahoo finance than a simple once a year thing") - real daily closes
// where fetch_market_data.py has them, falling back to the coarser
// year-end series for stale data files from before history_daily existed.
// Overlays a second, marker-only dataset at each verified full-year
// results announcement date (REPORT_ANNOUNCEMENT_DATES in
// build_deliverable.py) - "highlight the days when these financial
// reports came out" - snapped to the nearest trading day actually present
// in the series (RNS dates are weekdays, but a specific day can still be
// a data gap) within a 5-day window either side.
function parentMarketDataChart(canvas, pmd){
  const daily = Object.entries(pmd.history_daily || {}).sort((a, b) => a[0] < b[0] ? -1 : 1);
  let dates, prices;
  if (daily.length > 1) {
    dates = daily.map(e => e[0]);
    prices = daily.map(e => e[1]);
  } else {
    dates = Object.keys(pmd.history || {}).sort();
    if (dates.length < 2) return false;
    prices = dates.map(y => pmd.history[y]);
  }
  const dateIndex = new Map(dates.map((d, i) => [d, i]));
  const markerData = new Array(dates.length).fill(null);
  const markerLabels = new Array(dates.length).fill(null);
  Object.entries(pmd.report_dates || {}).forEach(([year, dateStr]) => {
    let idx = dateIndex.get(dateStr);
    for (let offset = 1; idx === undefined && offset <= 5; offset++) {
      for (const dir of [1, -1]) {
        const cand = new Date(dateStr);
        cand.setUTCDate(cand.getUTCDate() + dir * offset);
        idx = dateIndex.get(cand.toISOString().slice(0, 10));
        if (idx !== undefined) break;
      }
    }
    if (idx !== undefined) {
      markerData[idx] = prices[idx];
      markerLabels[idx] = `FY${year} results announced — ${dateStr}`;
    }
  });
  const hasMarkers = markerData.some(v => v != null);

  new Chart(canvas, {
    type: 'line',
    data: { labels: dates, datasets: [
      {
        label: 'Share price', data: prices,
        borderColor: '#5c3d8f', backgroundColor: 'rgba(92,61,143,0.08)',
        fill: true, tension: 0.05, pointRadius: 0, borderWidth: 1.5,
      },
      ...(hasMarkers ? [{
        label: 'Results announced', data: markerData,
        showLine: false, pointStyle: 'rectRot', pointRadius: 5, pointHoverRadius: 7,
        borderColor: '#a6741f', backgroundColor: '#a6741f',
      }] : []),
    ] },
    options: {
      responsive: true, maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      scales: {
        y: { ticks: { callback: v => v + 'p' }, grid: { color: '#edece7' } },
        x: { grid: { display: false }, ticks: { autoSkip: true, maxTicksLimit: 8, maxRotation: 0 } },
      },
      plugins: {
        legend: hasMarkers
          ? { display: true, position: 'bottom', labels: { boxWidth: 10, font: { size: 10 }, usePointStyle: true } }
          : { display: false },
        tooltip: { callbacks: { label: (ctx) => ctx.datasetIndex === 1 ? markerLabels[ctx.dataIndex] : `${ctx.raw.toFixed(2)}p` } },
      },
    },
  });
  return true;
}

function leverageChart(canvas, leverage){
  const years = [...new Set([
    ...Object.keys(leverage.equity_to_assets_pct||{}),
    ...Object.keys(leverage.leverage_ratio_reported_pct||{}),
  ])].sort();
  if (!years.length) return false;
  new Chart(canvas, {
    type: 'line',
    data: { labels: years, datasets: [
      {
        label: 'Equity / total assets (accounting)', data: years.map(y => leverage.equity_to_assets_pct[y] ?? null),
        borderColor: '#1e3a5f', backgroundColor: '#1e3a5f', tension: 0.15, spanGaps: true, pointRadius: 3, borderWidth: 2,
      },
      {
        label: 'Leverage ratio (Pillar 3, reported)', data: years.map(y => leverage.leverage_ratio_reported_pct[y] ?? null),
        borderColor: '#a6741f', backgroundColor: '#a6741f', borderDash: [6, 3], pointStyle: 'rect',
        tension: 0.15, spanGaps: true, pointRadius: 3, borderWidth: 2,
      },
    ] },
    options: {
      responsive: true, maintainAspectRatio: false,
      scales: { y: { ticks: { callback: v => v + '%' }, grid: { color: '#edece7' } }, x: { grid: { display: false } } },
      plugins: {
        legend: { display: true, position: 'bottom', labels: { boxWidth: 10, font: { size: 10 }, usePointStyle: true } },
        tooltip: { callbacks: { label: (ctx) => `${ctx.dataset.label}: ${ctx.raw}%` } },
      },
    },
  });
  return true;
}
const ARCHIVE_HISTORY_CUTOFF = 2008;

function historyChartHtml(id, years){
  const hasArchive = years.some(y => Number(y) < ARCHIVE_HISTORY_CUTOFF);
  const control = hasArchive ? `<div class="history-chart-control">
    <button type="button" data-history-toggle>Show full available history</button>
    <span data-history-caption>Showing FY${ARCHIVE_HISTORY_CUTOFF} onwards</span>
  </div>` : '';
  return `<div class="history-chart" id="${id}">${control}
    <div class="history-chart-scroll"><div class="mini-chart-wrap tall"><canvas></canvas></div></div>
  </div>`;
}

function mountHistoryChart(id, years, draw){
  const host = document.getElementById(id);
  if (!host) return;
  const allYears = [...years].sort();
  const recentYears = allYears.filter(y => Number(y) >= ARCHIVE_HISTORY_CUTOFF);
  const toggle = host.querySelector('[data-history-toggle]');
  const caption = host.querySelector('[data-history-caption]');
  const wrap = host.querySelector('.mini-chart-wrap');
  const canvas = host.querySelector('canvas');
  let fullHistory = false;
  let chart = null;
  function redraw(){
    const shownYears = fullHistory ? allYears : recentYears;
    host.classList.toggle('showing-full-history', fullHistory);
    // Preserve legible labels in archival mode instead of squeezing 50+
    // annual observations into a standard dashboard card.
    wrap.style.minWidth = fullHistory ? `${Math.max(720, shownYears.length * 44)}px` : '';
    if (chart) chart.destroy();
    chart = draw(canvas, shownYears);
    if (toggle) toggle.textContent = fullHistory ? `Show FY${ARCHIVE_HISTORY_CUTOFF} onwards` : 'Show full available history';
    if (caption) caption.textContent = fullHistory
      ? `Showing FY${allYears[0]}–FY${allYears[allYears.length - 1]}`
      : `Showing FY${ARCHIVE_HISTORY_CUTOFF} onwards`;
  }
  if (toggle) toggle.addEventListener('click', () => { fullHistory = !fullHistory; redraw(); });
  redraw();
}

function incomeVolatilityChart(canvas, iVol, selectedYears){
  const years = selectedYears || Object.keys(iVol.yoy_change_pct||{}).sort();
  if (!years.length) return false;
  return new Chart(canvas, {
    type: 'bar',
    data: { labels: years, datasets: [{
      label: 'YoY change in profit/(loss) for the year',
      data: years.map(y => iVol.yoy_change_pct[y]),
      backgroundColor: years.map(y => (iVol.yoy_change_pct[y] >= 0 ? '#1f6e52' : '#9c3b2e')),
    }] },
    options: {
      responsive: true, maintainAspectRatio: false,
      scales: { y: { ticks: { callback: v => v + '%' }, grid: { color: '#edece7' } }, x: { grid: { display: false } } },
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: (ctx) => `${ctx.raw >= 0 ? '+' : ''}${ctx.raw}%` } },
      },
    },
  });
}
function efficiencyChart(canvas, efficiency){
  const windows = efficiency.windows||[];
  if (!windows.length || !canvas) return false;
  new Chart(canvas, {
    type: 'line',
    data: { labels: windows, datasets: [
      {
        label: 'Cost-to-income worsening (% of comparable banks)', data: efficiency.cost_to_income_pct_worsening,
        borderColor: '#9c3b2e', backgroundColor: '#9c3b2e', tension: 0.15, spanGaps: true, pointRadius: 3, borderWidth: 2,
      },
      {
        label: 'Profit/(loss) declining (% of comparable banks)', data: efficiency.profit_pct_declining,
        borderColor: '#a6741f', backgroundColor: '#a6741f', borderDash: [6, 3], pointStyle: 'rect',
        tension: 0.15, spanGaps: true, pointRadius: 3, borderWidth: 2,
      },
    ] },
    options: {
      responsive: true, maintainAspectRatio: false,
      scales: { y: { ticks: { callback: v => v + '%' }, grid: { color: '#edece7' } }, x: { grid: { display: false } } },
      plugins: {
        legend: { display: true, position: 'bottom', labels: { boxWidth: 10, font: { size: 10 }, usePointStyle: true } },
        tooltip: { callbacks: { label: (ctx) => `${ctx.dataset.label}: ${ctx.raw}%` } },
      },
    },
  });
  return true;
}
// ---- comparison.html: Gapminder-style bubble charts (user request,
// 2026-09-05) - bubble size = total assets, color = parent group, always.
// A year slider (with play/pause) steps through FY2021-FY2025 snapshots,
// restyling each year's dataset in place rather than rebuilding the
// chart, since the point is watching bubbles move smoothly, not a jump
// cut. `spec` carries what differs per chart: DOM id prefix, axis
// labels/tooltip units, and fixed axis bounds (see call sites for why
// each is capped short of its true max). ----
function initBubbleChart(spec, payload){
  const years = payload.years;
  if (!years.length) return null;
  const canvas = document.getElementById(`${spec.idPrefix}-chart`).querySelector('canvas');
  const allPoints = years.flatMap(y => payload.points_by_year[y]);
  const maxAssets = Math.max(1, ...allPoints.map(p => p.assets || 0));
  const minR = 4, maxR = 26;
  const radiusFor = (assets) => assets == null ? 6 : minR + (maxR - minR) * Math.sqrt(assets / maxAssets);

  const groups = [...new Set(allPoints.map(p => p.group).filter(Boolean))].sort();
  const groupColor = (g) => CATEGORICAL_PALETTE[groups.indexOf(g) % CATEGORICAL_PALETTE.length];

  function bucketize(y){
    const byGroup = {};
    groups.forEach(g => { byGroup[g] = []; });
    const standalone = [];
    (payload.points_by_year[y] || []).forEach(p => {
      const bubble = { x: p.x, y: p.y, r: radiusFor(p.assets), bank: p.bank, assets: p.assets };
      (p.group && byGroup[p.group] ? byGroup[p.group] : standalone).push(bubble);
    });
    return { byGroup, standalone };
  }

  let idx = years.length - 1;
  const initial = bucketize(years[idx]);
  const datasets = [
    ...groups.map(g => ({
      label: g, data: initial.byGroup[g],
      backgroundColor: groupColor(g) + 'b3', borderColor: groupColor(g), borderWidth: 1, clip: false,
    })),
    { label: 'Standalone', data: initial.standalone, backgroundColor: '#c7c2b499', borderColor: '#a39a86', borderWidth: 1, clip: false },
  ];

  const chart = new Chart(canvas, {
    type: 'bubble',
    data: { datasets },
    options: {
      responsive: true, maintainAspectRatio: false,
      // A bubble centered exactly on an axis min (e.g. 0% customer loans)
      // draws half its radius past that edge - without headroom here, that
      // half gets clipped by the chart area boundary. `clip: false` above
      // lets each dataset draw past the chart area, and this padding (sized
      // to the biggest bubble on the chart) keeps the canvas itself large
      // enough that the overflow doesn't then get clipped by the canvas
      // edge instead.
      layout: { padding: maxR },
      scales: {
        // Fixed across every year (not recalculated per frame) so bubble
        // movement between years is real, not an artifact of the axes
        // rescaling - the same reason Gapminder's own chart fixes its axes
        // for the whole animation. Each spec's min/max is capped short of
        // the true max - a handful of banks carry atypically extreme
        // ratios (e.g. Monzo/Chetwood's CET1 swings, or a few small
        // banks' LCR denominators producing 5-6 figure percentages) - see
        // "Flagged as noise, not signal" in Cross-Bank Trends Analysis.md.
        // Those banks simply sit off-chart in the years they're this
        // extreme, rather than compressing everyone else into one corner.
        x: { title: { display: true, text: spec.xLabel }, min: spec.xMin ?? 0, max: spec.xMax, grid: { color: '#edece7' } },
        y: { title: { display: true, text: spec.yLabel }, min: spec.yMin ?? 0, max: spec.yMax, grid: { color: '#edece7' } },
      },
      plugins: {
        legend: { display: true, position: 'bottom', labels: { boxWidth: 10, font: { size: 10 }, usePointStyle: true } },
        tooltip: { callbacks: { label: (ctx) => {
          const p = ctx.raw;
          return `${p.bank}: ${spec.xShort} ${p.x}%, ${spec.yShort} ${p.y}%${p.assets != null ? `, total assets ${fmtK(p.assets)}` : ''}`;
        } } },
      },
    },
  });

  const slider = document.getElementById(`${spec.idPrefix}-year-slider`);
  const label = document.getElementById(`${spec.idPrefix}-year-label`);
  const playBtn = document.getElementById(`${spec.idPrefix}-play`);
  let timer = null;

  function setYear(i){
    idx = i;
    const b = bucketize(years[idx]);
    chart.data.datasets.forEach(ds => { ds.data = ds.label === 'Standalone' ? b.standalone : (b.byGroup[ds.label] || []); });
    chart.update();
    slider.value = idx;
    label.textContent = `FY${years[idx]}`;
  }
  slider.addEventListener('input', () => setYear(Number(slider.value)));

  function stopPlay(){
    if (timer) { clearInterval(timer); timer = null; playBtn.textContent = '▶ Play'; }
  }
  playBtn.addEventListener('click', () => {
    if (timer) { stopPlay(); return; }
    playBtn.textContent = '⏸ Pause';
    timer = setInterval(() => {
      const next = (idx + 1) % years.length;
      setYear(next);
      if (next === years.length - 1) stopPlay();
    }, 900);
  });

  return chart;
}
// Statistical peer-cluster PCA projection (user request, 2026-09-05,
// following wayfinder/insights/prototype/cluster_bubble_prototype.html -
// the user reacted to a 2-variant prototype (raw 2 dimensions vs. a PCA
// projection of all 7) and preferred PCA, since a handful of outlier banks
// on any single ratio otherwise squash everyone else into an unreadable
// clump. build_deliverable.py's curate_comparison_clusters() computes the
// projection itself (numpy, mirroring cluster_banks.py's own median/IQR
// standardize + winsorize method) and ships PC1/PC2 loadings alongside the
// points so this function can build the plain-language explainer
// dynamically from the real numbers, rather than hand-written prose that
// could silently drift out of sync with a future rebuild.
function describeLoadings(dims, loadings){
  const pairs = dims.map((d,i) => ({ d, w: loadings[i] })).sort((a,b) => Math.abs(b.w) - Math.abs(a.w));
  const strong = pairs.filter(p => Math.abs(p.w) >= 0.2);
  const groupA = strong.filter(p => p.w > 0).map(p => p.d);
  const groupB = strong.filter(p => p.w < 0).map(p => p.d);
  return { groupA, groupB, dropped: pairs.filter(p => Math.abs(p.w) < 0.2).map(p => p.d) };
}
function clusterPcaExplainerHtml(clusters){
  const list = (arr) => arr.length === 0 ? '' : arr.length === 1 ? arr[0] : arr.slice(0, -1).join(', ') + ' and ' + arr[arr.length - 1];
  const d1 = describeLoadings(clusters.dims, clusters.pca.pc1_loadings);
  const d2 = describeLoadings(clusters.dims, clusters.pca.pc2_loadings);
  const pc1Groups = [d1.groupA, d1.groupB].filter(g => g.length);
  const pc1Text = pc1Groups.length === 1
    ? `mainly reflects ${list(pc1Groups[0])} moving together: banks with all of these ratios high sit toward one end of the X axis, and banks with them all low sit toward the other, so a bank's X position summarises "strong or weak across this whole group at once," not any single ratio`
    : `splits banks whose ${list(d1.groupA)} run ahead of their ${list(d1.groupB)} from banks where it's the other way round`;
  const pc2Groups = [d2.groupA, d2.groupB].filter(g => g.length);
  const pc2Text = pc2Groups.length === 1
    ? `mainly reflects ${list(pc2Groups[0])} moving together, the same kind of "all high together / all low together" pattern as the X axis, just along a second, independent direction`
    : `separates banks whose ${list(d2.groupA)} run ahead of, or behind, their ${list(d2.groupB)} — so it's about how a bank's liquidity position compares to its capital strength, not how strong either one is on its own`;
  return `
    <strong>What is "PCA" and what does this chart actually show?</strong>
    <p class="sub" style="margin:6px 0 0;">Each bank here has 7 numbers attached to it — its CET1, Tier 1, Total Capital, Leverage, LCR, NSFR and MREL Ratios. That's too many dimensions to draw on a flat chart, so this technique (Principal Component Analysis) finds the two "directions" through that 7-number space that capture the most real variation between banks, and draws every bank as a single dot along those two directions instead.</p>
    <p class="sub" style="margin:6px 0 0;"><strong>X (PC1)</strong> captures ${clusters.pca.var_explained_1.toFixed(0)}% of the variation between banks here, and ${pc1Text}.${d1.dropped.length ? ` ${list(d1.dropped)} ${d1.dropped.length === 1 ? 'barely factors' : 'barely factor'} into it.` : ''}</p>
    <p class="sub" style="margin:6px 0 0;"><strong>Y (PC2)</strong> captures a further ${clusters.pca.var_explained_2.toFixed(0)}%, and ${pc2Text}.</p>
    <p class="sub" style="margin:6px 0 0;">The practical payoff versus picking any two ratios directly: a handful of banks have extreme, atypical values on one or two ratios that would otherwise dominate and squash everyone else into an unreadable clump. PCA's math naturally balances across all 7 at once, so the picture reflects the whole profile rather than whichever one or two ratios happen to have an outlier in them.</p>
  `;
}
function initClusterPcaChart(canvas, clusters){
  if (!clusters || !clusters.banks || !clusters.banks.length) return false;
  const clusterColor = (id) => CATEGORICAL_PALETTE[clusters.cluster_ids.indexOf(id) % CATEGORICAL_PALETTE.length];
  const datasets = clusters.cluster_ids.map(id => {
    const points = clusters.banks.filter(b => b.cluster_id === id);
    const color = clusterColor(id);
    return {
      label: clusters.cluster_labels[id],
      data: points.map(b => ({ x: b.pc1, y: b.pc2, bank: b.bank, n_imputed: b.n_imputed })),
      backgroundColor: points.map(b => b.n_imputed ? color + '55' : color + 'b3'),
      borderColor: color,
      borderWidth: points.map(b => b.n_imputed ? 1 : 0),
      radius: 6, hoverRadius: 8,
    };
  });
  new Chart(canvas, {
    type: 'bubble',
    data: { datasets },
    options: {
      responsive: true, maintainAspectRatio: false,
      scales: {
        x: { title: { display: true, text: `PC1 (${clusters.pca.var_explained_1.toFixed(0)}% of variance)` }, grid: { color: '#edece7' } },
        y: { title: { display: true, text: `PC2 (${clusters.pca.var_explained_2.toFixed(0)}% of variance)` }, grid: { color: '#edece7' } },
      },
      plugins: {
        legend: { display: true, position: 'bottom', labels: { boxWidth: 10, font: { size: 10 }, usePointStyle: true } },
        tooltip: { callbacks: { label: (ctx) => {
          const p = ctx.raw;
          return `${p.bank}${p.n_imputed ? ` (${p.n_imputed} of 7 ratios imputed)` : ''}: PC1 ${p.x.toFixed(2)}, PC2 ${p.y.toFixed(2)}`;
        } } },
      },
    },
  });
  return true;
}
function cashFlowChart(canvas, cashFlow){
  const years = Object.keys(cashFlow).sort();
  if (!years.length) return false;
  new Chart(canvas, {
    type: 'bar',
    data: { labels: years, datasets: CASHFLOW_ORDER.map(k => ({
      label: k, data: years.map(y => cashFlow[y][k] ?? null), backgroundColor: CASHFLOW_COLOR[k],
    })) },
    options: {
      responsive:true, maintainAspectRatio:false,
      scales: { x:{ grid:{display:false} }, y:{ ticks:{callback: v=>fmtK(v)}, grid:{color:'#edece7'} } },
      plugins: {
        legend: { display:true, position:'bottom', labels:{boxWidth:10, font:{size:10}} },
        tooltip: { callbacks: { label: (ctx) => ctx.raw != null ? `${ctx.dataset.label}: ${fmtK(ctx.raw)}` : `${ctx.dataset.label}: n/d` } } },
    },
  });
  return true;
}

// ---- business-model.html ----
const BUSINESS_MODEL_TAG_COLOR = { digital: "#2b5f63", traditional: "#1e3a5f", other: "#a6741f" };
const BUSINESS_MODEL_TAG_LABEL = { digital: "Digital / challenger", traditional: "Traditional", other: "Fee / markets-driven" };
// total_assets spans many orders of magnitude (a few million to over a
// trillion £ across 145 banks of wildly different scale) - a linear axis
// crushes every bank except the largest handful into an unreadable clump
// against the origin, so it gets a logarithmic scale; the three % ratios
// are already naturally bounded to a comparable range and stay linear.
const BUSINESS_MODEL_Y_AXIS_OPTIONS = [
  { key: "total_assets", label: "Total assets", fmt: (v) => fmtK(v), scaleType: "logarithmic" },
  { key: "cost_to_income_pct", label: "Cost-to-income (%)", fmt: (v) => v + "%", scaleType: "linear" },
  { key: "leverage_ratio_pct", label: "Leverage ratio (%)", fmt: (v) => v + "%", scaleType: "linear" },
  { key: "rwa_to_assets_pct", label: "RWA / Total assets (%)", fmt: (v) => v + "%", scaleType: "linear" },
];

function renderBusinessModelPage(records){
  const sorted = [...records].sort((a, b) => b.fee_share_pct - a.fee_share_pct);
  const legend = Object.entries(BUSINESS_MODEL_TAG_LABEL)
    .map(([tag, label]) => `<span><span class="sw" style="background:${BUSINESS_MODEL_TAG_COLOR[tag]}"></span>${label}</span>`).join('');

  document.getElementById('app').innerHTML = `
    ${blockOpen('Fee income share of total income', `${sorted.length} banks · fee / (fee + net interest), latest year each discloses both`)}
    <div class="card">
      <div class="view-toggle" id="bm-view-toggle">
        <button type="button" data-view="bar" class="active">Ranked bar</button>
        <button type="button" data-view="scatter">Scatter</button>
      </div>
      <div id="bm-bar-view">
        <div class="mini-chart-wrap" id="bm-bar-chart" style="height:${Math.max(320, sorted.length * 20)}px"><canvas></canvas></div>
      </div>
      <div id="bm-scatter-view" hidden>
        <div class="chart-controls">
          <label for="bm-y-axis">Y-axis</label>
          <select id="bm-y-axis">${BUSINESS_MODEL_Y_AXIS_OPTIONS.map(o => `<option value="${o.key}">${o.label}</option>`).join('')}</select>
        </div>
        <div class="mini-chart-wrap tall" id="bm-scatter-chart" style="height:420px"><canvas></canvas></div>
      </div>
      <div class="legend-row">${legend}</div>
    </div>
    ${blockClose()}
  `;

  let barChart = null, scatterChart = null;

  function drawBar(){
    const canvas = document.querySelector('#bm-bar-chart canvas');
    barChart = new Chart(canvas, {
      type: 'bar',
      data: { labels: sorted.map(r => r.bank), datasets: [{
        data: sorted.map(r => r.fee_share_pct),
        backgroundColor: sorted.map(r => BUSINESS_MODEL_TAG_COLOR[r.bank_type]),
      }] },
      options: {
        indexAxis: 'y', responsive: true, maintainAspectRatio: false,
        scales: {
          x: { min: 0, max: 100, title: { display: true, text: 'Fee income share of total income (%)' }, ticks: { callback: (v) => v + '%' }, grid: { color: '#edece7' } },
          y: { grid: { display: false }, ticks: { font: { size: 9 } } },
        },
        plugins: {
          legend: { display: false },
          tooltip: { callbacks: { label: (ctx) => {
            const r = sorted[ctx.dataIndex];
            return `${r.fee_share_pct}% fee share (FY${r.fee_share_year}) — ${BUSINESS_MODEL_TAG_LABEL[r.bank_type]}`;
          } } },
        },
      },
    });
  }

  function drawScatter(yKey){
    const opt = BUSINESS_MODEL_Y_AXIS_OPTIONS.find(o => o.key === yKey);
    // A log scale can't plot zero/negative - only relevant for total_assets,
    // and every bank with a real Total assets row reports a positive value,
    // so this drops no genuine data point.
    const points = sorted.filter(r => r[yKey] != null && (opt.scaleType !== 'logarithmic' || r[yKey] > 0));
    if (scatterChart) scatterChart.destroy();
    const canvas = document.querySelector('#bm-scatter-chart canvas');
    scatterChart = new Chart(canvas, {
      type: 'scatter',
      data: { datasets: Object.keys(BUSINESS_MODEL_TAG_LABEL).map((tag) => ({
        label: BUSINESS_MODEL_TAG_LABEL[tag],
        data: points.filter(r => r.bank_type === tag).map(r => ({ x: r.fee_share_pct, y: r[yKey], bank: r.bank })),
        backgroundColor: BUSINESS_MODEL_TAG_COLOR[tag] + 'cc', borderColor: BUSINESS_MODEL_TAG_COLOR[tag],
        pointRadius: 5, pointHoverRadius: 7,
      })) },
      options: {
        responsive: true, maintainAspectRatio: false,
        scales: {
          x: { min: 0, max: 100, title: { display: true, text: 'Fee income share of total income (%)' }, ticks: { callback: (v) => v + '%' }, grid: { color: '#edece7' } },
          y: { type: opt.scaleType, title: { display: true, text: opt.label }, grid: { color: '#edece7' } },
        },
        plugins: {
          // The persistent .legend-row below the chart already carries the
          // tag colors (and matches the bar view's legend, which has no
          // per-dataset Chart.js legend of its own) - a second, duplicate
          // legend here just repeats it.
          legend: { display: false },
          tooltip: { callbacks: { label: (ctx) => `${ctx.raw.bank}: ${ctx.raw.x}% fee share, ${opt.fmt(ctx.raw.y)}` } },
        },
      },
    });
  }

  drawBar();
  const toggle = document.getElementById('bm-view-toggle');
  toggle.addEventListener('click', (e) => {
    const btn = e.target.closest('button[data-view]');
    if (!btn) return;
    toggle.querySelectorAll('button').forEach(b => b.classList.toggle('active', b === btn));
    const isBar = btn.dataset.view === 'bar';
    document.getElementById('bm-bar-view').hidden = !isBar;
    document.getElementById('bm-scatter-view').hidden = isBar;
    if (!isBar && !scatterChart) drawScatter(document.getElementById('bm-y-axis').value);
  });
  document.getElementById('bm-y-axis').addEventListener('change', (e) => drawScatter(e.target.value));
  initCollapsibleBlocks();
}

// ---- investments.html ----
const INVESTMENT_BASIS_COLOR = { amortised_cost: "#1e3a5f", mark_to_market: "#a6741f" };
const INVESTMENT_BASIS_LABEL = { amortised_cost: "Amortised cost (hold to collect)", mark_to_market: "Mark to market (FVOCI / FVTPL / trading)" };
const INVESTMENT_GOVT_COLOR = { government: "#1f6e52", other: "#5c6b73" };
const INVESTMENT_GOVT_LABEL = { government: "Government / sovereign", other: "Other investment securities" };
// Each view's scatter plots its own primary leg (% mark-to-market, %
// government) on X against the SAME reusable y-axis candidates
// business-model.html's scatter already offers - both pages share the same
// per-bank size/efficiency fields (curate()'s _scatter_y_axis_fields), so
// there's no reason to invent a second set of y-axis options.
const INVESTMENT_SCATTER_X = {
  "inv-basis": { field: "measurement_basis", key: "mark_to_market", label: "Mark-to-market share of investment book (%)", color: INVESTMENT_BASIS_COLOR.mark_to_market },
  "inv-govt": { field: "government_vs_other", key: "government", label: "Government/sovereign share of investment securities (%)", color: INVESTMENT_GOVT_COLOR.government },
};

function renderInvestmentsPage(records){
  document.getElementById('app').innerHTML = `
    ${investmentBlockHtml('inv-basis', 'Measurement basis', INVESTMENT_BASIS_LABEL,
      records.filter(r => r.measurement_basis).length,
      'banks with an amortised-cost / mark-to-market split disclosed, latest year each discloses it')}
    ${investmentBlockHtml('inv-govt', 'Government vs other investment securities', INVESTMENT_GOVT_LABEL,
      records.filter(r => r.government_vs_other).length,
      'banks that disclose a government/sovereign line separately from other investment securities, latest year')}
  `;
  drawInvestmentStackedBar('inv-basis', records, 'measurement_basis', INVESTMENT_BASIS_LABEL, INVESTMENT_BASIS_COLOR, 'amortised_cost');
  drawInvestmentStackedBar('inv-govt', records, 'government_vs_other', INVESTMENT_GOVT_LABEL, INVESTMENT_GOVT_COLOR, 'government');
  initInvestmentViewToggle('inv-basis', records);
  initInvestmentViewToggle('inv-govt', records);
  initCollapsibleBlocks();
}

function investmentBlockHtml(id, title, labelMap, count, hint){
  const colorMap = id === 'inv-basis' ? INVESTMENT_BASIS_COLOR : INVESTMENT_GOVT_COLOR;
  const legend = Object.entries(labelMap)
    .map(([key, label]) => `<span><span class="sw" style="background:${colorMap[key]}"></span>${label}</span>`).join('');
  const tagLegend = Object.entries(BUSINESS_MODEL_TAG_LABEL)
    .map(([tag, label]) => `<span><span class="sw" style="background:${BUSINESS_MODEL_TAG_COLOR[tag]}"></span>${label}</span>`).join('');
  return `
    ${blockOpen(title, `${count} banks · ${hint}`)}
    <div class="card">
      <div class="view-toggle" id="${id}-view-toggle">
        <button type="button" data-view="bar" class="active">Stacked bar</button>
        <button type="button" data-view="scatter">Scatter</button>
      </div>
      <div id="${id}-bar-view">
        <div class="mini-chart-wrap" id="${id}-chart" style="height:${Math.max(320, count * 20)}px"><canvas></canvas></div>
        <div class="legend-row" style="margin-top:2px;"><span class="hint" style="margin-right:6px;">Bank name colored by:</span>${tagLegend}</div>
      </div>
      <div id="${id}-scatter-view" hidden>
        <div class="chart-controls">
          <label for="${id}-y-axis">Y-axis</label>
          <select id="${id}-y-axis">${BUSINESS_MODEL_Y_AXIS_OPTIONS.map(o => `<option value="${o.key}">${o.label}</option>`).join('')}</select>
        </div>
        <div class="mini-chart-wrap tall" id="${id}-scatter-chart" style="height:420px"><canvas></canvas></div>
        <div class="legend-row" style="margin-top:2px;">${tagLegend}</div>
      </div>
      <div class="legend-row">${legend}</div>
    </div>
    ${blockClose()}
  `;
}

function drawInvestmentStackedBar(id, records, field, labelMap, colorMap, sortKey){
  const rows = records.filter(r => r[field]).sort((a, b) => b[field][sortKey] - a[field][sortKey]);
  const keys = Object.keys(labelMap);
  const canvas = document.querySelector(`#${id}-chart canvas`);
  if (!canvas || !rows.length) return;
  new Chart(canvas, {
    type: 'bar',
    data: {
      labels: rows.map(r => r.bank),
      datasets: keys.map(key => ({
        label: labelMap[key],
        data: rows.map(r => r[field][key]),
        backgroundColor: colorMap[key],
      })),
    },
    options: {
      indexAxis: 'y', responsive: true, maintainAspectRatio: false,
      scales: {
        x: { stacked: true, min: 0, max: 100, ticks: { callback: (v) => v + '%' }, grid: { color: '#edece7' } },
        y: {
          stacked: true, grid: { display: false },
          ticks: { font: { size: 9 }, color: (ctx) => BUSINESS_MODEL_TAG_COLOR[rows[ctx.index].bank_type] || '#3a3a38' },
        },
      },
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: {
          label: (ctx) => {
            const r = rows[ctx.dataIndex];
            return `${ctx.dataset.label}: ${ctx.raw}% (FY${r[field].year})`;
          },
          footer: (items) => BUSINESS_MODEL_TAG_LABEL[rows[items[0].dataIndex].bank_type],
        } },
      },
    },
  });
}

const _investmentScatterCharts = {};

function drawInvestmentScatter(id, records, yKey){
  const xConf = INVESTMENT_SCATTER_X[id];
  const opt = BUSINESS_MODEL_Y_AXIS_OPTIONS.find(o => o.key === yKey);
  const rows = records.filter(r => r[xConf.field] && r[yKey] != null && (opt.scaleType !== 'logarithmic' || r[yKey] > 0));
  if (_investmentScatterCharts[id]) _investmentScatterCharts[id].destroy();
  const canvas = document.querySelector(`#${id}-scatter-chart canvas`);
  _investmentScatterCharts[id] = new Chart(canvas, {
    type: 'scatter',
    data: { datasets: Object.keys(BUSINESS_MODEL_TAG_LABEL).map((tag) => ({
      label: BUSINESS_MODEL_TAG_LABEL[tag],
      data: rows.filter(r => r.bank_type === tag)
        .map(r => ({ x: r[xConf.field][xConf.key], y: r[yKey], bank: r.bank, year: r[xConf.field].year })),
      backgroundColor: BUSINESS_MODEL_TAG_COLOR[tag] + 'cc', borderColor: BUSINESS_MODEL_TAG_COLOR[tag],
      pointRadius: 5, pointHoverRadius: 7,
    })) },
    options: {
      responsive: true, maintainAspectRatio: false,
      scales: {
        x: { min: 0, max: 100, title: { display: true, text: xConf.label }, ticks: { callback: (v) => v + '%' }, grid: { color: '#edece7' } },
        y: { type: opt.scaleType, title: { display: true, text: opt.label }, grid: { color: '#edece7' } },
      },
      plugins: {
        // Points are colored by bank_type here (unlike the stacked bar,
        // which is already using its 2 colors for the composition legs) -
        // the persistent tag legend below the chart carries this, so the
        // built-in per-dataset legend would just duplicate it.
        legend: { display: false },
        tooltip: { callbacks: { label: (ctx) => `${ctx.raw.bank}: ${ctx.raw.x}% (FY${ctx.raw.year}), ${opt.fmt(ctx.raw.y)}` } },
      },
    },
  });
}

function initInvestmentViewToggle(id, records){
  const toggle = document.getElementById(`${id}-view-toggle`);
  toggle.addEventListener('click', (e) => {
    const btn = e.target.closest('button[data-view]');
    if (!btn) return;
    toggle.querySelectorAll('button').forEach(b => b.classList.toggle('active', b === btn));
    const isBar = btn.dataset.view === 'bar';
    document.getElementById(`${id}-bar-view`).hidden = !isBar;
    document.getElementById(`${id}-scatter-view`).hidden = isBar;
    if (!isBar && !_investmentScatterCharts[id]) drawInvestmentScatter(id, records, document.getElementById(`${id}-y-axis`).value);
  });
  document.getElementById(`${id}-y-axis`).addEventListener('change', (e) => drawInvestmentScatter(id, records, e.target.value));
}

// ---- balance-sheet.html ----
const ASSET_COMPOSITION_COLOR = {
  loans_pct_of_assets: "#1f6e52", treasury_investments_pct_of_assets: "#45566b",
  cash_pct_of_assets: "#a6741f", other: "#a39a86",
};
const ASSET_COMPOSITION_LABEL = {
  loans_pct_of_assets: "Customer loans", treasury_investments_pct_of_assets: "Treasury investments",
  cash_pct_of_assets: "Cash & central bank balances", other: "Other assets",
};
const ASSET_COMPOSITION_ORDER = ["loans_pct_of_assets", "treasury_investments_pct_of_assets", "cash_pct_of_assets", "other"];

// Same color roles as ASSET_COMPOSITION_COLOR/LIABILITY_COLOR (primary
// line = green, secondary = slate, tertiary = amber, residual = tan) -
// kept consistent across all three balance-sheet-side charts so a color
// means the same *kind* of thing (biggest named line vs residual)
// everywhere on this page, even though the actual categories differ.
const EQUITY_COMPOSITION_COLOR = { share_capital_pct: "#45566b", retained_earnings_pct: "#1f6e52", other_pct: "#a39a86" };
const EQUITY_COMPOSITION_LABEL = { share_capital_pct: "Share capital & premium", retained_earnings_pct: "Retained earnings", other_pct: "Other reserves" };
const EQUITY_COMPOSITION_ORDER = ["share_capital_pct", "retained_earnings_pct", "other_pct"];

// Peer-size filter (2026-09-08 follow-up: "compare banks with a similar
// amount of assets on what those specific assets are") - the tier labels
// must match _size_tier()'s output in build_deliverable.py exactly, since
// they're compared as plain strings against each record's size_tier.
const BALANCE_SHEET_SIZE_TIERS = [
  "Under £250m", "£250m – £1bn", "£1bn – £2bn", "£2bn – £5bn", "£5bn – £10bn", "£10bn – £100bn", "£100bn+",
];

function renderBalanceSheetPage(records, deployment){
  // The size chart always shows every bank (that's the point of it - see
  // the whole distribution at once); the three composition charts below
  // are filtered by the peer-group select, defaulting to "All banks".
  // All three composition charts share one bank order (largest Total
  // assets first, within whatever the current filter includes) so a
  // reader can scan down all three at once - unlike business-model.html/
  // investments.html, which each sort by their own single leg.
  const sorted = [...records].sort((a, b) => b.total_assets - a.total_assets);
  const tagLegend = Object.entries(BUSINESS_MODEL_TAG_LABEL)
    .map(([tag, label]) => `<span><span class="sw" style="background:${BUSINESS_MODEL_TAG_COLOR[tag]}"></span>${label}</span>`).join('');
  const tierOptions = ['<option value="">All banks</option>']
    .concat(BALANCE_SHEET_SIZE_TIERS.map(t => `<option value="${t}">${t} (${records.filter(r => r.size_tier === t).length} banks)</option>`))
    .join('');

  // Box-and-whisker distribution of one asset-composition metric across
  // every bank, by year (user request, 2026-09-09) - the same "median,
  // quartiles, outliers per year" lens the Pillar 3 boxplot already gives
  // comparison.html, applied to the balance-sheet side instead of Pillar 3
  // ratios. `deployment` is {bank: {year: {metric: value}}}, already
  // curated server-side from the same capital_deployment series the
  // per-bank drilldown page's own "Capital deployment" chart uses.
  const bsBoxplotMetrics = ["cash_pct_of_assets", "loans_pct_of_assets", "treasury_investments_pct_of_assets"];

  document.getElementById('app').innerHTML = `
    ${blockOpen('Total assets', `${sorted.length} banks · latest year disclosed, log scale (spans a few million to over £1tn)`)}
    <div class="card">
      <div class="mini-chart-wrap" id="bs-size-chart" style="height:${Math.max(320, sorted.length * 20)}px"><canvas></canvas></div>
      <div class="legend-row" style="margin-top:2px;"><span class="hint" style="margin-right:6px;">Bank name colored by:</span>${tagLegend}</div>
    </div>
    ${blockClose()}
    ${blockOpen('Balance sheet composition', 'What each side of the balance sheet is made of, latest year each discloses it')}
    <div class="card">
      <div class="chart-controls">
        <label for="bs-tier-filter">Compare banks with a similar amount of assets</label>
        <select id="bs-tier-filter">${tierOptions}</select>
      </div>
      ${compositionSubsectionHtml('bs-assets', 'Assets', ASSET_COMPOSITION_LABEL, ASSET_COMPOSITION_COLOR, true)}
      ${compositionSubsectionHtml('bs-liabilities', 'Liabilities', LIABILITY_LABEL, LIABILITY_COLOR, true)}
      ${compositionSubsectionHtml('bs-equity', 'Equity', EQUITY_COMPOSITION_LABEL, EQUITY_COMPOSITION_COLOR, false)}
    </div>
    ${blockClose()}
    ${blockOpen('Distribution across banks', 'spread of one asset-mix ratio across all banks, by year')}
    <div class="card chart-card">
      <div class="chart-controls">
        <label for="bs-boxplot-metric">Metric</label>
        <select id="bs-boxplot-metric">${bsBoxplotMetrics.map(m => `<option value="${m}">${ASSET_COMPOSITION_LABEL[m]}</option>`).join('')}</select>
      </div>
      <div class="mini-chart-wrap tall" id="bs-boxplot-chart" style="height:340px;"><canvas></canvas></div>
      <p class="sub" id="bs-boxplot-note" style="margin:8px 0 0;"></p>
    </div>
    ${blockClose()}
  `;

  new Chart(document.querySelector('#bs-size-chart canvas'), {
    type: 'bar',
    data: { labels: sorted.map(r => r.bank), datasets: [{
      data: sorted.map(r => r.total_assets),
      backgroundColor: sorted.map(r => BUSINESS_MODEL_TAG_COLOR[r.bank_type]),
    }] },
    options: {
      indexAxis: 'y', responsive: true, maintainAspectRatio: false,
      scales: {
        x: { type: 'logarithmic', title: { display: true, text: 'Total assets' }, ticks: { callback: (v) => fmtBn(v) }, grid: { color: '#edece7' } },
        y: { grid: { display: false }, ticks: { font: { size: 9 } } },
      },
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: (ctx) => {
          const r = sorted[ctx.dataIndex];
          return `${fmtK(r.total_assets)} (FY${r.year}) — ${BUSINESS_MODEL_TAG_LABEL[r.bank_type]}`;
        } } },
      },
    },
  });

  const compCharts = {};
  function drawAll(tier){
    const rows = tier ? sorted.filter(r => r.size_tier === tier) : sorted;
    compCharts.assets = drawBalanceSheetCompositionBar(
      'bs-assets', compCharts.assets, rows, 'assets', ASSET_COMPOSITION_ORDER, ASSET_COMPOSITION_LABEL, ASSET_COMPOSITION_COLOR, true);
    compCharts.liabilities = drawBalanceSheetCompositionBar(
      'bs-liabilities', compCharts.liabilities, rows.filter(r => r.liabilities), 'liabilities', LIABILITY_ORDER, LIABILITY_LABEL, LIABILITY_COLOR, true);
    compCharts.equity = drawBalanceSheetCompositionBar(
      'bs-equity', compCharts.equity, rows.filter(r => r.equity), 'equity', EQUITY_COMPOSITION_ORDER, EQUITY_COMPOSITION_LABEL, EQUITY_COMPOSITION_COLOR, false);
  }
  drawAll('');
  document.getElementById('bs-tier-filter').addEventListener('change', (e) => drawAll(e.target.value));

  const bsBoxplotCanvas = document.querySelector('#bs-boxplot-chart canvas');
  const bsBoxplotNote = document.getElementById('bs-boxplot-note');
  let bsBoxplotChart = null;
  const drawBsBoxplot = (metric) => {
    bsBoxplotChart = yearMetricBoxplotChart(bsBoxplotCanvas, bsBoxplotChart, deployment, metric, {
      color: ASSET_COMPOSITION_COLOR[metric], label: ASSET_COMPOSITION_LABEL[metric], noteEl: bsBoxplotNote,
    });
  };
  drawBsBoxplot(bsBoxplotMetrics[0]);
  document.getElementById('bs-boxplot-metric').addEventListener('change', (e) => drawBsBoxplot(e.target.value));

  initCollapsibleBlocks();
}

function compositionSubsectionHtml(id, title, labelMap, colorMap, startOpen){
  const legend = Object.entries(labelMap)
    .map(([key, label]) => `<span><span class="sw" style="background:${colorMap[key]}"></span>${label}</span>`).join('');
  return `
    ${subOpen(title, '% of the total, by bank', !startOpen)}
    <div class="mini-chart-wrap" id="${id}-chart" style="height:340px"><canvas></canvas></div>
    <div class="legend-row" style="margin-top:2px;">${legend}</div>
    ${subClose()}
  `;
}

// Shared by all three balance-sheet-side composition charts. `fixedScale`
// is true for assets/liabilities (every leg is a non-negative % of a
// positive total, by construction - see curate_asset_composition_absolute/
// curate_liability_composition, both clamp their residual at 0), so a
// fixed 0-100% x-axis is always safe there. It's false for equity: retained
// earnings is genuinely negative for a bank still working through
// accumulated losses (real example: Monzo's FY2025 retained_earnings_pct
// is -25%, offset by a correspondingly larger "other reserves" share, not
// a bug), so equity's x-axis is left to auto-scale rather than clipped at a
// fixed 0-100 - a fixed range would silently clip that segment off-chart.
function drawBalanceSheetCompositionBar(id, existing, rows, field, order, labelMap, colorMap, fixedScale){
  if (existing) existing.destroy();
  const canvas = document.querySelector(`#${id}-chart canvas`);
  if (!canvas || !rows.length) return null;
  return new Chart(canvas, {
    type: 'bar',
    data: {
      labels: rows.map(r => r.bank),
      datasets: order.map(key => ({
        label: labelMap[key],
        data: rows.map(r => r[field][key]),
        backgroundColor: colorMap[key],
      })),
    },
    options: {
      indexAxis: 'y', responsive: true, maintainAspectRatio: false,
      scales: {
        x: {
          stacked: true, ...(fixedScale ? { min: 0, max: 100 } : {}),
          ticks: { callback: (v) => v + '%' }, grid: { color: '#edece7' },
        },
        y: {
          stacked: true, grid: { display: false },
          ticks: { font: { size: 9 }, color: (ctx) => BUSINESS_MODEL_TAG_COLOR[rows[ctx.index].bank_type] || '#3a3a38' },
        },
      },
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: {
          label: (ctx) => {
            const r = rows[ctx.dataIndex];
            return `${ctx.dataset.label}: ${ctx.raw}% (FY${r[field].year})`;
          },
          footer: (items) => BUSINESS_MODEL_TAG_LABEL[rows[items[0].dataIndex].bank_type],
        } },
      },
    },
  });
}

// ---- profit-loss.html ----
const INCOME_COMPOSITION_COLOR = {
  net_interest_pct: "#1f6e52", net_fee_pct: "#45566b", trading_investment_pct: "#a6741f", other_pct: "#a39a86",
};
const INCOME_COMPOSITION_LABEL = {
  net_interest_pct: "Net interest income", net_fee_pct: "Net fee & commission income",
  trading_investment_pct: "Trading & investment income", other_pct: "Other income",
};
const INCOME_COMPOSITION_ORDER = ["net_interest_pct", "net_fee_pct", "trading_investment_pct", "other_pct"];
const EXPENSE_COMPOSITION_COLOR = { personnel_pct: "#45566b", other_operating_pct: "#1f6e52", other_pct: "#a39a86" };
const EXPENSE_COMPOSITION_LABEL = { personnel_pct: "Personnel expense", other_operating_pct: "Other operating expense", other_pct: "Other" };
const EXPENSE_COMPOSITION_ORDER = ["personnel_pct", "other_operating_pct", "other_pct"];
// Must match _pnl_size_tier()'s output in build_deliverable.py exactly -
// same "compare banks with a similar amount of [X]" filter mechanic as
// balance-sheet.html's BALANCE_SHEET_SIZE_TIERS, keyed to income scale
// instead of asset scale (income runs roughly 2 orders of magnitude
// smaller than assets for a typical bank, so the bands are separate, not
// reused).
const PNL_SIZE_TIERS = [
  "Under £10m", "£10m – £25m", "£25m – £50m", "£50m – £100m",
  "£100m – £250m", "£250m – £500m", "£500m – £1bn", "£1bn+",
];

const PNL_BOXPLOT_LABEL = {
  cost_to_income_pct: "Cost-to-income ratio",
  personnel_expense_pct_of_revenue: "Personnel expense (% of revenue)",
  other_operating_expense_pct_of_revenue: "Other operating expense (% of revenue)",
};
const PNL_BOXPLOT_COLOR = { cost_to_income_pct: "#9c3b2e", personnel_expense_pct_of_revenue: "#45566b", other_operating_expense_pct_of_revenue: "#1f6e52" };

function renderPnlPage(records, deployment){
  const sorted = [...records].sort((a, b) => b.total_income - a.total_income);
  const tagLegend = Object.entries(BUSINESS_MODEL_TAG_LABEL)
    .map(([tag, label]) => `<span><span class="sw" style="background:${BUSINESS_MODEL_TAG_COLOR[tag]}"></span>${label}</span>`).join('');
  const tierOptions = ['<option value="">All banks</option>']
    .concat(PNL_SIZE_TIERS.map(t => `<option value="${t}">${t} (${records.filter(r => r.size_tier === t).length} banks)</option>`))
    .join('');
  // Same cross-bank distribution lens as balance-sheet.html's boxplot,
  // applied to P&L cost ratios (server-side trimmed to PNL_BOXPLOT_METRICS
  // in curate_pnl_deployment - the absolute-£ cost_base entries aren't
  // comparable bank to bank on one axis).
  const pnlBoxplotMetrics = Object.keys(PNL_BOXPLOT_LABEL)
    .filter(m => Object.values(deployment).some(byYear => Object.values(byYear).some(vals => vals[m] != null)));

  document.getElementById('app').innerHTML = `
    ${blockOpen('Total operating income', `${sorted.length} banks · latest year disclosed, log scale`)}
    <div class="card">
      <div class="mini-chart-wrap" id="pnl-size-chart" style="height:${Math.max(320, sorted.length * 20)}px"><canvas></canvas></div>
      <div class="legend-row" style="margin-top:2px;"><span class="hint" style="margin-right:6px;">Bank name colored by:</span>${tagLegend}</div>
    </div>
    ${blockClose()}
    ${blockOpen('Profit & loss composition', 'What makes up income and expenses, latest year each discloses it')}
    <div class="card">
      <div class="chart-controls">
        <label for="pnl-tier-filter">Compare banks with a similar amount of income</label>
        <select id="pnl-tier-filter">${tierOptions}</select>
      </div>
      ${compositionSubsectionHtml('pnl-income', 'Income', INCOME_COMPOSITION_LABEL, INCOME_COMPOSITION_COLOR, true)}
      ${compositionSubsectionHtml('pnl-expenses', 'Expenses', EXPENSE_COMPOSITION_LABEL, EXPENSE_COMPOSITION_COLOR, true)}
    </div>
    ${blockClose()}
    ${pnlBoxplotMetrics.length ? `${blockOpen('Distribution across banks', 'spread of one cost ratio across all banks, by year')}
    <div class="card chart-card">
      <div class="chart-controls">
        <label for="pnl-boxplot-metric">Metric</label>
        <select id="pnl-boxplot-metric">${pnlBoxplotMetrics.map(m => `<option value="${m}">${PNL_BOXPLOT_LABEL[m]}</option>`).join('')}</select>
      </div>
      <div class="mini-chart-wrap tall" id="pnl-boxplot-chart" style="height:340px;"><canvas></canvas></div>
      <p class="sub" id="pnl-boxplot-note" style="margin:8px 0 0;"></p>
    </div>
    ${blockClose()}` : ''}
  `;

  new Chart(document.querySelector('#pnl-size-chart canvas'), {
    type: 'bar',
    data: { labels: sorted.map(r => r.bank), datasets: [{
      data: sorted.map(r => r.total_income),
      backgroundColor: sorted.map(r => BUSINESS_MODEL_TAG_COLOR[r.bank_type]),
    }] },
    options: {
      indexAxis: 'y', responsive: true, maintainAspectRatio: false,
      scales: {
        x: { type: 'logarithmic', title: { display: true, text: 'Total operating income' }, ticks: { callback: (v) => fmtBn(v) }, grid: { color: '#edece7' } },
        y: { grid: { display: false }, ticks: { font: { size: 9 } } },
      },
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: (ctx) => {
          const r = sorted[ctx.dataIndex];
          return `${fmtK(r.total_income)} (FY${r.year}) — ${BUSINESS_MODEL_TAG_LABEL[r.bank_type]}`;
        } } },
      },
    },
  });

  const compCharts = {};
  function drawAll(tier){
    const rows = tier ? sorted.filter(r => r.size_tier === tier) : sorted;
    // Neither chart gets a fixed 0-100% x-axis, unlike assets/liabilities
    // on balance-sheet.html - income and expense categories here are NOT
    // clamped at 0 in curate_pnl_composition (a negative net fee line, or
    // unclassified expenses exceeding total opex, are real disclosed
    // outcomes, not bugs), so a fixed range could silently clip a segment
    // off-chart. Same reasoning as equity's chart there.
    compCharts.income = drawBalanceSheetCompositionBar(
      'pnl-income', compCharts.income, rows.filter(r => r.income), 'income', INCOME_COMPOSITION_ORDER, INCOME_COMPOSITION_LABEL, INCOME_COMPOSITION_COLOR, false);
    compCharts.expenses = drawBalanceSheetCompositionBar(
      'pnl-expenses', compCharts.expenses, rows.filter(r => r.expenses), 'expenses', EXPENSE_COMPOSITION_ORDER, EXPENSE_COMPOSITION_LABEL, EXPENSE_COMPOSITION_COLOR, false);
  }
  drawAll('');
  document.getElementById('pnl-tier-filter').addEventListener('change', (e) => drawAll(e.target.value));

  if (pnlBoxplotMetrics.length) {
    const pnlBoxplotCanvas = document.querySelector('#pnl-boxplot-chart canvas');
    const pnlBoxplotNote = document.getElementById('pnl-boxplot-note');
    let pnlBoxplotChart = null;
    const drawPnlBoxplot = (metric) => {
      pnlBoxplotChart = yearMetricBoxplotChart(pnlBoxplotCanvas, pnlBoxplotChart, deployment, metric, {
        color: PNL_BOXPLOT_COLOR[metric], label: PNL_BOXPLOT_LABEL[metric], noteEl: pnlBoxplotNote,
      });
    };
    drawPnlBoxplot(pnlBoxplotMetrics[0]);
    document.getElementById('pnl-boxplot-metric').addEventListener('change', (e) => drawPnlBoxplot(e.target.value));
  }

  initCollapsibleBlocks();
}

// ---- sidebar: nav + compact search only (the full bank list lives on
// banks.html now, not in the sidebar, so it stays a fixed size regardless
// of how many banks the real build eventually covers) ----
function renderSidebar(activeNav, banksIndex){
  assignBankColors(banksIndex);
  document.getElementById('sidebar-nav').innerHTML = `
    <a href="comparison.html" class="${activeNav==='comparison'?'active':''}">Comparison</a>
    <a href="banks.html" class="${activeNav==='banks'?'active':''}">Banks</a>
    <a href="business-model.html" class="${activeNav==='business-model'?'active':''}">Business model</a>
    <a href="investments.html" class="${activeNav==='investments'?'active':''}">Investments</a>
    <a href="balance-sheet.html" class="${activeNav==='balance-sheet'?'active':''}">Balance sheet</a>
    <a href="profit-loss.html" class="${activeNav==='profit-loss'?'active':''}">Profit &amp; loss</a>
  `;
  const wrap = document.getElementById('bank-search-wrap');
  wrap.innerHTML = `
    <div class="nav-label">Jump to a bank</div>
    <input class="bank-search" id="bank-search" placeholder="Search banks…" autocomplete="off">
    <div class="search-results" id="search-results" hidden></div>
  `;
  const input = document.getElementById('bank-search');
  const results = document.getElementById('search-results');
  input.addEventListener('input', () => {
    const q = input.value.trim().toLowerCase();
    if (!q) { results.hidden = true; results.innerHTML = ''; return; }
    const matches = banksIndex.filter(b => b.name.toLowerCase().includes(q));
    results.innerHTML = matches.length
      ? matches.map(b => `<a href="bank-${b.slug}.html"><span class="bank-swatch" style="background:${BANK_COLOR[b.name]||'#9aa0a8'}"></span>${b.name}</a>`).join('')
      : '<div class="none">No banks match.</div>';
    results.hidden = false;
  });
  document.addEventListener('click', (e) => { if (!wrap.contains(e.target)) results.hidden = true; });
}

// ---- collapsible blocks (comparison.html - long page, less scrolling when
// a reader only cares about one or two sections at a time) ----
function blockOpen(title, hint){
  return `<div class="block"><div class="block-head"><h2>${title}</h2><div class="block-head-right"><span class="hint">${hint}</span><span class="chevron">▾</span></div></div><div class="block-body">`;
}
function blockClose(){ return `</div></div>`; }
// A subsection: one collapsible piece INSIDE a block, for a block that's
// grown too large to scan at a glance in one open state (e.g. "Capital,
// liquidity & RWA" bundles 4 genuinely distinct comparisons). Native
// <details>/<summary> - no extra JS wiring needed, unlike .block's
// click-to-toggle, and it degrades fine with JS disabled.
function subOpen(title, hint, startClosed){
  return `<details class="subsection"${startClosed ? '' : ' open'}><summary><h3>${title}</h3>${hint ? `<span class="hint">${hint}</span>` : ''}</summary><div class="subsection-body">`;
}
function subClose(){ return `</div></details>`; }
function initCollapsibleBlocks(){
  document.querySelectorAll('.block-head').forEach(el => {
    el.addEventListener('click', () => el.closest('.block').classList.toggle('collapsed'));
  });
}

// ---- comparison.html ----
// Comparing a bank against 144 others is only useful when it actually has
// something to plot - an empty "No X disclosed" card next to real charts
// reads as broken, not informative, and 40-140 of the 145 banks are
// genuinely blank for any given section (RWA breakdown, MREL, etc. - see
// the 2026-09-04 disclosure-gap audit). Each block below filters banks to
// the ones with real data for THAT section before rendering, rather than
// sharing one bank list across every section.
function hasLoanData(bd){ return !!latestChartableLoanYear(bd.loan_composition); }
function hasRwaData(bd){ return !!latestYear(bd.rwa_category_composition); }
// Distinct from hasRwaData: a bank can have an RWA composition breakdown
// (rwa_category_composition) for the latest year without ever having a
// disclosed RWA/total-assets density series (rwa_to_assets_pct) - e.g.
// Union Bancaire Privee UK. The trend chart/bank-picker needs its own,
// narrower filter so banks with nothing to plot there don't still get a
// checkbox and an empty line.
function hasRwaDensityData(bd){ return Object.keys(bd.rwa_to_assets_pct||{}).length > 0; }
function hasPillar3Sheets(bd, sheets){ return sheets.some(s => Object.keys((bd.pillar3||{})[s]||{}).length); }
function hasCapitalDeployment(bd){ return !!latestChartableCapitalYear(bd.capital_deployment); }
function hasCostBase(bd){ return !!latestYear(bd.cost_base); }

function renderComparisonPage(data, banks, trends, outliers, parentGroups, efficiency, bubbles, clusters){
  // Exposure-class banks (no IFRS 9 stage split disclosed at all) are
  // deliberately excluded here - that's a different, product-level
  // concentration signal, not comparable to Stage 1/2/3 credit quality, so
  // mixing it into this cross-bank comparison would be misleading. It still
  // shows on that bank's own per-bank page (see renderDrilldownPage).
  const loanBanks = banks.filter(b => data[b].loan_composition.kind === 'stage' && hasLoanData(data[b]));
  const rwaBanks = banks.filter(b => hasRwaData(data[b]));
  const rwaDensityBanks = banks.filter(b => hasRwaDensityData(data[b]));
  const capitalBanks = banks.filter(b => hasPillar3Sheets(data[b], PILLAR3_CAPITAL_SHEETS));
  const liquidityBanks = banks.filter(b => hasPillar3Sheets(data[b], PILLAR3_LIQUIDITY_SHEETS));
  const deploymentBanks = banks.filter(b => hasCapitalDeployment(data[b]));
  const costBanks = banks.filter(b => hasCostBase(data[b]));

  document.getElementById('page-sub').textContent = `Comparing up to ${banks.length} banks (each section only shows banks with real data for it — see each section's own count) — sourced from research/in040_risk_metrics.json and research/in041_spend_metrics.json (+ a direct DB pull for a few per-bank pages, see each bank's own page).`;
  let html = '';

  html += blockOpen('Loan concentration &amp; quality', `${loanBanks.length} of ${banks.length} banks disclose an IFRS 9 stage split — latest disclosed year`);
  html += `<div class="grid cols" id="loan-grid">`;
  loanBanks.forEach(bank => {
    const comp = data[bank].loan_composition;
    const year = latestChartableLoanYear(comp);
    const catNames = year ? Object.keys(comp.years[year]) : [];
    html += `<div class="card bank-card">
      <h3><a href="bank-${slugify(bank)}.html" style="color:inherit;text-decoration:none;">${bank}</a></h3>
      <div class="book-label">${catNames.map(shortCategoryName).join(' + ')}</div>
      <div class="mini-chart-wrap" data-chart="loan" data-bank="${bank}"><canvas></canvas></div>
      ${coverageNplChipsHtml(data[bank], year || latestCoverageYear(data[bank]))}
    </div>`;
  });
  html += `</div>
    <div class="legend-row">
      <span><span class="sw" style="background:${STAGE_COLOR.stage_1}"></span>Stage 1 (performing)</span>
      <span><span class="sw" style="background:${STAGE_COLOR.stage_2}"></span>Stage 2 (watch)</span>
      <span><span class="sw" style="background:${STAGE_COLOR.stage_3}"></span>Stage 3 (default)</span>
    </div>
  ` + blockClose();

  // Capital ratios, liquidity ratios, RWA density, and ratio trajectories
  // are all comparisons of the same 4 core Pillar 3 metrics (+ RWA) - IN-052
  // follow-up merged them into one section (2026-09-05, user request) rather
  // than RWA density and Ratio trajectories staying separate blocks.
  const frnName = frnToBankName(data);
  const trajectoryMetrics = Object.keys(trends.trajectories.metrics);
  html += blockOpen('Capital, liquidity &amp; RWA (Pillar 3)', 'core ratios, RWA composition, and multi-year trend');

  html += subOpen('Capital ratios', `${capitalBanks.length} of ${banks.length} banks`);
  html += `<div class="grid cols" id="pillar3-capital-grid">`;
  capitalBanks.forEach(bank => {
    html += `<div class="card bank-card">
      <h3><a href="bank-${slugify(bank)}.html" style="color:inherit;text-decoration:none;">${bank}</a></h3>
      <div class="mini-chart-wrap tall" data-chart="pillar3-capital" data-bank="${bank}"><canvas></canvas></div>
    </div>`;
  });
  html += `</div>
    <div class="legend-row">
      ${PILLAR3_CAPITAL_SHEETS.map(s => `<span><span class="sw" style="background:${PILLAR3_STYLE[s].color}"></span>${PILLAR3_LABEL[s]}</span>`).join('')}
    </div>` + subClose();

  html += subOpen('Liquidity ratios', `${liquidityBanks.length} of ${banks.length} banks`);
  html += `<div class="grid cols" id="pillar3-liquidity-grid">`;
  liquidityBanks.forEach(bank => {
    html += `<div class="card bank-card">
      <h3><a href="bank-${slugify(bank)}.html" style="color:inherit;text-decoration:none;">${bank}</a></h3>
      <div class="mini-chart-wrap tall" data-chart="pillar3-liquidity" data-bank="${bank}"><canvas></canvas></div>
    </div>`;
  });
  html += `</div>
    <div class="legend-row">
      ${PILLAR3_LIQUIDITY_SHEETS.map(s => `<span><span class="sw" style="background:${PILLAR3_STYLE[s].color}"></span>${PILLAR3_LABEL[s]}</span>`).join('')}
    </div>` + subClose();

  html += subOpen('RWA breakdown', `${rwaBanks.length} of ${banks.length} banks`);
  html += `<div class="card chart-card">
    <div class="bank-picker-panel">
      ${bankPickerSidebarHtml('rwa-bank-picker', rwaDensityBanks)}
      <div class="bank-picker-chart-area">
        <div class="bank-picker-note">Trend line above compares up to ${RWA_PICKER_MAX} banks at once (${rwaDensityBanks.length} banks disclose an RWA/total-assets density series) — pick which ones. All ${rwaBanks.length} banks with an RWA breakdown still appear in the composition cards below.</div>
        <div class="mini-chart-wrap tall" data-chart="rwa-trend"><canvas></canvas></div>
      </div>
    </div>
  </div>`;
  html += `<div class="grid cols" style="margin-top:14px;" id="rwa-grid">`;
  rwaBanks.forEach(bank => {
    const year = latestYear(data[bank].rwa_category_composition);
    const isDerived = bank === 'Weatherbys';
    html += `<div class="card bank-card">
      <h3><a href="bank-${slugify(bank)}.html" style="color:inherit;text-decoration:none;">${bank}</a></h3>
      <div class="book-label">RWA composition, ${year||'—'}${isDerived?` <span class="kind-flag" data-tip="This bank's RWA Breakdown is a documented derived reconstruction, not a directly-disclosed total — see IN-039/ST-037.">ⓘ</span>`:''}</div>
      <div class="mini-chart-wrap" data-chart="rwa-cat" data-bank="${bank}"><canvas></canvas></div>
    </div>`;
  });
  html += `</div>` + subClose();

  html += subOpen('Bank comparison', `ratio trajectories, FY${trends.trajectories.years[0]}–FY${trends.trajectories.years[trends.trajectories.years.length-1]}`);
  trajectoryMetrics.forEach(metric => {
    const metricSlug = slugify(metric);
    const metricBanks = trends.trajectories.metrics[metric].map(r => frnName[r.frn] || r.bank).filter(b => banks.includes(b));
    html += `<div class="book-label" style="margin:14px 0 6px;">${metric} <span style="color:var(--ink-faint);">(${metricBanks.length} of ${banks.length} banks)</span></div>
    <div class="card chart-card">
      <div class="bank-picker-panel">
        ${bankPickerSidebarHtml(`trend-picker-${metricSlug}`, metricBanks)}
        <div class="bank-picker-chart-area">
          <div class="bank-picker-note">Trend line compares up to ${TRAJECTORY_PICKER_MAX} banks at once — default picks banks with data across every year shown (FY${trends.trajectories.years[0]}–FY${trends.trajectories.years[trends.trajectories.years.length-1]}).</div>
          <div class="mini-chart-wrap tall" data-chart="trend" data-metric="${metric}"><canvas></canvas></div>
        </div>
      </div>
    </div>`;
  });
  html += subClose();

  // Box-and-whisker distribution of one Pillar 3 ratio across every bank,
  // by year (user request, 2026-09-09) - a genuinely different lens from
  // the per-bank trend lines and trajectory picker above: instead of
  // following individual banks, this shows the whole peer group's spread
  // (median, quartiles, outliers) per year for whichever metric is picked.
  // Computed client-side from `data` (already embedded in full on this
  // page) rather than a new Python curation step - no new server-side
  // shape needed, just a reduction over pillar3[metric][year] across banks.
  const boxplotMetrics = [...PILLAR3_CAPITAL_SHEETS, ...PILLAR3_LIQUIDITY_SHEETS]
    .filter(m => banks.some(b => Object.keys(data[b].pillar3?.[m] || {}).length));
  if (boxplotMetrics.length) {
    html += subOpen('Distribution across banks', 'spread of one ratio across all banks, by year');
    html += `<div class="card chart-card">
      <div class="chart-controls">
        <label for="pillar3-boxplot-metric">Metric</label>
        <select id="pillar3-boxplot-metric">${boxplotMetrics.map(m => `<option value="${m}">${PILLAR3_LABEL[m]}</option>`).join('')}</select>
      </div>
      <div class="mini-chart-wrap tall" id="pillar3-boxplot-chart" style="height:340px;"><canvas></canvas></div>
      <p class="sub" id="pillar3-boxplot-note" style="margin:8px 0 0;"></p>
    </div>` + subClose();
  }

  // Three Gapminder-style bubble charts (user request, 2026-09-05: the
  // user picked risk_vs_capital first, then asked for the other two axis
  // pairings offered alongside it to be added too). bubbleSectionHtml
  // below is shared markup; each spec supplies its own DOM id prefix,
  // axis labels/units, fixed axis bounds, and explanatory note.
  const BUBBLE_SPECS = [
    {
      key: 'risk_vs_capital', idPrefix: 'risk-bubble',
      title: 'Risk-taking vs. capital strength',
      hint: 'RWA density vs. CET1 Ratio, bubble size = total assets — drag the year slider to watch banks move',
      xLabel: 'RWA density (% of total assets)', yLabel: 'CET1 Ratio (%)',
      xShort: 'RWA density', yShort: 'CET1', xMax: 110, yMax: 90,
      note: 'Bottom-right (high RWA density, low CET1) is the quadrant worth watching.',
    },
    {
      key: 'efficiency_vs_capital', idPrefix: 'efficiency-bubble',
      title: 'Cost efficiency vs. capital strength',
      hint: 'Cost-to-income ratio vs. CET1 Ratio, bubble size = total assets — drag the year slider to watch banks move',
      xLabel: 'Cost-to-income ratio (%)', yLabel: 'CET1 Ratio (%)',
      xShort: 'cost-to-income', yShort: 'CET1', xMax: 200, yMax: 90,
      note: 'Bottom-right (costly to run, thin capital) is the quadrant worth watching. Fewer banks disclose a clean cost-to-income figure than the other two bubble charts — see the coverage note on finding 5 in Cross-Bank Trends Analysis.md.',
    },
    {
      key: 'leverage_vs_liquidity', idPrefix: 'leverage-bubble',
      title: 'Leverage vs. liquidity',
      hint: 'Leverage Ratio vs. LCR, bubble size = total assets — drag the year slider to watch banks move',
      xLabel: 'Leverage Ratio (%)', yLabel: 'LCR (%)',
      xShort: 'Leverage Ratio', yShort: 'LCR', xMax: 50, yMax: 1000,
      note: 'Bottom-left (thin on both fronts) is the quadrant worth watching. A few small banks\' LCR denominators produce five- to six-figure percentages (real disclosures, not comparable moves) and sit off-chart here.',
    },
    {
      key: 'balance_sheet_vs_pnl', idPrefix: 'bs-pnl-bubble',
      title: 'Balance sheet mix vs. cost efficiency',
      hint: 'Customer loans as % of total assets vs. cost-to-income ratio, bubble size = total assets — drag the year slider to watch banks move',
      xLabel: 'Customer loans (% of total assets)', yLabel: 'Cost-to-income ratio (%)',
      xShort: 'loans/assets', yShort: 'cost-to-income', xMax: 100, yMax: 200,
      note: 'Top-right (loan-heavy and costly to run) is the quadrant worth watching. Coverage is limited to banks disclosing both a clean asset-mix split and a cost-to-income figure.',
    },
    {
      key: 'capital_cushion_vs_growth', idPrefix: 'capital-growth-bubble',
      title: 'Capital cushion vs. income growth',
      hint: 'Equity as % of total assets vs. year-on-year income growth, bubble size = total assets — drag the year slider to watch banks move',
      xLabel: 'Equity (% of total assets)', yLabel: 'Income growth, year-on-year (%)',
      xShort: 'equity/assets', yShort: 'income growth', xMax: 100, yMin: -150, yMax: 300,
      note: 'Does a thinly-capitalised bank grow income faster? A handful of small/young banks swing 1,000%+ in a single year off a near-zero prior-year income base (real, not a data error) and sit off-chart.',
    },
    {
      key: 'cost_structure', idPrefix: 'cost-structure-bubble',
      title: 'Cost structure: staff vs. overhead',
      hint: 'Personnel expense vs. other operating expense, both as % of revenue, bubble size = total assets — drag the year slider to watch banks move',
      xLabel: 'Personnel expense (% of revenue)', yLabel: 'Other operating expense (% of revenue)',
      xShort: 'personnel/revenue', yShort: 'other opex/revenue', xMax: 150, yMax: 100,
      note: 'Top-left is overhead-heavy, bottom-right is staff-heavy. Needs both cost lines cleanly disclosed against revenue, so coverage is the smallest of these charts — read it as illustrative, not comprehensive. A few very small-revenue banks push either ratio well past 100% and sit off-chart.',
    },
    {
      key: 'liquidity_vs_loans', idPrefix: 'liquidity-loans-bubble',
      title: 'Cash buffer vs. loan book',
      hint: 'Cash vs. customer loans, both as % of total assets, bubble size = total assets — drag the year slider to watch banks move',
      xLabel: 'Cash (% of total assets)', yLabel: 'Customer loans (% of total assets)',
      xShort: 'cash/assets', yShort: 'loans/assets', xMax: 100, yMax: 100,
      note: 'The two ends of the same asset-mix decision — a bank sitting high on both isn\'t possible for long, since both draw from the same pool of total assets.',
    },
  ];
  BUBBLE_SPECS.forEach(spec => {
    const payload = (bubbles && bubbles[spec.key]) || { years: [] };
    if (!payload.years.length) return;
    const latestIdx = payload.years.length - 1;
    html += subOpen(spec.title, spec.hint);
    html += `<div class="card chart-card">
      <div class="bubble-controls" style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
        <button type="button" class="btn-play" id="${spec.idPrefix}-play">▶ Play</button>
        <input type="range" id="${spec.idPrefix}-year-slider" min="0" max="${latestIdx}" value="${latestIdx}" step="1" style="flex:1;">
        <span id="${spec.idPrefix}-year-label" style="font-weight:600;min-width:56px;text-align:right;">FY${payload.years[latestIdx]}</span>
      </div>
      <div class="mini-chart-wrap tall" id="${spec.idPrefix}-chart" style="height:420px;"><canvas></canvas></div>
      <p class="sub" style="margin:8px 0 0;">Bubble size = total assets (balance-sheet scale). Color = parent group — grouped banks share a color, standalone banks are gray. Axes are fixed across every year so movement between frames is real, not rescaling. ${spec.note}</p>
    </div>` + subClose();
  });

  // Statistical peer clusters: projects scripts/insights/cluster_banks.py's
  // existing k-means fit (previously computed but never visualized
  // anywhere in the deliverable, despite being one of the two things
  // wayfinder/insights/map.md's Destination names as a client goal) onto
  // its own top-2 principal components. Placed in this same block since
  // it clusters on the same 7 Pillar 3 ratios shown above.
  if (clusters) {
    html += subOpen('Peer clusters (statistical)', `k=${clusters.best_k}, silhouette ${clusters.silhouette.toFixed(2)}, ${clusters.n_included} of ${clusters.n_included + clusters.n_excluded} banks clustered`);
    html += `<div class="card chart-card">
      <div class="mini-chart-wrap tall" id="cluster-pca-chart" style="height:420px;"><canvas></canvas></div>
      <p class="sub" style="margin:8px 0 0;">A k-means clustering of all ${clusters.n_included + clusters.n_excluded} banks on their 7 Pillar 3 ratios (CET1/Tier1/Total Capital/Leverage/LCR/NSFR/MREL Ratios), k chosen by silhouette score. ${clusters.n_excluded} banks disclose fewer than 4 of these 7 ratios and are excluded rather than clustered on mostly-imputed data. Lighter/fewer-solid bubbles have 1+ of their 7 dimensions median-imputed rather than disclosed.</p>
    </div>
    <div class="card" style="margin-top:14px;">${clusterPcaExplainerHtml(clusters)}</div>` + subClose();
  }

  html += blockClose();

  html += blockOpen('Balance sheet &amp; P&amp;L', 'where the bank is making money — latest disclosed year');
  html += `<h3 style="font-family:var(--font-serif);font-size:14px;margin:0 0 10px;">Capital deployment <span style="font-weight:400;color:var(--ink-faint);font-size:12px;">(${deploymentBanks.length} of ${banks.length} banks)</span></h3>`;
  html += `<div class="grid cols" id="capital-grid">`;
  deploymentBanks.forEach(bank => {
    const cap = data[bank].capital_deployment;
    const year = latestChartableCapitalYear(cap);
    html += `<div class="card bank-card">
      <h3><a href="bank-${slugify(bank)}.html" style="color:inherit;text-decoration:none;">${bank}</a></h3>
      <div class="book-label">Assets by deployment, ${year||'—'}</div>
      <div class="mini-chart-wrap" data-chart="capital" data-bank="${bank}"><canvas></canvas></div>
    </div>`;
  });
  html += `</div>
    <div class="legend-row">
      <span><span class="sw" style="background:${ASSET_COLOR.cash_pct_of_assets}"></span>Cash</span>
      <span><span class="sw" style="background:${ASSET_COLOR.loans_pct_of_assets}"></span>Customer loans</span>
      <span><span class="sw" style="background:${ASSET_COLOR.treasury_investments_pct_of_assets}"></span>Treasury investments</span>
      <span><span class="sw" style="background:${ASSET_COLOR.other}"></span>Other assets</span>
    </div>`;
  html += `<h3 style="font-family:var(--font-serif);font-size:14px;margin:24px 0 10px;">Cost base <span style="font-weight:400;color:var(--ink-faint);font-size:12px;">(${costBanks.length} of ${banks.length} banks)</span></h3>`;
  html += costBaseTableHtml(data, costBanks);
  html += blockClose();

  const parentGroupCount = new Set(Object.values(parentGroups.metrics).flat().map(g => g.group)).size;
  html += blockOpen('Parent groupings', `${parentGroupCount} commonly-owned groups with 2+ comparable UK entities — do they report similar Pillar 3 outcomes?`);
  html += `<p class="sub" style="margin:0 0 12px;">Each core metric's latest comparable year's median across the group (hover a cell for min/max/range and trend agreement). Most of Katalysis's 145 banks are the only UK entity in their group - shown here are only the groups with two or more. Click a group for its full overview, including each member's own contribution.</p>
  <div class="card" style="overflow-x:auto;">${parentGroupsTableHtml(parentGroups)}</div>`;
  html += blockClose();

  html += blockOpen('Most extreme', `${outliers.length} flagged bank-metric observations — latest value per core metric, flagged for an extreme level, an extreme year-over-year move, or a special disclosure`);
  html += `<p class="sub" style="margin:0 0 12px;">Each bank's latest disclosed value per core metric, flagged when it sits outside the 5th-95th percentile band, scores a robust z-score of 3.5+, moved more than 95% of observed year-over-year changes, or carries a special/non-standard disclosure marker. Click a column heading to sort.</p>
  <div class="card" style="overflow-x:auto;padding:0;">${outliersTableHtml(outliers)}</div>`;
  html += blockClose();

  html += blockOpen('Cost efficiency & profitability', `IN-045: cost-to-income and profit both broadly improved through FY2023, then reversed`);
  html += `<p class="sub" style="margin:0 0 12px;">Share of comparable banks moving the wrong way each year: cost-to-income <em>worsening</em> (rising), profit/(loss) for the year <em>declining</em> — see the coverage note in Cross-Bank Trends Analysis.md before reading these as a majority-of-145 result.</p>
  <div class="card chart-card"><div class="mini-chart-wrap tall" id="comparison-efficiency-chart"><canvas></canvas></div></div>`;
  html += blockClose();

  const screenedCount = trends.headroom.filter(r => r.status === 'screened').length;
  html += blockOpen('Regulatory headroom trajectory', `${screenedCount} bank-metric pairs screened — current ratio minus the dated regulatory floor, plus multi-year trend direction`);
  html += `<p class="sub" style="margin:0 0 12px;">Early-warning screen, not a forecast: <em>headroom</em> is the latest disclosed ratio minus the applicable regulatory minimum and buffer; <em>change</em> is the observed move from the first to latest comparable year. Click a column heading to sort.</p>
  <div class="card" style="overflow-x:auto;padding:0;">${headroomTableHtml(trends.headroom)}</div>`;
  html += blockClose();

  document.getElementById('app').innerHTML = html;
  initCollapsibleBlocks();
  efficiencyChart(document.querySelector('#comparison-efficiency-chart canvas'), efficiency);
  BUBBLE_SPECS.forEach(spec => {
    const payload = (bubbles && bubbles[spec.key]) || { years: [] };
    if (payload.years.length) initBubbleChart(spec, payload);
  });
  if (clusters) initClusterPcaChart(document.querySelector('#cluster-pca-chart canvas'), clusters);

  document.querySelectorAll('[data-chart="capital"]').forEach(el => {
    const bank = el.dataset.bank, cap = data[bank].capital_deployment, year = latestChartableCapitalYear(cap);
    const canvas = el.querySelector('canvas');
    const ok = year && capitalCompositionMiniChart(canvas, cap[year]);
    if (!ok) el.outerHTML = '<div class="empty-note">No capital-deployment data disclosed for this bank.</div>';
  });
  document.querySelectorAll('[data-chart="loan"]').forEach(el => {
    // loanBanks is stage-only (see its filter above), so comp.kind is
    // always 'stage' here - exposure-class banks render on their own
    // per-bank page instead (see renderDrilldownPage).
    const bank = el.dataset.bank, comp = data[bank].loan_composition, year = latestChartableLoanYear(comp);
    const canvas = el.querySelector('canvas');
    const ok = year && stageCompositionMiniChart(canvas, comp.years[year]);
    if (!ok) el.outerHTML = '<div class="empty-note">No loan concentration data disclosed for this bank.</div>';
  });
  document.querySelectorAll('[data-chart="rwa-cat"]').forEach(el => {
    const bank = el.dataset.bank, year = latestYear(data[bank].rwa_category_composition);
    const canvas = el.querySelector('canvas');
    const ok = year && rwaCatMiniChart(canvas, data[bank].rwa_category_composition[year]);
    if (!ok) el.outerHTML = '<div class="empty-note">No RWA category breakdown this year.</div>';
  });
  initRwaBankPicker(document.getElementById('rwa-bank-picker'), document.querySelector('[data-chart="rwa-trend"] canvas'), rwaDensityBanks, data);
  wireBankPickerSearch(document.getElementById('rwa-bank-picker'));
  document.querySelectorAll('[data-chart="pillar3-capital"]').forEach(el => {
    const bank = el.dataset.bank;
    const canvas = el.querySelector('canvas');
    const ok = pillar3TrendChart(canvas, data[bank].pillar3||{}, PILLAR3_CAPITAL_SHEETS, {showLegend:false, pointRadius:2});
    if (!ok) el.outerHTML = '<div class="empty-note">No capital ratios disclosed for this bank.</div>';
  });
  document.querySelectorAll('[data-chart="pillar3-liquidity"]').forEach(el => {
    const bank = el.dataset.bank;
    const canvas = el.querySelector('canvas');
    const ok = pillar3TrendChart(canvas, data[bank].pillar3||{}, PILLAR3_LIQUIDITY_SHEETS, {showLegend:false, pointRadius:2});
    if (!ok) el.outerHTML = '<div class="empty-note">No LCR/NSFR disclosed for this bank.</div>';
  });
  document.querySelectorAll('[data-chart="trend"]').forEach(el => {
    const metric = el.dataset.metric;
    const metricSlug = slugify(metric);
    const metricBanks = trends.trajectories.metrics[metric].map(r => frnName[r.frn] || r.bank).filter(b => banks.includes(b));
    const container = document.getElementById(`trend-picker-${metricSlug}`);
    initTrajectoryBankPicker(container, el.querySelector('canvas'), metric, metricBanks, trends.trajectories, frnName);
    wireBankPickerSearch(container);
  });
  if (boxplotMetrics.length) {
    const boxplotCanvas = document.querySelector('#pillar3-boxplot-chart canvas');
    const boxplotNote = document.getElementById('pillar3-boxplot-note');
    let boxplotChart = null;
    const drawBoxplot = (metric) => { boxplotChart = pillar3BoxplotChart(boxplotCanvas, boxplotChart, data, banks, metric, boxplotNote); };
    drawBoxplot(boxplotMetrics[0]);
    document.getElementById('pillar3-boxplot-metric').addEventListener('change', (e) => drawBoxplot(e.target.value));
  }
  initSortableTables();
}

// ---- bank-<slug>.html ----
function renderDrilldownPage(bank, bankData){
  document.getElementById('page-sub').textContent = `${bank} — full risk profile.`;
  const rwaYears = Object.entries(bankData.rwa_to_assets_pct).sort();
  const latestRwa = rwaYears.length ? rwaYears[rwaYears.length-1][1] : null;
  const comp = bankData.loan_composition;
  const lYear = latestChartableLoanYear(comp);
  const lTotals = stageTotalsForYear(comp, lYear);
  const stage3Pct = lTotals ? (lTotals.stage_3/(lTotals.stage_1+lTotals.stage_2+lTotals.stage_3)*100) : null;
  const profitYears = Object.keys(bankData.profit_for_year||{}).sort();
  const lProfitYear = profitYears.length ? profitYears[profitYears.length-1] : null;
  const lProfit = lProfitYear ? bankData.profit_for_year[lProfitYear] : null;

  // Balance sheet headline figures (user request, 2026-09-09): total assets
  // (size) and equity/assets (capital cushion, an accounting leverage
  // measure distinct from the Pillar 3 Leverage Ratio further down the
  // page) - both already curated per-bank, just not previously surfaced at
  // the top. Replaces the old "years of history available" tile, which
  // was a data-coverage stat rather than something about the bank itself.
  const totalAssetsYears = Object.entries(bankData.total_assets||{}).sort();
  const latestTotalAssets = totalAssetsYears.length ? totalAssetsYears[totalAssetsYears.length-1][1] : null;
  const latestTotalAssetsYear = totalAssetsYears.length ? totalAssetsYears[totalAssetsYears.length-1][0] : null;
  const equityPctYears = Object.entries((bankData.leverage||{}).equity_to_assets_pct||{}).sort();
  const latestEquityPct = equityPctYears.length ? equityPctYears[equityPctYears.length-1][1] : null;

  const radar = bankData.radar;
  const radarLabels = radar ? RADAR_METRIC_ORDER.filter(m => radar[m]) : [];
  const hasRadar = radarLabels.length >= 3;

  let html = `<div style="display:flex;gap:14px;align-items:stretch;margin-bottom:20px;">
    <div class="kpi-row" style="margin-bottom:0;flex:1;">
      <div class="kpi"><div class="val">${latestTotalAssets!=null?fmtBn(latestTotalAssets):'—'}</div><div class="lbl">Total assets${latestTotalAssetsYear?' (FY'+latestTotalAssetsYear+')':''}</div></div>
      <div class="kpi"><div class="val" style="color:${lProfit==null?'inherit':(lProfit>=0?'var(--green)':'var(--red)')}">${lProfit!=null?fmtBn(lProfit):'—'}</div><div class="lbl">Profit for the year${lProfitYear?' (FY'+lProfitYear+')':''}</div></div>
      <div class="kpi"><div class="val">${latestEquityPct!=null?latestEquityPct+'%':'—'}</div><div class="lbl">Equity / Total assets (latest)</div></div>
      <div class="kpi"><div class="val">${latestRwa!==null?latestRwa+'%':'—'}</div><div class="lbl">RWA / Total assets (latest)</div></div>
      <div class="kpi"><div class="val">${stage3Pct!==null?stage3Pct.toFixed(1)+'%':(comp.kind==='exposure_class'?'n/a — no stage data':'n/d')}</div><div class="lbl">Stage 3 share of book (latest)</div></div>
    </div>`;
  if (hasRadar) {
    html += `<div class="card" style="flex:0 0 190px;padding:8px;" title="${bank} vs. every other bank, percentile rank per Pillar 3 metric — further out means stronger than more peers">
      <div style="height:170px;"><canvas id="drilldown-radar-chart"></canvas></div>
    </div>`;
  }
  html += `</div>`;

  html += blockOpen('Loan concentration &amp; quality', `${bank}, by year`) + `<div class="card">`;
  const years = Object.keys(comp.years).sort();
  if (!years.length) {
    html += `<div class="empty-note">No loan concentration data disclosed for ${bank} in any year.</div>`;
  } else if (comp.kind === 'stage') {
    html += historyChartHtml('drilldown-stage-chart', years);
  } else {
    html += `<div class="empty-note">No IFRS&nbsp;9 stage split disclosed — showing Pillar&nbsp;3 credit-risk exposure by class instead (a different, product-level concentration view).</div>`;
    html += historyChartHtml('drilldown-exposure-chart', years);
  }
  html += `<div style="margin-top:12px;">${coverageNplChipsHtml(bankData, lYear || latestCoverageYear(bankData))}</div>`;
  html += `</div>` + blockClose();

  html += blockOpen('RWA density', `${bank}, by year`);
  if (!rwaYears.length) {
    html += `<div class="card"><div class="empty-note">No RWA / total assets figures disclosed for ${bank} in any year.</div></div>`;
  } else {
    html += `<div class="card chart-card"><div class="mini-chart-wrap tall"><canvas id="drilldown-rwa-trend"></canvas></div></div>`;
  }
  const catYear = latestYear(bankData.rwa_category_composition);
  const isDerived = bank === 'Weatherbys';
  html += subOpen(`RWA composition, ${catYear||'—'}${isDerived?` <span class="kind-flag" data-tip="This bank's RWA Breakdown is a documented derived reconstruction, not a directly-disclosed total — see IN-039/ST-037.">ⓘ</span>`:''}`)
    + `<div class="card" id="drilldown-rwa-cat-card">
        <div class="view-toggle" id="drilldown-rwa-cat-toggle">
          <button type="button" data-view="bar" class="active">Bar</button>
          <button type="button" data-view="pie">Pie</button>
        </div>
        <div id="drilldown-rwa-cat-bar-view"><div class="mini-chart-wrap tall" id="drilldown-rwa-cat"><canvas></canvas></div></div>
        <div id="drilldown-rwa-cat-pie-view" hidden><div class="mini-chart-wrap tall" id="drilldown-rwa-cat-pie"><canvas></canvas></div></div>
      </div>`
    + subClose();
  html += blockClose();

  const pillar3 = bankData.pillar3 || {};
  const capitalP3Sheets = PILLAR3_CAPITAL_SHEETS.filter(s => Object.keys(pillar3[s]||{}).length);
  const liquidityP3Sheets = PILLAR3_LIQUIDITY_SHEETS.filter(s => Object.keys(pillar3[s]||{}).length);
  html += blockOpen('Capital &amp; liquidity (Pillar 3)', `${bank}, by year`);
  if (!capitalP3Sheets.length && !liquidityP3Sheets.length) {
    html += `<div class="card"><div class="empty-note">No Pillar 3 capital or liquidity ratios disclosed for ${bank} in any year.</div></div>`;
  } else {
    html += subOpen('Capital ratios') + `<div class="card chart-card">` + (capitalP3Sheets.length
      ? `<div class="mini-chart-wrap tall" id="drilldown-pillar3-capital-chart"><canvas></canvas></div>`
      : `<div class="empty-note">No capital ratios disclosed for ${bank} in any year.</div>`) + `</div>` + subClose();
    html += subOpen('Liquidity ratios') + `<div class="card chart-card">` + (liquidityP3Sheets.length
      ? `<div class="mini-chart-wrap tall" id="drilldown-pillar3-liquidity-chart"><canvas></canvas></div>`
      : `<div class="empty-note">No LCR/NSFR disclosed for ${bank} in any year.</div>`) + `</div>` + subClose();
  }
  const leverage = bankData.leverage || {};
  const hasLeverage = Object.keys(leverage.equity_to_assets_pct||{}).length || Object.keys(leverage.leverage_ratio_reported_pct||{}).length;
  if (hasLeverage) {
    html += subOpen('Leverage') + `<div class="card chart-card"><div class="mini-chart-wrap tall" id="drilldown-leverage-chart"><canvas></canvas></div></div>` + subClose();
  }
  const headroomTable = bankHeadroomTableHtml(bankData.headroom);
  if (headroomTable) {
    html += subOpen('Regulatory headroom')
      + `<p class="sub" style="margin:0 0 10px;">How far above the applicable regulatory minimum (plus buffer) ${bank}'s latest disclosed ratio sits, per metric — an early-warning screen, not a forecast. <em>Change</em> is the move from the first to latest comparable year.</p>`
      + `<div class="card" style="overflow-x:auto;padding:0;">${headroomTable}</div>`
      + subClose();
  }
  html += blockClose();

  const capYears = Object.keys(bankData.capital_deployment).sort();
  const costYears = Object.keys(bankData.cost_base).sort();
  const lCostYear = costYears.length ? costYears[costYears.length-1] : null;
  html += blockOpen('Balance sheet &amp; P&amp;L', `${bank}, by year — where the bank is making money`);
  html += subOpen('Capital deployment');
  html += `<div class="card chart-card">`;
  html += capYears.length
    ? `${historyChartHtml('drilldown-capital-chart', capYears)}
       <div class="legend-row">
         <span><span class="sw" style="background:${ASSET_COLOR.cash_pct_of_assets}"></span>Cash</span>
         <span><span class="sw" style="background:${ASSET_COLOR.loans_pct_of_assets}"></span>Customer loans</span>
         <span><span class="sw" style="background:${ASSET_COLOR.treasury_investments_pct_of_assets}"></span>Treasury investments</span>
         <span><span class="sw" style="background:${ASSET_COLOR.other}"></span>Other assets</span>
       </div>`
    : `<div class="empty-note">No capital-deployment data disclosed for ${bank} in any year.</div>`;
  html += `</div>` + subClose();

  const bsSankey = bankData.balance_sheet_sankey;
  if (bsSankey) {
    html += subOpen('How the balance sheet is funded', `assets → total assets → liabilities &amp; equity`);
    html += `<div class="card chart-card">
      <div class="mini-chart-wrap tall" id="drilldown-bs-sankey" style="height:380px;"><canvas></canvas></div>
    </div>`;
    html += subClose();
  }

  const incomeYears = Object.keys(bankData.income_breakdown||{}).sort();
  html += subOpen('Income mix');
  html += `<div class="card chart-card">`;
  html += incomeYears.length
    ? `${historyChartHtml('drilldown-income-chart', incomeYears)}
       <div class="legend-row">
         ${INCOME_ORDER.map(k => `<span><span class="sw" style="background:${INCOME_COLOR[k]}"></span>${k}</span>`).join('')}
       </div>`
    : `<div class="empty-note">No income-mix data disclosed for ${bank} in any year.</div>`;
  html += `</div>` + subClose();

  const pnlSankey = bankData.pnl_sankey;
  if (pnlSankey) {
    html += subOpen('Where the income goes', `income sources → total income → expenses / operating profit → costs / profit for the year`);
    html += `<div class="card chart-card">
      <div class="view-toggle" id="drilldown-pnl-flow-toggle">
        <button type="button" data-view="sankey" class="active">Sankey</button>
        <button type="button" data-view="waterfall">Waterfall</button>
      </div>
      <div id="drilldown-pnl-flow-sankey-view"><div class="mini-chart-wrap tall" id="drilldown-pnl-sankey" style="height:460px;"><canvas></canvas></div></div>
      <div id="drilldown-pnl-flow-waterfall-view" hidden><div class="mini-chart-wrap tall" id="drilldown-pnl-waterfall" style="height:380px;"><canvas></canvas></div></div>
    </div>`;
    html += subClose();
  }

  const iVol = bankData.income_volatility || {};
  const iVolYears = Object.keys(iVol.yoy_change_pct||{}).sort();
  if (iVolYears.length) {
    html += subOpen('Income volatility');
    html += `<div class="card chart-card">`;
    if (iVol.volatility_stdev_of_yoy_pct != null) {
      html += `<div class="chip-row" style="margin-bottom:12px;"><span class="chip raw"><b>${iVol.volatility_stdev_of_yoy_pct.toFixed(1)}pp</b> YoY swing, std. dev.</span></div>`;
    }
    html += historyChartHtml('drilldown-income-volatility-chart', iVolYears);
    html += `</div>` + subClose();
  }

  html += subOpen('Cost base');
  html += `<div class="card" style="margin-bottom:14px;">${costBaseChipsHtml(lCostYear ? bankData.cost_base[lCostYear] : null)}</div>`;
  const hasCostToIncomeTrend = costYears.some(y => bankData.cost_base[y].cost_to_income_pct != null);
  if (hasCostToIncomeTrend) {
    html += `<div class="card chart-card">${historyChartHtml('drilldown-cti-chart', costYears)}</div>`;
  }
  html += subClose();
  html += blockClose();

  const cashFlowYears = Object.keys(bankData.cash_flow||{}).sort();
  html += blockOpen('Cash flow', `${bank}, by year`);
  html += `<div class="card chart-card">`;
  html += cashFlowYears.length
    ? `<div class="mini-chart-wrap tall" id="drilldown-cashflow-chart"><canvas></canvas></div>`
    : `<div class="empty-note">No cash flow statement data disclosed for ${bank} in any year.</div>`;
  html += `</div>` + blockClose();

  const equity = bankData.equity_changes;
  const hasMovements = equity && equity.waterfall && equity.waterfall.length;
  html += blockOpen('Statement of Changes in Equity', `${bank}, chronological roll-forward`);
  if (hasMovements) {
    // Same recent-by-default / full-history-behind-a-toggle treatment as
    // the capital deployment and income mix charts below (see
    // `mountEquityMovementsChart`) - archival, pre-cutoff segments (some
    // of which are undisclosed-movement gaps, e.g. Union Bancaire Privee
    // UK's own pre-2013 checkpoints) are hidden by default.
    const hasArchive = equity.waterfall.some(s => s.start_year != null && s.start_year < ARCHIVE_HISTORY_CUTOFF);
    const control = hasArchive ? `<div class="history-chart-control">
      <button type="button" data-history-toggle>Show full available history</button>
      <span data-history-caption>Showing FY${ARCHIVE_HISTORY_CUTOFF} onwards</span>
    </div>` : '';
    html += subOpen('Where each year\'s equity change came from');
    html += `<div class="card chart-card"><div class="history-chart" id="drilldown-equity-movements">${control}<div class="mini-chart-wrap"><canvas></canvas></div></div></div>` + subClose();
  }
  const mixYears = equity && equity.mix_by_year ? Object.keys(equity.mix_by_year) : [];
  html += subOpen('Equity mix over time');
  html += `<div class="card chart-card">` + (mixYears.length
    ? historyChartHtml('drilldown-equity-mix', mixYears)
    : `<div class="empty-note">No year-by-year equity composition available for ${bank}.</div>`) + `</div>` + subClose();
  html += subOpen('Full roll-forward', `${equity && equity.rows ? equity.rows.length : ''} rows`, true);
  html += `<div class="card">${equityChangesTableHtml(equity)}</div>` + subClose();
  html += blockClose();

  // Parent-company market data (user request, 2026-09-09; demoted lower on
  // the page and out of the KPI row per 2026-09-09 follow-up - a secondary,
  // hand-fetched reference point, not a headline figure). Only rendered
  // for the subset of banks whose ultimate parent is a separately,
  // currently LSE-listed company - most tracked entities are wholly-owned
  // subsidiaries with nothing to show here.
  const pmd = bankData.parent_market_data;
  const pmdChartable = pmd && (Object.keys(pmd.history_daily || {}).length > 1 || Object.keys(pmd.history || {}).length > 1);
  if (pmd) {
    const priceStr = pmd.share_price_gbx.toFixed(2) + 'p';
    const capStr = fmtBn(pmd.market_cap_gbp);
    html += blockOpen('Parent company market data', `${pmd.parent} (${pmd.exchange}: ${pmd.ticker})`);
    html += `<div class="card" style="padding:12px 16px;display:flex;gap:24px;align-items:center;flex-wrap:wrap;">
      <div><span class="sub">Share price</span> <strong>${priceStr}</strong></div>
      <div><span class="sub">Market cap</span> <strong>${capStr}</strong></div>
      <div class="sub">as of ${pmd.as_of} — <a href="${pmd.source}" target="_blank" rel="noopener">source</a></div>
    </div>`;
    if (pmdChartable) {
      html += `<div class="card chart-card" style="margin-top:10px;">
        <div class="mini-chart-wrap tall" id="drilldown-parent-market-chart"><canvas></canvas></div>
        <p class="sub" style="margin:8px 0 0;">Daily share price, spanning the years ${bank} also has balance-sheet data${Object.keys(pmd.report_dates||{}).length ? ' — markers show when that year\'s full-year results were announced' : ''}.</p>
      </div>`;
    }
    html += blockClose();
  }

  if (bankData.source_workbook) {
    html += blockOpen('Full workbook', `${bank}, every sheet as published`) + `
      <div class="card" style="padding:0;">
        <iframe src="workbook-${slugify(bank)}.html" style="width:100%;height:560px;border:0;display:block;" loading="lazy" title="${bank} workbook"></iframe>
      </div>
      <div class="workbook-link-block"><a href="../../../banks/${encodeURIComponent(bankData.source_workbook)}">Open the full workbook (.xlsx) for ${bank} ↗</a></div>
    ` + blockClose();
  }

  document.getElementById('app').innerHTML = html;
  initCollapsibleBlocks();

  if (hasRadar) radarChart(document.getElementById('drilldown-radar-chart'), radar, bank);
  if (bsSankey) sankeyChart(document.querySelector('#drilldown-bs-sankey canvas'), bsSankey.links, ['Total assets'], {'Total assets': 'Total assets / Liabilities + Equity'});
  if (pnlSankey) {
    sankeyChart(document.querySelector('#drilldown-pnl-sankey canvas'), pnlSankey.links, ['Total income', 'Operating expenses', 'Operating profit']);
    let pnlWaterfallDrawn = false;
    const pnlFlowToggle = document.getElementById('drilldown-pnl-flow-toggle');
    pnlFlowToggle.addEventListener('click', (e) => {
      const btn = e.target.closest('button[data-view]');
      if (!btn) return;
      pnlFlowToggle.querySelectorAll('button').forEach(b => b.classList.toggle('active', b === btn));
      const isSankey = btn.dataset.view === 'sankey';
      document.getElementById('drilldown-pnl-flow-sankey-view').hidden = !isSankey;
      document.getElementById('drilldown-pnl-flow-waterfall-view').hidden = isSankey;
      if (!isSankey && !pnlWaterfallDrawn) {
        pnlWaterfallDrawn = pnlWaterfallChart(document.querySelector('#drilldown-pnl-waterfall canvas'), pnlSankey);
      }
    });
  }
  if (capitalP3Sheets.length) pillar3TrendChart(document.querySelector('#drilldown-pillar3-capital-chart canvas'), pillar3, PILLAR3_CAPITAL_SHEETS);
  if (liquidityP3Sheets.length) pillar3TrendChart(document.querySelector('#drilldown-pillar3-liquidity-chart canvas'), pillar3, PILLAR3_LIQUIDITY_SHEETS);
  if (hasLeverage) leverageChart(document.querySelector('#drilldown-leverage-chart canvas'), leverage);
  if (pmdChartable) parentMarketDataChart(document.querySelector('#drilldown-parent-market-chart canvas'), pmd);
  if (iVolYears.length) mountHistoryChart('drilldown-income-volatility-chart', iVolYears,
    (canvas, chartYears) => incomeVolatilityChart(canvas, iVol, chartYears));
  if (cashFlowYears.length) cashFlowChart(document.querySelector('#drilldown-cashflow-chart canvas'), bankData.cash_flow);
  if (hasMovements) mountEquityMovementsChart('drilldown-equity-movements', equity);
  if (mixYears.length) mountHistoryChart('drilldown-equity-mix', mixYears,
    (canvas, chartYears) => equityMixChart(canvas, equity, chartYears));

  if (comp.kind === 'stage' && years.length) {
    mountHistoryChart('drilldown-stage-chart', years, (canvas, chartYears) => {
      const totalsByYear = chartYears.map(y => {
        const t = {stage_1:0,stage_2:0,stage_3:0};
        Object.values(comp.years[y]).forEach(c => Object.entries(c).forEach(([k,v]) => { if (k in t) t[k]+=v; }));
        return t;
      });
      return new Chart(canvas, {
        type: 'bar',
        data: { labels: chartYears, datasets: [
          {label:'Stage 1', data: totalsByYear.map(t=>t.stage_1), backgroundColor: STAGE_COLOR.stage_1},
          {label:'Stage 2', data: totalsByYear.map(t=>t.stage_2), backgroundColor: STAGE_COLOR.stage_2},
          {label:'Stage 3', data: totalsByYear.map(t=>t.stage_3), backgroundColor: STAGE_COLOR.stage_3},
        ]},
        options: { responsive:true, maintainAspectRatio:false,
          scales: { x:{stacked:true, grid:{display:false}}, y:{stacked:true, grid:{color:'#edece7'}} },
          plugins: { legend: { display:true, position:'bottom' } },
        },
      });
    });
  } else if (comp.kind === 'exposure_class' && years.length) {
    mountHistoryChart('drilldown-exposure-chart', years, (canvas, chartYears) => {
      const cats = [...new Set(chartYears.flatMap(y => Object.keys(comp.years[y])))];
      return new Chart(canvas, {
        type: 'bar',
        data: { labels: chartYears, datasets: cats.map((cat,i) => ({
          label: cat, data: chartYears.map(y => comp.years[y][cat] ?? 0),
          backgroundColor: CATEGORICAL_PALETTE[i % CATEGORICAL_PALETTE.length],
        })) },
        options: { responsive:true, maintainAspectRatio:false,
          scales: { x:{stacked:true, grid:{display:false}}, y:{stacked:true, grid:{color:'#edece7'}} },
          plugins: { legend: { display:true, position:'bottom', labels:{boxWidth:10, font:{size:10}} } },
        },
      });
    });
  }

  if (rwaYears.length) {
    new Chart(document.getElementById('drilldown-rwa-trend'), {
      type: 'line',
      data: { labels: rwaYears.map(([y])=>y), datasets: [{
        label: bank, data: rwaYears.map(([,v])=>v),
        borderColor: BANK_COLOR[bank] || '#2563eb', backgroundColor: BANK_COLOR[bank] || '#2563eb', tension:0.15, pointRadius:4,
      }] },
      options: { responsive:true, maintainAspectRatio:false,
        scales: { y:{ ticks:{callback: v=>v+'%'}, grid:{color:'#edece7'} }, x:{grid:{display:false}} },
      },
    });
  }

  {
    const catRows = catYear ? bankData.rwa_category_composition[catYear] : null;
    if (!catRows || !rwaCatChart(document.querySelector('#drilldown-rwa-cat canvas'), catRows)) {
      document.getElementById('drilldown-rwa-cat-card').outerHTML = '<div class="empty-note">No data.</div>';
    } else {
      let rwaPieDrawn = false;
      const rwaCatToggle = document.getElementById('drilldown-rwa-cat-toggle');
      rwaCatToggle.addEventListener('click', (e) => {
        const btn = e.target.closest('button[data-view]');
        if (!btn) return;
        rwaCatToggle.querySelectorAll('button').forEach(b => b.classList.toggle('active', b === btn));
        const isBar = btn.dataset.view === 'bar';
        document.getElementById('drilldown-rwa-cat-bar-view').hidden = !isBar;
        document.getElementById('drilldown-rwa-cat-pie-view').hidden = isBar;
        if (!isBar && !rwaPieDrawn) {
          rwaPieDrawn = rwaCatPieChart(document.querySelector('#drilldown-rwa-cat-pie canvas'), catRows);
        }
      });
    }
  }

  if (capYears.length) {
    mountHistoryChart('drilldown-capital-chart', capYears, (canvas, chartYears) => {
    const mixes = chartYears.map(y => assetMixForYear(bankData.capital_deployment[y]));
    return new Chart(canvas, {
      type: 'bar',
      data: { labels: chartYears, datasets: [
        {label: ASSET_LABEL.cash_pct_of_assets, data: mixes.map(m=>m.cash_pct_of_assets), backgroundColor: ASSET_COLOR.cash_pct_of_assets},
        {label: ASSET_LABEL.loans_pct_of_assets, data: mixes.map(m=>m.loans_pct_of_assets), backgroundColor: ASSET_COLOR.loans_pct_of_assets},
        {label: ASSET_LABEL.treasury_investments_pct_of_assets, data: mixes.map(m=>m.treasury_investments_pct_of_assets), backgroundColor: ASSET_COLOR.treasury_investments_pct_of_assets},
        {label: ASSET_LABEL.other, data: mixes.map(m=>m.other), backgroundColor: ASSET_COLOR.other},
      ]},
      options: { responsive:true, maintainAspectRatio:false,
        scales: { x:{stacked:true, grid:{display:false}}, y:{stacked:true, max:100, ticks:{callback:v=>v+'%'}, grid:{color:'#edece7'}} },
        plugins: { tooltip: { callbacks: { label: (ctx) => ctx.raw != null ? `${ctx.dataset.label}: ${ctx.raw.toFixed(1)}%` : `${ctx.dataset.label}: n/d` } } },
      },
    });
    });
  }
  if (incomeYears.length) {
    mountHistoryChart('drilldown-income-chart', incomeYears, (canvas, chartYears) => {
    const mixes = chartYears.map(y => incomeMixPct(bankData.income_breakdown[y]));
    return new Chart(canvas, {
      type: 'bar',
      data: { labels: chartYears, datasets: INCOME_ORDER.map(k => ({
        label: k, data: mixes.map(m => m[k] != null ? Math.max(0, m[k]) : null),
        backgroundColor: INCOME_COLOR[k],
      })) },
      options: { responsive:true, maintainAspectRatio:false,
        scales: { x:{stacked:true, grid:{display:false}}, y:{stacked:true, max:100, ticks:{callback:v=>v+'%'}, grid:{color:'#edece7'}} },
        plugins: { tooltip: { callbacks: { label: (ctx) => ctx.raw != null ? `${ctx.dataset.label}: ${ctx.raw.toFixed(1)}%` : `${ctx.dataset.label}: n/d` } } },
      },
    });
    });
  }
  if (hasCostToIncomeTrend) {
    mountHistoryChart('drilldown-cti-chart', costYears, (canvas, chartYears) => new Chart(canvas, {
      type: 'line',
      data: { labels: chartYears, datasets: [{
        label: 'Cost-to-income', data: chartYears.map(y => bankData.cost_base[y].cost_to_income_pct ?? null),
        borderColor: BANK_COLOR[bank] || '#1e3a5f', backgroundColor: BANK_COLOR[bank] || '#1e3a5f', tension:0.15, spanGaps:true, pointRadius:4,
      }] },
      options: { responsive:true, maintainAspectRatio:false,
        scales: { y:{ ticks:{callback: v=>v+'%'}, grid:{color:'#edece7'} }, x:{grid:{display:false}} },
      },
    }));
  }
}

// ---- group-<slug>.html: a multi-member parent group's overview (user
// request, 2026-09-05: click a group in comparison.html's Parent groupings
// table -> a page for the group, not just a table row). Member roster +
// headline figures (Total P&L) + the ratio dispersion/trend-agreement view
// already computed for comparison.html, scoped to just this one group. ----
function renderGroupPage(groupData, banksIndex){
  const { group, meta, metrics, group_level_metrics } = groupData;
  document.getElementById('page-sub').textContent = `${group} — ${meta.members.length} comparable UK entities.`;

  const pnlYears = Object.keys(meta.total_pnl_by_year).sort();
  const latestYearKey = pnlYears.length ? pnlYears[pnlYears.length-1] : null;
  const latestPnl = latestYearKey ? meta.total_pnl_by_year[latestYearKey] : null;
  const chartAssetYears = [...new Set(Object.values(meta.member_total_assets).flatMap(a => Object.keys(a)))].sort();
  const combinedAssetYears = Object.keys(meta.total_assets_by_year).sort();
  const latestCombinedAssetYear = combinedAssetYears.length ? combinedAssetYears[combinedAssetYears.length-1] : null;
  const latestTotalAssets = latestCombinedAssetYear ? meta.total_assets_by_year[latestCombinedAssetYear] : null;

  let html = `<div class="kpi-row">
    <div class="kpi"><div class="val" style="color:${latestPnl==null?'inherit':(latestPnl>=0?'var(--green)':'var(--red)')}">${latestPnl!=null?fmtK(latestPnl):'—'}</div><div class="lbl">Total P&amp;L${latestYearKey?' (FY'+latestYearKey+')':''}</div></div>
    <div class="kpi"><div class="val">${latestTotalAssets!=null?fmtK(latestTotalAssets):'—'}</div><div class="lbl">Combined total assets${latestCombinedAssetYear?' (FY'+latestCombinedAssetYear+')':''}</div></div>
    <div class="kpi"><div class="val">${meta.members.length}</div><div class="lbl">Comparable UK entities</div></div>
    <div class="kpi"><div class="val">${pnlYears.length}</div><div class="lbl">Years with every member reporting</div></div>
  </div>`;

  html += blockOpen('Members', group) + `<div class="card" style="padding:0;">
    <table class="bank-table"><thead><tr><th>Bank</th><th></th></tr></thead><tbody>
    ${meta.members.map(m => `<tr><td><a href="bank-${slugify(m.bank)}.html">${m.bank}</a></td><td>${m.caveat ? `<span class="hint">${m.caveat}</span>` : ''}</td></tr>`).join('')}
    </tbody></table>
  </div>` + blockClose();

  html += blockOpen('Total P&amp;L', 'summed only across years every member discloses') + `<div class="card chart-card">` + (pnlYears.length
      ? `<div class="mini-chart-wrap tall" id="group-pnl-chart"><canvas></canvas></div>`
      : `<div class="empty-note">No year where every member of ${group} discloses profit or loss.</div>`) + `</div>` + blockClose();

  html += blockOpen('Balance sheet contribution', `each member's own Total assets, by year`) + `<div class="card chart-card">` + (chartAssetYears.length
      ? `<div class="mini-chart-wrap tall" id="group-assets-chart"><canvas></canvas></div>`
      : `<div class="empty-note">No member of ${group} has a usable Total assets figure (non-GBP disclosures are excluded, not converted).</div>`) + `</div>` + blockClose();

  const membersWithAssetMix = meta.members.filter(m => latestChartableCapitalYear(meta.member_capital_deployment[m.bank]));
  const membersWithLiabilityMix = meta.members.filter(m => Object.keys(meta.member_liability_composition[m.bank] || {}).length);
  const combinedAssetYear = latestChartableCapitalYear(meta.group_asset_composition);
  const combinedAssetMix = combinedAssetYear ? assetMixForYear(meta.group_asset_composition[combinedAssetYear]) : null;
  const combinedLiabYears = Object.keys(meta.group_liability_composition).sort();
  const combinedLiabYear = combinedLiabYears.length ? combinedLiabYears[combinedLiabYears.length-1] : null;
  const combinedLiabMix = combinedLiabYear ? meta.group_liability_composition[combinedLiabYear] : null;

  html += blockOpen('What those assets &amp; liabilities are', `each member's own latest-year composition, plus the whole group combined`);
  html += `<h3 style="font-family:var(--font-serif);font-size:14px;margin:0 0 10px;">Assets</h3>`;
  if (combinedAssetMix) {
    html += `<p class="sub" style="margin:0 0 12px;">Combining every member's own £ figures for FY${combinedAssetYear}: <strong>${combinedAssetMix.loans_pct_of_assets.toFixed(1)}%</strong> of ${group}'s combined assets are customer loans, <strong>${combinedAssetMix.cash_pct_of_assets.toFixed(1)}%</strong> cash &amp; central bank balances, <strong>${combinedAssetMix.treasury_investments_pct_of_assets.toFixed(1)}%</strong> treasury investments, and <strong>${combinedAssetMix.other.toFixed(1)}%</strong> other assets.</p>`;
  }
  html += `<div class="card chart-card">` + (membersWithAssetMix.length
    ? `<div class="mini-chart-wrap tall" id="group-asset-mix-chart"><canvas></canvas></div>
       <div class="legend-row">
         <span><span class="sw" style="background:${ASSET_COLOR.cash_pct_of_assets}"></span>Cash</span>
         <span><span class="sw" style="background:${ASSET_COLOR.loans_pct_of_assets}"></span>Customer loans</span>
         <span><span class="sw" style="background:${ASSET_COLOR.treasury_investments_pct_of_assets}"></span>Treasury investments</span>
         <span><span class="sw" style="background:${ASSET_COLOR.other}"></span>Other assets</span>
       </div>`
    : `<div class="empty-note">No member of ${group} has a usable asset-mix figure.</div>`) + `</div>`;
  html += `<h3 style="font-family:var(--font-serif);font-size:14px;margin:24px 0 10px;">Liabilities</h3>`;
  if (combinedLiabMix) {
    html += `<p class="sub" style="margin:0 0 12px;">Combining every member's own £ figures for FY${combinedLiabYear}: <strong>${combinedLiabMix.customer_deposits_pct.toFixed(1)}%</strong> of ${group}'s combined liabilities are customer deposits, <strong>${combinedLiabMix.bank_deposits_pct.toFixed(1)}%</strong> bank deposits, <strong>${combinedLiabMix.wholesale_funding_pct.toFixed(1)}%</strong> wholesale funding, and <strong>${combinedLiabMix.other_pct.toFixed(1)}%</strong> other liabilities.</p>`;
  }
  html += `<div class="card chart-card">` + (membersWithLiabilityMix.length
    ? `<div class="mini-chart-wrap tall" id="group-liability-mix-chart"><canvas></canvas></div>
       <div class="legend-row">
         ${LIABILITY_ORDER.map(k => `<span><span class="sw" style="background:${LIABILITY_COLOR[k]}"></span>${LIABILITY_LABEL[k]}</span>`).join('')}
       </div>`
    : `<div class="empty-note">No member of ${group} has a usable liability-mix figure.</div>`) + `</div>`;
  html += blockClose();

  const groupIncomeYears = Object.keys(meta.total_income_breakdown_by_year).sort();
  html += blockOpen('Where the group made its profit &amp; loss', 'income mix, summed only across years every member discloses') + `<div class="card chart-card">` + (groupIncomeYears.length
      ? `<div class="mini-chart-wrap tall" id="group-income-chart"><canvas></canvas></div>
         <div class="legend-row">
           ${INCOME_ORDER.map(k => `<span><span class="sw" style="background:${INCOME_COLOR[k]}"></span>${k}</span>`).join('')}
         </div>`
      : `<div class="empty-note">No year where every member of ${group} discloses an income mix.</div>`) + `</div>` + blockClose();

  html += blockOpen(`Pillar 3 ratios — each member's contribution`, `${group}, latest comparable year per metric`) + `<div class="card">${groupMetricChartsHtml(metrics)}</div>` + blockClose();

  const glmSheets = Object.keys(group_level_metrics || {});
  if (glmSheets.length) {
    html += blockOpen('Reported only at the parent-group level', `${glmSheets.length} metric${glmSheets.length===1?'':'s'} some members don't disclose solo`) + `
      <p class="sub" style="margin:0 0 12px;">Found while building each member's own workbook: these metrics aren't disclosed by every member on its own account, because the figure is only set/published at a wider group level. Where a sibling member's own disclosure IS that group-consolidated figure, it's shown here as the best available stand-in for the whole group.</p>
      <div class="card">${groupLevelMetricsHtml(group_level_metrics)}</div>
    ` + blockClose();
  }

  document.getElementById('app').innerHTML = html;
  initCollapsibleBlocks();
  mountGroupMetricCharts(metrics);

  if (pnlYears.length) {
    new Chart(document.querySelector('#group-pnl-chart canvas'), {
      type: 'line',
      data: { labels: pnlYears, datasets: [{
        label: 'Total P&L', data: pnlYears.map(y => meta.total_pnl_by_year[y]),
        borderColor: '#2563eb', backgroundColor: '#2563eb', tension: 0.15, pointRadius: 4,
      }] },
      options: { responsive:true, maintainAspectRatio:false,
        scales: { y:{ ticks:{callback: v=>fmtK(v)}, grid:{color:'#edece7'} }, x:{grid:{display:false}} },
      },
    });
  }

  if (chartAssetYears.length) {
    const memberNames = Object.keys(meta.member_total_assets);
    new Chart(document.querySelector('#group-assets-chart canvas'), {
      type: 'bar',
      data: { labels: chartAssetYears, datasets: memberNames.map(bank => ({
        label: bank, data: chartAssetYears.map(y => meta.member_total_assets[bank][y] ?? null),
        backgroundColor: BANK_COLOR[bank] || '#2563eb',
      })) },
      options: { responsive:true, maintainAspectRatio:false,
        scales: { x:{stacked:true, grid:{display:false}}, y:{stacked:true, ticks:{callback: v=>fmtK(v)}, grid:{color:'#edece7'}} },
        plugins: { legend: { display:true, position:'bottom', labels:{boxWidth:10, font:{size:10}} },
          tooltip: { callbacks: { label: ctx => `${ctx.dataset.label}: ${ctx.raw!=null?fmtK(ctx.raw):'n/d'}` } } },
      },
    });
  }

  if (membersWithAssetMix.length) {
    const labels = membersWithAssetMix.map(m => m.bank);
    const mixes = membersWithAssetMix.map(m => assetMixForYear(meta.member_capital_deployment[m.bank][latestChartableCapitalYear(meta.member_capital_deployment[m.bank])]));
    if (combinedAssetMix) { labels.unshift(`${group} — combined`); mixes.unshift(combinedAssetMix); }
    new Chart(document.querySelector('#group-asset-mix-chart canvas'), {
      type: 'bar',
      data: { labels, datasets: [
        {label: ASSET_LABEL.cash_pct_of_assets, data: mixes.map(m=>m.cash_pct_of_assets), backgroundColor: ASSET_COLOR.cash_pct_of_assets},
        {label: ASSET_LABEL.loans_pct_of_assets, data: mixes.map(m=>m.loans_pct_of_assets), backgroundColor: ASSET_COLOR.loans_pct_of_assets},
        {label: ASSET_LABEL.treasury_investments_pct_of_assets, data: mixes.map(m=>m.treasury_investments_pct_of_assets), backgroundColor: ASSET_COLOR.treasury_investments_pct_of_assets},
        {label: ASSET_LABEL.other, data: mixes.map(m=>m.other), backgroundColor: ASSET_COLOR.other},
      ] },
      options: { indexAxis:'y', responsive:true, maintainAspectRatio:false,
        scales: { x:{stacked:true, ticks:{callback:v=>v+'%'}, grid:{color:'#edece7'}}, y:{stacked:true, grid:{display:false},
          ticks:{font: ctx => ({weight: combinedAssetMix && ctx.index===0 ? 'bold' : 'normal'})}} },
        plugins: { legend:{display:false}, tooltip:{callbacks:{label: ctx => `${ctx.dataset.label}: ${ctx.raw.toFixed(1)}%`}} },
      },
    });
  }

  if (membersWithLiabilityMix.length) {
    const labels = membersWithLiabilityMix.map(m => m.bank);
    const mixes = membersWithLiabilityMix.map(m => {
      const liab = meta.member_liability_composition[m.bank];
      const years = Object.keys(liab).sort();
      return liab[years[years.length-1]];
    });
    if (combinedLiabMix) { labels.unshift(`${group} — combined`); mixes.unshift(combinedLiabMix); }
    new Chart(document.querySelector('#group-liability-mix-chart canvas'), {
      type: 'bar',
      data: { labels, datasets: LIABILITY_ORDER.map(k => ({
        label: LIABILITY_LABEL[k], data: mixes.map(m=>m[k]), backgroundColor: LIABILITY_COLOR[k],
      })) },
      options: { indexAxis:'y', responsive:true, maintainAspectRatio:false,
        scales: { x:{stacked:true, ticks:{callback:v=>v+'%'}, grid:{color:'#edece7'}}, y:{stacked:true, grid:{display:false},
          ticks:{font: ctx => ({weight: combinedLiabMix && ctx.index===0 ? 'bold' : 'normal'})}} },
        plugins: { legend:{display:false}, tooltip:{callbacks:{label: ctx => `${ctx.dataset.label}: ${ctx.raw.toFixed(1)}%`}} },
      },
    });
  }

  if (groupIncomeYears.length) {
    new Chart(document.querySelector('#group-income-chart canvas'), {
      type: 'bar',
      data: { labels: groupIncomeYears, datasets: INCOME_ORDER.map(k => ({
        label: k, data: groupIncomeYears.map(y => meta.total_income_breakdown_by_year[y][k] ?? null),
        backgroundColor: INCOME_COLOR[k],
      })) },
      options: { responsive:true, maintainAspectRatio:false,
        scales: { x:{stacked:true, grid:{display:false}}, y:{stacked:true, ticks:{callback: v=>fmtK(v)}, grid:{color:'#edece7'}} },
        plugins: { legend:{display:false}, tooltip:{callbacks:{label: ctx => `${ctx.dataset.label}: ${ctx.raw!=null?fmtK(ctx.raw):'n/d'}`}} },
      },
    });
  }
}

// "Reported only at the parent-group level" (2026-09-05 follow-up: earlier
// in this project's own disclosure audit, missing metrics were often
// traced to being set only at a wider group level - now surfaced per
// group rather than only living in each bank's own workbook note).
function groupLevelMetricsHtml(groupLevelMetrics){
  return Object.keys(groupLevelMetrics).map(sheet => {
    const entry = groupLevelMetrics[sheet];
    const flaggedHtml = entry.flagged.map(f => `<span class="kind-flag" data-tip="${f.note.replace(/"/g,'&quot;')}">${f.bank} ⓘ</span>`).join(', ');
    const sub = entry.substitute;
    const ult = entry.ultimate_parent;
    const subLine = sub
      ? (() => {
          const years = Object.keys(sub.values).sort();
          const latest = years[years.length-1];
          return `Reported by <a href="bank-${slugify(sub.bank)}.html">${sub.bank}</a> on its own Group-consolidated basis: <strong>${sub.values[latest]}%</strong> <span class="hint">FY${latest}</span> - taken as the best available stand-in for the whole group.`;
        })()
      : '';
    // Ultimate/resolution parent's own consolidated figure is a genuinely
    // better "whole group" answer than a sibling member's solo figure -
    // shown as the primary line, with the sibling-member figure kept
    // underneath for context when both exist (2026-09-05 follow-up:
    // "instead of a sibling member substitute, perhaps we try search in
    // the ultimate parent as well, and see if that can get a better
    // picture for the whole group").
    const subHtml = ult
      ? (() => {
          const years = Object.keys(ult.values).sort();
          const latest = years[years.length-1];
          const primary = `Reported by <strong>${ult.entity}</strong> (the ultimate/resolution parent, not one of Katalysis's 145 banks) in its own public disclosures: <strong>${ult.values[latest]}%</strong> <span class="hint">FY${latest}</span>. <span class="hint" data-tip="${ult.citation.replace(/"/g,'&quot;')}">Source ⓘ</span>`;
          return subLine ? `${primary}<br><span class="hint">Also: ${subLine}</span>` : primary;
        })()
      : sub
      ? subLine
      : `Not captured by any member's own workbook in this dataset - likely disclosed only at the ultimate parent, which isn't one of Katalysis's 145 banks.`;
    return `<div style="margin-bottom:16px;">
      <div class="book-label" style="margin-bottom:4px;">${sheet}</div>
      <div style="margin-bottom:4px;">Not disclosed solo by: ${flaggedHtml}</div>
      <div class="hint">${subHtml}</div>
    </div>`;
  }).join('');
}
