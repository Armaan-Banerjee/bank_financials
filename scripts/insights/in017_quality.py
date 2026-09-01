"""Build source-lineage and data-quality facts for IN-017."""

import argparse
import json
import os
from collections import Counter, defaultdict
from datetime import datetime, timezone

from in009_analysis import CORE_METRICS, normalize_observation
from analysis_queries import AnalysisQueries


def _text(value):
    return str(value or "").strip()


def _lineage(row):
    """Keep the source fields needed to trace a displayed observation."""
    return {key: row.get(key, "") for key in (
        "frn", "bank", "canonical_bank", "source_workbook", "workbook_kind",
        "sheet", "row_label", "year", "value_raw", "value_numeric", "is_numeric",
        "unit", "reporting_basis", "basis_note", "restatement_note", "source_note",
    )}


def _quality_fact(rows, metric, sheet):
    relevant = [row for row in rows if row.get("sheet") == sheet]
    numeric = [row for row in relevant if row.get("value_status") == "numeric"]
    missing = [row for row in relevant if row.get("value_status") == "missing"]
    special = [row for row in relevant if row.get("value_status") == "special_numeric"]
    non_numeric = [row for row in relevant if row.get("value_status") == "non_numeric_string"]
    years = sorted({row.get("fiscal_year") for row in relevant if row.get("fiscal_year") is not None})
    bases = Counter(_text(row.get("reporting_basis")) or "unknown" for row in relevant)
    units = Counter(_text(row.get("unit")) or "unknown" for row in relevant)
    labels = Counter(_text(row.get("row_label")) for row in relevant)
    variants = sum(count - 1 for count in labels.values() if count > 1)
    return {
        "metric": metric, "sheet": sheet, "observations": len(relevant),
        "banks": len({row.get("frn") for row in relevant}),
        "numeric": len(numeric), "missing": len(missing),
        "non_numeric_disclosure": len(non_numeric), "special_numeric": len(special),
        "years": years, "reporting_basis_counts": dict(bases),
        "unit_counts": dict(units), "row_label_variant_count": variants,
        "missing_classification": "genuine_non_disclosure" if missing else "none",
        "non_numeric_classification": "disclosed_but_unparsed" if non_numeric else "none",
        "structural_status": "ok",
    }


def _structural_checks(rows, db_path):
    checks = []
    integrity = AnalysisQueries(db_path).annual_integrity()
    for table in ("banks", "annual_metrics", "refresh_metadata"):
        checks.append({"check": f"table:{table}", "status": "pass" if table in integrity["tables"] else "fail"})
    checks.append({"check": "annual_metrics_foreign_keys", "status": "pass" if integrity["orphan_rows"] == 0 else "fail", "count": integrity["orphan_rows"]})
    checks.append({"check": "annual_metric_identity_duplicates", "status": "pass" if integrity["identity_duplicates"] == 0 else "fail", "count": integrity["identity_duplicates"]})
    expected_frns = {row.get("frn") for row in rows}
    checks.append({"check": "normalized_rows_have_frn", "status": "pass" if all(expected_frns) else "fail"})
    failed = [item for item in checks if item["status"] == "fail"]
    return checks, failed


def build_in017_payload(db_path):
    from analysis_queries import AnalysisQueries
    raw_rows = AnalysisQueries(db_path).observations()
    rows = raw_rows
    checks, failed = _structural_checks(rows, db_path)
    if failed:
        raise RuntimeError("IN-017 structural quality checks failed: " + "; ".join(item["check"] for item in failed))

    facts = [_quality_fact(rows, metric, sheet) for metric, sheet in CORE_METRICS.items()]
    bank_dimensions = {}
    for row in raw_rows:
        if row.get("frn") and row["frn"] not in bank_dimensions:
            bank_dimensions[row["frn"]] = {"frn": row["frn"], "bank": row["canonical_bank"], "source_workbook": row["source_workbook"], "workbook_kind": row["workbook_kind"]}
    dimensions = {
        "banks": list(bank_dimensions.values()),
        "metrics": [{"metric": metric, "sheet": sheet} for metric, sheet in CORE_METRICS.items()],
    }
    # One row per source observation is intentionally retained for Power BI
    # and audit tooling; the HTML only presents a small, readable summary.
    lineage = [_lineage(row) for row in raw_rows]
    metadata = AnalysisQueries(db_path).refresh_metadata()
    metadata.update({"source": os.path.abspath(db_path), "generated_at": datetime.now(timezone.utc).isoformat(),
                     "lineage_contract": "annual source observation: bank/workbook/sheet/row/year/value/unit/basis/restatement/source note",
                     "quality_facts": "one row per metric sheet; counts are post-dedup SQLite observations"})
    return {"metadata": metadata, "structural_checks": checks, "quality_facts": facts,
            "dimensions": dimensions, "lineage": lineage}


def main():
    root = os.path.join(os.path.dirname(__file__), "..", "..")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=os.path.join(root, "research", "insights.db"))
    parser.add_argument("--out", default=os.path.join(root, "research", "in017_quality.json"))
    args = parser.parse_args()
    with open(args.out, "w", encoding="utf-8") as handle:
        json.dump(build_in017_payload(args.db), handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(f"Wrote IN-017 quality payload to {args.out}")


if __name__ == "__main__":
    main()
