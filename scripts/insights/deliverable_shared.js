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
function initRwaBankPicker(container, canvas, banks, data){
  let selected = new Set(banks.slice(0, RWA_PICKER_MAX));
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

function renderComparisonPage(data, banks){
  const loanBanks = banks.filter(b => hasLoanData(data[b]));
  const rwaBanks = banks.filter(b => hasRwaData(data[b]));
  const capitalBanks = banks.filter(b => hasPillar3Sheets(data[b], PILLAR3_CAPITAL_SHEETS));
  const liquidityBanks = banks.filter(b => hasPillar3Sheets(data[b], PILLAR3_LIQUIDITY_SHEETS));
  const deploymentBanks = banks.filter(b => hasCapitalDeployment(data[b]));
  const costBanks = banks.filter(b => hasCostBase(data[b]));

  document.getElementById('page-sub').textContent = `Comparing up to ${banks.length} banks (each section only shows banks with real data for it — see each section's own count) — sourced from research/in040_risk_metrics.json and research/in041_spend_metrics.json (+ a direct DB pull for Weatherbys, see note).`;
  let html = '';

  html += blockOpen('Loan concentration &amp; quality', `${loanBanks.length} of ${banks.length} banks disclose this — latest disclosed year`);
  html += `<div class="grid cols" id="loan-grid">`;
  loanBanks.forEach(bank => {
    const comp = data[bank].loan_composition;
    const year = latestChartableLoanYear(comp);
    const catNames = year ? Object.keys(comp.years[year]) : [];
    const flag = comp.kind === 'exposure_class'
      ? ` <span class="kind-flag" data-tip="No IFRS 9 stage split disclosed by this bank. Shown instead: Pillar 3 credit-risk exposure by class — a different, product-level view of concentration, not the same stage-quality signal.">ⓘ by exposure class</span>`
      : '';
    html += `<div class="card bank-card">
      <h3><a href="bank-${slugify(bank)}.html" style="color:inherit;text-decoration:none;">${bank}</a></h3>
      <div class="book-label">${comp.kind==='stage' ? catNames.map(shortCategoryName).join(' + ') : ''}${flag}</div>
      <div class="mini-chart-wrap" data-chart="loan" data-bank="${bank}"><canvas></canvas></div>
      ${coverageNplChipsHtml(data[bank], year || latestCoverageYear(data[bank]))}
    </div>`;
  });
  html += `</div>
    <div class="legend-row">
      <span><span class="sw" style="background:${STAGE_COLOR.stage_1}"></span>Stage 1 (performing)</span>
      <span><span class="sw" style="background:${STAGE_COLOR.stage_2}"></span>Stage 2 (watch)</span>
      <span><span class="sw" style="background:${STAGE_COLOR.stage_3}"></span>Stage 3 (default)</span>
      <span style="color:var(--ink-faint)">— exposure-class bars use a different (categorical) palette, hover each segment for its label</span>
    </div>
  ` + blockClose();

  html += blockOpen('RWA density', `${rwaBanks.length} of ${banks.length} banks disclose an RWA breakdown — Total RWAs ÷ Total assets, and RWA by category (latest year)`);
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
  html += `</div>` + blockClose();

  html += blockOpen('Capital &amp; liquidity (Pillar 3)', 'full trend');
  html += `<h3 style="font-family:var(--font-serif);font-size:14px;margin:0 0 10px;">Capital ratios <span style="font-weight:400;color:var(--ink-faint);font-size:12px;">(${capitalBanks.length} of ${banks.length} banks)</span></h3>`;
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
    </div>`;
  html += `<h3 style="font-family:var(--font-serif);font-size:14px;margin:24px 0 10px;">Liquidity ratios <span style="font-weight:400;color:var(--ink-faint);font-size:12px;">(${liquidityBanks.length} of ${banks.length} banks)</span></h3>`;
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
    </div>
  ` + blockClose();

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

  document.getElementById('app').innerHTML = html;
  initCollapsibleBlocks();

  document.querySelectorAll('[data-chart="capital"]').forEach(el => {
    const bank = el.dataset.bank, cap = data[bank].capital_deployment, year = latestChartableCapitalYear(cap);
    const canvas = el.querySelector('canvas');
    const ok = year && capitalCompositionMiniChart(canvas, cap[year]);
    if (!ok) el.outerHTML = '<div class="empty-note">No capital-deployment data disclosed for this bank.</div>';
  });
  document.querySelectorAll('[data-chart="loan"]').forEach(el => {
    const bank = el.dataset.bank, comp = data[bank].loan_composition, year = latestChartableLoanYear(comp);
    const canvas = el.querySelector('canvas');
    let ok = false;
    if (year) ok = comp.kind === 'stage' ? stageCompositionMiniChart(canvas, comp.years[year]) : exposureClassMiniChart(canvas, comp.years[year]);
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

  html += `<div class="block"><div class="block-head"><h2>Statement of Changes in Equity</h2><span class="hint">${bank}, chronological roll-forward</span></div>`;
  html += `<div class="card">${equityChangesTableHtml(bankData.equity_changes)}</div></div>`;

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
  if (cashFlowYears.length) cashFlowChart(document.querySelector('#drilldown-cashflow-chart canvas'), bankData.cash_flow);

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
