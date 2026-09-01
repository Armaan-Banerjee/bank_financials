"""Conservative distributional benchmarks for comparable annual data (IN-016)."""

import argparse
import csv
import json
import os
from collections import defaultdict

from in009_analysis import (
    CORE_METRICS,
    _is_percent_value,
    _select_metric_observations,
    comparable_observations,
)
from in012_absolute_analysis import ABSOLUTE_METRICS, normalize_amount_observation

MIN_DISTRIBUTION_N = 8


def percentile(values, fraction):
    values = sorted(float(value) for value in values)
    if not values:
        return None
    position = (len(values) - 1) * fraction
    low = int(position)
    high = min(low + 1, len(values) - 1)
    return values[low] + (values[high] - values[low]) * (position - low)


def percentile_rank(value, values):
    values = [float(item) for item in values]
    if not values:
        return None
    less = sum(item < value for item in values)
    equal = sum(item == value for item in values)
    return (less + equal / 2) / len(values) * 100


def summarize(values):
    """Apply documented N gates to one exact cohort."""
    values = [float(value) for value in values]
    n = len(values)
    result = {"n": n, "minimum": min(values) if values else None,
              "maximum": max(values) if values else None, "p10": None,
              "p90": None, "q1": None, "median": None, "q3": None,
              "iqr": None, "mad": None,
              "status": "insufficient_cohort" if n < 8 else "small_n" if n < 12 else "comparable"}
    if n < 8:
        return result
    result["q1"] = percentile(values, 0.25)
    result["p10"] = percentile(values, 0.10)
    result["median"] = percentile(values, 0.5)
    result["q3"] = percentile(values, 0.75)
    result["p90"] = percentile(values, 0.90)
    result["iqr"] = result["q3"] - result["q1"]
    if n >= 12:
        result["mad"] = percentile([abs(value - result["median"]) for value in values], 0.5)
    return result


def distribution_for_metric(observations, metric, sheet, mode="strict", fiscal_year=None, reporting_basis=None):
    """Build one exact metric/year/basis cohort; never mixes years or bases."""
    # CORE_METRICS sheets carry supporting absolute £m/£bn rows (exposure
    # measures, capital amounts) alongside the true percentage ratio under
    # label text too varied to key off reliably - keep only disclosed
    # percentages, or an outlier absolute figure gets treated as if it were
    # the ratio itself (e.g. a leverage exposure measure inflating the
    # "Leverage Ratio" distribution's p90 into the hundreds of thousands).
    source = [row for row in observations if row.get("sheet") == sheet and _is_percent_value(row)]
    if mode == "strict" and reporting_basis is None:
        bases = {row.get("reporting_basis") for row in source if row.get("fiscal_year") == fiscal_year and row.get("reporting_basis")}
        if len(bases) != 1:
            return {"metric": metric, "mode": mode, "fiscal_year": fiscal_year,
                    "reporting_basis": reporting_basis, "summary": {"n": 0, "status": "ambiguous_basis"}, "observations": []}
    if mode == "strict" and reporting_basis:
        # An explicitly requested basis is already the comparability decision.
        # Do not run it through comparable_observations(), which deliberately
        # selects a modal basis and can silently discard this cohort.
        selected = [row for row in source
                    if row.get("annual_eligible") and row.get("fiscal_year") == fiscal_year
                    and row.get("reporting_basis") == reporting_basis]
    else:
        selected = comparable_observations(source, mode=mode, fiscal_year=fiscal_year)
    selected = [row for row in selected if row.get("value_status") == "numeric"]
    canonical = _select_metric_observations(selected, sheet)
    rows = sorted(
        [row for row in canonical
         if row.get("fiscal_year") == fiscal_year
         and (reporting_basis is None or row.get("reporting_basis") == reporting_basis)],
        key=lambda row: row["frn"],
    )
    values = [float(row["value_numeric"]) for row in rows]
    summary = summarize(values)
    if mode == "broad":
        summary["status"] = "coverage_only"
    if summary["status"] not in ("insufficient_cohort", "coverage_only"):
        for row in rows:
            value = float(row["value_numeric"])
            row["value"] = value
            row["percentile_rank"] = percentile_rank(value, values)
            row["robust_z"] = None if summary["mad"] in (None, 0) else 0.67448975 * (value - summary["median"]) / summary["mad"]
    return {"metric": metric, "mode": mode, "fiscal_year": fiscal_year,
            "reporting_basis": reporting_basis, "summary": summary, "observations": rows}


def _ranked(rows):
    values = [float(row["value_numeric"]) for row in rows]
    for row in rows:
        row["value"] = float(row["value_numeric"])
        row["percentile_rank"] = percentile_rank(row["value"], values)
    return rows


def _exact_cohort(observations, sheet, year, basis, amount=False, unit=None):
    rows = [row for row in _select_metric_observations(observations, sheet)
            if row.get("fiscal_year") == year and row.get("reporting_basis") == basis]
    if amount:
        rows = [row for row in rows if row.get("amount_unit") == unit]
    return _ranked(rows)


def _cohort_record(metric, year, basis, rows, **extra):
    summary = summarize([row["value_numeric"] for row in rows])
    if summary["status"] not in ("insufficient_cohort",):
        for row in rows:
            row["robust_z"] = None if summary["mad"] in (None, 0) else 0.67448975 * (row["value"] - summary["median"]) / summary["mad"]
    result = {"metric": metric, "fiscal_year": year, "reporting_basis": basis,
              "summary": summary, "observations": rows}
    result.update(extra)
    return result


def _load_peer_groups(db_path):
    path = os.path.join(os.path.dirname(db_path), "bank_clusters.csv")
    if not os.path.exists(path):
        return {}
    with open(path, newline="", encoding="utf-8") as handle:
        return {str(row["frn"]): row.get("cluster_label") or f"cluster {row.get('cluster_id', '')}"
                for row in csv.DictReader(handle) if row.get("frn") and row.get("insufficient_data") != "1"}


def _group_benchmark_coverage(observations, groups, group_type):
    """Return coverage and suppressed cohorts; never publish tiny benchmarks."""
    result = {"model": group_type, "minimum_n": MIN_DISTRIBUTION_N, "groups": [], "eligible": 0, "suppressed": 0}
    for name, members in sorted(groups.items()):
        available = len({row.get("frn") for row in observations if row.get("frn") in members})
        status = "eligible" if available >= MIN_DISTRIBUTION_N else "suppressed_insufficient_cohort"
        result["groups"].append({"group": name, "members": available, "status": status})
        result["eligible" if status == "eligible" else "suppressed"] += 1
    return result


def build_in016_payload(db_path):
    from analysis_queries import AnalysisQueries
    observations = AnalysisQueries(db_path).observations()
    payload = {"metadata": {"source": db_path, "minimum_n": MIN_DISTRIBUTION_N,
                             "statistics": ["median", "quartiles", "iqr", "mad", "percentile_rank", "robust_z"],
                             "policy": "strict exact fiscal-year, reporting-basis and amount-unit cohorts; broad is coverage-only",
                             "rank_change": "end_rank minus start_rank; negative means movement toward rank 1"},
               "distributions": {}, "absolute_distributions": {}, "rank_movement": {},
               "group_benchmark_coverage": {}}
    for metric, sheet in CORE_METRICS.items():
        metric_rows = [row for row in observations if row.get("sheet") == sheet]
        years = sorted({row.get("fiscal_year") for row in metric_rows if row.get("fiscal_year") is not None})
        cohorts = []
        for year in years:
            bases = sorted({row.get("reporting_basis") for row in metric_rows if row.get("fiscal_year") == year and row.get("reporting_basis")})
            for basis in bases:
                cohorts.append(distribution_for_metric(observations, metric, sheet, "strict", year, basis))
        payload["distributions"][metric] = {"strict": cohorts,
                                             "broad": [distribution_for_metric(observations, metric, sheet, "broad", year) for year in years]}

        movements = []
        for start, end in zip(years, years[1:]):
            bases = sorted({row.get("reporting_basis") for row in metric_rows
                            if row.get("fiscal_year") in (start, end) and row.get("reporting_basis")})
            for basis in bases:
                before = {row["frn"]: row for row in _exact_cohort(observations, sheet, start, basis)}
                after = {row["frn"]: row for row in _exact_cohort(observations, sheet, end, basis)}
                common = sorted(set(before) & set(after))
                panel = []
                if len(common) >= MIN_DISTRIBUTION_N:
                    start_rows = _ranked([before[frn] for frn in common])
                    end_rows = _ranked([after[frn] for frn in common])
                    start_map = {row["frn"]: row for row in start_rows}
                    end_map = {row["frn"]: row for row in end_rows}
                    for frn in common:
                        # start_rank/end_rank are filled in by the loop just
                        # below, not here - _ranked() never sets a "rank" key
                        # (it computes percentile rank, not ordinal rank), so
                        # this dict only ever needs a placeholder.
                        panel.append({"frn": frn, "bank": end_map[frn].get("bank", end_map[frn].get("canonical_bank", frn)),
                                      "start_value": start_map[frn]["value"], "end_value": end_map[frn]["value"],
                                      "start_rank": None, "end_rank": None})
                # rank is assigned separately because percentile rank is not ordinal rank.
                if panel:
                    for row in panel:
                        start_values = sorted(item["start_value"] for item in panel)
                        end_values = sorted(item["end_value"] for item in panel)
                        row["start_rank"] = 1 + sum(value < row["start_value"] for value in start_values) + (sum(value == row["start_value"] for value in start_values) - 1) / 2
                        row["end_rank"] = 1 + sum(value < row["end_value"] for value in end_values) + (sum(value == row["end_value"] for value in end_values) - 1) / 2
                        row["rank_change"] = row["end_rank"] - row["start_rank"]
                movements.append({"metric": metric, "start_year": start, "end_year": end, "reporting_basis": basis,
                                  "n": len(common), "status": "comparable" if len(common) >= MIN_DISTRIBUTION_N else "insufficient_cohort",
                                  "up": sum(row["rank_change"] < 0 for row in panel), "down": sum(row["rank_change"] > 0 for row in panel),
                                  "same": sum(row["rank_change"] == 0 for row in panel), "observations": panel})
        payload["rank_movement"][metric] = movements

    amount_observations = [normalize_amount_observation(row) for row in observations]
    for metric, sheet in ABSOLUTE_METRICS.items():
        metric_rows = [row for row in amount_observations if row.get("sheet") == sheet]
        cohorts = []
        years = sorted({row.get("fiscal_year") for row in metric_rows if row.get("fiscal_year") is not None})
        for year in years:
            pairs = sorted({(row.get("reporting_basis"), row.get("amount_unit")) for row in metric_rows
                            if row.get("fiscal_year") == year and row.get("reporting_basis") and row.get("amount_unit")})
            for basis, unit in pairs:
                rows = _exact_cohort(amount_observations, sheet, year, basis, amount=True, unit=unit)
                cohorts.append(_cohort_record(metric, year, basis, rows, amount_unit=unit))
        payload["absolute_distributions"][metric] = cohorts

    group_map = AnalysisQueries(db_path).groups()
    parent_groups = defaultdict(set)
    for frn, (_bank, group, _status) in group_map.items():
        if group:
            parent_groups[group].add(frn)
    peer_members = defaultdict(set)
    for frn, label in _load_peer_groups(db_path).items():
        peer_members[label].add(frn)
    payload["group_benchmark_coverage"] = {
        "parent": _group_benchmark_coverage(observations, parent_groups, "ultimate parent group"),
        "peer": _group_benchmark_coverage(observations, peer_members, "peer cluster"),
    }
    return payload


def main():
    root = os.path.join(os.path.dirname(__file__), "..", "..")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=os.path.join(root, "research", "insights.db"))
    parser.add_argument("--out", default=os.path.join(root, "research", "in016_distribution.json"))
    args = parser.parse_args()
    with open(args.out, "w", encoding="utf-8") as handle:
        json.dump(build_in016_payload(args.db), handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(f"Wrote IN-016 distribution payload to {args.out}")


if __name__ == "__main__":
    main()
