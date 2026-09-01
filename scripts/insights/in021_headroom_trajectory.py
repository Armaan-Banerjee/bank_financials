"""Screen annual regulatory headroom alongside observed ratio trajectories."""

import argparse
import json
import os
import tempfile
from datetime import datetime, timezone

import build_insights_db
from in009_analysis import CORE_METRICS, _select_metric_observations, build_metric_series, comparison_diagnostics, normalize_observation
from in020_regulatory_context import CONTEXT

SCHEMA_VERSION = "1.0"


def applicable_context(observation, metric, year):
    """Return a dated floor using IN-020's safe unit/basis policy."""
    if observation.get("unit") != "%" or not observation.get("reporting_basis"):
        return None
    candidates = [item for item in CONTEXT if item["metric"] == metric
                  and item["effective_from"] <= year
                  and (item["effective_to"] is None or year <= item["effective_to"])
                  and item["value"] is not None]
    if not candidates:
        return None
    minimum = sum(item["value"] for item in candidates
                  if item["context_type"] in ("regulatory_minimum", "regulatory_minimum_or_supervisory_expectation"))
    buffer_value = sum(item["value"] for item in candidates if item["context_type"] == "buffer")
    floor = minimum + buffer_value
    if floor == 0:
        # Guard on the combined floor, not `minimum` alone, so this agrees
        # with in020_regulatory_context.py's match_context() - a metric with
        # only a buffer record (no separate minimum) would otherwise be
        # wrongly dropped here while still matching there.
        return None
    return {"minimum": minimum, "buffer": buffer_value, "floor": floor,
            "context_ids": [item["context_id"] for item in candidates],
            "sources": sorted({item["source"] for item in candidates})}


def build_headroom_payload(db_path):
    from analysis_queries import AnalysisQueries
    normalized = AnalysisQueries(db_path).observations()
    records = []
    for metric, sheet in CORE_METRICS.items():
        # Plain sheet filter, not the removed `_metric_observations` label-text
        # pre-filter - see in009_analysis.py's build_in009_payload for why.
        metric_rows = [item for item in normalized if item.get("sheet") == sheet]
        eligible = []
        years = sorted({row.get("fiscal_year") for row in metric_rows if row.get("fiscal_year") is not None})
        for year in years:
            selected, _ = comparison_diagnostics(metric_rows, "broad", year)
            eligible.extend(selected)
        series = build_metric_series(eligible, sheet)
        canonical_rows = _select_metric_observations(eligible, sheet)
        by_frn_year = {(row["frn"], row["fiscal_year"]): row for row in canonical_rows}
        for frn, values in sorted(series.items()):
            ordered_years = sorted(values)
            latest_year = ordered_years[-1]
            latest = by_frn_year[(frn, latest_year)]
            context = applicable_context(latest, metric, latest_year)
            comparable_pairs = len(ordered_years) - 1
            change = values[latest_year] - values[ordered_years[0]] if comparable_pairs else None
            if context is None:
                status = "no_regulatory_context"
            elif comparable_pairs < 1:
                status = "insufficient_evidence"
            else:
                status = "screened"
            records.append({
                "frn": frn, "bank": latest.get("canonical_bank", latest.get("bank", "")),
                "metric": metric, "latest_year": latest_year, "current_value": values[latest_year],
                "applicable_minimum": context["minimum"] if context else None,
                "applicable_buffer": context["buffer"] if context else None,
                "regulatory_floor": context["floor"] if context else None,
                "current_headroom": values[latest_year] - context["floor"] if context else None,
                "trend_direction": ("declining" if change < 0 else "increasing" if change > 0 else "unchanged") if change is not None else None,
                "trend_change": change, "trend_magnitude": abs(change) if change is not None else None,
                "comparable_year_count": len(ordered_years), "comparable_pair_count": comparable_pairs,
                "status": status, "context_ids": context["context_ids"] if context else [],
                "sources": context["sources"] if context else [],
            })
    records.sort(key=lambda row: (0 if row["status"] == "screened" and row["trend_direction"] == "declining" else 1,
                                  row["current_headroom"] if row["current_headroom"] is not None else float("inf"),
                                  row["frn"], row["metric"]))
    return {"schema_version": SCHEMA_VERSION, "source_database": os.path.abspath(db_path),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "policy": "screening only: observed headroom and multi-year movement are ranked; no breach date or future value is projected",
            "records": records}


def validate_payload(db_path, payload):
    if os.path.abspath(db_path) != payload.get("source_database"):
        raise ValueError("IN-021 payload source database does not match deliverable database")
    from analysis_queries import AnalysisQueries
    expected = len(AnalysisQueries(db_path).observations())
    if not payload.get("records") and expected:
        raise ValueError("IN-021 payload is empty while the source database has annual observations")
    if payload.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("unsupported IN-021 payload schema")


def _write_if_changed(path, content):
    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    try:
        if open(path, encoding="utf-8").read() == content:
            return
    except FileNotFoundError:
        pass
    fd, temporary = tempfile.mkstemp(prefix=".in021_", dir=os.path.dirname(os.path.abspath(path)) or ".", text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def main():
    root = os.path.join(os.path.dirname(__file__), "..", "..")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=os.path.join(root, "research", "insights.db"))
    parser.add_argument("--out", default=os.path.join(root, "research", "in021_headroom_trajectory.json"))
    args = parser.parse_args()
    payload = build_headroom_payload(args.db)
    _write_if_changed(args.out, json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"Wrote IN-021 payload with {len(payload['records'])} bank-metric records to {args.out}")


if __name__ == "__main__":
    main()
