# Unresolved profitability retry — round 2 (2026-10-12)

> Superseded in part by the round-3 reports on 13 October 2026: Metro Bank was
> resolved with three exact RoTE values and Tandem was closed as an exact-report
> non-disclosure. Four banks remain unresolved; see
> `unresolved_retry_round3_2026-10-13.md`.

## Outcome

This collection-only retry resolved **Arab Bank Europe** and reduced the
bank-level acquisition queue from seven to six. No worksheet, curated store,
extract, CSV/XLSX or deliverable was changed.

The bank's exact reports publish the following own-edition series on printed
p.6:

| year | Return on equity | Return on assets |
|---|---:|---:|
| FY2025 | 4.82% | 0.61% |
| FY2024 | 5.25% | 0.68% |
| FY2023 | 3.65% | 0.50% |

The stated formulas are `Net Income / Shareholder Equity` and
`Net Income / Total Assets`. Both therefore use period-end denominators and are
not comparable with the project's average-balance ROE/ROA. The evidence is the
search-indexed text of the bank's own [FY2025 report](https://www.eabplc.com/downloads/202602_EABAnnualReport_v9.pdf),
[FY2024 report](https://www.eabplc.com/downloads/202502_EABAnnualReport_v3.pdf)
and [FY2023 report](https://www.eabplc.com/downloads/202304_EABAnnualReport_v4_Publish.pdf).
The legacy URLs now redirect before a page can be rendered, so the six records
are conservatively marked `ocr_lead`, not `300dpi`. Companies House independently
confirms the exact 132-page FY2025 filing for company 05575857 and document
`MzUxOTg3MjI1NWFkaXF6a2N4` in the bank's [official filing history](https://find-and-update.company-information.service.gov.uk/company/05575857/filing-history).

## Remaining exact-source queue

| bank | exact source now pinned down | remaining blocker |
|---|---|---|
| Metro Bank | [Metro Bank PLC FY2025 filing](https://find-and-update.company-information.service.gov.uk/company/06419578/filing-history/MzUzODAzNTg0NWFkaXF6a2N4/document?format=pdf&download=0), company 06419578, 163 pages | The bank-consolidated RoTE label and formula are recoverable on printed p.11, but its three value cells are image-only and still unread. The listed parent's 6%/(23)%/4% series remains excluded. |
| Co-operative Bank | [The Co-operative Bank p.l.c. FY2025 filing](https://find-and-update.company-information.service.gov.uk/company/00990937/filing-history/MzUxOTQwMjIzNGFkaXF6a2N4/document?format=pdf&download=0), company 00990937, 81 pages | The bank's [CRD V page](https://www.co-operativebank.co.uk/about-us/our-business/capital-requirements-directive-compliance/) says its ARA publishes ROA and defines it as net profit / total balance sheet, but the decisive 81-page PDF still redirects to an inaccessible signed object. |
| Monument Bank | [official FY2025 report](https://cdn.prod.website-files.com/6435124ea79f72c265f72807/6ab68b85f380864b01e45564_Monument%20Bank%20Limited%20-%202025%20Annual%20Report.pdf), company 10921940; Companies House document `MzU0ODQzMjY2OWFkaXF6a2N4`, 166 pages | Exact PDF is identified but could not be rendered or reliably indexed. |
| Goldman Sachs International Bank | [FY2025 filing](https://find-and-update.company-information.service.gov.uk/company/01122503/filing-history/MzUxNzc2NzE5OGFkaXF6a2N4/document?format=pdf&download=0), company 01122503, 64 pages | Signed Companies House object is inaccessible and the exact bank report is absent from the local cache. Goldman Sachs International and The Goldman Sachs Group are different entities and remain excluded. |
| Philippine National Bank Europe | [FY2025 filing](https://find-and-update.company-information.service.gov.uk/company/02939223/filing-history/MzUyNjIwMTYzNWFkaXF6a2N4/document?format=pdf&download=0), company 02939223, 45 pages | Exact filing/document ID is recovered, but the image-only PDF remains inaccessible. Parent Philippine National Bank figures are excluded. |
| Tandem | [FY2025 filing](https://find-and-update.company-information.service.gov.uk/company/00955491/filing-history/MzUzMDYwOTUxN2FkaXF6a2N4/document?format=pdf&download=0), company 00955491, 59 pages; also listed in the bank's [official newsroom](https://www.tandem.co.uk/newsroom) | Exact filing redirects to an inaccessible signed object and no explicit bank-published return value is exposed in indexed text. Tandem Money Limited and third-party calculated ratios are excluded. |

## Perimeter checks and exclusions

- Coventry Building Society's [2025 Annual Report](https://www.coventrybuildingsociety.co.uk/content/dam/cbs/member/pdfs/financial-results/2025/Annual-Report-and-Accounts-2025.pdf)
  was searched. Its 0.92% “Net profit as a percentage of total Balance Sheet”
  is for the enlarged Coventry Group, not The Co-operative Bank p.l.c. or the
  Bank sub-group, and was not substituted.
- A preserved text version of Metro Bank PLC's exact filing confirms that its
  bank-consolidated statutory PBT differs from Metro Bank Holdings PLC. This
  reinforces the existing perimeter exclusion; it does not justify copying the
  parent's RoTE values into the bank record.
- Third-party computed ROE/ROA values for Tandem, Monument and Goldman Sachs
  International Bank were used only as search leads and were not collected.

## Current collection state

Historical snapshot at the end of round 2; superseded by the round-3 report
linked at the top of this file.

The seven batches now contain **376 raw records across 140 banks**:
`300dpi` 327, `press_release` 3, `ocr_lead` 40 and unresolved/null 6. The
curated store remains unchanged by this retry at 157 records across 60 banks.
