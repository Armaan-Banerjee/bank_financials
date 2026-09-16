# Zenith 1000x scale defect — fix log (2026-09-15)

Target: `scripts/build_zenith.py` -> `banks/ZENITH FINANCIALS.xlsx`
Ticket source: `research/RESUME_SESSION.md` section 8a.

## 1. VERIFICATION OF THE DIAGNOSIS — CONFIRMED FROM PRIMARY SOURCES

The Pillar 3 dictionaries hold **US$'000**, not raw USD. Confirmed by opening the cited
source PDFs, not by inference.

### FY2024 Pillar 3 (`media/2274/31dec24-pillar-3-zbuk.pdf`, section 9 "Key Metrics", p.17)
Table header reads `Available own funds (US$)` and **every figure carries a literal
trailing " k"**:

```
Common Equity Tier 1 (CET1) capital                            378,325 k    338,086 k
Tier 1 capital                                                 378,325 k    338,086 k
Total capital                                                  378,325 k    338,086 k
Total risk-weighted exposure amount*                         1,475,750 k  1,203,364 k
Total exposure measure excluding claims on central banks      2,987,483 k  2,872,422 k
Total high-quality liquid assets (HQLA) (Weighted – average)  1,013,789 k  1,147,653 k
Total net cash outflows (adjusted value)                        306,820 k    369,648 k
Total available stable funding (avg last four quarters)       1,136,904 k  1,066,880 k
Total required stable funding (avg last four quarters)          768,308 k    744,377 k
```

The same page's footnote spells the unit out in prose: *"the average ASF **US$1,136,904k**
/ the average RSF **US$768,308k** = 147.98%"*.

Independent corroboration inside the same document (section UK CC1, p.20): the Bank's
share capital is **"136,701,620 ordinary shares of US$1"** and the capital table renders
that line as **`136,702 k`**. A figure known to be US$136,701,620 printed as 136,702 is
proof that the table scale is thousands.

### FY2024 Pillar 3, UK OV1 (p.21) — the RWA Breakdown source
Column header `US$`, every cell suffixed ` k`:
`Credit Risk (excluding CCR) 1,205,520 k / CCR 98,068 k / of which CVA 1,392 k /
Market risk 4,202 k / Operational Risk (BIA) 167,960 k / Amounts below thresholds 1,024 k /
Total 1,475,750 k`. All match `rwa_rows_usd` literally.

### FY2015 Pillar 3 (Wayback `ZBL_Pillar_3_Disclosure_Document_2015.pdf`, s.4.2/4.3)
Explicit column header **`US$000's`**:
`Share capital 136,702 / Profit and loss reserve 53,819 / Total tier 1 capital 190,521`
and `Credit Risk 68,766 / Market Risk 451 / Operational Risk 4,755 / Total 73,972 /
Regulatory Available Capital 188,483`.
188,483 == `CET1_TIER1_TOTAL_USD["FY2015"]`. 68,766/0.08 = 859,575 == the FY2015 Credit
Risk row; 451/0.08 = 5,638; 4,755/0.08 = 59,438; sum 924,650 == `RWA_USD["FY2015"]`.

### Contrast — the statement dicts really are raw USD
`bs_rows_usd` FY2024 Share Capital = **136,701,620**, i.e. the same capital expressed in
whole dollars. So `stock()`/`flow()`'s `/1000` is correct there and only there.

**Conclusion: diagnosis confirmed. The `/1000` in `stock()` must not be applied to the
Pillar 3 / RWA Breakdown dicts.**

## 2. CALL SITES CHANGED

New helper `stock_k()` added next to `stock()` (FX only, no `/1000`). Repointed:

| # | Sheet | Line (pre-edit) | Was | Now |
|---|---|---|---|---|
| 1 | CET1 Capital | 1309 | `stock(CET1_TIER1_TOTAL_USD)` | `stock_k(...)` |
| 2 | Tier 1 Capital | 1313 | `stock(CET1_TIER1_TOTAL_USD)` | `stock_k(...)` |
| 3 | Total Capital | 1317 | `stock(CET1_TIER1_TOTAL_USD)` | `stock_k(...)` |
| 4 | Total RWAs | 1321 | `stock(RWA_USD)` | `stock_k(...)` |
| 5 | RWA Breakdown | 1352 | `stock(v)` per row | `stock_k(v)` |
| 6 | Leverage Ratio | 1411 | `stock({exposure measure})` | `stock_k(...)` |
| 7 | LCR | 1435 | `stock({HQLA})` | `stock_k(...)` |
| 8 | LCR | 1436 | `stock({net cash outflows})` | `stock_k(...)` |
| 9 | NSFR | 1472 | `stock({ASF})` | `stock_k(...)` |
| 10 | NSFR | 1473 | `stock({RSF})` | `stock_k(...)` |
| 11 | FY2011 Basel II rows | 1275-1276 | `43.6` / `40.0` | `43631` / `40002` (true £'000 per HIST_P3_NOTE) |

NOT changed (verified, deliberately):
- `stock2`/`flow2`/`opening_cash2`/`eq_stock`/`eq_flow`/`eq_gbp` — statement sheets, raw USD
  or raw GBP. Correct as they stand.
- Asset Quality (`aq_rows_usd`, `stock()` at line 1182) — sourced from the Annual Reports,
  raw USD (FY2024 gross exposure 446,909,206). Correct as it stands.
- Overview sheet — passes only statement totals (raw USD) and ratio strings. It carries no
  Pillar 3 absolute amount at all, so it needed no rescaling. Verified by reading the
  `add_overview_sheet(...)` call and by re-reading the built sheet after the rebuild.
- All ratio series (`CAPITAL_RATIO`, leverage %, LCR %, NSFR %) — strings, scale-invariant.

## 3. CONSISTENCY / RATIO-REPRODUCTION RESULTS

Rebuilt with `python3 scripts/build_zenith.py`. **18 sheets**, correct order. All values
below are read back out of the rebuilt `.xlsx`, not recomputed from the script.

### 3a. CET1 vs Balance Sheet Total equity, and CET1 ratio reproduction

| Year | CET1 (£'000) | Total equity (£'000) | CET1/equity | Total RWAs (£'000) | CET1/RWA | printed CET1 ratio | reproduces |
|---|---|---|---|---|---|---|---|
| FY2025 | 320,773.3 | (no AR yet) | - | 1,370,696 | 23.40% | 23.40% | YES |
| FY2024 | 302,297.2 | 305,356.2 | 99.0% | 1,179,185 | 25.64% | 25.64% | YES |
| FY2023 | 265,540.4 | 263,918.8 | 100.6% | 917,285.6 | 28.95% | 28.95% | YES |
| FY2022 | 240,324.9 | 237,583.7 | 101.2% | 930,103.3 | 25.84% | 25.84% | YES |
| FY2021 | 207,889.9 | 202,894.4 | 102.5% | 1,000,519.9 | 20.78% | 20.78% | YES |
| FY2020 | 205,416.1 | 201,722.6 | 101.8% | 725,993 | 28.29% | 28.29% | YES |
| FY2015 | 127,190.1 | 128,565.1 | 98.9% | 623,962.5 | 20.38% | 20.38% | YES |
| FY2014 | 109,432.3 | 118,654.9 | 92.2% | 490,357.5 | 22.32% | 22.32% | YES |

CET1 is now 92%-103% of Total equity in every year — same order of magnitude, as it must be
for a bank whose entire capital base is CET1. Before the fix this column read 0.099%. The
few years above 100% are the Bank's own regulatory adjustments ADDING to book equity
(FY2020 is spelled out in its source: CET1 before adjustments 275,574 + adjustments 5,045 =
280,619); the 92% in FY2014 is the gap between the memo Tier 1 ($185,197k, which equals book
equity) and the Regulatory Available Capital actually used ($170,802k). Both pre-existing
and already documented in the script.

Total RWAs exceeds CET1 by the inverse of the CET1 ratio in every year by construction,
e.g. FY2024 1,179,185 / 302,297.2 = 3.90x = 1/0.2564.

### 3b. Every printed ratio still reproduces — old scale vs new scale

Computed both ways from the same dicts. Ratios are scale-invariant, so nothing could break,
and nothing did:

| Metric | Years | Max |new - old| | Still reproduces printed? |
|---|---|---|---|
| CET1 / Total RWAs -> CET1/Tier 1/Total Capital ratio | 8 | 0.009 pp | yes, all 8 |
| HQLA / net cash outflows -> LCR | 6 | 0.061 pp | yes (see caveat) |
| ASF / RSF -> NSFR | 4 | 0.007 pp | yes, all 4 |
| CET1 / leverage exposure | 6 | 0.002 pp | n/a, see caveat |

The sub-0.07pp movements are 1-decimal-place rounding only, and they move TOWARD the true
USD-basis ratio: the £ figures are now 1000x larger before being rounded to 1dp, so the
stored precision is strictly better than before.

RWA Breakdown components sum to that sheet's own Total, and to the Total RWAs sheet, in all
8 populated years (residuals <= 0.8 £'000, from per-row 1dp rounding, already documented in
the sheet's note).

Tier 1 Capital == CET1 Capital == Total Capital in every year (the Bank has no AT1/Tier 2) —
verified cell by cell after the fix.

### 3c. Two ratios that do NOT reproduce — both pre-existing, both unaffected by this fix
Stated explicitly so neither is mistaken for fix damage. Both were identical before the fix
(see 3b: scale-invariant).

1. **Leverage ratio.** CET1/exposure gives 12.66% for FY2024 against a printed 11.25% (same
   pattern every year). The script's existing note already explains it: the Bank uses its own
   tier-1-for-leverage measurement, and the printed figure is carried as disclosed. Nothing
   is derived. Untouched.
2. **LCR FY2022.** 1,014,739.2 / 309,847.1 = 327.50% against a printed 343%. This is a
   source-side inconsistency in FY2022's own report and reproduces identically in raw USD
   (1,227,530 / 374,822 = 327.5%). The script's LCR note already records the FY2022
   own-report vs FY2023-restated-comparative divergence. Untouched. FY2023 (310.47% vs a
   printed "310%"), FY2020 and FY2021 all reproduce to their printed precision.

### 3d. Overview sheet
The Overview carries **no Pillar 3 absolute amount at all** — only statement totals (raw USD,
via the untouched `stock()`/`flow()`) and ratio strings. So the scale fix required no
rescaling there, and Balance Sheet Total equity still reads 305,356.2 on both the Overview
and the Balance Sheet sheet.

One genuine internal contradiction WAS found and fixed while checking it: FY2020's capital
ratios (28.29%) and leverage ratio (10.68%) were on the detail sheets but missing from the
Overview — left behind by the earlier pass that recovered FY2020 from the FY2021 report's
comparative column. Added as a straight duplication of the detail-sheet cells; nothing
recomputed. Verified after rebuild: every populated Overview ratio cell now equals its
detail-sheet source exactly, across all six ratio rows.

**The LCR two-basis split was preserved.** FY2020 (435%) and FY2021 (276%) are point-in-time
and remain OFF the Overview's LCR trend row, which carries only the 12-month averages; the
Overview note was extended from FY2021-only to cover both years and to say why the FY2020
capital/leverage figures ARE shown while its LCR is not.

### 3e. Deliberately NOT changed
- FY2014/FY2015 Total RWAs derived as Pillar 1 requirement / 8% — still populated, still
  flagged in the script. Not withdrawn (user's call), not propagated.
- FY2011's "Solvency Ratio against Pillar 1 203%" — still off the ratio sheets; it is a
  capital-COVER multiple, not a CRR ratio.
- The LCR 12-month-average vs point-in-time row split — intact on the LCR sheet.
- Asset Quality's `stock()` call — correct as is, its dict is raw USD from the Annual Reports.
- No transcribed source literal was altered. The only numeric literals touched are the two
  FY2011 cells, restored FROM a deliberate stopgap TO the figures the source prints.

## 4. NOTE ON GIT STATE
This agent ran no git command that writes. Another process in this repo committed at
21:47 and 21:50 ("cleanup", 21e02b1 / 36917eb) while this work was in progress, sweeping the
`stock_k()` change, the FY2011 rescale and the rebuilt workbook into HEAD. `git diff` against
HEAD therefore shows only the later Overview edit; the full change is visible as
`git diff 21e02b1 -- scripts/build_zenith.py`. Everything described above is on disk and in
the rebuilt workbook.

## 5. NOT RUN, per instruction
`refresh_all.py` was NOT run and the test suite was NOT run, so `research/insights.db`,
`bank_metrics.csv` and the downstream deliverables still hold the OLD 1000x-understated
Zenith Pillar 3 figures. **A refresh is required before those outputs are trusted for
Zenith.** Nothing was committed by this agent and no other session was messaged.
