# RESUME — historical Pillar 3 batch (4 banks), started 2026-09-15

Task: transcribe Wayback-recovered historical Pillar 3 editions into four build
scripts. Checkpoint file — update after each bank.

Banks in scope:
1. National Bank of Egypt (UK) — `scripts/build_national_bank_of_egypt_uk.py` — **STATUS: DONE, rebuilt, 18 sheets**
2. Aldermore — `scripts/build_aldermore.py` — STATUS: in progress
3. Bank of Ceylon (UK) — `scripts/build_bank_of_ceylon_uk.py` — STATUS: not started
4. Persia International Bank — `scripts/build_persia_international_bank.py` — STATUS: not started

## 1. National Bank of Egypt (UK) — DONE

YEARS extended from 6 to 12 columns: added FY2015, FY2014, FY2013, FY2012,
FY2010, FY2009 (all 30 JUNE year-ends).

Three editions recovered (2010, 2013, 2015); each carries a prior-year
comparative column, so six years of data came out of three documents.

Figures transcribed (£000):

| | FY2015 | FY2014 | FY2013 | FY2012 | FY2010 | FY2009 |
|---|---|---|---|---|---|---|
| Tier 1 (= CET1 row) | 134,291 | 134,291 | 130,000 | 130,000 | 123,922 | 118,891 |
| Total capital | 153,368 | 151,829 | 149,733 | 150,469 | 127,422 | 122,391 |
| Printed "RWA" | 469,969 | 487,653 | 324,189 | 275,431 | 480,466 | 562,792 |
| Capital adequacy ratio | 32.63% | 31.13% | 46.19% | 54.63% | 26.52% | 21.75% |
| Leverage | 12.86% | 9.17% | — | — | — | — |
| One-month LCR (observation) | 314% | — | 422% | — | — | — |
| NSFR (observation) | 81% | — | 97% | — | — | — |
| Total Pillar 1 capital req. | 40,051 | 41,497 | 28,474 | 24,870 | 42,050 | 47,903 |

Key findings recorded in the script:
- "SOLVENCY RATIO" = capital-cover ratio (proved on 4 columns). Used nowhere.
- "CAPITAL ADEQUACY RATIO" in these older editions IS total capital / RWA
  (reproduces exactly on all 6 columns) — unlike FY2017's "TOTAL CAPITAL RATIO",
  which is capital / total exposures. Placed on Total Capital Ratio sheet.
- "TIER 1 CAPITAL RATIO ( LEVERAGE )" = leverage ratio (FY2015 reproduces).
  FY2014's printed 9.17% does NOT reproduce (9.47% expected) — transcribed as
  printed, divergence documented, not recalculated.
- **Printed "Risk Weighted Assets" is credit-risk RWA only in all six columns**
  (= credit risk capital × 12.5 to the rounding). The printed ratio reproduces
  against it, so the usual diagnostic can't replace it and no document states a
  true total — transcribed as-is and flagged on Total RWAs + RWA Breakdown.
- CET1 Ratio / Tier 1 Ratio left blank for all six years — never printed, not
  back-solved.
- NSFR CRR row marked "Not applicable" for all six (pre-2022 structural);
  observation-period values on a separate labelled row.
- FY2016: capture is a 404 → published, capture broken.
- FY2011/FY2012/FY2014: published-but-lost (FY2014 accounts confirm publication;
  FY2013 edition states annual publication policy). FY2012/FY2014 data recovered
  anyway via comparatives; FY2011 stays blank.
- OCR misreads caught by visual check: market risk capital "A 9" → 41 / 9;
  Core Funding Ratio "WM%" → 31%.
- Did NOT touch the §8b FY2017 £'000-vs-£ Balance Sheet defect (out of scope).

## Progress log

- NBE: complete, `python3 scripts/build_national_bank_of_egypt_uk.py` → 18 sheets.

## 2. Aldermore — DONE

**ENTITY FINDING (the check the task asked for): NO basis break.** Both recovered
editions are **Aldermore Bank PLC** (Companies House 00947662, FRN 204503 — named
and registered on every page footer of both PDFs). That is exactly the entity this
workbook is built on ("Bank solo, not the Aldermore Group PLC holding company").
Aldermore Group PLC did not exist as a Pillar 3 reporting entity in 2011/2013.
From FY2014 onward the workbook already takes Bank-solo *columns* out of
Group-level Pillar 3 reports — so the change across the series is in the reporting
**vehicle**, not the reporting **entity**, and the figures are Bank-solo
throughout. Recorded on the sheets; no separate basis-labelled series needed.

`P3_DISCLOSURE_YEARS` extended by FY2013, FY2012, FY2011 (metric sheets + RWA
Breakdown only — `PILLAR3_YEARS` untouched so Asset Quality does not gain blank
columns).

Filled (£m):
- CET1 Capital: FY2013 250.4, FY2011 158.2
- Tier 1 Capital: FY2013 250.4, FY2011 158.2 (identical — no AT1 in either year,
  each document states Tier 1 = ordinary shares + audited reserves, no Tier 3)
- Total Capital: FY2011 159.6 (printed "Total capital less deductions" £159,602k)
- RWA Breakdown, new labelled CAPITAL block: credit-risk Pillar 1 capital
  FY2013 165.0 / FY2011 68.1; operational risk 6.5 / 1.9; memo exposure value
  4,746.6 / 1,647.4
- Leverage / LCR / NSFR: "n/a" for FY2013, FY2012, FY2011 (structural — none
  existed as a UK measure at those dates)

**Deliberately NOT written:**
- Total Capital FY2013. The edition states £250.4m Tier 1 and £39.3m Tier 2 but
  never prints a total, and does not say whether either is pre- or post-deduction
  (the 2011 edition shows £167.5m before vs £159.6m after). Publishing £289.7m
  would present a derived figure as a disclosed one. Components recorded in the note.
- Total RWAs / CET1 Ratio / Tier 1 Ratio / Total Capital Ratio for FY2013 and
  FY2011. **Neither edition discloses any RWA or any capital ratio** — they
  publish the Pillar 1 CAPITAL requirement (8% × risk weight) instead. Not
  grossed up by 12.5.
- FY2012: no edition in the archive, and neither adjacent edition carries a
  comparative column (both are single-period documents). Blank column kept
  visible on purpose.

**VALIDATION GATE PASSED:** FY2011's Total Core Tier 1 of £166,143k reproduces
exactly the £166.1m Total equity already in the workbook's FY2011 Balance Sheet.
FY2013's £250.4m sits £7.0m below FY2013 statutory equity of £257.4m — same shape
as FY2011's £7.9m intangibles deduction — and below FY2014's existing £280.7m CET1.

Pre-existing defect noticed, NOT fixed (out of scope): the RWA Breakdown sheet's
column headers read "(£'000)" while the sheet's data and subtitle are £m.

Rebuilt: 19 sheets (18 standard + this bank's extra "Interim Pillar 3").

## 3. Bank of Ceylon (UK) — DONE

Added a single **non-contiguous FY2013 column** (YEARS: FY2025…FY2018, FY2013),
labelled "FY2013 (Pillar 3 only - 4-year gap, see notes)". FY2017–FY2014 omitted
rather than added blank — the Wayback CDX sweep of the whole domain lists Pillar 3
captures for 2013, 2018–2021, 2024, 2025 only. Entity confirmed: Company
Registration no. 06736473 on the 2013 cover — same entity as every other column.

Filled (£'000, all from the 31 Dec 2013 edition, genuine text layer, no OCR):
- CET1 Capital / Tier 1 Capital: 13,436 (Core Tier 1: 15,000 share capital + 31
  fair value reserve − 1,073 cumulative revenue losses = 13,958, less 522 intangibles)
- Total Capital: 13,899 (printed "Total Regulatory Capital")
- Leverage Ratio sheet, Tier 1 capital row: 13,436
- RWA Breakdown, two new labelled CAPITAL blocks: Pillar 1 by risk type
  (credit 2,454 / market 24 / operational 292 / total 2,770) and credit risk by
  exposure class (0 / 1,620 / 156 / 231 / 227 / 220 = 2,454), plus memo gross
  credit risk exposure 63,175.

**Deliberately NOT written:** Total RWAs, CET1/Tier 1/Total Capital Ratio,
leverage exposure + ratio, LCR, NSFR, MREL for FY2013. The edition discloses **no
RWA and no capital ratio at all** — only the Pillar 1 capital requirement, which
its own text defines as "8% of the risk weighted exposure amounts". 2,770 / 8% =
~34,625 would be back-solving, and this is exactly the bank where a printed
"Total RWAs" has already proved to be a credit-risk subtotal three times.
Leverage/LCR/NSFR are structurally absent at 31 Dec 2013.

**Substantive finding recorded on the Total Capital sheet:** that sheet said the
Bank began recognising its revaluation reserve as Tier 2 capital "from FY2020 on".
The FY2013 edition shows it was already doing so in 2013 (Tier 2 Capital:
Revaluation reserve 463). The real anomaly is FY2018/FY2019, the two years with no
Tier 2 at all. Existing wording left in place but annotated.

**FY2022/FY2023 closure:** already fully documented in the script (sourced
negative with positive + negative controls, byte-identical 404s, md5 recorded).
Nothing added.

**Nothing undone:** FY2021 RWA 29,052, FY2019 28,513, FY2018 24,492 (left
defective on purpose), and the three labelled FY2022 CET1 rows
(13,959 / 13,734 / 12,852) all verified intact after rebuild.

Rebuilt: 18 sheets.
