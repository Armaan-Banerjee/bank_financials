# RESUME — AIB Group (UK) + Melli Bank (session 2026-09-15)

Two-bank task: (1) AIB Group (UK) FY2021 access reversal via Companies House;
(2) Melli Bank Pillar 3 disclosure-policy timeline FY2013–FY2025.

## Status

- [x] Read CLAUDE.md, CODING_STANDARDS.md, RESUME_SESSION.md §6/§7
- [x] AIB: FY2021 Annual Financial Report downloaded from Companies House
      (NI018800, filing `MzMzMjQ0MDUyOWFkaXF6a2N4`, 168pp, %PDF confirmed,
      9,246,343 bytes) → scratchpad `aib/aib_fy2021.pdf`
- [x] AIB: OCR (168pp rendered at 200dpi grey, tesseract --psm 6) + VISUAL
      verification of every page used (p.20, 21, 66, 68, 69, 70, 118, 144)
- [x] AIB: validation gate vs FY2022-comparative-derived values — DONE,
      one real divergence found (see below)
- [x] AIB: script edits + rebuild — `scripts/build_aib_uk.py`, 18 sheets, OK
- [x] Melli: FY2014 + FY2016 Pillar 3 fetch + transcribe — both fetched
      (%PDF, 16pp and 23pp, covers name "Registered number 4152338"), both
      text-native, transcribed into new FY2016/FY2014 Pillar 3 columns
- [x] Melli: disclosure-policy timeline recorded (4 phases + FY2023 reversal)
- [x] Melli: access routes (Companies House 04152338, HKMA 100273, Wayback
      `id_` form) recorded in ACCESS_ROUTES_NOTE on every Pillar 3 sheet
- [x] Melli: rebuild — `scripts/build_melli_bank.py`, 18 sheets, OK

## MELLI RESULT (complete, 2026-09-16)

Pillar 3 sheets now run on `P3_YEARS = FY2025..FY2021 + FY2016 + FY2014`
(statement sheets and Overview stay at 5 years). Cells added:

| Metric | FY2016 | FY2014 |
|---|---|---|
| CET1 Capital | 280,654 | blank — see below |
| Tier 1 Capital | 280,654 | 207,738 |
| Total Capital | 280,654 | 269,548 (of which Tier 2 61,810) |
| Leverage Ratio | 75% | "approximately 60%" (verbatim hedge kept) |
| LCR | 119.16% | blank — disclosed non-disclosure |

FY2014 CET1 left blank deliberately: that edition says "Total Tier 1
Capital", never "CET1". Inferring equivalence would not be transcription.

Not filled, and why (all evidenced against the primaries, do not re-chase):
- CET1/Tier 1/Total Capital **Ratio** — no percentage in either edition.
  Both give a Pillar 1 minimum capital requirement against an "at least 8%"
  floor; grossing that up would be back-solving.
- Total RWAs / RWA Breakdown — no RWA figure in either edition. What they do
  give is the Pillar 1 minimum capital requirement by category and exposure
  class (FY2016 total 30,383; FY2014 total 23,792), recorded in the Total
  RWAs note and deliberately kept OUT of the RWA Breakdown rows so nothing
  can read a capital requirement as an RWA (12.5x understatement).
- NSFR — FY2016 names the NSFR as a tool but gives no number; FY2014 silent.
- MREL — neither document mentions it.
- FY2015 not added as a column: exists only as narrative in the FY2016
  edition, which contradicts itself (€278,147k "of which 75% ... €209,264k"
  in s.4 vs "Euro 276m of which 75%" in s.5.5; 75% of 278,147 = 208,610).
  Both recorded in the note, neither reconciled.

Deliberately NOT done: the FY2014/FY2016 Basel credit-exposure and
impairment tables were not pushed into the Asset Quality sheet. Different
measurement basis (pre-provision Basel exposure by class, EUR m) from that
sheet's FRS 102 loan book (EUR '000) — mixing them would mislead.

Publication-history finding recorded in `PILLAR3_HISTORY_NOTE`, carried on
every Pillar 3 sheet: four phases (FY2013–15 "will be posted"; FY2016–19
"have been posted"; FY2020–22 "available on request"; FY2023 reverses to
"available on the Bank's website"; FY2024–25 back to "on request"). The
FY2023 claim is recorded as **contradicted by the bank's own website** —
five archived /reports captures (Sept 2021 → May 2026) all say "available
on request" — stated as a tension between two of the bank's own statements
and deliberately not resolved. FY2013–19 + FY2023 = published-then-lost
(worth a written request); FY2020–22 + FY2024–25 = declared
non-publication, a complete answer, not to be re-chased.

## Known pre-existing defect NOT touched

`banks/MELLI BANK FINANCIALS.xlsx` "Statement of Changes in Equity" source
cell is clipped (needs ~286pt of row height, has 150). It uses the
unmodified `STATEMENTS_SOURCES` at `add_equity_changes_sheet`'s default
`source_height`. Pre-existing and out of this task's scope — left alone.

## AIB RESULT (complete, 2026-09-16)

**Validation gate outcome: the primary REPRODUCES the comparative-derived
figures everywhere except the income statement, where it diverges by a
£3m reclassification.**

Reproduced exactly (no change needed anywhere):
- Cash flow: all 22 FY2021 lines.
- Balance sheet: every line and all three totals (12,688 / 10,896 / 1,792).
- Statement of changes in equity: every FY2021 movement and both balances.
- Asset quality: full stage × grade table (6,399 gross, (201) ECL, 6,198 net).
- Capital: CET1 £1,508m, Total RWA £6,611m, LCR 169%.

DIVERGENCE (documented on labelled memorandum rows, nothing overwritten):
the FY2022 edition reclassified a £3m loss on disposal of property from
below operating profit into other operating income. FY2021 edition vs
FY2022 edition — Other operating income nil vs (3); Other income 46 vs 43;
Total operating income 244 vs 241; Operating profit before impairment 84 vs
81; "Operating profit before taxation 92" and "Loss on disposal of property
(3)" dropped entirely. Profit before tax (89) and profit for the year (170)
identical on both bases. Both editions were opened and both confirmed to
print what is shown, so this is an inter-edition restatement, not a
transcription error.

New cells / facts the primary added:
- **CET1 Ratio FY2021 22.81% is now TRANSCRIBED, not calculated.** The old
  script flagged it CALCULATED (CET1 ÷ RWA); the FY2021 report states it
  directly ("Capital ratio at 31 December 2021 ... 22.81% / 22.01%", p.20).
- Fully-loaded FY2021 triplet: CET1 £1,442m, ratio 22.01%, RWA £6,554m.
- Pillar 1 + Pillar 2a requirement 9.95% for 2021 (FY2022 report corroborates:
  9.86% "for 2022, a reduction from 9.95% in 2021").
- Balance sheet: "Items in course of collection" £3m + "Other assets" £14m
  (FY2022 edition folds these into £17m); "Reserves" (22) + "Retained
  earnings" (570) (FY2022 edition combines into (592)); "Secondary
  non-preferential debt" explicitly NIL at 31 Dec 2021 (£45m at 31 Dec 2020).
- Cash flow: "Net decrease in items in course of collection" £1m, "Net
  decrease in other assets" nil, "Dividends received from subsidiaries" nil
  (Group basis).
- **MREL — an existing script claim was WRONG.** The script said MREL is "not
  mentioned anywhere in any of the five Annual Financial Reports". The FY2021
  report mentions it twice: glossary p.165, and note 34 (p.144) — AIB plc
  issued a £45m secondary non-preferential loan to AIB UK on 31 Dec 2020
  "for the purposes of meeting AIB UK MREL requirements", SONIA + 130bps,
  repaid 31 Dec 2021. Still no MREL *ratio*, so the sheet stays "Not
  publicly disclosed", but the narrative is corrected.
- SOCE judgement call CONFIRMED: note 35 names the £2m "Other reserves"
  component as "Revaluation reserves", settling the column mapping.

Evidenced absences in the FY2021 primary (do not re-chase): no leverage
ratio (only "leverage lending"/"leveraged exposures" prose); no NSFR / no
mention of stable funding (binding only from 1 Jan 2022, so FY2021's 156%
is a retrospective comparative in the FY2022 report); no Total Capital and
no Tier 1 capital figure (CET1 only); no absolute category-level RWA split
(movement table only — must not be back-solved); no Strong vs Satisfactory
split (confirms the existing blank cells).

Other 403-driven fallbacks in this script: **none.** FY2021 was the only one.

OCR trap caught by the visual check: tesseract read the Criticised watch
row on p.118 as 187 — that is the Stage 2 cell; the Total column reads 242
(242 + 435 = 677, the printed Total criticised). Recorded in the script.

## Working routes discovered

- AIB Group (UK) p.l.c. FY2021 AFR — **Companies House**, company NI018800,
  filing filed 11 March 2022. The bank's own aibgb.co.uk returns 403; aib.ie
  hosts only FY2022 onward. Direct document URL:
  `https://find-and-update.company-information.service.gov.uk/company/NI018800/filing-history/MzMzMjQ0MDUyOWFkaXF6a2N4/document?format=pdf&download=0`
  Scanned filing — OCR required, verify digits visually.
- Melli Bank plc — Companies House company **04152338** for annual reports;
  **HKMA public register** hosts readable copies:
  `https://vpr.hkma.gov.hk/statics/assets/doc/100273/ar_23/ar_23_eng.pdf` (FY2023),
  `.../ar_22/ar_22_eng.pdf` (FY2022). mellibank.com currently unreachable.

## Findings log

(appended as work lands)
