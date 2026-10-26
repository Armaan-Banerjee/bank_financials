# Profitability unresolved retry — early batches (2026-10-12)

Scope: retry the nine remaining batch 1–3 cases against the exact annual accounts already used for the project financial statements. This was a collection-only pass: no bank worksheet, build script, curated store, extract, CSV or XLSX was changed.

## Outcome

Eight of the nine cases are now settled. The retry resolved all eight earlier OCR leads: six unique records were retained at 300-dpi quality, while HSBC UK's two FY2024 later-edition comparatives were confirmed against—and omitted in favour of—the existing FY2024 own-edition records. It also established five defensible `publishes_none` findings. Metro Bank remains unresolved pending one exact statutory PDF.

| Bank | Outcome | Primary-source evidence |
|---|---|---|
| Methodist Chapel Aid | FY2025 Return on Assets **1.0%**; FY2024 comparative 1.1%. No definition, and FY2025 is a nine-month period. | [MCA Annual Report and Accounts 2025](https://www.mcafundingforchurches.co.uk/media/4bcl2vk5/mca-ar-2025.pdf), printed p.10/PDF p.12, read at 300 dpi. |
| HSBC UK Bank plc | FY2025 RoE **15.8%** and RoTE **19.2%**; FY2024 comparatives 16.5% and 20.2%. Both use ordinary/tangible equity adjustments and are not directly comparable with total-equity computed ROE. | [HSBC UK Bank plc Annual Report and Accounts 2025](https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2025/annual/pdfs/hsbc-uk-bank-plc/260225-annual-report-and-accounts-2025.pdf), printed pp.10 and 123/PDF pp.12 and 125, read at 300 dpi. |
| Turkish Bank (UK) | FY2025 Return on Equity **(2.01)%**; FY2024 comparative 2.61%. The report separately prints loss/PBT as a percentage of equity but does not define ROE, so comparability remains false. FY2021–FY2024 leads were also promoted after visual checks. | [Turkish Bank (UK) Annual Report and Financial Statements 2025](https://www.turkishbank.co.uk/wp-content/uploads/2026/04/Financial-Statements-TBUK-signed.pdf), printed p.5/PDF p.7, read at 300 dpi after full-report OCR. |
| RBS plc | Verified `publishes_none`. Whole-report searches found no ROE/ROA/RoTE, and the complete KPI table contains cost:income, impairment, CET1, leverage, RWAs and loan:deposit only. | [RBS plc Annual Report and Accounts 2025](https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/results-center/13022026/rbs-annual-report.pdf), printed p.4/PDF p.5, read at 300 dpi. |
| StreamBank | Verified `publishes_none`. The full KPI table reports income, PBT, CET1 and leverage but no return ratio; whole-report return searches were clean. | [StreamBank Annual Report and Financial Statements 2025](https://streambank.co.uk/pdf/March-2025-Annual-Report-2025.pdf), printed/PDF p.12, read at 300 dpi. |
| Vida Bank | Verified `publishes_none`. The only explicit return-on-equity language is a future 2026 ambition, not a FY2025 value. | [Vida Bank Annual Report and Accounts 2025](https://www.vidabank.co.uk/media/pkmnxlqg/annual-report-and-accounts-2025-company.pdf), printed/PDF pp.4 and 6, read at 300 dpi after whole-report search. |
| Perenna Bank | Verified `publishes_none`. Full OCR search of the 76-page scan found no ROE/ROA/RoTE; the complete KPI table contains leverage and CET1 only. | [Perenna Bank PLC FY2025 Companies House filing](https://find-and-update.company-information.service.gov.uk/company/13084174/filing-history/MzUyNTM5NTkxM2FkaXF6a2N4/document?format=pdf&download=0), printed p.1/PDF p.4, read at 300 dpi. |
| Schroder & Co. | Verified `publishes_none` at the Company perimeter. The Company says its KPIs align with group measures but refers readers to the separate Schroders plc report and publishes no Company return ratio; full OCR return search was clean. | [Schroder & Co. Limited FY2025 Companies House filing](https://find-and-update.company-information.service.gov.uk/company/02280926/filing-history/MzUxODQzNTIxOWFkaXF6a2N4/document?download=0&format=pdf), printed p.4/PDF p.6, read at 300 dpi. |

## Remaining document request

Metro Bank is the sole unresolved case in these three batches. The cached [Metro Bank Holdings PLC Annual Report and Accounts 2025](https://www.metrobankonline.co.uk/globalassets/documents/investor_documents/metro-bank---annual-report-2025.pdf) visually confirms consolidated holding-company RoTE of 6%, (23)% and 4% for FY2025–FY2023, but those figures cannot be substituted for Metro Bank PLC.

To settle the bank record, supply the exact **Metro Bank PLC Annual Report and Accounts 2025**, company 06419578, Companies House document `MzUzODAzNTg0NWFkaXF6a2N4` (163 pages): [direct Companies House PDF](https://find-and-update.company-information.service.gov.uk/company/06419578/filing-history/MzUzODAzNTg0NWFkaXF6a2N4/document?format=pdf&download=0). The target is its Strategic Report, “Key performance indicators”, printed p.11; the report is expected to contain the bank-consolidated RoTE cells and definition.

## Validation

- Batch 1: 64 records / 20 banks; zero unresolved; zero OCR leads.
- Batch 2: 48 records / 20 banks; one unresolved (Metro Bank); zero OCR leads.
- Batch 3: 42 records / 20 banks; zero unresolved; zero OCR leads; all records `300dpi`.
- JSON parsing, batch roster coverage and duplicate-record checks were rerun after editing.
