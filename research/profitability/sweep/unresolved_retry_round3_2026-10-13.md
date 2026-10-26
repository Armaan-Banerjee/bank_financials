# Unresolved profitability retry — round 3 (2026-10-13)

> Historical checkpoint, superseded later on 13 October 2026 after the four
> exact reports were supplied. All four gaps are now closed; see
> `unresolved_final_resolution_2026-10-13.md`.

## Outcome

This collection-only pass resolved **Metro Bank PLC** and closed **Tandem Bank
Limited** as a verified exact-report non-disclosure. The acquisition queue is
now four banks:

1. The Co-operative Bank p.l.c.
2. Monument Bank Limited
3. Goldman Sachs International Bank
4. Philippine National Bank (Europe) Plc

No worksheet, bank build script, curated profitability store, extract,
CSV/XLSX or downstream deliverable was changed.

## Newly settled

### Metro Bank PLC

The exact bank-consolidated [Metro Bank PLC FY2025 filing](https://find-and-update.company-information.service.gov.uk/company/06419578/filing-history/MzUzODAzNTg0NWFkaXF6a2N4/document?format=pdf&download=0)
was recovered through a faithful [preserved copy](https://cdn.financialreports.eu/financialreports/media/filings/4947/2026/RNS/4947_rns_2026-08-13_fc2af718-accf-4f50-a989-0ac163d4dea1.pdf).
Its KPI row on printed p.11/PDF p.12 publishes **Return on tangible equity**:

| year | RoTE |
|---|---:|
| FY2025 | 5% |
| FY2024 | -22% |
| FY2023 | 7% |

The report defines the numerator as statutory profit after tax attributable to
shareholders and the denominator as average tangible equity, excluding other
equity instruments, intangible assets and deferred tax assets. These are
bank-consolidated and tangible-equity figures, whereas the workbook statements
are Metro Bank PLC Company/standalone; all three records are therefore marked
non-comparable. Metro Bank Holdings PLC's separate 6%/(23)%/4% series remains
excluded. Full evidence and perimeter analysis are in
[`round3_metro_coop_2026-10-12.md`](round3_metro_coop_2026-10-12.md).

### Tandem Bank Limited

The exact 59-page [Tandem Bank Limited FY2025 filing](https://find-and-update.company-information.service.gov.uk/company/00955491/filing-history/MzUzMDYwOTUxN2FkaXF6a2N4/document?format=pdf&download=0)
had already been fully OCR'd with Tesseract and cross-checked against rendered
page images for the existing Tandem workbook source workflow. Re-auditing that
exact-report trail found no published ROE, ROA or RoTE. Tandem is therefore a
positive `publishes_none` finding rather than an unresolved acquisition gap.
The wider Tandem Money Limited group Pillar 3 is a different perimeter and was
excluded. Full evidence is in
[`round3_monument_tandem_2026-10-12.md`](round3_monument_tandem_2026-10-12.md).

## Remaining acquisition queue

| bank | exact source | current result |
|---|---|---|
| The Co-operative Bank p.l.c. | [FY2025 filing, company 00990937, 81 pages](https://find-and-update.company-information.service.gov.uk/company/00990937/filing-history/MzUxOTQwMjIzNGFkaXF6a2N4/document?format=pdf&download=0) | Its official CRD V page defines annual-report ROA, but no numeric value is exposed. The exact filing remains inaccessible; Coventry's enlarged-group 0.92% is excluded. |
| Monument Bank Limited | [official FY2025 report](https://cdn.prod.website-files.com/6435124ea79f72c265f72807/6ab68b85f380864b01e45564_Monument%20Bank%20Limited%20-%202025%20Annual%20Report.pdf), 166 pages | Exact report identified but neither first-party route can currently be rendered or indexed. FY2024's -22%/-44% ROE is already separately collected and does not establish FY2025. |
| Goldman Sachs International Bank | [FY2025 filing, company 01122503, 64 pages](https://find-and-update.company-information.service.gov.uk/company/01122503/filing-history/MzUxNzc2NzE5OGFkaXF6a2N4/document?format=pdf&download=0) | The GSG UK Pillar 3 has GSIB prudential columns but no numeric GSIB profitability return. The exact annual accounts remain inaccessible. Parent, GSG UK and Goldman Sachs International figures are excluded. |
| Philippine National Bank (Europe) Plc | [FY2025 filing, company 02939223, 45 pages](https://find-and-update.company-information.service.gov.uk/company/02939223/filing-history/MzUyNjIwMTYzNWFkaXF6a2N4/document?format=pdf&download=0) | The exact standalone [FY2025 Pillar 3](https://www.pnb.com.ph/storage/asset-libraries/Me1hxgtaSlrRs32Dvl6SIB1qgOfY1WbTDfGv2ZzQ.pdf) was searched end-to-end and contains no return ratio, but it points to the annual accounts, which remain inaccessible. Parent PNB figures are excluded. |

GSIB/PNBE source detail is recorded in
[`round3_gsib_pnbe_2026-10-12.md`](round3_gsib_pnbe_2026-10-12.md).

As a final acquisition check, exact-company-number parsed-account mirrors were
also searched for Co-operative Bank and GSIB. They exposed statement values
but no verbatim published ROE, ROA or RoTE. Any ratios calculated by the mirror
itself were treated only as search leads and excluded under the no-backsolving
rule, so neither bank's status changed.

## Current collection state

The seven raw batches contain **378 records across 140 banks**:

- `300dpi`: 331
- `ocr_lead`: 40
- `press_release`: 3
- unresolved/null: 4

The curated store remains unchanged at **157 records across 60 banks**.
