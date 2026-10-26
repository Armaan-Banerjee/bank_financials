# Batch 4 unresolved-bank retry — 12 October 2026

Collection only. No bank workbook, build script, curated store, extract, CSV or XLSX was changed.

## Outcome

- Retried all **13** formerly unresolved batch-4 banks from cached primary-source reports first.
- Closed **10** current-report questions: seven verified `publishes_none` findings and three banks with newly recovered current-year figures.
- Recovered **13 verified figures**: six for Hampshire Trust Bank, two for Monument Bank, four for UBA UK and one for Weatherbys.
- **Three report-specific gaps remain**: Co-operative Bank FY2025, Monument Bank FY2025 and Tandem FY2025.
- Every promoted PDF finding was read from a 300-dpi page rendering. Whole-report text/OCR was used for navigation and negative searches only.

## Newly recovered figures

| Bank | Years | Finding | Primary source |
|---|---|---|---|
| Hampshire Trust Bank | FY2025 / FY2024 | Bank-column RoTE **16.7% / 16.9%**; return on required equity **22.4% / 25.6%**; post-tax ROE **14.9% / 15.2%** | [HTB Annual Report 2025](https://www.htb.co.uk/htbcontent/uploads/2026/04/HTB_Annual_Report_2025.pdf), printed p.13; definitions printed p.166 |
| Monument Bank | FY2024 / FY2023 | ROE **-22% / -44%**, defined as loss after tax divided by average equity | Monument Bank Limited Annual Report 2024, printed p.12, Companies House company 10921940 |
| UBA UK | FY2024 / FY2023 | Pre-tax ROE **16% / 24%**; return on total assets **2.75% / 2.93%** | [UBA UK Annual Report 2024](https://www.ubauk.com/wp-content/uploads/sites/29/2025/07/UBA-UK-2024-AR-1.pdf), p.28 |
| Weatherbys | FY2025 | Group ROE **8.9%**; profit after tax excluding exceptional items divided by average shareholders' funds excluding AT1 | [Weatherbys Banking Group Annual Report 2025](https://www.weatherbys.bank/app/uploads/2026/05/Weatherbys-Banking-Group-Annual-report-2025.pdf), printed pp.11 and 93 |

HTB's decisive table has four columns—Group 2025, Group 2024, Bank 2025 and Bank 2024. The figures recorded above are deliberately the **Bank** columns, matching the workbook's parent-entity perimeter. Weatherbys' consolidated Group figure matches that workbook's consolidated reporting perimeter but is non-comparable with unadjusted computed ROE because it excludes exceptional items and AT1 capital.

## Verified no published return value

| Bank | Year | Evidence |
|---|---:|---|
| Aldermore Bank PLC | FY2025 | Whole-report OCR; 300-dpi KPI page lists NIM, cost/income and cost of risk only. The glossary defines ROE but no value is reported. The Aldermore Group 7.7% figure remains outside the Bank-solo perimeter. |
| Bank Saderat PLC | FY2025 | Whole-report OCR; 300-dpi KPI page says return-style KPIs would have limited value in the current circumstances and lists other indicators. |
| Charity Bank | FY2025 | Born-digital whole-report search; 300-dpi financial-highlights pages contain statement, lending and regulatory indicators but no return ratio. |
| J.P. Morgan Europe Limited | FY2025 | Whole-report OCR; 300-dpi KPI page contains earnings, balance-sheet, customer and regulatory metrics but no return ratio. |
| Nomura Bank International plc | FY2026 | Born-digital whole-report search; 300-dpi financial-KPI page contains profit, assets, liabilities and shareholders' funds but no return ratio. [Official report](https://www.nomuranow.com/portal/site/public/en-gb/resources/upload/NBI-Annual-Report-310326.pdf). |
| Persia International Bank PLC | FY2025 | Whole-report OCR; 300-dpi Strategic Report pages identify interest income, administrative expenses and regulatory compliance as the relevant KPIs, with no numeric return value. |
| RCI Bank UK Limited | FY2025 | Preserved audit of the exact 140-page Companies House scan confirms whole-report OCR navigation and independent 300/400-dpi readings; the Strategic Report's business-performance/KPI discussion on folios 6-8 and the separate FY2025 Pillar 3 report publish no return value. |

`publishes_none` means the own report does not publish a return ratio; it does not mean a return cannot later be calculated from the statements.

## Remaining source requests

1. **The Co-operative Bank p.l.c. FY2025 ARA.** The [official CRD V page](https://www.co-operativebank.co.uk/about-us/our-business/capital-requirements-directive-compliance/) says the 2025 annual report publishes ROA and defines it as net profit divided by total balance sheet. The locally available [FY2024 ARA](https://www.co-operativebank.co.uk/pdfs/bank/investorrelations/2024-annual-report-and-accounts.pdf) was searched in full and contains no numeric ROA, so the FY2025 report is the required source.
2. **Monument Bank Limited FY2025 Annual Report.** The cached document attached to the earlier route is visibly FY2024. The exact [official FY2025 PDF](https://cdn.prod.website-files.com/6435124ea79f72c265f72807/6ab68b85f380864b01e45564_Monument%20Bank%20Limited%20-%202025%20Annual%20Report.pdf) is now known but could not be opened through the available document route. FY2024/FY2023 ROE is captured; the linked FY2025 PDF still needs downloading.
3. **Tandem Bank Limited Annual Report and Accounts Year End 2025.** The [official newsroom](https://www.tandem.co.uk/newsroom) lists it, but the dynamically loaded PDF URL could not be recovered. The report must be for company **00955491**, not Tandem Money Limited.

## Evidence boundary

- No return was backsolved from P&L and balance-sheet values.
- No parent, segment or similarly named entity figure was assigned to a bank.
- OCR alone was not promoted as verified evidence; decisive positive and negative pages were visually checked at 300 dpi.
- Detailed row-level citations and comparability flags are in [`batch_4.jsonl`](batch_4.jsonl).
