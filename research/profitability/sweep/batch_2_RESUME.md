# batch_2 sweep — cold resume handoff

Output: `research/profitability/sweep/batch_2.jsonl` (append one JSON object per bank-year).
Scratchpad (PDFs/renders): `/private/tmp/claude-501/-Users-armaan-code-katalysis/20f20984-c24d-413e-b487-68c0d0793341/scratchpad/sweep/b2`

## Done
1. AFIN BANK — publishes_none (FY2024), 300dpi
2. ATOM BANK — PUBLISHES RoTE 10% FY2026 (y/e 31 Mar 2026), 300dpi, no stated
   definition. FY2025 publishes_none is now confirmed at 300dpi against the official bank-hosted born-digital report; the former ocr_lead has been replaced.
3. BANK OF SCOTLAND — PUBLISHES post-tax return on average total assets
   0.39% FY2025 / 0.25% FY2024, 300dpi. PERIMETER WARNING: the figure is the
   consolidated Group; the workbook is the Bank unconsolidated. No ROE published.
4. BLME — PUBLISHES Pre-tax return on equity: FY2025 0.7%, FY2024 3.4%
   (own edition) vs 3.6% (restated in the FY2025 edition — both recorded,
   not reconciled), FY2023 1.7% restated. 300dpi. No stated definition.

5. CASTLE TRUST CAPITAL — publishes_none (FY2025, y/e 30 Sep), 300dpi
6. CLOSE BROTHERS — PUBLISHES Return on opening equity 8.7% FY2025 / 11.1%
   FY2024 and Return on net loan book 2.1% / 2.2%, 300dpi. NO definition
   stated anywhere in the document; basis (adjusted vs statutory) unresolved.

7. DB UK BANK — PUBLISHES Return on Assets 0.68% FY2025 / 0.80% FY2024,
   300dpi, definition verbatim (PBT / year-end total assets). No ROE.
8. GATEHOUSE BANK — PUBLISHES Return on tangible equity (13.28)% FY2025 /
   4.15% FY2024, 300dpi, definition verbatim (PAT / average tangible equity).

9. HABIB BANK ZURICH — PUBLISHES ROE 8% / ROA 0.7% FY2025 (FY2024 9% / 0.9%),
   300dpi, no definitions given, figures rounded.

10. ITAU BBA INTERNATIONAL — completed before this resume update; consolidated-group ROE/ROA records retained with explicit perimeter mismatch.
11. KROO BANK — publishes_none (FY2024), 300dpi.
12. TSB — PUBLISHES ROTE 12.6% FY2025 / 10.6% FY2024 and Post-tax return on assets 0.55% / 0.44%, 300dpi. Neither denominator is defined; tangible-equity and undefined asset basis mean neither is marked comparable.
13. NATIONAL WESTMINSTER BANK PLC — publishes_none (FY2025), 300dpi. NatWest Group plc's RoTE is excluded as a different parent perimeter.
14. PARAGON — PUBLISHES Return on assets 0.91% FY2025 / 0.93% FY2024 restated, 300dpi, with verbatim calculation (PAT / year-end total balance sheet). Parent-group RoTE excluded.
15. SANTANDER FINANCIAL SERVICES — publishes_none (FY2025), 300dpi. Its own report explicitly says KPIs are not set, monitored or managed at Company level.
16. STATE BANK OF INDIA UK — FY2025 publishes_none, 300dpi (new KPI set drops returns). FY2024 edition publishes ROE 9.25% / 8.61% / 5.92% for FY2024/23/22 and ROA 1.27% / 1.15% / 0.84%, with verbatim definitions; neither matches the computed denominator.
17. VANQUIS — publishes_none (FY2025), 300dpi. Vanquis Banking Group plc's 2.3% statutory RoTE is explicitly excluded as parent-group perimeter.
18. RBC EUROPE — PUBLISHES Return on assets ratio (0.08)% FY2025 / 0.09% FY2024, 300dpi. No definition is supplied; the report is RBC Europe Limited company-level.
19. METRO BANK — PUBLISHES Return on tangible equity 5% FY2025 / (22)% FY2024 / 7% FY2023, 300dpi, with its verbatim definition (statutory PAT attributable to shareholders / average tangible equity). The exact Metro Bank PLC report is bank-consolidated while the workbook statements are Company/standalone, so all three records are perimeter-mismatched and non-comparable. Metro Bank Holdings PLC's 6% / (23)% / 4% parent series is explicitly excluded.

## Remaining
None. Batch coverage is complete and no unresolved or OCR-lead record remains.

## Current validation (2026-10-13)
- 50 valid JSONL records covering all 20 banks in `batch_2.json`; no missing or extra banks.
- All 50 records are verified at 300 dpi.
- 41 resolved measure records, 9 `publishes_none` records, and no unresolved record.
- Atom FY2025 is now a 300 dpi `publishes_none` finding; no record retains the former unverified lead status.

## 2026-10-12 unresolved retry

- METRO BANK was retried cache-first. The official bank-site cache contains Metro Bank Holdings PLC's FY2025 report and its 6%/(23)%/4% RoTE series was visually confirmed at 300 dpi, but that is the listed holding-company consolidated perimeter, not a safe substitute for the exact Metro Bank PLC statutory filing described in the unresolved record.
- The remaining required document is **Metro Bank PLC Annual Report and Accounts 2025**, company 06419578, Companies House document `MzUzODAzNTg0NWFkaXF6a2N4` (163 pages): https://find-and-update.company-information.service.gov.uk/company/06419578/filing-history/MzUzODAzNTg0NWFkaXF6a2N4/document?format=pdf&download=0 . Supply that exact PDF to resolve the final batch-2 record.
- At the end of that retry, batch 2 still stood at 48 records / 20 banks: 47
  `300dpi`, one explicit unresolved and zero OCR leads. The later round-3
  recovery below supersedes that state.

## 2026-10-13 round-3 recovery

- A faithful preserved copy of the exact 163-page Metro Bank PLC filing was
  rendered and its KPI row read at printed p.11/PDF p.12. It publishes RoTE of
  **5% / (22)% / 7%** for FY2025/24/23. The former unresolved placeholder was
  replaced by three `300dpi` records.
- Batch 2 is now 50 records / 20 banks: all 50 `300dpi`, no unresolved and no
  OCR leads. No worksheet, curated store or downstream deliverable was changed.
