# RESUME — ICICI Bank UK Plc Pillar 3 history (started 2026-09-15)

Target script: `scripts/build_icici_bank_uk.py`
Workbook: `banks/ICICI BANK UK FINANCIALS.xlsx`
Year-end: **31 MARCH**. Reporting currency: **USD** (sole primary currency; only an
unaudited INR convenience translation alongside — no GBP anywhere).

## Starting state (before this session's edits)

- `YEARS` already spans FY2026..FY2008.
- `Y_CORE = FY2026..FY2014` — this is what the Pillar 3 metric sheets, Asset Quality,
  RWA Breakdown and Overview use. Statutory statements (BS/P&L/SOCIE/CF) already reach FY2008.
- `P3_URLS` had 12 entries (FY2026, FY2025, FY2024, FY2023, FY2022, FY2020..FY2014).
  **FY2021 had NO edition** — its figures came from the FY2022 edition's comparative column,
  which is why Leverage/LCR/NSFR were blank for FY2021.
- FY2013 and earlier: no Pillar 3 at all.

## Documents downloaded & verified (scratchpad `icici/`)

All `%PDF`, all text-native (`pdftotext -layout` clean, no OCR needed), all 10pp except FY2021 (59pp).
Cover dates read individually — **the filename trap is REAL and confirmed**:

| File | Cover says | => |
|---|---|---|
| `basel2_disclosures_FY2008.pdf` | "year ended 31 March 2008" | FY2008 |
| `Basel_II_p3_Disclosure_Statement.pdf` | "year ended 31 March 2009" | FY2009 |
| `basel2_disclosures_FY09_10.pdf` | "year ended 31 March 2010" | FY2010 |
| `basel2_disclosures_FY10_11.pdf` | "year ended 31 March 2011" | FY2011 |
| `basel2_disclosures_March31_11.pdf` | **"year ended March 31, 2012"** | **FY2012 — TRAP CONFIRMED** |
| `disclosures2012-13.pdf` | "year ended 31 March 2013" | FY2013 |
| `ICICI-Bank-UK-Plc-Pillar3-disclosures-FY2020-21.pdf` | 31 March 2021 | FY2021 |

Entity check: every one of these opens "ICICI Bank UK PLC ('the Bank') ... a wholly owned
subsidiary of ICICI Bank Limited", and states "The disclosures have been prepared for ICICI
Bank UK PLC", explicitly distinguishing itself from "the consolidated Basel II – Pillar 3
Disclosures made by ICICI Bank Limited ('the Parent Bank')". **No parent-entity contamination.**

## KEY FINDING — FY2008–FY2013 Basel II docs contain NO Pillar 3 key metrics

Grepped every one of the six for tier/capital resource/capital ratio/own funds/RWA/risk
weighted/leverage/LCR/NSFR. The only capital content in any of them is:

> "The following table shows the Bank's Pillar 1 capital requirement by each of the
> standardised credit risk exposure classes" — a credit-risk-only table, USD million.

Totals (credit risk Pillar 1 **capital requirement**, NOT RWA, NOT total):
FY2008 335.02 | FY2009 426.62 | FY2010 459.49 | FY2011 402.24 | FY2012 260.31 | FY2013 241.69

There is **no** Tier 1, Tier 2, total capital, capital ratio, total RWA, operational-risk or
market-risk capital requirement, leverage, LCR or NSFR figure anywhere in these six documents.
=> None of the 11 Pillar 3 metric sheets can be filled for FY2008–FY2013 from Pillar 3.
=> Do NOT derive RWA from 335.02/8% etc. — the op-risk and market-risk components are absent,
   so such a figure would not even be a complete credit-risk RWA let alone a total.

## KEY FINDING 2 — three genuine definitional breaks, each confirmed by the Bank's own words

### (a) Leverage: CRR full exposure (to FY2021) vs UK KM1 excl. central banks (FY2022+)

FY2017–FY2021 editions carry the **CRR LRSum/LRCom** template, whose line 8/21 is
"Total leverage ratio exposure" — the FULL measure, with **no** central-bank exclusion:

| | exposure | ratio |
|---|---|---|
| FY2021 | 3,153.7 | 15.7% |
| FY2020 | 3,747.3 | 11.8% |
| FY2019 | 4,153.1 | 10.7% |
| FY2018 | 4,180.3 | 11.7% |
| FY2017 | 3,731.1 | 13.97% |

FY2022+ KM1 rows 13/14 are captioned "**excluding** claims on central banks"
(FY2022 2,085.6 / 14.05% … FY2026 2,845.7 / 11.54%) and leave the FY2021 comparative BLANK.
The FY2022 edition's own note h says why, verbatim:
> "At March 31, 2021, the Bank's leverage ratio was 15.66% **in accordance with the regulation
> applicable as at that date**."

The workbook previously had FY2017–FY2020 sitting on the row captioned "excluding claims on
central banks". **That caption was wrong for those years** — they are the full CRR measure.

### (b) LCR: 12-month average (KM1) vs point-in-time (narrative), BOTH printed every year

KM1 row 17 note: "computed using the liquidity balances which are calculated as the simple
averages of month end observations over the 12 months preceding the end of the year."
Each edition ALSO prints "The LCR of the Bank as at March 31, XXXX was …". They differ
materially — FY2022: 226.90% (avg) vs 245.23% (spot).

- KM1 12-month average: FY2022 226.90 | FY2023 226.83 | FY2024 240.20 | FY2025 190.08 | FY2026 169.42
- Point-in-time at 31 March: FY2018 203.9 | FY2019 225.0 | FY2020 183.3 | FY2021 329.5 |
  FY2022 245.23 | FY2023 346.1 | FY2024 221.17 | FY2025 216.84 | FY2026 171.83

FY2018–FY2021 have ONLY the point-in-time figure (no KM1 existed yet). The workbook previously
merged FY2018–FY2020 point-in-time onto the same row as FY2022+ averages.

### (c) NSFR: FY2022's KM1 figure is NOT an average

FY2022 note g, verbatim: "The NSFR ratio in the above table is **computed as at March 31, 2022**."
FY2023 note h, verbatim: "the average for the previous year (FY 2022) **was not computed**."
So 141.69% is point-in-time; FY2023+ KM1 is "the simple averages of four data sets covering the
latest and the three previous quarters".

- KM1 4-quarter average: FY2023 147.72 | FY2024 159.20 | FY2025 151.03 | FY2026 136.53
- Point-in-time at 31 March: FY2022 141.69 | FY2023 169.72 | FY2024 152.71 | FY2025 147.50 | FY2026 132.18

Pre-FY2022 the Bank's own editions say NSFR "is yet to be introduced as a regulatory requirement
in the UK" => **Not applicable**, not blank.

## KEY FINDING 3 — FY2021 own edition validates every figure already in the workbook

FY2021 Annexure I rows 59/60/61/62/63 + LRCom row 20 give CET1 493.9, Tier 1 493.9, Total
capital 586.7, Total RWA 2,075.1, CET1/Tier1 23.80%, Total capital 28.27% — identical to what
the workbook already carried from the FY2022 comparative. FY2020 comparatives in the same
document (440.9 / 547.2 / 2,941.4 / 14.99% / 18.60%) also tie exactly. **No restatement.**

## FLAG FOR THE USER (not actioned — mirrors the Cater Allen escalation)

`Total RWAs` FY2014/FY2015/FY2016 (3,737.5 / 3,685.0 / 4,093.8) are **derived**, and the sheet
note misdescribes the method as "implied from Total capital / Total capital ratio" — the
forbidden back-solve. The figures are in fact the printed "Total Capital Resource requirement
under Pillar 1" (FY2014 299.0, FY2015 294.8, FY2016 327.5) divided by 8%, which is what the RWA
Breakdown sheet's own note already says. The note text is corrected in this session; **the
derived values themselves are left in place** — withdrawing populated data is the user's call.

## Progress log

- [x] Downloaded + cover-verified all 7 new documents (+ FY2014-FY2026 for basis checking)
- [x] FY2008–FY2013 Basel II content assessed — see KEY FINDING above
- [x] FY2021 own edition — KM1/CRR figures extracted and validated
- [x] Basis breaks (a)(b)(c) established with verbatim source wording
- [x] Edit script, rebuild, confirm 18 sheets — **DONE, workbook rebuilt, 18 sheets**

## What was written (all in `scripts/build_icici_bank_uk.py`)

1. `P3_URLS` gains **FY2021** (its own edition, previously absent).
2. New `P3_BASEL2_URLS` + `BASEL2_CREDIT_RISK_PILLAR1_REQUIREMENT` + `BASEL2_NOTE`
   documenting all six Basel II editions, their URLs, their cover-verified dates, the
   filename trap, the entity check, and exactly what they do/don't contain.
3. `p3_sources()` rewritten: every year FY2008–FY2026 now cites its own edition; the
   FY2008–FY2013 lines say "published and read, discloses no key metric" instead of the old
   "out of scope … left blank"; a FY2021 source-upgrade + validation paragraph added.
4. **Leverage Ratio**: 2 rows → 4 rows, split by basis. FY2021 newly filled (3,153.7 / 15.7%).
   FY2017–FY2020 moved off the wrongly-captioned "excluding central banks" rows.
5. **LCR**: 1 row → 2 rows. New point-in-time row carries 9 years FY2018–FY2026; FY2018–FY2020
   moved there off the average row; FY2021 newly filled; FY2022–FY2026 spot figures all new.
6. **NSFR**: 1 row → 2 rows + explicit "Not applicable" for FY2014–FY2021 and "Not computed -
   first year of the requirement" for FY2022 on the average row. FY2023–FY2026 spot figures new.
7. **Total RWAs**: note corrected — the FY2014–FY2016 method is printed-total-Pillar-1-
   requirement ÷ 8%, NOT capital ÷ ratio as the old note claimed. Values untouched.
8. **Overview** ratio block updated to match (it is a copy, so it was edited separately).

## Cells filled (net new, all sheets)

| year | new cells |
|---|---|
| FY2026 | 2 (LCR spot 171.83%, NSFR spot 132.18%) |
| FY2025 | 2 (LCR spot 216.84%, NSFR spot 147.50%) |
| FY2024 | 2 (LCR spot 221.17%, NSFR spot 152.71%) |
| FY2023 | 2 (LCR spot 346.1%, NSFR spot 169.72%) |
| FY2022 | 1 (LCR spot 245.23%) + 1 explicit "Not computed" marker |
| FY2021 | 3 (leverage exposure 3,153.7, leverage ratio 15.7%, LCR spot 329.5%) |
| FY2014–FY2021 | 16 explicit "Not applicable" NSFR markers (2 rows × 8 years) |
| FY2008–FY2013 | 0 — none exist; see KEY FINDING 1 |

## Deliberately NOT written

- No Pillar 3 key metric for FY2008–FY2013. The documents contain none.
- No RWA derived from the Basel II credit-risk-only capital requirement ÷ 8% — the op-risk
  and market-risk components are absent from those documents, so it would understate RWA.
- `Y_CORE` left at FY2014 (Pillar 3 sheets still span FY2026–FY2014). Extending it to FY2008
  would add six wholly-blank columns to Asset Quality, RWA Breakdown and Overview for no data.
  The absence is recorded in `BASEL2_NOTE` on every Pillar 3 sheet's source cell instead.
- The derived FY2014–FY2016 Total RWA values are left in place (note corrected only) — see FLAG.
- No commit, no `refresh_all.py`, no test suite, per brief.
