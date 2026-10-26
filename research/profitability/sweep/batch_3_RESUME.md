# batch_3 sweep — cold-resume handoff

Output: `research/profitability/sweep/batch_3.jsonl` (append-only, one record per
bank-year). The jsonl IS the checkpoint: whatever is on disk stands alone.

Scratchpad (PDFs/renders, never in repo):
`/private/tmp/claude-501/-Users-armaan-code-katalysis/20f20984-c24d-413e-b487-68c0d0793341/scratchpad/sweep/b3`

## Status

- RESEARCHED/CHECKPOINTED (20/20): all batch banks now have at least one JSONL checkpoint.
- VERIFIED/SETTLED AT BANK LEVEL (20/20): all batch banks.
- UNRESOLVED OR AWAITING 300 DPI VERIFICATION (0/20): none.

## 2026-10-11 continuation

- HSBC UK BANK PLC rechecked against HSBC's live subsidiary-reporting index. The FY2025 own-entity ARA is now available at the official URL `.../2025/annual/pdfs/hsbc-uk-bank-plc/260225-annual-report-and-accounts-2025.pdf` (128 pages, `application/pdf`). Four exact text-layer leads appended: RoE 15.8%/16.5% and RoTE 19.2%/20.2% for FY2025/FY2024, with the report's full definitions and reconciliation. The screenshot endpoint failed, so these are correctly labelled `ocr_lead`, not findings. HSBC UK remains bank-level settled because its earlier FY2024 records in this file are already 300 dpi verified.
- RBS has a robust official-ARA negative: zero whole-document return-measure hits and the complete p.4 key-metrics table has no return; NatWest Group and RBS International were excluded as different perimeters. Because no 300 dpi render was available, this is recorded `unresolved`, not `publishes_none`.
- STREAMBANK has a robust official-FY2025-ARA negative: whole-document return searches are clean and the full CFO KPI table has no return ratio. Because no 300 dpi render was available, this is recorded `unresolved`, not `publishes_none`.
- VIDA has a robust official-FY2025-ARA negative: the only return-on-equity wording is a future ambition to drive a higher return in 2026; there is no reported value, and the report's five actual performance metrics contain no return ratio. Because no 300 dpi render was available, this is recorded `unresolved`, not `publishes_none`.
- TURKISH BANK UK exact text-layer ROE leads: FY2022 4.22%, FY2023 9.41%, FY2024 2.61%, plus FY2021 (0.12)% from the FY2022 comparative. The reports give no definition and separately label a PBT/equity ratio, so comparability remains false. All four are `ocr_lead` pending 300 dpi verification. The official FY2025 edition is a 66-page scan with no browser text layer; local network restrictions prevented OCR/300dpi download, so FY2025 is explicitly unresolved rather than guessed.
- PERENNA remains unresolved after first-class checks of the official customer/intermediary sites and Companies House. The FY2025 76-page own filing is an image-only scan behind a redirect the browser cannot fetch; local network is disabled. Existing workbook notes identify CET1/leverage on p.1 but are not a profitability-specific full-document search, so no absence claim was made.
- SCHRODER remains unresolved after checking Schroders' official reporting centre and Companies House. The official site carries parent-group reports, not Schroder & Co. Limited's accounts; the own-entity Companies House filing is an inaccessible image-only scan. Parent figures were excluded and no absence claim was made.

## Continuation counts (2026-10-11)

- 14 new JSONL records appended in this continuation: 8 `ocr_lead` figures (HSBC UK 4; Turkish Bank UK 4) and 6 unresolved records (RBS, StreamBank, Vida, Turkish Bank UK FY2025, Perenna, Schroder). The pre-existing HSBC unresolved is superseded for discovery purposes by the four new leads, but only the earlier FY2024 300 dpi records are presentation-ready.
- Full batch verification census: 30 `300dpi`, 8 `ocr_lead`, 7 null/unresolved. There are no non-standard verification states and no text-only negative is marked `publishes_none`.

## Method in force
Verify %PDF magic + Content-Type; prefer most recent ARA; text-layer grep for
`[Rr]eturn on|RoTE|ROE|ROA|return on average`; render the target page at
300 dpi and READ the image before recording any figure. Scans (zero-byte text
layer): 150 dpi + tesseract to LOCATE the KPI page only, then 300 dpi to read.
Entity discipline: a group/parent figure is `excluded`, never the bank's own.
`publishes_none` is a finding and must be recorded with evidence.

## 2026-10-12 cache-first unresolved retry

- HSBC UK BANK PLC: FY2025 RoE 15.8% and RoTE 19.2% were promoted from OCR leads after 300 dpi reads of the headline table and reconciliation in the exact official report. The FY2025 edition's FY2024 comparatives (16.5%/20.2%) were confirmed but not duplicated because the FY2024 own-edition records already exist.
- TURKISH BANK UK: FY2025 Return on Equity `(2.01)%` was recovered from the exact official image-only report. The FY2021-FY2024 leads were also visually verified and promoted to `300dpi`.
- RBS, STREAMBANK and VIDA: their exact official reports were whole-report searched and decisive KPI/performance pages read at 300 dpi; each now has a verified `publishes_none` finding.
- PERENNA and SCHRODER: the exact cached Companies House scans and existing full OCR layers were recovered. Whole-report searches plus 300 dpi reads of their complete KPI disclosures support `publishes_none` findings.
- Final batch census: 42 records / 20 banks; all 42 are `300dpi`, with 28 published figures and 14 `publishes_none` findings. Zero unresolved and zero OCR leads remain.
- No bank worksheet, build script, curated store, extract, CSV or XLSX was changed.
