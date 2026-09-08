"""Absolute capital and RWA analysis for IN-012."""

import argparse
import json
import os
import re
from collections import defaultdict
from tempfile import NamedTemporaryFile

from in009_analysis import normalize_observation


ABSOLUTE_METRICS = {
    "CET1 Capital": "CET1 Capital",
    "Tier 1 Capital": "Tier 1 Capital",
    "Total Capital": "Total Capital",
    "Total RWAs": "Total RWAs",
}


def classify_amount_unit(text):
    """Return a conservative unit key from explicit source text."""
    value = (text or "").lower().replace(" ", "")
    if not value:
        return None
    if re.search(r"£(?:'|’)?000|gbp(?:'|’)?000|pounds(?:'|’)?000", value):
        return "GBP_thousand"
    if re.search(r"£m|gbpm|£million|gbpmillion", value):
        return "GBP_million"
    if re.search(r"\$(?:'|’)?000|usd(?:'|’)?000", value):
        return "USD_thousand"
    if re.search(r"\$m|usdm|\$million|usdmillion", value):
        return "USD_million"
    if re.search(r"€(?:'|’)?000|eur(?:'|’)?000", value):
        return "EUR_thousand"
    if re.search(r"€m|eurm|€million|eurmillion", value):
        return "EUR_million"
    if re.search(r"cad(?:'|’)?000", value):
        return "CAD_thousand"
    if re.search(r"cadm|cadmillion", value):
        return "CAD_million"
    if re.search(r"£|gbp|pounds", value):
        return "GBP_unit"
    if re.search(r"\$|usd", value):
        return "USD_unit"
    if re.search(r"€|eur", value):
        return "EUR_unit"
    if re.search(r"\bcad\b", value):
        return "CAD_unit"
    return None


def normalize_amount_observation(raw):
    result = normalize_observation(raw)
    result["amount_unit"] = classify_amount_unit(raw.get("unit", "")) or classify_amount_unit(raw.get("basis_note", ""))
    result["amount_unit_status"] = "known" if result["amount_unit"] else "unknown"
    return result


def scale_adjusted_ratio(capital, rwa):
    """Return capital/RWA as a percentage only for matched unit and basis."""
    if any(item.get("value_status") not in ("numeric", "special_numeric") for item in (capital, rwa)):
        return None
    if capital.get("amount_unit") is None or capital.get("amount_unit") != rwa.get("amount_unit"):
        return None
    if not capital.get("reporting_basis") or capital.get("reporting_basis") != rwa.get("reporting_basis"):
        return None
    denominator = float(rwa["value_numeric"])
    if denominator == 0:
        return None
    return float(capital["value_numeric"]) / denominator * 100


def assign_size_bands(values):
    """Assign deterministic small/medium/large bands by ranked value."""
    ordered = sorted(values.items(), key=lambda item: (item[1], item[0]))
    count = len(ordered)
    result = {}
    for index, (frn, _value) in enumerate(ordered):
        rank = (index + 1) / count if count else 0
        result[frn] = "small" if rank <= 1 / 3 else "medium" if rank <= 2 / 3 else "large"
    return result


def _selected_rows(observations, sheet):
    rows = [item for item in observations if item.get("sheet") == sheet and item.get("annual_eligible") and item.get("value_status") in ("numeric", "special_numeric")]
    by_key = {}
    for item in rows:
        key = (item["frn"], item["fiscal_year"])
        current = by_key.get(key)
        candidate_key = (item.get("period_qualified", False), item.get("period_key", ""), str(item.get("value_raw", "")))
        current_key = (current.get("period_qualified", False), current.get("period_key", ""), str(current.get("value_raw", ""))) if current else None
        if current is None or candidate_key < current_key:
            by_key[key] = item
    return sorted(by_key.values(), key=lambda item: (item["frn"], item["fiscal_year"]))


def _series(rows):
    result = defaultdict(dict)
    identities = defaultdict(set)
    for item in rows:
        identity = (item.get("amount_unit"), item.get("reporting_basis"))
        if all(identity):
            identities[item["frn"]].add(identity)
            result[item["frn"]][item["fiscal_year"]] = float(item["value_numeric"])
    stable = {
        frn: dict(sorted(values.items()))
        for frn, values in result.items()
        if len(identities[frn]) == 1
    }
    return stable


def analyze_absolute_metrics(observations, metrics=None):
    metrics = metrics or ABSOLUTE_METRICS
    normalized = [normalize_amount_observation(item) if "fiscal_year" not in item else item for item in observations]
    output = {}
    selected_by_sheet = {}
    for metric, sheet in metrics.items():
        rows = _selected_rows(normalized, sheet)
        selected_by_sheet[sheet] = rows
        series = _series(rows)
        years = sorted({year for values in series.values() for year in values})
        trends = []
        for left, right in zip(years, years[1:]):
            changes = [values[right] - values[left] for values in series.values() if left in values and right in values]
            if changes:
                trends.append({"start_year": left, "end_year": right, "n": len(changes), "up": sum(x > 0 for x in changes), "down": sum(x < 0 for x in changes), "same": sum(x == 0 for x in changes)})
        latest_rows = {}
        for item in rows:
            current = latest_rows.get(item["frn"])
            if current is None or (item["fiscal_year"], item["period_key"]) > (current["fiscal_year"], current["period_key"]):
                latest_rows[item["frn"]] = item
        latest = {frn: float(item["value_numeric"]) for frn, item in latest_rows.items()}
        latest_metadata = {
            frn: {
                "amount_unit": item.get("amount_unit"),
                "reporting_basis": item.get("reporting_basis"),
            }
            for frn, item in latest_rows.items()
        }
        cohorts = defaultdict(dict)
        for frn, item in latest_rows.items():
            if item.get("reporting_basis") and item.get("amount_unit"):
                cohorts[(item["amount_unit"], item["reporting_basis"])][frn] = latest[frn]
        size_bands = {}
        size_cohorts = []
        for (amount_unit, reporting_basis), cohort_values in sorted(cohorts.items()):
            cohort_status = "comparable" if len(cohort_values) >= 3 else "insufficient_cohort"
            if cohort_status == "comparable":
                size_bands.update(assign_size_bands(cohort_values))
            size_cohorts.append({
                "amount_unit": amount_unit,
                "reporting_basis": reporting_basis,
                "banks": sorted(cohort_values),
                "count": len(cohort_values),
                "status": cohort_status,
            })
        unstable_banks = sorted({
            item["frn"] for item in rows
            if item.get("amount_unit") and item.get("reporting_basis")
            and item["frn"] not in series
        })
        output[metric] = {
            "coverage": {
                "observations": len(rows),
                "known_unit_observations": sum(bool(item.get("amount_unit")) for item in rows),
                "unknown_unit_observations": sum(not item.get("amount_unit") for item in rows),
                "banks": len(series),
                "years": years,
                "known_unit_banks": len(series),
                "unstable_unit_or_basis_banks": len(unstable_banks),
                "unstable_unit_or_basis_bank_ids": unstable_banks,
            },
            "latest": {
                "values": latest,
                "years": {frn: item["fiscal_year"] for frn, item in latest_rows.items()},
                "metadata": latest_metadata,
            },
            "trends": trends,
            "size_bands": size_bands,
            "size_cohorts": size_cohorts,
        }
    capital_sheets = {metric: selected_by_sheet[sheet] for metric, sheet in metrics.items() if metric != "Total RWAs"}
    rwa_by_key = {(item["frn"], item["fiscal_year"]): item for item in selected_by_sheet.get("Total RWAs", [])}
    for metric, rows in capital_sheets.items():
        adjusted = {}
        exclusions = defaultdict(int)
        for item in rows:
            rwa = rwa_by_key.get((item["frn"], item["fiscal_year"]))
            if rwa is None:
                exclusions["missing_rwa"] += 1
                continue
            if not item.get("amount_unit") or not rwa.get("amount_unit"):
                exclusions["unknown_unit"] += 1
                continue
            if item.get("amount_unit") != rwa.get("amount_unit"):
                exclusions["unit_mismatch"] += 1
                continue
            if not item.get("reporting_basis") or not rwa.get("reporting_basis"):
                exclusions["unknown_basis"] += 1
                continue
            if item.get("reporting_basis") != rwa.get("reporting_basis"):
                exclusions["basis_mismatch"] += 1
                continue
            if float(rwa["value_numeric"]) == 0:
                exclusions["zero_rwa"] += 1
                continue
            ratio = scale_adjusted_ratio(item, rwa)
            if ratio is not None:
                adjusted.setdefault(item["frn"], {})[item["fiscal_year"]] = ratio
        scale_adjusted = {frn: dict(sorted(values.items())) for frn, values in adjusted.items()}
        output[metric]["scale_adjusted"] = scale_adjusted
        output[metric]["scale_adjusted_coverage"] = {
            "banks": len(scale_adjusted),
            "observations": sum(len(values) for values in scale_adjusted.values()),
            "years": sorted({year for values in scale_adjusted.values() for year in values}),
            "exclusions": dict(sorted(exclusions.items())),
        }
    return output


def write_json_atomic(payload, output_path):
    """Write a deterministic JSON artefact without leaving a partial file."""
    output_dir = os.path.dirname(os.path.abspath(output_path)) or "."
    os.makedirs(output_dir, exist_ok=True)
    with NamedTemporaryFile("w", encoding="utf-8", dir=output_dir, delete=False) as handle:
        temporary_path = handle.name
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")
    os.replace(temporary_path, output_path)


def build_in012_payload(db_path):
    from analysis_queries import AnalysisQueries
    rows = AnalysisQueries(db_path).observations()
    return {"metadata": {"source": os.path.abspath(db_path), "metrics": list(ABSOLUTE_METRICS)}, "absolute_metrics": analyze_absolute_metrics(rows)}


def main():
    root = os.path.join(os.path.dirname(__file__), "..", "..")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=os.path.join(root, "research", "insights.db"))
    parser.add_argument("--out", default=os.path.join(root, "research", "in012_absolute_analysis.json"))
    args = parser.parse_args()
    write_json_atomic(build_in012_payload(args.db), args.out)
    print(f"Wrote IN-012 absolute-analysis payload to {args.out}")


if __name__ == "__main__":
    main()
