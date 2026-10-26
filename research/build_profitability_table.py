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
# FY2020 is extracted but not reported: an AVERAGE denominator for FY2021 needs
# the year before it. The user's decision of 2026-10-10 is that the denominator
# is the AVERAGE, for ROA as well as ROE - so assets now need the prior year
# too, which the first version of this file did not capture.
EXTRACT_YEARS = YEARS + ["FY2020"]

# Row resolution lives in scripts/profitability_rows.py and is IMPORTED, not
# restated, because BankWorkbook.add_profitability_sheet must resolve the same
# rows the same way. Two copies of this logic would drift the moment one was
# corrected, which is the defect class CLAUDE.md documents for the Overview
# ratio derivation. The tables and their reasoning moved verbatim.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                os.pardir, 'scripts'))
from profitability_rows import (  # noqa: E402
    NUM_RE, FY_RE, UNIT_RE, canon, norm, to_num, rank_row, read_sheet, pick,
    PROFIT_PATTERNS, PROFIT_EXCLUDE, PBT_PATTERNS, PBT_EXCLUDE,
    TCI_PATTERNS, TCI_EXCLUDE, EQUITY_PATTERNS, EQUITY_EXCLUDE,
    ASSET_PATTERNS, ASSET_EXCLUDE,
)
# Likewise imported, not restated: whether a ratio across a bank's two
# statement sheets cancels its units. The first edition of this table gated
# only on `units_agree`, which is TRUE for all 725 bank-years - the two sheets
# are both labelled GBP - and so never fired on the case that matters, where
# the balance sheet was converted at year-end SPOT and the profit and loss at
# the year's AVERAGE. That shipped 360 contaminated ratio cells across 20
# banks into the 2026-10-22 edition. See scripts/profitability_fx_basis.py.
from profitability_fx_basis import (  # noqa: E402
    ENTITY_MISMATCH, FX_RATIO_BASIS,
)


def basis_refusal(bank, year):
    """-> a reason string if this bank-year's ratio does not cancel, else None."""
    if bank in ENTITY_MISMATCH:
        return ("the Balance Sheet and the Profit & Loss describe different "
                "entities - " + ENTITY_MISMATCH[bank])
    verdict = FX_RATIO_BASIS.get(bank)
    if verdict in (None, "cancels"):
        return None
    if verdict == "mixed" or (isinstance(verdict, (set, frozenset))
                              and year in verdict):
        return ("the numerator and the denominator are converted on different "
                "bases - balance-sheet stocks at the year-end SPOT rate, "
                "profit-and-loss flows at that year's AVERAGE rate - so the "
                "ratio does not cancel its unit")
    return None


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

        p_lab, profit = pick(pl, PROFIT_PATTERNS, PROFIT_EXCLUDE, YEARS)
        pbt_lab, pbt = pick(pl, PBT_PATTERNS, PBT_EXCLUDE, YEARS)
        tci_lab, tci = pick(pl, TCI_PATTERNS, TCI_EXCLUDE, YEARS)
        e_lab, equity = pick(bs, EQUITY_PATTERNS, EQUITY_EXCLUDE, YEARS)
        a_lab, assets = pick(bs, ASSET_PATTERNS, ASSET_EXCLUDE, YEARS)
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
                "assets_prior_year": assets.get(prev) if assets else None,
                "unit": pl_unit if same_unit else None,
                "pl_unit": pl_unit, "bs_unit": bs_unit, "units_agree": same_unit,
                "profit_row": p_lab, "equity_row": e_lab, "assets_row": a_lab,
                "pl_year_label": pl_lab.get(y), "bs_year_label": bs_lab.get(y),
                "profit_before_tax": pbt.get(y) if pbt else None,
                "total_comprehensive_income": tci.get(y) if tci else None,
                "pbt_row": pbt_lab, "tci_row": tci_lab,
                "basis_refused": None,
                "roe_avg_equity": None, "roe_year_end": None,
                "roa_avg_assets": None, "roa_year_end": None,
            }
            # AVERAGE is the headline denominator (user, 2026-10-10), for ROA
            # as well as ROE. The year-end variant is kept in its own column
            # rather than dropped, for two reasons: it is the only figure
            # available for a bank's oldest reported year, where no prior-year
            # balance sheet exists; and an outside figure that reproduces on
            # one basis and not the other is how a divergence gets EXPLAINED
            # rather than merely reported - thebanks.eu's United Trust ROA of
            # 1.79% reproduces on average assets (1.789%) and not on year-end
            # (1.681%), which is what identified their basis.
            rec["basis_refused"] = basis_refusal(rec["bank"], rec["year"])
            if (same_unit and rec["basis_refused"] is None
                    and rec["profit_after_tax"] is not None):
                p = rec["profit_after_tax"]
                if rec["total_equity"]:
                    rec["roe_year_end"] = round(100.0 * p / rec["total_equity"], 2)
                    if rec["equity_prior_year"]:
                        avg = (rec["total_equity"] + rec["equity_prior_year"]) / 2.0
                        if avg:
                            rec["roe_avg_equity"] = round(100.0 * p / avg, 2)
                if rec["total_assets"]:
                    rec["roa_year_end"] = round(100.0 * p / rec["total_assets"], 2)
                    if rec["assets_prior_year"]:
                        avg_a = (rec["total_assets"] + rec["assets_prior_year"]) / 2.0
                        if avg_a:
                            rec["roa_avg_assets"] = round(100.0 * p / avg_a, 2)
            out.append(rec)

    json.dump({"rows": out, "unmatched": unmatched, "unit_mismatch": unit_mismatch},
              open(sys.argv[1], "w"), indent=1)
    banks = {r["bank"] for r in out}
    print(f"{len(banks)} banks x {len(YEARS)} years = {len(out)} bank-years")
    print(f"  ROE (avg equity): {sum(1 for r in out if r['roe_avg_equity'] is not None)}")
    print(f"  ROE (year-end):   {sum(1 for r in out if r['roe_year_end'] is not None)}")
    print(f"  ROA (avg assets): {sum(1 for r in out if r['roa_avg_assets'] is not None)}")
    print(f"  ROA (year-end):   {sum(1 for r in out if r['roa_year_end'] is not None)}")
    print(f"  banks with an unmatched input: {len(unmatched)}")
    print(f"  banks whose P&L and Balance Sheet units differ: {len(unit_mismatch)}")


if __name__ == "__main__":
    main()
