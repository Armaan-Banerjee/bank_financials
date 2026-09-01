"""Export the SQLite source of truth as a Power BI-ready star schema."""

import argparse
import csv
import json
import os
import re
from collections import OrderedDict

import build_insights_db
from in009_analysis import normalize_observation


SCHEMA_VERSION = "1.0"
FACT_GRAIN = "one annual source observation per FRN, metric sheet, source row label, and reported period"


def _slug(value):
    value = re.sub(r"[^a-z0-9]+", "_", str(value or "").lower()).strip("_")
    return value or "unknown"


def _dimension(rows, key, id_name, fields):
    values = OrderedDict()
    for row in rows:
        value = row.get(key) or "unknown"
        values.setdefault(value, {id_name: _slug(value), key: value})
    return [dict(item, **{field: next((row.get(field, "") for row in rows if (row.get(key) or "unknown") == item[key]), "") for field in fields}) for item in values.values()]


def _period_id(row):
    """Return a stable key that preserves qualified reporting periods."""
    fiscal_year = row.get("fiscal_year")
    reported_year = row.get("year") or "reported"
    suffix = _slug(reported_year)
    if fiscal_year is None:
        return f"reported_{suffix}"
    ordinary = f"FY{fiscal_year}"
    return ordinary if reported_year == ordinary else f"{ordinary}_{suffix}"


def _write_csv(path, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fields = list(rows[0]) if rows else []
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def build_powerbi_model(db_path):
    from analysis_queries import AnalysisQueries
    rows = AnalysisQueries(db_path).observations()
    raw = rows
    group_map = AnalysisQueries(db_path).groups()

    banks = OrderedDict()
    for row in raw:
        frn = str(row["frn"])
        if frn not in banks:
            bank, group, caveat = group_map.get(frn, (row.get("canonical_bank", ""), "", ""))
            banks[frn] = {"bank_id": frn, "frn": frn, "bank": row.get("canonical_bank", ""),
                          "source_filename_bank": row.get("source_filename_bank", ""),
                          "source_workbook": row.get("source_workbook", ""),
                          "workbook_kind": row.get("workbook_kind", ""),
                          "parent_group_id": _slug(group), "parent_group": group or "unknown",
                          "parent_group_status_caveat": caveat or ""}
    metrics = []
    metric_keys = OrderedDict()
    for row in rows:
        sheet = row.get("sheet") or "unknown"
        if sheet not in metric_keys:
            metric_keys[sheet] = {"metric_id": _slug(sheet), "metric": sheet, "sheet": sheet,
                                  "metric_type": "cash_flow" if "cash" in sheet.lower() else "pillar_3"}
    metrics = list(metric_keys.values())
    periods = []
    period_keys = OrderedDict()
    for row in rows:
        key = row.get("fiscal_year")
        period_id = _period_id(row)
        period_keys.setdefault(period_id, {"period_id": period_id, "fiscal_year": key or "", "period_label": row.get("year", ""), "period_type": row.get("period_type", "annual")})
    periods = list(period_keys.values())
    sources = _dimension(raw, "source_workbook", "source_id", ["source_note"])
    units = _dimension(raw, "unit", "unit_id", [])
    bases = _dimension(raw, "reporting_basis", "comparability_id", ["basis_note"])
    quality = [
        {"quality_id": "numeric", "quality_status": "numeric", "is_comparable_candidate": True, "description": "Parsed numeric annual observation."},
        {"quality_id": "missing", "quality_status": "missing", "is_comparable_candidate": False, "description": "No value was disclosed in the source row."},
        {"quality_id": "non_numeric", "quality_status": "non_numeric_string", "is_comparable_candidate": False, "description": "Text was disclosed but could not be parsed as a number."},
        {"quality_id": "special_numeric", "quality_status": "special_numeric", "is_comparable_candidate": False, "description": "Special numeric marker; excluded from statistical benchmarking."},
    ]
    facts = []
    for index, row in enumerate(rows, start=1):
        status = row.get("value_status", "missing")
        period_id = _period_id(row)
        basis = row.get("reporting_basis") or "unknown"
        facts.append({
            "observation_id": str(index), "bank_id": str(row["frn"]), "metric_id": _slug(row.get("sheet")),
            "period_id": period_id, "source_id": _slug(row.get("source_workbook")),
            "unit_id": _slug(row.get("unit") or "unknown"), "comparability_id": _slug(basis),
            "quality_id": status, "row_label": row.get("row_label", ""), "reported_year": row.get("year", ""),
            "fiscal_year": row.get("fiscal_year") or "", "value_raw": row.get("value_raw", ""),
            "value_numeric": row.get("value_numeric", "") if status == "numeric" else "",
            "is_numeric": status == "numeric", "annual_eligible": bool(row.get("annual_eligible")),
            "reporting_basis": basis, "basis_note": row.get("basis_note", ""),
            "restatement_note": row.get("restatement_note", ""), "source_note": row.get("source_note", ""),
        })
    return {"schema_version": SCHEMA_VERSION, "fact_grain": FACT_GRAIN,
            "tables": {"fact_observation": facts, "dim_bank": list(banks.values()), "dim_metric": metrics,
                       "dim_period": periods, "dim_source": sources, "dim_unit": units,
                       "dim_comparability": bases, "dim_quality": quality}}


def semantic_contract():
    return {"schema_version": SCHEMA_VERSION, "refresh_contract": {
        "source": "research/insights.db", "command": "python3 scripts/insights/refresh_all.py",
        "order": "extract -> parent groups -> clusters -> analysis -> Power BI export -> deliverables",
        "schema_change": "Bump schema_version and update this contract when grain, field meaning, or keys change.",
        "validation": "Refresh fails before export if SQLite structural checks fail; downstream outputs consume the same snapshot.",
    }, "relationships": [
        "dim_bank[bank_id] 1:* fact_observation[bank_id]",
        "dim_metric[metric_id] 1:* fact_observation[metric_id]",
        "dim_period[period_id] 1:* fact_observation[period_id]",
        "dim_source[source_id] 1:* fact_observation[source_id]",
        "dim_unit[unit_id] 1:* fact_observation[unit_id]",
        "dim_comparability[comparability_id] 1:* fact_observation[comparability_id]",
        "dim_quality[quality_id] 1:* fact_observation[quality_id]",
    ], "measures": {
        "Numeric Observations": "CALCULATE(COUNTROWS(fact_observation), fact_observation[quality_id] = \"numeric\")",
        "Reported Value": "SUM(fact_observation[value_numeric])",
        "Banks with Numeric Value": "CALCULATE(DISTINCTCOUNT(fact_observation[bank_id]), fact_observation[quality_id] = \"numeric\")",
        "Observation Coverage %": "DIVIDE([Numeric Observations], COUNTROWS(fact_observation))",
        "Missing Observations": "CALCULATE(COUNTROWS(fact_observation), fact_observation[quality_id] = \"missing\")",
        "Non-numeric Disclosures": "CALCULATE(COUNTROWS(fact_observation), fact_observation[quality_id] = \"non_numeric_string\")",
        "Comparable N": "CALCULATE(DISTINCTCOUNT(fact_observation[bank_id]), fact_observation[quality_id] = \"numeric\", fact_observation[annual_eligible] = TRUE(), fact_observation[reporting_basis] <> \"unknown\")",
        "Latest Fiscal Year": "MAX(dim_period[fiscal_year])",
    }, "authoring_rules": [
        "Use dimension fields for slicers and grouping; do not group directly on raw labels.",
        "Use Comparable N beside every benchmark or percentile visual.",
        "Filter quality_id=numeric and annual_eligible=TRUE for annual comparisons.",
        "Do not compare absolute values across unit_id or reporting_basis without an explicit conversion contract.",
        "Use IN-009/IN-016 findings for outliers and ranks; do not recreate those business rules in DAX.",
    ]}


def export_model(db_path, out_dir):
    model = build_powerbi_model(db_path)
    os.makedirs(out_dir, exist_ok=True)
    for table, rows in model["tables"].items():
        _write_csv(os.path.join(out_dir, f"{table}.csv"), rows)
    contract = semantic_contract()
    contract["source"] = os.path.abspath(db_path)
    contract["table_row_counts"] = {table: len(rows) for table, rows in model["tables"].items()}
    with open(os.path.join(out_dir, "semantic_model.json"), "w", encoding="utf-8") as handle:
        json.dump(contract, handle, indent=2, sort_keys=True)
    return model, contract


def main():
    root = os.path.join(os.path.dirname(__file__), "..", "..")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=os.path.join(root, "research", "insights.db"))
    parser.add_argument("--out-dir", default=os.path.join(root, "research", "powerbi"))
    args = parser.parse_args()
    _model, contract = export_model(args.db, args.out_dir)
    print(f"Wrote Power BI star schema ({sum(contract['table_row_counts'].values())} rows) to {args.out_dir}")


if __name__ == "__main__":
    main()
