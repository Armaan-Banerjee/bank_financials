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
  // A handful of banks have two roll-forward segments landing on the same
  // calendar-year label (e.g. a mid-year restatement checkpoint alongside
  // the calendar year-end) - disambiguate with (i)/(ii) rather than showing
  // two identical "FY2023" rows.
  const yearCounts = {};
  segments.forEach(s => { yearCounts[s.year] = (yearCounts[s.year] || 0) + 1; });
  const yearSeen = {};
  const rowLabels = segments.map(s => {
    if (yearCounts[s.year] <= 1) return `FY${s.year}`;
    yearSeen[s.year] = (yearSeen[s.year] || 0) + 1;
    return `FY${s.year} (${'i'.repeat(yearSeen[s.year])})`;
  });
  new Chart(canvas, {
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
  return true;
}
function equityMixChart(canvas, equity){
  const years = Object.keys(equity.mix_by_year || {}).sort();
  if (!years.length) return false;
  const comps = equity.components.filter(c => years.some(y => c in equity.mix_by_year[y]));
  if (!comps.length) return false;
  new Chart(canvas, {
    type: 'bar',
    data: { labels: years, datasets: comps.map((c, i) => ({
      label: c, data: years.map(y => equity.mix_by_year[y][c] ?? 0),
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
  return true;
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
function incomeVolatilityChart(canvas, iVol){
  const years = Object.keys(iVol.yoy_change_pct||{}).sort();
  if (!years.length) return false;
  new Chart(canvas, {
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
  return true;
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
      backgroundColor: groupColor(g) + 'b3', borderColor: groupColor(g), borderWidth: 1,
    })),
    { label: 'Standalone', data: initial.standalone, backgroundColor: '#c7c2b499', borderColor: '#a39a86', borderWidth: 1 },
  ];

  const chart = new Chart(canvas, {
    type: 'bubble',
    data: { datasets },
    options: {
      responsive: true, maintainAspectRatio: false,
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
        x: { title: { display: true, text: spec.xLabel }, min: 0, max: spec.xMax, grid: { color: '#edece7' } },
        y: { title: { display: true, text: spec.yLabel }, min: 0, max: spec.yMax, grid: { color: '#edece7' } },
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

// ---- sidebar: nav + compact search only (the full bank list lives on
// banks.html now, not in the sidebar, so it stays a fixed size regardless
// of how many banks the real build eventually covers) ----
function renderSidebar(activeNav, banksIndex){
  assignBankColors(banksIndex);
  document.getElementById('sidebar-nav').innerHTML = `
    <a href="comparison.html" class="${activeNav==='comparison'?'active':''}">Comparison</a>
    <a href="banks.html" class="${activeNav==='banks'?'active':''}">Banks</a>
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
function subOpen(title, hint){
  return `<details class="subsection" open><summary><h3>${title}</h3>${hint ? `<span class="hint">${hint}</span>` : ''}</summary><div class="subsection-body">`;
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
    <div class="bank-picker" id="rwa-bank-picker">${rwaBanks.map(b => `<label><input type="checkbox" value="${b}"><span class="sw" style="background:${BANK_COLOR[b]}"></span>${b}</label>`).join('')}</div>
    <div class="bank-picker-note">Trend line above compares up to ${RWA_PICKER_MAX} banks at once — pick which ones. All ${rwaBanks.length} banks with an RWA breakdown still appear in the composition cards below.</div>
    <div class="mini-chart-wrap tall" data-chart="rwa-trend"><canvas></canvas></div>
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
      <div class="bank-picker" id="trend-picker-${metricSlug}">${metricBanks.map(b => `<label><input type="checkbox" value="${b}"><span class="sw" style="background:${BANK_COLOR[b]}"></span>${b}</label>`).join('')}</div>
      <div class="bank-picker-note">Trend line compares up to ${TRAJECTORY_PICKER_MAX} banks at once — default picks banks with data across every year shown (FY${trends.trajectories.years[0]}–FY${trends.trajectories.years[trends.trajectories.years.length-1]}).</div>
      <div class="mini-chart-wrap tall" data-chart="trend" data-metric="${metric}"><canvas></canvas></div>
    </div>`;
  });
  html += subClose();

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
  initRwaBankPicker(document.getElementById('rwa-bank-picker'), document.querySelector('[data-chart="rwa-trend"] canvas'), rwaBanks, data);
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
    initTrajectoryBankPicker(document.getElementById(`trend-picker-${metricSlug}`), el.querySelector('canvas'), metric, metricBanks, trends.trajectories, frnName);
  });
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

  let html = `<div class="kpi-row">
    <div class="kpi"><div class="val" style="color:${lProfit==null?'inherit':(lProfit>=0?'var(--green)':'var(--red)')}">${lProfit!=null?fmtK(lProfit):'—'}</div><div class="lbl">Profit for the year${lProfitYear?' (FY'+lProfitYear+')':''}</div></div>
    <div class="kpi"><div class="val">${latestRwa!==null?latestRwa+'%':'—'}</div><div class="lbl">RWA / Total assets (latest)</div></div>
    <div class="kpi"><div class="val">${stage3Pct!==null?stage3Pct.toFixed(1)+'%':(comp.kind==='exposure_class'?'n/a — no stage data':'n/d')}</div><div class="lbl">Stage 3 share of book (latest)</div></div>
    <div class="kpi"><div class="val">${Object.keys(comp.years).length}</div><div class="lbl">Years with loan-concentration data</div></div>
  </div>`;

  html += `<div class="block"><div class="block-head"><h2>Loan concentration &amp; quality</h2><span class="hint">${bank}, by year</span></div><div class="card">`;
  const years = Object.keys(comp.years).sort();
  if (!years.length) {
    html += `<div class="empty-note">No loan concentration data disclosed for ${bank} in any year.</div>`;
  } else if (comp.kind === 'stage') {
    html += `<div class="mini-chart-wrap tall" id="drilldown-stage-chart"><canvas></canvas></div>`;
  } else {
    html += `<div class="empty-note">No IFRS&nbsp;9 stage split disclosed — showing Pillar&nbsp;3 credit-risk exposure by class instead (a different, product-level concentration view).</div>`;
    html += `<div class="mini-chart-wrap tall" id="drilldown-exposure-chart"><canvas></canvas></div>`;
  }
  html += `<div style="margin-top:12px;">${coverageNplChipsHtml(bankData, lYear || latestCoverageYear(bankData))}</div>`;
  html += `</div></div>`;

  html += `<div class="block"><div class="block-head"><h2>RWA density</h2><span class="hint">${bank}, by year</span></div>`;
  html += `<div class="card chart-card"><div class="mini-chart-wrap tall"><canvas id="drilldown-rwa-trend"></canvas></div></div>`;
  const catYear = latestYear(bankData.rwa_category_composition);
  const isDerived = bank === 'Weatherbys';
  html += `<div class="card" style="margin-top:14px;">
    <h3 style="margin-top:0;font-size:13px;">RWA composition, ${catYear||'—'}${isDerived?` <span class="kind-flag" data-tip="This bank's RWA Breakdown is a documented derived reconstruction, not a directly-disclosed total — see IN-039/ST-037.">ⓘ</span>`:''}</h3>
    <div class="mini-chart-wrap tall" id="drilldown-rwa-cat"><canvas></canvas></div>
  </div>`;
  html += `</div>`;

  const pillar3 = bankData.pillar3 || {};
  const capitalP3Sheets = PILLAR3_CAPITAL_SHEETS.filter(s => Object.keys(pillar3[s]||{}).length);
  const liquidityP3Sheets = PILLAR3_LIQUIDITY_SHEETS.filter(s => Object.keys(pillar3[s]||{}).length);
  html += `<div class="block"><div class="block-head"><h2>Capital &amp; liquidity (Pillar 3)</h2><span class="hint">${bank}, by year</span></div>`;
  if (!capitalP3Sheets.length && !liquidityP3Sheets.length) {
    html += `<div class="card"><div class="empty-note">No Pillar 3 capital or liquidity ratios disclosed for ${bank} in any year.</div></div>`;
  } else {
    html += `<h3 style="font-family:var(--font-serif);font-size:14px;margin:0 0 10px;">Capital ratios</h3>`;
    html += `<div class="card chart-card">` + (capitalP3Sheets.length
      ? `<div class="mini-chart-wrap tall" id="drilldown-pillar3-capital-chart"><canvas></canvas></div>`
      : `<div class="empty-note">No capital ratios disclosed for ${bank} in any year.</div>`) + `</div>`;
    html += `<h3 style="font-family:var(--font-serif);font-size:14px;margin:24px 0 10px;">Liquidity ratios</h3>`;
    html += `<div class="card chart-card">` + (liquidityP3Sheets.length
      ? `<div class="mini-chart-wrap tall" id="drilldown-pillar3-liquidity-chart"><canvas></canvas></div>`
      : `<div class="empty-note">No LCR/NSFR disclosed for ${bank} in any year.</div>`) + `</div>`;
  }
  const leverage = bankData.leverage || {};
  const hasLeverage = Object.keys(leverage.equity_to_assets_pct||{}).length || Object.keys(leverage.leverage_ratio_reported_pct||{}).length;
  if (hasLeverage) {
    html += `<h3 style="font-family:var(--font-serif);font-size:14px;margin:24px 0 10px;">Leverage</h3>`;
    html += `<div class="card chart-card"><div class="mini-chart-wrap tall" id="drilldown-leverage-chart"><canvas></canvas></div></div>`;
  }
  const headroomTable = bankHeadroomTableHtml(bankData.headroom);
  if (headroomTable) {
    html += `<h3 style="font-family:var(--font-serif);font-size:14px;margin:24px 0 10px;">Regulatory headroom</h3>`;
    html += `<p class="sub" style="margin:0 0 10px;">How far above the applicable regulatory minimum (plus buffer) ${bank}'s latest disclosed ratio sits, per metric — an early-warning screen, not a forecast. <em>Change</em> is the move from the first to latest comparable year.</p>`;
    html += `<div class="card" style="overflow-x:auto;padding:0;">${headroomTable}</div>`;
  }
  html += `</div>`;

  const capYears = Object.keys(bankData.capital_deployment).sort();
  const costYears = Object.keys(bankData.cost_base).sort();
  const lCostYear = costYears.length ? costYears[costYears.length-1] : null;
  html += `<div class="block"><div class="block-head"><h2>Balance sheet &amp; P&amp;L</h2><span class="hint">${bank}, by year — where the bank is making money</span></div>`;
  html += `<h3 style="font-family:var(--font-serif);font-size:14px;margin:0 0 10px;">Capital deployment</h3>`;
  html += `<div class="card chart-card">`;
  html += capYears.length
    ? `<div class="mini-chart-wrap tall" id="drilldown-capital-chart"><canvas></canvas></div>
       <div class="legend-row">
         <span><span class="sw" style="background:${ASSET_COLOR.cash_pct_of_assets}"></span>Cash</span>
         <span><span class="sw" style="background:${ASSET_COLOR.loans_pct_of_assets}"></span>Customer loans</span>
         <span><span class="sw" style="background:${ASSET_COLOR.treasury_investments_pct_of_assets}"></span>Treasury investments</span>
         <span><span class="sw" style="background:${ASSET_COLOR.other}"></span>Other assets</span>
       </div>`
    : `<div class="empty-note">No capital-deployment data disclosed for ${bank} in any year.</div>`;
  html += `</div>`;

  const incomeYears = Object.keys(bankData.income_breakdown||{}).sort();
  html += `<h3 style="font-family:var(--font-serif);font-size:14px;margin:24px 0 10px;">Income mix</h3>`;
  html += `<div class="card chart-card">`;
  html += incomeYears.length
    ? `<div class="mini-chart-wrap tall" id="drilldown-income-chart"><canvas></canvas></div>
       <div class="legend-row">
         ${INCOME_ORDER.map(k => `<span><span class="sw" style="background:${INCOME_COLOR[k]}"></span>${k}</span>`).join('')}
       </div>`
    : `<div class="empty-note">No income-mix data disclosed for ${bank} in any year.</div>`;
  html += `</div>`;

  const iVol = bankData.income_volatility || {};
  const iVolYears = Object.keys(iVol.yoy_change_pct||{}).sort();
  if (iVolYears.length) {
    html += `<h3 style="font-family:var(--font-serif);font-size:14px;margin:24px 0 10px;">Income volatility</h3>`;
    html += `<div class="card chart-card">`;
    if (iVol.volatility_stdev_of_yoy_pct != null) {
      html += `<div class="chip-row" style="margin-bottom:12px;"><span class="chip raw"><b>${iVol.volatility_stdev_of_yoy_pct.toFixed(1)}pp</b> YoY swing, std. dev.</span></div>`;
    }
    html += `<div class="mini-chart-wrap tall" id="drilldown-income-volatility-chart"><canvas></canvas></div>`;
    html += `</div>`;
  }

  html += `<h3 style="font-family:var(--font-serif);font-size:14px;margin:24px 0 10px;">Cost base</h3>`;
  html += `<div class="card" style="margin-bottom:14px;">${costBaseChipsHtml(lCostYear ? bankData.cost_base[lCostYear] : null)}</div>`;
  const hasCostToIncomeTrend = costYears.some(y => bankData.cost_base[y].cost_to_income_pct != null);
  if (hasCostToIncomeTrend) {
    html += `<div class="card chart-card"><div class="mini-chart-wrap tall" id="drilldown-cti-chart"><canvas></canvas></div></div>`;
  }
  html += `</div>`;

  const cashFlowYears = Object.keys(bankData.cash_flow||{}).sort();
  html += `<div class="block"><div class="block-head"><h2>Cash flow</h2><span class="hint">${bank}, by year</span></div>`;
  html += `<div class="card chart-card">`;
  html += cashFlowYears.length
    ? `<div class="mini-chart-wrap tall" id="drilldown-cashflow-chart"><canvas></canvas></div>`
    : `<div class="empty-note">No cash flow statement data disclosed for ${bank} in any year.</div>`;
  html += `</div></div>`;

  const equity = bankData.equity_changes;
  const hasMovements = equity && equity.waterfall && equity.waterfall.length;
  html += `<div class="block"><div class="block-head"><h2>Statement of Changes in Equity</h2><span class="hint">${bank}, chronological roll-forward</span></div>`;
  if (hasMovements) {
    // One horizontal row per fiscal year plus room for the bottom legend -
    // the fixed 150px "tall" wrap (sized for line/vertical-bar charts) left
    // no room for the legend once there were more than ~3 years of rows.
    const movementsHeight = Math.max(150, equity.waterfall.length * 34 + 50);
    html += `<h3 style="font-family:var(--font-serif);font-size:14px;margin:0 0 10px;">Where each year's equity change came from</h3>`;
    html += `<div class="card chart-card"><div class="mini-chart-wrap" style="height:${movementsHeight}px" id="drilldown-equity-movements"><canvas></canvas></div></div>`;
  }
  html += `<h3 style="font-family:var(--font-serif);font-size:14px;margin:24px 0 10px;">Equity mix over time</h3>`;
  html += `<div class="card chart-card">` + (equity && equity.mix_by_year && Object.keys(equity.mix_by_year).length
    ? `<div class="mini-chart-wrap tall" id="drilldown-equity-mix"><canvas></canvas></div>`
    : `<div class="empty-note">No year-by-year equity composition available for ${bank}.</div>`) + `</div>`;
  html += `<h3 style="font-family:var(--font-serif);font-size:14px;margin:24px 0 10px;">Full roll-forward</h3>`;
  html += `<div class="card">${equityChangesTableHtml(equity)}</div></div>`;

  if (bankData.source_workbook) {
    html += `<div class="block"><div class="block-head"><h2>Full workbook</h2><span class="hint">${bank}, every sheet as published</span></div>
      <div class="card" style="padding:0;">
        <iframe src="workbook-${slugify(bank)}.html" style="width:100%;height:560px;border:0;display:block;" loading="lazy" title="${bank} workbook"></iframe>
      </div>
      <div class="workbook-link-block"><a href="../../../banks/${encodeURIComponent(bankData.source_workbook)}">Open the full workbook (.xlsx) for ${bank} ↗</a></div>
    </div>`;
  }

  document.getElementById('app').innerHTML = html;

  if (capitalP3Sheets.length) pillar3TrendChart(document.querySelector('#drilldown-pillar3-capital-chart canvas'), pillar3, PILLAR3_CAPITAL_SHEETS);
  if (liquidityP3Sheets.length) pillar3TrendChart(document.querySelector('#drilldown-pillar3-liquidity-chart canvas'), pillar3, PILLAR3_LIQUIDITY_SHEETS);
  if (hasLeverage) leverageChart(document.querySelector('#drilldown-leverage-chart canvas'), leverage);
  if (iVolYears.length) incomeVolatilityChart(document.querySelector('#drilldown-income-volatility-chart canvas'), iVol);
  if (cashFlowYears.length) cashFlowChart(document.querySelector('#drilldown-cashflow-chart canvas'), bankData.cash_flow);
  if (hasMovements) equityMovementsChart(document.querySelector('#drilldown-equity-movements canvas'), equity);
  if (equity) equityMixChart(document.querySelector('#drilldown-equity-mix canvas'), equity);

  if (comp.kind === 'stage' && years.length) {
    const totalsByYear = years.map(y => {
      const t = {stage_1:0,stage_2:0,stage_3:0};
      Object.values(comp.years[y]).forEach(c => Object.entries(c).forEach(([k,v]) => { if (k in t) t[k]+=v; }));
      return t;
    });
    new Chart(document.querySelector('#drilldown-stage-chart canvas'), {
      type: 'bar',
      data: { labels: years, datasets: [
        {label:'Stage 1', data: totalsByYear.map(t=>t.stage_1), backgroundColor: STAGE_COLOR.stage_1},
        {label:'Stage 2', data: totalsByYear.map(t=>t.stage_2), backgroundColor: STAGE_COLOR.stage_2},
        {label:'Stage 3', data: totalsByYear.map(t=>t.stage_3), backgroundColor: STAGE_COLOR.stage_3},
      ]},
      options: { responsive:true, maintainAspectRatio:false,
        scales: { x:{stacked:true, grid:{display:false}}, y:{stacked:true, grid:{color:'#edece7'}} },
        plugins: { legend: { display:true, position:'bottom' } },
      },
    });
  } else if (comp.kind === 'exposure_class' && years.length) {
    const cats = [...new Set(years.flatMap(y => Object.keys(comp.years[y])))];
    new Chart(document.querySelector('#drilldown-exposure-chart canvas'), {
      type: 'bar',
      data: { labels: years, datasets: cats.map((cat,i) => ({
        label: cat, data: years.map(y => comp.years[y][cat] ?? 0),
        backgroundColor: CATEGORICAL_PALETTE[i % CATEGORICAL_PALETTE.length],
      })) },
      options: { responsive:true, maintainAspectRatio:false,
        scales: { x:{stacked:true, grid:{display:false}}, y:{stacked:true, grid:{color:'#edece7'}} },
        plugins: { legend: { display:true, position:'bottom', labels:{boxWidth:10, font:{size:10}} } },
      },
    });
  }

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

  if (catYear) {
    const rows = bankData.rwa_category_composition[catYear].filter(r=>r.pct_of_total_rwa>0.05);
    document.getElementById('drilldown-rwa-cat').style.height = Math.max(150, rows.length * 28) + 'px';
    new Chart(document.querySelector('#drilldown-rwa-cat canvas'), {
      type: 'bar',
      data: { labels: distinguishingLabels(rows), datasets: [{
        data: rows.map(r=>r.pct_of_total_rwa), backgroundColor: rows.map(r=>rwaCatColor(r.label)),
      }] },
      options: { indexAxis:'y', responsive:true, maintainAspectRatio:false,
        scales: { x:{ ticks:{callback:v=>v+'%'}, grid:{color:'#edece7'} }, y:{grid:{display:false}} },
      },
    });
  } else {
    document.getElementById('drilldown-rwa-cat').outerHTML = '<div class="empty-note">No data.</div>';
  }

  if (capYears.length) {
    const mixes = capYears.map(y => assetMixForYear(bankData.capital_deployment[y]));
    new Chart(document.querySelector('#drilldown-capital-chart canvas'), {
      type: 'bar',
      data: { labels: capYears, datasets: [
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
  }
  if (incomeYears.length) {
    const mixes = incomeYears.map(y => incomeMixPct(bankData.income_breakdown[y]));
    new Chart(document.querySelector('#drilldown-income-chart canvas'), {
      type: 'bar',
      data: { labels: incomeYears, datasets: INCOME_ORDER.map(k => ({
        label: k, data: mixes.map(m => m[k] != null ? Math.max(0, m[k]) : null),
        backgroundColor: INCOME_COLOR[k],
      })) },
      options: { responsive:true, maintainAspectRatio:false,
        scales: { x:{stacked:true, grid:{display:false}}, y:{stacked:true, max:100, ticks:{callback:v=>v+'%'}, grid:{color:'#edece7'}} },
        plugins: { tooltip: { callbacks: { label: (ctx) => ctx.raw != null ? `${ctx.dataset.label}: ${ctx.raw.toFixed(1)}%` : `${ctx.dataset.label}: n/d` } } },
      },
    });
  }
  if (hasCostToIncomeTrend) {
    new Chart(document.querySelector('#drilldown-cti-chart canvas'), {
      type: 'line',
      data: { labels: costYears, datasets: [{
        label: 'Cost-to-income', data: costYears.map(y => bankData.cost_base[y].cost_to_income_pct ?? null),
        borderColor: BANK_COLOR[bank] || '#1e3a5f', backgroundColor: BANK_COLOR[bank] || '#1e3a5f', tension:0.15, spanGaps:true, pointRadius:4,
      }] },
      options: { responsive:true, maintainAspectRatio:false,
        scales: { y:{ ticks:{callback: v=>v+'%'}, grid:{color:'#edece7'} }, x:{grid:{display:false}} },
      },
    });
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

  html += `<div class="block"><div class="block-head"><h2>Members</h2><span class="hint">${group}</span></div><div class="card" style="padding:0;">
    <table class="bank-table"><thead><tr><th>Bank</th><th></th></tr></thead><tbody>
    ${meta.members.map(m => `<tr><td><a href="bank-${slugify(m.bank)}.html">${m.bank}</a></td><td>${m.caveat ? `<span class="hint">${m.caveat}</span>` : ''}</td></tr>`).join('')}
    </tbody></table>
  </div></div>`;

  html += `<div class="block"><div class="block-head"><h2>Total P&amp;L</h2><span class="hint">summed only across years every member discloses</span></div>
    <div class="card chart-card">` + (pnlYears.length
      ? `<div class="mini-chart-wrap tall" id="group-pnl-chart"><canvas></canvas></div>`
      : `<div class="empty-note">No year where every member of ${group} discloses profit or loss.</div>`) + `</div></div>`;

  html += `<div class="block"><div class="block-head"><h2>Balance sheet contribution</h2><span class="hint">each member's own Total assets, by year</span></div>
    <div class="card chart-card">` + (chartAssetYears.length
      ? `<div class="mini-chart-wrap tall" id="group-assets-chart"><canvas></canvas></div>`
      : `<div class="empty-note">No member of ${group} has a usable Total assets figure (non-GBP disclosures are excluded, not converted).</div>`) + `</div></div>`;

  const membersWithAssetMix = meta.members.filter(m => latestChartableCapitalYear(meta.member_capital_deployment[m.bank]));
  const membersWithLiabilityMix = meta.members.filter(m => Object.keys(meta.member_liability_composition[m.bank] || {}).length);
  const combinedAssetYear = latestChartableCapitalYear(meta.group_asset_composition);
  const combinedAssetMix = combinedAssetYear ? assetMixForYear(meta.group_asset_composition[combinedAssetYear]) : null;
  const combinedLiabYears = Object.keys(meta.group_liability_composition).sort();
  const combinedLiabYear = combinedLiabYears.length ? combinedLiabYears[combinedLiabYears.length-1] : null;
  const combinedLiabMix = combinedLiabYear ? meta.group_liability_composition[combinedLiabYear] : null;

  html += `<div class="block"><div class="block-head"><h2>What those assets &amp; liabilities are</h2><span class="hint">each member's own latest-year composition, plus the whole group combined</span></div>`;
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
  html += `</div>`;

  const groupIncomeYears = Object.keys(meta.total_income_breakdown_by_year).sort();
  html += `<div class="block"><div class="block-head"><h2>Where the group made its profit &amp; loss</h2><span class="hint">income mix, summed only across years every member discloses</span></div>
    <div class="card chart-card">` + (groupIncomeYears.length
      ? `<div class="mini-chart-wrap tall" id="group-income-chart"><canvas></canvas></div>
         <div class="legend-row">
           ${INCOME_ORDER.map(k => `<span><span class="sw" style="background:${INCOME_COLOR[k]}"></span>${k}</span>`).join('')}
         </div>`
      : `<div class="empty-note">No year where every member of ${group} discloses an income mix.</div>`) + `</div></div>`;

  html += `<div class="block"><div class="block-head"><h2>Pillar 3 ratios — each member's contribution</h2><span class="hint">${group}, latest comparable year per metric</span></div>
    <div class="card">${groupMetricChartsHtml(metrics)}</div>
  </div>`;

  const glmSheets = Object.keys(group_level_metrics || {});
  if (glmSheets.length) {
    html += `<div class="block"><div class="block-head"><h2>Reported only at the parent-group level</h2><span class="hint">${glmSheets.length} metric${glmSheets.length===1?'':'s'} some members don't disclose solo</span></div>
      <p class="sub" style="margin:0 0 12px;">Found while building each member's own workbook: these metrics aren't disclosed by every member on its own account, because the figure is only set/published at a wider group level. Where a sibling member's own disclosure IS that group-consolidated figure, it's shown here as the best available stand-in for the whole group.</p>
      <div class="card">${groupLevelMetricsHtml(group_level_metrics)}</div>
    </div>`;
  }

  document.getElementById('app').innerHTML = html;
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
