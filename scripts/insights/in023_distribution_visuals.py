"""Distribution and evidence-coverage payload for IN-023."""

import argparse
import json
import os
from collections import defaultdict
from tempfile import NamedTemporaryFile

from in009_analysis import CORE_METRICS, normalize_observation
from in016_distribution import build_in016_payload, summarize
from in017_quality import build_in017_payload


def distribution_band(values):
    """Return the documented robust distribution summary without a mean."""
    return summarize(values)


def coverage_state(rows):
    """Classify one bank/metric/year cell without converting absence to zero."""
    if not rows:
        return "missing"
    numeric_rows = [row for row in rows if row.get("value_status") in ("numeric", "special_numeric") and row.get("annual_eligible")]
    if numeric_rows:
        return "numeric" if any(row.get("reporting_basis") for row in numeric_rows) else "numeric_unknown_basis"
    if any(row.get("period_type") == "annual" and not row.get("annual_eligible") for row in rows):
        return "shortened_period"
    if any(row.get("value_status") == "non_numeric_disclosure" for row in rows):
        return "non_numeric"
    if any(row.get("value_status") == "missing" for row in rows):
        return "missing"
    return "missing"


def build_coverage_grid(rows):
    """Build a deterministic bank/metric/year evidence-status grid."""
    normalized = [normalize_observation(row) for row in rows]
    banks = {}
    for row in normalized:
        banks.setdefault(row["frn"], row.get("canonical_bank") or row.get("bank") or row["frn"])
    years = sorted({row["fiscal_year"] for row in normalized if row.get("fiscal_year") is not None})
    grouped = defaultdict(list)
    for row in normalized:
        metric = next((metric for metric, sheet in CORE_METRICS.items() if sheet == row.get("sheet")), None)
        if metric and row.get("fiscal_year") is not None:
            grouped[(row["frn"], metric, row["fiscal_year"])].append(row)
    cells = []
    counts = defaultdict(int)
    for frn, bank in sorted(banks.items()):
        for metric in CORE_METRICS:
            for year in years:
                state = coverage_state(grouped.get((frn, metric, year), []))
                cells.append({"frn": frn, "bank": bank, "metric": metric, "year": year, "state": state})
                counts[state] += 1
    return {"banks": len(banks), "metrics": list(CORE_METRICS), "years": years, "cells": cells, "state_counts": dict(sorted(counts.items()))}


def build_in023_payload(db_path, in016=None, in017=None):
    from analysis_queries import AnalysisQueries
    rows = AnalysisQueries(db_path).observations()
    in016 = in016 or build_in016_payload(db_path)
    in017 = in017 or build_in017_payload(db_path)
    return {"metadata": {"source": os.path.abspath(db_path), "minimum_n": 8, "default_mode": "broad", "statistics": ["median", "quartiles", "iqr", "mad", "p10", "p90"]}, "in016": in016, "in017": in017, "coverage": build_coverage_grid(rows)}


def write_json_atomic(payload, output_path):
    output_dir = os.path.dirname(os.path.abspath(output_path)) or "."
    os.makedirs(output_dir, exist_ok=True)
    with NamedTemporaryFile("w", encoding="utf-8", dir=output_dir, delete=False) as handle:
        temporary_path = handle.name
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")
    os.replace(temporary_path, output_path)


def main():
    root = os.path.join(os.path.dirname(__file__), "..", "..")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=os.path.join(root, "research", "insights.db"))
    parser.add_argument("--out", default=os.path.join(root, "research", "in023_distribution_visuals.json"))
    args = parser.parse_args()
    write_json_atomic(build_in023_payload(args.db), args.out)
    print(f"Wrote IN-023 distribution-visuals payload to {args.out}")


if __name__ == "__main__":
    main()
