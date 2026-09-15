"""Build the standalone PDF companion for the client deliverable (IN-053).

Full rewrite (2026-09-05): previously a hand-rolled, stdlib-only PDF writer
drawing every chart in raw PDF syntax, sourced from in011_deliverables.py's
older single-file dashboard. Per the grilled decisions in
wayfinder/insights/tickets/IN-053.md, this now MIRRORS deliverable/
comparison.html's own sections (loan concentration & quality, capital/
liquidity/RWA incl. peer clusters, balance sheet & P&L, parent groupings,
most extreme, regulatory headroom trajectory) - a stand-alone document, not
a summarized executive brief - rendered via headless Chromium (Playwright)
printing a dedicated print-only HTML page, instead of re-implementing every
chart type by hand. in011_deliverables.py itself is untouched and still
callable standalone (kept, per that ticket's decision, even though nothing
here calls it any more).

Playwright is this pipeline's first real external dependency - see
scripts/insights/requirements.txt. The per-bank build_<bank>.py scripts
elsewhere in the repo stay dependency-free, per CLAUDE.md; only this
pipeline (scripts/insights/) needs a real manifest.

One-time setup:
    python3 -m pip install --user -r scripts/insights/requirements.txt
    python3 -m playwright install chromium

Run:
    python3 scripts/insights/build_in006_pdf.py
    python3 scripts/insights/build_in006_pdf.py --db path/to.db --out path/to.pdf
"""

import argparse
import html
import json
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

import build_deliverable as bd
from analysis_queries import AnalysisQueries

ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_DB = ROOT / "research" / "insights.db"
DEFAULT_OUT = ROOT / "wayfinder" / "insights" / "deliverable" / "uk_bank_insights.pdf"

PRINT_HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>UK bank Pillar 3 &amp; financial insights</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,500;8..60,600;8..60,700&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<link rel="stylesheet" href="deliverable_shared.css">
<style>
  /* Print-only overrides. Every .block/.subsection in comparison.html
     already renders expanded by default (blockOpen/subOpen don't start
     collapsed - see deliverable_shared.js), so nothing here needs to force
     content open; this just removes interactive-only chrome (sidebar,
     bank search) that has no meaning on paper and sets sane page breaks. */
  body{background:#fff;}
  aside.sidebar,.bank-search-wrap{display:none!important;}
  main{margin:0 auto;max-width:900px;padding:24px 32px 60px;}
  details>summary{cursor:default;}
  .block{break-inside:avoid-page;}
  .print-cover{padding:140px 0 60px;text-align:center;}
  .print-cover h1{font-family:'Source Serif 4',serif;font-size:32px;margin:0 0 10px;}
  .print-cover .sub{color:var(--ink-faint);font-size:14px;}
  .print-section-break{page-break-before:always;padding-top:20px;}
  .group-summary-card{border:1px solid var(--ink-faint);border-radius:8px;padding:16px 20px;margin-bottom:16px;break-inside:avoid;}
  .group-summary-card h3{margin:0 0 4px;font-size:16px;}
  .group-summary-card .roster{color:var(--ink-faint);font-size:12.5px;margin-bottom:10px;}
  .group-summary-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:8px 24px;font-size:12.5px;margin:0;}
  .group-summary-grid dt{color:var(--ink-faint);margin:0;}
  .group-summary-grid dd{margin:0 0 6px;font-variant-numeric:tabular-nums;}
  /* comparison.html's tables are sized for a 1180px-wide live main column
     (with a sidebar eating further space) - A4 portrait's printable width
     is far narrower, so wide tables (headroom's 8 columns especially) were
     clipped at the page edge at the live page's font/padding. Compact
     print-only sizing, not a redesign. */
  .bank-table th{font-size:8.5px;padding:5px 6px;}
  .bank-table td{font-size:8.5px;padding:5px 6px;}
  .bank-table a{font-size:8.5px!important;}
  table{table-layout:auto;width:100%;}
</style>
<script src="chart.umd.min.js"></script>
</head>
<body>
<div class="print-cover">
  <h1>UK bank Pillar 3 &amp; financial insights</h1>
  <div class="sub">__N_BANKS__ banks &middot; snapshot __SNAPSHOT_DATE__</div>
</div>
<main>
  <div id="page-sub" style="display:none;"></div>
  <div id="app"></div>
  <div class="print-section-break">
    <h2>Parent group summaries</h2>
    <div class="sub" style="margin-bottom:16px;">Condensed profile for each of the __N_GROUPS__ multi-entity groups in this dataset with comparable members - full per-member charts and the ultimate-parent lookups live on each group's own page in the HTML deliverable.</div>
    __GROUP_SUMMARIES_HTML__
  </div>
</main>
<script id="data" type="application/json">__DATA_JSON__</script>
<script id="trends-data" type="application/json">__TRENDS_JSON__</script>
<script id="outliers-data" type="application/json">__OUTLIERS_JSON__</script>
<script id="parent-groups-data" type="application/json">__PARENT_GROUPS_JSON__</script>
<script id="efficiency-data" type="application/json">__EFFICIENCY_JSON__</script>
<script id="bubbles-data" type="application/json">__BUBBLES_JSON__</script>
<script id="clusters-data" type="application/json">__CLUSTERS_JSON__</script>
<script src="chartjs-chart-sankey.min.js"></script>
<script src="chartjs-chart-boxplot.min.js"></script>
<script src="deliverable_shared.js"></script>
<script>
const DATA = JSON.parse(document.getElementById('data').textContent);
const TRENDS = JSON.parse(document.getElementById('trends-data').textContent);
const OUTLIERS = JSON.parse(document.getElementById('outliers-data').textContent);
const PARENT_GROUPS = JSON.parse(document.getElementById('parent-groups-data').textContent);
const EFFICIENCY = JSON.parse(document.getElementById('efficiency-data').textContent);
const BUBBLES = JSON.parse(document.getElementById('bubbles-data').textContent);
const CLUSTERS = JSON.parse(document.getElementById('clusters-data').textContent);
renderComparisonPage(DATA, Object.keys(DATA), TRENDS, OUTLIERS, PARENT_GROUPS, EFFICIENCY, BUBBLES, CLUSTERS);
window.__printReady = true;
</script>
</body>
</html>
"""


def _snapshot_date_label(db_path):
    """Human-readable snapshot date from the database's own refresh
    metadata, not a hardcoded literal - see the old version of this
    function's docstring (git history) for why: the cover page previously
    said "29 August 2026" no matter how many times the PDF was regenerated
    afterward."""
    built_at = AnalysisQueries(db_path).refresh_metadata().get("metrics_built_at")
    if built_at:
        try:
            when = datetime.fromisoformat(built_at)
        except ValueError:
            when = datetime.now(timezone.utc)
    else:
        when = datetime.now(timezone.utc)
    return f"{when.day} {when.strftime('%B %Y')}"


def _money(v):
    """Every absolute-£ figure in group_meta (total_pnl_by_year,
    total_assets_by_year, total_income_breakdown_by_year) is already scaled
    to actual GBP by curate_total_assets()/curate_income_pnl() - same
    convention as deliverable_shared.js's fmtK(), which also applies no
    further scaling, just formatting."""
    if v is None:
        return "—"
    sign = "-" if v < 0 else ""
    return f"{sign}£{abs(round(v)):,}"


def _latest(d):
    if not d:
        return None, None
    y = sorted(d)[-1]
    return y, d[y]


def condensed_group_summary_html(group, meta):
    """A short, plain-HTML profile per multi-entity group - headline
    figures and combined composition, deliberately NOT the full per-member
    chart grid each group's own live page has (per IN-053's grilled scope:
    condensed, not a like-for-like copy of write_group_page())."""
    roster = ", ".join(m["bank"] for m in meta["members"])
    pnl_year, pnl_val = _latest(meta["total_pnl_by_year"])
    assets_year, assets_val = _latest(meta["total_assets_by_year"])
    asset_year, asset_comp = _latest(meta["group_asset_composition"])
    liab_year, liab_comp = _latest(meta["group_liability_composition"])
    income_year, income_comp = _latest(meta["total_income_breakdown_by_year"])

    rows = []
    if pnl_val is not None:
        rows.append(("Combined profit for the year", f"{_money(pnl_val)} (FY{pnl_year})"))
    if assets_val is not None:
        rows.append(("Combined total assets", f"{_money(assets_val)} (FY{assets_year})"))
    if asset_comp:
        parts = ", ".join(f"{label}: {asset_comp[key]:.1f}%" for label, key in [
            ("Customer loans", "loans_pct_of_assets"),
            ("Cash & central bank", "cash_pct_of_assets"),
            ("Treasury investments", "treasury_investments_pct_of_assets"),
            ("Other", "other"),
        ])
        rows.append((f"Combined asset mix (FY{asset_year})", parts))
    if liab_comp:
        parts = ", ".join(f"{label}: {liab_comp[key]:.1f}%" for label, key in [
            ("Customer deposits", "customer_deposits_pct"),
            ("Bank deposits", "bank_deposits_pct"),
            ("Wholesale funding", "wholesale_funding_pct"),
            ("Other", "other_pct"),
        ])
        rows.append((f"Combined liability mix (FY{liab_year})", parts))
    if income_comp:
        parts = ", ".join(f"{cat}: {_money(v)}" for cat, v in income_comp.items())
        rows.append((f"Combined income mix (FY{income_year})", parts))

    dl_html = "".join(
        f"<dt>{html.escape(k)}</dt><dd>{html.escape(v)}</dd>" for k, v in rows
    )
    return f"""<div class="group-summary-card">
  <h3>{html.escape(group)}</h3>
  <div class="roster">{len(meta['members'])} members: {html.escape(roster)}</div>
  <dl class="group-summary-grid">{dl_html}</dl>
</div>"""


def assemble_print_payload(db_path):
    """Mirrors build_deliverable.main()'s data assembly for comparison.html,
    without writing any of the per-bank/per-group HTML pages this PDF
    doesn't need."""
    bd.DB_PATH = Path(db_path)
    data = bd.curate()
    parent_groups = bd.curate_comparison_parent_groups(data)
    trends = bd.curate_comparison_trends()
    outliers = bd.curate_comparison_outliers()
    efficiency = bd.curate_comparison_efficiency(data)
    bubbles = bd.curate_comparison_bubbles(data, parent_groups)
    clusters = bd.curate_comparison_clusters()
    return data, parent_groups, trends, outliers, efficiency, bubbles, clusters


def write_print_html(work_dir, db_path):
    data, parent_groups, trends, outliers, efficiency, bubbles, clusters = assemble_print_payload(db_path)

    group_meta = parent_groups["group_meta"]
    group_summaries_html = "".join(
        condensed_group_summary_html(group, meta) for group, meta in sorted(group_meta.items())
    )

    html_out = PRINT_HEAD
    for token, value in [
        ("__N_BANKS__", str(len(data))),
        ("__N_GROUPS__", str(len(group_meta))),
        ("__SNAPSHOT_DATE__", _snapshot_date_label(db_path)),
        ("__GROUP_SUMMARIES_HTML__", group_summaries_html),
        ("__DATA_JSON__", json.dumps(data)),
        ("__TRENDS_JSON__", json.dumps(trends)),
        ("__OUTLIERS_JSON__", json.dumps(outliers)),
        ("__PARENT_GROUPS_JSON__", json.dumps(parent_groups)),
        ("__EFFICIENCY_JSON__", json.dumps(efficiency)),
        ("__BUBBLES_JSON__", json.dumps(bubbles)),
        ("__CLUSTERS_JSON__", json.dumps(clusters)),
    ]:
        html_out = html_out.replace(token, value)
    (work_dir / "print_report.html").write_text(html_out)

    shutil.copy(ROOT / "scripts" / "insights" / "deliverable_shared.css", work_dir / "deliverable_shared.css")
    shutil.copy(ROOT / "scripts" / "insights" / "deliverable_shared.js", work_dir / "deliverable_shared.js")
    shutil.copy(ROOT / "vendor" / "chartjs" / "chart.umd.min.js", work_dir / "chart.umd.min.js")
    shutil.copy(ROOT / "vendor" / "chartjs-chart-sankey" / "chartjs-chart-sankey.min.js", work_dir / "chartjs-chart-sankey.min.js")
    shutil.copy(ROOT / "vendor" / "chartjs-chart-boxplot" / "chartjs-chart-boxplot.min.js", work_dir / "chartjs-chart-boxplot.min.js")

    return work_dir / "print_report.html", len(data)


def render_pdf(html_path, out_path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(html_path.as_uri())
        page.wait_for_function("window.__printReady === true", timeout=30000)
        # Charts mount synchronously inside renderComparisonPage() (Chart.js
        # draws to canvas immediately, no promise/animation-frame delay in
        # this codebase's chart-init functions), so __printReady already
        # implies the canvases are painted - this is just a small safety
        # margin for webfont/layout settle before the print snapshot.
        page.wait_for_timeout(300)
        page.pdf(
            path=str(out_path),
            format="A4",
            print_background=True,
            margin={"top": "14mm", "bottom": "14mm", "left": "12mm", "right": "12mm"},
        )
        browser.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=DEFAULT_DB, help="SQLite source-of-truth database")
    parser.add_argument("--out", default=DEFAULT_OUT, help="PDF output path")
    args = parser.parse_args()
    db_path = Path(args.db)
    out_path = Path(args.out)

    with tempfile.TemporaryDirectory(prefix="katalysis-pdf-") as tmp:
        html_path, n_banks = write_print_html(Path(tmp), db_path)
        render_pdf(html_path, out_path)

    print(f"Wrote {out_path} ({out_path.stat().st_size} bytes, {n_banks} banks)")


if __name__ == "__main__":
    main()
