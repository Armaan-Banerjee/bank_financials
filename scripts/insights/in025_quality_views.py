"""Source-quality, disclosure-cadence, and evidence-coverage payload (IN-025)."""

import argparse
import json
import os
from collections import Counter, defaultdict
from tempfile import NamedTemporaryFile

import build_insights_db
from analysis_queries import AnalysisQueries
from in009_analysis import CORE_METRICS, _select_metric_observations, normalize_observation


TRACE_FIELDS = ("frn", "source_workbook", "sheet", "row_label", "year", "value_raw", "value_numeric", "unit", "reporting_basis", "basis_note", "restatement_note", "source_note")
REQUIRED_TRACE_FIELDS = ("frn", "source_workbook", "sheet", "row_label", "year", "value_raw")


def classify_quality(row):
    """Return one visible quality state; non-numeric disclosure is not missing."""
    value_status = row.get("value_status")
    if value_status in ("non_numeric_disclosure", "non_numeric") or (not row.get("is_numeric") and str(row.get("value_raw") or "").strip()):
        return "non_numeric"
    if value_status in ("missing", None) and not row.get("value_raw"):
        return "missing"
    if row.get("period_type") == "annual" and row.get("annual_eligible") is False:
        return "shortened_period"
    if value_status in ("numeric", "special_numeric") or row.get("is_numeric") in (1, "1", True):
        if not row.get("reporting_basis") and not row.get("basis_raw"):
            return "numeric_unknown_basis"
        if not row.get("unit") and not row.get("unit_raw"):
            return "numeric_unknown_unit"
        return "numeric"
    return "missing"


def cadence_summary(rows):
    """Count cadence and quality by annual/interim source domain."""
    result = {}
    for domain in ("annual", "interim"):
        relevant = [row for row in rows if row.get("source_domain") == domain]
        states = Counter(classify_quality(row) for row in relevant)
        result[domain] = {"observations": len(relevant),
                          "banks": len({row.get("frn") for row in relevant if row.get("frn")}),
                          "period_types": dict(sorted(Counter(row.get("period_type", "unknown") for row in relevant).items())),
                          "quality_states": dict(sorted(states.items()))}
    return result


def trace_completeness(rows, fields=TRACE_FIELDS):
    """Report trace-field completeness while retaining incomplete rows."""
    missing = Counter()
    complete = 0
    for row in rows:
        absent = [field for field in fields if row.get(field) in (None, "")]
        if not absent:
            complete += 1
        for field in absent:
            missing[field] += 1
    return {"rows": len(rows), "complete_rows": complete, "missing_fields": dict(sorted(missing.items()))}


def _annual_trace(rows):
    result = []
    for raw in rows:
        row = normalize_observation(raw)
        row["source_domain"] = "annual"
        row["quality_status"] = classify_quality(row)
        result.append(row)
    return result


def _interim_trace(rows):
    result = []
    for raw in rows:
        row = dict(raw)
        row.update({"sheet": row.get("source_sheet"), "row_label": row.get("row_label_raw"),
                    "year": row.get("period_label_raw"), "value_raw": row.get("value_raw"),
                    "value_numeric": row.get("value_numeric"), "unit": row.get("unit_raw"),
                    "basis_note": row.get("basis_raw"), "source_note": row.get("sheet_note"),
                    "source_domain": "interim", "value_status": "numeric" if row.get("is_numeric") else "non_numeric_disclosure"})
        row["quality_status"] = classify_quality(row)
        result.append(row)
    return result


def build_quality_grid(rows):
    """Build annual bank/metric/year quality cells with explicit flags."""
    banks = {}
    years = sorted({row.get("fiscal_year") for row in rows if row.get("fiscal_year") is not None})
    grouped = defaultdict(list)
    for row in rows:
        banks.setdefault(row["frn"], row.get("canonical_bank") or row.get("bank") or row["frn"])
        metric = next((name for name, sheet in CORE_METRICS.items() if sheet == row.get("sheet")), None)
        if metric and row.get("fiscal_year") is not None:
            grouped[(row["frn"], metric, row["fiscal_year"])].append(row)
    canonical_by_metric = {
        metric: {(row["frn"], row["fiscal_year"]): row
                 for row in _select_metric_observations(rows, sheet)}
        for metric, sheet in CORE_METRICS.items()
    }
    cells = []
    state_counts = Counter()
    for frn, bank in sorted(banks.items()):
        for metric in CORE_METRICS:
            for year in years:
                source = grouped.get((frn, metric, year), [])
                states = [classify_quality(row) for row in source]
                if any(state.startswith("numeric") for state in states):
                    state = "numeric" if "numeric" in states else next(item for item in states if item.startswith("numeric"))
                elif "non_numeric" in states:
                    state = "non_numeric"
                elif "shortened_period" in states:
                    state = "shortened_period"
                else:
                    state = "missing"
                flags = sorted({flag for row in source for flag in (("unknown_basis",) if not row.get("reporting_basis") else ()) + (("unknown_unit",) if not row.get("unit") else ())})
                numeric_source = [row for row in source if classify_quality(row).startswith("numeric")]
                display_source = canonical_by_metric[metric].get((frn, year)) or (source[0] if source else None)
                display_value = None if display_source is None else display_source.get("value_raw") or display_source.get("value_numeric")
                cells.append({"frn": frn, "bank": bank, "metric": metric, "year": year, "state": state, "display_value": display_value, "n": len(source), "flags": flags})
                state_counts[state] += 1
    return {"banks": len(banks), "metrics": list(CORE_METRICS), "years": years, "cells": cells, "state_counts": dict(sorted(state_counts.items()))}


def build_in025_payload(db_path):
    queries = AnalysisQueries(db_path)
    annual = _annual_trace(queries.observations())
    interim = _interim_trace(queries.interim_observations())
    all_trace = annual + interim
    conn = build_insights_db.connect(db_path)
    try:
        annual_orphans = conn.execute("SELECT COUNT(*) FROM annual_metrics m LEFT JOIN banks b ON b.frn=m.frn WHERE b.frn IS NULL").fetchone()[0]
        interim_orphans = conn.execute("SELECT COUNT(*) FROM interim_observations m LEFT JOIN banks b ON b.frn=m.frn WHERE b.frn IS NULL").fetchone()[0]
    finally:
        conn.close()
    return {"metadata": {"source": os.path.abspath(db_path), "annual_domain": "annual_metrics only", "interim_domain": "interim_observations only", "trace_fields": list(TRACE_FIELDS), "required_trace_fields": list(REQUIRED_TRACE_FIELDS)},
            "cadence": cadence_summary(annual + interim), "coverage": build_quality_grid(annual),
            "trace_completeness": trace_completeness(all_trace, REQUIRED_TRACE_FIELDS),
            "join_checks": {"annual_orphan_rows": annual_orphans, "interim_orphan_rows": interim_orphans},
            "trace": [{field: row.get(field, "") for field in TRACE_FIELDS} | {"source_domain": row["source_domain"], "quality_status": row["quality_status"]} for row in all_trace]}


def write_json_atomic(payload, output_path):
    output_dir = os.path.dirname(os.path.abspath(output_path)) or "."
    os.makedirs(output_dir, exist_ok=True)
    with NamedTemporaryFile("w", encoding="utf-8", dir=output_dir, delete=False) as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")
        temporary_path = handle.name
    os.replace(temporary_path, output_path)


def main():
    root = os.path.join(os.path.dirname(__file__), "..", "..")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=os.path.join(root, "research", "insights.db"))
    parser.add_argument("--out", default=os.path.join(root, "research", "in025_quality_views.json"))
    args = parser.parse_args()
    write_json_atomic(build_in025_payload(args.db), args.out)
    print(f"Wrote IN-025 quality-views payload to {args.out}")


if __name__ == "__main__":
    main()
