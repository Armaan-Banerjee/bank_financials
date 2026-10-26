# batch_7 profitability sweep — cold-resume handoff

Output: `research/profitability/sweep/batch_7.jsonl` (append-only, one record per
bank-year or one explicit unresolved checkpoint per bank).

## Status

- Complete: 20/20 banks checkpointed and matched exactly to `batch_7.json`.
- 64 JSONL records: 54 published-figure records and 10 explicit
  `publishes_none` records; no bank-level unresolved checkpoint remains.
- 19/20 banks have presentation-ready evidence; 58 records are backed by
  300 dpi page reads and Arab Bank Europe's six exact primary-text records are
  retained as `ocr_lead` pending page rendering.
- Bank outcomes: 10 publish relevant return figures and 10 publish none.
- This is collection only. Nothing has been added to worksheets, curated
  `published_returns.jsonl`, extracts, CSV/XLSX or delivery files.

## Method in force

Primary sources only. Check the bank's own site/disclosure index and Companies
House where needed. Verify own legal-entity perimeter. Born-digital text is
navigation only; figures require a 300 dpi page read to be presentation-ready.
Scans may be OCR'd only to locate candidate pages. A blocked render/download is
`unresolved`; an exact text-layer figure without a readable render is
`ocr_lead`. Parent/group/segment metrics are excluded. Never backsolve.

## Source log

- **ARAB BANK EUROPE** — the search-indexed text of the bank's exact legacy-site
  reports recovered a complete own-edition FY2025-FY2023 ROE/ROA series from
  printed p.6: ROE 4.82%/5.25%/3.65% and ROA 0.61%/0.68%/0.50%. The reports
  define ROE as Net Income / Shareholder Equity and ROA as Net Income / Total
  Assets, so both use period-end denominators and are non-comparable with the
  project's average-balance measures. The old PDF routes now redirect before
  rendering; all six are therefore `ocr_lead`, not `300dpi`. Parent Arab Bank
  plc figures were excluded.
- **BANK OF CHINA UK** — official FY2024 report/index:
  `https://www.bankofchina.com/uk/aboutus/ab4/202507/t20250718_25422008.html`
  and `https://pic.bankofchina.com/bocappd/uk/202507/P020250718380377744220.pdf`.
  The exact 122-page report was recovered from the document cache, searched in
  full, and its CEO/Strategic Business Review pages read at 300 dpi. They report
  assets, income and profit but no ROE/ROA/RoTE. `publishes_none`; parent and
  overseas-branch figures excluded.
- **BARCLAYS BANK PLC** — exact 451-page FY2025 Companies House filing recovered
  from the document cache; performance-measures page read at 300 dpi. Captured
  FY2025/FY2024 solo-consolidated ROA of 0.4%/0.4% and Barclays Bank PLC Group
  ROA of 0.4%/0.3%. The two perimeters are kept distinct and formulas are not
  inferred. Barclays PLC/divisional RoTE excluded.
- **CITIBANK UK** — official FY2024 KPI page rendered at 300 dpi. Captured ROCE
  `(16)%` (PBT/year-end shareholder equity) and ROA `(8.35%)` (PBT/year-end
  assets), both non-comparable with the project's post-tax average-balance
  measures.
- **IFAST GLOBAL BANK LIMITED** — official 70-page FY2025 report searched in
  full; strategic financial-performance/capital pages rendered. No bank return
  ratio; parent/biographical mentions excluded. `publishes_none`, 300 dpi.
- **RELIANCE BANK** — official 62-page FY2025 report searched in full and KPI
  pages rendered. Complete KPI set contains no return ratio. `publishes_none`,
  300 dpi.
- **ZOPA** — official 188-page FY2024 report searched in full; dedicated KPI
  page rendered, APM appendix checked. No return ratio. `publishes_none`, 300
  dpi.
- **CAF BANK** — official FY2025 report searched in full; dedicated KPI spread
  printed pp.25-26 rendered and read. It reports lending, deposits, PAT and NII
  but no return ratio. `publishes_none`, 300 dpi.
- **CROWN AGENTS BANK** — official FY2025 report searched in full; KPI spread
  printed/PDF pp.18-19 rendered and read. No ROE, ROA or RoTE.
  `publishes_none`, 300 dpi.
- **FIDBANK UK** — exact FY2025 Companies House own-entity filing, Financial
  Highlights printed/PDF p.6. Captured the bank's five-year ROE series:
  1.63%, (3.9)%, (5.3)%, (15.2)% and (14.6)% for FY2025-FY2021. Formula is PAT
  divided by year-end shareholders' funds, so it is not comparable with the
  project's average-equity measure. Page read at 300 dpi.
- **GUARANTY TRUST BANK UK** — exact FY2024 own-entity filing, KPI printed/PDF
  p.5. Captured FY2024/FY2023 Return on Equity Ratio of 19.75%/30.73%; the bank
  defines it as PBT divided by average equity, hence non-comparable. Page read
  at 300 dpi.
- **HBL BANK UK** — exact FY2025 own-entity filing searched in full;
  financial-performance and three-year-trend pages checked. No return ratio.
  `publishes_none`, 300 dpi.
- **KEXIM BANK UK** — exact FY2025 own-entity filing searched in full; KPI page
  printed p.3/PDF p.5 checked. No return ratio. `publishes_none`, 300 dpi.
- **MELLI BANK** — exact FY2025 own-entity filing searched in full; KPI and
  capital/liquidity pages checked. Its Equity to Assets Ratio is a
  capital-structure ratio, not ROA; pension-plan return wording was also
  excluded. `publishes_none`, 300 dpi.
- **NATIONAL BANK OF EGYPT UK** — exact own-entity filings for FY2025-FY2021
  checked at 300 dpi. Captured seven records: the defined, comparable Return on
  average shareholders' funds series for FY2025-FY2023 (2.26%, 3.41%, 4.07%)
  plus both separately labelled but undefined return measures in each of
  FY2022 and the 18-month FY2021 period. No formula was inferred for the latter.
- **ONESAVINGS** — exact bank filings for FY2025-FY2021 checked at 300 dpi.
  Captured ten Group-perimeter bank-published APM records: FY2025/FY2024 RoTE,
  and statutory/underlying ROE for FY2024, FY2023, FY2022 and FY2021. Tangible,
  underlying and AT1 adjustments are recorded explicitly; no PLC-wide metric
  from outside the bank's own accounts was substituted.
- **QIB UK** — exact own-entity filings for FY2025-FY2021 checked at 300 dpi.
  Captured five annual Pre-Tax Return on Capital values plus FY2023 ROA. The
  defined return-on-capital denominator is share capital plus prior retained
  earnings; earlier undefined formulas were not inferred from later editions.
- **STANDARD CHARTERED BANK** — official Standard Chartered Bank 2025 report,
  supplementary information printed p.205/PDF p.206. Captured Bank Group ROA
  of 0.6%/0.5% for FY2025/FY2024, defined over year-end Group assets. Standard
  Chartered PLC RoTE was excluded. Page read at 300 dpi.
- **THIS BANK** — exact FY2025 own-entity filing under its then legal name JN
  Bank UK Limited searched in full; KPI printed/PDF pp.6-7 checked. No return
  ratio. `publishes_none`, 300 dpi. The January 2026 rename is documented in
  the record.
- **UNITED NATIONAL** — exact own-entity filings for FY2025-FY2021 checked at
  300 dpi. Captured ten ROE/ROA records. The 2025 report's revised post-tax,
  average-balance methodology and FY2024 comparative are kept distinct from
  the older pre-tax/period-end definitions.

## Validation

- Every JSONL line parses successfully.
- Distinct bank set equals the 20-bank `batch_7.json` manifest (no missing or
  extra banks).
- Outcome partition is exhaustive: 10 figure banks + 10 `publishes_none` banks
  = 20.
- Record partition is exhaustive: 54 figure records + 10 `publishes_none`
  records = 64.
- All 54 figure records use the established batch schema: the exact published
  label is in `measure` and the displayed percentage string is in `value`.
  No `value_pct`, `published_label`, `numerator` or `denominator` helper fields
  remain.
- Duplicate-key check on `[bank, year, measure, value]` returns zero duplicate
  groups.
