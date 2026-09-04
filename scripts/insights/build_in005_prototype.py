"""Build the throwaway, single-file IN-005 client-deliverable prototype."""

import csv
import json
import os
import re
import argparse
from pathlib import Path

from analyze_trends import METRICS, extract, load_rows, pairwise_counts
import build_insights_db
from in011_deliverables import build_in011_payload, render_html_analysis
from chart_contract import LOCAL_CHART_RUNTIME, load_chartjs_bundle


ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
CLUSTERS = os.path.join(ROOT, "research", "bank_clusters.csv")
OUTPUT = os.path.join(ROOT, "wayfinder", "insights", "deliverable", "uk_bank_insights.html")
DEFAULT_DB = os.path.join(ROOT, "research", "insights.db")


def load_clusters(path=CLUSTERS):
    return build_insights_db.load_cluster_rows(path)


def normalize_name(value):
    return re.sub(r"[^A-Z0-9]", "", value.upper())


CLUSTER_LABELS = {"0": "Lower capital-ratio cluster", "1": "Higher capital-ratio cluster"}
CENTROIDS_PATH = os.path.join(ROOT, "research", "bank_clusters_centroids.csv")
CHART_CSS_PATH = Path(__file__).with_name("dashboard.css")

# validate_cluster_inputs lives in build_insights_db.py now - shared with
# build_in006_pdf.py so both deliverable generators get the same staleness
# guard rather than one having it and the other silently lacking it.
validate_cluster_inputs = build_insights_db.validate_cluster_inputs


def compute_clusters_summary(centroids_path=CENTROIDS_PATH):
    """Replaces the previously-hardcoded {size, cet1, tier1, total} literals
    with values read from research/bank_clusters_centroids.csv - IN-003's
    OWN computed centroids, not a naive re-derivation. This matters: a
    plain mean of each cluster's raw CET1 Ratio_value column (the first,
    wrong version of this fix) gets dragged far off by known extreme
    outliers like Afin Bank's 418.5% CET1 year, which cluster_banks.py's
    winsorized/robust-scaled centroid calculation deliberately guards
    against (see its own module docstring). Reading the centroid IN-003
    already computed correctly, rather than re-deriving a different
    (worse) number here, is the right fix, not just "any computed number
    instead of a hardcoded one"."""
    with open(centroids_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return [
        {
            "label": CLUSTER_LABELS.get(row["cluster_id"], f"Cluster {row['cluster_id']}"),
            "size": int(row["cluster_size"]),
            "cet1": round(float(row["CET1 Ratio"]), 2),
            "tier1": round(float(row["Tier 1 Ratio"]), 2),
            "total": round(float(row["Total Capital Ratio"]), 2),
        }
        for row in rows
    ]


def compute_trends_payload(trend_series):
    """Replaces the previously-hardcoded, and never actually read by the
    page's own JS (D.trends was unused - confirmed before removing the
    literal version), list of {period, metric, down, up, n} dicts with one
    computed fresh via analyze_trends.pairwise_counts() for every metric
    across every adjacent fiscal-year pair currently present in the data."""
    years = [2021, 2022, 2023, 2024, 2025]
    trends = []
    for metric, series in trend_series.items():
        numeric_series = {frn: {int(y): v for y, v in years_map.items()} for frn, years_map in series.items()}
        for start, end in zip(years, years[1:]):
            c = pairwise_counts(numeric_series, start, end)
            if c["n"] == 0:
                continue
            trends.append({
                "period": f"FY{start}→FY{end}", "metric": metric, "label": metric,
                "down": c["down"], "up": c["up"], "n": c["n"],
            })
    return trends


# Curated editorial verdicts ("Aligned"/"Mixed"/"Not comparable") and the
# supporting note for each multi-entity parent group - these are genuine
# analytical judgments from IN-004's reviewed trend work, not something a
# script can safely re-derive, so they stay hand-authored. What they must
# NOT do is hardcode which/how-many entities exist per group - that's pure
# data, live-loaded from parent_group_lookup below via multi_entity_groups().
# Keyed by the ultimate_group text exactly as it appears in
# research/bank_parent_groups.md's lookup table.
GROUP_VERDICTS = {
    "HSBC group": {"name": "HSBC", "capital": "Aligned", "cash": "Mixed",
                   "note": "CET1 down in all 3 comparable entities."},
    "NatWest group": {"name": "NatWest", "capital": "Aligned", "cash": "Mixed",
                       "note": "CET1 and Total Capital down in all 3."},
    "Lloyds Banking Group": {"name": "Lloyds", "capital": "Mixed", "cash": "Mixed",
                              "note": "Entity-level divergence is material."},
    "Banco Santander S.A.": {"name": "Santander", "capital": "Not comparable", "cash": "Mixed",
                              "note": "Different entity series and cash-flow directions."},
    "UBS group (current)": {"name": "UBS / Credit Suisse", "capital": "Not comparable", "cash": "Aligned",
                             "note": "Acquisition/wind-down transition caveat."},
    "JPMorgan Chase group": {"name": "JPMorgan", "capital": "Not comparable", "cash": "Not comparable",
                              "note": "Insufficient FY21→FY22 pair coverage."},
}


def compute_groups_payload(db_path):
    """Builds payload["groups"] with LIVE entities/members from
    parent_group_lookup (via multi_entity_groups()), keeping only the
    editorial capital/cash/note verdict hardcoded (see GROUP_VERDICTS
    above). A multi-entity group with no curated verdict yet is reported to
    stdout rather than silently included with a fabricated verdict or
    silently dropped - a future session needs to notice and curate it."""
    from analysis_queries import AnalysisQueries
    groups = AnalysisQueries(db_path).groups()
    multi = build_insights_db.multi_entity_groups(groups)
    payload_groups = []
    for ultimate_group, members in multi:
        verdict = GROUP_VERDICTS.get(ultimate_group)
        if verdict is None:
            print(f"  !! multi-entity group {ultimate_group!r} ({len(members)} entities) has no "
                  f"curated verdict in GROUP_VERDICTS - omitted from the deliverable, not guessed")
            continue
        payload_groups.append({
            "name": verdict["name"],
            "entities": len(members),
            "capital": verdict["capital"],
            "cash": verdict["cash"],
            "note": verdict["note"],
            "members": [bank_name for _frn, bank_name in members],
            "member_frns": [frn for frn, _bank_name in members],
        })
    return payload_groups


def build_key_takeaways_html(trend_series):
    """Builds the "Key takeaways" HTML paragraphs FROM CURRENT DATABASE
    VALUES - see build_in006_pdf.py's headline_signal_lines() for the PDF
    equivalent of this same fix. Both read the same trend_series/
    pairwise_counts, so the HTML and PDF deliverables can never quietly
    report different numbers for the same underlying data."""
    def cnt(metric, start, end):
        series = {frn: {int(y): v for y, v in years_map.items()} for frn, years_map in trend_series.get(metric, {}).items()}
        return pairwise_counts(series, start, end)

    rwa_23, rwa_24 = cnt("RWA", 2022, 2023), cnt("RWA", 2023, 2024)
    cet1_23, cet1_24, cet1_25 = cnt("CET1 ratio", 2022, 2023), cnt("CET1 ratio", 2023, 2024), cnt("CET1 ratio", 2024, 2025)
    ocf_24, ocf_25 = cnt("Operating cash flow", 2023, 2024), cnt("Operating cash flow", 2024, 2025)
    return (
        '<article id="takeaways" class="card"><h2>Key takeaways</h2>'
        '<p class="sub">Distinct signals from the available year-on-year comparisons.</p>'
        f'<p><strong>Risk-weighted assets generally expanded:</strong> RWA increased for {rwa_23["up"]} of {rwa_23["n"]} '
        f'comparable entities from FY2022 to FY2023 and {rwa_24["up"]} of {rwa_24["n"]} from FY2023 to FY2024. '
        'This is an amount, not a capital-ratio percentage.</p>'
        f'<p><strong>Capital ratios turned more defensive after FY2022→FY2023:</strong> CET1 increased for {cet1_23["up"]} of '
        f'{cet1_23["n"]} entities in FY2022→FY2023, but declined for {cet1_24["down"]} of {cet1_24["n"]} in FY2023→FY2024 '
        f'and {cet1_25["down"]} of {cet1_25["n"]} in FY2024→FY2025.</p>'
        f'<p><strong>Operating cash flow was cyclical:</strong> {ocf_24["up"]} of {ocf_24["n"]} comparable entities improved '
        f'in FY2023→FY2024, followed by declines for {ocf_25["down"]} of {ocf_25["n"]} in FY2024→FY2025.</p></article>'
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=DEFAULT_DB, help="SQLite source-of-truth database")
    parser.add_argument("--out", default=OUTPUT, help="HTML output path")
    parser.add_argument("--clusters", default=CLUSTERS, help="derived cluster CSV")
    parser.add_argument("--centroids", default=CENTROIDS_PATH, help="derived cluster centroids CSV")
    parser.add_argument("--headline", default="Capital, liquidity and group movement",
                        help="headline shown at the top of the HTML deliverable")
    args = parser.parse_args()
    banks = load_clusters(args.clusters)
    validate_cluster_inputs(args.db, banks, args.clusters, args.centroids)
    in011 = build_in011_payload(args.db)
    bank_by_name = {normalize_name(row["bank"]): row for row in banks}
    bank_by_frn = {row["frn"]: row for row in banks}
    metric_specs = dict(METRICS)
    metric_specs["MREL ratio"] = ("MREL Ratio", re.compile(r"MREL.*ratio|ratio.*MREL", re.I), ())
    metric_specs["RWA"] = ("Total RWAs", re.compile(r"total|overall", re.I), ("credit risk", "market risk", "operational risk", "crwa", "mrwa", "orwa"))
    trend_series = {}
    from analysis_queries import AnalysisQueries
    metric_rows = AnalysisQueries(args.db).observations()
    for metric, spec in metric_specs.items():
        values, _ = extract(metric_rows, metric, spec)
        trend_series[metric] = {frn: {str(fiscal_year): value for fiscal_year, value in series.items()} for frn, series in values.items()}
    payload = {
        "banks": [
            {
                "name": row["bank"].title(),
                "cluster": row["cluster_id"],
                "insufficient": row["insufficient_data"] == "1",
                "cet1": None if not row["CET1 Ratio_value"] else float(row["CET1 Ratio_value"]),
                "leverage": None if not row["Leverage Ratio_value"] else float(row["Leverage Ratio_value"]),
            }
            for row in banks
        ],
        "trend_series": trend_series,
        "clusters": compute_clusters_summary(args.centroids),
        "trends": compute_trends_payload(trend_series),
        "groups": compute_groups_payload(args.db),
        "in011": in011,
    }
    for group in payload["groups"]:
        group["member_data"] = []
        for frn, name in zip(group.pop("member_frns"), group["members"]):
            # Join by FRN, not by fuzzy name matching: parent_group_lookup's
            # bank_name ("Santander UK") and the cluster CSV's filename-
            # derived name ("SANTANDER") are different legitimate spellings
            # for the same entity - name-normalization silently dropped
            # exactly these two members before this fix (see
            # multi_entity_groups()'s docstring for the full story).
            row = bank_by_frn.get(frn)
            if row:
                group["member_data"].append({
                    "name": name.title(),
                    "cet1": row["CET1 Ratio_value"] if row["CET1 Ratio_imputed"] == "0" else "",
                    "leverage": row["Leverage Ratio_value"] if row["Leverage Ratio_imputed"] == "0" else "",
                    "tier1": row["Tier 1 Ratio_value"] if row["Tier 1 Ratio_imputed"] == "0" else "",
                    "total": row["Total Capital Ratio_value"] if row["Total Capital Ratio_imputed"] == "0" else "",
                    "lcr": row["LCR_value"] if row["LCR_imputed"] == "0" else "",
                    "nsfr": row["NSFR_value"] if row["NSFR_imputed"] == "0" else "",
                    "mrel": row["MREL Ratio_value"] if row["MREL Ratio_imputed"] == "0" else "",
                })
    key_takeaways_html = build_key_takeaways_html(trend_series)
    analysis_html = render_html_analysis(in011)
    # `in011["in025"]["trace"]` is a full per-observation raw record dump
    # (14k+ rows, ~32MB) that render_html_analysis() above already consumed
    # to build the static evidence-quality table baked into `analysis_html`.
    # No client-side JS ever reads `D.in011.in025.trace` - only the small
    # `trace_completeness` summary is - so it must be dropped from `in011`
    # (the same object referenced by `payload["in011"]`) before the JSON
    # dump below, not kept around just because it was needed a moment ago.
    in011["in025"].pop("trace", None)
    # `in011["in016"]` (distributions/absolute_distributions/rank_movement/
    # group_benchmark_coverage across every metric, year and basis, ~12.7MB)
    # is likewise only ever read server-side - render_html_analysis() above
    # already used it (via the `in016` argument threaded through to
    # render_html_distribution_visuals()) to draw the static SVG distribution
    # charts baked into `analysis_html`. No client-side JS references
    # `D.in011.in016` at all, so it doesn't belong in the client payload
    # either - same reasoning as the `in025["trace"]` drop just above.
    in011.pop("in016", None)
    # Escape a literal "</" so a hand-transcribed bank name/source-note/
    # citation string can never prematurely close this <script> tag and
    # corrupt the rest of the page - same pattern already used for in022's
    # smaller payload in in011_deliverables.py. Currently safe with the live
    # dataset only by chance (no such substring happens to appear today).
    data = json.dumps(payload, separators=(",", ":")).replace("</", "<\\/")
    html = (TEMPLATE.replace("__DATA__", data)
            .replace("__HEADLINE__", escape_html(args.headline))
            .replace("__KEY_TAKEAWAYS__", key_takeaways_html)
            .replace("__IN011_ANALYSIS__", analysis_html))
    html = decorate_dashboard_html(html)
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as handle:
        handle.write(html)
    print(f"Wrote {args.out} from {len(banks)} cluster rows")


def escape_html(value):
    return (str(value).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#39;"))


def decorate_dashboard_html(html):
    """Apply the dashboard shell to the existing generated page seam."""
    css = '''<style>.dashboard-shell{display:grid;grid-template-columns:228px minmax(0,1fr);min-height:100vh}.dashboard-sidebar{background:#132b3f;color:#dce9ef;padding:24px 16px;position:sticky;top:0;height:100vh}.dashboard-brand{font:700 20px Georgia,serif;color:#fff;padding:0 12px 24px;border-bottom:1px solid #ffffff2b}.dashboard-brand small{display:block;font:600 10px system-ui,sans-serif;letter-spacing:.12em;text-transform:uppercase;color:#9dc5d4;margin-bottom:6px}.dashboard-nav{display:grid;gap:5px;margin-top:22px}.dashboard-nav a{color:#c8dce5;text-decoration:none;border-radius:6px;padding:9px 12px;font-size:13px}.dashboard-nav a:hover,.dashboard-nav a:focus{background:#ffffff18;color:#fff;outline:2px solid #8cc8d5;outline-offset:1px}.dashboard-context{border-top:1px solid #ffffff2b;margin:28px 12px 0;padding-top:16px;color:#9eb7c3;font-size:11px}.dashboard-kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:0 0 20px}.kpi-card{background:#fff;border:1px solid var(--line);border-radius:8px;padding:14px 16px;box-shadow:0 2px 8px #132b3f0d}.kpi-label{color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.07em}.kpi-value{display:block;color:#132b3f;font-size:25px;font-weight:750;line-height:1.15;margin:4px 0}.kpi-note{color:var(--muted);font-size:11px}.dashboard-section{scroll-margin-top:18px}.section-heading{display:flex;align-items:end;justify-content:space-between;gap:16px;margin:0 0 12px}.section-heading h2{margin:0}.section-heading p{margin:0;color:var(--muted);font-size:12px}.in011-analysis{scroll-margin-top:18px}.dashboard-shell button{cursor:pointer}.dashboard-shell button:focus,.dashboard-shell select:focus,.dashboard-shell input:focus{outline:2px solid #2f8f9d;outline-offset:1px}@media(max-width:920px){.dashboard-shell{grid-template-columns:185px minmax(0,1fr)}main{padding:22px 18px 50px}.dashboard-kpis{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:700px){.dashboard-shell{display:block}.dashboard-sidebar{position:static;height:auto;padding:14px 16px}.dashboard-brand{display:inline-block;border:0;padding:0}.dashboard-nav{display:flex;overflow-x:auto;margin-top:12px}.dashboard-nav a{white-space:nowrap}.dashboard-context{display:none}}</style>'''
    css += '<style>.dashboard-watchlist{background:#fff;border:1px solid var(--line);border-left:4px solid var(--gold);border-radius:8px;padding:14px 16px;margin-bottom:18px}.dashboard-watchlist h2{font-size:18px}.watchlist-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}.watch-item{border:1px solid var(--line);border-radius:6px;padding:9px;background:#fffaf0}.watch-item button,.bank-link{border:0;background:none;color:var(--blue);font:inherit;font-weight:700;padding:0;text-align:left;text-decoration:underline;cursor:pointer}.watch-reason{display:block;color:var(--muted);font-size:11px;margin-top:3px}.freshness-badge{display:inline-block;color:#285d2d;background:#dcebdc;border-radius:999px;padding:3px 8px;font-size:11px;font-weight:650}.bank-drillthrough{position:fixed;z-index:20;right:0;top:0;width:min(440px,92vw);height:100vh;overflow:auto;background:#fff;box-shadow:-8px 0 24px #132b3f33;padding:24px;transform:translateX(105%);transition:transform .2s ease}.bank-drillthrough.is-open{transform:translateX(0)}.bank-drillthrough-close{float:right;border:1px solid var(--line);background:#fff;border-radius:5px;padding:4px 8px}.drill-table{margin-top:14px}.global-search{margin:18px 0}.global-search input{width:100%;font:inherit;border:1px solid #557789;border-radius:5px;padding:8px 10px;background:#fff}.dashboard-shell .in025-filter-row,.dashboard-shell .in024-filter-row,.dashboard-shell .coverage-row{scroll-margin-top:20px}.kpi-sparkline{display:block;width:100%;height:24px;margin-top:4px}@media(max-width:920px){.watchlist-grid{grid-template-columns:1fr 1fr}}@media(max-width:700px){.watchlist-grid{grid-template-columns:1fr}}</style>'
    css += '''<style>
/* Compact dashboard system; analytical colour is reserved for status. */
:root{--paper:#f3f6f8;--card:#fff;--ink:#172b3a;--muted:#60717d;--blue:#1f5f8b;--teal:#2f8f9d;--gold:#b87916;--red:#b94c42;--line:#d8e1e7}
body{background:var(--paper);color:var(--ink);font-size:14px}
main{max-width:1440px;padding:24px 32px 56px}
h1,h2,h3{font-family:system-ui,-apple-system,"Segoe UI",sans-serif;letter-spacing:-.015em}
h1{font-size:30px;line-height:1.15;margin-bottom:6px}h2{font-size:19px}h3{font-size:14px}
header{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:20px 22px;margin-bottom:16px;box-shadow:0 1px 3px #1732470a}
.lede{max-width:900px;font-size:13px}
.dashboard-sidebar{padding:20px 14px;background:#102d43}.dashboard-brand{font-family:system-ui,-apple-system,"Segoe UI",sans-serif;font-size:17px;padding:0 10px 18px}.dashboard-nav{gap:2px;margin-top:16px}.dashboard-nav a{padding:8px 10px;font-size:12px}.dashboard-nav a[aria-current="page"],.dashboard-nav a:hover{background:#ffffff1c}
.dashboard-kpis{grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;margin-bottom:12px}.kpi-card{border-radius:6px;padding:12px 14px;box-shadow:none}.kpi-label{font-size:10px}.kpi-value{font-size:23px}
.dashboard-watchlist{border-left-width:3px;border-radius:6px;padding:12px 14px;margin-bottom:12px}.dashboard-watchlist h2{margin-bottom:2px}.watchlist-grid{gap:6px}.watch-item{border-radius:4px;padding:8px;background:#fffdf8}
.in024-chart-layout{display:block;width:100%;align-items:center}.in024-chart-layout>.in024-bank-list{display:none}.in024-shared-bank-list{max-height:220px;overflow:auto;display:grid;grid-template-columns:repeat(3,minmax(160px,1fr));gap:4px;border:1px solid var(--line);padding:8px;font-size:12px}.in024-shared-controls{margin:10px 0 14px}.in024-shared-controls .controls{margin:0 0 8px}.in024-shared-controls button{border:1px solid var(--line);border-radius:4px;background:#fff;padding:5px 8px;font:inherit;font-size:12px}.in024-shared-controls label{display:block}
.in024-chart-stage{width:100%;height:330px;display:flex;flex-direction:column;align-items:center}.in024-chart-stage canvas{display:block!important;width:100%!important;max-width:100%;align-self:stretch;height:280px!important}
.appendix-panel{border:1px solid var(--line);border-radius:5px;background:#f8fafb;margin:12px 0;padding:0 10px}.appendix-panel>summary{cursor:pointer;padding:10px 2px;color:var(--blue);font-weight:700;font-size:13px}.appendix-content{padding:0 2px 10px}.appendix-content table{margin-top:4px}
.grid{gap:12px;margin-bottom:18px}.card{border-radius:6px;padding:15px;box-shadow:0 1px 3px #1732470a}.sub{font-size:12px;margin-bottom:10px}
.section-heading{margin-bottom:9px}.section-heading p{font-size:11px}.pill{border-radius:4px}
@media(max-width:920px){main{padding:18px 18px 44px}.dashboard-kpis{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:700px){main{padding:14px 12px 36px}header{padding:16px}.dashboard-kpis{gap:7px}.kpi-card{padding:10px}.kpi-value{font-size:20px}}
</style>'''
    # `navigation` is the single, final sidebar markup - it already carries
    # the full 9-link nav plus the global-search box. A second `html.replace`
    # used to try to "upgrade" an old 4-link nav (with a "Deep analysis"
    # label) into this 9-link version after the fact, but that old 4-link nav
    # was never actually inserted anywhere (TEMPLATE's own stale duplicate of
    # it, which pre-empted this whole function, has been removed - see the
    # note below) - so that second replace always matched nothing and the
    # global-search box never appeared. Build the final navigation once here
    # instead of patching it in a separate dead step.
    navigation = ('<aside class="dashboard-sidebar"><div class="dashboard-brand"><small>Analytical pack</small>UK Bank Insights</div>'
                  '<nav class="dashboard-nav" aria-label="Dashboard navigation"><a href="#overview">Overview</a><a href="#trend-signals">Trends</a>'
                  '<a href="#parent-groups">Parent groups</a><a href="#analysis">Coverage</a><a href="#ratio-decomposition">Decomposition</a>'
                  '<a href="#distribution-visuals">Distributions</a><a href="#trajectories">Trajectories</a><a href="#quality">Data quality</a>'
                  '<a href="#headroom">Headroom</a><a href="#outliers">Outliers</a></nav>'
                  '<div class="global-search"><label for="global-bank-search">Find a bank</label>'
                  '<input id="global-bank-search" type="search" placeholder="Bank, metric, or FRN"></div>'
                  '<div class="dashboard-context">145 regulated entities<br>Python-generated snapshot<br>Evidence-led screening</div></aside>')
    watchlist = '<section id="watchlist" class="dashboard-watchlist" aria-label="Banks to review"><h2>Banks to review</h2><p class="sub">Cross-cutting alerts from existing outlier, regulatory-headroom, and disclosure-quality screens.</p><div id="watchlist-items" class="watchlist-grid"></div></section>'
    drillthrough = '<style>.bank-drillthrough{position:static;width:auto;height:auto;display:none;transform:none;box-shadow:none;margin:0 0 18px;border-left:4px solid var(--blue)}.bank-drillthrough.is-open{display:block}</style><aside id="bank-drillthrough" class="bank-drillthrough" aria-label="Bank detail" aria-hidden="true"><button type="button" class="bank-drillthrough-close" aria-label="Close bank detail">Close</button><div id="bank-drillthrough-content"></div></aside>'
    # This is the ONE seam TEMPLATE is meant to expose (see this function's
    # own docstring) - it used to be pre-empted by a stale duplicate of this
    # exact dashboard-shell CSS/nav baked directly into TEMPLATE (an older
    # snapshot with only 4 nav links and none of the watchlist/freshness-
    # badge/sparkline/global-search CSS added since), which meant this
    # replace's target string never existed and every patch below silently
    # never applied - confirmed empirically (0 watchlist/freshness/sparkline
    # CSS, no 9-link nav, no global search box in the live generated file
    # despite this function appearing to add all of them). Removed that
    # duplicate from TEMPLATE so this function is the single source of truth
    # for the dashboard shell again, as intended.
    html = html.replace('</style></head><body><main>', '</style>' + css + '</head><body><div class="dashboard-shell">' + navigation + '<main>')
    html = html.replace('<section class="grid"><article class="card"><h2>Two peer groups', watchlist + '<section id="dashboard-kpis" class="dashboard-kpis" aria-label="Executive summary"></section><section id="overview" class="dashboard-section"><div class="section-heading"><div><h2>Executive overview</h2><p>Start with the main signals, then move into the underlying comparisons.</p></div><span class="pill aligned">Interactive HTML snapshot</span></div><section class="grid"><article id="peer-groups" class="card"><h2>Two peer groups')
    # Keep the executive KPI strip first, then place the review watchlist and
    # its inline drill-through immediately before the overview content.
    kpi_section = '<section id="dashboard-kpis" class="dashboard-kpis" aria-label="Executive summary"></section>'
    html = html.replace(watchlist + kpi_section, kpi_section + watchlist, 1)
    html = html.replace(watchlist + '<section id="overview"', watchlist + drillthrough + '<section id="overview"', 1)
    html = html.replace('<article class="card wide"><h2>Trend signals', '<article id="trend-signals" class="card wide"><h2>Trend signals')
    html = html.replace('<article class="card wide"><h2>Inside the parent groups', '<article id="parent-groups" class="card wide"><h2>Inside the parent groups')
    html = html.replace('<section class="grid in011-analysis">', '<section id="analysis" class="grid in011-analysis">')
    # Close the #overview <section> opened above. Matching against the
    # literal '__IN011_ANALYSIS__' placeholder here was always a silent
    # no-op: main() already substitutes that placeholder with real rendered
    # content BEFORE calling decorate_dashboard_html(), so by the time this
    # replace runs the placeholder string no longer exists in `html` -
    # confirmed empirically (5 <section> opens, only 4 closes in the live
    # generated file). Anchoring on '\n<section id="analysis"' directly
    # ALSO failed silently: render_html_analysis()'s output puts two
    # <style> blocks between '</article></section>' and the analysis
    # <section>, so that adjacency never existed either. The
    # id="analysis" replace just above guarantees this exact analysis-
    # section-opener string is unique in the file, so anchor on it
    # directly instead of assuming what precedes it.
    html = html.replace('<section id="analysis" class="grid in011-analysis">',
                         '</section><section id="analysis" class="grid in011-analysis">')
    html = html.replace('</main><script>', '</main></div><script>' + load_chartjs_bundle() + '\n' + LOCAL_CHART_RUNTIME + '\nKatalysisCharts.observe();KatalysisCharts.refresh();\n')
    html = html.replace('function clusterBars(){', 'function dashboardSparklines(){const metrics=["CET1 ratio","Leverage ratio","NSFR"],cards=[...document.querySelectorAll(".kpi-card")];metrics.forEach((metric,index)=>{const series=D.trend_series?.[metric]||{},points=Object.entries(series).flatMap(([frn,values])=>Object.entries(values).map(([year,value])=>({year:Number(year),value:Number(value)}))).filter(x=>Number.isFinite(x.year)&&Number.isFinite(x.value));const byYear={};points.forEach(x=>(byYear[x.year]??=[]).push(x.value));const years=Object.keys(byYear).map(Number).sort((a,b)=>a-b),values=years.map(year=>{const v=byYear[year].sort((a,b)=>a-b);return v[Math.floor(v.length/2)]}),low=Math.min(...values),high=Math.max(...values),width=105,height=24,coords=values.map((value,i)=>`${(i/(values.length-1||1)*width).toFixed(1)},${(height-(value-low)/((high-low)||1)*(height-4)-2).toFixed(1)}`).join(" ");if(cards[index]&&values.length)cards[index].insertAdjacentHTML("beforeend",`<span class="kpi-note">${esc(metric)} median trend</span><svg class="kpi-sparkline" viewBox="0 0 ${width} ${height}" role="img" aria-label="${esc(metric)} median trend"><polyline points="${coords}" fill="none" stroke="var(--teal)" stroke-width="2"/></svg>`)})}\nfunction clusterBars(){')
    interaction_js = '''function applyGlobalBankFilter(){const input=document.querySelector("#global-bank-search");if(!input)return;input.addEventListener("input",()=>{const q=input.value.toLowerCase().trim();document.querySelectorAll("tr[data-search],tr[data-bank]").forEach(row=>{const text=(row.dataset.search||row.dataset.bank||row.textContent||"").toLowerCase();row.style.display=!q||text.includes(q)?"":"none"})})}
function openBank(name){const panel=document.querySelector("#bank-drillthrough"),content=document.querySelector("#bank-drillthrough-content"),key=String(name).toLowerCase(),tracks=[];for(const [metric,records] of Object.entries(D.in011?.in024?.trajectories||{})){const record=(records||[]).find(x=>String(x.bank).toLowerCase()===key);if(record)tracks.push(`<tr><td>${esc(metric)}</td><td>${record.years.filter(x=>x.value!==null).map(x=>`FY${x.year}: ${Number(x.value).toFixed(2)}%`).join(" · ")||"N/A"}</td></tr>`)}const head=(D.in011?.in021?.records||[]).filter(x=>String(x.bank).toLowerCase()===key),flags=(D.in011?.in025?.coverage?.cells||[]).filter(x=>String(x.bank).toLowerCase()===key&&(x.flags||[]).length),out=D.in011?.in009?.outliers||{},outRows=[...(out.broad||[]),...(out.strict||[])].filter(x=>String(x.bank).toLowerCase()===key);content.innerHTML=`<h2>${esc(name)}</h2><p class="sub">Bank-level drill-through from existing analytical payloads.</p><h3>Ratio history</h3><table class="drill-table"><tbody>${tracks.join("")||"<tr><td>No trajectory history available.</td></tr>"}</tbody></table><h3>Current headroom</h3><table class="drill-table"><tbody>${head.map(x=>`<tr><td>${esc(x.metric)}</td><td>${x.current_headroom==null?"N/A":Number(x.current_headroom).toFixed(2)+"pp"} · ${esc(x.status)}</td></tr>`).join("")||"<tr><td>No headroom record available.</td></tr>"}</tbody></table><h3>Flags and review prompts</h3><ul>${outRows.map(x=>`<li>${esc(x.metric)}: ${esc((x.reasons||[]).join("; "))}</li>`).concat(flags.map(x=>`<li>${esc(x.metric)} FY${x.year}: ${esc((x.flags||[]).join(", "))}</li>`)).join("")||"<li>No flags recorded.</li>"}</ul>`;panel.classList.add("is-open");panel.setAttribute("aria-hidden","false")}
function initBankDrillthrough(){const close=document.querySelector(".bank-drillthrough-close");if(close)close.addEventListener("click",()=>{const panel=document.querySelector("#bank-drillthrough");panel.classList.remove("is-open");panel.setAttribute("aria-hidden","true")});document.addEventListener("click",event=>{const button=event.target.closest("[data-bank-open]");if(button){openBank(button.dataset.bankOpen);if(button.closest("#watchlist")){const outliers=document.querySelector("#outliers");if(outliers)outliers.open=true}}});document.querySelectorAll("td").forEach(cell=>{const bank=(D.banks||[]).find(x=>String(x.name).toLowerCase()===cell.textContent.trim().toLowerCase());if(bank)cell.innerHTML=`<button type="button" class="bank-link" data-bank-open="${esc(bank.name)}">${esc(bank.name)}</button>`})}
applyGlobalBankFilter();initBankDrillthrough();
function initHeadroomSorting(){'''
    html = html.replace('function initHeadroomSorting(){', interaction_js)
    dashboard_kpis_js = '''function dashboardKpis(){const banks=D.banks||[],groups=D.groups||[],source=D.in011||{},years=Object.values(D.trend_series||{}).flatMap(series=>Object.values(series).flatMap(values=>Object.keys(values).map(Number))).filter(Number.isFinite),latest=years.length?Math.max(...years):"—",quality=source.in025?.trace_completeness||{},outliers=source.in009?.outliers||{},headroom=source.in021?.records||[],review=(outliers.broad||[]).length+(outliers.strict||[]).length+headroom.filter(x=>x.status==="screened"&&x.trend_direction==="declining").length;document.querySelector("#dashboard-kpis").innerHTML=[["Entities",banks.length,"regulated bank entities"],["Comparable cluster",banks.filter(b=>!b.insufficient).length,"with enough data for clustering"],["Parent groups",groups.length,"with reviewed context"],["Review signals",review,"outlier or declining-headroom flags"],["Latest annual data",latest,`trace complete: ${quality.complete_rows||0}/${quality.rows||0}`]].map(k=>`<article class="kpi-card"><span class="kpi-label">${esc(k[0])}</span><strong class="kpi-value">${esc(k[1])}</strong><span class="kpi-note">${esc(k[2])}</span></article>`).join("")}'''
    dashboard_watchlist_js = '''function dashboardWatchlist(){const source=D.in011||{},outliers=source.in009?.outliers||{},headroom=source.in021?.records||[],quality=source.in025?.coverage?.cells||[],items=[];for(const mode of ["broad","strict"])for(const x of (outliers[mode]||[]))items.push({bank:x.bank,reason:`${x.metric}: ${(x.reasons||[]).join("; ")}`,anchor:"outliers"});for(const x of headroom)if(x.status==="screened"&&x.trend_direction==="declining")items.push({bank:x.bank,reason:`${x.metric}: declining headroom`,anchor:"headroom"});const flagged={};for(const x of quality)if((x.flags||[]).length)flagged[x.bank]=(flagged[x.bank]||0)+(x.flags||[]).length;Object.entries(flagged).forEach(([bank,n])=>items.push({bank,reason:`${n} quality flag${n===1?"":"s"}`,anchor:"quality"}));const unique=[...new Map(items.map(x=>[x.bank+"|"+x.reason,x])).values()].slice(0,9);document.querySelector("#watchlist-items").innerHTML=unique.length?unique.map(x=>`<article class="watch-item"><button type="button" data-bank-open="${esc(x.bank)}">${esc(x.bank)}</button><a class="watch-reason" href="#${x.anchor}">${esc(x.reason)}</a></article>`).join(""):'<span class="watch-reason">No cross-cutting review alerts in the current payload.</span>'}'''
    html = html.replace('function dashboardSparklines(){', dashboard_kpis_js + dashboard_watchlist_js + 'function dashboardSparklines(){')
    search_fix_js = '''const trajectorySearchState=new Map();function restoreTrajectorySearchState(){trajectorySearchState.forEach((wasChecked,toggle)=>{if(toggle.isConnected&&toggle.checked!==wasChecked){toggle.checked=wasChecked;toggle.dispatchEvent(new Event("change",{bubbles:true}))}});trajectorySearchState.clear()}function focusTrajectoryBank(query){const q=query.toLowerCase().trim();if(!q){restoreTrajectorySearchState();return}restoreTrajectorySearchState();const names=[...new Set(Object.values(D.in011?.in024?.trajectories||{}).flatMap(records=>(records||[]).map(record=>String(record.bank))))],normalise=name=>name.toLowerCase().replace(/\\s+/g," ").trim(),normalised=normalise(q),exact=names.find(name=>normalise(name)===normalised),prefix=names.filter(name=>normalise(name).startsWith(normalised)),contains=names.filter(name=>normalise(name).includes(normalised)),matches=exact?[exact]:prefix.length===1?prefix:contains;if(matches.length!==1)return;const bank=matches[0],section=document.querySelector("#trajectories"),toggleBank=toggle=>normalise(toggle.value)===normalise(bank);if(section){section.open=true;section.scrollIntoView({behavior:"smooth",block:"start"})}document.querySelectorAll(".in024-bank-toggle").forEach(toggle=>{if(toggleBank(toggle)){if(!trajectorySearchState.has(toggle))trajectorySearchState.set(toggle,toggle.checked);toggle.checked=true;toggle.dispatchEvent(new Event("change",{bubbles:true}))}})}function bindReliableBankSearch(){const input=document.querySelector("#global-bank-search");if(!input)return;input.addEventListener("input",()=>focusTrajectoryBank(input.value))}bindReliableBankSearch();document.addEventListener("click",event=>{if(event.target.closest("[data-bank-open]"))setTimeout(()=>document.querySelector("#bank-drillthrough")?.scrollIntoView({behavior:"smooth",block:"nearest"}),0)});'''
    html = html.replace('applyGlobalBankFilter();initBankDrillthrough();', 'applyGlobalBankFilter();initBankDrillthrough();' + search_fix_js)
    shared_bank_js = '''<script>(function(){const toggles=[...document.querySelectorAll('.in024-shared-bank-toggle')];if(!toggles.length)return;const apply=()=>{const active=new Set(toggles.filter(item=>item.checked).map(item=>item.value));document.querySelectorAll('.in024-trajectory-chart [data-bank]').forEach(item=>{item.style.display=active.has(item.dataset.bank)?'':'none'})};toggles.forEach(item=>item.addEventListener('change',apply));document.querySelectorAll('[data-bank-preset]').forEach(button=>button.addEventListener('click',()=>{const mode=button.dataset.bankPreset;toggles.forEach(item=>{item.checked=mode==='all'||(mode==='top'&&item.dataset.defaultVisible==='true')});apply();if(window.KatalysisCharts)KatalysisCharts.refresh()}));apply();if(window.KatalysisCharts)KatalysisCharts.refresh()})();</script>'''
    chart_css = f'<style id="dashboard-chart-css">{CHART_CSS_PATH.read_text(encoding="utf-8")}</style>'
    return html.replace('clusterBars();peerGroups();renderMetricSelectors();trendBars();groups();', 'dashboardKpis();dashboardSparklines();dashboardWatchlist();clusterBars();peerGroups();renderMetricSelectors();trendBars();groups();').replace('</body>', chart_css + shared_bank_js + '</body>')


TEMPLATE = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>UK Bank Insights — client deliverable</title>
<style>
:root{--ink:#17202a;--muted:#65717d;--paper:#f6f3ed;--card:#fff;--blue:#195b8f;--red:#c45a49;--gold:#d49a35;--line:#d9d4c9}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.5 system-ui,-apple-system,Segoe UI,sans-serif}main{max-width:1180px;margin:auto;padding:32px 22px 60px}header{border-bottom:1px solid var(--line);padding-bottom:22px;margin-bottom:24px}h1{font:700 34px/1.1 Georgia,serif;margin:0 0 8px}h2{font:700 23px Georgia,serif;margin:0 0 6px}h3{font-size:16px;margin:0 0 4px}.eyebrow{text-transform:uppercase;letter-spacing:.12em;font-size:11px;color:var(--blue);font-weight:700}.lede{max-width:760px;color:var(--muted);margin:0}.prototype{float:right;background:#f3dfad;padding:5px 9px;border-radius:4px;font-size:11px;font-weight:700}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px;margin-bottom:26px}.card{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:18px;box-shadow:0 2px 8px #31281a0a}.wide{grid-column:1/-1}.sub{color:var(--muted);font-size:13px;margin:0 0 14px}.statrow{display:flex;gap:12px;margin:14px 0 4px}.stat{font-size:26px;font-weight:700}.stat small{display:block;font-size:11px;color:var(--muted);font-weight:500}.legend{display:flex;gap:14px;color:var(--muted);font-size:12px;margin-top:8px}.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:4px}.lower{background:var(--blue)}.higher{background:var(--gold)}.insufficient{background:#aaa}svg{width:100%;height:auto;display:block}.axis{stroke:var(--line);stroke-width:1}.bar-down{fill:var(--red)}.bar-up{fill:var(--blue)}.cluster-lower{fill:var(--blue)}.cluster-higher{fill:var(--gold)}.label{font-size:12px;fill:var(--ink)}.value{font-size:11px;fill:var(--muted)}.basis{display:flex;align-items:center;gap:12px;margin-top:16px}.basis-box{flex:1;border:1px solid var(--line);border-radius:6px;padding:12px;background:#faf9f5}.basis-box strong{display:block;font-size:13px}.basis-arrow{font-size:24px;color:var(--gold)}.controls{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin:10px 0 14px}.controls label{font-size:12px;color:var(--muted)}.controls select,.controls input{font:inherit;border:1px solid var(--line);border-radius:4px;padding:5px 7px;background:#fff}table{width:100%;border-collapse:collapse;font-size:13px}th,td{text-align:left;padding:9px 7px;border-bottom:1px solid var(--line)}th{font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}.pill{border-radius:12px;padding:3px 8px;font-size:11px;font-weight:650;display:inline-block}.aligned{background:#dcebdc;color:#285d2d}.mixed{background:#f4e5bd;color:#76520d}.not{background:#eee;color:#666}.foot{color:var(--muted);font-size:12px;border-top:1px solid var(--line);padding-top:16px;margin-top:24px}@media(max-width:760px){.grid{grid-template-columns:1fr}.wide{grid-column:auto}.prototype{float:none;display:inline-block;margin-bottom:10px}.basis{flex-direction:column;align-items:stretch}.basis-arrow{text-align:center;transform:rotate(90deg)}}
</style></head><body><main>
<header><span class="prototype">CLIENT DELIVERABLE · 2026 SNAPSHOT</span><div class="eyebrow">UK bank insights</div><h1>__HEADLINE__</h1><p class="lede">An interactive overview of 145 regulated entities: where banks cluster, which metrics moved together, and where legal-entity differences matter. Values are screening evidence, not a replacement for each bank’s source notes.</p></header>
<section class="grid"><article class="card"><h2>Two peer groups by capital buffers</h2><p class="sub">Each bar shows the average latest disclosed ratio for one group. 32 entities did not have enough comparable ratios to place in either group.</p><div id="cluster-bars"></div><div class="legend"><span><i class="dot" style="background:var(--blue)"></i>established/lower-buffer group</span><span><i class="dot" style="background:var(--gold)"></i>specialist/higher-buffer group</span></div><div id="peer-group-buttons" class="controls"></div><div id="peer-group-detail" style="display:none"></div></article>
__KEY_TAKEAWAYS__
<article class="card wide"><h2>Trend signals</h2><p class="sub">Choose how many metric rows to show, select a metric for each row, and set one start/end fiscal-year range. Counts are calculated from entities with both years available.</p><div class="controls"><label>Start year <input id="start-year" type="number" min="2021" max="2026" value="2021" style="width:70px"></label><label>End year <input id="end-year" type="number" min="2021" max="2026" value="2022" style="width:70px"></label><label>Show rows <input id="metric-count" type="number" min="1" max="8" value="4" style="width:55px"></label></div><div id="trend-metric-selectors" class="controls"></div><div id="trend-bars"></div><div class="basis"><div class="basis-box"><strong>Leverage basis before 2022</strong>Some disclosures include claims on central banks.</div><div class="basis-arrow">→</div><div class="basis-box"><strong>Comparable basis used here</strong>Use the ratio excluding claims on central banks.</div></div><div class="metric-guide"><strong>Metric guide</strong><ul style="margin:0;padding-left:20px"><li><b>CET1 ratio:</b> highest-quality capital ÷ risk-weighted assets.</li><li><b>Tier 1 ratio:</b> core and additional Tier 1 capital ÷ risk-weighted assets.</li><li><b>Total capital ratio:</b> total regulatory capital, including Tier 2 where applicable, ÷ risk-weighted assets.</li><li><b>Leverage ratio:</b> Tier 1 capital ÷ total exposure, without risk weighting.</li><li><b>LCR:</b> high-quality liquid assets ÷ stressed 30-day net cash outflows; it is not directly comparable in scale with capital ratios.</li><li><b>NSFR:</b> available stable funding ÷ required stable funding over a longer horizon.</li><li><b>MREL ratio:</b> loss-absorbing and recapitalisation resources relative to the applicable exposure measure; coverage is sparse.</li><li><b>RWA:</b> risk-weighted assets, an amount rather than a percentage; source currencies and bases vary.</li><li><b>Operating cash flow:</b> net cash generated by or used in operating activities; reporting bases vary.</li></ul></div></article>
<article class="card wide"><h2>Inside the parent groups</h2><p class="sub">Select a group to inspect its built legal entities and latest disclosed ratios. “Aligned” means the comparable entities moved in the same direction for the checked window; basis and acquisition caveats remain essential.</p><div id="group-table"></div><div id="group-detail" class="card" style="margin-top:16px;display:none"></div></article></section>
__IN011_ANALYSIS__
<p class="foot">Snapshot generated from the parent mapping, peer-group outputs, and trend analysis. Use the accompanying Python generators to recreate the HTML and PDF after refreshing the source data.</p>
</main><script>
const D=__DATA__;
function esc(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function clusterBars(){const max=60,w=700,h=190,left=210,metricX=100;let s=`<svg viewBox="0 0 ${w} ${h}" role="img" aria-label="Capital buffer peer group comparison">`;D.clusters.forEach((c,i)=>{let y=22+i*85;s+=`<text class="label" x="0" y="${y+8}">${i?'Specialist':'Established'}</text>`;[['CET1',c.cet1],['Tier 1',c.tier1],['Total capital',c.total]].forEach((x,j)=>{let bw=x[1]/max*400, yy=y+j*17;s+=`<rect class="${i?'cluster-higher':'cluster-lower'}" x="${left}" y="${yy}" width="${bw}" height="12" rx="2"/><text class="value" x="${metricX}" y="${yy+10}">${x[0]}</text><text class="value" x="${left+bw+6}" y="${yy+10}">${x[1].toFixed(1)}%</text>`})});s+='</svg>';document.querySelector('#cluster-bars').innerHTML=s}
function trendBars(){const start=Number(document.querySelector('#start-year').value),end=Number(document.querySelector('#end-year').value),count=Math.max(1,Math.min(8,Number(document.querySelector('#metric-count').value)||4)),selected=[...document.querySelectorAll('.trend-metric')].slice(0,count).map(x=>x.value),trends=selected.map(metric=>{const series=D.trend_series[metric]||{},changes=Object.values(series).filter(v=>v[start]!==undefined&&v[end]!==undefined).map(v=>v[end]-v[start]);return {label:metric,down:changes.filter(v=>v<0).length,up:changes.filter(v=>v>0).length,n:changes.length}}),w=1080,h=trends.length*48+18,labelX=0,barX=270,barWidth=180,upBarX=590,downCountX=460,upCountX=780,nX=900,max=Math.max(70,...trends.map(t=>Math.max(t.down,t.up)));let s=`<svg viewBox="0 0 ${w} ${h}" role="img" aria-label="Trend direction counts">`;trends.forEach((t,i)=>{let y=10+i*48,down=t.down/max*barWidth,up=t.up/max*barWidth;s+=`<text class="label" x="${labelX}" y="${y+12}">${esc(t.label)} FY${start}→FY${end}</text><rect class="bar-down" x="${barX}" y="${y}" width="${down}" height="18" rx="2"/><text class="label" x="${downCountX}" y="${y+13}">↓ ${t.down}</text><rect class="bar-up" x="${upBarX}" y="${y}" width="${up}" height="18" rx="2"/><text class="label" x="${upCountX}" y="${y+13}">↑ ${t.up}</text><text class="value" x="${nX}" y="${y+13}">n=${t.n}</text>`});s+='</svg><div class="legend"><span><i class="dot" style="background:var(--red)"></i>declined</span><span><i class="dot" style="background:var(--blue)"></i>rose</span><span>n = comparable entities</span></div>';document.querySelector('#trend-bars').innerHTML=s}
function renderMetricSelectors(){const metrics=['CET1 ratio','Tier 1 ratio','Total capital ratio','Leverage ratio','LCR','NSFR','MREL ratio','RWA','Operating cash flow'],defaults=['CET1 ratio','Total capital ratio','NSFR','RWA'],count=Math.max(1,Math.min(8,Number(document.querySelector('#metric-count').value)||4)),box=document.querySelector('#trend-metric-selectors');box.innerHTML=Array.from({length:count},(_,i)=>`<label>Metric ${i+1} <select class="trend-metric">${metrics.map(metric=>`<option ${metric===defaults[i]?'selected':''}>${metric}</option>`).join('')}</select></label>`).join('');box.querySelectorAll('.trend-metric').forEach(select=>select.addEventListener('change',trendBars))}
function peerGroups(){const groups=[['established','Established',b=>!b.insufficient&&String(b.cluster)==='0'],['specialist','Specialist',b=>!b.insufficient&&String(b.cluster)==='1'],['unspecified','Unspecified',b=>b.insufficient]],box=document.querySelector('#peer-group-buttons');box.innerHTML=groups.map(g=>`<button type="button" data-peer="${g[0]}">${g[1]} (${D.banks.filter(g[2]).length})</button>`).join('');box.querySelectorAll('button').forEach(button=>button.addEventListener('click',()=>{const group=groups.find(g=>g[0]===button.dataset.peer),detail=document.querySelector('#peer-group-detail');if(detail.dataset.peer===group[0]){detail.style.display='none';detail.dataset.peer='';}else showPeerGroup(group)}))}
function showPeerGroup(group){const members=D.banks.filter(group[2]),detail=document.querySelector('#peer-group-detail');detail.innerHTML=`<p class="sub"><strong>${group[1]}</strong>: ${members.length} entities</p><p>${members.length?members.map(b=>esc(b.name)).join(' · '):'No entities in this category.'}</p>`;detail.dataset.peer=group[0];detail.style.display='block'}
function groups(){let s='<table><thead><tr><th>Parent group</th><th>Entities</th><th>Capital movement</th><th>Cash-flow movement</th><th>Reading</th></tr></thead><tbody>';D.groups.forEach((g,i)=>{let cls=x=>x==='Aligned'?'aligned':x==='Mixed'?'mixed':'not';s+=`<tr><td><button class="group-button" data-group="${i}"><strong>${esc(g.name)}</strong></button></td><td>${g.entities}</td><td><span class="pill ${cls(g.capital)}">${esc(g.capital)}</span></td><td><span class="pill ${cls(g.cash)}">${esc(g.cash)}</span></td><td>${esc(g.note)}</td></tr>`});s+='</tbody></table>';document.querySelector('#group-table').innerHTML=s;document.querySelectorAll('.group-button').forEach(button=>button.addEventListener('click',()=>showGroup(Number(button.dataset.group))))}
function showGroup(index,metric1,metric2){const g=D.groups[index],detail=document.querySelector('#group-detail'),metrics=[['cet1','CET1 ratio'],['tier1','Tier 1 ratio'],['total','Total capital ratio'],['leverage','Leverage ratio'],['lcr','LCR'],['nsfr','NSFR'],['mrel','MREL ratio']],chosen1=metric1||'cet1',chosen2=metric2||'total',label1=metrics.find(x=>x[0]===chosen1)[1],label2=metrics.find(x=>x[0]===chosen2)[1],options=key=>metrics.map(x=>`<option value="${x[0]}" ${x[0]===key?'selected':''}>${x[1]}</option>`).join('');let s=`<h3>${esc(g.name)} group</h3><p class="sub">${esc(g.note)} Reporting bases may differ; these are latest disclosed values, not substituted parent figures.</p><div class="controls"><label>Metric 1 <select id="group-metric-1">${options(chosen1)}</select></label><label>Metric 2 <select id="group-metric-2">${options(chosen2)}</select></label></div><table><thead><tr><th>Legal entity</th><th>${esc(label1)} (latest)</th><th>${esc(label2)} (latest)</th></tr></thead><tbody>`;g.member_data.forEach(m=>{const value1=m[chosen1],value2=m[chosen2];s+=`<tr><td>${esc(m.name)}</td><td>${value1?esc(value1)+'%':'Not available'}</td><td>${value2?esc(value2)+'%':'Not available'}</td></tr>`});if(!g.member_data.length)s+='<tr><td colspan="3">No matching cluster row is available.</td></tr>';s+='</tbody></table>';detail.innerHTML=s;detail.style.display='block';document.querySelector('#group-metric-1').addEventListener('change',event=>showGroup(index,event.target.value,document.querySelector('#group-metric-2').value));document.querySelector('#group-metric-2').addEventListener('change',event=>showGroup(index,document.querySelector('#group-metric-1').value,event.target.value))}clusterBars();peerGroups();renderMetricSelectors();trendBars();groups();document.querySelector('#start-year').addEventListener('input',trendBars);document.querySelector('#end-year').addEventListener('input',trendBars);document.querySelector('#metric-count').addEventListener('input',()=>{renderMetricSelectors();trendBars()});
function initHeadroomSorting(){const table=document.querySelector('#headroom-table');if(!table)return;const body=table.tBodies[0],rows=[...body.rows];rows.forEach((row,index)=>row.dataset.originalIndex=index);table.querySelectorAll('.sort-headroom').forEach(button=>button.addEventListener('click',()=>{const key=button.dataset.sortKey,numeric=['current','floor','headroom','change','latest'].includes(key),ascending=table.dataset.sortKey===key?table.dataset.direction!=='asc':!numeric;table.dataset.sortKey=key;table.dataset.direction=ascending?'asc':'desc';rows.sort((a,b)=>{let av=a.dataset[key],bv=b.dataset[key];if(numeric){av=av===''?null:Number(av);bv=bv===''?null:Number(bv);if(av===null)return 1;if(bv===null)return -1;return (av-bv)*(ascending?1:-1)}return av.localeCompare(bv)*(ascending?1:-1)});rows.forEach(row=>body.appendChild(row));table.querySelectorAll('.sort-headroom').forEach(item=>{item.removeAttribute('aria-sort');item.textContent=item.textContent.replace(/ [↑↓]$/,'')});button.setAttribute('aria-sort',ascending?'ascending':'descending');button.textContent+=ascending?' ↑':' ↓'}))}initHeadroomSorting();
</script></body></html>'''


if __name__ == "__main__":
    main()
