"""CET1 ratio movement decomposition for IN-022."""

import argparse
import json
import os
from tempfile import NamedTemporaryFile

from in009_analysis import _select_metric_observations, normalize_observation
from in012_absolute_analysis import normalize_amount_observation


def _numeric(observation):
    return observation is not None and observation.get("value_status") in ("numeric", "special_numeric") and observation.get("value_numeric") is not None


def _relative_change(start, end):
    if float(start) == 0:
        return None
    return round((float(end) - float(start)) / abs(float(start)) * 100, 2)


def fit_trend(records, x_key, y_key):
    """Fit an OLS line and R² for selected numeric fields."""
    pairs = [(float(row[x_key]), float(row[y_key])) for row in records if row.get(x_key) is not None and row.get(y_key) is not None]
    result = {"n": len(pairs), "slope": None, "intercept": None, "r_squared": None, "status": "insufficient_data" if len(pairs) < 2 else "ok"}
    if len(pairs) < 2:
        return result
    x_mean = sum(x for x, _ in pairs) / len(pairs)
    y_mean = sum(y for _, y in pairs) / len(pairs)
    denominator = sum((x - x_mean) ** 2 for x, _ in pairs)
    if denominator == 0:
        result["status"] = "insufficient_variation"
        return result
    slope = sum((x - x_mean) * (y - y_mean) for x, y in pairs) / denominator
    intercept = y_mean - slope * x_mean
    residual = sum((y - (intercept + slope * x)) ** 2 for x, y in pairs)
    total = sum((y - y_mean) ** 2 for _, y in pairs)
    result.update({"slope": round(slope, 6), "intercept": round(intercept, 6), "r_squared": None if total == 0 else round(1 - residual / total, 6)})
    return result


def decompose_pair(capital_start, capital_end, rwa_start, rwa_end, ratio_start, ratio_end, mode="broad"):
    """Classify one annual CET1 capital/RWA/ratio movement.

    Broad mode permits an unknown reporting basis but still requires a known,
    consistent amount unit and no explicit basis conflict. Strict mode also
    requires a known, consistent reporting basis. This is a semantic seam used
    by both the database analysis and its tests.
    """
    if mode not in ("broad", "strict"):
        raise ValueError("mode must be 'broad' or 'strict'")
    amounts = (capital_start, capital_end, rwa_start, rwa_end)
    if any(not _numeric(item) for item in amounts):
        return {"status": "insufficient_data", "reason": "missing_amount_observation"}
    if not _numeric(ratio_start) or not _numeric(ratio_end):
        return {"status": "insufficient_data", "reason": "missing_ratio_observation"}
    units = {item.get("amount_unit") for item in amounts}
    if None in units:
        return {"status": "incompatible", "reason": "unknown_unit"}
    if len(units) != 1:
        return {"status": "incompatible", "reason": "unit_mismatch"}
    bases = {item.get("reporting_basis") for item in amounts}
    known_bases = bases - {None, ""}
    if len(known_bases) > 1:
        return {"status": "incompatible", "reason": "basis_mismatch"}
    if mode == "strict" and (not known_bases or None in bases or "" in bases):
        return {"status": "incompatible", "reason": "unknown_basis"}
    capital_change = _relative_change(capital_start["value_numeric"], capital_end["value_numeric"])
    rwa_change = _relative_change(rwa_start["value_numeric"], rwa_end["value_numeric"])
    if capital_change is None:
        return {"status": "incompatible", "reason": "zero_capital_start"}
    if rwa_change is None:
        return {"status": "incompatible", "reason": "zero_rwa_start"}
    if capital_change == 0 and rwa_change == 0:
        pattern = "neither"
    elif capital_change == 0:
        pattern = "rwa_only"
    elif rwa_change == 0:
        pattern = "capital_only"
    else:
        pattern = "both"
    return {
        "status": "comparable",
        "comparability_mode": mode,
        "amount_unit": next(iter(units)),
        "reporting_basis": next(iter(known_bases)) if known_bases else None,
        "capital_change_pct": capital_change,
        "rwa_change_pct": rwa_change,
        "ratio_change_pp": round(float(ratio_end["value_numeric"]) - float(ratio_start["value_numeric"]), 2),
        "movement_pattern": pattern,
    }


def _selected(observations, sheet):
    normalized = [normalize_amount_observation(item) if sheet in ("CET1 Capital", "Total RWAs") else normalize_observation(item) for item in observations]
    return {(item["frn"], item["fiscal_year"]): item for item in _select_metric_observations(normalized, sheet) if item.get("annual_eligible")}


def analyze_decomposition(observations, start_year=2023, end_year=2024, mode="broad"):
    capital = _selected(observations, "CET1 Capital")
    rwa = _selected(observations, "Total RWAs")
    ratio = _selected(observations, "CET1 Ratio")
    banks = {item["frn"]: item.get("bank", item.get("canonical_bank", "")) for item in observations}
    frns = sorted({frn for frn, year in capital if year in (start_year, end_year)} | {frn for frn, year in rwa if year in (start_year, end_year)} | {frn for frn, year in ratio if year in (start_year, end_year)})
    records = []
    exclusions = {}
    for frn in frns:
        result = decompose_pair(capital.get((frn, start_year)), capital.get((frn, end_year)), rwa.get((frn, start_year)), rwa.get((frn, end_year)), ratio.get((frn, start_year)), ratio.get((frn, end_year)), mode)
        if result["status"] != "comparable":
            exclusions[result["reason"]] = exclusions.get(result["reason"], 0) + 1
            continue
        result.update({"frn": frn, "bank": banks.get(frn, frn), "start_year": start_year, "end_year": end_year, "capital_start": capital[(frn, start_year)]["value_numeric"], "capital_end": capital[(frn, end_year)]["value_numeric"], "rwa_start": rwa[(frn, start_year)]["value_numeric"], "rwa_end": rwa[(frn, end_year)]["value_numeric"], "latest_capital": capital[(frn, end_year)]["value_numeric"], "capital_source_note": capital[(frn, end_year)].get("source_note", ""), "rwa_source_note": rwa[(frn, end_year)].get("source_note", "")})
        records.append(result)
    return {"start_year": start_year, "end_year": end_year, "mode": mode, "coverage": {"candidate_banks": len(frns), "comparable_banks": len(records), "exclusions": dict(sorted(exclusions.items()))}, "records": records}


def write_json_atomic(payload, output_path):
    output_dir = os.path.dirname(os.path.abspath(output_path)) or "."
    os.makedirs(output_dir, exist_ok=True)
    with NamedTemporaryFile("w", encoding="utf-8", dir=output_dir, delete=False) as handle:
        temporary_path = handle.name
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")
    os.replace(temporary_path, output_path)


def build_in022_payload(db_path):
    from analysis_queries import AnalysisQueries
    rows = AnalysisQueries(db_path).observations()
    return {"metadata": {"source": os.path.abspath(db_path), "metric": "CET1 ratio decomposition"}, "broad": analyze_decomposition(rows), "strict": analyze_decomposition(rows, mode="strict")}


def main():
    root = os.path.join(os.path.dirname(__file__), "..", "..")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=os.path.join(root, "research", "insights.db"))
    parser.add_argument("--out", default=os.path.join(root, "research", "in022_ratio_decomposition.json"))
    args = parser.parse_args()
    write_json_atomic(build_in022_payload(args.db), args.out)
    print(f"Wrote IN-022 ratio-decomposition payload to {args.out}")


if __name__ == "__main__":
    main()
