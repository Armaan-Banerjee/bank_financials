"""Parent-group level analysis for IN-010.

The public analysis function accepts normalized observations and the typed
FRN-to-group mapping.  Database loading and JSON output are thin adapters.
"""

import argparse
import json
import os
from collections import defaultdict
from statistics import median
from analysis_queries import AnalysisQueries

from in009_analysis import (
    CORE_METRICS,
    _select_metric_observations,
    comparison_diagnostics,
    normalize_observation,
)


def _group_members(groups):
    result = defaultdict(list)
    for frn, (bank, group, caveat) in groups.items():
        result[group].append({"frn": frn, "bank": bank, "caveat": caveat})
    return {group: sorted(members, key=lambda item: item["frn"]) for group, members in sorted(result.items())}


def _level(series_by_frn, members):
    years = sorted({year for series in series_by_frn.values() for year in series}, reverse=True)
    for year in years:
        values = {frn: series[year] for frn, series in series_by_frn.items() if year in series}
        if len(values) >= 2:
            numbers = list(values.values())
            return {
                "status": "comparable",
                "year": year,
                "n": len(values),
                "values": dict(sorted(values.items())),
                "median": median(numbers),
                "min": min(numbers),
                "max": max(numbers),
                "range": max(numbers) - min(numbers),
            }
    return {"status": "insufficient", "reason": "fewer than two entities share a comparable year"}


def _trends(series_by_frn):
    years = sorted({year for series in series_by_frn.values() for year in series})
    rows = []
    for left, right in zip(years, years[1:]):
        changes = [series[right] - series[left] for series in series_by_frn.values() if left in series and right in series]
        if len(changes) < 2:
            continue
        up = sum(change > 0 for change in changes)
        down = sum(change < 0 for change in changes)
        same = len(changes) - up - down
        winning = max(up, down, same)
        direction = "mixed" if (up and down) else "+" if up else "-" if down else "unchanged"
        rows.append({
            "start_year": left,
            "end_year": right,
            "n": len(changes),
            "up": up,
            "down": down,
            "same": same,
            "direction": direction,
            "agreement": winning / len(changes),
        })
    return rows


def analyze_parent_groups(observations, groups, metrics=None):
    """Return latest-level dispersion and trend agreement by metric and group."""
    metrics = metrics or CORE_METRICS
    normalized = [normalize_observation(item) if "fiscal_year" not in item else item for item in observations]
    output = {metric: {"broad": [], "strict": []} for metric in metrics}
    for metric, sheet in metrics.items():
        # Plain sheet filter - see in009_analysis.py's build_in009_payload for
        # why the old `_metric_observations` label-text pre-filter was removed
        # (it silently dropped genuine percentage rows with atypical
        # phrasing before `_select_metric_observations` ever saw them).
        metric_rows = [item for item in normalized if item.get("sheet") == sheet]
        for mode in ("broad", "strict"):
            selected = []
            years = sorted({item.get("fiscal_year") for item in metric_rows if item.get("fiscal_year") is not None})
            for year in years:
                rows, _diagnostics = comparison_diagnostics(metric_rows, mode, fiscal_year=year)
                selected.extend(rows)
            canonical = _select_metric_observations(selected, sheet)
            series = defaultdict(dict)
            for item in canonical:
                series[item["frn"]][item["fiscal_year"]] = float(item["value_numeric"])
            for group, members in _group_members(groups).items():
                member_frns = {member["frn"] for member in members}
                group_series = {frn: series[frn] for frn in member_frns if frn in series}
                output[metric][mode].append({
                    "group": group,
                    "member_count": len(members),
                    "members": members,
                    "latest_level": _level(group_series, members),
                    "trends": _trends(group_series),
                })
    return output


def build_in010_payload(db_path):
    queries = AnalysisQueries(db_path)
    rows = queries.observations()
    groups = queries.groups()
    return {
        "metadata": {"source": os.path.abspath(db_path), "metrics": list(CORE_METRICS)},
        "parent_groups": analyze_parent_groups(rows, groups),
    }


def main():
    root = os.path.join(os.path.dirname(__file__), "..", "..")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=os.path.join(root, "research", "insights.db"))
    parser.add_argument("--out", default=os.path.join(root, "research", "in010_parent_groups.json"))
    args = parser.parse_args()
    payload = build_in010_payload(args.db)
    with open(args.out, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(f"Wrote IN-010 parent-group payload to {args.out}")


if __name__ == "__main__":
    main()
