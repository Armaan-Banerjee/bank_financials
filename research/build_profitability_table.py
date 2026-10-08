#!/usr/bin/env /usr/bin/python3
"""Build the UK bank ROE / ROA table from the delivered workbooks.

Reads banks/*.xlsx (the delivered artefact, which is current - insights.db is a
periodic extract and lags it), pulls profit after tax, total equity and total
assets off the Profit & Loss and Balance Sheet sheets, and computes ROE and ROA.

It does NOT write to any workbook. Output is research/UK_banks_profitability_*.

Three rules this file exists to enforce, all of them from the project's standing
practice rather than invented here:
  - every value carries its provenance, and computed values are never merged
    into the same column as published ones;
  - a scale mismatch between the two sheets is reported, never silently divided
    through - the ratio only cancels the unit if both sides share it;
  - a row we cannot match is listed by name, never dropped silently, because a
    silent drop is indistinguishable from a bank that does not disclose.
"""
import glob
import json
import os
import re
import sys

import openpyxl

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
# FY2020 is extracted but not reported: an average-equity denominator for
# FY2021 needs the year before it.
EXTRACT_YEARS = YEARS + ["FY2020"]

FY_RE = re.compile(r"^(FY\d{4})")
UNIT_RE = re.compile(r"\(([^)]*)\)\s*$")
NUM_RE = re.compile(r"^-?[\d,]+\.?\d*$")

# Banks write the same line a dozen ways: "(Loss)/Profit after tax", "Profit/
# (loss) for the year", "Total equity (Shareholders' funds)". canon() strips the
# alternation parentheses and any trailing parenthetical gloss so one pattern
# covers the family, instead of one pattern per spelling.
_ALT_PAREN = re.compile(r"\((loss|losses|deficit|profit|surplus|charge|credit)e?s?\)", re.I)
_TRAIL_PAREN = re.compile(r"\s*\([^)]*\)\s*$")


def canon(label):
    lab = re.sub(r"\s+", " ", str(label or "")).strip().lower().rstrip(":")
    lab = _TRAIL_PAREN.sub("", lab)        # "total equity (shareholders' funds)"
    lab = _ALT_PAREN.sub("", lab)          # "(loss)/profit after tax"
    lab = lab.replace("\u2019", "'").replace("`", "'")
    lab = lab.replace("'", "")             # shareholders' -> shareholders
    lab = re.sub(r"[/,]", " ", lab)
    return re.sub(r"\s+", " ", lab).strip()


# Ranked: lower number wins. Ranking rather than first-match matters because a
# sheet may carry several admissible rows, and "profit for the year" must beat
# "profit and total comprehensive income for the year" where both are present.
PROFIT_PATTERNS = [
    # "loss" and "deficit" are first-class here, not an afterthought: a loss is
    # a valid numerator and a negative return is a real figure. Matching only
    # "profit" silently dropped every loss-making bank in the corpus - Afin,
    # Chetwood, Kroo, Monument, Oxbury, Griffin, The Bank of London, This Bank -
    # which is exactly the population a profitability table most needs to show.
    (1, r"^(net |total )?(profit|loss|surplus|deficit) (after|net of) tax"),
    # The words between the noun and "after tax" vary by bank: "on ordinary
    # activities after tax", "from ordinary activities after tax", "on
    # activities after tax". Allow a gap rather than one pattern per spelling.
    (1, r"^(net |total )?(profit|loss|surplus|deficit)\b.{0,45}(after|net of) tax"),
    (1, r"^(net |total )?(profit|loss|surplus|deficit)( attributable to [\w ]+)? for the (financial )?(year|period)$"),
    (2, r"^(net |total )?(profit|loss|surplus|deficit).{0,60}for the (financial )?(year|period)"),
    (2, r"^(profit|loss|surplus|deficit) attributable to"),
    (3, r"^(net |total )?(profit|loss|surplus|deficit)$"),
    (3, r"^retained (profit|earnings|loss) for the (financial )?year"),
]
# "before tax" is excluded outright - a pre-tax numerator in a return series is
# the mixed-basis trap this project documents elsewhere. Note "comprehensive
# income" is NOT excluded: for most small banks profit IS total comprehensive
# income and the sheet prints them as one line, so excluding it loses the bank.
PROFIT_EXCLUDE = re.compile(
    r"before tax|before income tax|before taxation|pre-tax|operating|"
    r"company-only|bank company|parent|discontinued|per share|margin|"
    r"underlying|adjusted|impairment|interest|fee|commission|trading|"
    r"foreign exchange|dealing|investment|disposal|fair value|hedge",
    re.I,
)
# Alternative numerators, captured so a divergence can be EXPLAINED rather than
# just reported. A published "ROE" is often struck on one of these instead of
# profit after tax, and saying which one is far more useful than saying the
# figures disagree: Al Rayan's three published values all reproduce exactly on
# profit BEFORE tax, and Lloyds' on total comprehensive income.
PBT_PATTERNS = [
    (1, r"^(net |total )?(profit|loss|surplus|deficit)\b.{0,45}before (tax|taxation|income tax)"),
    (2, r"^operating (profit|loss)\b.{0,30}before tax"),
]
PBT_EXCLUDE = re.compile(r"after tax|impairment|per share|underlying|adjusted|company-only|parent", re.I)
TCI_PATTERNS = [(1, r"^total comprehensive (income|loss|expense)")]
TCI_EXCLUDE = re.compile(r"company-only|parent|attributable to non-controlling", re.I)
EQUITY_PATTERNS = [
    (1, r"^total equity$"),
    (1, r"^total (shareholders|shareholder|owners|owner|member) (equity|funds)$"),
    (1, r"^(equity )?(shareholders|shareholder|owners|owner|member) (equity|funds)$"),
    (2, r"^total equity attributable to"),
    (2, r"^equity attributable to"),
    (2, r"^total (share capital and reserves|capital and reserves)$"),
    # "Total shareholders funds - equity interests" (Bank Mandiri Europe)
    (2, r"^total (shareholders|shareholder|owners|owner|member) (equity|funds)\b"),
    (3, r"^total (equity|reserves) "),
]
EQUITY_EXCLUDE = re.compile(r"liabilit|non-controlling|minority|excluding", re.I)
ASSET_PATTERNS = [(1, r"^total assets$")]
ASSET_EXCLUDE = re.compile(r"liabilit|weighted|risk|excluding", re.I)


def norm(s):
    return re.sub(r"\s+", " ", str(s or "")).strip()


def to_num(v):
    if isinstance(v, (int, float)):
        return float(v)
    s = norm(v).replace("£", "").replace("$", "").replace("€", "")
    if s.startswith("(") and s.endswith(")"):
        s = "-" + s[1:-1]
    s = s.replace(",", "")
    return float(s) if NUM_RE.match(s) else None


def rank_row(label, patterns, exclude):
    """Best (lowest) matching rank for a label, or None if it matches nothing."""
    lab = canon(label)
    if exclude.search(lab):
        return None
    ranks = [r for r, p in patterns if re.search(p, lab)]
    return min(ranks) if ranks else None


def read_sheet(ws):
    """-> (unit, {label: {year: number}}) for one statement sheet."""
    rows = list(ws.iter_rows(values_only=True))
    # Find the header row by SCORE, not by first match. A sheet's subtitle
    # routinely opens with a year - Recognise Bank's reads "FY2025-FY2026
    # Company/standalone basis..." - so a first-match scan locks onto the
    # subtitle and then treats column 0, the label column, as a data column.
    # That lost three banks outright here; in a sheet whose subtitle mentioned
    # a year further along the row it would instead have assigned figures to
    # the WRONG YEAR, silently. Hence: year columns never include column 0,
    # and the row with the most of them wins.
    hdr_i, col_year, unit, best = None, {}, None, 0
    for i, row in enumerate(rows[:8]):
        cells = [norm(c) for c in row]
        years = {j: FY_RE.match(c).group(1)
                 for j, c in enumerate(cells) if j > 0 and FY_RE.match(c)}
        if len(years) > best:
            hdr_i, col_year, best = i, years, len(years)
    if hdr_i is not None:
        cells = [norm(c) for c in rows[hdr_i]]
        for j in col_year:
            m = UNIT_RE.search(cells[j])
            if m and not unit:
                unit = m.group(1)
    if hdr_i is None:
        return None, {}, {}
    # Keep each year column's RAW header. The year key alone hides that a
    # column may not be a 12-month year or even the same entity: Clydesdale's
    # FY2025 is an 18-month transition period, Griffin's and StreamBank's
    # FY2023 are 15 months, and Monzo's FY2024 switches from MBL to MBHG.
    # Dividing an 18-month profit by a year-end balance sheet overstates the
    # return, and nothing downstream can detect that from "FY2025".
    year_label = {y: norm(rows[hdr_i][j]) for j, y in col_year.items()}
    out = {}
    for row in rows[hdr_i + 1:]:
        label = norm(row[0] if row else "")
        if not label:
            continue
        vals = {}
        for j, y in col_year.items():
            if j < len(row):
                n = to_num(row[j])
                if n is not None:
                    vals[y] = n
        if vals:
            out.setdefault(label, vals)
    return unit, out, year_label


def pick(rows, patterns, exclude):
    """Best row, scored (rank, -years covered, sheet order).

    Coverage breaks a rank tie because a sheet may carry two equally
    well-named rows where only one spans the reporting years: Bank Sepah
    International prints both "Total assets" and "Total assets (FY2026
    presentation)", and the latter - which canonicalises identically once the
    trailing gloss is stripped - holds a single FY2026 figure. Taking it cost
    all five of that bank's ROA years. Sheet order is the last tiebreak, since
    statements run top-to-bottom and the earlier row is the primary
    presentation.
    """
    best = None
    for i, (label, vals) in enumerate(rows.items()):
        r = rank_row(label, patterns, exclude)
        if r is None:
            continue
        key = (r, -sum(1 for y in YEARS if y in vals), i)
        if best is None or key < best[0]:
            best = (key, label, vals)
    return (best[1], best[2]) if best else (None, None)


def main():
    out, unmatched, unit_mismatch = [], [], []
    for path in sorted(glob.glob("banks/*FINANCIALS.xlsx")):
        bank = os.path.basename(path).replace(" FINANCIALS.xlsx", "")
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        pl_unit, pl, pl_lab = (None, {}, {})
        bs_unit, bs, bs_lab = (None, {}, {})
        if "Profit & Loss" in wb.sheetnames:
            pl_unit, pl, pl_lab = read_sheet(wb["Profit & Loss"])
        if "Balance Sheet" in wb.sheetnames:
            bs_unit, bs, bs_lab = read_sheet(wb["Balance Sheet"])
        wb.close()

        p_lab, profit = pick(pl, PROFIT_PATTERNS, PROFIT_EXCLUDE)
        pbt_lab, pbt = pick(pl, PBT_PATTERNS, PBT_EXCLUDE)
        tci_lab, tci = pick(pl, TCI_PATTERNS, TCI_EXCLUDE)
        e_lab, equity = pick(bs, EQUITY_PATTERNS, EQUITY_EXCLUDE)
        a_lab, assets = pick(bs, ASSET_PATTERNS, ASSET_EXCLUDE)
        missing = [n for n, v in (("profit", profit), ("equity", equity), ("assets", assets)) if not v]
        if missing:
            unmatched.append({"bank": bank, "missing": missing})
        # A ratio cancels its unit only if both sides share one.
        same_unit = (pl_unit or "") == (bs_unit or "")
        if profit and (equity or assets) and not same_unit:
            unit_mismatch.append({"bank": bank, "pl_unit": pl_unit, "bs_unit": bs_unit})

        for y in YEARS:
            prev = "FY" + str(int(y[2:]) - 1)
            rec = {
                "bank": bank, "year": y,
                "profit_after_tax": profit.get(y) if profit else None,
                "total_equity": equity.get(y) if equity else None,
                "total_assets": assets.get(y) if assets else None,
                "equity_prior_year": equity.get(prev) if equity else None,
                "unit": pl_unit if same_unit else None,
                "pl_unit": pl_unit, "bs_unit": bs_unit, "units_agree": same_unit,
                "profit_row": p_lab, "equity_row": e_lab, "assets_row": a_lab,
                "pl_year_label": pl_lab.get(y), "bs_year_label": bs_lab.get(y),
                "profit_before_tax": pbt.get(y) if pbt else None,
                "total_comprehensive_income": tci.get(y) if tci else None,
                "pbt_row": pbt_lab, "tci_row": tci_lab,
                "roe_avg_equity": None, "roe_year_end": None, "roa": None,
            }
            if same_unit and rec["profit_after_tax"] is not None:
                p = rec["profit_after_tax"]
                if rec["total_equity"]:
                    rec["roe_year_end"] = round(100.0 * p / rec["total_equity"], 2)
                    if rec["equity_prior_year"]:
                        avg = (rec["total_equity"] + rec["equity_prior_year"]) / 2.0
                        if avg:
                            rec["roe_avg_equity"] = round(100.0 * p / avg, 2)
                if rec["total_assets"]:
                    rec["roa"] = round(100.0 * p / rec["total_assets"], 2)
            out.append(rec)

    json.dump({"rows": out, "unmatched": unmatched, "unit_mismatch": unit_mismatch},
              open(sys.argv[1], "w"), indent=1)
    banks = {r["bank"] for r in out}
    print(f"{len(banks)} banks x {len(YEARS)} years = {len(out)} bank-years")
    print(f"  ROE (avg equity): {sum(1 for r in out if r['roe_avg_equity'] is not None)}")
    print(f"  ROE (year-end):   {sum(1 for r in out if r['roe_year_end'] is not None)}")
    print(f"  ROA:              {sum(1 for r in out if r['roa'] is not None)}")
    print(f"  banks with an unmatched input: {len(unmatched)}")
    print(f"  banks whose P&L and Balance Sheet units differ: {len(unit_mismatch)}")


if __name__ == "__main__":
    main()
