# RWA sheet unit/currency consistency — judgement

**Date:** 2026-09-15
**Scope:** the seven banks whose `Total RWAs` sheet and `RWA Breakdown` sheet declare
different units or currencies, which made them incomparable in the cross-sheet RWA sweep.
**Nothing was converted or relabelled.** This file records, per bank, (a) whether both
sheets are internally correct in their own declared unit, and (b) whether the mixed
presentation is deliberate (the source documents themselves use different units) or
accidental (a workbook-side choice).

Method: read each build script's `Total RWAs` metric call, its `rwa_breakdown_rows` /
`add_rwa_breakdown_sheet` call, and both sheets' source-citation text, then compare the two
totals after putting them on the same scale by hand.

---

## Summary

| Bank | Total RWAs sheet | RWA Breakdown sheet | Both internally correct? | Mixed presentation is… |
|---|---|---|---|---|
| ClearBank | £m | £'000 | Yes (FY2024 £211m vs £212m is a disclosed 1-unit rounding artifact, already documented) | **Accidental** — the sources are in £m; the £'000 is workbook-introduced |
| Jordan International Bank | £m | £'000 | Yes — every year ties exactly | **Deliberate-ish** — JIB's own documents use both units across years |
| Bank of Beirut (UK) | £m | £'000 | Yes — every year ties to ≤£1k | **Accidental** — the source is £'000 in all years; the £m rounds disclosed precision away |
| Credit Suisse (UK) | £m | £'000 | Yes — all five years round exactly | **Deliberate** — the KPI table is in £m, the UK OV1 is in £'000 |
| Kuwait Finance House | **USD m** (not £m) | **USD'000** (not £'000) | Yes — agree to ~0.05% | **Accidental** but harmless; the deeper issue is that *both* sides are derived, not disclosed |
| ABC International Bank | £m (3 d.p.) | £'000 | Yes on scale — but FY2023 differs by £3.566m for a separate, non-unit reason (see below) | **Deliberate** — £m with 3 decimals is £'000 precision |
| J.P. Morgan Securities plc | £'000 (FX-converted) | US$'000 (raw) | Yes — the ~35% gap is the USD/GBP spot rate, as suspected | **Deliberate and already documented in the sheet subtitle** |

**No conversion is recommended anywhere on this evidence.** Two labelling improvements are
noted below as suggestions only.

---

## Bank by bank

### ClearBank — £m vs £'000
- `Total RWAs` (£m): FY2025 266, FY2024 211, FY2023 163, FY2022 38, FY2021 26, FY2020 26.2.
- `RWA Breakdown` TOTAL (£'000): 266000, 212000, 163000, 38000, 26000, 26200.
- Rescaled they agree in every year except FY2024 (£211m vs £212m). That £1m is **already
  documented in the script**: "FY2024's Total here (£212m = £34m + £178m) is £1m higher than
  the FY2024 figure on this workbook's own Total RWAs sheet (£211m) — an immaterial rounding
  artifact in ClearBank's own Pillar 3 table, reproduced as disclosed rather than
  force-matched." Both sides are internally correct.
- **Judgement: accidental.** ClearBank's Pillar 3 tables are in **£m** — the breakdown sheet's
  own subtitle says so ("source tables are in £m; converted x1000 for unit consistency with
  other sheets"). So the £'000 label is a workbook-side multiplication, and it implies
  precision to the nearest £1,000 that the source does not have (e.g. "£45,000k" is really
  "£45m"). Not wrong, but the more honest label for that sheet would be £m, matching both the
  source and the Total RWAs sheet.
- **Recommendation (not applied):** relabel the RWA Breakdown sheet to £m rather than convert
  anything. Deferred because it changes a sheet's declared unit and is presentational only.

### Jordan International Bank — £m vs £'000
- `Total RWAs` (£m): 473, 449, 435.3, 407.5, 401.6, 397.8, 383.1, 392.6, 391.8 (FY2024→FY2016).
- `RWA Breakdown` TOTAL (£'000): 473013, 448934, 435349, 407500, 401600, 397800, 383100,
  392600, 391800.
- Every single year ties (473 ↔ 473,013k; 449 ↔ 448,934k; 435.3 ↔ 435,349k; the rest exact).
  Both sheets internally correct.
- **Judgement: substantially deliberate.** JIB's own Pillar 3 Reports genuinely use both
  units: Section 3.3 is an RWA-by-risk-type table in £'000 for FY2016–FY2019 and FY2022–FY2024,
  but FY2020 and FY2021 disclose Pillar 1 capital requirements **in £m** (which the script then
  ×12.5s, documenting it). The breakdown sheet's subtitle already says "£'000, except
  FY2021/FY2020 derived from £m". The Total RWAs sheet's £m is a rounding of the same series.
  No action.

### Bank of Beirut (UK) — £m vs £'000
- `Total RWAs` (£m): FY2025 294.9, FY2024 250.1, FY2023 248.5, FY2022 317.6, FY2021 295.9.
- `RWA Breakdown` TOTAL (£'000): 294920, 250107, 248534, 317552, 295938 → 294.920, 250.107,
  248.534, 317.552, 295.938. Every year agrees to within £1k of the rounded £m figure.
- Category rows foot to their own totals within £1k (FY2024 208,563+110+41,433 = 250,106 vs a
  printed 250,107; FY2022 289,747+128+27,678 = 317,553 vs 317,552) — ordinary source rounding.
- **Judgement: accidental.** The breakdown sheet's own source line states the Bank's Pillar 3
  Disclosures are "£'000s, all years" — so the source unit is £'000 throughout and the Total
  RWAs sheet's £m is a workbook-side rounding that discards one decimal place of *disclosed*
  precision. Harmless (the FY2022 KM1-vs-ICAAP ~1% basis note on that sheet matters far more
  than the rounding), but the £m label is the less faithful of the two.
- **Recommendation (not applied):** if either sheet is ever revisited, carry the Total RWAs
  sheet in £'000 to match the source. Presentational only; deferred.

### Credit Suisse (UK) Limited — £m vs £'000
- `Total RWAs` (£m): FY2025 160, FY2024 672, FY2023 1000, FY2022 1124, FY2021 1340
  (FY2020–FY2016 also populated: 1338, 1371, 1225, 1241).
- `RWA Breakdown` TOTAL (£'000): 160021, 671676, 999597, 1123970, 1339867; FY2020–FY2016 are
  "Not publicly disclosed".
- Rescaled: 160.021, 671.676, 999.597, 1123.970, 1339.867 — these round to exactly 160, 672,
  1000, 1124, 1340. Perfect agreement in all five overlapping years.
- **Judgement: deliberate.** Two different source tables with two different native units — the
  Bank's KPI table (whole £m, which is also the only source for FY2016–FY2020) and the UK OV1
  template (£'000, which only exists FY2021–FY2025). Keeping the Total RWAs sheet on the KPI
  table preserves a nine-year consistent series; adopting OV1 precision for five of nine years
  would break it. No action.

### Kuwait Finance House — USD m vs USD'000 (the sweep's "£m vs £'000" label is wrong here)
- `Total RWAs` unit is **"USD m"**, not £m: FY2025 1618.4, FY2024 1649.3, FY2023 1666.0,
  FY2022 1530.2, FY2021 1421.3.
- `RWA Breakdown` TOTAL is **USD'000**: 1617663, 1648188, 1664325, 1527425, 1423413 →
  1617.663, 1648.188, 1664.325, 1527.425, 1423.413. Agreement is ~0.03–0.2% every year.
- **Judgement: accidental and harmless as a *unit* matter** (nothing is being compared across
  currencies — both sides are USD). No conversion needed or advisable.
- **The more important finding, recorded here rather than acted on:** *neither* number is a
  disclosed RWA. The Total RWAs sheet's own note says so — "Total RWAs are NOT directly
  disclosed in the source — calculated as Own Funds / Total Capital ratio for each year …
  Treat as an approximation" — which is exactly the **back-solved-RWA pattern** flagged for
  Cater Allen in `RESUME_SESSION.md` §2a and withdrawn for Bank Mandiri and Alpha Bank. The
  breakdown side is derived too (disclosed Pillar 1 capital requirement × 12.5), but that is a
  definitional conversion rather than a back-solve from a rounded printed ratio, and it is the
  sounder of the two. **This belongs in the same user decision as Cater Allen and is
  deliberately not changed here** — it is outside this task's scope, and the two derivations
  agreeing to 0.2% is a genuine cross-validation rather than evidence either is quoted.

### ABC International Bank plc — £m (3 d.p.) vs £'000
- `Total RWAs` (£m): FY2025 3880.104, FY2024 3486.256, FY2023 3104.763, FY2022 2450.11,
  FY2021 2507.675, FY2020 2397.973, FY2019 2824.811, FY2018 2940.867, FY2017 2574.027,
  FY2016 2342, FY2015 2152, FY2014 1914.
- `RWA Breakdown` TOTAL rows (£'000), across three basis blocks: consolidated {FY2025 3880104,
  FY2024 3486256, FY2023 3101197}; solo {FY2025 3131618, FY2022 2450110, FY2021 2507676};
  derived solo {FY2020 2397976, FY2019 2824814, FY2018 2940876, FY2017 2574025}.
- **Unit judgement: deliberate and correct.** "£m" carried to three decimals *is* £'000
  precision; FY2025 3880.104 ↔ 3,880,104k, FY2024 3486.256 ↔ 3,486,256k, FY2022 2450.11 ↔
  2,450,110k, FY2021 2507.675 ↔ 2,507,676k (1k), FY2020–FY2017 all within 3k. Both sheets are
  internally correct in their own declared unit and no conversion is needed.
- **Separate finding, NOT a unit problem (recorded, not changed):** FY2023 is 3,104.763 on the
  Total RWAs sheet against 3,101,197k on the breakdown — **£3.566m apart**, which is an edition
  restatement, not rounding. The breakdown's own source note explains why: ABCIB's FY2023
  Pillar 3 document carries only a single Total RWA figure and no OV1 category table, so the
  breakdown's FY2023 column is taken from the **FY2024 report's comparative column** while the
  Total RWAs sheet's FY2023 comes from the **FY2023 document's own Table 3**. That is the
  correct handling under the project's own-edition rule. But the RWA Breakdown sheet's subtitle
  currently claims "Each year's TOTAL matches (within rounding) the Total RWAs sheet's figure
  for that year" — which is not true for FY2023 and would mislead a reader who checks.
  **Suggested (not applied): amend that subtitle clause to carve out FY2023 and name the
  restatement.** Left alone here because the ten-row sweep did not flag ABCIB (the differing
  unit labels hid it) and changing a subtitle is outside this pass's remit.

### J.P. Morgan Securities plc — £'000 vs US$'000
- `Total RWAs` is declared **£'000** and is built as `stock(RWA_USD)`, where
  `stock()` = `round(usd_value / FX_SPOT[year])` — i.e. the disclosed US$'000 RWA converted to
  GBP at that year-end's spot rate. Underlying US$'000: FY2025 227,965,642; FY2024
  195,273,360; FY2023 187,226,000; FY2022 166,720,000; FY2021 226,258,000.
- `RWA Breakdown` TOTAL is the **same `RWA_USD` dict, unconverted**, and the sheet declares it:
  `unit_suffix=" ($'000)"`, subtitle "Entity-level basis, US$'000 (not GBP-converted)", and the
  source note says "US$'000 (NOT GBP-converted, consistent with the Balance Sheet/P&L/Equity
  sheets above)".
- **Both are correct and the suspicion in the sweep is confirmed: the ~35% gap is the USD/GBP
  rate, nothing more.** The two sheets are the same numbers, one converted and one not.
- **Judgement: deliberate, and the only one of the seven that is explicitly labelled as such on
  the sheet itself.** The asymmetry is odd (the statement sheets and the breakdown stay in USD
  while the Pillar 3 metric sheets convert to GBP), but it is a stated, consistent choice and
  the FX conversion is applied at a documented point-in-time spot rate for a point-in-time
  stock figure, which is the methodologically right convention. **No change.** A wrong or
  double conversion here would be far worse than the inconsistent label.

---

## What was deliberately NOT done

- **No unit conversions, on any of the seven.** Every one was found internally correct in its
  own declared unit, so a conversion could only introduce error.
- **No relabelling**, including the two cases where a label is arguably less faithful than the
  source (ClearBank's £'000, Bank of Beirut's £m). Both are presentational, both are recorded
  above, and neither changes a number.
- **Kuwait Finance House's back-solved Total RWAs** — flagged above, left for the same user
  decision as Cater Allen (`RESUME_SESSION.md` §2a).
- **ABC International's FY2023 £3.566m Total-vs-Breakdown gap and its overclaiming subtitle** —
  diagnosed above, not edited.
