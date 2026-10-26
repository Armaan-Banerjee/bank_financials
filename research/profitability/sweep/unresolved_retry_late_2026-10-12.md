# Profitability unresolved retry — late batches (2026-10-12)

> **Superseded in part:** the later
> [`unresolved_retry_round2_2026-10-12.md`](unresolved_retry_round2_2026-10-12.md)
> recovered Arab Bank Europe's exact FY2025-FY2023 ROE/ROA series from the
> bank's search-indexed primary reports. Its old unresolved entry and the
> batch-7 counts below describe the earlier checkpoint; the other gaps remain
> current.

Scope: retry the seven unresolved batch 5 and batch 7 cases against the exact annual accounts and official bank disclosure routes. This was collection-only work: no bank worksheet, build script, curated store, extract, CSV or XLSX was changed.

## Outcome

Four of the seven cases are now settled. The retry added fourteen published-figure records across Credit Suisse International and Barclays Bank PLC, and established two defensible `publishes_none` findings for Union Bancaire Privée (UK) and Bank of China (UK). Three exact annual reports remain inaccessible to the required page-render workflow.

| Bank | Outcome | Primary-source evidence |
|---|---|---|
| Credit Suisse International | Five years each of Return on Total Assets and Return on Tier 1 capital were captured. FY2025 is **(2.7)%** and **(5.1)%** respectively; FY2024 is explicitly restated to exclude discontinued operations. The report prints no formula, and the Tier 1 denominator is regulatory capital. | [FY2025 Financial Statements](https://find-and-update.company-information.service.gov.uk/company/02500199/filing-history/MzUxNDA4Njk0M2FkaXF6a2N4/document?format=pdf&download=0), KPI table printed/PDF p.6, read at 300 dpi. |
| Barclays Bank PLC | Captured FY2025/FY2024 solo-consolidated ROA of **0.4%/0.4%** and Barclays Bank PLC Group ROA of **0.4%/0.3%**. The two perimeters are kept distinct and the unprinted formula is not inferred. | [Barclays Bank PLC Annual Report 2025](https://find-and-update.company-information.service.gov.uk/company/01026167/filing-history/MzUyMzkyMDY5MmFkaXF6a2N4/document?format=pdf&download=0), performance measures printed p.9/PDF p.11, read at 300 dpi. |
| Union Bancaire Privée (UK) | Verified `publishes_none`. The complete KPI table reports operating income, operating expenses, PBT, AUM and Tier 1 ratio but no ROE, ROA or RoTE. The Tier 1 ratio was not misclassified as a profitability return. | [FY2025 Companies House filing](https://find-and-update.company-information.service.gov.uk/company/00964058/filing-history/MzU0NzY3Mjg2OGFkaXF6a2N4/document?format=pdf&download=0), printed/PDF p.5; exact report read page-by-page at both 300 and 400 dpi. |
| Bank of China (UK) | Verified `publishes_none`. The CEO statement and Strategic Business Review report assets, income and profit but no return ratio; whole-document searches found no relevant ROE/ROA/RoTE. | [Bank of China (UK) Annual Report 2024](https://pic.bankofchina.com/bocappd/uk/202507/P020250718380377744220.pdf), printed/PDF pp.4 and 12, read at 300 dpi. |

## Remaining document requests

- **Goldman Sachs International Bank** — supply the exact 64-page FY2025 accounts for company 01122503, Companies House document `MzUxNzc2NzE5OGFkaXF6a2N4`: [direct PDF](https://find-and-update.company-information.service.gov.uk/company/01122503/filing-history/MzUxNzc2NzE5OGFkaXF6a2N4/document?format=pdf&download=0). The official Goldman Sachs UK Pillar 3 material was checked, but it is a different disclosure/perimeter and does not settle the bank's annual-report publication state.
- **Philippine National Bank (Europe) Plc** — supply the exact 45-page FY2025 full accounts filed 19 June 2026 for company 02939223: [Companies House accounts index](https://find-and-update.company-information.service.gov.uk/company/02939223/filing-history?category=accounts). Parent Philippine National Bank figures cannot substitute for the UK bank.
- **Arab Bank Europe plc** — supply the bank's 111-page FY2025 Annual Report: [official bank PDF](https://arabbankeurope.com/wp-content/uploads/202602_EABAnnualReport_v9.pdf). The project build notes record a prior full transcription and indicate the KPI table contains capital adequacy and CET1 only, but the source PDF/300-dpi evidence is no longer locally recoverable, so the profitability sweep remains conservatively unresolved rather than promoting an unverified absence.

## Validation

- Batch 5: 52 records / 20 banks; 43 figures, 7 `publishes_none`, 2 unresolved.
- Batch 7: 59 records / 20 banks; 48 figures, 10 `publishes_none`, 1 unresolved.
- All newly settled records are backed by 300-dpi evidence; JSON parsing, roster coverage and duplicate-record checks are rerun in the cross-batch validation.
