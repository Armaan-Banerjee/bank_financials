# Batch 4 profitability sweep checkpoint

Collection only. No bank or profitability workbook, curated store, extraction, CSV, XLSX or build script is touched.

## Progress

- Settled/checkpointed at the bank level: **20 of 20 banks**.
- Raw records: **59**.
- Published figures/leads: **49**; verified `publishes_none`: **10**; unresolved current-report records: **0**.
- Evidence state: **23 `300dpi`**, **34 `ocr_lead`**, **2 official `press_release`**, **0 null/unresolved**.
- The 23 `300dpi` records comprise 13 figures and ten verified no-publication findings.

## 12 October unresolved-bank retry

All 13 previously unresolved banks were retried from the local primary-source cache. Results and citations are in [`unresolved_retry_batch4_2026-10-12.md`](unresolved_retry_batch4_2026-10-12.md).

New verified figures:

- Hampshire Trust Bank Bank columns, FY2025/FY2024: RoTE **16.7%/16.9%**, required-equity return **22.4%/25.6%**, post-tax ROE **14.9%/15.2%**.
- Monument Bank FY2024/FY2023: ROE **-22%/-44%**.
- UBA UK FY2024/FY2023: pre-tax ROE **16%/24%**, return on total assets **2.75%/2.93%**.
- Weatherbys FY2025: consolidated Group ROE **8.9%**.

Verified `publishes_none`: Aldermore, Bank Saderat, Charity Bank, J.P. Morgan Europe, Nomura Bank International, Persia International Bank and RCI Bank UK.

## Remaining acquisition list

None. The two exact FY2025 reports were supplied and fully reviewed on 13
October 2026.

## Quality notes

- HTB's report prints Group and Bank columns side by side. The six new values are the **Bank** columns matching the workbook perimeter.
- Weatherbys' 8.9% matches the consolidated workbook perimeter, but excludes exceptional items and AT1 capital.
- Aldermore Group's 7.7% FY2025 RoE remains excluded from Aldermore Bank PLC's solo perimeter.
- Co-operative Bank's separate CRD V page describes an ROA formula, but the
  exact FY2025 annual report publishes no numeric ROA and no value was inferred.
- No value was inferred, backsolved or imported from an aggregator.
- EFG's FY2023 `10.5%` versus `105 bps` discrepancy remains a separate provisional-record QA issue.

## 13 October round-3 recovery

- TANDEM is now a positive `publishes_none` finding. The exact 59-page
  Company-only FY2025 report had already been fully OCR'd and cross-checked
  against rendered page images in the Tandem source workflow; the renewed
  report-wide/source-trail search found no explicit ROE, ROA or RoTE. Tandem
  Money Limited group Pillar 3 metrics remain excluded.
- CO-OPERATIVE BANK and MONUMENT BANK were subsequently closed as verified
  exact-report `publishes_none` findings. Co-op's KPI page has no return ratio;
  its apparent ROA hit is pension-plan assets. Monument's complete FY2025 APM
  section contains EBITDA, NIM and cost/income, but no ROE/ROA/RoTE.
- No worksheet, build script, curated store, extract, CSV/XLSX or deliverable
  was changed.

## Next actions

1. Separately render and adjudicate the 34 pre-existing `ocr_lead` records before any curated merge.
2. Reconcile the EFG FY2023 cross-edition discrepancy.
