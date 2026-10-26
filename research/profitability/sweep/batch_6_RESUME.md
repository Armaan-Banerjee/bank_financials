# Batch 6 profitability sweep — cold-resume handoff

Updated 2026-10-11. Output: `research/profitability/sweep/batch_6.jsonl`
(append-only, one record per bank-year/measure). This is collection-only work:
do not merge it into the curated store, rebuild deliverables, or edit bank
workbooks yet.

## Status

- DONE (20/20): ALPHA BANK LONDON, BANK OF CEYLON UK, BARCLAYS, C HOARE AND CO, CHETWOOD, CREDIT SUISSE UK, FCMB UK, GRIFFIN BANK, HAVIN BANK, ICICI BANK UK, JULIAN HODGE BANK, MARKS AND SPENCER FINANCIAL SERVICES, MORGAN STANLEY BANK INTERNATIONAL, OAKNORTH BANK, PUNJAB NATIONAL BANK INTERNATIONAL, REDWOOD BANK, SMBC, THE BANK OF LONDON GROUP, UNION BANK OF INDIA UK, ZENITH
- IN PROGRESS: none
- REMAINING (0): none

## Validation summary

- 47 schema-valid JSONL records cover all 20 worklist banks exactly at bank level: 36 published figures and 11 verified `publishes_none` findings.
- Every record is supported by a decisive page inspected at 300 dpi; scan-only reports were OCR-searched only for navigation before visual verification.
- Of the 36 published figures, 13 are own-edition figures and 23 are later-edition comparatives. Eight are definitionally comparable with the project's computed series; 28 are conservatively non-comparable because they use opening/year-end/monthly-average/tangible/regulatory/RWA/pre-tax bases or lack a complete definition.
- Final checks found no missing or extra worklist banks, duplicate bank/year/measure/value keys, malformed JSON lines, provisional OCR leads, unresolved records, or invalid positive/negative record shapes.

## Findings and primary sources

- **Alpha Bank London:** FY2025/FY2024 ROE is -1%/3%, explicitly net profit divided by opening total equity, from the [FY2025 exact-entity filing](https://find-and-update.company-information.service.gov.uk/company/00185070/filing-history/MzUyMzkyMTM5MGFkaXF6a2N4/document?format=pdf&download=0). Opening equity makes both non-comparable with average-equity ROE.
- **Bank of Ceylon UK:** verified `publishes_none` after a report-wide search and review of the complete KPI panel in the [FY2025 exact-entity filing](https://find-and-update.company-information.service.gov.uk/company/06736473/filing-history/MzUyMjY1MjQxM2FkaXF6a2N4/document?format=pdf&download=0).
- **Barclays:** FY2025/FY2024 ROA is 0.9%/0.9%; the [official FY2025 Barclays Bank UK PLC report](https://home.barclays/content/dam/home-barclays/documents/investor-relations/reports-and-events/annual-reports/2025/Barclays-Bank-UK-PLC-Annual-Report-2025.pdf) defines it as profit after tax divided by balance-sheet-date assets, so it is not comparable with average-assets ROA.
- **C. Hoare & Co.:** verified `publishes_none` from the complete KPI and financial coverage in the [official FY2026 report](https://www.hoaresbank.co.uk/files/2026-06/Financial_Report_2026.pdf).
- **Chetwood:** verified `publishes_none` after full-report and KPI review of the [official FY2025 report](https://chetwoodbank.co.uk/documents/chetwood-bank-annual-report.pdf).
- **Credit Suisse UK:** verified `publishes_none`; its KPI panel contains profit, cost/income, capital, leverage, liquidity, client assets and credit volume but no return measure in the [FY2025 exact-entity filing](https://find-and-update.company-information.service.gov.uk/company/02009520/filing-history/MzUxNzE0OTI3NGFkaXF6a2N4/document?format=pdf&download=0). UBS's official Credit Suisse legal-entity archive was also checked.
- **FCMB UK:** verified `publishes_none` from the complete KPI table and full-text review of the [official FY2025 report](https://fcmbuk.com/wp-content/uploads/2026/08/SIGNED-FCMB-Bank-UK-Limited-Audited-Accounts-2025.pdf).
- **Griffin Bank:** FY2025/FY2024 return on assets is (17%)/(89%) in the [official FY2025 report](https://cms.griffin.com/griffin-assets/Griffin_Bank_Ltd_Annual_Report_2025_edeb37eca7.pdf). Parentheses are preserved as negative values; no denominator definition is inferred.
- **Havin Bank:** FY2025/FY2024 return on investment is 1.52%/3.14% and return on assets is 0.31%/0.69% in the [FY2025 exact-entity filing](https://find-and-update.company-information.service.gov.uk/company/01074897/filing-history/MzUzNzM1MjkyOGFkaXF6a2N4/document?format=pdf&download=0). Both are explicitly pre-tax and non-comparable.
- **ICICI Bank UK:** verified `publishes_none`; the [official FY2026 report](https://www.icicibank.co.uk/content/dam/icicibank-revamp/uk/doc/financial-report-FY2026.pdf) identifies PBT as the bank's KPI and reports no own ROE/RoTE/ROA.
- **Julian Hodge Bank:** verified `publishes_none` from the [official FY2024 report](https://hodgebank.co.uk/wp-content/uploads/2025/02/Hodge-annual-report-21.02.25.pdf). A pension-plan “return on assets” hit was explicitly excluded as not a bank profitability metric.
- **Marks and Spencer Financial Services:** FY2025/FY2024 pre-tax return on average five-quarter RWAs is 0.3%/1.8%, and RoTE is 0.8%/8.1%, from the [FY2025 exact-entity filing](https://find-and-update.company-information.service.gov.uk/company/01772585/filing-history/MzUyNzI0MDUzNGFkaXF6a2N4/document?format=pdf&download=0). The RWA and tangible-equity bases are preserved and marked non-comparable.
- **Morgan Stanley Bank International:** FY2025/FY2024 return on shareholders' equity is 4.64%/5.98% and ROA is 0.63%/0.79% in the [FY2025 exact-entity filing](https://find-and-update.company-information.service.gov.uk/company/03722571/filing-history/MzUxNTMzMjAyMmFkaXF6a2N4/document?format=pdf&download=0). Both use beginning-of-year denominators and are non-comparable.
- **OakNorth Bank:** the [official FY2025 report](https://oaknorth.co.uk/wp-content/uploads/2026/03/Annual_Report_2025.pdf) supplies FY2020-FY2025 ROE of 12%, 17%, 16%, 17%, 17%, 16% and adjusted ROE of 19%, 30%, 26%, 22%, 22%, 22%, respectively. Statutory ROE is PAT attributable to ordinary shareholders over average equity excluding minority interest and is comparable; adjusted ROE uses required regulatory equity excluding surplus and is not.
- **Punjab National Bank International:** verified `publishes_none`; the [official FY2026 report](https://www.pnbint.com/PNBIL/pdf/Financial_Reports/PNBIL-Annual-Report-2026.pdf) enumerates five KPIs, none a return ratio.
- **Redwood Bank:** verified `publishes_none` from the complete key-highlights panel and full-text review of the [official FY2025 report](https://redwoodbank.co.uk/media/howpdnen/2025-annual-report-and-accounts_redwood-bank-signed-150426.pdf).
- **SMBC:** the [official FY2025 report](https://www.smbcgroup.com/emea/getmedia/28eec268-62ab-4d64-b597-02b7f918c767/smbcbi-annual-report-2025.pdf) reports ROE of 6.1%, 7.5%, 5.0% and 2.7% for FY2025-FY2022. It uses monthly-average equity, not the project's two-point average.
- **The Bank of London Group:** verified `publishes_none`; its KPI table reports net interest income, annual loss and year-end net assets but no return ratio in the [FY2025 exact-entity filing](https://find-and-update.company-information.service.gov.uk/company/12844788/filing-history/MzUzODUxMzE5M2FkaXF6a2N4/document?format=pdf&download=0).
- **Union Bank of India UK:** verified `publishes_none` from the complete KPI page and report-wide review of the [official FY2025 report](https://www.unionbankofindiauk.co.uk/Portals/0/pdf/Annual_report_UBI_UK_signed_31-03-2025.pdf). An OCR-noise “ROE” hit in a credit-risk table was excluded.
- **Zenith:** FY2020/FY2019 ROE is 7%/11% in the [official FY2020 report](https://www.zenith-bank.co.uk/media/2199/zenith-bank-uk-limited-annual-report-2020.pdf), explicitly PAT as a percentage of average shareholders' equity; both records are comparable.

## Method in force

Use official bank-hosted reports and report indexes first, then exact-entity
Companies House filings. Search the whole report for navigation and inspect the
decisive KPI/financial-highlights/APM page at 300 dpi. A negative grep alone
never establishes `publishes_none`; inspect the report's complete performance
coverage. Preserve exact entity, printed definition, sign, denominator and
edition status. OCR is navigation only; unverified text-only figures remain
`ocr_lead`, and inaccessible evidence remains `unresolved`.
