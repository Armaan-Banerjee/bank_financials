# Goldman Sachs International Bank FY2025 profitability audit (2026-10-13)

## Outcome

**Classify Goldman Sachs International Bank (GSIB) FY2025 as
`publishes_none`.** The exact 64-page annual report publishes no numeric return
on equity (ROE), return on assets (ROA), return on tangible equity (RoTE), or
synonymous profitability-return measure. No value should be calculated from
the published profit, assets or equity balances.

This is a collection-only finding. No worksheet, script, curated store, batch
JSONL, extract or deliverable was changed.

## Exact source and perimeter

- The source inspected is **Goldman Sachs International Bank (unlimited
  company), company 01122503, Annual Report for the financial year ended
  31 December 2025**. Companies House lists the filing as 64 pages, filed
  26 April 2026: [official filing history](https://find-and-update.company-information.service.gov.uk/company/01122503/filing-history),
  [exact filing document](https://find-and-update.company-information.service.gov.uk/company/01122503/filing-history/MzUxNzc2NzE5OGFkaXF6a2N4/document?format=pdf&download=0).
- The downloaded report's cover gives the same legal name, company number and
  reporting date (PDF page 1). Its SHA-256 is
  `b615a27ab709f7a0bf58d4ff8d2f78a7d4ff97ed4dda72e23a842a502472c0f0`.
- This is the exact bank perimeter, including its Frankfurt and Johannesburg
  branches, rather than Goldman Sachs International or the wider Goldman Sachs
  Group. The auditor describes the bank and its branches as one audit component
  (printed page 16; PDF page 17). The strategic report separately explains that
  GSIB's results are included in the wider parent's consolidated U.S. GAAP
  statements; parent or affiliate return measures are therefore excluded
  (printed page 2; PDF page 3).

## Evidence

The image-only report was OCR'd across all 64 pages and searched for `return`,
`return on equity`, `return on assets`, `return on tangible equity`, `ROE`,
`ROA`, `RoTE`, `average assets`, `average equity`, `tangible equity`, `yield`,
`ratio`, `margin`, `profitability` and `performance indicator`, including
likely OCR variants. The result was then checked against 300-dpi renders of the
decisive pages.

- The directors explicitly identify **profit for the year, total assets and
  CET1 capital** as the bank's key performance indicators. They report profit
  of $488 million for 2025 (up 7%), total assets of $110.15 billion and CET1
  capital of $4.95 billion, but no profitability return ratio (printed page 2;
  PDF page 3 of the [exact filing](https://find-and-update.company-information.service.gov.uk/company/01122503/filing-history/MzUxNzc2NzE5OGFkaXF6a2N4/document?format=pdf&download=0)).
- The primary statements publish profit of $488 million for 2025 and $458
  million for 2024 (printed page 20; PDF page 21), total assets of $110.147
  billion and $89.783 billion and shareholder's equity of $5.075 billion and
  $4.488 billion (printed page 21; PDF page 22), and the components of equity
  (printed page 22; PDF page 23). None of these pages publishes ROE, ROA or
  RoTE. Deriving a ratio from them would violate the no-backsolving rule.
- The report's qualitative references to the wider GS Group seeking long-term
  shareholder “returns” and higher “margins and returns” are strategy wording,
  not numeric GSIB measures (printed page 7; PDF page 8). Other numeric ratios
  and yields in the notes concern credit-loss allowances, tax, regulatory
  capital or valuation inputs; they are not profitability-return measures.

## Collection decision

Replace the existing GSIB FY2025 unresolved/null acquisition gap with a
verified **`publishes_none`** finding when the batch collation is updated. Do
not add a numeric return record, do not calculate one from the statements, and
do not substitute a ratio for Goldman Sachs International, Goldman Sachs Group
UK Limited or The Goldman Sachs Group, Inc.

