# batch_5 sweep - cold-resume handoff

Output: `research/profitability/sweep/batch_5.jsonl` (append-only, one record per
bank-year). This is collection-only work: do not merge or rebuild deliverables.

## Status (updated after every bank)

- DONE (20/20): ALLICA, BANK OF BEIRUT UK, BANK SEPAH INTERNATIONAL, BROWN SHIPLEY, CHARTER COURT FINANCIAL SERVICES, CREDIT SUISSE INTERNATIONAL, FCE BANK, GOLDMAN SACHS INTERNATIONAL BANK, HANDELSBANKEN, ICBC STANDARD BANK PLC, JP MORGAN SECURITIES, LLOYDS BANK CORPORATE MARKETS, MONZO, NORTHERN BANK, PHILIPPINE NATIONAL BANK EUROPE, RECOGNISE BANK, SHAWBROOK, TD BANK EUROPE, UNION BANCAIRE PRIVEE UK, ZEMPLER
- IN PROGRESS: none
- REMAINING (0): none

## Validation summary

- 53 schema-valid JSONL records covering all 20 worklist banks exactly once at
  bank level: 45 published figures, 8 verified `publishes_none` findings and no
  unresolved findings.
- All 45 published figures and all 8 positive `publishes_none` findings were
  verified from a 300 dpi render.
- Of the 45 published figures, 15 are from their own edition and 30 are
  later-edition comparatives. All 45 are conservatively marked not comparable
  with the computed series because their published basis is pre-tax, tangible,
  year-end, or insufficiently defined.
- Final checks found no duplicate bank/year/measure keys, no missing worklist
  banks, no extra banks, and no malformed JSON lines.

## Latest checkpoint

- ALLICA: settled `publishes_none` from Allica Bank Limited's official FY2025 Annual Report. Its full 175-page born-digital text was searched, the exhaustive key-metrics page was read at 300 dpi, and the Non-IFRS appendix was checked. It publishes PBT, underlying PBT, gross revenue/profit after risk, lending and NIM, but no ROE/RoTE/ROA.
- BANK OF BEIRUT UK: two historical entity-only figures verified from the bank's official FY2017 report: Return on Average Equity 7.85% (FY2017 own edition) and 5.96% (FY2016 comparative). The newer official FY2021 and FY2023-FY2025 reports no longer publish a return measure. Neither historical record is marked comparable because the ratio's numerator is not explicitly defined and the table's shareholders' funds include a parent term subordinated loan.
- BANK SEPAH INTERNATIONAL: ten figures verified from the exact-entity FY2025 five-year KPI table: pre-tax return on average equity and pre-tax return on average total assets for FY2021-FY2025. Both FY2025 records are own-edition; FY2021-FY2024 are later-edition comparatives. All are non-comparable because the numerator is explicitly pre-tax.
- BROWN SHIPLEY: settled `publishes_none` from its FY2024 exact-entity accounts, official annual-report page and official Pillar 3. The full KPI coverage includes PBT/adjusted PBT, cost/income, AUM, flows and prudential ratios but no ROE/RoTE/ROA.
- CHARTER COURT FINANCIAL SERVICES: FY2025 14.3% and FY2024 17.0% Return on tangible equity, verified with the full printed definition. The definition says profit for the year over total share capital and reserves but does not state average timing, so neither is marked comparable.
- FCE BANK: FY2025 ROA 1.28% and FY2024 0.85%, explicitly PBT divided by year-end total assets; verified at 300 dpi and non-comparable.
- JP MORGAN SECURITIES: FY2025 ROA 0.3% and FY2024 0.4% from the exact-entity KPI table. No printed formula, so denominator timing is not asserted and the records remain non-comparable.
- HANDELSBANKEN: official FY2022 report publishes RoE 9.6% (FY2021 4%). No denominator definition, so non-comparable.
- ICBC STANDARD BANK PLC: official FY2021 consolidated report publishes ROE 7.3% (FY2020 9.4%). No denominator definition, so non-comparable.
- LLOYDS BANK CORPORATE MARKETS: five statutory RoTE figures from the official FY2023 report's five-year chart (FY2019-FY2023), with the verbatim definition from the performance-measures page. Tangible-net-assets basis, all non-comparable.
- SHAWBROOK: four FY2025/FY2024 underlying/statutory RoTE records from the official FY2025 report, with its verbatim average-tangible-equity definition. All non-comparable.
- ZEMPLER: official FY2023 report publishes RoTE 30% (FY2022: (16%)); newer FY2025/FY2026 reports no longer do. No formula, so non-comparable.
- MONZO: settled `publishes_none` from the official FY2026 report. The 'high return on equity model' wording is aspirational, not a reported ratio.
- NORTHERN BANK: settled `publishes_none` from the official FY2025 exact-bank report and its complete financial-highlights panel.
- RECOGNISE BANK: settled `publishes_none` from the bank's official FY2026 investor index/report and full financial summary; no ratio was backsolved despite first-time profitability.
- TD BANK EUROPE: settled `publishes_none` from the FY2025 exact-entity accounts and official solo Pillar 3 index; full KPI table read at 300 dpi.
- CREDIT SUISSE INTERNATIONAL: the exact FY2025 filing's KPI page was recovered from the document cache and read at 300 dpi. Captured five years each of Return on Total Assets and Return on Tier 1 capital (ten records); the FY2024 comparatives are explicitly restated to exclude discontinued operations. Formulas are not printed and the Tier 1 denominator is regulatory capital, so comparability is not asserted.
- UNION BANCAIRE PRIVEE UK: settled `publishes_none` from its exact FY2025 Companies House accounts. The complete KPI page was read at both 300 and 400 dpi and the report was searched page-by-page; it reports operating income, expenses, PBT, AUM and Tier 1 ratio but no ROE/ROA/RoTE. No ratio was backsolved.
- GOLDMAN SACHS INTERNATIONAL BANK: exact FY2025 report closed as
  `publishes_none`; its stated KPIs are profit, total assets and CET1 capital,
  with no ROE/ROA/RoTE.
- PHILIPPINE NATIONAL BANK EUROPE: exact FY2025 report publishes return on
  assets of **-3.5%** for FY2025 and **0.1%** for FY2024 on printed p.3.

## 13 October round-3 retry

- GSIB's official GSG UK Pillar 3 route was checked again. Its return language
  is a generic remuneration-performance list, not a numeric GSIB return; the
  exact 64-page GSIB annual accounts remain inaccessible. Goldman Sachs Group,
  GSG UK and Goldman Sachs International figures were not substituted.
- PNBE's exact standalone 12-page FY2025 Pillar 3 was searched end-to-end and
  contains no ROE, ROA or RoTE, but it explicitly points readers to PNBE's
  annual accounts. The exact 45-page accounts remain inaccessible, so this is
  not promoted to `publishes_none`. Parent Philippine National Bank figures
  were not substituted.
- The exact reports were subsequently supplied and completed: GSIB is a
  verified `publishes_none`, while PNBE adds two 300 dpi ROA records. Batch 5
  is now 53 records / 20 banks, all `300dpi`, with no unresolved record. No
  worksheet, build script, curated store, extract,
  CSV/XLSX or deliverable was changed.

## Method in force

Use official bank-hosted reports/indexes first, then Companies House. Confirm
PDF magic, search the whole report for navigation, and read the decisive page
at 300 dpi. A negative grep alone never establishes `publishes_none`; inspect
the report's KPI/financial-highlights/APM coverage. Preserve exact entity and
definition. OCR is navigation only; unverified text-only figures are
`ocr_lead`, and inaccessible evidence is `unresolved`.

Scratchpad: `/private/tmp/profit-b5`
