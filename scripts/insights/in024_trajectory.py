"""Persistent bank trajectories and fixed-panel rank mobility (IN-024)."""

import argparse
import json
import os
from collections import defaultdict
from tempfile import NamedTemporaryFile

from in009_analysis import CORE_METRICS, _select_metric_observations, normalize_observation
from in016_distribution import percentile_rank


MIN_OBSERVATIONS = 4
MIN_CHANGES = 3
FLAT_TOLERANCE = 0.01


def direction(change, tolerance=FLAT_TOLERANCE):
    """Classify one adjacent-year change without turning missing into zero."""
    if change is None:
        return "missing"
    change = float(change)
    if abs(change) < tolerance:
        return "flat"
    return "up" if change > 0 else "down"


def score_fingerprint(directions, magnitudes=None, minimum_changes=MIN_CHANGES):
    """Score a direction fingerprint and suppress insufficient series."""
    usable = [item for item in directions if item in ("up", "down", "flat")]
    magnitudes = list(magnitudes or [])
    up = usable.count("up")
    down = usable.count("down")
    flat = usable.count("flat")
    changes = len(usable)
    total_change = sum(float(value) for value in magnitudes) if magnitudes else None
    robust_total_change = total_change
    if magnitudes:
        ordered = sorted(float(value) for value in magnitudes)
        median = ordered[len(ordered) // 2] if len(ordered) % 2 else (ordered[len(ordered) // 2 - 1] + ordered[len(ordered) // 2]) / 2
        deviations = sorted(abs(value - median) for value in ordered)
        mad = deviations[len(deviations) // 2] if len(deviations) % 2 else (deviations[len(deviations) // 2 - 1] + deviations[len(deviations) // 2]) / 2
        if mad:
            robust_total_change = sum(max(median - 3 * mad, min(median + 3 * mad, value)) for value in ordered)
    result = {
        "changes": changes, "up_changes": up, "down_changes": down,
        "flat_changes": flat, "persistence_score": None,
        "total_change": total_change, "robust_total_change": robust_total_change,
        "status": "insufficient_series", "label": None,
    }
    if changes < minimum_changes:
        return result
    dominant = max(up, down)
    result["persistence_score"] = dominant / changes
    if dominant / changes >= 0.75 and dominant > 0:
        result["label"] = "persistent_up" if up >= down else "persistent_down"
    else:
        result["label"] = "mixed"
    result["status"] = "eligible"
    return result


def _metric_rows(rows, sheet):
    return {
        (item["frn"], item["fiscal_year"]): item
        for item in _select_metric_observations(rows, sheet)
        if item.get("annual_eligible")
    }


def _trajectory_record(bank, metric, selected, years):
    points = []
    changes = []
    for year in years:
        row = selected.get((bank[0], year))
        points.append({"year": year, "value": None if row is None else float(row["value_numeric"]),
                       "status": "missing" if row is None else "numeric",
                       "reporting_basis": None if row is None else row.get("reporting_basis"),
                       "source_note": None if row is None else row.get("basis_note")})
    for previous, current in zip(points, points[1:]):
        delta = None if previous["value"] is None or current["value"] is None else current["value"] - previous["value"]
        changes.append({"start_year": previous["year"], "end_year": current["year"],
                        "change": delta, "direction": direction(delta)})
    usable = [item for item in changes if item["change"] is not None]
    score = score_fingerprint([item["direction"] for item in usable], [item["change"] for item in usable])
    score["bank"] = bank[1]
    score["frn"] = bank[0]
    score["metric"] = metric
    score["first_year"] = usable[0]["start_year"] if usable else None
    score["last_year"] = usable[-1]["end_year"] if usable else None
    return {"frn": bank[0], "bank": bank[1], "metric": metric, "years": points,
            "changes": changes, "score": score}


def fixed_panel_mobility(rows, metric, sheet, years):
    """Return deterministic same-basis rank panels for every adjacent year pair."""
    selected = _metric_rows(rows, sheet)
    result = []
    for start, end in zip(years, years[1:]):
        candidates = {}
        for (frn, year), row in selected.items():
            if year in (start, end) and row.get("reporting_basis"):
                candidates.setdefault(frn, {})[year] = row
        bases = defaultdict(int)
        for values in candidates.values():
            if start in values and end in values and values[start].get("reporting_basis") == values[end].get("reporting_basis"):
                bases[values[start]["reporting_basis"]] += 1
        basis = max(bases, key=lambda value: (bases[value], value)) if bases else None
        panel = [frn for frn, values in candidates.items() if basis and start in values and end in values
                 and values[start].get("reporting_basis") == basis and values[end].get("reporting_basis") == basis]
        start_values = sorted(((float(selected[(frn, start)]["value_numeric"]), frn) for frn in panel), reverse=True)
        end_values = sorted(((float(selected[(frn, end)]["value_numeric"]), frn) for frn in panel), reverse=True)
        start_rank = {frn: 1 + sum(value > current for value, _ in start_values) for current, frn in start_values}
        end_rank = {frn: 1 + sum(value > current for value, _ in end_values) for current, frn in end_values}
        result.append({"start_year": start, "end_year": end, "reporting_basis": basis,
                       "n": len(panel), "status": "eligible" if len(panel) >= 8 else "insufficient_panel",
                       "records": [{"frn": frn, "start_rank": start_rank[frn], "end_rank": end_rank[frn],
                                    "rank_change": end_rank[frn] - start_rank[frn]} for frn in sorted(panel)]})
    return result


def build_in024_payload(db_path):
    from analysis_queries import AnalysisQueries
    rows = AnalysisQueries(db_path).observations()
    banks = {}
    for row in rows:
        banks.setdefault(row["frn"], row.get("canonical_bank") or row.get("bank") or row["frn"])
    years = sorted({row.get("fiscal_year") for row in rows if row.get("fiscal_year") is not None})
    payload = {"metadata": {"source": os.path.abspath(db_path), "minimum_observations": MIN_OBSERVATIONS,
                             "minimum_changes": MIN_CHANGES, "flat_tolerance": FLAT_TOLERANCE,
                             "default_mode": "broad", "rank_policy": "same-basis fixed panel; rank 1 is highest ratio"},
               "trajectories": {}, "rank_mobility": {}, "coverage_churn": {}}
    for metric, sheet in CORE_METRICS.items():
        selected = _metric_rows(rows, sheet)
        trajectories = [_trajectory_record(bank, metric, selected, years) for bank in sorted(banks.items())]
        payload["trajectories"][metric] = trajectories
        payload["rank_mobility"][metric] = fixed_panel_mobility(rows, metric, sheet, years)
        eligible_by_year = {year: {frn for (frn, current_year), row in selected.items() if current_year == year} for year in years}
        churn = []
        for start, end in zip(years, years[1:]):
            retained = eligible_by_year[start] & eligible_by_year[end]
            churn.append({"start_year": start, "end_year": end, "start_n": len(eligible_by_year[start]),
                          "end_n": len(eligible_by_year[end]), "retained_n": len(retained),
                          "entered": sorted(eligible_by_year[end] - eligible_by_year[start]),
                          "exited": sorted(eligible_by_year[start] - eligible_by_year[end])})
        payload["coverage_churn"][metric] = churn
    return payload


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
    parser.add_argument("--out", default=os.path.join(root, "research", "in024_trajectory.json"))
    args = parser.parse_args()
    write_json_atomic(build_in024_payload(args.db), args.out)
    print(f"Wrote IN-024 trajectory payload to {args.out}")


if __name__ == "__main__":
    main()
