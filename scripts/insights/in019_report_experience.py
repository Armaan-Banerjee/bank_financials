"""Generate the governed Power BI report-experience hand-off for IN-019."""

import argparse
import csv
import json
import os
from datetime import datetime, timezone

import build_insights_db
from in009_analysis import build_in009_payload
from in018_powerbi import build_powerbi_model, semantic_contract


REPORT_SCHEMA_VERSION = "1.0"


def _visual(visual_id, title, visual_type, fields, measures, denominator, filters, note=""):
    return {"id": visual_id, "title": title, "type": visual_type, "fields": fields,
            "measures": measures, "denominator": denominator, "comparability_filter": filters,
            "interpretation_note": note}


def report_pages():
    numeric = "quality_id = 'numeric' AND annual_eligible = TRUE()"
    strict = numeric + " AND reporting_basis <> 'unknown'"
    return [
        {"id": "executive", "title": "Executive snapshot", "bookmark": "executive",
         "purpose": "Start with coverage, sample size, selected metric levels and reviewed findings.",
         "visuals": [
             _visual("kpi_numeric", "Numeric observations", "card", [], ["Numeric Observations"], "all fact observations", numeric),
             _visual("kpi_comparable_n", "Comparable N", "card", [], ["Comparable N"], "distinct banks in the selected metric/year/basis cohort", strict),
             _visual("metric_selector", "Selected metric", "field_parameter", ["dim_metric[metric]"], [], "not applicable", "metric dimension only"),
             _visual("latest_levels", "Latest disclosed levels", "column", ["dim_metric[metric]", "dim_bank[parent_group]"], ["Reported Value"], "selected metric/year/basis numeric observations", strict),
             _visual("reviewed_findings", "Deterministic review prompts", "table", ["finding_detail[metric]", "finding_detail[bank]", "finding_detail[reason]"], [], "rows in the IN-009 finding extract", "use finding_detail[mode] and finding_detail[comparability_status]", "A prompt for review is not a conclusion."),
         ]},
        {"id": "comparability", "title": "Comparability and coverage", "bookmark": "method",
         "purpose": "Make the denominator, exclusions, source quality and basis visible before comparison.",
         "visuals": [
             _visual("coverage_by_metric", "Coverage by metric and basis", "matrix", ["dim_metric[metric]", "dim_comparability[reporting_basis]"], ["Numeric Observations", "Comparable N", "Observation Coverage %"], "fact observations in the current metric/year/basis filter", "quality_id = 'numeric'; annual_eligible is visible as a slicer"),
             _visual("quality_mix", "Disclosure quality mix", "stacked_bar", ["dim_metric[metric]", "dim_quality[quality_status]"], ["Numeric Observations", "Missing Observations", "Non-numeric Disclosures"], "all fact observations in the selected metric/period", "do not treat missing or non-numeric as zero"),
             _visual("source_trace", "Source trace", "table", ["dim_bank[bank]", "fact_observation[row_label]", "dim_period[period_label]", "dim_source[source_id]", "fact_observation[source_note]"], [], "selected fact observations", "retain current bank/metric/period/quality filters"),
         ]},
        {"id": "investigate", "title": "Exceptions and investigation", "bookmark": "investigate",
         "purpose": "Follow a selected observation into its source, peer, parent and time context.",
         "visuals": [
             _visual("trend", "Comparable annual trend", "line_anomaly", ["dim_period[fiscal_year]", "fact_observation[value_numeric]"], ["Reported Value"], "numeric observations for one bank, metric and reporting basis", strict, "Anomaly detection is exploratory and requires a sufficiently long comparable series."),
             _visual("distribution", "Comparable distribution", "box_strip_percentile", ["fact_observation[value_numeric]", "dim_bank[bank]"], ["Reported Value", "Comparable N"], "distinct numeric banks in one exact fiscal-year/basis/unit cohort", strict, "Suppress percentile interpretation below the IN-016 minimum cohort."),
             _visual("decomposition", "Exploratory contribution paths", "decomposition_tree", ["dim_metric[metric]", "dim_period[fiscal_year]", "dim_bank[parent_group]", "dim_comparability[reporting_basis]", "dim_unit[unit]", "dim_quality[quality_status]"], ["Reported Value", "Numeric Observations"], "selected fact observations", numeric, "AI splits are exploratory associations, not causal, compliance or prudential findings."),
             _visual("detail", "Bank / observation drillthrough", "drillthrough_table", ["dim_bank[bank]", "dim_metric[metric]", "dim_period[period_label]", "fact_observation[value_raw]", "dim_unit[unit]", "dim_comparability[reporting_basis]", "dim_source[source_id]", "fact_observation[basis_note]", "fact_observation[restatement_note]", "fact_observation[source_note]"], [], "selected observation rows", "bank_id, metric_id and period_id are required drillthrough fields"),
         ]},
        {"id": "scale", "title": "Capital and RWA scale", "bookmark": "scale",
         "purpose": "Explore absolute amounts without mixing units or reporting bases.",
         "visuals": [
             _visual("scale_trend", "Capital and RWA amounts", "line", ["dim_period[fiscal_year]", "dim_metric[metric]", "dim_unit[unit]"], ["Reported Value"], "numeric observations within one metric/year/unit/basis cohort", numeric + " AND unit_id <> 'unknown'", "Amounts are not strength rankings; pair with the relevant ratio."),
             _visual("size_cohort", "Size-aware comparison", "scatter", ["dim_metric[metric]", "dim_unit[unit]", "dim_bank[bank]"], ["Reported Value"], "numeric banks with matching unit and reporting basis", numeric + " AND unit_id <> 'unknown'", "Do not infer financial strength from amount size."),
         ]},
    ]


def _finding_rows(db_path):
    payload = build_in009_payload(db_path)
    rows = []
    for mode, findings in payload["outliers"].items():
        for item in findings:
            rows.append({"finding_id": f"{mode}:{item['frn']}:{item['metric']}:{item['fiscal_year']}",
                         "mode": mode, "frn": item["frn"], "bank": item["bank"],
                         "metric": item["metric"], "fiscal_year": item["fiscal_year"],
                         "value": item["value"], "reason": "; ".join(item["reasons"]),
                         "comparability_status": item.get("comparability_status", "unknown"),
                         "interpretation": "deterministic review prompt; inspect source before conclusion"})
    return rows


def build_report_experience(db_path):
    model = build_powerbi_model(db_path)
    contract = semantic_contract()
    return {
        "report_schema_version": REPORT_SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": os.path.abspath(db_path),
        "authoritative_outputs": ["research/insights.db", "research/powerbi/semantic_model.json", "uk_bank_insights.html", "uk_bank_insights.pdf"],
        "pages": report_pages(),
        "navigation": {"default": "executive", "bookmarks": [
            {"name": "executive", "page": "executive", "preserves": ["metric", "period", "basis", "unit"]},
            {"name": "method", "page": "comparability", "preserves": ["metric", "period", "basis", "quality"]},
            {"name": "investigate", "page": "investigate", "preserves": ["bank", "metric", "period", "basis", "unit"]},
            {"name": "scale", "page": "scale", "preserves": ["metric", "period", "basis", "unit"]},
        ]},
        "drillthrough": {"page": "investigate", "required_fields": ["bank_id", "metric_id", "period_id"],
                         "fallback": "visible source-trace table; do not make tooltip content the only evidence"},
        "tooltip": {"fields": ["value_raw", "period_label", "unit", "reporting_basis", "source_id", "annual_eligible", "quality_id"],
                    "required_redundancy": "all caveats required for interpretation must also appear on the page or drillthrough"},
        "accessibility": {"requirements": ["descriptive visual titles", "alt text for charts", "keyboard-reachable slicers and navigation", "logical tab order", "no colour-only status", "tables for every chart's key values"],
                          "fallbacks": ["use the HTML tables for accessible/print review", "use the fixed PDF for controlled export", "do not rely on report-page tooltips for screen-reader interpretation"]},
        "export_limits": ["Power BI PDF export is not the controlled narrative output", "hidden and tooltip pages may be absent from PDF export", "bookmark, drill and scroll state may not survive export", "use the generated HTML/PDF for the formal client pack"],
        "governance": {"exploratory_labels": ["decomposition tree", "key influencers", "anomaly detection"], "non_causal_warning": "Associations and detected anomalies are exploratory and non-causal; they are not compliance findings or evidence of weakness.", "deterministic_findings": "IN-009 outlier rows remain the official review screen and are exposed in finding_detail.csv."},
        "semantic_model_schema_version": contract["schema_version"],
    }


def _write_csv(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as handle:
        fields = list(rows[0]) if rows else ["finding_id"]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def export_report_experience(db_path, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    report = build_report_experience(db_path)
    with open(os.path.join(out_dir, "report_experience.json"), "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, sort_keys=True)
        handle.write("\n")
    findings = _finding_rows(db_path)
    _write_csv(os.path.join(out_dir, "finding_detail.csv"), findings)
    return report, findings


def main():
    root = os.path.join(os.path.dirname(__file__), "..", "..")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=os.path.join(root, "research", "insights.db"))
    parser.add_argument("--out-dir", default=os.path.join(root, "research", "powerbi"))
    args = parser.parse_args()
    report, findings = export_report_experience(args.db, args.out_dir)
    print(f"Wrote IN-019 report experience ({len(report['pages'])} pages, {len(findings)} findings) to {args.out_dir}")


if __name__ == "__main__":
    main()
