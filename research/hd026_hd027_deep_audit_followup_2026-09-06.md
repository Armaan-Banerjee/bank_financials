# HD-026/HD-027 deep audit follow-up — 2026-09-06

The completed historical-depth workbooks for Credit Suisse (UK), Jordan International Bank, Hampden & Co, Hampshire Trust Bank, Methodist Chapel Aid and United National Bank were reviewed for unsupported blanks and source inconsistencies.

## Recovery

Credit Suisse (UK)'s existing Total Capital sheet had left FY2021–FY2025 blank because its annual-report KPI tables only showed combined Tier 1/CET1. The bank's official UBS-hosted Pillar 3 disclosures provide the missing own-funds totals and total-capital ratios:

| Year | Total capital (£m, rounded) | Total capital ratio |
|---|---:|---:|
| FY2021 | 391 | 29.19% |
| FY2022 | 385 | 34.29% |
| FY2023 | 345 | 34.50% |
| FY2024 | 299 | 51.64% |
| FY2025 | 306 | 191.10% |

Sources: [CSUK Pillar 3 2021](https://www.ubs.com/global/en/investor-relations/complementary-financial-information/disclosure-legal-entities/archive-credit-suisse.html), [CSUK Pillar 3 2023](https://www.ubs.com/global/en/investor-relations/complementary-financial-information/disclosure-legal-entities/archive-credit-suisse.html), and [CSUK Pillar 3 2025](https://www.ubs.com/global/en/investor-relations/complementary-financial-information/other-subsidiaries.html), including the FY2024 comparative.

The figures were added to `scripts/build_credit_suisse_uk.py`; the workbook was rebuilt and its 18-sheet verifier passed with only the pre-documented cash-flow heuristic warnings. The other five banks' remaining blanks were supported by their source presentation or genuine non-disclosure; no further verified additions were made.

