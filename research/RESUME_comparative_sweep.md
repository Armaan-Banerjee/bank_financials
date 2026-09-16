# RESUME — corpus-wide comparative-column sweep

Opened 2026-09-16. **Written to disk BEFORE any document was fetched**, per the
brief's rate-limit instruction. Phase 2 progress is appended at the bottom as it
happens; the tables below are the frozen Phase 1 target set.

## The idea

A Pillar 3 edition almost always prints a **prior-year comparative column**. A
blank cell for year N can therefore often be filled from the edition for year
N+1 — a document this project may already hold and already cite. The corpus has
been read one-edition-per-year; nobody has swept the comparative columns.

Two accidental proofs on 2026-09-16:
- **Gulf International Bank UK** — FY2021 edition's 2020 comparative supplied
  FY2020 NSFR and a full RWA breakdown the FY2020 document never disclosed
  (`research/RESUME_gib_comparatives.md`).
- **Reliance Bank** — the 31 Mar 2022 Pillar 3 prints a full 31 Mar 2021
  comparative column that four sheets leave blank
  (`research/RESUME_reliance_leverage.md` §6).

## Phase 1 — how the target set was built

Scanned all 145 workbooks in `banks/` with `openpyxl`. For each of the 11
Pillar 3 metric sheets, a (bank, sheet, year) cell is a **target** when:

1. every data row is empty / "Not publicly disclosed" for year N, AND
2. the same sheet **has a real figure for year N+1** — which is the operational
   proof that a document for N+1 was located, read and cited.

Exclusions applied in the scan:
- **"Not applicable" cells skipped** — structurally impossible; no comparative
  column will contain them.
- **MREL Ratio sheet excluded entirely** (only meaningful for UK resolution
  entities).
- **NSFR: targets before FY2022 dropped** (PRA PS17/21; the four-quarter-average
  rule pushes first disclosures past 1 Jan 2023).
- **LCR: targets before FY2016 dropped** (phase-in).
- **All capital metrics: targets before FY2014 dropped** (pre-CRD IV; capital
  definitions changed 1 Jan 2014 and Basel II editions often contain zero
  occurrences of "risk-weighted" — Hodge FY2010-FY2013 have none at all).

### Size of the target set

| | |
|---|---:|
| Target cells (all) | **387** |
| Distinct (bank, source-edition) pairs | **130** |
| Banks involved | **86** |
| Cells in scripts locked by other agents | 99 (31 pairs) |
| **Cells available to this sweep** | **288 (99 pairs)** |

Ranked by cells a **single document** could fill — one edition often fills a
whole column.

## Available targets (ranked)

Sheet abbreviations: CET1$ = CET1 Capital, CET1% = CET1 Ratio, T1$/T1% = Tier 1,
TC$/TC% = Total Capital, RWA = Total RWAs, LEV = Leverage Ratio.

| # | Bank | Read this edition | To fill | Cells | Sheets |
|---:|---|---|---|---:|---|
| 1 | BANK OF AFRICA UK | FY2021 | FY2020 | 9 | CET1$, CET1%, LCR, LEV, T1$, T1%, TC$, TC%, RWA |
| 2 | CHETWOOD | FY2020 | FY2019 | 9 | CET1$, CET1%, LCR, LEV, T1$, T1%, TC$, TC%, RWA |
| 3 | HAMPDEN & CO | FY2018 | FY2017 | 9 | CET1$, CET1%, LCR, LEV, T1$, T1%, TC$, TC%, RWA |
| 4 | HSBC INNOVATION BANK | FY2022 | FY2021 | 9 | CET1$, CET1%, LCR, LEV, T1$, T1%, TC$, TC%, RWA |
| 5 | UNION BANCAIRE PRIVEE UK | FY2021 | FY2020 | 9 | CET1$, CET1%, LCR, LEV, T1$, T1%, TC$, TC%, RWA |
| 6 | ALDERMORE | FY2018 | FY2017 | 8 | CET1$, CET1%, LEV, T1$, T1%, TC$, TC%, RWA |
| 7 | CHETWOOD | FY2025 | FY2024 | 8 | CET1$, LCR, LEV, NSFR, T1$, T1%, TC$, TC% |
| 8 | METHODIST CHAPEL AID | FY2019 | FY2018 | 8 | CET1$, CET1%, LEV, T1$, T1%, TC$, TC%, RWA |
| 9 | PARAGON | FY2021 | FY2020 | 8 | CET1$, CET1%, LCR, T1$, T1%, TC$, TC%, RWA |
| 10 | WEATHERBYS | FY2020 | FY2019 | 8 | CET1$, CET1%, LEV, T1$, T1%, TC$, TC%, RWA |
| 11 | PHILIPPINE NATIONAL BANK EUROPE | FY2019 | FY2018 | 7 | CET1$, CET1%, T1$, T1%, TC$, TC%, RWA |
| 12 | ZOPA | FY2018 | FY2017 | 7 | CET1$, CET1%, T1$, T1%, TC$, TC%, RWA |
| 13 | ALDERMORE | FY2021 | FY2020 | 6 | CET1$, T1$, T1%, TC$, TC%, RWA |
| 14 | MONUMENT BANK | FY2021 | FY2020 | 6 | CET1%, LCR, LEV, T1%, TC%, RWA |
| 15 | MONZO | FY2020 | FY2019 | 6 | CET1$, LCR, LEV, T1$, TC$, RWA |
| 16 | TURKISH BANK UK | FY2023 | FY2022 | 6 | CET1%, LCR, LEV, NSFR, T1%, TC% |
| 17 | BANK OF CEYLON UK | FY2023 | FY2022 | 5 | LCR, LEV, NSFR, T1%, RWA |
| 18 | ICBC (LONDON) PLC | FY2021 | FY2020 | 5 | CET1%, LEV, T1%, TC%, RWA |
| 19 | MORGAN STANLEY BANK INTERNATIONAL | FY2015 | FY2014 | 5 | CET1$, CET1%, LEV, T1$, T1% |
| 20 | OXBURY | FY2021 | FY2020 | 5 | CET1%, LCR, LEV, T1%, TC% |
| 21 | PHILIPPINE NATIONAL BANK EUROPE | FY2023 | FY2022 | 5 | CET1$, CET1%, T1%, TC%, RWA |
| 22 | PHILIPPINE NATIONAL BANK EUROPE | FY2016 | FY2015 | 5 | CET1$, CET1%, T1%, TC%, RWA |
| 23 | RELIANCE BANK | FY2022 | FY2021 | 5 | CET1$, T1$, T1%, TC$, RWA |
| 24 | CATER ALLEN | FY2022 | FY2021 | 4 | CET1%, T1%, TC%, RWA |
| 25 | CREDIT SUISSE UK | FY2017 | FY2016 | 4 | CET1%, LEV, T1%, RWA |
| 26 | MORGAN STANLEY BANK INTERNATIONAL | FY2019 | FY2018 | 4 | LCR, TC$, TC%, RWA |
| 27 | OXBURY | FY2022 | FY2021 | 4 | CET1$, T1$, TC$, RWA |
| 28 | QIB UK | FY2016 | FY2015 | 4 | CET1%, T1%, TC%, RWA |
| 29 | SHAWBROOK | FY2019 | FY2018 | 4 | CET1%, T1%, TC%, RWA |
| 30 | ZOPA | FY2021 | FY2020 | 4 | CET1%, T1%, TC%, RWA |
| 31 | ALPHA BANK LONDON | FY2023 | FY2022 | 3 | LCR, LEV, TC% |
| 32 | CHARTER COURT FINANCIAL SERVICES | FY2022 | FY2021 | 3 | CET1%, LEV, TC% |
| 33 | EFG PRIVATE BANK | FY2023 | FY2022 | 3 | LCR, LEV, NSFR |
| 34 | JP MORGAN EUROPE | FY2023 | FY2022 | 3 | LCR, LEV, NSFR |
| 35 | KINGDOM BANK | FY2015 | FY2014 | 3 | CET1%, LEV, T1% |
| 36 | NATIONAL BANK OF EGYPT UK | FY2022 | FY2021 | 3 | CET1%, LCR, T1% |
| 37 | NATIONAL BANK OF KUWAIT INTERNATIONAL | FY2024 | FY2023 | 3 | LCR, LEV, NSFR |
| 38 | RCI BANK UK | FY2023 | FY2022 | 3 | CET1$, T1$, TC$ |
| 39 | RECOGNISE BANK | FY2022 | FY2021 | 3 | LCR, LEV, RWA |
| 40 | THIS BANK | FY2021 | FY2020 | 3 | CET1%, T1%, TC% |
| 41 | ABC INTERNATIONAL BANK | FY2017 | FY2016 | 2 | LCR, LEV |
| 42 | ALDERMORE | FY2022 | FY2021 | 2 | LCR, LEV |
| 43 | BANK OF BEIRUT UK | FY2022 | FY2021 | 2 | LCR, LEV |
| 44 | BROWN SHIPLEY | FY2023 | FY2022 | 2 | LEV, NSFR |
| 45 | CYNERGY BANK | FY2018 | FY2017 | 2 | TC$, RWA |
| 46 | INVESTEC BANK PLC | FY2023 | FY2022 | 2 | LCR, NSFR |
| 47 | ITAU BBA INTERNATIONAL | FY2021 | FY2020 | 2 | T1$, T1% |
| 48 | KINGDOM BANK | FY2020 | FY2019 | 2 | TC%, RWA |
| 49 | MONZO | FY2019 | FY2018 | 2 | CET1%, T1% |
| 50 | QIB UK | FY2019 | FY2018 | 2 | LCR, LEV |
| 51 | RCI BANK UK | FY2022 | FY2021 | 2 | LEV, RWA |
| 52 | STREAMBANK | FY2024 | FY2023 | 2 | LCR, NSFR |
| 53 | ZOPA | FY2022 | FY2021 | 2 | LCR, LEV |
| 54 | ATOM BANK | FY2017 | FY2016 | 1 | LCR |
| 55 | BANK OF AFRICA UK | FY2016 | FY2015 | 1 | LEV |
| 56 | BANK OF AFRICA UK | FY2024 | FY2023 | 1 | NSFR |
| 57 | BANK OF CHINA UK | FY2017 | FY2016 | 1 | LCR |
| 58 | BANK OF SCOTLAND | FY2022 | FY2021 | 1 | LEV |
| 59 | BLME | FY2015 | FY2014 | 1 | LEV |
| 60 | BRITISH ARAB COMMERCIAL BANK | FY2015 | FY2014 | 1 | LEV |
| 61 | BRITISH ARAB COMMERCIAL BANK | FY2019 | FY2018 | 1 | LCR |
| 62 | CAF BANK | FY2022 | FY2021 | 1 | LCR |
| 63 | CAMBRIDGE AND COUNTIES BANK | FY2018 | FY2017 | 1 | LCR |
| 64 | CLOSE BROTHERS | FY2022 | FY2021 | 1 | LCR |
| 65 | CLYDESDALE | FY2022 | FY2021 | 1 | LCR |
| 66 | CO-OPERATIVE BANK | FY2023 | FY2022 | 1 | NSFR |
| 67 | COUTTS | FY2022 | FY2021 | 1 | LEV |
| 68 | CREDIT SUISSE UK | FY2021 | FY2020 | 1 | TC% |
| 69 | CREDIT SUISSE UK | FY2024 | FY2023 | 1 | LEV |
| 70 | CREDIT SUISSE UK | FY2022 | FY2021 | 1 | LCR |
| 71 | CREDIT SUISSE UK | FY2018 | FY2017 | 1 | LCR |
| 72 | CYNERGY BANK | FY2020 | FY2019 | 1 | LCR |
| 73 | FCE BANK | FY2022 | FY2021 | 1 | LCR |
| 74 | HANDELSBANKEN | FY2022 | FY2021 | 1 | LCR |
| 75 | ICBC (LONDON) PLC | FY2017 | FY2016 | 1 | LCR |
| 76 | LLOYDS BANK CORPORATE MARKETS | FY2019 | FY2018 | 1 | LEV |
| 77 | LLOYDS BANK CORPORATE MARKETS | FY2022 | FY2021 | 1 | LCR |
| 78 | METHODIST CHAPEL AID | FY2021 | FY2020 | 1 | LCR |
| 79 | METRO BANK | FY2016 | FY2015 | 1 | RWA |
| 80 | MIZUHO INTERNATIONAL | FY2015 | FY2014 | 1 | LEV |
| 81 | MIZUHO INTERNATIONAL | FY2018 | FY2017 | 1 | LCR |
| 82 | MONZO | FY2021 | FY2020 | 1 | TC% |
| 83 | NATIONAL WESTMINSTER BANK PLC | FY2015 | FY2014 | 1 | LEV |
| 84 | NATIONAL WESTMINSTER BANK PLC | FY2018 | FY2017 | 1 | LCR |
| 85 | OAKNORTH BANK | FY2022 | FY2021 | 1 | LCR |
| 86 | OAKNORTH BANK | FY2017 | FY2016 | 1 | LCR |
| 87 | PARAGON | FY2023 | FY2022 | 1 | LEV |
| 88 | RBC EUROPE | FY2015 | FY2014 | 1 | LEV |
| 89 | RBC EUROPE | FY2022 | FY2021 | 1 | LCR |
| 90 | SHAWBROOK | FY2022 | FY2021 | 1 | LCR |
| 91 | SHAWBROOK | FY2023 | FY2022 | 1 | NSFR |
| 92 | STANDARD CHARTERED BANK | FY2022 | FY2021 | 1 | LCR |
| 93 | THE BANK OF LONDON GROUP | FY2023 | FY2022 | 1 | CET1% |
| 94 | THIS BANK | FY2023 | FY2022 | 1 | LCR |
| 95 | TRIODOS | FY2020 | FY2019 | 1 | LCR |
| 96 | TSB | FY2021 | FY2020 | 1 | LCR |
| 97 | UNITED NATIONAL | FY2024 | FY2023 | 1 | LCR |
| 98 | UNITED TRUST BANK | FY2021 | FY2020 | 1 | LCR |
| 99 | WEATHERBYS | FY2019 | FY2018 | 1 | LCR |

## Locked — report only, do NOT edit

These are in scripts named in the brief's lock list or in
`research/RESUME_fx_scale_sweep.md` / `research/RESUME_entity_basis_sweep.md`.
`build_gulf_international_bank_uk.py` and `build_reliance_bank.py` appear in
those files but are explicitly released, so they are in the available table.

| Bank | Edition | To fill | Cells | Script |
|---|---|---|---:|---|
| LLOYDS BANK | FY2019 | FY2018 | 9 | `build_lloyds_bank.py` |
| ONESAVINGS | FY2021 | FY2020 | 9 | `build_onesavings.py` |
| STARLING | FY2021 | FY2020 | 9 | `build_starling.py` |
| ZENITH | FY2020 | FY2019 | 9 | `build_zenith.py` |
| ACCESS BANK UK | FY2020 | FY2019 | 8 | `build_access_bank.py` |
| C HOARE AND CO | FY2020 | FY2019 | 8 | `build_c_hoare.py` |
| FCMB UK | FY2020 | FY2019 | 7 | `build_fcmb_uk.py` |
| JULIAN HODGE BANK | FY2016 | FY2015 | 7 | `build_julian_hodge_bank.py` |
| BANK MANDIRI EUROPE | FY2022 | FY2021 | 3 | `build_bank_mandiri_europe.py` |
| PERSIA INTERNATIONAL BANK | FY2016 | FY2015 | 3 | `build_persia_international_bank.py` |
| BANK MANDIRI EUROPE | FY2020 | FY2019 | 2 | `build_bank_mandiri_europe.py` |
| FCMB UK | FY2021 | FY2020 | 2 | `build_fcmb_uk.py` |
| FIDBANK UK | FY2022 | FY2021 | 2 | `build_fidbank_uk.py` |
| ICICI BANK UK | FY2017 | FY2016 | 2 | `build_icici_bank_uk.py` |
| PERSIA INTERNATIONAL BANK | FY2020 | FY2019 | 2 | `build_persia_international_bank.py` |
| PERSIA INTERNATIONAL BANK | FY2018 | FY2017 | 2 | `build_persia_international_bank.py` |
| ACCESS BANK UK | FY2021 | FY2020 | 1 | `build_access_bank.py` |
| ARAB BANK EUROPE | FY2022 | FY2021 | 1 | `build_arab_bank_europe.py` |
| BANK OF THE PHILIPPINE ISLANDS EUROPE | FY2023 | FY2022 | 1 | `build_bpi_europe.py` |
| BANK SADERAT | FY2021 | FY2020 | 1 | `build_bank_saderat.py` |
| C HOARE AND CO | FY2022 | FY2021 | 1 | `build_c_hoare.py` |
| CLEARBANK | FY2020 | FY2019 | 1 | `build_clearbank.py` |
| CREDIT SUISSE INTERNATIONAL | FY2017 | FY2016 | 1 | `build_credit_suisse_international.py` |
| FIRSTBANK UK | FY2020 | FY2019 | 1 | `build_firstbank_uk.py` |
| HSBC BANK PLC | FY2022 | FY2021 | 1 | `build_hsbc_bank_plc.py` |
| HSBC UK BANK PLC | FY2022 | FY2021 | 1 | `build_hsbc_uk_bank_plc.py` |
| ICICI BANK UK | FY2018 | FY2017 | 1 | `build_icici_bank_uk.py` |
| JULIAN HODGE BANK | FY2018 | FY2017 | 1 | `build_julian_hodge_bank.py` |
| LLOYDS BANK | FY2023 | FY2022 | 1 | `build_lloyds_bank.py` |
| ONESAVINGS | FY2023 | FY2022 | 1 | `build_onesavings.py` |
| SECURE TRUST BANK | FY2022 | FY2021 | 1 | `build_secure_trust.py` |

## Traps that govern Phase 2

1. **A comparative may be RESTATED onto a different basis.** GIB restated FY2021
   leverage from $10,573,209k / 3.52% to $5,268,295k / 7.06% when the UK excluded
   central-bank claims from 1 Jan 2022. Both correct, different measures. Never
   merge, reconcile or overwrite — a restated comparative goes on its **own
   labelled row** beside the as-reported figure. If the basis cannot be
   established, **leave it out and say so**.
2. **LCR/NSFR basis** — UK KM1 prints a 12-month average; an annual report prints
   point-in-time. Never one row. A row captioned "average" does not always hold
   one (Methodist Chapel Aid's captions a year-end value) — which matters here,
   MCA is target #8.
3. **Column headers can be wrong in the source.** Reliance's FY2020 AR KPI table
   is headed "2019"/"2018 (as stated)" while holding FY2020/FY2019. Cross-check
   every comparative against the document's own narrative or a second table.
4. **Date every edition from its COVER** — never filename, URL or index label.

## Absolute rules

- Never fabricate, derive or back-solve. No RWA from capital / ratio. A blank
  comparative column is the answer.
- Entity basis: a parent/group figure never enters an entity-level sheet.
  Significant-subsidiaries annexes and solo-consolidation sections naming the
  entity ARE valid. Segmental figures are NOT.
- A year-N figure taken from the year-N+1 edition must SAY SO on the sheet:
  document, page, table, and that it is the comparative column of the following
  year's edition.
- Watch for a printed "Total RWA" that is really the credit-risk subtotal —
  check capital / RWA reproduces the printed ratio.
- Verify every URL: status AND Content-Type AND `%PDF`, following redirects.
  Soft-404 behaviour is per-FILENAME.
- Exactly 1,048,576 bytes = investigate (test whether the LAST page carries
  text), not a verdict.
- 403/401/429/503 = BLOCKED, never an absence.
- Overview sheets are COPIES — update both.
- Do NOT run `refresh_all.py`, the test suite, or commit.

## Phase 2 log

(appended as work proceeds)
