"""Build the fixed PDF companion for the IN-006 client deliverable.

The writer deliberately uses only the Python standard library so the snapshot
can be regenerated wherever the existing extraction scripts run.
"""

import os
import re
import textwrap
import argparse
from datetime import datetime, timezone
from statistics import median

from analyze_trends import METRICS, extract, pairwise_counts
import build_insights_db
from analysis_queries import AnalysisQueries
from in011_deliverables import build_in011_payload, render_pdf_analysis_lines
from in022_ratio_decomposition import fit_trend


ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
OUTPUT = os.path.join(ROOT, "wayfinder", "insights", "deliverable", "uk_bank_insights.pdf")
DEFAULT_DB = os.path.join(ROOT, "research", "insights.db")
DEFAULT_CLUSTERS = os.path.join(ROOT, "research", "bank_clusters.csv")

# Same curated display-name map as build_in005_prototype.py's GROUP_VERDICTS,
# but this PDF only needs the short display name (no capital/cash/note
# verdict) - kept as a separate, smaller constant rather than importing the
# HTML generator's dict, since the two deliverables' content isn't meant to
# be coupled beyond sharing the underlying data-access helpers.
GROUP_DISPLAY_NAMES = {
    "HSBC group": "HSBC",
    "NatWest group": "NatWest",
    "Lloyds Banking Group": "Lloyds",
    "Banco Santander S.A.": "Santander",
    "UBS group (current)": "UBS / Credit Suisse",
    "JPMorgan Chase group": "JPMorgan",
}


def metric_series(db_path):
    specs = dict(METRICS)
    specs["MREL ratio"] = ("MREL Ratio", re.compile(r"MREL.*ratio|ratio.*MREL", re.I), ())
    specs["RWA"] = (
        "Total RWAs",
        re.compile(r"total|overall", re.I),
        ("credit risk", "market risk", "operational risk", "crwa", "mrwa", "orwa"),
    )
    from analysis_queries import AnalysisQueries
    rows = AnalysisQueries(db_path).observations()
    result = {}
    for metric, spec in specs.items():
        values, _ = extract(rows, metric, spec)
        result[metric] = values
    return result


def counts(series, start, end):
    """Thin wrapper over analyze_trends.pairwise_counts() returning the
    (down, up, n) tuple this module's callers expect - kept as a local name
    so the appendix-table loop below doesn't need to change, but the actual
    counting logic is the single shared implementation, not a local copy."""
    c = pairwise_counts(series, start, end)
    return c["down"], c["up"], c["n"]


def headline_signal_lines(series):
    """Builds the "Headline signals" bullet text FROM CURRENT DATABASE
    VALUES via pairwise_counts() - no figure here is hand-typed. Per
    CODING_STANDARDS.md ("Avoid hardcoding data-derived figures in
    generated deliverables"): this is computed fresh on every run against
    whatever --db points at, so a headline count can never silently drift
    from what the appendix table (built the same way, just below) reports."""
    rwa_23 = pairwise_counts(series["RWA"], 2022, 2023)
    rwa_24 = pairwise_counts(series["RWA"], 2023, 2024)
    cet1_23 = pairwise_counts(series["CET1 ratio"], 2022, 2023)
    cet1_24 = pairwise_counts(series["CET1 ratio"], 2023, 2024)
    cet1_25 = pairwise_counts(series["CET1 ratio"], 2024, 2025)
    ocf_24 = pairwise_counts(series["Operating cash flow"], 2023, 2024)
    ocf_25 = pairwise_counts(series["Operating cash flow"], 2024, 2025)
    return [
        f"- Risk-weighted assets increased for {rwa_23['up']} of {rwa_23['n']} comparable entities in FY2022->FY2023",
        f"  and {rwa_24['up']} of {rwa_24['n']} in FY2023->FY2024.",
        f"- CET1 increased for {cet1_23['up']} of {cet1_23['n']} entities in FY2022->FY2023, then declined for {cet1_24['down']} of",
        f"  {cet1_24['n']} in FY2023->FY2024 and {cet1_25['down']} of {cet1_25['n']} in FY2024->FY2025.",
        f"- Operating cash flow improved for {ocf_24['up']} of {ocf_24['n']} entities in FY2023->FY2024, followed",
        f"  by declines for {ocf_25['down']} of {ocf_25['n']} in FY2024->FY2025.",
    ]


def five_year_summary_lines(series):
    """Return a compact, computed executive view of the five-year snapshot.

    The small horizontal bars are deliberately text-based: they survive the
    existing dependency-free PDF writer and remain readable when copied from
    the PDF. Values are annual medians of available numeric entity series;
    n is shown so a sparse metric cannot look as representative as CET1.
    """
    years = [2021, 2022, 2023, 2024, 2025]
    lines = [
        "Five-year movement at a glance",
        "The figures below use available numeric entity observations for each year; n is the",
        "number of entities contributing to that year's median. They describe movement in the",
        "disclosure population, not a like-for-like panel unless the comparison says so.",
        "",
        "Median ratio trajectory (each # is approximately 5 percentage points)",
    ]
    for metric in ("CET1 ratio", "Tier 1 ratio", "Total capital ratio", "Leverage ratio"):
        values = series.get(metric, {})
        cells = []
        for year in years:
            numbers = [float(years_map[year]) for years_map in values.values() if year in years_map]
            if numbers:
                value = median(numbers)
                cells.append(f"FY{str(year)[-2:]} {value:5.1f}% n={len(numbers):3d} {'#' * max(1, min(20, round(value / 5)))}")
            else:
                cells.append(f"FY{str(year)[-2:]}   n=  0 —")
        lines.append(metric + ":")
        lines.extend("  " + cell for cell in cells)
    lines += [
        "",
        "Five-year comparable movement (FY2021->FY2025)",
    ]
    for metric in ("CET1 ratio", "Total capital ratio", "RWA", "Operating cash flow"):
        c = pairwise_counts(series.get(metric, {}), 2021, 2025)
        lines.append(f"- {metric}: {c['up']} increased / {c['down']} declined / {c['n']} comparable entities")
    return lines


def year_on_year_lines(series):
    """Move the full year-pair metric changes into the main analysis body."""
    years = [2021, 2022, 2023, 2024, 2025]
    lines = ["YEAR-ON-YEAR MOVEMENT BY METRIC", "Counts show entities declining / increasing / comparable for each selected pair."]
    for metric, values in series.items():
        lines += ["", metric]
        for start_index, start in enumerate(years):
            for end in years[start_index + 1:]:
                down, up, comparable = counts(values, start, end)
                lines.append(f"FY{start}->FY{end}: {down} declining / {up} increasing / {comparable} comparable")
    return lines


def executive_chart_data(series):
    """Prepare chart data from the same computed series as the summary text."""
    years = [2021, 2022, 2023, 2024, 2025]
    trends = []
    for metric in ("CET1 ratio", "Tier 1 ratio", "Total capital ratio", "Leverage ratio"):
        values = series.get(metric, {})
        medians = []
        for year in years:
            numbers = [float(item[year]) for item in values.values() if year in item]
            medians.append(round(median(numbers), 2) if numbers else None)
        trends.append((metric, medians))
    movements = []
    for metric in ("CET1 ratio", "Total capital ratio", "RWA", "Operating cash flow"):
        c = pairwise_counts(series.get(metric, {}), 2021, 2025)
        movements.append((metric, c["up"], c["down"], c["n"]))
    return {"years": years, "trends": trends, "movements": movements}


def _snapshot_date_label(db_path):
    """Return a human-readable snapshot date computed from the database's own
    refresh metadata (`metrics_built_at`), not a hardcoded literal - the
    cover page previously said "29 August 2026" no matter how many times the
    PDF was actually regenerated afterward. Falls back to the current date
    only if the database genuinely has no refresh metadata yet (a fresh
    database that hasn't been refreshed), so the label is never blank."""
    built_at = AnalysisQueries(db_path).refresh_metadata().get("metrics_built_at")
    if built_at:
        try:
            when = datetime.fromisoformat(built_at)
        except ValueError:
            when = datetime.now(timezone.utc)
    else:
        when = datetime.now(timezone.utc)
    return f"{when.day} {when.strftime('%B %Y')}"


def executive_pages(series, headline, snapshot_date):
    """Build two readable executive pages with vector chart markers."""
    chart = executive_chart_data(series)
    first = [
        f"UK BANK INSIGHTS - {headline.upper()}", f"Fixed snapshot | {snapshot_date}", "",
        "EXECUTIVE SUMMARY", "Five-year view: FY2021-FY2025", "",
        "This summary covers 145 regulated UK banking entities. It highlights changes",
        "in the disclosure population and shows sample sizes so sparse metrics are not",
        "mistaken for full-market evidence. Ratios are not mixed with cash-flow or RWA",
        "amounts, and comparable movement is based only on entities with both years.", "",
        "Median regulatory-ratio trajectory | available numeric observations",
        {"type": "line_chart", **chart},
        "Note: medians are descriptive, not regulatory pass/fail tests; basis and entity scope vary.",
    ]
    second = [
        "EXECUTIVE SUMMARY (CONTINUED)", "What changed over five years", "",
        "The movement chart compares FY2021 with FY2025 where the same entity has both",
        "values. It is a fixed-panel direction count, not a claim that every entity was",
        "available in every intervening year.", "",
        {"type": "movement_chart", **chart}, "",
        *headline_signal_lines(series), "",
        "Reading the charts", "A rising median indicates a higher typical disclosed value",
        "among the available entities. It does not establish causation, strength, or",
        "compliance. The detailed year-pair tables and source notes follow in the report.",
    ]
    return [first, second]


def peer_groups_line(cluster_rows):
    """Replaces the previously-hardcoded "95 entities | ... 18 ... | ... 32
    entities" text with counts computed from the current cluster CSV, via
    the same build_insights_db.cluster_size_summary() helper
    build_in005_prototype.py uses for its own cluster payload."""
    sizes, insufficient = build_insights_db.cluster_size_summary(cluster_rows)
    lower = sizes.get("0", 0)
    higher = sizes.get("1", 0)
    return (
        f"Established/lower-buffer cluster: {lower} entities | Specialist/higher-buffer cluster: {higher}",
        f"entities | Unspecified because of insufficient comparable data: {insufficient} entities.",
    )


def parent_group_coverage_line(db_path):
    """Replaces the previously-hardcoded "HSBC (4), NatWest (3), ..." text
    with a list computed from parent_group_lookup via the shared
    multi_entity_groups() helper - see build_in005_prototype.py's
    GROUP_VERDICTS/compute_groups_payload() for the fuller version of this
    same fix (this PDF only needs the name+count, no capital/cash verdict)."""
    from analysis_queries import AnalysisQueries
    groups = AnalysisQueries(db_path).groups()
    multi = build_insights_db.multi_entity_groups(groups)
    parts = []
    for ultimate_group, members in multi:
        display_name = GROUP_DISPLAY_NAMES.get(ultimate_group)
        if display_name is None:
            print(f"  !! multi-entity group {ultimate_group!r} ({len(members)} entities) has no "
                  f"curated display name in GROUP_DISPLAY_NAMES - omitted from the PDF, not guessed")
            continue
        parts.append(f"{display_name} ({len(members)})")
    if len(parts) > 1:
        joined = ", ".join(parts[:-1]) + f", and {parts[-1]}"
    else:
        joined = parts[0] if parts else "none"
    return f"{joined} legal entities are available for comparative drill-down."


def pdf_escape(value):
    return value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def make_pages(lines):
    wrapped = []
    for line in lines:
        if isinstance(line, dict):
            wrapped.append(line)
            continue
        if not line:
            wrapped.append("")
        else:
            wrapped.extend(textwrap.wrap(line, width=96, break_long_words=False) or [""])
    return [wrapped[index:index + 47] for index in range(0, len(wrapped), 47)]


def write_pdf(pages, output_path=OUTPUT):
    objects = []

    def add(body):
        objects.append(body)
        return len(objects)

    font_id = add(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    page_ids = []
    content_ids = []
    for page in pages:
        commands = ["BT", "/F1 10 Tf", "50 760 Td"]
        y = 760
        for line in page:
            if isinstance(line, dict):
                commands += ["ET"]
                if line["type"] == "line_chart":
                    commands += _line_chart_commands(line, 50, y - 8)
                    y -= 205
                elif line["type"] == "movement_chart":
                    commands += _movement_chart_commands(line, 50, y - 8)
                    y -= 190
                elif line["type"] == "decomposition_chart":
                    commands += _decomposition_chart_commands(line, 50, y - 8)
                    y -= 220
                elif line["type"] == "distribution_chart":
                    commands += _distribution_chart_commands(line, 50, y - 8)
                    y -= 205
                elif line["type"] == "trajectory_candidates":
                    commands += _trajectory_candidate_commands(line, 50, y - 8)
                    y -= 180
                commands += ["BT", "/F1 10 Tf", f"50 {y} Td"]
                continue
            commands.append(f"({pdf_escape(line)}) Tj")
            commands.append("0 -15 Td")
            y -= 15
        commands.append("ET")
        content = "\n".join(commands).encode("latin-1", "replace")
        content_ids.append(add(f"<< /Length {len(content)} >>\nstream\n".encode() + content + b"\nendstream"))
        page_ids.append(None)
    pages_id = add(b"")
    for index, content_id in enumerate(content_ids):
        page_ids[index] = add(
            f"<< /Type /Page /Parent {pages_id} 0 R /MediaBox [0 0 612 792] "
            f"/Resources << /Font << /F1 {font_id} 0 R >> >> /Contents {content_id} 0 R >>".encode()
        )
    objects[pages_id - 1] = (
        f"<< /Type /Pages /Kids [{' '.join(f'{page_id} 0 R' for page_id in page_ids)}] "
        f"/Count {len(page_ids)} >>"
    ).encode()
    catalog_id = add(f"<< /Type /Catalog /Pages {pages_id} 0 R >>".encode())

    output = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for index, body in enumerate(objects, 1):
        offsets.append(len(output))
        output.extend(f"{index} 0 obj\n".encode())
        output.extend(body)
        output.extend(b"\nendobj\n")
    xref = len(output)
    output.extend(f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode())
    output.extend("".join(f"{offset:010d} 00000 n \n" for offset in offsets[1:]).encode())
    output.extend(f"trailer\n<< /Size {len(objects) + 1} /Root {catalog_id} 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode())
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "wb") as handle:
        handle.write(output)


def _pdf_text(text, x, y, size=8):
    return ["BT", f"/F1 {size} Tf", f"{x} {y} Td", f"({pdf_escape(str(text))}) Tj", "ET"]


def _line_chart_commands(chart, x, y):
    width, height = 500, 150
    years = chart["years"]
    commands = ["0.85 G", f"{x} {y - height} m", f"{x + width} {y - height} l S", f"{x} {y} m", f"{x} {y - height} l S"]
    all_values = [value for _, values in chart["trends"] for value in values if value is not None]
    maximum = max(all_values or [1]) * 1.15
    for index, year in enumerate(years):
        px = x + index * width / (len(years) - 1)
        commands += ["0.9 G", f"{px:.1f} {y - height} m", f"{px:.1f} {y} l S"]
        commands += _pdf_text(f"FY{year}", px - 12, y - height - 14)
    colours = [(0.08, 0.32, 0.55), (0.75, 0.44, 0.08), (0.35, 0.55, 0.25), (0.50, 0.22, 0.42)]
    for trend_index, ((metric, values), colour) in enumerate(zip(chart["trends"], colours)):
        commands += [f"{colour[0]} {colour[1]} {colour[2]} RG"]
        previous = None
        for index, value in enumerate(values):
            if value is None:
                previous = None
                continue
            px = x + index * width / (len(years) - 1)
            py = y - (value / maximum) * height
            if previous is not None:
                commands += [f"{previous[0]:.1f} {previous[1]:.1f} m", f"{px:.1f} {py:.1f} l S"]
            commands += [f"{px - 2:.1f} {py - 2:.1f} {4} {4} re f"]
            previous = (px, py)
        # Use the loop's own index, not `.index((metric, values))` - two
        # metrics with identical (possibly all-None) `values` lists would
        # make `.index()` return the FIRST match's position for both,
        # silently overlapping their legend labels at the same y-coordinate.
        commands += _pdf_text(metric, x + width + 12, y - 12 - trend_index * 16, 8)
    commands += _pdf_text("Median percentage", x, y + 14, 8)
    return commands


def _movement_chart_commands(chart, x, y):
    width, height = 500, 145
    maximum = max([max(up, down) for _, up, down, _ in chart["movements"]] or [1])
    commands = ["0.85 G", f"{x} {y - height} m", f"{x + width} {y - height} l S"]
    for index, (metric, up, down, n) in enumerate(chart["movements"]):
        base = y - 25 - index * 31
        up_width = up / maximum * 190
        down_width = down / maximum * 190
        commands += ["0.12 0.42 0.65 rg", f"{x + 155} {base} {up_width:.1f} 10 re f", "0.72 0.25 0.22 rg", f"{x + 360} {base} {down_width:.1f} 10 re f"]
        commands += _pdf_text(metric, x, base + 1, 8)
        commands += _pdf_text(f"up {up}", x + 155 + up_width + 5, base + 1, 8)
        commands += _pdf_text(f"down {down}", x + 360 + down_width + 5, base + 1, 8)
        commands += _pdf_text(f"n={n}", x + 470, base + 1, 8)
    commands += _pdf_text("FY2021 -> FY2025 comparable entity direction", x, y + 14, 8)
    return commands


def _decomposition_chart_commands(chart, x, y):
    """Render a compact vector scatter plot for the PDF companion."""
    width, height = 500, 170
    records = chart.get("records", [])
    x_values = sorted(abs(float(item["rwa_change_pct"])) for item in records)
    y_values = sorted(abs(float(item["capital_change_pct"])) for item in records)
    def limit(values):
        if not values:
            return 1.0
        index = min(len(values) - 1, round((len(values) - 1) * 0.95))
        return max(1.0, values[index]) * 1.1
    x_limit, y_limit = limit(x_values), limit(y_values)
    mid_x, mid_y = x + width / 2, y - height / 2
    commands = ["0.85 G", f"{x} {y - height} m", f"{x + width} {y - height} l S", f"{x} {y} m", f"{x} {y - height} l S", f"{mid_x} {y - height} m", f"{mid_x} {y} l S", f"{x} {mid_y} m", f"{x + width} {mid_y} l S"]
    fit = fit_trend(records, "rwa_change_pct", "capital_change_pct")
    if fit["slope"] is not None:
        left_y = max(-y_limit, min(y_limit, fit["intercept"] + fit["slope"] * -x_limit))
        right_y = max(-y_limit, min(y_limit, fit["intercept"] + fit["slope"] * x_limit))
        commands += ["0.15 0.15 0.15 RG", f"{x} {mid_y - left_y / y_limit * height / 2:.1f} m", f"{x + width} {mid_y - right_y / y_limit * height / 2:.1f} l S"]
    for item in records:
        rwa_change = max(-x_limit, min(x_limit, float(item["rwa_change_pct"])))
        capital_change = max(-y_limit, min(y_limit, float(item["capital_change_pct"])))
        px = mid_x + rwa_change / x_limit * width / 2
        py = mid_y - capital_change / y_limit * height / 2
        colour = "0.12 0.42 0.65 rg" if item["ratio_change_pp"] >= 0 else "0.72 0.25 0.22 rg"
        commands += [colour, f"{px - 2:.1f} {py - 2:.1f} 4 4 re f"]
    commands += _pdf_text("RWA change (%)", mid_x - 28, y - height - 16, 8)
    commands += _pdf_text("CET1 capital change (%)", x, y + 12, 8)
    r_squared = "—" if fit["r_squared"] is None else f"{fit['r_squared']:.3f}"
    commands += _pdf_text(f"Broad comparable N={chart.get('coverage', {}).get('comparable_banks', 0)}; OLS R2={r_squared}; plotting range is robustly clipped", x, y - height - 30, 7)
    return commands


def _distribution_chart_commands(chart, x, y):
    """Render latest broad p10/median/p90 values without hover dependence."""
    width, row_height = 500, 30
    rows = list(chart.get("distributions", {}).items())
    commands = []
    for index, (metric, cohort) in enumerate(rows):
        summary = cohort["summary"]
        values = [summary.get(key) for key in ("p10", "p90") if summary.get(key) is not None]
        if not values or summary.get("median") is None:
            continue
        low, high = min(values), max(values)
        if high == low:
            high += 1
        base = y - 20 - index * row_height
        px_low = x + 150
        px_high = x + 450
        median_x = px_low + (summary["median"] - low) / (high - low) * (px_high - px_low)
        commands += ["0.12 0.42 0.65 RG", f"{px_low:.1f} {base} m", f"{px_high:.1f} {base} l S", f"{median_x:.1f} {base - 3} {6} {6} re f"]
        commands += _pdf_text(metric, x, base - 2, 8)
        commands += _pdf_text(f"FY{cohort.get('fiscal_year', '—')} n={summary.get('n', 0)} median={summary['median']:.2f}", x + 150, base - 13, 7)
    commands += _pdf_text("Each line spans p10-p90; dot marks median", x, y + 10, 8)
    return commands


def _trajectory_candidate_commands(chart, x, y):
    """Render a concise persistent-trajectory candidate table for PDF."""
    commands = _pdf_text("Persistent review candidates | broad annual series", x, y, 9)
    current_y = y - 18
    for item in chart.get("candidates", []):
        score = item["score"]
        text = f'{item["bank"]} | {item["metric"]} | {score["label"]} | persistence={score["persistence_score"]:.2f} | changes={score["changes"]} | robust total={score["robust_total_change"]:+.2f}pp'
        commands += _pdf_text(text[:125], x, current_y, 7)
        current_y -= 12
    if not chart.get("candidates"):
        commands += _pdf_text("No eligible persistent candidates.", x, current_y, 8)
    return commands


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=DEFAULT_DB, help="SQLite source-of-truth database")
    parser.add_argument("--clusters", default=DEFAULT_CLUSTERS, help="derived cluster CSV")
    parser.add_argument("--out", default=OUTPUT, help="PDF output path")
    parser.add_argument("--headline", default="Capital, liquidity and group movement",
                        help="headline shown in the PDF title")
    args = parser.parse_args()
    cluster_rows = build_insights_db.load_cluster_rows(args.clusters)
    build_insights_db.validate_cluster_inputs(args.db, cluster_rows, args.clusters)
    in011 = build_in011_payload(args.db)
    series = metric_series(args.db)
    snapshot_date = _snapshot_date_label(args.db)
    executive = executive_pages(series, args.headline, snapshot_date)
    lines = [
        *year_on_year_lines(series),
        "",
        *render_pdf_analysis_lines(in011),
        "",
        "Headline signals",
        *headline_signal_lines(series),
        "",
        "Peer groups",
        *peer_groups_line(cluster_rows),
        "",
        "Metric guide",
        "CET1, Tier 1 and Total capital ratios: regulatory capital relative to risk-weighted",
        "assets. Leverage ratio: Tier 1 capital relative to total exposure without risk weighting.",
        "LCR: high-quality liquid assets relative to stressed 30-day net cash outflows.",
        "NSFR: available stable funding relative to required stable funding. MREL: loss-absorbing",
        "and recapitalisation resources relative to the applicable exposure measure.",
        "RWA: risk-weighted assets, an amount rather than a percentage. Operating cash flow:",
        "net cash generated by or used in operating activities.",
        "",
        "Parent-group coverage",
        parent_group_coverage_line(args.db),
        "",
        "Appendix note: all metric/year combinations are listed in the year-on-year section above.",
    ]
    write_pdf([*executive, *make_pages(lines)], args.out)
    print(f"Wrote {args.out} ({os.path.getsize(args.out)} bytes)")


if __name__ == "__main__":
    main()
