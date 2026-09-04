"""Shared adapter and presentation helpers for IN-011 deliverables."""

import html
import json
import re

from in009_analysis import build_in009_payload
from in010_parent_groups import build_in010_payload
from in012_absolute_analysis import build_in012_payload
from in022_ratio_decomposition import build_in022_payload, fit_trend
from in023_distribution_visuals import build_in023_payload
from in024_trajectory import build_in024_payload
from in025_quality_views import build_in025_payload
from analysis_queries import AnalysisQueries
from in016_distribution import build_in016_payload
from in017_quality import build_in017_payload
from in021_headroom_trajectory import build_headroom_payload, validate_payload
from in040_risk_metrics import build_in040_payload
from chart_contract import build_line_chart_spec, build_rank_chart_spec, validate_chart_spec


DEFAULT_BANK_MIX = (
    ("large", 1, ("HSBC Bank Plc", "Barclays Bank Plc", "Lloyds Bank PLC")),
    ("medium", 3, ("Metro Bank PLC", "Shawbrook Bank Limited", "Aldermore Bank Plc")),
    ("small / specialist", 3, ("Oxbury Bank PLC", "Atom Bank PLC", "Starling Bank Limited")),
    ("international", 1, ("Goldman Sachs International Bank", "Citibank UK Limited", "J.P. Morgan Europe Limited")),
)
DEFAULT_EXCLUDED_BANK_FRAGMENTS = ("cater allen", "gb bank")


def default_bank_mix(records, years, limit=8):
    """Choose a readable, representative default set for a trajectory chart."""
    available = {str(record["bank"]): record for record in records}
    usable = {name for name, record in available.items()
              if sum(point["value"] is not None and point["year"] in years for point in record["years"]) >= 2
              and not any(fragment in name.casefold() for fragment in DEFAULT_EXCLUDED_BANK_FRAGMENTS)}
    recent_years = set(sorted(years)[-2:])
    recent_usable = {name for name in usable
                     if all(next((point["value"] for point in available[name]["years"]
                                  if point["year"] == year), None) is not None
                            for year in recent_years)}
    if recent_usable:
        usable = recent_usable
    chosen = []
    for _group, quota, candidates in DEFAULT_BANK_MIX:
        group_chosen = 0
        for candidate in candidates:
            match = next((name for name in usable if name.casefold() == candidate.casefold()), None)
            if not match:
                match = next((name for name in usable if candidate.casefold() in name.casefold()), None)
            if match and match not in chosen:
                chosen.append(match)
                group_chosen += 1
                if group_chosen >= quota:
                    break
    if len(chosen) < limit:
        fallback = sorted(usable - set(chosen), key=lambda name: (
            0 if available[name]["score"]["label"] in ("persistent_up", "persistent_down") else 1,
            -abs(available[name]["score"].get("robust_total_change") or 0), name,
        ))
        chosen.extend(fallback[:limit - len(chosen)])
    return set(chosen[:limit])


def build_in011_payload(db_path):
    """Assemble both upstream analysis payloads from one database snapshot."""
    in016 = build_in016_payload(db_path)
    in017 = build_in017_payload(db_path)
    # in017["lineage"] is one row per raw annual observation (~13k rows,
    # ~32MB) - deliberately kept in full in the standalone
    # in017_quality.json artifact refresh_all.py's own in017_quality.py step
    # writes independently (see that module's docstring: "intentionally
    # retained for Power BI and audit tooling"). But render_html_analysis()'s
    # "Sample source trace" table and render_pdf_analysis_lines()'s PDF
    # equivalent (both in this file) only ever read the first 8 rows of it -
    # keeping the other ~13,000 rows in *this* payload (the one embedded in
    # the client-facing HTML/PDF deliverable) was pure dead weight, the same
    # shape of bug as in023's duplication below.
    in017 = {**in017, "lineage": in017.get("lineage", [])[:8]}
    # build_in023_payload() embeds full copies of in016/in017 inside its own
    # returned dict - that's the right shape for its standalone
    # in023_distribution_visuals.json artifact (a self-contained snapshot),
    # but in011's payload already carries in016/in017 as siblings below, so
    # nesting them again here just doubled ~45MB into the client-facing HTML
    # deliverable for nothing: nothing ever reads in023["in017"], and
    # in023["in016"] was only ever read for its "distributions" sub-key
    # (now sourced from the sibling "in016" entry - see
    # render_html_distribution_visuals's in016 argument).
    in023 = build_in023_payload(db_path, in016, in017)
    in023 = {"metadata": in023["metadata"], "coverage": in023["coverage"]}
    return {
        "in009": build_in009_payload(db_path),
        "in010": build_in010_payload(db_path),
        "in012": build_in012_payload(db_path),
        "in022": build_in022_payload(db_path),
        "interim": {
            "coverage": AnalysisQueries(db_path).interim_coverage(),
            "latest_count": len(AnalysisQueries(db_path).latest_interim_snapshot(numeric_only=True)),
        },
        "in016": in016,
        "in017": in017,
        "in023": in023,
        "in024": build_in024_payload(db_path),
        "in025": build_in025_payload(db_path),
        "in021": build_headroom_payload(db_path),
        "in040": build_in040_payload(db_path),
    }


def render_html_risk_composition(in040):
    """Render loan concentration/quality and RWA density (IN-043). Own
    section, deliberately not woven into the 7 existing sections above -
    same scope as the IN-042 prototype (loan concentration/quality + RWA
    density), across every bank the underlying observations cover."""
    banks = in040["metadata"]["banks"]
    stage_balances = in040["loan_concentration_quality"]["stage_balances"]
    coverage_npl = in040["loan_concentration_quality"]["coverage_and_npl_ratios"]
    rwa_to_assets = in040["rwa_density"]["rwa_to_assets_pct"]
    rwa_category_composition = in040["rwa_density"]["rwa_category_composition"]

    loan_rows = []
    for frn, years in sorted(stage_balances.items(), key=lambda kv: banks.get(kv[0], "")):
        bank = banks.get(frn, frn)
        usable_years = [year for year, categories in years.items()
                        if sum(stages.get(f"stage_{n}", 0) for stages in categories.values() for n in (1, 2, 3)) > 0]
        if not usable_years:
            continue
        year = max(usable_years)
        categories = years[year]
        totals = {1: 0.0, 2: 0.0, 3: 0.0}
        for stages in categories.values():
            for n in (1, 2, 3):
                totals[n] += stages.get(f"stage_{n}", 0)
        grand_total = sum(totals.values())
        stage3_pct = round(totals[3] / grand_total * 100, 1) if grand_total else None
        npl = coverage_npl.get(frn, [])
        latest_npl = max((item for item in npl if item["year"] == year), key=lambda item: item["label"], default=None)
        category_list = ", ".join(sorted(categories)) or "—"
        loan_rows.append(
            f"<tr><td>{html.escape(bank)}</td><td>{year}</td><td>{html.escape(category_list)}</td>"
            f"<td>{'—' if stage3_pct is None else f'{stage3_pct}%'}</td>"
            f"<td>{html.escape(latest_npl['value_raw']) if latest_npl else '—'}</td></tr>"
        )
    if not loan_rows:
        loan_rows.append('<tr><td colspan="5">No IFRS 9 stage data available.</td></tr>')

    rwa_rows = []
    for frn, years in sorted(rwa_to_assets.items(), key=lambda kv: banks.get(kv[0], "")):
        bank = banks.get(frn, frn)
        year = max(years)
        density = years[year]
        composition = rwa_category_composition.get(f"{frn}:{year}", [])
        top_category = max(composition, key=lambda row: row["pct_of_total_rwa"], default=None)
        top_text = f"{html.escape(top_category['label'])} ({top_category['pct_of_total_rwa']}%)" if top_category else "—"
        rwa_rows.append(
            f"<tr><td>{html.escape(bank)}</td><td>{year}</td><td>{density}%</td><td>{top_text}</td></tr>"
        )
    if not rwa_rows:
        rwa_rows.append('<tr><td colspan="4">No RWA density data available.</td></tr>')

    return f'''<details class="card wide analysis-collapsible"><summary>Loan concentration, asset quality, and RWA density</summary><div class="collapsible-content">
<p class="explanation"><strong>What this shows:</strong> each bank's IFRS 9 loan-stage balances and RWA composition in its own most recent year with disclosed figures. Loan categories are reported as each bank actually discloses them - a bank with no customer loan book (e.g. a wholesale/treasury-led balance sheet) shows its own asset categories instead of an empty row. Stage 3 % is the share of the disclosed loan/exposure balance in Stage 3 (credit-impaired), a rough concentration-of-risk signal, not a formal NPL ratio unless the bank discloses one directly. RWA density is total RWAs as a % of total assets; the top RWA category is that bank-year's largest disclosed risk-weighted-asset category as a % of its own Total RWAs.</p>
<h3>Loan concentration and quality</h3>
<table><thead><tr><th>Bank</th><th>Year</th><th>Disclosed categories</th><th>Stage 3 %</th><th>Disclosed coverage/NPL ratio</th></tr></thead><tbody>{"".join(loan_rows)}</tbody></table>
<h3>RWA density</h3>
<table><thead><tr><th>Bank</th><th>Year</th><th>RWA / total assets</th><th>Largest RWA category</th></tr></thead><tbody>{"".join(rwa_rows)}</tbody></table>
</div></details>'''


def render_html_absolute_analysis(in012):
    """Render unit-aware absolute analysis with chart and table fallbacks."""
    metrics = in012["absolute_metrics"]
    bars = []
    rows = []
    cohort_rows = []
    for index, (metric, data) in enumerate(metrics.items()):
        coverage = data["coverage"]
        scaled = data.get("scale_adjusted_coverage", {})
        known = coverage.get("known_unit_banks", 0)
        bars.append(
            f'<text class="label" x="0" y="{index * 32 + 14}">{html.escape(metric)}</text>'
            f'<rect class="cluster-lower" x="170" y="{index * 32 + 3}" width="{known * 3}" height="16" rx="2"/>'
            f'<text class="value" x="{180 + known * 3}" y="{index * 32 + 15}">{known} known-unit banks</text>'
        )
        exclusions = ", ".join(f"{key}: {value}" for key, value in scaled.get("exclusions", {}).items()) or "none"
        latest_period = data["trends"][-1] if data.get("trends") else None
        movement = "—" if latest_period is None else f"FY{latest_period['start_year']}→FY{latest_period['end_year']}: ↑{latest_period['up']} / ↓{latest_period['down']} / n={latest_period['n']}"
        rows.append(
            f"<tr><td>{html.escape(metric)}</td><td>{coverage.get('observations', 0)}</td>"
            f"<td>{known}</td><td>{coverage.get('unknown_unit_observations', 0)}</td>"
            f"<td>{coverage.get('banks', 0)}</td><td>{scaled.get('banks', 0)}</td>"
            f"<td>{html.escape(movement)}</td><td>{html.escape(exclusions)}</td></tr>"
        )
        for cohort in data.get("size_cohorts", []):
            cohort_rows.append(
                f"<tr><td>{html.escape(metric)}</td><td>{html.escape(cohort['amount_unit'])}</td>"
                f"<td>{html.escape(cohort['reporting_basis'])}</td><td>{cohort['count']}</td>"
                f"<td>{html.escape(cohort['status'])}</td></tr>"
            )
    return """<details class="card wide analysis-collapsible"><summary>Absolute capital and RWA analysis</summary>
<div class="grid in014-analysis"><article class="card wide">
<p class="explanation"><strong>What this shows:</strong> the size of regulatory capital and risk-weighted assets in the units disclosed by each bank, plus comparisons after matching the source unit and reporting basis. These are amounts, unlike capital ratios. A larger amount does not by itself mean a stronger capital position; compare it with the related RWA and use the ratio sections for capital adequacy.</p>
<div role="img" aria-label="Known-unit bank coverage by absolute metric"><svg viewBox="0 0 760 %d">%s</svg></div>
<div class="legend"><span><i class="dot" style="background:var(--blue)"></i>banks with recognized source units</span><span>Scale-adjusted values require matching units and reporting basis.</span></div>
</article>
<article class="card wide"><h3>Coverage, movement and scale-adjusted comparisons</h3>
<table><thead><tr><th>Metric</th><th>Observations</th><th>Known-unit banks</th><th>Unknown-unit observations</th><th>Stable series</th><th>Scale-adjusted banks</th><th>Latest movement</th><th>Scale exclusions</th></tr></thead><tbody>%s</tbody></table></article>
<article class="card wide"><h3>Size-cohort guardrails</h3>
<p class="explanation"><strong>What this shows:</strong> which banks can be ranked as smaller, medium, or larger within a genuinely comparable population. Banks are grouped only when their disclosed currency scale and reporting basis match, and cohorts smaller than three are marked insufficient rather than ranked.</p>
<table><thead><tr><th>Metric</th><th>Unit</th><th>Reporting basis</th><th>Banks</th><th>Status</th></tr></thead><tbody>%s</tbody></table></article>
</div></details>""" % (max(32, len(metrics) * 32), "".join(bars), "".join(rows), "".join(cohort_rows))


def _repair_trajectory_interactions(fragment):
    """Keep one coordinated reset path for each trajectory chart.

    The trajectory renderer is intentionally kept as a compact HTML template,
    so this small post-processing seam removes the older reset listeners and
    makes both button and double-click reset the outer and data-layer transforms.
    """
    fragment = fragment.replace("svg.addEventListener('dblclick',reset);", "")
    fragment = fragment.replace(
        "const button=document.querySelector('.in024-reset-zoom[data-chart=\"'+svg.dataset.chart+'\"]');if(button)button.addEventListener('click',reset)",
        "",
    )
    fragment = fragment.replace(
        "const refreshDomain=chart=>",
        "const resetView=chart=>{const layer=chart.querySelector('.in024-trajectory-layer');if(layer)layer.removeAttribute('transform');chart.classList.remove('is-zoomed');chart.querySelectorAll('[data-base-stroke-width]').forEach(line=>line.setAttribute('stroke-width',line.dataset.baseStrokeWidth));refreshDomain(chart)};const refreshDomain=chart=>",
    )
    fragment = fragment.replace(
        "if(reset)reset.addEventListener('click',()=>refreshDomain(chart))",
        "if(reset)reset.addEventListener('click',()=>resetView(chart));chart.addEventListener('dblclick',()=>resetView(chart))",
    )
    return fragment


def render_html_analysis(payload):
    """Render the client-facing HTML fragment from computed payloads."""
    in009 = payload["in009"]
    in010 = payload["in010"]["parent_groups"]
    lines = [
        '<style>.in011-analysis{grid-template-columns:1fr}.in011-analysis .card{min-width:0;overflow:hidden}.in011-analysis table{display:block;overflow-x:auto;white-space:nowrap}.in011-analysis th,.in011-analysis td{vertical-align:top}.in011-analysis .explanation{color:var(--ink);background:#faf9f5;border-left:3px solid var(--blue);padding:10px 12px;margin:0 0 16px}.analysis-collapsible{grid-column:1/-1}.analysis-collapsible>summary{cursor:pointer;font:700 23px Georgia,serif;list-style-position:inside}.analysis-collapsible[open]>summary{margin-bottom:16px}.legend{flex-wrap:wrap}.quality-badge{display:inline-block;border:1px solid var(--blue);border-radius:999px;padding:3px 8px;font-size:12px;background:#eef5f9}.in024-chart-layout{display:grid;grid-template-columns:220px minmax(0,1fr);gap:16px;align-items:start}.in024-bank-list{max-height:220px;overflow:auto;border:1px solid #d7d9dc;padding:8px;display:grid;gap:4px;font-size:12px}.in024-bank-list label{display:block}.in024-chart-stage{min-width:0;overflow:hidden;position:relative}.in024-trajectory-chart{width:100%;height:auto;cursor:crosshair;user-select:none}.in024-trajectory-chart.is-zoomed{cursor:default}.in024-brush{fill:rgba(30,100,150,.16);stroke:var(--blue);stroke-dasharray:4 3;pointer-events:none}.in024-tooltip{min-height:18px;margin:3px 0;color:var(--ink);font-size:12px;font-weight:700}.in024-hover-line{stroke:var(--ink);stroke-width:1;stroke-dasharray:3 3;opacity:.55;pointer-events:none}</style>',
        '<style>.sort-headroom{border:0;background:none;color:inherit;cursor:pointer;font:inherit;font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;padding:0;text-align:left}.sort-headroom:hover,.sort-headroom:focus{color:var(--blue);text-decoration:underline}</style>',
        '<section id="analysis" class="grid in011-analysis">',
        '<details class="card wide analysis-collapsible"><summary>Strict versus broad coverage</summary><div class="collapsible-content">',
        '<p class="explanation"><strong>What this shows:</strong> how many banks can be compared for each Pillar 3 metric. <em>Broad</em> coverage is a screening view that includes valid annual disclosures even when the reporting basis is not explicit. <em>Strict</em> coverage keeps only observations with a known, common basis, so differences are less likely to reflect entity-versus-group reporting rather than bank performance.</p>',
        '<table><thead><tr><th>Metric</th><th>Broad banks</th><th>Strict banks</th><th>Strict exclusions</th></tr></thead><tbody>',
    ]
    for metric in in009["metadata"]["metrics"]:
        broad = in009["coverage"][metric]["broad"]
        strict = in009["coverage"][metric]["strict"]
        exclusions = ", ".join(f"{key}: {value}" for key, value in strict.get("exclusions", {}).items()) or "none"
        lines.append(f"<tr><td>{html.escape(metric)}</td><td>{broad['banks']}</td><td>{strict['banks']}</td><td>{html.escape(exclusions)}</td></tr>")
    lines += ["</tbody></table></div></details>"]
    if payload.get("in022"):
        lines.append(render_html_ratio_decomposition(payload["in022"]))
    if payload.get("in023"):
        lines.append(render_html_distribution_visuals(payload["in023"], payload["in016"]))
    if payload.get("in024"):
        lines.append(_repair_trajectory_interactions(render_html_trajectory_visuals(payload["in024"])))
    if payload.get("in025"):
        lines.append(render_html_quality_views(payload["in025"]))
    lines += ['<details class="card wide analysis-collapsible"><summary>Outlier investigation</summary><div class="collapsible-content">', '<p class="explanation"><strong>What this shows:</strong> Pillar 3 disclosures that deserve a closer look because their level, year-on-year movement, data quality, or peer position is unusual. An outlier is a review prompt, not evidence of an error or weakness; use the bank’s source report and basis notes before drawing a conclusion.</p>', '<table><thead><tr><th>Metric</th><th>Bank</th><th>Year</th><th>Value</th><th>Reason</th><th>Status</th></tr></thead><tbody>']
    outliers = [item for mode in ("broad", "strict") for item in in009["outliers"][mode]]
    for item in outliers:
        lines.append(
            f"<tr><td>{html.escape(item['metric'])}</td><td>{html.escape(item['bank'])}</td>"
            f"<td>{item['fiscal_year']}</td><td>{item['value']}</td>"
            f"<td>{html.escape('; '.join(item['reasons']))}</td>"
            f"<td>{html.escape(item.get('comparability_status', 'unknown'))}</td></tr>"
        )
    if not outliers:
        lines.append('<tr><td colspan="6">No outliers flagged.</td></tr>')
    lines += ["</tbody></table></div></details>"]
    parent_rows = []
    for metric, modes in in010.items():
        for group in modes["strict"]:
            level = group["latest_level"]
            trends = group["trends"]
            latest_trend = trends[-1] if trends else None
            level_text = level.get("status", "insufficient")
            range_text = str(level.get("range", "—"))
            trend_text = latest_trend["direction"] if latest_trend else "insufficient"
            if level.get("status") == "comparable" or (latest_trend and latest_trend.get("n", 0) > 0):
                parent_rows.append(f"<tr><td>{html.escape(metric)}</td><td>{html.escape(group['group'])}</td><td>{html.escape(level_text)}</td><td>{html.escape(range_text)}</td><td>{html.escape(trend_text)}</td></tr>")
    if parent_rows:
        lines += ['<details class="card wide analysis-collapsible"><summary>Parent-group dispersion and agreement</summary><div class="collapsible-content">', '<p class="explanation"><strong>What this shows:</strong> whether separately regulated entities in the same banking group report similar Pillar 3 outcomes. The latest range describes the spread between the lowest and highest comparable entity; the trend describes whether entities moved in the same direction between reporting years. This is a legal-entity comparison, not a consolidated-group result.</p>', '<table><thead><tr><th>Metric</th><th>Group</th><th>Latest level</th><th>Range</th><th>Latest trend</th></tr></thead><tbody>', *parent_rows, "</tbody></table></div></details>"]
    if payload.get("in012"):
        lines.append(render_html_absolute_analysis(payload["in012"]))
    if payload.get("in040"):
        lines.append(render_html_risk_composition(payload["in040"]))
    if payload.get("in016"):
        distribution_rows = []
        for metric, modes in payload["in016"]["distributions"].items():
            cohorts = modes["strict"]
            eligible_cohorts = [item for item in cohorts if item["summary"].get("n", 0) >= 8]
            chosen = max(eligible_cohorts or cohorts, key=lambda item: (item.get("fiscal_year") or 0, item.get("reporting_basis") or "")) if cohorts else None
            summary = chosen["summary"] if chosen else {"n": 0, "median": None, "q1": None, "q3": None, "iqr": None, "status": "no cohort"}
            fmt = lambda value: "—" if value is None else f"{value:.2f}"
            distribution_rows.append(
                f"<tr><td>{html.escape(metric)}</td><td>{summary['n']}</td><td>{fmt(summary['median'])}</td>"
                f"<td>{fmt(summary['q1'])}–{fmt(summary['q3'])}</td><td>{fmt(summary['iqr'])}</td>"
                f"<td>{html.escape(chosen.get('reporting_basis', '—') if chosen else '—')}</td><td>{summary['status']}</td></tr>"
            )
        lines.append('<details class="card wide analysis-collapsible"><summary>Comparable distribution benchmarks</summary><div class="collapsible-content"><p class="explanation"><strong>What this shows:</strong> the middle and spread of each core ratio within one exact fiscal-year and reporting-basis cohort. The median is the middle observation; the interquartile range contains the middle half of banks. Small cohorts are labelled and broad coverage is not treated as a benchmark.</p><table><thead><tr><th>Metric</th><th>N</th><th>Median</th><th>Q1–Q3</th><th>IQR</th><th>Basis</th><th>Status</th></tr></thead><tbody>' + ''.join(distribution_rows) + '</tbody></table></div></details>')
        absolute_rows = []
        for metric, cohorts in payload["in016"].get("absolute_distributions", {}).items():
            usable = [item for item in cohorts if item["summary"].get("n", 0) >= 8]
            chosen = max(usable or cohorts, key=lambda item: (item.get("fiscal_year") or 0, item.get("amount_unit") or "")) if cohorts else None
            summary = chosen["summary"] if chosen else {"n": 0, "median": None, "iqr": None, "status": "no cohort"}
            fmt = lambda value: "—" if value is None else f"{value:.2f}"
            absolute_rows.append(f"<tr><td>{html.escape(metric)}</td><td>{chosen.get('fiscal_year', '—') if chosen else '—'}</td><td>{html.escape(chosen.get('amount_unit', '—') if chosen else '—')}</td><td>{summary['n']}</td><td>{fmt(summary['median'])}</td><td>{fmt(summary['iqr'])}</td><td>{summary['status']}</td></tr>")
        lines.append('<details class="card wide analysis-collapsible"><summary>Absolute-value distribution benchmarks</summary><div class="collapsible-content"><p class="explanation"><strong>What this shows:</strong> the typical disclosed amount of capital or risk-weighted assets among banks in the same fiscal year, reporting basis, and explicitly identified source unit. This avoids ranking a bank in thousands against a bank in millions. Amount size is not financial strength; use the ratio and RWA context alongside it.</p><table><thead><tr><th>Metric</th><th>Fiscal year</th><th>Unit</th><th>N</th><th>Median</th><th>IQR</th><th>Status</th></tr></thead><tbody>' + ''.join(absolute_rows) + '</tbody></table></div></details>')
        movement_rows = []
        for metric, movements in payload["in016"].get("rank_movement", {}).items():
            usable = [item for item in movements if item.get("n", 0) >= 8]
            chosen = max(usable or movements, key=lambda item: (item.get("end_year") or 0, item.get("reporting_basis") or "")) if movements else None
            if chosen:
                movement_rows.append(f"<tr><td>{html.escape(metric)}</td><td>FY{chosen['start_year']}→FY{chosen['end_year']}</td><td>{chosen['n']}</td><td>{chosen['up']}</td><td>{chosen['down']}</td><td>{chosen['same']}</td><td>{html.escape(chosen['reporting_basis'])}</td><td>{chosen['status']}</td></tr>")
        lines.append('<details class="card wide analysis-collapsible"><summary>Fixed-panel rank movement</summary><div class="collapsible-content"><p class="explanation"><strong>What this shows:</strong> how the same banks moved through the ratio ranking between two years. Only banks present in both years with the same reporting basis are included, so a bank entering or leaving the dataset cannot create artificial movement. A lower rank number means a stronger position in the sorted cohort; ties use shared ranks.</p><table><thead><tr><th>Metric</th><th>Period</th><th>Fixed panel</th><th>Moved up</th><th>Moved down</th><th>Unchanged</th><th>Basis</th><th>Status</th></tr></thead><tbody>' + (''.join(movement_rows) or '<tr><td colspan="8">No fixed panel reached the minimum cohort size.</td></tr>') + '</tbody></table></div></details>')
        group_rows = []
        for kind, coverage in payload["in016"].get("group_benchmark_coverage", {}).items():
            group_rows.append(f"<tr><td>{html.escape(coverage['model'])}</td><td>{len(coverage['groups'])}</td><td>{coverage['eligible']}</td><td>{coverage['suppressed']}</td><td>{coverage['minimum_n']}</td></tr>")
        lines.append('<details class="card wide analysis-collapsible"><summary>Group-model benchmark guardrails</summary><div class="collapsible-content"><p class="explanation"><strong>What this shows:</strong> whether the available parent-group and peer-cluster populations are large enough for distributional benchmarking. Groups below the minimum are retained as coverage information but suppressed from percentile statistics, because a small group would make its “benchmark” unstable or expose individual entities.</p><table><thead><tr><th>Model</th><th>Groups found</th><th>Eligible benchmarks</th><th>Suppressed</th><th>Minimum N</th></tr></thead><tbody>' + ''.join(group_rows) + '</tbody></table></div></details>')
    quality = payload.get("in017")
    if quality:
        quality_rows = []
        for item in quality.get("quality_facts", []):
            quality_rows.append(f"<tr><td>{html.escape(item['metric'])}</td><td>{item['banks']}</td><td>{item['observations']}</td><td>{item['numeric']}</td><td>{item['missing']}</td><td>{item['non_numeric_disclosure']}</td><td>{item['row_label_variant_count']}</td><td>{html.escape(item['structural_status'])}</td></tr>")
        source_rows = []
        for item in quality.get("lineage", [])[:8]:
            source_rows.append(f"<tr><td>{html.escape(item.get('canonical_bank', ''))}</td><td>{html.escape(item.get('source_workbook', ''))}</td><td>{html.escape(item.get('sheet', ''))}</td><td>{html.escape(item.get('row_label', ''))}</td><td>{html.escape(item.get('year', ''))}</td><td>{html.escape(item.get('value_raw', ''))}</td><td>{html.escape(item.get('source_note', '') or '—')}</td></tr>")
        lines.append('<details class="card wide analysis-collapsible"><summary>Source lineage and data-quality monitoring</summary><div class="collapsible-content"><p class="explanation"><strong>What this shows:</strong> whether each metric has a usable extracted value and where those values came from. “Missing” means the source did not provide a value; “non-numeric disclosure” means text was present but could not be parsed. These are different from extraction errors, which fail the structural checks before a deliverable is generated. The lineage table shows the workbook, sheet, row label, period, raw value, and source note behind each observation.</p><table><thead><tr><th>Metric</th><th>Banks</th><th>Observations</th><th>Numeric</th><th>Missing</th><th>Non-numeric</th><th>Label variants</th><th>Structure</th></tr></thead><tbody>' + ''.join(quality_rows) + '</tbody></table><h3>Sample source trace</h3><table><thead><tr><th>Bank</th><th>Workbook</th><th>Sheet</th><th>Source row</th><th>Period</th><th>Raw value</th><th>Source note</th></tr></thead><tbody>' + ''.join(source_rows) + '</tbody></table></div></details>')
    headroom = payload.get("in021")
    if headroom:
        validate_payload(headroom["source_database"], headroom)
        rows = []
        for item in headroom["records"]:
            def fmt(value):
                return "—" if value is None else f"{value:.2f}%"
            change_text = "—" if item["trend_change"] is None else f"{item['trend_change']:+.2f}%"
            rows.append(
                f"<tr data-bank=\"{html.escape(item['bank'])}\" data-metric=\"{html.escape(item['metric'])}\" data-latest=\"{item['latest_year']}\" data-current=\"{item['current_value'] if item['current_value'] is not None else ''}\" data-floor=\"{item['regulatory_floor'] if item['regulatory_floor'] is not None else ''}\" data-headroom=\"{item['current_headroom'] if item['current_headroom'] is not None else ''}\" data-direction=\"{html.escape(item['trend_direction'] or '')}\" data-change=\"{item['trend_change'] if item['trend_change'] is not None else ''}\" data-status=\"{html.escape(item['status'])}\"><td>{html.escape(item['bank'])}</td><td>{html.escape(item['metric'])}</td>"
                f"<td>FY{item['latest_year']}</td><td>{fmt(item['current_value'])}</td>"
                f"<td>{fmt(item['regulatory_floor'])}</td><td>{fmt(item['current_headroom'])}</td>"
                f"<td>{html.escape(item['trend_direction'] or '—')}</td><td>{change_text}</td>"
                f"<td>{html.escape(item['status'])}</td></tr>"
            )
        lines.append('<details class="card wide analysis-collapsible"><summary>Regulatory headroom trajectory</summary><div class="collapsible-content"><p class="explanation"><strong>What this shows:</strong> a screening list of banks whose latest disclosed ratio sits above a dated regulatory floor and whose own annual observations have moved over time. <em>Headroom</em> is the current ratio minus the applicable minimum and buffer; <em>trend magnitude</em> is the observed change from the first to latest comparable year. This is an early-warning screen, not a forecast or a breach-date calculation. “No regulatory context” means the policy could not safely match a dated percentage floor; “insufficient evidence” means too few comparable years.</p><p class="sub">Click any column heading to sort the table. The initial order is the analytical screening order; clicking the same heading again reverses the sort.</p><table id="headroom-table"><thead><tr><th><button type="button" class="sort-headroom" data-sort-key="bank">Bank</button></th><th><button type="button" class="sort-headroom" data-sort-key="metric">Metric</button></th><th><button type="button" class="sort-headroom" data-sort-key="latest">Latest</button></th><th><button type="button" class="sort-headroom" data-sort-key="current">Current</button></th><th><button type="button" class="sort-headroom" data-sort-key="floor">Floor</button></th><th><button type="button" class="sort-headroom" data-sort-key="headroom">Headroom</button></th><th><button type="button" class="sort-headroom" data-sort-key="direction">Direction</button></th><th><button type="button" class="sort-headroom" data-sort-key="change">Change</button></th><th><button type="button" class="sort-headroom" data-sort-key="status">Status</button></th></tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div></details>')
    interim = payload.get("interim")
    if interim:
        coverage = interim["coverage"]
        types = ", ".join(f"{key.replace('_', ' ')}: {value}" for key, value in coverage["period_types"].items()) or "none"
        lines.append(
            '<details class="card wide analysis-collapsible"><summary>Interim disclosure coverage</summary>'
            '<div class="collapsible-content"><p class="explanation"><strong>What this shows:</strong> additional quarterly, half-year, and point-in-time disclosures available for selected banks. These observations are kept separate from the annual analysis because dates, durations, legal-entity scope, and reporting bases do not line up automatically across banks. Use them to inspect cadence and recent snapshots, not to assume a like-for-like annual comparison.</p>'
            f'<table><thead><tr><th>Banks</th><th>Observations</th><th>Numeric</th><th>Period types</th><th>Latest comparable snapshots</th><th>Source-register rows</th></tr></thead><tbody><tr><td>{coverage["banks"]}</td><td>{coverage["observations"]}</td><td>{coverage["numeric_observations"]}</td><td>{html.escape(types)}</td><td>{interim["latest_count"]}</td><td>{coverage["source_register_rows"]}</td></tr></tbody></table></div></details>'
        )
    lines.append("</section>")
    rendered = "\n".join(lines)
    anchors = {
        "Strict versus broad coverage": "coverage",
        "CET1 ratio movement decomposition": "ratio-decomposition",
        "Robust distributions and evidence coverage": "distribution-visuals",
        "Persistent trajectories and rank mobility": "trajectories",
        "Source quality and disclosure coverage": "quality",
        "Outlier investigation": "outliers",
        "Parent-group dispersion and agreement": "parent-dispersion",
        "Absolute capital and RWA analysis": "absolute-analysis",
        "Loan concentration, asset quality, and RWA density": "risk-composition",
        "Comparable distribution benchmarks": "distribution-benchmarks",
        "Regulatory headroom trajectory": "headroom",
        "Interim disclosure coverage": "interim-coverage",
    }
    for title, anchor in anchors.items():
        rendered = rendered.replace(
            f'<details class="card wide analysis-collapsible"><summary>{title}',
            f'<details id="{anchor}" class="card wide analysis-collapsible"><summary>{title}',
        )
    for anchor in ("headroom",):
        rendered = rendered.replace(f'<details id="{anchor}" class="card wide analysis-collapsible">', f'<details id="{anchor}" open class="card wide analysis-collapsible">')
    return rendered


def _plot_limit(records, field):
    values = sorted(abs(float(item[field])) for item in records if item.get(field) is not None)
    if not values:
        return 1.0
    position = min(len(values) - 1, max(0, int(round((len(values) - 1) * 0.95))))
    return max(1.0, values[position]) * 1.1


def render_html_ratio_decomposition(in022):
    """Render the broad decomposition with a strict validation table."""
    broad = in022["broad"]
    records = broad.get("records", [])
    axis_options = {"rwa_change_pct": "RWA change (%)", "capital_change_pct": "CET1 capital change (%)", "ratio_change_pp": "CET1 ratio change (pp)"}
    axis_data = [{"bank": item.get("bank", item.get("frn", "")), **{key: item.get(key) for key in axis_options}, "ratio_change_pp": item.get("ratio_change_pp")} for item in records]
    data_json = json.dumps(axis_data, ensure_ascii=True).replace("</", "<\\/")
    default_fit = fit_trend(records, "rwa_change_pct", "capital_change_pct")
    strict = in022.get("strict", {})
    rows = []
    for item in strict.get("records", []):
        sources = html.escape(f"Capital: {item.get('capital_source_note', '')} | RWA: {item.get('rwa_source_note', '')}")
        rows.append(
            f"<tr><td>{html.escape(str(item['bank']))}</td><td>FY{item['start_year']}→FY{item['end_year']}</td>"
            f"<td>{item['capital_change_pct']:+.2f}%</td><td>{item['rwa_change_pct']:+.2f}%</td>"
            f"<td>{item['ratio_change_pp']:+.2f}pp</td><td>{html.escape(str(item.get('amount_unit') or '—'))}</td>"
            f"<td>{html.escape(str(item.get('reporting_basis') or 'unknown'))}</td><td>{html.escape(item['movement_pattern'])}</td>"
            f"<td><details><summary>view source notes</summary>{sources}</details></td></tr>"
        )
    exclusions = ", ".join(f"{key}: {value}" for key, value in broad["coverage"].get("exclusions", {}).items()) or "none"
    x_options = "".join(
        f'<option value="{key}"{" selected" if key == "rwa_change_pct" else ""}>{label}</option>'
        for key, label in axis_options.items()
    )
    y_options = "".join(
        f'<option value="{key}"{" selected" if key == "capital_change_pct" else ""}>{label}</option>'
        for key, label in axis_options.items()
    )
    return f'''<details class="card wide analysis-collapsible"><summary>CET1 ratio movement decomposition</summary><div class="collapsible-content">
<p class="explanation"><strong>What this shows:</strong> whether a CET1 ratio movement coincided with growth in CET1 capital, growth in total RWAs, or both. The broad screening view includes banks with a consistent known amount unit even when basis is unknown. Points are clipped to a robust plotting range for readability; the table retains the exact derived values. This is a decomposition of observed movement, not a causal attribution.</p>
<div class="controls"><label>X-axis <select id="in022-x-axis">{x_options}</select></label><label>Y-axis <select id="in022-y-axis">{y_options}</select></label></div>
<div id="in022-trend-summary" class="legend">Default fit: slope={default_fit['slope'] if default_fit['slope'] is not None else '—'}, R²={default_fit['r_squared'] if default_fit['r_squared'] is not None else '—'}, N={default_fit['n']}</div>
<div id="in022-chart" role="img" aria-label="Selectable CET1 ratio movement decomposition scatter plot"></div>
<div class="legend"><span><i class="dot" style="background:var(--blue)"></i>CET1 ratio rose or unchanged</span><span><i class="dot" style="background:var(--red)"></i>CET1 ratio fell</span><span>Broad comparable N={broad['coverage'].get('comparable_banks', 0)}; exclusions: {html.escape(exclusions)}</span><span>Trend line is OLS over unclipped numeric records; plotted extremes are robustly clipped.</span></div>
<script>(function(){{const data={data_json};const labels={json.dumps(axis_options)};const xSelect=document.getElementById('in022-x-axis');const ySelect=document.getElementById('in022-y-axis');const chart=document.getElementById('in022-chart');const summary=document.getElementById('in022-trend-summary');if(!chart)return;function render(){{const xKey=xSelect.value,yKey=ySelect.value;const points=data.filter(row=>row[xKey]!==null&&row[yKey]!==null);const absLimit=key=>{{const values=points.map(row=>Math.abs(Number(row[key]))).sort((a,b)=>a-b);return values.length?Math.max(1,values[Math.min(values.length-1,Math.round((values.length-1)*.95))])*1.1:1}};const xLimit=absLimit(xKey),yLimit=absLimit(yKey);const left=75,top=25,pw=620,ph=285,cx=left+pw/2,cy=top+ph/2;const mean=key=>points.reduce((sum,row)=>sum+Number(row[key]),0)/points.length;let slope=null,intercept=null,r2=null;if(points.length>1){{const xm=mean(xKey),ym=mean(yKey),den=points.reduce((sum,row)=>sum+(Number(row[xKey])-xm)**2,0);if(den){{slope=points.reduce((sum,row)=>sum+(Number(row[xKey])-xm)*(Number(row[yKey])-ym),0)/den;intercept=ym-slope*xm;const total=points.reduce((sum,row)=>sum+(Number(row[yKey])-ym)**2,0);const residual=points.reduce((sum,row)=>sum+(Number(row[yKey])-(intercept+slope*Number(row[xKey])))**2,0);r2=total?1-residual/total:null}}}}const esc=value=>String(value).replace(/[&<>"']/g,char=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[char]));const sx=value=>cx+Math.max(-xLimit,Math.min(xLimit,Number(value)))/xLimit*pw/2;const sy=value=>cy-Math.max(-yLimit,Math.min(yLimit,Number(value)))/yLimit*ph/2;let svg='<svg viewBox="0 0 760 390"><line class="axis" x1="'+cx+'" y1="'+top+'" x2="'+cx+'" y2="'+(top+ph)+'"/><line class="axis" x1="'+left+'" y1="'+cy+'" x2="'+(left+pw)+'" y2="'+cy+'"/>';if(slope!==null){{const yLeft=intercept+slope*(-xLimit),yRight=intercept+slope*xLimit;svg+='<line class="trend-line" x1="'+sx(-xLimit)+'" y1="'+sy(yLeft)+'" x2="'+sx(xLimit)+'" y2="'+sy(yRight)+'" stroke="var(--ink)" stroke-width="2" stroke-dasharray="6 4"/>'}}points.forEach(row=>{{const colour=Number(row.ratio_change_pp)>=0?'var(--blue)':'var(--red)';svg+='<circle cx="'+sx(row[xKey]).toFixed(1)+'" cy="'+sy(row[yKey]).toFixed(1)+'" r="5" fill="'+colour+'"><title>'+esc(row.bank)+' | '+esc(labels[xKey])+'='+Number(row[xKey]).toFixed(2)+' | '+esc(labels[yKey])+'='+Number(row[yKey]).toFixed(2)+'</title></circle>'}});svg+='<text class="label" x="'+(left+pw/2-35)+'" y="'+(top+ph+28)+'">'+esc(labels[xKey])+'</text><text class="label" x="8" y="'+(top+ph/2-8)+'">'+esc(labels[yKey])+'</text></svg>';chart.innerHTML=svg;summary.textContent='OLS trend: '+labels[yKey]+' = '+(slope===null?'—':slope.toFixed(3)+' × '+labels[xKey]+' '+(intercept>=0?'+ ':'- ')+Math.abs(intercept).toFixed(3))+', R²='+(r2===null?'—':r2.toFixed(3))+', N='+points.length}}xSelect.addEventListener('change',render);ySelect.addEventListener('change',render);render();window.requestAnimationFrame(render)}})();</script>
<h3>Strict validation table</h3><table><thead><tr><th>Bank</th><th>Period</th><th>Capital change (%)</th><th>RWA change (%)</th><th>Ratio change (pp)</th><th>Unit</th><th>Basis</th><th>Pattern</th><th>Source</th></tr></thead><tbody>{''.join(rows) or '<tr><td colspan="9">No strict comparable observations.</td></tr>'}</tbody></table></div></details>'''


def render_html_distribution_visuals(in023, in016):
    """Render robust broad distributions and the bank/metric/year quality grid."""
    distributions = in016["distributions"]
    metrics = list(distributions)
    years = sorted({item.get("fiscal_year") for data in distributions.values() for item in data.get("broad", []) if item.get("fiscal_year") is not None})
    width, row_height, left, plot_width = 760, 100, 150, 560
    chart_rows = []
    for index, metric in enumerate(metrics):
        cohorts = {item["fiscal_year"]: item["summary"] for item in distributions[metric].get("broad", [])}
        usable = [summary for summary in cohorts.values() if summary.get("median") is not None]
        values = [value for summary in usable for value in (summary.get("p10"), summary.get("p90")) if value is not None]
        low = min(values) if values else 0
        high = max(values) if values else 1
        if high == low:
            high += 1
        top = index * row_height + 18
        bottom = top + 60
        middle = (top + bottom) / 2
        fmt_axis = lambda value: f"{value:.1f}" if abs(value) < 1000 else f"{value:.0f}"
        chart_rows.append(f'<text class="label" x="0" y="{top + 5}">{html.escape(metric)} (%)</text>')
        for tick_y, tick_value in ((top, high), (middle, (low + high) / 2), (bottom, low)):
            chart_rows.append(f'<line class="axis" x1="{left}" y1="{tick_y:.1f}" x2="{left + plot_width}" y2="{tick_y:.1f}" opacity=".25"/><text class="value" text-anchor="end" x="{left - 8}" y="{tick_y + 3:.1f}">{fmt_axis(tick_value)}</text>')
        chart_rows.append(f'<line class="axis" x1="{left}" y1="{top}" x2="{left}" y2="{bottom}"/>')
        for year_index, year in enumerate(years):
            summary = cohorts.get(year, {})
            if summary.get("median") is None:
                continue
            x = left + (plot_width * year_index / max(1, len(years) - 1))
            p10 = bottom - (summary["p10"] - low) / (high - low) * (bottom - top)
            p90 = bottom - (summary["p90"] - low) / (high - low) * (bottom - top)
            median_y = bottom - (summary["median"] - low) / (high - low) * (bottom - top)
            chart_rows.append(f'<line class="axis" x1="{x:.1f}" y1="{p10:.1f}" x2="{x:.1f}" y2="{p90:.1f}"/><circle cx="{x:.1f}" cy="{median_y:.1f}" r="4" fill="var(--blue)"><title>{html.escape(metric)} FY{year}: p10={summary["p10"]:.2f}, median={summary["median"]:.2f}, p90={summary["p90"]:.2f}, n={summary["n"]}</title></circle>')
        for year_index, year in enumerate(years):
            x = left + (plot_width * year_index / max(1, len(years) - 1))
            chart_rows.append(f'<text class="value" text-anchor="middle" x="{x:.1f}" y="{bottom + 18}">FY{year}</text>')
    summary_rows = []
    for metric in metrics:
        for cohort in distributions[metric].get("broad", []):
            summary = cohort["summary"]
            fmt = lambda value: "—" if value is None else f"{value:.2f}"
            summary_rows.append(f'<tr><td>{html.escape(metric)}</td><td>FY{cohort["fiscal_year"]}</td><td>{summary["n"]}</td><td>{fmt(summary.get("p10"))}</td><td>{fmt(summary.get("median"))}</td><td>{fmt(summary.get("p90"))}</td><td>{fmt(summary.get("iqr"))}</td><td>{fmt(summary.get("mad"))}</td><td>{html.escape(summary["status"])}</td></tr>')
    coverage = in023["coverage"]
    years = coverage["years"]
    cells = {(item["frn"], item["metric"], item["year"]): item for item in coverage["cells"]}
    heat_rows = []
    for frn in sorted({item["frn"] for item in coverage["cells"]}):
        bank = next(item["bank"] for item in coverage["cells"] if item["frn"] == frn)
        for metric in coverage["metrics"]:
            cell_html = []
            for year in years:
                state = cells[(frn, metric, year)]["state"]
                short = {"numeric": "NUM", "numeric_unknown_basis": "NUM?", "non_numeric": "TEXT", "shortened_period": "SHORT", "missing": "—"}.get(state, "—")
                cell_html.append(f'<td class="coverage-{state}" title="{state}">{short}</td>')
            heat_rows.append(f'<tr class="coverage-row" data-search="{html.escape((str(bank) + " " + metric).lower())}"><td>{html.escape(str(bank))}</td><td>{html.escape(metric)}</td>{"".join(cell_html)}</tr>')
    return f'''<details class="card wide analysis-collapsible"><summary>Robust distributions and evidence coverage</summary><div class="collapsible-content">
<p class="explanation"><strong>What this shows:</strong> broad annual distributions for the core ratios. The vertical range is p10–p90, the dot is the median, and every point carries its cohort size. Each metric has its own labelled y-axis and gridlines so the vertical position is interpretable; compare values within a metric, not across metrics. Broad coverage is the default discovery lens; the existing strict benchmark tables below remain available for validation.</p>
<div role="img" aria-label="Robust annual distribution bands for core regulatory ratios"><svg viewBox="0 0 {width} {row_height * len(metrics) + 50}">{"".join(chart_rows)}</svg></div>
<div class="legend"><span><i class="dot" style="background:var(--blue)"></i>median</span><span>vertical line = p10–p90</span><span>Each metric has its own y-axis in percentage points; N is shown in the table.</span></div>
<h3>Broad distribution summary</h3><table><thead><tr><th>Metric</th><th>Year</th><th>N</th><th>P10</th><th>Median</th><th>P90</th><th>IQR</th><th>MAD</th><th>Status</th></tr></thead><tbody>{"".join(summary_rows)}</tbody></table>
<h3>Bank × metric × year evidence coverage</h3><div class="controls"><label>Filter bank or metric <input id="in023-coverage-filter" type="search" placeholder="e.g. HSBC or CET1"></label></div><table class="in023-coverage"><thead><tr><th>Bank</th><th>Metric</th>{"".join(f"<th>FY{year}</th>" for year in years)}</tr></thead><tbody>{"".join(heat_rows)}</tbody></table>
<p class="explanation"><strong>Coverage legend:</strong> NUM = numeric annual observation; NUM? = numeric but basis unknown; TEXT = disclosed non-numeric text; SHORT = shortened annual period; — = no usable annual value. Counts: {html.escape(str(coverage.get("state_counts", {})))}.</p>
    <script>(function(){{const input=document.getElementById('in023-coverage-filter');if(!input)return;input.addEventListener('input',function(){{const q=input.value.toLowerCase();document.querySelectorAll('.coverage-row').forEach(row=>row.style.display=!q||row.dataset.search.includes(q)?'':'none')}})}})();</script></div></details>'''


def render_html_trajectory_visuals(in024):
    """Render trajectories, direction magnitudes, and latest rank panels."""
    trajectories = in024["trajectories"]
    chart_blocks = []
    heat_rows = []
    candidate_items = []
    rank_blocks = []
    all_years = sorted({point["year"] for records in trajectories.values() for record in records for point in record["years"]})
    display_all_years = [year for year in all_years if 2020 < year < 2026]
    shared_records = {}
    for records in trajectories.values():
        for record in records:
            shared_records.setdefault(str(record["bank"]), record)
    for metric, records in trajectories.items():
        metric_slug = re.sub(r"[^a-z0-9]+", "-", metric.lower()).strip("-") or "metric"
        years = [point for point in (records[0]["years"] if records else []) if 2020 < point["year"] < 2026]
        display_year_numbers = [point["year"] for point in years]
        chart_spec = validate_chart_spec(build_line_chart_spec(
            metric_slug, metric, "percentage points", records, display_year_numbers,
            description=f"{metric} bank trajectories by fiscal year",
        ))
        numeric = [point["y"] for series in chart_spec["series"] for point in series["points"] if point["y"] is not None]
        low, high = (min(numeric), max(numeric)) if numeric else (0, 1)
        if high == low:
            high += 1
        paths = []
        point_markers = []
        tick_rows = []
        top, bottom = 18, 108
        axis_fmt = lambda value: f"{value:.1f}" if abs(value) < 1000 else f"{value:.0f}"
        for tick_y, tick_value in ((top, high), ((top + bottom) / 2, (low + high) / 2), (bottom, low)):
            tick_rows.append(f'<line class="axis" x1="48" y1="{tick_y:.1f}" x2="738" y2="{tick_y:.1f}" opacity=".25"/><text class="value in024-axis-value" data-axis-position="{tick_y:.1f}" text-anchor="end" x="40" y="{tick_y + 3:.1f}">{axis_fmt(tick_value)}</text>')
        tick_rows.append(f'<line class="axis" x1="48" y1="{top}" x2="48" y2="{bottom}"/>')
        contract_series = {series["id"]: series for series in chart_spec["series"]}
        for record in records:
            points = []
            record_points = {point["x"]: point for point in contract_series[str(record["bank"])] ["points"]}
            colour = "var(--blue)" if record["score"]["label"] == "persistent_up" else "var(--red)" if record["score"]["label"] == "persistent_down" else "#9aa4ab"
            for index, year in enumerate(display_year_numbers):
                point = record_points[year]
                if point["y"] is None:
                    continue
                x = 48 + index * 690 / max(1, len(years) - 1)
                y = bottom - (point["y"] - low) / (high - low) * (bottom - top)
                points.append(f"{x:.1f},{y:.1f}")
                point_markers.append(f'<ellipse class="in024-point" data-bank="{html.escape(str(record["bank"]), quote=True)}" data-year="{year}" data-value="{point["y"]}" cx="{x:.1f}" cy="{y:.1f}" rx="2.25" ry=".18" fill="{colour}" opacity=".85"><title>{html.escape(str(record["bank"]))} | FY{year}: {point["y"]:.2f}%</title></ellipse>')
            if len(points) >= 2:
                paths.append(f'<polyline data-bank="{html.escape(str(record["bank"]), quote=True)}" points="{" ".join(points)}" fill="none" stroke="{colour}" stroke-width="1.8" data-base-stroke-width="1.8" vector-effect="non-scaling-stroke" opacity=".7"><title>{html.escape(record["bank"])} | {record["score"]["label"] or "insufficient series"} | N={record["score"]["changes"] + 1}</title></polyline>')
            changes = {item["start_year"]: item for item in record["changes"]}
            cells = []
            for year in display_all_years[:-1]:
                item = changes.get(year, {"direction": "missing", "change": None})
                value = "—" if item["change"] is None else f'{item["change"]:+.2f}'
                cells.append(f'<td class="trajectory-{item["direction"]}" title="{item["direction"]}: {value}">{value}</td>')
            heat_rows.append(f'<tr class="in024-filter-row" data-search="{html.escape((str(record["bank"]) + " " + metric).lower())}"><td>{html.escape(str(record["bank"]))}</td><td>{html.escape(metric)}</td>{"".join(cells)}<td>{html.escape(record["score"]["label"] or "insufficient series")}</td></tr>')
            score = record["score"]
            if score["status"] == "eligible":
                latest = next((point for point in reversed(record["years"]) if point["value"] is not None), None)
                candidate_items.append(record)
        labels = "".join(f'<text class="value" text-anchor="middle" x="{48 + index * 690 / max(1, len(years) - 1):.1f}" y="130">FY{year["year"]}</text>' for index, year in enumerate(years))
        default_visible = default_bank_mix(records, display_year_numbers)
        bank_controls = "".join(f'<label><input type="checkbox" class="in024-bank-toggle" data-chart="{metric_slug}" data-default-visible="{"true" if str(record["bank"]) in default_visible else "false"}" value="{html.escape(str(record["bank"]), quote=True)}"{" checked" if str(record["bank"]) in default_visible else ""}> {html.escape(str(record["bank"]))}</label>' for record in records)
        contract_json = html.escape(json.dumps(chart_spec, separators=(",", ":")), quote=True)
        chart_blocks.append(f'<article class="card wide"><h3>{html.escape(metric)}</h3><div class="in024-chart-layout"><aside class="in024-bank-list" aria-label="Banks shown for {html.escape(metric)}"><strong>Include banks</strong><span class="sub">Representative default mix: large, medium, small/specialist, international ({len(default_visible)} shown)</span>{bank_controls}</aside><div class="in024-chart-stage" data-chart-contract="{contract_json}"><div class="controls"><button type="button" class="in024-reset-zoom" data-chart="{metric_slug}">Reset zoom</button><span>Hover a point for bank, year, and value. Drag across a chart region to zoom; double-click to restore.</span></div><div class="in024-tooltip" role="status" aria-live="polite"></div><div role="img" aria-label="{html.escape(metric)} bank trajectory small multiple"><svg id="in024-chart-{metric_slug}" class="in024-trajectory-chart" data-chart="{metric_slug}" data-low="{low}" data-high="{high}" data-top="{top}" data-bottom="{bottom}" viewBox="0 0 760 145"><g class="in024-y-axis">{"".join(tick_rows)}</g><g class="in024-trajectory-layer"><line class="axis" x1="48" y1="108" x2="738" y2="108"/><g class="in024-data-layer">{"".join(paths)}{"".join(point_markers)}</g>{labels}</g><line class="in024-hover-line" x1="48" y1="18" x2="48" y2="108" style="display:none"></line><rect class="in024-brush" x="0" y="0" width="0" height="0" style="display:none"></rect></svg></div></div></div><p class="sub">FY2021–FY2025 shown; y-axis is metric-specific percentage points and rescales to the selected banks and zoom region. Missing years break the line. Persistent colours require at least {in024["metadata"]["minimum_changes"]} observed changes.</p></article>')
        panels = in024["rank_mobility"].get(metric, [])
        panel = next((item for item in reversed(panels) if item["status"] == "eligible"), None)
        if panel:
            n = panel["n"]
            lines = []
            for item in panel["records"]:
                y1 = 24 + (item["start_rank"] - 1) * 105 / max(1, n - 1)
                y2 = 24 + (item["end_rank"] - 1) * 105 / max(1, n - 1)
                colour = "var(--blue)" if item["rank_change"] < 0 else "var(--red)" if item["rank_change"] > 0 else "#9aa4ab"
                lines.append(f'<line class="in024-rank-line" data-bank="{html.escape(str(item.get("bank", item["frn"])), quote=True)}" x1="170" y1="{y1:.1f}" x2="590" y2="{y2:.1f}" stroke="{colour}" stroke-width="1.3" data-base-stroke-width="1.3" vector-effect="non-scaling-stroke"><title>{html.escape(str(item.get("bank", item["frn"]))) }: rank {item["start_rank"]} to {item["end_rank"]}</title></line>')
            rank_slug = re.sub(r"[^a-z0-9]+", "-", f"{metric}-rank".lower()).strip("-") or "rank"
            rank_spec = validate_chart_spec(build_rank_chart_spec(rank_slug, metric, panel["records"], f"FY{panel['start_year']}", f"FY{panel['end_year']}", n))
            rank_contract = html.escape(json.dumps(rank_spec, separators=(",", ":")), quote=True)
            rank_blocks.append(f'<article class="card"><h3>{html.escape(metric)}</h3><div class="controls"><button type="button" class="in024-reset-zoom" data-chart="{rank_slug}">Reset zoom</button><span>Chart.js line chart; use the wheel to zoom the rank axis.</span></div><div class="in024-chart-stage" data-chart-contract="{rank_contract}" role="img" aria-label="{html.escape(metric)} fixed-panel percentile rank chart"><svg id="in024-chart-{rank_slug}" class="in024-trajectory-chart in024-rank-chart" data-chart="{rank_slug}" data-x-min="170" data-x-max="590" data-y-min="24" data-y-max="129" viewBox="0 0 640 155"><g class="in024-trajectory-layer">{"".join(lines)}<text class="label" x="140" y="145">FY{panel["start_year"]}</text><text class="label" x="560" y="145">FY{panel["end_year"]}</text></g><rect class="in024-brush" x="0" y="0" width="0" height="0" style="display:none"></rect></svg></div><p class="sub">Fixed same-basis panel N={n}; rank 1 is highest ratio. Blue = moved toward rank 1, red = moved away. The table remains the accessible detail view.</p></article>')
    candidate_items.sort(key=lambda record: (-record["score"]["persistence_score"], -abs(record["score"]["robust_total_change"] or 0), record["bank"], record["metric"]))
    candidate_rows = []
    for record in candidate_items:
        score = record["score"]
        latest = next((point for point in reversed(record["years"]) if point["value"] is not None), None)
        note = latest.get("source_note") if latest else None
        basis = latest.get("reporting_basis") if latest else None
        candidate_rows.append(f'<tr class="in024-filter-row" data-search="{html.escape((str(record["bank"]) + " " + record["metric"]).lower())}"><td>{html.escape(str(record["bank"]))}</td><td>{html.escape(record["metric"])}</td><td>{score["label"]}</td><td>{score["persistence_score"]:.2f}</td><td>{score["changes"]}</td><td>{score["robust_total_change"]:+.2f}</td><td><details><summary>{html.escape(str(basis or "unknown basis"))}</summary>{html.escape(str(note or "No source note recorded"))}</details></td></tr>')
    year_headers = "".join(f"<th>FY{year}→FY{year + 1}</th>" for year in display_all_years[:-1])
    churn_rows = "".join(f'<tr><td>{html.escape(metric)}</td><td>FY{item["start_year"]}→FY{item["end_year"]}</td><td>{item["start_n"]}</td><td>{item["end_n"]}</td><td>{item["retained_n"]}</td><td>{len(item["entered"])}</td><td>{len(item["exited"])}</td></tr>' for metric, items in in024["coverage_churn"].items() for item in items if item["start_year"] in display_all_years and item["end_year"] in display_all_years)
    shared_default = default_bank_mix(list(shared_records.values()), display_all_years)
    shared_bank_controls = "".join(f'<label><input type="checkbox" class="in024-shared-bank-toggle" data-default-visible="{"true" if name in shared_default else "false"}" value="{html.escape(name, quote=True)}"{" checked" if name in shared_default else ""}> {html.escape(name)}</label>' for name in sorted(shared_records, key=str.casefold))
    return f'''<details class="card wide analysis-collapsible"><summary>Persistent trajectories and rank mobility</summary><div class="collapsible-content">
<p class="explanation"><strong>What this shows:</strong> whether a bank’s movement is persistent across adjacent annual observations rather than a one-year change or sample-coverage effect. Broad annual numeric observations are used for trajectories; at least {in024["metadata"]["minimum_changes"]} observed changes are required before a persistent label is assigned. Missing years remain missing and do not count as zero changes.</p>
<div class="legend"><span><i class="dot" style="background:var(--blue)"></i>persistent up: ≥75% of observed changes are up</span><span><i class="dot" style="background:var(--red)"></i>persistent down: ≥75% are down</span><span><i class="dot" style="background:#9aa4ab"></i>grey: mixed or insufficient series</span><span>blank gap: missing year, excluded from change count</span><span>y-axis ticks are metric-specific percentage points</span></div>
<div class="in024-shared-controls"><div class="controls"><strong>Bank selection</strong><button type="button" data-bank-preset="top">Representative defaults</button><button type="button" data-bank-preset="all">All banks</button><button type="button" data-bank-preset="clear">Clear</button><span class="sub">The same selection applies to every trajectory and rank chart.</span></div><div class="in024-bank-list in024-shared-bank-list" aria-label="Banks shown across trajectory and rank charts">{shared_bank_controls}</div></div>
<p class="sub">Drag across a specific plot region to zoom into clustered lines; use Reset zoom or double-click the chart to restore the full view.</p>
<div class="grid in024-trajectories">{"".join(chart_blocks)}</div>
<h3>Direction and magnitude heatmap</h3><div class="controls"><label>Filter bank or metric <input id="in024-filter" type="search" placeholder="e.g. HSBC or CET1"></label></div><table><thead><tr><th>Bank</th><th>Metric</th>{year_headers}<th>Fingerprint</th></tr></thead><tbody>{"".join(heat_rows)}</tbody></table>
<h3>Persistent review candidates</h3><p class="sub">Candidates are ordered by persistence score and absolute MAD-clipped accumulated change. This is a review queue, not a strength judgement; source notes and basis context remain visible.</p><table><thead><tr><th>Bank</th><th>Metric</th><th>Fingerprint</th><th>Persistence</th><th>Changes</th><th>Robust total change (pp)</th><th>Source / basis</th></tr></thead><tbody>{"".join(candidate_rows) or '<tr><td colspan="7">No eligible persistent candidates.</td></tr>'}</tbody></table>
<h3>Fixed-panel percentile-rank slopegraphs</h3><p class="sub">Each slopegraph uses the latest adjacent-year panel with a common reporting basis and at least 8 banks. Banks entering or leaving the broad annual sample are handled separately in the coverage churn table below.</p><div class="grid in024-ranks">{"".join(rank_blocks) or '<p>No fixed panel reached the minimum N.</p>'}</div>
<h3>Coverage churn, separate from movement</h3><table><thead><tr><th>Metric</th><th>Period</th><th>Start N</th><th>End N</th><th>Retained N</th><th>Entered</th><th>Exited</th></tr></thead><tbody>{churn_rows}</tbody></table>
<script>(function(){{const input=document.getElementById('in024-filter');if(input)input.addEventListener('input',function(){{const q=input.value.toLowerCase();document.querySelectorAll('.in024-filter-row').forEach(row=>row.style.display=!q||row.dataset.search.includes(q)?'':'none')}});const applyBanks=toggle=>{{const chart=toggle.closest('.in024-chart-layout').querySelector('.in024-trajectory-chart');const active=new Set([...toggle.closest('.in024-bank-list').querySelectorAll('.in024-bank-toggle:checked')].map(item=>item.value));chart.querySelectorAll('[data-bank]').forEach(item=>item.style.display=active.has(item.dataset.bank)?'':'none')}};document.querySelectorAll('.in024-bank-toggle').forEach(toggle=>{{toggle.addEventListener('change',()=>applyBanks(toggle));applyBanks(toggle)}});const clamp=(value,low,high)=>Math.max(low,Math.min(high,value));document.querySelectorAll('.in024-trajectory-chart').forEach(svg=>{{const layer=svg.querySelector('.in024-trajectory-layer');const axis=svg.querySelector('.in024-y-axis');const brush=svg.querySelector('.in024-brush');const hoverLine=svg.querySelector('.in024-hover-line');const tooltip=svg.closest('.in024-chart-stage').querySelector('.in024-tooltip');const xMin=Number(svg.dataset.xMin||48),xMax=Number(svg.dataset.xMax||738),yMin=Number(svg.dataset.yMin||18),yMax=Number(svg.dataset.yMax||108);const baseWidth=Number(svg.classList.contains('in024-rank-chart')?1.3:1.8);let start=null;const point=event=>{{const raw=svg.createSVGPoint();raw.x=event.clientX;raw.y=event.clientY;const transformed=raw.matrixTransform(svg.getScreenCTM().inverse());return {{x:clamp(transformed.x,xMin,xMax),y:clamp(transformed.y,yMin,yMax)}}}};const setLineWidth=scale=>{{layer.querySelectorAll('[data-base-stroke-width]').forEach(line=>line.setAttribute('stroke-width',Math.max(.7,Number(line.dataset.baseStrokeWidth||baseWidth)/Math.sqrt(scale)).toFixed(2)))}};const updateYAxis=(low,high)=>{{if(!axis)return;const formatter=value=>Math.abs(value)<1000?value.toFixed(1):value.toFixed(0);axis.querySelectorAll('.in024-axis-value').forEach(label=>{{const position=Number(label.dataset.axisPosition),fraction=(position-yMin)/(yMax-yMin);label.textContent=formatter(high-fraction*(high-low))}})}};const reset=()=>{{layer.setAttribute('transform','translate(0 0) scale(1)');setLineWidth(1);if(axis)updateYAxis(Number(svg.dataset.low),Number(svg.dataset.high));svg.classList.remove('is-zoomed')}};const updateHover=event=>{{if(start)return;const cursor=point(event);const candidates=[...svg.querySelectorAll('.in024-point')].filter(item=>item.style.display!=='none');if(!candidates.length)return;const nearest=candidates.reduce((best,item)=>{{const distance=Math.abs(Number(item.getAttribute('cx'))-cursor.x)+Math.abs(Number(item.getAttribute('cy'))-cursor.y);return distance<best.distance?{{item,distance}}:best}},{{item:candidates[0],distance:Infinity}});const x=Number(nearest.item.getAttribute('cx'));if(hoverLine){{hoverLine.setAttribute('x1',x);hoverLine.setAttribute('x2',x);hoverLine.style.display=''}}if(tooltip)tooltip.textContent=nearest.item.dataset.bank+' — FY'+nearest.item.dataset.year+': '+Number(nearest.item.dataset.value).toFixed(2)+'%'}};setLineWidth(1);svg.addEventListener('mousemove',event=>{{updateHover(event);if(!start)return;const end=point(event);brush.setAttribute('x',Math.min(start.x,end.x));brush.setAttribute('y',Math.min(start.y,end.y));brush.setAttribute('width',Math.abs(end.x-start.x));brush.setAttribute('height',Math.abs(end.y-start.y))}});svg.addEventListener('mouseleave',()=>{{if(tooltip)tooltip.textContent='';if(hoverLine)hoverLine.style.display='none'}});svg.addEventListener('mousedown',event=>{{if(event.button!==0)return;start=point(event);brush.setAttribute('x',start.x);brush.setAttribute('y',start.y);brush.setAttribute('width',0);brush.setAttribute('height',0);brush.style.display='block';event.preventDefault()}});window.addEventListener('mouseup',event=>{{if(!start)return;const end=point(event);const x1=Math.min(start.x,end.x),x2=Math.max(start.x,end.x),y1=Math.min(start.y,end.y),y2=Math.max(start.y,end.y);start=null;brush.style.display='none';if(x2-x1<20||y2-y1<10)return;const scale=Math.min((xMax-xMin)/(x2-x1),(yMax-yMin)/(y2-y1));const centreX=(xMin+xMax)/2,centreY=(yMin+yMax)/2;layer.setAttribute('transform','translate('+(centreX-scale*(x1+x2)/2)+' '+(centreY-scale*(y1+y2)/2)+') scale('+scale+')');setLineWidth(scale);if(axis){{const originalLow=Number(svg.dataset.low),originalHigh=Number(svg.dataset.high),selectedHigh=originalHigh-(y1-yMin)/(yMax-yMin)*(originalHigh-originalLow),selectedLow=originalHigh-(y2-yMin)/(yMax-yMin)*(originalHigh-originalLow);updateYAxis(Math.min(selectedLow,selectedHigh),Math.max(selectedLow,selectedHigh))}}svg.classList.add('is-zoomed')}});svg.addEventListener('dblclick',reset);const button=document.querySelector('.in024-reset-zoom[data-chart="'+svg.dataset.chart+'"]');if(button)button.addEventListener('click',reset)}});}})();</script>
<script>(function(){{const refreshDomain=chart=>{{const points=[...chart.querySelectorAll('.in024-point')].filter(item=>item.style.display!=='none').map(item=>Number(item.dataset.value));if(!points.length)return;let low=Math.min(...points),high=Math.max(...points),padding=(high-low)*.05||.5;low-=padding;high+=padding;const originalLow=Number(chart.dataset.originalLow||chart.dataset.low),originalHigh=Number(chart.dataset.originalHigh||chart.dataset.high),top=Number(chart.dataset.top||18),bottom=Number(chart.dataset.bottom||108),scale=(originalHigh-originalLow)/(high-low),translation=bottom-(originalHigh-low)*(bottom-top)/(high-low)-scale*top;chart.dataset.originalLow=originalLow;chart.dataset.originalHigh=originalHigh;chart.dataset.low=low;chart.dataset.high=high;const dataLayer=chart.querySelector('.in024-data-layer');if(dataLayer)dataLayer.setAttribute('transform','translate(0 '+translation+') scale(1 '+scale+')');const axis=chart.querySelector('.in024-y-axis');if(axis)axis.querySelectorAll('.in024-axis-value').forEach(label=>{{const fraction=(Number(label.dataset.axisPosition)-top)/(bottom-top);label.textContent=(high-fraction*(high-low)).toFixed(1)}})}};document.querySelectorAll('.in024-bank-list').forEach(list=>{{const chart=list.closest('.in024-chart-layout').querySelector('.in024-trajectory-chart');const refresh=()=>{{const checked=[...list.querySelectorAll('.in024-bank-toggle:checked')];checked.forEach(toggle=>{{const active=new Set(checked.map(item=>item.value));chart.querySelectorAll('[data-bank]').forEach(item=>item.style.display=active.has(item.dataset.bank)?'':'none')}});refreshDomain(chart)}};list.querySelectorAll('.in024-bank-toggle').forEach(toggle=>toggle.addEventListener('change',refresh));refresh();const reset=document.querySelector('.in024-reset-zoom[data-chart="'+chart.dataset.chart+'"]');if(reset)reset.addEventListener('click',()=>refreshDomain(chart))}})}})();</script></div></details>'''


def render_html_quality_views(in025):
    """Render evidence quality, cadence, coverage, and searchable source trace."""
    coverage = in025["coverage"]
    cells = {(item["frn"], item["metric"], item["year"]): item for item in coverage["cells"]}
    coverage_years = sorted(set(coverage["years"]) | set(range(2020, 2027)))
    coverage_rows = []
    for frn in sorted({item["frn"] for item in coverage["cells"]}):
        bank = next(item["bank"] for item in coverage["cells"] if item["frn"] == frn)
        for metric in coverage["metrics"]:
            rendered = []
            for year in coverage_years:
                item = cells.get((frn, metric, year), {"state": "missing", "display_value": None, "n": 0, "flags": []})
                raw_cell_value = item.get("display_value")
                cell_value = "N/A" if raw_cell_value in (None, "") or "not publicly disclosed" in str(raw_cell_value).lower() else raw_cell_value
                rendered.append(f'<td class="quality-{item["state"]}" title="{item["state"]}; source rows={item["n"]}; flags={",".join(item["flags"]) or "none"}">{html.escape(str(cell_value))}</td>')
            coverage_rows.append(f'<tr class="in025-filter-row" data-search="{html.escape((str(bank) + " " + metric).lower())}"><td>{html.escape(str(bank))}</td><td>{html.escape(metric)}</td>{"".join(rendered)}</tr>')
    cadence_rows = []
    for domain in ("annual", "interim"):
        item = in025["cadence"][domain]
        periods = ", ".join(f"{key.replace('_', ' ')}: {value}" for key, value in item["period_types"].items()) or "none"
        states = ", ".join(f"{key}: {value}" for key, value in item["quality_states"].items()) or "none"
        cadence_rows.append(f'<tr><td>{domain}</td><td>{item["banks"]}</td><td>{item["observations"]}</td><td>{html.escape(periods)}</td><td>{html.escape(states)}</td></tr>')
    trace_rows = []
    for item in in025["trace"]:
        trace_rows.append(f'<tr class="in025-filter-row" data-search="{html.escape((str(item.get("frn", "")) + " " + str(item.get("source_workbook", "")) + " " + str(item.get("sheet", "")) + " " + str(item.get("row_label", ""))).lower())}"><td>{html.escape(str(item.get("frn", "")))}</td><td>{html.escape(str(item.get("source_workbook", "")))}</td><td>{html.escape(str(item.get("sheet", "")))}</td><td>{html.escape(str(item.get("row_label", "")))}</td><td>{html.escape(str(item.get("year", "")))}</td><td>{html.escape(str(item.get("value_raw", "") or "—"))}</td><td>{html.escape(str(item.get("unit", "") or "—"))}</td><td>{html.escape(str(item.get("reporting_basis", "") or "unknown"))}</td><td>{html.escape(str(item.get("quality_status", "")))}</td></tr>')
    trace = in025["trace_completeness"]
    join = in025["join_checks"]
    return f'''<details class="card wide analysis-collapsible"><summary>Source quality and disclosure coverage</summary><div class="collapsible-content">
<p class="explanation"><strong>What this shows:</strong> where the evidence is strong enough for cross-bank interpretation and where disclosure quality limits it. Annual and interim observations are separate domains. The heatmap shows the actual disclosed value where available; unavailable or not-publicly-disclosed values are shown as N/A. Cell colour and tooltip retain the underlying quality state and comparability flags. No state is converted to zero.</p>
<div class="legend"><span class="quality-badge">N={coverage["banks"]} banks</span><span class="quality-badge">unresolved flags={sum(1 for item in coverage["cells"] if item["flags"])}</span><span class="quality-badge">trace complete={trace["complete_rows"]}/{trace["rows"]}</span><span class="quality-badge">orphan annual/interim={join["annual_orphan_rows"]}/{join["interim_orphan_rows"]}</span></div>
<h3>Cadence and quality by source domain</h3><table><thead><tr><th>Domain</th><th>Banks</th><th>Observations</th><th>Period types</th><th>Quality states</th></tr></thead><tbody>{"".join(cadence_rows)}</tbody></table>
<details class="appendix-panel"><summary>Annual evidence-quality heatmap · open for bank/year detail</summary><div class="appendix-content"><div class="controls"><label>Filter bank, workbook, metric, or FRN <input id="in025-filter" type="search" placeholder="e.g. HSBC or CET1"></label></div><table><thead><tr><th>Bank</th><th>Metric</th>{"".join(f"<th>FY{year}</th>" for year in coverage_years)}</tr></thead><tbody>{"".join(coverage_rows)}</tbody></table></div></details>
<details class="appendix-panel"><summary>Searchable source trace · open for row-level provenance</summary><div class="appendix-content"><p class="sub">Trace rows retain the FRN, workbook, sheet, source row, period, raw value, unit, reporting basis, and quality state. Interim rows remain identifiable by their source domain and period label.</p><table><thead><tr><th>FRN</th><th>Workbook</th><th>Sheet</th><th>Row label</th><th>Period</th><th>Raw value</th><th>Unit</th><th>Basis</th><th>Quality</th></tr></thead><tbody>{"".join(trace_rows)}</tbody></table></div></details>
<script>(function(){{const input=document.getElementById('in025-filter');if(!input)return;input.addEventListener('input',function(){{const q=input.value.toLowerCase();document.querySelectorAll('.in025-filter-row').forEach(row=>row.style.display=!q||row.dataset.search.includes(q)?'':'none')}})}})();</script></div></details>'''


def render_pdf_analysis_lines(payload):
    """Render a concise text version suitable for the existing PDF writer."""
    in009 = payload["in009"]
    in010 = payload["in010"]["parent_groups"]
    lines = ["Core-ratio coverage"]
    outliers = [item for mode in ("broad", "strict") for item in payload["in009"]["outliers"].get(mode, [])]
    declining_headroom = [item for item in payload.get("in021", {}).get("records", [])
                          if item.get("status") == "screened" and item.get("trend_direction") == "declining"]
    quality = payload.get("in025", {})
    flags = sum(1 for item in quality.get("coverage", {}).get("cells", []) if item.get("flags"))
    trace = quality.get("trace_completeness", {})
    lines += [
        "Dashboard watchlist",
        f"Review prompts: {len(outliers)} outlier records, {len(declining_headroom)} declining-headroom records, {flags} quality-flagged cells",
        f"Evidence freshness: trace complete {trace.get('complete_rows', 0)}/{trace.get('rows', 0)} rows",
    ]
    for metric in in009["metadata"]["metrics"]:
        broad = in009["coverage"][metric]["broad"]["banks"]
        strict = in009["coverage"][metric]["strict"]["banks"]
        lines.append(f"{metric}: broad={broad} banks, strict={strict} banks")
    if payload.get("in022"):
        decomposition = payload["in022"]["broad"]
        coverage = decomposition["coverage"]
        lines += [
            "CET1 ratio movement decomposition",
            "Broad screening: capital and RWA relative changes explain the observed ratio movement; not causal.",
            f"FY{decomposition['start_year']}→FY{decomposition['end_year']} | comparable N={coverage.get('comparable_banks', 0)} | exclusions={coverage.get('exclusions', {})}",
            {"type": "decomposition_chart", **decomposition},
        ]
    if payload.get("in023"):
        distributions = payload["in016"]["distributions"]
        latest = {}
        for metric, data in distributions.items():
            cohorts = [item for item in data.get("broad", []) if item["summary"].get("median") is not None]
            if cohorts:
                latest[metric] = max(cohorts, key=lambda item: item.get("fiscal_year", 0))
        lines += [
            "Robust distributions and evidence coverage",
            "Broad discovery view: p10-p90 range and median; values are not arithmetic means.",
            f"Coverage states: {payload['in023']['coverage'].get('state_counts', {})}",
            {"type": "distribution_chart", "distributions": latest},
        ]
    if payload.get("in024"):
        candidates = []
        for metric, records in payload["in024"]["trajectories"].items():
            for record in records:
                score = record["score"]
                if score["status"] == "eligible" and score["label"] in ("persistent_up", "persistent_down"):
                    candidates.append(record)
        candidates.sort(key=lambda record: (-record["score"]["persistence_score"], -abs(record["score"]["robust_total_change"] or 0), record["bank"], record["metric"]))
        lines += [
            "Persistent trajectories and rank mobility",
            "Broad annual fingerprints require at least three observed changes; missing years are not zero; totals are MAD-clipped.",
            {"type": "trajectory_candidates", "candidates": candidates[:24]},
        ]
    if payload.get("in025"):
        cadence = payload["in025"]["cadence"]
        trace = payload["in025"]["trace_completeness"]
        joins = payload["in025"]["join_checks"]
        lines += [
            "Source quality and disclosure coverage",
            f"Annual: {cadence['annual']['banks']} banks / {cadence['annual']['observations']} observations; interim: {cadence['interim']['banks']} banks / {cadence['interim']['observations']} observations.",
            f"Trace completeness={trace['complete_rows']}/{trace['rows']}; orphan annual/interim rows={joins['annual_orphan_rows']}/{joins['interim_orphan_rows']}.",
        ]
    headroom = payload.get("in021")
    if headroom:
        validate_payload(headroom["source_database"], headroom)
        lines.append("Regulatory headroom trajectory")
        lines.append("Screening only: current ratio minus applicable floor, alongside observed multi-year change; no forecast.")
        shown = headroom["records"][:24]
        for item in shown:
            current = "—" if item["current_value"] is None else f"{item['current_value']:.2f}%"
            floor = "—" if item["regulatory_floor"] is None else f"{item['regulatory_floor']:.2f}%"
            head = "—" if item["current_headroom"] is None else f"{item['current_headroom']:.2f}pp"
            change = "—" if item["trend_change"] is None else f"{item['trend_change']:+.2f}pp"
            lines.append(f"{item['bank']} | {item['metric']} | FY{item['latest_year']} | current={current} | floor={floor} | headroom={head} | change={change} | {item['status']}")
        if len(headroom["records"]) > len(shown):
            lines.append(f"Additional screened records: {len(headroom['records']) - len(shown)}; see the interactive deliverable.")
    lines.append("Outlier investigation")
    outliers = [item for mode in ("broad", "strict") for item in in009["outliers"][mode]]
    for item in outliers[:12]:
        lines.append(f"{item['metric']} | {item['bank']} | FY{item['fiscal_year']} | {item['value']} | {'; '.join(item['reasons'])} | {item.get('comparability_status', 'unknown')}")
    if not outliers:
        lines.append("No outliers flagged")
    lines.append("Parent-group dispersion and agreement")
    for metric, modes in in010.items():
        for group in modes["strict"]:
            level = group["latest_level"]
            trends = group["trends"]
            if not trends:
                continue
            latest = trends[-1]["direction"]
            lines.append(f"{metric} | {group['group']} | {level.get('status', 'unavailable')} | latest trend: {latest}")
    if payload.get("in012"):
        lines.append("Absolute capital/RWA analysis")
        for metric, data in payload["in012"]["absolute_metrics"].items():
            coverage = data["coverage"]
            scaled = data.get("scale_adjusted_coverage", {})
            exclusions = ", ".join(f"{key}: {value}" for key, value in scaled.get("exclusions", {}).items()) or "none"
            lines.append(
                f"{metric} | {coverage.get('known_unit_banks', 0)} known-unit banks | "
                f"{scaled.get('banks', 0)} scale-adjusted banks | exclusions={exclusions}"
            )
    if payload.get("in040"):
        in040 = payload["in040"]
        banks = in040["metadata"]["banks"]
        stage_coverage = in040["loan_concentration_quality"]["coverage"]
        rwa_coverage = in040["rwa_density"]["coverage"]
        lines.append("Loan concentration, asset quality, and RWA density")
        lines.append(
            f"Loan/asset-quality: {stage_coverage['banks_with_stage_data']} banks with IFRS 9 stage data, "
            f"{stage_coverage['banks_with_coverage_or_npl_disclosure']} with a disclosed coverage/NPL ratio."
        )
        lines.append(
            f"RWA density: {rwa_coverage['bank_years_with_rwa_to_assets']} bank-years with RWA/assets, "
            f"{rwa_coverage['bank_years_with_category_breakdown']} bank-years with a category breakdown."
        )
        rwa_to_assets = in040["rwa_density"]["rwa_to_assets_pct"]
        for frn, years in sorted(rwa_to_assets.items(), key=lambda kv: banks.get(kv[0], ""))[:24]:
            year = max(years)
            lines.append(f"{banks.get(frn, frn)} | FY{year} | RWA/assets={years[year]}%")
    if payload.get("interim"):
        coverage = payload["interim"]["coverage"]
        lines.append("Interim disclosure coverage")
        lines.append(f"{coverage['banks']} banks | {coverage['observations']} observations | numeric={coverage['numeric_observations']} | source-register rows={coverage['source_register_rows']}")
    if payload.get("in016"):
        lines.append("Distribution benchmarks (strict comparable population)")
        for metric, modes in payload["in016"]["distributions"].items():
            cohorts = modes["strict"]
            eligible_cohorts = [item for item in cohorts if item["summary"].get("n", 0) >= 8]
            chosen = max(eligible_cohorts or cohorts, key=lambda item: (item.get("fiscal_year") or 0, item.get("reporting_basis") or "")) if cohorts else None
            summary = chosen["summary"] if chosen else {"n": 0, "median": None, "iqr": None}
            median = "—" if summary["median"] is None else f"{summary['median']:.2f}"
            iqr = "—" if summary["iqr"] is None else f"{summary['iqr']:.2f}"
            lines.append(f"{metric} | FY{chosen['fiscal_year'] if chosen else '—'} | {chosen.get('reporting_basis', '—') if chosen else '—'} | n={summary['n']} | median={median} | IQR={iqr}")
        lines.append("Absolute-value distribution benchmarks")
        for metric, cohorts in payload["in016"].get("absolute_distributions", {}).items():
            usable = [item for item in cohorts if item["summary"].get("n", 0) >= 8]
            chosen = max(usable or cohorts, key=lambda item: (item.get("fiscal_year") or 0, item.get("amount_unit") or "")) if cohorts else None
            summary = chosen["summary"] if chosen else {"n": 0, "median": None, "iqr": None}
            median = "—" if summary["median"] is None else f"{summary['median']:.2f}"
            iqr = "—" if summary["iqr"] is None else f"{summary['iqr']:.2f}"
            lines.append(f"{metric} | FY{chosen['fiscal_year'] if chosen else '—'} | {chosen.get('amount_unit', '—') if chosen else '—'} | n={summary['n']} | median={median} | IQR={iqr}")
        lines.append("Fixed-panel rank movement")
        for metric, movements in payload["in016"].get("rank_movement", {}).items():
            usable = [item for item in movements if item.get("n", 0) >= 8]
            chosen = max(usable or movements, key=lambda item: (item.get("end_year") or 0, item.get("reporting_basis") or "")) if movements else None
            if chosen:
                lines.append(f"{metric} | FY{chosen['start_year']}→FY{chosen['end_year']} | n={chosen['n']} | up={chosen['up']} | down={chosen['down']} | same={chosen['same']} | {chosen['status']}")
        coverage = payload["in016"].get("group_benchmark_coverage", {})
        lines.append("Group-model benchmark guardrails")
        for item in coverage.values():
            lines.append(f"{item['model']} | groups={len(item['groups'])} | eligible={item['eligible']} | suppressed={item['suppressed']} | minimum_n={item['minimum_n']}")
    if payload.get("in017"):
        lines.append("Source lineage and data-quality monitoring")
        for item in payload["in017"].get("quality_facts", []):
            lines.append(f"{item['metric']} | banks={item['banks']} | observations={item['observations']} | numeric={item['numeric']} | missing={item['missing']} | non-numeric={item['non_numeric_disclosure']} | structure={item['structural_status']}")
        checks = payload["in017"].get("structural_checks", [])
        lines.append(f"Structural checks: {sum(item['status'] == 'pass' for item in checks)} passed, {sum(item['status'] == 'fail' for item in checks)} failed")
    return lines
