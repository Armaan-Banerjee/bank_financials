# RESUME — Al Rayan / Northern Bank / Starling profitability discrepancies
Last updated: 2026-10-08, mid-task.
Working dir /Users/armaan/code/katalysis. READ-ONLY on banks/ and scripts/.
Scratchpad: /private/tmp/claude-501/-Users-armaan-code-katalysis/20f20984-c24d-413e-b487-68c0d0793341/scratchpad
Findings log: alrayan_northern_starling.jsonl (same dir)

## Documents already fetched (all under scratchpad/prof/)
| file | doc | pages | text layer? | PDF page -> printed folio |
|---|---|---|---|---|
| ar24.pdf | Al Rayan Bank PLC AR & FS 2024 | 82 | YES | PDF n -> folio n-1 (PDF 10 = p.9, PDF 40 = p.39, PDF 41 = p.40) |
| ar25.pdf | Al Rayan AR & FS 2025 (Companies House scan) | 87 | NO (scanned) | PDF n -> folio n-1 (PDF 9 = p.8 KPI table) |
| ar22.pdf | Al Rayan AR & FS 2022 (Companies House scan) | 74 | NO (scanned) | offset NOT yet established |
| nb24.pdf | Northern Bank Ltd AR & FS 2024 | 98 (99 text pages) | YES | 2-UP LANDSCAPE A3. PDF 13 = printed pp.24-25; PDF 65 = printed pp.128 (left) & 129 (right); PDF 66 = printed p.130-131 (SOCE) |
| st24.pdf | Starling Bank Ltd Annual Report 2024 (ye 31 Mar 2024) | 235 | YES | not yet established |
| st25.pdf | Starling Bank Ltd Annual Report 2025 (ye 31 Mar 2025) | 226 | YES | not yet established |
Page images already rendered: ar10-10.png, ar40-40.png, ar41-41.png, a25k-09.png(+a25k_kpi.png crop),
nb13-13.png, nb65-65.png(+_L/_R halves), nb66-66.png(+_L/_R), t25_sheet.png, t22_sheet.png (90dpi contact sheets pp.5-16).

## Status by bank
### 1. AL RAYAN — ESSENTIALLY DONE (confirmation only; coordinator resolved the arithmetic)
- CONFIRMED: AR2024 printed p.9 (PDF 10) "Key financial performance indicators (KPIs)" prints
  **Return on equity 11.40% (2023: 16.89%)**, Basis of Calculation: *"The ratio of profit for the year
  (before tax) to average equity, expressed as a percentage."* Read on 300dpi image.
  Same table: PBT 23.47m/30.61m, PAT 17.72m/23.03m, cost:income 58%/53%, CET1 16.03%/17.36%, LCR 746%/786%.
- CONFIRMED: AR2025 printed p.8 (PDF 9) same table prints **ROE 10.47% (2024: 11.40%)**, PBT 23.59m/23.47m,
  PAT 17.68m/17.72m, C:I 57%/58%, CET1 15.41%/16.03%, LCR 598%/746%. (read on 90dpi contact sheet; a
  300dpi crop was made but cropped off the value columns — re-crop right-hand side of a25k-09.png if challenged.)
- CONFIRMED digit-for-digit, AR2024 printed p.39 (PDF 40) & p.40 (PDF 41): PBT 23,469; tax (5,752);
  profit 17,717; total assets 2,835,724 (2023: 2,493,218); total equity 216,474 (2023: 195,138);
  PBT2023 30,608; PAT2023 23,028.
- CONCLUSION: desk research = the bank's OWN published ROE = PBT / average equity. Our 8.61% = PAT / same
  average equity. Gap = tax charge / avg equity (FY2024: 5,752/205,806 = 2.795pp). thebanks.eu 8.61% agrees
  with ours. NOT an error in either source — a definitional difference, now documented from the primary source.
- ONE ANOMALY LEFT (low priority): desk file says FY2023 = 12.6%, but the bank's own FY2023 ROE is 16.89%
  (printed as the comparative in the AR2024 KPI table) and PAT/avg equity gives 12.71%. The desk file's
  FY2023 entry matches NEITHER definition. Flag, do not reconcile.
- NOT DONE: FY2022 own-report KPI (would confirm the printed 12.82% vs computed 12.81%). ar22.pdf is on
  disk, scanned, KPI table likely around PDF p.8-12 — t22_sheet.png contact sheet rendered but not yet read.

### 2. NORTHERN BANK — PARTLY DONE
- CONFIRMED digit-for-digit on 300dpi image, printed p.129 (PDF 65 right half) Balance Sheet and
  printed p.127/128 Income Statement/SOCI:
  total assets 14,474,391 (2023: 13,697,367); total equity 943,995 (2023: 929,341);
  profit for the year 165,495 (2023: 156,719); Other equity instruments (AT1) 226,526 (2023: 226,895);
  total comprehensive income 169,665 (2023: 111,890). Entity = Northern Bank Limited, co. no. R0000568;
  statements are UNCONSOLIDATED ("Balance Sheet", "the Bank").
- CONFIRMED: Northern Bank publishes NO ROE and NO RoTE. Its KPI set (2024 Financial Review, printed
  pp.24-25 = PDF 13) is: net interest margin 2.60% (2.37%), cost income ratio 46% (48%), deposit growth
  6.3%, loan growth 4.3%, PBT 218,164 (185,960), tax (52,669)/(29,241), profit 165,495 (156,719).
  A full-document grep for "eturn on" finds only pension-scheme "return on Scheme assets" — no ROE anywhere.
  Also printed there: "profit attributable to the shareholders (i.e. excluding Additional Tier 1 capital
  holders) for the year ended 31 December 2024 amounted to £143.9m (2023: £136.0m)".
  SOCE (PDF 66) gives shareholders' funds excl AT1: 717,469 (2023: 702,446); AT1 profit share 21,642.
- OPEN QUESTION: what definition produces thebanks.eu 19.80% ROE / 1.32% ROA (multiple 15.00)?
  Tested and REJECTED: AT1 exclusion (gives 23.30%/mult 20.4). Year-end equity+assets gives mult 15.33.
  BEST FIT SO FAR: AVERAGE equity (936,668) and AVERAGE assets (14,085,879) -> mult 15.04, implying a
  numerator of ~£185.5-185.9m, which is NOT 165,495 (PAT), NOT 218,164 (FY24 PBT), NOT 169,665 (TCI),
  NOT 143,853 (attributable). Note the coincidence that FY2023 PBT = 185,960 (= 1.3202% of avg assets and
  19.85% of avg equity) — possibly a one-year lag in thebanks.eu's data, UNPROVEN.
  thebanks.eu/banks/14401 returns HTTP 403 to both WebFetch and curl, so the underlying profit/equity/asset
  figures they used could not be retrieved. Next idea: Google cache / Bing / a different thebanks.eu path,
  or accept as unresolved and report the arithmetic envelope.

### 3. STARLING — NOT STARTED (st24.pdf and st25.pdf downloaded only)
- Our inputs to verify: FY2024 profit 220,001; equity 889,770 (prior 695,277); assets 14,767,892.
- thebanks.eu "2024": ROE 28.76%, ROA 1.69%, and it states total assets 14,764.42m and annual profit 241.14m.
  Note 241.14/14,764.42 = 1.633%, NOT their 1.69% -> their ROA denominator is probably AVERAGE assets
  (~14,269m). 241.14/0.2876 = 838.5m implied average equity vs our 792.5m. Nothing verified yet.
- Questions: (a) does our FY2024 column = year ended 31 March 2024? (b) is thebanks.eu's "2024" the same
  period or ye 31 Mar 2025? (c) entity: Starling Bank Limited vs Starling Group Holdings Limited (workbook
  FY2026 flagged SGHL). (d) does Starling publish its own ROE/RoTE — AR2024 highlights/Strategic Report.

## Plan
1. [DONE] Read workbook citation cells for the three banks.
2. [DONE] Al Rayan: verify FY2024 inputs + find published ROE + definition.
3. [DONE] Al Rayan: FY2025 published ROE.
4. [NOT DONE, optional] Al Rayan FY2022 published ROE from ar22.pdf.
5. [DONE] Northern Bank: verify FY2024 inputs on image.
6. [DONE] Northern Bank: establish there is no published ROE.
7. [PARTLY DONE] Northern Bank: explain thebanks.eu 19.80/1.32 — unresolved, see above.
8. [NOT DONE] Starling: establish FY2024 period + entity; verify profit/equity/assets on image.
9. [NOT DONE] Starling: find published ROE/RoTE in AR2024 and its definition.
10. [NOT DONE] Starling: explain thebanks.eu 28.76/1.69.
11. [NOT DONE] Final SubagentHandback report.
