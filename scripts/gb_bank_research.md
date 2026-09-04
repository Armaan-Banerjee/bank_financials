# WF-024 — GB Bank Limited source notes

## Entity and reporting basis

- GB Bank Limited: Companies House company `10702260`, PRA FRN `850286`.
- Companies House shows the entity active and accounts made up to 30 September 2025. The 2025 accounts were filed on 6 January 2026.
- GB Bank's 2025 Pillar 3 report states that figures at 30 September 2025 are prepared on a solo basis. It also notes PRA permission, backdated to 1 October 2025, for an individual-consolidation method including SilverRock Financial Services Ltd going forward.
- The bank states that it publishes Pillar 3 annually and is small and non-complex under CRR Article 433b.

## Official sources

- Companies House filing history: https://find-and-update.company-information.service.gov.uk/company/10702260/filing-history
- GB Bank Pillar 3 archive: https://www.gbbank.co.uk/pillar-3-disclosure/
- 2022 Pillar 3 report: https://www.gbbank.co.uk/download/4416/?tmstv=1760374739
- 2023 Pillar 3 report: https://www.gbbank.co.uk/download/4420/?tmstv=1760374863
- 2024 Pillar 3 report: https://www.gbbank.co.uk/download/4423/?tmstv=1760374514
- 2025 Pillar 3 report: https://www.gbbank.co.uk/download/5065/?tmstv=1766062359
- GB Bank annual report page: https://www.gbbank.co.uk/annual-reports/

## Extracted annual KM1 values

Amounts are £'000. FY2024 is the shortened nine-month period ended 30 September 2024; the other periods end 31 December except FY2025, which ends 30 September 2025.

| Period | CET1/Tier 1/Total capital | RWA | Capital ratio | Leverage ratio | LCR | NSFR |
|---|---:|---:|---:|---:|---:|---:|
| FY2025 | 104,969 | 548,458 | 19.14% | 4.97% | 210% | 191% |
| FY2024 | 69,270 | 151,536 | 45.71% | 9.26% | 306% | 538% |
| FY2023 | 19,299 | 34,184 | 56.46% | 39.60% | 416% | 3,375% |
| FY2022 | 22,096 | 9,434 | 234.21% | 94.25% | 20,091% | 2,061.89% |
| FY2021 | 16,586 | 4,112 | 403.37% | 94.21% | 9,999.99% | 978.24% |

The 2023 report prints RWA of £2,735k while its 56.46% ratio implies approximately £34,184k; the 2024 report's 2023 comparative prints £34,184k. The build uses £34,184k and documents the source inconsistency.

The 2025 report also includes an individual-consolidation appendix with different 30 September 2025 values. The build uses the main solo table because that is the stated basis for the period.

## Cash flow treatment

Cash-flow data was backfilled in a 2026-09-03 follow-up pass (ST-019), transcribed from each
year's own Statement of Cash Flows / Consolidated statement of cash flows in the same 5
Companies House filings used for the other statement sheets (all scanned/image-only, visually
transcribed): FY2021 p.23, FY2022 p.27, FY2023 p.28, FY2024 p.28 (9-month period), FY2025 p.47
(Consolidated). All 5 years have a disclosed statement, so no year was left blank. See
`scripts/build_gb_bank.py`'s `cash_flow_rows` / `add_cash_flow_sheet(...)` sources_text for two
genuine (documented, not force-reconciled) discrepancies: a £2k FY2025-opening-vs-FY2024-closing
cash mismatch, and a relabelled £29,291k FY2024 line between that year's own report and FY2025's
comparative column.
