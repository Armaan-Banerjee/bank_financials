"""Generate versioned, scope-aware regulatory context for IN-020."""

import argparse
import csv
import json
import os
from datetime import datetime, timezone

import build_insights_db
from in009_analysis import normalize_observation


SCHEMA_VERSION = "1.0"
RESEARCH_NOTE = "research/regulatory_context_2026-08-30.md"

CONTEXT = [
    {"context_id": "cet1_pillar1_uk_2021", "metric": "CET1 Ratio", "context_type": "regulatory_minimum", "value": 4.5, "unit": "%", "denominator": "RWA", "jurisdiction": "UK", "scope": "risk-based capital framework", "basis": "unknown", "effective_from": 2021, "effective_to": None, "source": "https://www.bankofengland.co.uk/prudential-regulation/publication/2022/november/implementation-of-the-basel-3-1-standards/output-floor"},
    {"context_id": "tier1_pillar1_uk_2021", "metric": "Tier 1 Ratio", "context_type": "regulatory_minimum", "value": 6.0, "unit": "%", "denominator": "RWA", "jurisdiction": "UK", "scope": "risk-based capital framework", "basis": "unknown", "effective_from": 2021, "effective_to": None, "source": "https://www.bankofengland.co.uk/prudential-regulation/publication/2022/november/implementation-of-the-basel-3-1-standards/output-floor"},
    {"context_id": "totalcapital_pillar1_uk_2021", "metric": "Total Capital Ratio", "context_type": "regulatory_minimum", "value": 8.0, "unit": "%", "denominator": "RWA", "jurisdiction": "UK", "scope": "risk-based capital framework", "basis": "unknown", "effective_from": 2021, "effective_to": None, "source": "https://www.bankofengland.co.uk/prudential-regulation/publication/2022/november/implementation-of-the-basel-3-1-standards/output-floor"},
    {"context_id": "cocb_uk_2021", "metric": "CET1 Ratio", "context_type": "buffer", "value": 2.5, "unit": "%", "denominator": "RWA", "jurisdiction": "UK", "scope": "banks", "basis": "unknown", "effective_from": 2021, "effective_to": None, "source": "https://www.bankofengland.co.uk/-/media/boe/files/stress-testing/2024/boes-approach-to-stress-testing-the-uk-banking-system.pdf"},
    {"context_id": "leverage_uk_325_2024", "metric": "Leverage Ratio", "context_type": "regulatory_minimum_or_supervisory_expectation", "value": 3.25, "unit": "%", "denominator": "UK leverage exposure measure", "jurisdiction": "UK", "scope": "major UK firms/significant non-UK assets; supervisory expectation otherwise", "basis": "unknown", "effective_from": 2024, "effective_to": None, "source": "https://www.bankofengland.co.uk/prudential-regulation/publication/2025/march/leverage-ratio-changes-to-the-retail-deposits-threshold-for-application-of-the-requirement"},
    {"context_id": "lcr_uk_100_2021", "metric": "LCR", "context_type": "regulatory_minimum", "value": 100.0, "unit": "%", "denominator": "30-day net liquidity outflows", "jurisdiction": "UK", "scope": "credit institutions", "basis": "unknown", "effective_from": 2021, "effective_to": None, "source": "https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/policy-statement/2021/october/ps2221app1.pdf"},
    {"context_id": "nsfr_uk_100_2021", "metric": "NSFR", "context_type": "regulatory_minimum", "value": 100.0, "unit": "%", "denominator": "one-year required stable funding", "jurisdiction": "UK", "scope": "firms under NSFR framework", "basis": "unknown", "effective_from": 2021, "effective_to": None, "source": "https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/consultation-paper/2021/february/cp521.pdf"},
    {"context_id": "mrel_firm_specific_2026", "metric": "MREL Ratio", "context_type": "firm_specific_requirement", "value": None, "unit": "%", "denominator": "RWA or leverage exposure measure", "jurisdiction": "UK", "scope": "UK resolution entities with bail-in or transfer strategy", "basis": "firm_specific", "effective_from": 2026, "effective_to": None, "source": "https://www.bankofengland.co.uk/financial-stability/resolution/mrels-2026"},
]


def match_context(observation, metric=None, year=None):
    metric = metric or observation.get("metric") or observation.get("sheet")
    year = year or observation.get("fiscal_year")
    candidates = [item for item in CONTEXT if item["metric"] == metric and item["effective_from"] <= (year or 0) and (item["effective_to"] is None or year <= item["effective_to"])]
    if not candidates:
        return {"status": "context_unavailable", "reason": "no dated context record for metric/period"}
    if observation.get("unit") != "%":
        return {"status": "context_unavailable", "reason": "observation unit does not match percentage context"}
    if not observation.get("reporting_basis"):
        return {"status": "context_unavailable", "reason": "observation reporting basis is not classified"}
    if all(item["value"] is None for item in candidates):
        return {"status": "context_unavailable", "reason": "context is firm-specific and no firm-level requirement is loaded"}
    # Sum minimum + buffer rather than picking one arbitrary matching record -
    # CET1 Ratio genuinely has two simultaneously-applicable context records
    # for the same year (the 4.5% Pillar 1 minimum and the 2.5% buffer).
    # Picking just `next(item for item in candidates if item["value"] is not
    # None)` silently ignored the buffer and understated the real floor -
    # mirrors the fix already applied in in021_headroom_trajectory.py's
    # `applicable_context()`, which computes the same CONTEXT table's
    # minimum+buffer correctly; the two must agree on this or "distance to
    # floor" would mean two different things in two parts of this pipeline.
    valued = [item for item in candidates if item["value"] is not None]
    minimum = sum(item["value"] for item in valued
                  if item["context_type"] in ("regulatory_minimum", "regulatory_minimum_or_supervisory_expectation"))
    buffer_value = sum(item["value"] for item in valued if item["context_type"] == "buffer")
    floor = minimum + buffer_value
    if floor == 0:
        return {"status": "context_unavailable", "reason": "no non-zero regulatory minimum or buffer matched"}
    sources = sorted({item["source"] for item in valued})
    context_ids = [item["context_id"] for item in valued]
    return {"status": "matched", "context_id": context_ids, "value": floor,
            "distance": float(observation["value_numeric"]) - floor,
            "context_type": "minimum_plus_buffer", "source": sources}


def build_context_payload():
    return {"schema_version": SCHEMA_VERSION, "research_note": RESEARCH_NOTE, "generated_at": datetime.now(timezone.utc).isoformat(), "records": CONTEXT,
            "policy": "distance is emitted only for a dated metric/unit/basis match; no universal pass/fail is inferred", "historical_policy": "unmatched effective dates, scope or basis return context_unavailable"}


def export_context(out_dir, db_path=None):
    os.makedirs(out_dir, exist_ok=True)
    payload = build_context_payload()
    with open(os.path.join(out_dir, "regulatory_context.json"), "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")
    with open(os.path.join(out_dir, "regulatory_context.csv"), "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(CONTEXT[0]))
        writer.writeheader()
        writer.writerows(CONTEXT)
    if db_path:
        from analysis_queries import AnalysisQueries
        rows = []
        for observation in AnalysisQueries(db_path).observations():
            match = match_context(observation, metric=observation.get("sheet"), year=observation.get("fiscal_year"))
            context_id = match.get("context_id", "")
            source = match.get("source", "")
            rows.append({"frn": observation.get("frn", ""), "bank": observation.get("canonical_bank", observation.get("bank", "")),
                         "metric": observation.get("sheet", ""), "fiscal_year": observation.get("fiscal_year", ""),
                         "value_numeric": observation.get("value_numeric", ""), "unit": observation.get("unit", ""),
                         "reporting_basis": observation.get("reporting_basis", ""), "context_status": match["status"],
                         "context_id": "; ".join(context_id) if isinstance(context_id, list) else context_id,
                         "context_value": match.get("value", ""), "distance": match.get("distance", ""),
                         "reason": match.get("reason", ""),
                         "source": "; ".join(source) if isinstance(source, list) else source})
        with open(os.path.join(out_dir, "observation_context.csv"), "w", newline="", encoding="utf-8") as handle:
            fields = list(rows[0]) if rows else ["frn"]
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
    return payload


def main():
    root = os.path.join(os.path.dirname(__file__), "..", "..")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=os.path.join(root, "research", "insights.db"))
    parser.add_argument("--out-dir", default=os.path.join(root, "research", "powerbi"))
    args = parser.parse_args()
    payload = export_context(args.out_dir, args.db)
    print(f"Wrote {len(payload['records'])} versioned regulatory context records to {args.out_dir}")


if __name__ == "__main__":
    main()
