"""Pure normalization and comparison primitives for IN-009.

The module accepts the row shape returned by ``build_insights_db`` and does not
open databases or format deliverables.  That keeps semantic decisions at one
testable seam while preserving the raw extraction contract for existing
consumers.
"""

import re
import argparse
import json
import os
import tempfile
from datetime import datetime
from collections import defaultdict


_FISCAL_YEAR = re.compile(r"^FY(?P<year>20\d{2})(?P<qualifier>.*)$", re.I)
_MONTHS = re.compile(r"(?P<months>\d{1,2})\s*m(?:o(?:nths?)?)?\b", re.I)
_QUARTER = re.compile(r"(?P<year>20\d{2})\s*[- ]?Q(?P<quarter>[1-4])\b", re.I)
_HALF = re.compile(r"(?P<year>20\d{2})\s*[- ]?H(?P<half>[12])\b", re.I)
_REVERSE_HALF = re.compile(r"H(?P<half>[12])\s+(?P<year>20\d{2})$", re.I)
_ISO_DATE = re.compile(r"(?P<year>20\d{2})-(?P<month>\d{2})-(?P<day>\d{2})$")
_DATE = re.compile(r"(?P<day>\d{1,2})[ -](?P<month>[A-Za-z]{3,9})[ -](?P<year>20\d{2})$")
_MONTH_YEAR = re.compile(r"(?P<month>[A-Za-z]{3,9})[- ](?P<year>\d{2,4})$")


def _date_metadata(text):
    """Return an ISO end date for common interim header formats."""
    iso = _ISO_DATE.fullmatch(text)
    if iso:
        return text, int(iso.group("year"))
    for pattern, kind in ((_DATE, "date"), (_MONTH_YEAR, "month")):
        match = pattern.fullmatch(text)
        if not match:
            continue
        year = int(match.group("year"))
        if year < 100:
            year += 2000
        try:
            month = datetime.strptime(match.group("month")[:3].title(), "%b").month
        except ValueError:
            return None, None
        if kind == "date":
            day = int(match.group("day"))
        else:
            import calendar
            day = calendar.monthrange(year, month)[1]
        return f"{year:04d}-{month:02d}-{day:02d}", year
    return None, None


def normalize_period(period):
    """Return structured fiscal-period metadata without discarding qualifiers."""
    text = (period or "").strip()
    match = _FISCAL_YEAR.fullmatch(text)
    if not match:
        quarter = _QUARTER.fullmatch(text)
        if quarter:
            q = int(quarter.group("quarter"))
            import calendar
            month = q * 3
            return {
                "period_key": text, "fiscal_year": int(quarter.group("year")),
                "period_qualified": True, "period_type": "quarterly",
                "period_length_months": 3,
                "period_end": f"{quarter.group('year')}-{month:02d}-{calendar.monthrange(int(quarter.group('year')), month)[1]:02d}",
                "annual_eligible": False,
            }
        half = _HALF.fullmatch(text)
        if not half:
            half = _REVERSE_HALF.fullmatch(text)
        if half:
            h = int(half.group("half"))
            year = int(half.group("year"))
            import calendar
            month = 6 if h == 1 else 12
            return {
                "period_key": text, "fiscal_year": year,
                "period_qualified": True, "period_type": "semi_annual",
                "period_length_months": 6,
                "period_end": f"{year}-{month:02d}-{calendar.monthrange(year, month)[1]:02d}",
                "annual_eligible": False,
            }
        period_end, fiscal_year = _date_metadata(text)
        if period_end:
            return {
                "period_key": text, "fiscal_year": fiscal_year,
                "period_qualified": True, "period_type": "point_in_time",
                "period_length_months": None, "period_end": period_end,
                "annual_eligible": False,
            }
        return {
            "period_key": text,
            "fiscal_year": None,
            "period_qualified": bool(text),
            "period_type": "unknown",
            "period_length_months": None,
            "period_end": None,
            "annual_eligible": False,
        }

    qualifier = match.group("qualifier").strip()
    month_match = _MONTHS.search(qualifier)
    length = int(month_match.group("months")) if month_match else 12
    return {
        "period_key": text,
        "fiscal_year": int(match.group("year")),
        "period_qualified": bool(qualifier),
        "period_type": "annual",
        "period_length_months": length,
        "period_end": None,
        "annual_eligible": length == 12,
    }


def classify_reporting_basis(text):
    """Classify only explicit basis language; return ``None`` for unknown."""
    value = (text or "").lower()
    if not value:
        return None
    if value.strip() in ("entity", "standalone", "solo"):
        return "entity"
    if value.strip() in ("consolidated_group", "consolidated group", "group"):
        return "consolidated_group"
    if re.search(r"\b(company[- ]only|solo|standalone|entity[- ]level|entity basis|bank/solo)\b", value):
        return "entity"
    if re.search(r"\b(consolidated|group)\b", value) and "not the wider" not in value:
        return "consolidated_group"
    return None


def normalize_observation(raw):
    """Copy a raw row and add canonical period, basis, and value-status fields."""
    result = dict(raw)
    result.update(normalize_period(raw.get("year", "")))
    explicit_basis = classify_reporting_basis(raw.get("reporting_basis", ""))
    result["reporting_basis"] = explicit_basis or classify_reporting_basis(raw.get("basis_note", ""))
    numeric = raw.get("value_numeric")
    raw_value = str(raw.get("value_raw") or "")
    if raw.get("is_numeric") == "1" and numeric not in (None, ""):
        result["value_status"] = "special_numeric" if re.search(r"^\s*999999(?:\.0+)?\s*%", raw_value) else "numeric"
    elif raw_value.strip():
        result["value_status"] = "non_numeric_disclosure"
    else:
        result["value_status"] = "missing"
    return result


_BASIS_PREFERENCE = {"entity": 0, "consolidated_group": 1}


def comparable_observations(observations, mode="broad", fiscal_year=None):
    """Filter normalized observations for one year under a named policy.

    ``broad`` retains valid numeric annual observations. ``strict`` additionally
    requires a known reporting basis.  Shortened periods are excluded from both
    modes because they are not annual observations.
    """
    if mode not in ("strict", "broad"):
        raise ValueError("mode must be 'strict' or 'broad'")
    selected, _ = comparison_diagnostics(observations, mode, fiscal_year)
    return selected


def comparison_diagnostics(observations, mode="broad", fiscal_year=None):
    """Return selected observations and explicit exclusion counts."""
    if mode not in ("strict", "broad"):
        raise ValueError("mode must be 'strict' or 'broad'")
    selected = []
    exclusions = defaultdict(int)
    candidates = []
    for observation in observations:
        if fiscal_year is not None and observation.get("fiscal_year") != fiscal_year:
            continue
        if observation.get("value_status") not in ("numeric", "special_numeric"):
            exclusions[observation.get("value_status", "missing")] += 1
            continue
        if not observation.get("annual_eligible"):
            exclusions["non_annual_period"] += 1
            continue
        candidates.append(observation)
    common_basis = None
    if mode == "strict":
        bases = sorted({item.get("reporting_basis") for item in candidates if item.get("reporting_basis")})
        if bases:
            # Tie-break by an explicit basis preference, not the basis string's
            # alphabetical order - a lexical tie-break is the exact bug pattern
            # that has already caused three confirmed selection bugs elsewhere
            # in this pipeline (see PERCENT_ONLY_SHEETS's docstring above).
            # Entity-level is preferred on a count tie because this map's own
            # destination is entity-level comparison within a parent group.
            common_basis = max(
                bases,
                key=lambda basis: (
                    sum(item.get("reporting_basis") == basis for item in candidates),
                    -_BASIS_PREFERENCE.get(basis, 99),
                ),
            )
    for observation in candidates:
        if mode == "strict":
            if not observation.get("reporting_basis"):
                exclusions["unknown_basis"] += 1
                continue
            if observation.get("reporting_basis") != common_basis:
                exclusions["basis_mismatch"] += 1
                continue
            observation = dict(observation)
            observation["comparability_status"] = "strict-comparable"
        else:
            observation = dict(observation)
            observation["comparability_status"] = "broad-only" if not observation.get("reporting_basis") else "broad-comparable"
        selected.append(observation)
    return selected, dict(sorted(exclusions.items()))


def _label_rank(label):
    value = re.sub(r"\s+", " ", (label or "").strip().lower())
    preferred = {
        "common equity tier 1 (cet1) ratio": 0,
        "cet1 ratio": 1,
        "tier 1 ratio": 0,
        "total capital ratio": 0,
        "leverage ratio excluding claims on central banks (%)": 0,
        "leverage ratio excluding claims on central banks": 1,
        "leverage ratio": 2,
    }
    return preferred.get(value, 10)


PERCENT_ONLY_SHEETS = {
    "CET1 Ratio", "Tier 1 Ratio", "Total Capital Ratio",
    "Leverage Ratio", "LCR", "NSFR", "MREL Ratio",
}
"""Pillar 3 sheets whose selected metric must be a disclosed percentage. Each
of these sheets also carries supporting absolute £m/£bn rows (exposure
measures, eligible-instrument amounts, etc.) alongside the ratio itself; for
a bank/year where the ratio genuinely wasn't disclosed, `_select_metric_observations`
must treat that year as missing, never substitute one of those absolute rows
as if it were the ratio (e.g. Handelsbanken's MREL ratio is undisclosed for
FY2021-FY2024 - only a supporting debt-issuance £m figure exists those
years, which is not the MREL ratio)."""


def _is_percent_value(observation):
    """True when the originally-disclosed row is a percentage, not an
    absolute amount. Checked two ways since either field alone is
    incomplete in real data: the literal '%' usually survives in
    `value_raw` even though `value_numeric` strips it, and `unit` is
    populated for only a minority of rows but is authoritative when
    present. Ratio sheets (Leverage Ratio, LCR, NSFR, MREL Ratio) mix true
    percentage rows with supporting absolute £m/£bn rows under label text
    that varies too much per bank for `_label_rank`'s curated dict to cover
    exhaustively; without this signal the alphabetical tie-break below can
    pick an absolute amount and report it as if it were the ratio (e.g.
    picked "Tier 1 (T1) capital ... (£m)" = 56465 over "UK leverage ratio
    (%)" = 5.8% purely because "T" < "U")."""
    if observation.get("unit") == "%":
        return True
    return "%" in str(observation.get("value_raw") or "")


def build_metric_series(observations, sheet):
    """Select one deterministic numeric series per FRN for a metric sheet."""
    selected_observations = _select_metric_observations(observations, sheet)
    selected = defaultdict(dict)
    for observation in selected_observations:
        selected[observation["frn"]][observation["fiscal_year"]] = float(observation["value_numeric"])
    return {frn: dict(sorted(values.items())) for frn, values in selected.items()}


def _select_metric_observations(observations, sheet=None):
    """Select one deterministic observation per entity/year, retaining provenance."""
    by_bank_label = defaultdict(lambda: defaultdict(list))
    for observation in observations:
        if sheet is not None and observation.get("sheet") != sheet:
            continue
        if observation.get("value_status") not in ("numeric", "special_numeric"):
            continue
        by_bank_label[observation["frn"]][observation["row_label"]].append(observation)

    selected = []
    for frn, labels in by_bank_label.items():
        def _label_sort_key(name, labels=labels):
            rows = labels[name]
            all_percent = all(_is_percent_value(row) for row in rows)
            return (-len(rows), _label_rank(name), 0 if all_percent else 1, name.lower())

        label = min(labels, key=_label_sort_key)
        observations_by_year = defaultdict(list)
        for candidate_label, candidate_rows in labels.items():
            for observation in candidate_rows:
                observations_by_year[observation.get("fiscal_year")].append((candidate_label, observation))
        for year, candidates in observations_by_year.items():
            candidates = [candidate for candidate in candidates if candidate[1].get("annual_eligible")]
            if sheet in PERCENT_ONLY_SHEETS:
                candidates = [c for c in candidates if _is_percent_value(c[1])]
            if not candidates:
                continue
            primary = [candidate for candidate in candidates if candidate[0] == label]
            pool = primary or sorted(
                candidates,
                key=lambda item: (
                    _label_rank(item[0]),
                    0 if _is_percent_value(item[1]) else 1,
                    item[0].lower(),
                ),
            )
            observation = sorted(
                pool,
                key=lambda item: (
                    item[1].get("period_qualified", False),
                    item[1].get("period_key", ""),
                    _label_rank(item[0]),
                    0 if _is_percent_value(item[1]) else 1,
                    item[0].lower(),
                ),
            )[0][1]
            if year is not None:
                selected.append(observation)
    return selected


def pairwise_trend(series, left, right):
    """Count direction of change among entities with both observations."""
    changes = [
        values[right] - values[left]
        for values in series.values()
        if left in values and right in values
    ]
    down = sum(change < 0 for change in changes)
    up = sum(change > 0 for change in changes)
    return {"down": down, "up": up, "same": len(changes) - down - up, "n": len(changes)}


def _percentile(values, fraction):
    values = sorted(values)
    if not values:
        return None
    position = (len(values) - 1) * fraction
    lower = int(position)
    upper = min(lower + 1, len(values) - 1)
    weight = position - lower
    return values[lower] + (values[upper] - values[lower]) * weight


def detect_outliers(observations, metric, sheet=None):
    """Return flagged latest observations with transparent statistical reasons."""
    annual = [item for item in _select_metric_observations(observations, sheet) if item.get("annual_eligible")]
    by_frn = defaultdict(list)
    for item in annual:
        by_frn[item["frn"]].append(item)
    latest = {frn: max(items, key=lambda item: item["fiscal_year"]) for frn, items in by_frn.items()}
    values = [float(item["value_numeric"]) for item in latest.values()]
    if len(values) < 3:
        return []
    median = _percentile(values, 0.5)
    deviations = [abs(value - median) for value in values]
    mad = _percentile(deviations, 0.5)
    low, high = _percentile(values, 0.05), _percentile(values, 0.95)
    movements = []
    for items in by_frn.values():
        ordered = sorted(items, key=lambda item: item["fiscal_year"])
        movements.extend(
            abs(float(right["value_numeric"]) - float(left["value_numeric"]))
            for left, right in zip(ordered, ordered[1:])
        )
    movement_cutoff = _percentile(movements, 0.95) if movements else None

    result = []
    for frn, item in latest.items():
        value = float(item["value_numeric"])
        reasons = []
        if low is not None and value < low:
            reasons.append("level below 5th percentile")
        if high is not None and value > high:
            reasons.append("level above 95th percentile")
        if mad and abs(0.6745 * (value - median) / mad) >= 3.5:
            reasons.append("robust level score at least 3.5")
        # mad == 0 (>=50% of latest values tied at the median) leaves the
        # robust z-score undefined, so it's intentionally skipped rather than
        # dividing by zero - the percentile-bound and movement checks above/
        # below still cover this case independently.
        prior = [candidate for candidate in by_frn[frn] if candidate["fiscal_year"] < item["fiscal_year"]]
        if prior and movement_cutoff is not None:
            change = value - float(max(prior, key=lambda candidate: candidate["fiscal_year"])["value_numeric"])
            if abs(change) > movement_cutoff:
                reasons.append("year-over-year movement above 95th percentile")
        raw = str(item.get("value_raw") or "")
        if re.search(r"999999|not publicly disclosed|not applicable", raw, re.I):
            reasons.append("special or non-standard disclosure")
        if reasons:
            result.append({
                "metric": metric,
                "frn": frn,
                "bank": item.get("bank", ""),
                "fiscal_year": item["fiscal_year"],
                "value": value,
                "reasons": reasons,
                "reporting_basis": item.get("reporting_basis"),
                "comparability_status": item.get("comparability_status", "unknown"),
                "source_note": item.get("source_note", ""),
            })
    return sorted(result, key=lambda item: (item["metric"], item["frn"]))


CORE_METRICS = {
    "CET1 Ratio": "CET1 Ratio",
    "Tier 1 Ratio": "Tier 1 Ratio",
    "Total Capital Ratio": "Total Capital Ratio",
    "Leverage Ratio": "Leverage Ratio",
}


def _trend_rows(series, metric, years=None):
    if years is None:
        years = sorted({year for values in series.values() for year in values})
    rows = []
    for left, right in zip(years, years[1:]):
        counts = pairwise_trend(series, left, right)
        if counts["n"]:
            rows.append({"metric": metric, "start_year": left, "end_year": right, **counts})
    long_run_changes = []
    endpoints = []
    for values in series.values():
        available = sorted(values)
        if len(available) >= 2:
            endpoints.append((available[0], available[-1]))
            long_run_changes.append(values[available[-1]] - values[available[0]])
    if long_run_changes:
        rows.append({
            "metric": metric,
            "start_year": min(left for left, _ in endpoints),
            "end_year": max(right for _, right in endpoints),
            "horizon": "long_run",
            "down": sum(change < 0 for change in long_run_changes),
            "up": sum(change > 0 for change in long_run_changes),
            "same": sum(change == 0 for change in long_run_changes),
            "n": len(long_run_changes),
        })
    return rows


def build_in009_payload(db_path):
    """Build the JSON-serializable IN-009 payload from the source database."""
    import build_insights_db

    raw_rows = build_insights_db.load_rows_from_db(db_path)
    normalized = [normalize_observation(raw) for raw in raw_rows]
    payload = {"metadata": {"source": db_path, "metrics": list(CORE_METRICS)},
               "coverage": {}, "trends": {"broad": [], "strict": []},
               "outliers": {"broad": [], "strict": []}}
    for metric, sheet in CORE_METRICS.items():
        # Filter by sheet only - do not re-apply a label-text heuristic here.
        # `_select_metric_observations`/`comparison_diagnostics` already do the
        # real, correct percent-vs-absolute filtering downstream (via
        # PERCENT_ONLY_SHEETS), and this pre-filter used to require the literal
        # word "ratio" in the label (or exclude any "exposure"-labeled row for
        # Leverage) - a genuine percentage row with atypical phrasing would be
        # silently dropped here before the good selector ever saw it.
        metric_rows = [item for item in normalized if item.get("sheet") == sheet]
        payload["coverage"][metric] = {}
        for mode in ("broad", "strict"):
            years = sorted({item.get("fiscal_year") for item in metric_rows if item.get("fiscal_year") is not None})
            eligible = []
            exclusions = defaultdict(int)
            for fiscal_year in years:
                selected, diagnostics = comparison_diagnostics(metric_rows, mode=mode, fiscal_year=fiscal_year)
                eligible.extend(selected)
                for reason, count in diagnostics.items():
                    exclusions[reason] += count
            series = build_metric_series(eligible, sheet)
            payload["coverage"][metric][mode] = {
                "observations": len(eligible),
                "banks": len(series),
                "years": sorted({item["fiscal_year"] for item in eligible}),
                "exclusions": dict(sorted(exclusions.items())),
            }
            payload["trends"][mode].extend(_trend_rows(series, metric))
            payload["outliers"][mode].extend(detect_outliers(eligible, metric, sheet))
    return payload


def render_quality_report(payload):
    """Render a concise deterministic Markdown report from a payload."""
    lines = [
        "# IN-009 core-ratio quality and screening report",
        "",
        f"Source database: `{payload['metadata']['source']}`",
        "",
        "## Coverage",
        "",
        "| Metric | Mode | Observations | Banks | Years | Exclusions |",
        "|---|---|---:|---:|---|---|",
    ]
    for metric in payload["metadata"]["metrics"]:
        for mode in ("broad", "strict"):
            coverage = payload["coverage"][metric][mode]
            years = ", ".join(str(year) for year in coverage["years"])
            exclusions = ", ".join(f"{key}: {value}" for key, value in coverage.get("exclusions", {}).items()) or "none"
            lines.append(f"| {metric} | {mode} | {coverage['observations']} | {coverage['banks']} | {years} | {exclusions} |")
    lines += [
        "",
        "Strict mode includes numeric annual observations with an explicitly classified reporting basis.",
        "Broad mode includes numeric annual observations with a 12-month annual period; unknown basis is retained.",
        "",
        "## Outliers",
        "",
        "| Mode | Metric | FRN | Bank | Year | Value | Reasons |",
        "|---|---|---:|---|---:|---:|---|",
    ]
    for mode in ("broad", "strict"):
        for item in payload["outliers"][mode]:
            reasons = "; ".join(item["reasons"])
            lines.append(f"| {mode} | {item['metric']} | {item['frn']} | {item['bank']} | {item['fiscal_year']} | {item['value']} | {reasons} |")
    lines += [
        "",
        "## Method",
        "",
        "Levels are flagged below the 5th or above the 95th percentile, or at a robust score of at least 3.5.",
        "Year-over-year movement is flagged above the 95th percentile of observed absolute movements.",
        "Special or non-standard disclosures are surfaced as domain flags and are not silently discarded.",
    ]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=os.path.join(os.path.dirname(__file__), "..", "..", "research", "insights.db"))
    parser.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "..", "..", "research", "in009_analysis.json"))
    parser.add_argument("--report", default=os.path.join(os.path.dirname(__file__), "..", "..", "research", "in009_quality.md"))
    args = parser.parse_args()
    payload = build_in009_payload(args.db)
    _write_if_changed(args.out, json.dumps(payload, indent=2, sort_keys=True) + "\n")
    _write_if_changed(args.report, render_quality_report(payload))
    print(f"Wrote IN-009 payload to {args.out}")
    print(f"Wrote IN-009 quality report to {args.report}")


def _write_if_changed(path, content):
    """Atomically write generated content, preserving unchanged files."""
    directory = os.path.dirname(os.path.abspath(path)) or "."
    previous = None
    try:
        with open(path, encoding="utf-8") as handle:
            previous = handle.read()
    except FileNotFoundError:
        pass
    if previous == content:
        return
    os.makedirs(directory, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".in009_", dir=directory, text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


if __name__ == "__main__":
    main()
