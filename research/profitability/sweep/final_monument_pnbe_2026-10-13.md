# Final uploaded-report review — Monument Bank and PNB Europe (2026-10-13)

## Scope and method

This collection-only review used the exact uploaded FY2025 statutory reports
for Monument Bank Limited and Philippine National Bank (Europe) Plc. It did
not modify worksheets, build scripts, the curated profitability store or any
downstream deliverable. Explicit bank-level return measures were collected;
no ratio was inferred from financial statements.

The source files were searched report-wide. Decisive pages were then rendered
from the original PDFs at 300 dpi and visually read. The temporary uploaded
copies were deleted after the findings were recorded, as requested by the
user; SHA-256 hashes below preserve source identity.

## Monument Bank Limited

- Source: [Monument Bank Limited Annual Report and Financial Statements 2025](https://cdn.prod.website-files.com/6435124ea79f72c265f72807/6ab68b85f380864b01e45564_Monument%20Bank%20Limited%20-%202025%20Annual%20Report.pdf), company 10921940, 84 PDF pages.
- Uploaded-file SHA-256: `1be4bc9c0557ea884f70fb5b05606d26c14f5b1ee6687e80508c9e2c9ea0aafb`.
- Result: **verified `publishes_none` for FY2025**. The report contains no
  explicit ROE, ROA or RoTE value.
- Evidence: report-wide searches covered `return on`, `ROE`, `ROA`, `RoTE`,
  `tangible equity`, `average equity`, `average assets`, KPI and performance
  headings. The complete Alternative Performance Metrics section on printed
  p.13/PDF p.13 was visually checked at 300 dpi and contains only EBITDA, Net
  Interest Margin and cost/income ratio. Printed p.14/PDF p.14 then defines
  CET1, leverage, LCR and NSFR, with no profitability return.
- Historical distinction: the already-collected FY2024 report's ROE of -22%
  (and FY2023 comparative of -44%) remains valid. The FY2025 edition simply no
  longer publishes ROE, so those older records do not establish a FY2025 value.

## Philippine National Bank (Europe) Plc

- Source: [Philippine National Bank (Europe) Plc FY2025 full accounts](https://find-and-update.company-information.service.gov.uk/company/02939223/filing-history/MzUyNjIwMTYzNWFkaXF6a2N4/document?format=pdf&download=0), company 02939223, 45 PDF pages.
- Uploaded-file SHA-256: `65f0e427155b6588c7efda528ae9334148acaeaa61e4168fffb02524ba46d428`.
- Result: the exact bank's Strategic Report explicitly publishes **return on
  assets of -3.5% for FY2025 and +0.1% for FY2024** on printed p.3/PDF p.5.
- Verbatim substance: the report says total assets were £13,973k (2024:
  £14,962k), resulting in a negative return on assets of 3.5% (2024: positive
  return of 0.1%). The same page states a 2025 net loss of £492k and 2024
  income of £11k.
- Definition/comparability: no formal formula is stated. The paragraph pairs
  each return with total assets, but does not specify an average-assets
  denominator. Both records are therefore conservatively marked
  `definition_verbatim: false` and `comparable_with_computed: false`.
- Verification: the image-only report was OCR'd in full for navigation and the
  decisive original page was rendered and visually read at 300 dpi. Other
  return hits concern interest-earning assets or pension plan assets; no bank
  ROE or RoTE was found.

