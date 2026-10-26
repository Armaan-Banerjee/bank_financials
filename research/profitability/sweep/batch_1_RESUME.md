# batch_1 sweep - cold-resume handoff

Output: `research/profitability/sweep/batch_1.jsonl` (append-only, one record per
bank-year). Checkpoint is the jsonl itself: whatever is on disk stands alone.
**64 records written; batch complete.**

## Status (updated after every bank)

- DONE (20/20): ABC INTERNATIONAL BANK, ARBUTHNOT LATHAM, BANK OF IRELAND UK, BIRMINGHAM BANK, CAMBRIDGE AND COUNTIES BANK, CLEARBANK, CYNERGY BANK, FIRSTBANK UK, GULF INTERNATIONAL BANK UK, HSBC BANK PLC, INVESTEC BANK PLC, KINGDOM BANK, METHODIST CHAPEL AID, NATIONAL BANK OF KUWAIT INTERNATIONAL, OXBURY, RATHBONES INVESTMENT MANAGEMENT, SANTANDER, STARLING, TRIODOS, UNITY TRUST
- IN PROGRESS: none
- REMAINING (0): none

## Latest checkpoint

- KINGDOM BANK: settled `publishes_none` from the bank's official Oversight index and Annual Report and Accounts 2025. Official PDF response is `application/pdf`, file begins `%PDF`, 79-page image-only scan. The complete report was OCR-swept for navigation/coverage and the exhaustive KPI table at printed p.15 (PDF p.17) was read at 300 dpi. It contains CET1, leverage, LCR, NIM, lending and arrears KPIs, but no ROE/RoTE/ROA.
- METHODIST CHAPEL AID: settled. The exact official FY2025 report was recovered from `research/doc_cache` and visually checked at 300 dpi. Printed p.10/PDF p.12 publishes Return on Assets of 1.0% for the nine months ended 30 September 2025 (FY2024 comparative: 1.1%). No denominator definition is given, so it remains non-comparable. The earlier FY2025 unresolved record was replaced.
- NATIONAL BANK OF KUWAIT INTERNATIONAL: official NBKI FY2025 report publishes entity-specific Return on shareholders' equity of 6.37% (FY2024: 6.49%) at printed p.3/PDF p.4. It says only that the KPI is derived from the financial statements and does not define denominator timing, so both records are non-comparable. The parent NBK Group's 13.4% ROAE and 1.33% ROAA were explicitly excluded as a different perimeter.
- OXBURY: settled `publishes_none`. The official disclosure index shows FY2024 as the newest annual report and FY2025 only as Pillar 3. The Annual Report's exhaustive Company KPI table was visually checked and its full 80-page text layer searched; the locally retained FY2025 Pillar 3 was also searched. Neither publishes ROE/ROA/RoTE.
- RATHBONES INVESTMENT MANAGEMENT: four entity-only records from the newest FY2025 Companies House accounts: average net operating basis point return 79.7bps (FY2024: 75.7bps), plus the narrower fee/commission basis point return on FUMA 70.4bps (FY2024: 65.2bps). Both definitions concern client funds under management/administration, not Company equity/assets, and all are non-comparable. Rathbones Group consolidated metrics were excluded.
- SANTANDER: official Santander UK plc FY2025 report publishes Return on assets of 0.40% (FY2024: 0.36%), explicitly defined as profit after tax divided by average total assets. Both match the project's computed ROA basis. RoTE appears only as a future remuneration condition, not an actual bank return figure; holding-company and Banco Santander metrics were excluded.
- STARLING: eight figure records from Starling Bank Limited's official FY2025 report: statutory ROCE 26.7% (FY2024 51.5%), statutory ROTE 17.9% (31.5%), underlying ROCE 36.8% (51.5%), and underlying ROTE 24.7% (31.5%). Definitions and calculations were read at 300 dpi on the APM pages (printed/PDF pp.220 and 222), after whole-report text search. None is directly comparable: ROCE uses average minimum regulatory capital requirements; ROTE uses average tangible equity; the underlying versions also adjust PAT. One additional `excluded` FY2026 record captures the successor parent Starling Group Holdings Limited's 24.9% post-tax ROCE from its official investor page, so that different perimeter is explicit rather than silently substituted for Starling Bank Limited.
- TRIODOS: official Triodos Bank UK Limited FY2025 report publishes Return on equity 6.9% (FY2024 2.8%). The entity-only UK Bank report says PAT was £13.9m (£5.5m) but does not define equity denominator timing/composition, so both records are non-comparable. The bank-site PDF is `application/pdf`; its matching 108-page Companies House copy begins `%PDF-1.1`, is image-only, was OCR-swept solely for navigation/coverage, and the KPI page at printed/PDF p.14 was read at 300 dpi.
- UNITY TRUST: five directly comparable ROE records from the official FY2025 report's audited five-year KPI chart: FY2025 16.8%, FY2024 25.6%, FY2023 33.0%, FY2022 19.6%, FY2021 9.7%. The report defines RoE as PAT as a proportion of average shareholder equity. The official investor index independently headlines FY2025/FY2024; the 84-page born-digital bank-site PDF is `application/pdf`, begins `%PDF-1.7`, and KPI p.8 plus glossary p.82 were each read at 300 dpi after whole-report search.

## Method in force
See the dispatch brief: verify %PDF magic, prefer most recent ARA, text-layer
grep for `[Rr]eturn on|RoTE|ROE|ROA`, render target page at 300 dpi and READ
the image before recording any figure. Entity discipline: a group figure is
`excluded`, never the bank's figure. `publishes_none` is a FINDING.

Scratchpad (PDFs, renders): `/private/tmp/claude-501/-Users-armaan-code-katalysis/20f20984-c24d-413e-b487-68c0d0793341/scratchpad/sweep/b1`

## 2026-10-12 unresolved retry

- Batch 1 now has no unresolved or OCR-lead records: 64 records across 20 banks, comprising 63 `300dpi` and one official `press_release` verification.
- No bank worksheet, build script, curated store, extract, CSV or XLSX was changed.
