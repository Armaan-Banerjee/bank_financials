# FX scale/unit sweep — corpus-wide audit

Started 2026-09-16. Hunting the defect class confirmed three times:

1. **Zenith** (fixed, `research/RESUME_zenith_scale.md`) — one `stock()` helper
   served two source families holding different units (raw USD vs US$'000);
   `/1000` was correct for one and understated the other 1000x.
2. **Gulf International Bank (UK)** (found, not fixed,
   `research/RESUME_gib_fy2020_recovery.md` closing section) — `stock()`/`flow()`
   divide $'000 by the FX rate and then by 1000, so every figure is in
   £ millions while the sheet label says `£'000`.
3. **National Bank of Egypt (UK)** — FY2017 Balance Sheet in `£'000` on a sheet
   labelled `£`.

A uniform scale error is invisible to every check this project runs: ratios
reproduce, totals foot, cross-checks pass. Only an absolute figure compared
against an independent anchor reveals it.

## PHASE 1 — candidate list (COMPLETE)

### Method

Three independent sweeps over all **145** `scripts/build_*.py`, `ast`-based, not
regex over raw text (comments and citation prose mention "exchange rate" in 64
of 145 scripts — almost all of those are the cash-flow line item "Effect of
exchange rate changes on cash", not a conversion):

- **Sweep 1** — `ast` walk for `FunctionDef`s containing a `Div`/`Mult` `BinOp`
  whose name or body implies FX, plus module-level `Dict` assignments whose
  name carries a currency token.
- **Sweep 2** — module-level `float` constants and all-`float` dicts in the
  plausible FX range 0.2–5.0, cross-referenced against every `BinOp` that uses
  them as an operand (catches rate tables regardless of helper naming).
- **Sweep 3** — every *other* script (the 126 not already flagged) scanned for a
  `Div`/`Mult` by a bare float literal in 0.3–6.0. **Zero hits.** No script
  converts currency with an unnamed inline rate.

Sweep 2 missed `build_arab_bank_europe.py` (its rate table `FX_RATES` is a dict
*of dicts*, so the all-float test failed); sweep 1 caught it. Sweep 1 missed
`build_firstbank_uk.py` (scalar `FX_SPOT_2020`-style constants, no helper
function); sweep 2 caught it. The union is the candidate list.

### Candidate list — 19 scripts convert currency

| # | Script | Src ccy | Rate table | Helpers | Status |
|---|---|---|---|---|---|
| 1 | `build_access_bank.py` | USD | `FX_SPOT`/`FX_AVG` | `cf_flow`,`cf_stock`,`cf_opening`,`bs_stock`,`bs_flow`,`_convert_equity_row` | clean |
| 2 | `build_arab_bank_europe.py` | EUR | `FX_RATES` (nested) | `eq_gbp_spot`,`eq_gbp_spot_prior`,`eq_gbp_avg` | clean |
| 3 | `build_bank_mandiri_europe.py` | USD | `FX_SPOT`/`FX_AVG` | `stock`,`flow` | clean |
| 4 | `build_bank_saderat.py` | EUR | (in `_to_gbp_m`) | `gbp_m_spot`,`gbp_m_spot_prior`,`gbp_m_avg`,`_to_gbp_m` | clean |
| 5 | `build_bank_sepah_international.py` | EUR | `YEAR_END_RATE`/`AVG_RATE` | `_to_gbp` | clean |
| 6 | `build_bpi_europe.py` | USD | `FX_SPOT` | `stock` | **DEFECT — fixed** |
| 7 | `build_credit_suisse_international.py` | USD | `FX_SPOT`/`FX_AVG` | (inline) | clean |
| 8 | `build_fcmb_uk.py` | USD | `FX_SPOT`/`FX_AVG` | `flow`,`stock`,`opening_cash` | clean |
| 9 | `build_fidbank_uk.py` | USD | `FX_SPOT`/`FX_AVG` | (inline) | clean |
| 10 | `build_firstbank_uk.py` | USD | scalar `FX_SPOT_20xx` | (inline) | clean |
| 11 | `build_goldman_sachs_international_bank.py` | USD | `FX_SPOT`/`FX_AVG` | (inline) | clean |
| 12 | `build_gulf_international_bank_uk.py` | USD | `FX_SPOT`/`FX_AVG` | `flow`,`stock`,`opening_cash` | **DEFECT (2) — fixed** |
| 13 | `build_jp_morgan_securities.py` | USD | `FX_SPOT` | (inline) | **LOCKED** — leverage-basis sweep |
| 14 | `build_persia_international_bank.py` | EUR | `AVG_RATE`/`YEAR_END_RATE` | `stock`,`flow`,`stock_v`,`flow_v` | **DEFECT — fixed** |
| 15 | `build_punjab_national_bank_international.py` | USD | `FX_SPOT`/`FX_AVG` | (inline) | clean |
| 16 | `build_smbc.py` | JPY | `FX_RATES` | (inline) | clean |
| 17 | `build_uba_uk.py` | USD | `FX_SPOT`/`FX_AVG` | (inline) | clean |
| 18 | `build_ubi_uk.py` | USD | `FX_SPOT`/`FX_AVG` | (inline) | clean |
| 19 | `build_zenith.py` | USD | `FX_SPOT`/`FX_AVG` | `stock`,`stock_k`,`flow`,… | **FIXED 2026-09-15** |

### Locked — report but do not edit

`build_jp_morgan_securities.py` (leverage-basis sweep candidate list). No other
locked script (`build_icici_bank_uk.py`, `build_hodge.py`/`build_julian_hodge_bank.py`,
`build_arbuthnot_latham.py`, `build_starling.py`, the nine in
`research/RESUME_posthoc_columns.md`, the twenty in `research/RESUME_leverage_basis_sweep.md`)
converts currency, so no other collision exists.

## PHASE 2 — verification (COMPLETE)

### Method

Three checks per candidate, run against the BUILT workbooks on disk (openpyxl),
not against the scripts — the scripts are what produce the error, so reading the
output is the only way to see it:

1. **Unit consistency** — source-dict unit vs helper output vs sheet label.
2. **One helper, two source families** (the Zenith shape) — detected by footing
   the `RWA Breakdown` sheet against the `Total RWAs` sheet, and by comparing
   LCR/NSFR component amounts against total assets. A helper that is right for
   one caller and wrong for another shows up as a clean 1000x (or FX-rate)
   discrepancy between two sheets that must agree.
3. **Absolute sanity check** — CET1 vs Balance Sheet total equity, Total RWAs vs
   total assets, leverage exposure vs total assets, **each normalised by the
   unit its own sheet declares** (this corpus legitimately mixes `£`, `£'000`
   and `£m` across sheets of one workbook, so a raw ratio is meaningless).

### Results — all 19, unit-normalised

| Bank | FY | CET1/equity | RWA/assets | LevExp/assets | units P3 / BS | verdict |
|---|---|---|---|---|---|---|
| Access Bank UK | FY2024 | 95.7% | 68.4% | 96.0% | k / k | clean |
| Arab Bank Europe | FY2022 | 85.5% | 75.4% | - | k / k | clean |
| Bank Mandiri Europe | FY2021 | 100.0% | RWA n/d | - | k / k | clean |
| Bank Saderat | FY2025 | 100.0% | 100.2% | - | m / m | clean |
| Bank Sepah International | FY2025 | 100.1% | 53.0% | - | m / k | clean |
| BPI Europe | FY2025 | 100.0% | 71.3% | - | k / unit | **DEFECT — fixed** |
| Credit Suisse International | FY2025 | 100.0% | 36.3% | - | m / m | clean |
| FCMB UK | FY2025 | 98.1% | 60.7% | - | k / k | clean |
| Fidbank UK | FY2025 | 98.9% | 49.0% | - | k / k | clean |
| FirstBank UK | FY2025 | 97.7% | 60.9% | - | $k / $k | clean (unconverted USD) |
| Goldman Sachs Int'l Bank | FY2025 | 97.4% | 18.1% | 53.5% | m / m | clean |
| **Gulf International Bank UK** | FY2024 | 94.7% | 13.5% | 59.9% | m / m | **DEFECT — fixed** |
| JP Morgan Securities | FY2025 | 75.2%* | 27.4%* | 91.3%* | £k / US$k | clean — **LOCKED**, see below |
| **Persia International Bank** | FY2025 | 100.0% | 145.9% | - | k / k | **DEFECT (rate direction) — fixed** |
| Punjab National Bank Int'l | FY2026 | 66.0% | 60.4% | - | m / k | clean (see note) |
| SMBC | FY2026 | 97.1% | 37.7% | 94.9% | m / m | clean |
| UBA UK | FY2024 | 98.6% | 33.9% | 103.0% | k / k | clean |
| Union Bank of India UK | FY2025 | 99.9% | 85.2% | 103.3% | k / k | clean |
| Zenith | FY2024 | 99.0% | 55.7% | 112.8% | k / k | clean (fixed 2026-09-15) |

\* JPMS's Pillar 3 sheets are £'000 and its statements are US$'000 — both
labelled. The table shows the ratios after converting at the workbook's own
FY2025 spot 1.3448; the raw cross-currency figures are 55.9% / 20.4% / 67.8%.

`RWA Breakdown` total vs `Total RWAs` footed to **1.0000** on all 17 banks that
have both populated. The single exception is JPMS at exactly **1.3448** and
**1.2515** for FY2025/FY2024 — which are precisely that workbook's own FX_SPOT
rates, because its RWA Breakdown is deliberately left in US$'000 while Total
RWAs is converted to £'000. Both sheets say so. Reported, not touched (locked).

Sub-threshold observations, recorded, not defects:
- **PNBIL** CET1 is 66% of book equity. Not a scale error (a scale error is
  1000x, not 1.5x); consistent across all years and explained by CRR deductions.
- **Bank Saderat** RWA is 100.2% of total assets and **Persia** 145.9%. Both are
  currency- and scale-invariant, so neither can be an FX artefact; both are
  sanctioned banks in run-off with large off-balance-sheet exposures, and both
  figures are printed in the source.

## PHASE 3 — fixes

### 1. Gulf International Bank (UK) — `£'000` label on £m figures — FIXED

`stock()`/`flow()`/`opening_cash()` divide US$'000 by the FX rate **and** by
1000, so their output is £ MILLIONS. Every sheet said `£'000`.

Which was wrong — the labels, established before changing anything:
- The figures are right. FY2020 CET1 $378,549k / 1.3661 / 1000 = 277.1, and the
  sheet shows 277.1. The source prints $'000; the helper's output is £m.
- Total assets FY2024 reads 11,585.2. As £'000 that is an £11.6m bank; GIB UK is
  an £11.6bn one. As £m it is right.
- Six converted workbooks already use `£m`, including all three of GIB's
  size peers (Goldman Sachs International Bank, Credit Suisse International,
  SMBC). House style copied from `build_goldman_sachs_international_bank.py`.

This was not cosmetic: `scripts/insights/extract_metrics.py` parses the unit
label and `in040_risk_metrics.py` / `in041_spend_metrics.py` /
`build_deliverable.py` multiply by it, so GIB UK was entering every cross-bank
absolute comparison 1000x too small.

Rebuilt: **18 sheets**, **0 numeric cells changed**, 51 label/prose cells
changed. Before -> after, FY2024: CET1 348.0 `£'000` -> 348.0 `£m`; Total RWAs
1,569.1 -> `£m`; leverage exposure 6,937.5 -> `£m`; Balance Sheet total equity
367.4 and total assets 11,585.2 -> `£m`. Every ratio is carried as a disclosed
string and no numeric cell moved, so nothing could fail to reproduce.

### 2. BPI Europe — Overview labelled `£'000-equivalent` over whole-pound figures — FIXED

Found by comparing each Overview block's declared unit against the detail sheet
it copies. The `Balance Sheet`, `Profit & Loss` and `Statement of Changes in
Equity` sheets say `£-equivalent, whole pounds`; the Overview copied their cells
verbatim but declared `£'000-equivalent`. Total assets 211,103,396 is £211.1m,
not £211.1bn; profit for the year 693,543 is £0.69m for a bank with £211m of
assets.

Only the Overview was wrong — the detail sheets, the Pillar 3 sheets (genuinely
`£'000`) and the RWA Breakdown were all correct and were left alone. This
workbook really does mix two scales, so each label has to be right separately.

Rebuilt: **18 sheets**, **0 numeric cells changed**, 4 label cells changed.

### 3. Persia International Bank — inverted FX rate direction — FIXED

Not the 1000x class; found by the same sweep. `stock()`, `flow()`, `stock_v()`,
`flow_v()` and the FY2021 RWA literal all **divided** by the rate, on the
strength of a code comment reading *"Rates are EUR per GBP, so EUR / rate =
GBP."* The rates are GBP per EUR. Every converted figure was overstated by
1/rate^2 — about **1.43x**.

Proven twice before changing anything:
1. **The Bank's own accounting policy.** FY2025 Annual Report Note 2.1 (p.40 of
   the Companies House PDF, image-only, rendered at 200dpi and OCR'd): *"The
   euro is both the functional and presentation currency ... Amounts are rounded
   to the nearest thousand euros ... The average exchange rate for EUR/GBP
   applied during the year was 0.8390 (2023/24: 0.8630). The year-end exchange
   rate used was 0.8350 (2023/24: 0.8550)."* Those are `AVG_RATE`/
   `YEAR_END_RATE` FY2025 and FY2024 exactly. At 31 Mar 2025 EUR1 bought
   GBP0.8358 and GBP1 bought EUR1.1965, so 0.8350 can only be pounds per euro.
   No rate in either table exceeds 1.0, and EUR-per-GBP was never below 1.0 in
   the FY2015-FY2025 window (the FY2016 rate 0.7390 fixes the direction again at
   a very different point in the cycle).
2. **An in-corpus twin.** `build_bank_sepah_international.py` — Iranian-owned UK
   bank, EUR presentation, 31 March year-end — discloses near-identical rates
   (FY2025 0.8354/0.8418, FY2024 0.8548/0.8636, FY2021 0.8520 against Persia's
   0.8350/0.8390, 0.8550/0.8630, 0.8525), documents them as *"i.e. GBP per
   EUR 1"*, and **multiplies**. The two cannot both be right.

No prior deliberation exists on this direction (no research note, nothing in the
git history) — it is a plain mistake, not a considered choice.

Rebuilt: **18 sheets**. Verification:
- **0 percentage cells moved.** A ratio converts numerator and denominator by
  the same factor, so this change is ratio-invariant, and it is.
- 793 numeric cells changed. **784 moved by exactly the square of that year's
  own disclosed rate** (0.8350^2 = 0.697225, 0.8390^2 = 0.703921, 0.7390^2 =
  0.546121, and so on across all 18 distinct rate^2 values).
- The 9 exceptions are all the `Effect of GBP/EUR translation` row — the
  programmatic residual between average-rate flows and year-end-rate balances.
  It is not a source figure and does not scale linearly; inverting the rates
  flips its sign, which is what it did. The cash flow still reconciles
  **exactly** (opening + net change + both FX lines - closing = 0.00 in all 9
  populated years, identical to before the fix).
- FY2015/FY2016 stocks still pass through unconverted in EUR, as documented.

Before -> after (FY2025, FY2024, FY2023, FY2022), £'000:
| Row | was | now |
|---|---|---|
| Total assets | 186,378.4 / 208,526.3 / 237,279.5 / 247,655.5 | 129,947.7 / 152,437.9 / 183,749.3 / 177,880.1 |
| Total equity | 132,244.3 / 149,348.5 / 150,637.5 / 155,466.7 | 92,204.0 / 109,177.5 / 116,653.7 / 111,664.9 |
| CET1 capital | 132,244.3 / 149,348.5 / 150,637.5 / 155,466.7 | 92,204.0 / 109,177.5 / 116,653.7 / 111,664.9 |

Ties back to source: `CAPITAL_EUR["FY2025"]` = EUR110,424k x 0.8350 = £92,204.0.

## PHASE 4 — corpus-wide negative controls

The 19-bank sweep only covers FX converters. Two cheaper checks were then run
across **all 145** workbooks, because the defect class is "declared unit
disagrees with content" and that is not exclusive to FX banks (National Bank of
Egypt UK, instance 3, converts nothing).

**(a) Overview-block unit vs the detail sheet it copies** — 562 block/detail
pairs compared. **1 flagged, 1 false positive** (Shawbrook: both sheets are £m;
the detail subtitle mentions "£000" in incidental later prose about rounding).
BPI Europe was the one genuine hit and is fixed above.

**(b) Total assets, normalised to absolute £ by each sheet's declared unit,
against a plausibility band** — all **145** workbooks resolved. Only 2 fall
below £20m: Philippine National Bank Europe (£14.0m) and Afin Bank (£17.4m).
Both verified genuine — tiny run-off / newly-authorised entities whose CET1
ties to book equity at 100.0% and 84.1%. United National initially flagged at
£1.92tn and is a false positive: its subtitle reads *"Company basis, exact £
(not £'000/£m)"*, so the detector saw the `£'000` inside the denial; it is a
£1.92bn bank. No workbook is implausibly large.

**(c) CET1 vs book equity, unit-normalised, across all 145** — 126 comparable,
**126 in band (35-200%), 0 out of band**. Note this check cannot catch the GIB
shape: when a whole workbook is uniformly mislabelled the factor cancels out of
both sides. That is what check (b) is for, and why the two must be run together.

## Conclusion

**19 of 145 scripts convert currency. 16 clean, 3 defective, 0 unverifiable.**
Every candidate was verifiable — every one has both a Balance Sheet and Pillar 3
capital sheets populated in at least one common year.

The defect is **incidental, not systematic**. The three found here have three
different mechanisms (a mislabelled scale on every sheet; a mislabelled scale on
the Overview only; an inverted rate direction), and the two already known have
two more (one helper serving two unit families; one year's row at the wrong
scale). No shared helper, no copied idiom and no template propagates it — each
build script is hand-written, and each defect is a separate hand-made slip. What
they share is only the reason they survive: a uniform factor cancels out of
every ratio, every subtotal and every cross-check this project runs, so nothing
short of comparing an absolute figure against an outside anchor will show it.

The lasting fix is not more scripts but a habit: **every sheet's unit label is a
load-bearing assertion**, consumed by `scripts/insights/` and scaled on, so it
has to be verified against the figures, not just written.

## NOT run, per brief

`refresh_all.py` was NOT run and the test suite was NOT run. `research/insights.db`,
`bank_metrics.csv` and every downstream deliverable therefore still hold the OLD
values for **Gulf International Bank (UK)** (1000x understated), **BPI Europe**
(Overview 1000x overstated) and **Persia International Bank** (1.43x overstated),
as well as Zenith's from 2026-09-15. **A refresh is required before any of those
four banks is trusted downstream.** Nothing was committed; no other session was
messaged; no locked script was edited.
