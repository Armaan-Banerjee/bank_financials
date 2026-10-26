# RESUME — Coutts / Aldermore / Lloyds profitability discrepancies

Task: resolve 3 ROE/ROA discrepancies vs delivered workbooks. READ-ONLY on banks/ and scripts/.
Checkpoint file: `coutts_aldermore_lloyds.jsonl` (same dir). This file = cold-resume state.

## Documents on disk
Dir: `/private/tmp/claude-501/-Users-armaan-code-katalysis/20f20984-c24d-413e-b487-68c0d0793341/scratchpad/pdf/`
| file | what | text layer | index offset |
|---|---|---|---|
| lloyds2024.pdf (185pp) | Lloyds Bank plc ARA 2024 | native, `lloyds2024.txt` | PDF p = printed folio + 2 |
| lloyds2025.pdf (175pp) | Lloyds Bank plc ARA 2025 | native, `lloyds2025.txt` | PDF p = printed folio + 1 |
| coutts2025.pdf (77pp) | Coutts & Company ARA 2025 (CH co 00036695) | SCAN — OCR'd to `coutts2025_ocr.txt` + `coutts2025_ocr.pdf` | TBD (see below) |
| aldermore2025.pdf (115pp) | Aldermore Bank PLC full accounts y/e 30 Jun 2025 (CH co 00947662) | SCAN — OCR'd to `aldermore2025_ocr.txt` | TBD |

OCR text is for NAVIGATION ONLY. Every figure must be read off `pdftoppm -r 300 -f N -l N -png`.

## Plan / status
1. [DONE] Read workbook source-citation cells (Balance Sheet + P&L) for all 3 banks.
2. [DONE] LLOYDS: inputs verified on 300dpi images; outside figure fully explained. CLOSED except one loose end (see below).
3. [PART] COUTTS: outside 21.7% identified as NatWest Private Banking SEGMENT RoE FY2025. Coutts' OWN RoE 17.3% found in OCR — must verify on image + read footnote definition + verify profit/equity/assets on image.
4. [PART] ALDERMORE: outside 7.7% identified as Aldermore GROUP plc FY2025 RoE. Must get Group annual report page + definition; verify Bank-solo inputs on image.
5. [TODO] Final report via SubagentHandback.

## Bank 1 — LLOYDS BANK plc, FY2024 — ESSENTIALLY DONE
Inputs CONFIRMED digit-for-digit on 300dpi images:
- Profit for the year 3,486 — ARA2024 PDF p.77 / printed p.75, Consolidated income statement
- Total assets 611,213 (2023: 605,405); Total equity 39,747 (2023: 40,431) — PDF p.79 / printed p.77
- Also on image, PDF p.147 / printed p.145 "Bank balance sheet" (unconsolidated company):
  total assets 430,252 (2023: 419,441); Shareholders' equity 45,996 (2023: 46,348);
  Total equity 51,688 (2023: 51,366); footnote: Bank profit after tax 4,897 (2023: 4,660).
Lloyds Bank plc publishes NO ROE/RoTE/ROA in ARA2024 or ARA2025 (full-text search: zero genuine hits).
thebanks.eu id 14376 explained exactly:
  - their Total Assets 430.25bn (+2.58%) = Bank-only (unconsolidated) 430,252 vs 419,441
  - their Total Equity 51,688 (+11.52%) = Bank-only 2024 TOTAL equity vs Bank-only 2023 SHAREHOLDERS' equity 46,348 (inconsistent across years)
  - their Annual Profit 3,486 = GROUP consolidated profit
  - ROA 0.82% = 3,486 / avg(430,252; 419,441)=424,846.5 -> 0.8205%
  - ROE 7.11% = 3,486 / avg(51,688; 46,348)=49,018 -> 7.1117%
OPEN: their "Net Income (2023): 3,479" matches neither Group (5,207) nor Bank (4,660). Unexplained.

## Bank 2 — COUTTS & COMPANY, FY2025 — OPEN
Workbook inputs (not yet image-verified): profit 259.0, equity 1,544.0 (prior 1,497.0), assets 61,695.0.
Workbook cites Coutts ARA 2025 pp.53-55 (printed folios).
FOUND IN OCR (needs image verification):
- OCR page 2: "At the end of 2025, we delivered a return on equity of 17.3% and"
- OCR page 3: KPI table row "Return on Equity (RoE) (1) 17.3% 13.5% - na 3.8%"  <- footnote (1) = definition, MUST READ
Outside 21.7% = NatWest Group PRIVATE BANKING & WEALTH MANAGEMENT segment RoE FY2025 (op profit GBP394m; FY2024 16.3%).
STILL TO DO: 300dpi images of OCR pp.2-3 (KPI/strategic report) and of the balance sheet / income statement pages.

## Bank 3 — ALDERMORE BANK PLC, FY2025 (y/e 30 Jun 2025) — OPEN
Workbook inputs (not yet image-verified): profit 163.2, equity 1,514.6 (prior 1,371.8), assets 20,618.2.
Workbook cites CH full accounts y/e 30 Jun 2025, p.53 (P&L) and p.54 (SOFP) printed folios.
OCR hits: page 8 "Key performance indicators" table; page 114 "Return on equity (“RoE”)" (glossary/definition).
Outside 7.7% = Aldermore GROUP plc consolidated FY2025 (PBT 193.5, PAT 141.1; FY2024 11.8%).
STILL TO DO: image-verify Bank-solo p.53/p.54; read OCR p.8 KPI table + p.114 definition on image; get Aldermore Group plc FY2025 annual report page for the 7.7% + its definition.
SEPARATE DEFECT ALREADY SPOTTED (report it): workbook Balance Sheet row 37 "Total liabilities" FY2025 = 17050.8 but liabilities sum to 19103.6 and 20618.2 - 1514.6 = 19103.6. FY2024 and earlier tie. Looks like a transcription slip in the FY2025 Total liabilities cell only. Assets/equity/profit unaffected.
