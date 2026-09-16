# Leverage-ratio basis sweep — FY2021/FY2022 boundary

Started 2026-09-16. Hunting the defect confirmed at Gulf International Bank (UK):
the UK leverage ratio framework excluded claims on central banks from the total
exposure measure **with effect from 1 January 2022**, so a Leverage Ratio sheet
that runs FY2018-FY2021 on the old (including-central-bank-claims) basis and
FY2022-FY2025 on the new one, as one unlabelled series, shows deleveraging that
did not happen. See `research/RESUME_gib_comparatives.md` for the model
treatment (both bases, separate labelled rows, never reconciled).

## PHASE 1 — measurement (complete)

### Method

- Read the `Leverage Ratio` sheet of all **145** workbooks in `banks/` directly
  from disk with openpyxl (NOT from `research/insights.db`, whose last refresh
  was 2026-09-15T17:02Z — 50 workbooks have been rebuilt since, including the
  GIB UK fix). Script: scratchpad `lev_extract.py` / `lev_analyze.py` /
  `lev_rank.py` / `lev_master.py`.
- Year strings regex-extracted with `re.match(r"(FY\d{4})", year)` — the sheets
  carry annotations (`FY2025 (y/e 30 Jun 25)`, `FY2021†`, `FY2023 (15mo)`,
  `FY2022 (MBL)`), so exact-string comparison would have silently dropped them.
- Each ratio row classified EXCL / INCL / UNSPEC from its own label text.
- "Primary series" = the ratio row with the most populated years (ties broken
  toward the unlabelled row) — i.e. the row a reader would read as *the*
  leverage series.
- **Central-bank reserve intensity** computed independently from each bank's
  `Balance Sheet` sheet in `insights.db`: sum of asset rows matching
  `^Assets - .*central bank` (excluding `...facilities`, which are liabilities
  mislanded) over `Assets - Total assets`, at FY2021 and FY2022. Available for
  72 of 145 banks. This gives a *predicted* jump from the exclusion alone:
  `Δ_expected ≈ ratio_FY2021 × s / (1 − s)`. It is a screen, not evidence —
  total assets is only a proxy for the leverage exposure measure.
- "Basis documented" = the sheet's own `Note:` row or source-citation cell
  mentions central banks **and** a basis-break phrase.

### Headline counts

| | banks |
|---|---:|
| Workbooks with a `Leverage Ratio` sheet | 145 / 145 |
| Primary series populated on **both** sides of the FY2021/FY2022 boundary | **89** |
| …of those, sheet already documents the basis change | 40 |
| …of those, sheet does **not** document it | **49** |
| …undocumented **and** material (>1.5pp or >25% relative) | **26** |
| Already split across separate labelled basis rows (dual/triple rows) | 14 |
| No boundary comparison possible (a side is blank, or bank is post-2022) | 56 |
| "Flat but should have jumped" (|Δ| < half the CB-exclusion prediction) | 8 |

### Non-December year-ends — the boundary does NOT move

25 banks have a non-December year-end (31 Mar: C. Hoare, Chetwood, ICICI,
Investec, Nomura Bank International, Persia, PNBIL, Recognise, Reliance, SBI UK,
SMBC, StreamBank, THIS Bank, Union Bank of India UK, UBP UK, Zempler; 30 Jun:
Aldermore, Griffin, NBE UK; 30 Sep: Castle Trust, Clydesdale (later 31 Mar),
Julian Hodge; 30 Apr: CAF Bank; 31 Oct: RBC Europe, TD Bank Europe; 28 Feb→31
Mar: Monzo).

Each of these scripts' own source citations was read to establish what date its
`FY2022` column actually refers to. In every case the convention is the same:
the year is named for the **calendar year in which the year-end falls** — SMBC
"year ended 31 March 2022", ICICI "year ended 31 March 2022", Union Bank of India
"year ended 31 March 2022", PNBIL 31 March 2022, Persia / Nomura / THIS Bank /
Investec / Chetwood / Recognise likewise, Aldermore's headers literally read
`FY2022 (y/e 30 Jun 22)`, Castle Trust `y/e 30 September`, CAF Bank 30 April
2022, RBC Europe / TD Bank Europe 31 October 2022, Monzo 28 February 2022.

**Nobody in the estate uses the Indian/Japanese "FY2021 = y/e March 2022"
convention.** So the earliest FY2022 reference date anywhere is Monzo's 28
February 2022, which is still after 1 January 2022, and the boundary stays at
FY2021→FY2022 for every bank. Two notes: StreamBank has no FY2022 at all (its
accounting period was extended to 31 March 2023), and Zempler's FY2022 is taken
from the 31 March 2023 edition's comparative column — neither has a populated
FY2021, so neither can cross the boundary.

### Ranked table — all 89 boundary-crossing banks, by |Δ pp|

Columns: `Δ pp` and `Δ rel %` are the FY2021→FY2022 step in the primary series.
`Exposure Δ %` is the step in the exposure-measure row where the workbook carries
one — **this is the decisive column**: a sharp fall in the exposure measure while
total assets did not fall is the denominator changing. `CB reserves / assets`
and `Δ predicted` are the independent screen described above; `Residual` is
actual minus predicted.

| # | Bank | Primary row basis label | FY2021 | FY2022 | Δ pp | Δ rel % | Exposure Δ % | CB reserves / assets FY2022 | Δ predicted by CB exclusion alone | Residual | Basis documented on sheet? | Dual rows? |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|:-:|:-:|
| 1 | Monument Bank Limited | UNSPEC | 90.48 | 12.00 | -78.48 | -86.7 |  | 0.33 | 43.77 | -122.25 | **no** | no |
| 2 | iFAST Global Bank Limited | UNSPEC | 19.00 | 47.30 | 28.30 | 148.9 | 7.8 |  |  |  | **no** | no |
| 3 | ClearBank Limited | EXCL | 38.79 | 13.87 | -24.92 | -64.2 |  |  |  |  | yes | no |
| 4 | DB UK Bank Limited | UNSPEC | 37.00 | 25.00 | -12.00 | -32.4 |  |  |  |  | **no** | no |
| 5 | Morgan Stanley Bank International Limited | UNSPEC | 30.10 | 18.50 | -11.60 | -38.5 | 59.1 | 0.01 | 0.19 | -11.79 | **no** | no |
| 6 | Chetwood Financial Limited | UNSPEC | 23.40 | 14.58 | -8.82 | -37.7 | 82.4 |  |  |  | yes | no |
| 7 | Ghana International Bank Plc | EXCL | 15.20 | 23.86 | 8.66 | 57.0 |  |  |  |  | yes | no |
| 8 | Kroo Bank Ltd | EXCL | 91.82 | 99.97 | 8.15 | 8.9 |  | 0.38 | 56.86 | -48.71 | yes | no |
| 9 | Bank of China (UK) Limited | UNSPEC | 11.30 | 18.50 | 7.20 | 63.7 | -25.4 | 0.29 | 4.55 | 2.65 | yes | no |
| 10 | OakNorth Bank plc | EXCL | 21.40 | 14.50 | -6.90 | -32.2 |  | 0.27 | 7.73 | -14.63 | yes | yes |
| 11 | KEXIM Bank (UK) Limited | UNSPEC | 23.00 | 16.70 | -6.30 | -27.4 |  |  |  |  | **no** | no |
| 12 | Credit Suisse International | UNSPEC | 7.47 | 12.51 | 5.04 | 67.5 |  |  |  |  | **no** | no |
| 13 | Citibank UK Limited | UNSPEC | 5.20 | 9.90 | 4.70 | 90.4 | -30.6 | 0.24 | 1.60 | 3.10 | yes | no |
| 14 | SMBC Bank International plc | EXCL | 7.70 | 12.40 | 4.70 | 61.0 | -33.8 | 0.47 | 6.76 | -2.06 | yes | yes |
| 15 | Tandem Bank Limited | EXCL | 4.60 | 8.80 | 4.20 | 91.3 | 63.0 | 0.35 | 2.51 | 1.69 | yes | no |
| 16 | Jordan International Bank Plc | UNSPEC | 23.40 | 19.30 | -4.10 | -17.5 |  |  |  |  | **no** | no |
| 17 | Gulf International Bank (UK) Limited | UNSPEC | 3.52 | 7.17 | 3.65 | 103.7 | -45.7 |  |  |  | yes | yes |
| 18 | HBL Bank UK Limited | UNSPEC | 9.41 | 13.01 | 3.60 | 38.3 |  | 0.17 | 1.92 | 1.68 | **no** | no |
| 19 | DF Capital Bank Limited | EXCL | 21.20 | 17.60 | -3.60 | -17.0 |  | 0.18 | 4.79 | -8.39 | **no** | no |
| 20 | Reliance Bank Limited | EXCL | 4.50 | 7.60 | 3.10 | 68.9 |  | 0.36 | 2.57 | 0.53 | **no** | no |
| 21 | FirstBank UK Limited | UNSPEC | 6.83 | 9.84 | 3.01 | 44.1 |  |  |  |  | **no** | no |
| 22 | Vanquis Bank Limited | UNSPEC | 18.10 | 21.00 | 2.90 | 16.0 | -18.3 |  |  |  | yes | no |
| 23 | Oxbury Bank Plc | EXCL | 15.00 | 12.17 | -2.83 | -18.9 |  |  |  |  | **no** | no |
| 24 | FCMB Bank (UK) Limited | UNSPEC | 10.12 | 7.41 | -2.71 | -26.8 |  |  |  |  | **no** | no |
| 25 | Atom Bank Plc | UNSPEC | 3.90 | 6.60 | 2.70 | 69.2 | 13.7 | 0.32 | 1.83 | 0.87 | yes | no |
| 26 | Itau BBA International plc | UNSPEC | 14.60 | 11.90 | -2.70 | -18.5 |  | 0.00 | 0.00 | -2.70 | **no** | no |
| 27 | ICBC Standard Bank Plc | EXCL | 5.09 | 7.70 | 2.61 | 51.3 | -18.4 | 0.21 | 1.39 | 1.22 | yes | no |
| 28 | Julian Hodge Bank Limited | UNSPEC | 8.30 | 10.90 | 2.60 | 31.3 | -6.2 | 0.06 | 0.56 | 2.04 | **no** | no |
| 29 | United National Bank Limited | UNSPEC | 10.97 | 8.43 | -2.54 | -23.2 | 17.4 |  |  |  | **no** | no |
| 30 | Northern Bank Limited (trading as Danske Bank) | UNSPEC | 4.20 | 6.70 | 2.50 | 59.5 |  |  |  |  | **no** | no |
| 31 | Bank of Africa United Kingdom Plc | UNSPEC | 11.51 | 13.98 | 2.47 | 21.5 |  | 0.10 | 1.29 | 1.18 | **no** | no |
| 32 | Starling Bank Limited | EXCL | 5.40 | 7.85 | 2.45 | 45.4 |  |  |  |  | yes | yes |
| 33 | Triodos Bank UK Limited | UNSPEC | 9.30 | 11.73 | 2.43 | 26.1 | -17.1 |  |  |  | yes | no |
| 34 | Punjab National Bank (International) Limited | EXCL | 17.30 | 19.30 | 2.00 | 11.6 |  |  |  |  | yes | no |
| 35 | Cynergy Bank Plc | UNSPEC | 5.46 | 7.40 | 1.94 | 35.5 |  | 0.13 | 0.85 | 1.09 | **no** | no |
| 36 | Castle Trust Capital plc | EXCL | 11.10 | 9.17 | -1.93 | -17.4 | 26.9 |  |  |  | yes | yes |
| 37 | J.P. Morgan Securities plc | UNSPEC | 5.74 | 7.67 | 1.93 | 33.6 | -11.0 | 0.02 | 0.10 | 1.83 | **no** | no |
| 38 | Weatherbys Bank Limited | UNSPEC | 3.37 | 5.30 | 1.93 | 57.3 |  |  |  |  | **no** | no |
| 39 | Crown Agents Bank Limited | UNSPEC | 5.00 | 6.90 | 1.90 | 38.0 |  | 0.41 | 3.47 | -1.57 | **no** | no |
| 40 | Lloyds Bank Corporate Markets plc | UNSPEC | 3.50 | 5.40 | 1.90 | 54.3 |  | 0.22 | 1.01 | 0.89 | yes | no |
| 41 | Bank of Ireland (UK) Plc | UNSPEC | 7.20 | 9.10 | 1.90 | 26.4 | -25.9 | 0.12 | 0.97 | 0.93 | **no** | no |
| 42 | Kuwait Finance House Plc | UNSPEC | 10.50 | 12.30 | 1.80 | 17.1 |  | 0.16 | 1.99 | -0.19 | **no** | no |
| 43 | HSBC UK Bank plc | UNSPEC | 4.20 | 5.90 | 1.70 | 40.5 |  | 0.28 | 1.60 | 0.10 | yes | no |
| 44 | Gatehouse Bank Plc | EXCL | 9.20 | 7.50 | -1.70 | -18.5 |  |  |  |  | **no** | no |
| 45 | ABC International Bank plc | EXCL | 13.77 | 12.28 | -1.49 | -10.8 | 11.4 |  |  |  | **no** | no |
| 46 | Unity Trust Bank Plc | UNSPEC | 5.70 | 7.19 | 1.49 | 26.1 | 2.2 |  |  |  | yes | no |
| 47 | HSBC Bank plc | UNSPEC | 4.10 | 5.50 | 1.40 | 34.1 |  | 0.18 | 0.92 | 0.48 | yes | no |
| 48 | Investec Bank plc | UNSPEC | 8.00 | 9.30 | 1.30 | 16.3 | -9.4 | 0.20 | 1.94 | -0.64 | **no** | no |
| 49 | Allica Bank Limited | EXCL | 12.50 | 11.30 | -1.20 | -9.6 | 131.6 | 0.13 | 1.88 | -3.08 | yes | yes |
| 50 | Hampshire Trust Bank Plc | UNSPEC | 8.00 | 9.20 | 1.20 | 15.0 |  |  |  |  | **no** | no |
| 51 | NatWest Markets Plc | UNSPEC | 4.30 | 5.40 | 1.10 | 25.6 | -26.7 | 0.08 | 0.37 | 0.73 | **no** | no |
| 52 | Zenith Bank (UK) Limited | EXCL | 8.36 | 7.32 | -1.04 | -12.4 | 18.3 |  |  |  | yes | no |
| 53 | Cambridge & Counties Bank Limited | UNSPEC | 12.90 | 13.92 | 1.02 | 7.9 | 2.9 | 0.21 | 3.39 | -2.37 | **no** | no |
| 54 | Bank Sepah International Plc | UNSPEC | 47.00 | 46.00 | -1.00 | -2.1 |  |  |  |  | **no** | no |
| 55 | Birmingham Bank Limited | UNSPEC | 37.00 | 36.00 | -1.00 | -2.7 |  |  |  |  | **no** | no |
| 56 | British Arab Commercial Bank PLC | UNSPEC | 6.70 | 5.70 | -1.00 | -14.9 |  |  |  |  | **no** | no |
| 57 | ICBC (London) plc | UNSPEC | 30.75 | 31.75 | 1.00 | 3.3 | -2.1 | 0.07 | 2.30 | -1.30 | **no** | no |
| 58 | United Bank for Africa (UK) Limited | EXCL | 7.00 | 6.00 | -1.00 | -14.3 | 19.6 |  |  |  | yes | yes |
| 59 | Bank of London and The Middle East plc | EXCL | 14.92 | 14.00 | -0.92 | -6.2 |  |  |  |  | yes | no |
| 60 | Barclays Bank PLC | UNSPEC | 3.70 | 4.60 | 0.90 | 24.3 | -15.9 | 0.17 | 0.75 | 0.15 | **no** | no |
| 61 | The Access Bank UK Limited | UNSPEC | 11.18 | 12.00 | 0.82 | 7.3 | 34.3 |  |  |  | yes | no |
| 62 | National Bank of Egypt (UK) Limited | UNSPEC | 12.47 | 11.65 | -0.82 | -6.6 |  | 0.00 | 0.00 | -0.82 | yes | no |
| 63 | Shawbrook Bank Limited | UNSPEC | 8.00 | 8.80 | 0.80 | 10.0 |  | 0.15 | 1.37 | -0.57 | **no** | no |
| 64 | Mizuho International plc | UNSPEC | 4.75 | 4.07 | -0.68 | -14.3 |  | 0.02 | 0.11 | -0.79 | **no** | no |
| 65 | The Charity Bank Limited | UNSPEC | 7.72 | 8.39 | 0.67 | 8.7 |  |  |  |  | yes | no |
| 66 | Guaranty Trust Bank (UK) Limited | UNSPEC | 5.04 | 4.38 | -0.66 | -13.1 |  |  |  |  | yes | no |
| 67 | National Westminster Bank Public Limited Company | UNSPEC | 3.80 | 4.40 | 0.60 | 15.8 | -20.0 | 0.18 | 0.84 | -0.24 | **no** | no |
| 68 | OneSavings Bank plc | EXCL | 7.90 | 8.40 | 0.50 | 6.3 |  |  |  |  | **no** | no |
| 69 | Goldman Sachs International Bank | UNSPEC | 6.40 | 6.87 | 0.47 | 7.3 | 3.7 |  |  |  | **no** | no |
| 70 | Methodist Chapel Aid Limited | UNSPEC | 33.05 | 33.49 | 0.44 | 1.3 |  |  |  |  | **no** | no |
| 71 | TD Bank Europe Limited | EXCL | 5.10 | 4.70 | -0.40 | -7.8 | 14.3 | 0.00 | 0.02 | -0.42 | **no** | no |
| 72 | Secure Trust Bank Public Limited Company | EXCL | 10.30 | 10.70 | 0.40 | 3.9 |  |  |  |  | yes | no |
| 73 | National Bank of Kuwait (International) Plc | EXCL | 12.74 | 13.09 | 0.35 | 2.7 | 4.1 | 0.15 | 2.32 | -1.97 | **no** | no |
| 74 | Alrayan Bank Limited | UNSPEC | 6.40 | 6.70 | 0.30 | 4.7 |  |  |  |  | yes | no |
| 75 | The Co-operative Bank p.l.c. | EXCL | 3.70 | 4.00 | 0.30 | 8.1 |  | 0.18 | 0.82 | -0.52 | **no** | no |
| 76 | C. Hoare & Co. | EXCL | 6.32 | 6.61 | 0.29 | 4.6 |  | 0.25 | 2.15 | -1.86 | yes | no |
| 77 | QIB (UK) plc | EXCL | 8.75 | 8.50 | -0.25 | -2.9 |  |  |  |  | **no** | no |
| 78 | Redwood Bank Limited | EXCL | 8.60 | 8.80 | 0.20 | 2.3 |  | 0.16 | 1.58 | -1.38 | yes | no |
| 79 | Barclays Bank UK Group | INCL | 4.10 | 4.30 | 0.20 | 4.9 | 3.7 |  |  |  | yes | yes |
| 80 | Union Bancaire Privée (UK) Limited | EXCL | 8.90 | 9.10 | 0.20 | 2.2 | -9.5 | 0.11 | 1.06 | -0.86 | **no** | no |
| 81 | United Trust Bank Limited (consolidated UTB Partners basis) | EXCL | 8.10 | 7.90 | -0.20 | -2.5 | 24.2 |  |  |  | yes | no |
| 82 | CAF Bank Limited | EXCL | 3.81 | 3.97 | 0.16 | 4.2 |  |  |  |  | yes | yes |
| 83 | Habib Bank Zurich Plc | UNSPEC | 8.63 | 8.74 | 0.11 | 1.3 |  |  |  |  | yes | no |
| 84 | Lloyds Bank plc | UNSPEC | 5.30 | 5.40 | 0.10 | 1.9 |  | 0.12 | 0.70 | -0.60 | **no** | no |
| 85 | Standard Chartered Bank (standalone Company basis) | EXCL | 4.10 | 4.20 | 0.10 | 2.4 |  | 0.09 | 0.40 | -0.30 | yes | no |
| 86 | Santander UK Plc | EXCL | 5.30 | 5.20 | -0.10 | -1.9 | 0.8 | 0.15 | 0.97 | -1.07 | yes | yes |
| 87 | Union Bank of India (UK) Limited | UNSPEC | 27.57 | 27.49 | -0.08 | -0.3 | 6.9 |  |  |  | **no** | no |
| 88 | GB Bank Limited | EXCL | 94.21 | 94.25 | 0.04 | 0.0 | 33.2 | 0.63 | 160.40 | -160.36 | **no** | no |
| 89 | Clydesdale Bank PLC | EXCL | 5.10 | 5.10 | 0.00 | 0.0 | -0.6 | 0.13 | 0.78 | -0.78 | yes | yes |


### Banks with no boundary comparison (56)

Listed for completeness — a blank side cannot carry the defect, and the 14
marked "already split across labelled basis rows" are banks that have **already
had the correct treatment applied** (Arbuthnot, Hampden, Handelsbanken, Metro,
Monzo, RBC Europe, RBS plc, SBI UK, StreamBank, TSB, BNY Mellon International,
plus Barclays Bank UK Group / CAF / Clydesdale / Santander UK / OakNorth /
SMBC / Starling / Castle Trust / Allica / UBA UK / GIB UK in the crossing set).

| Bank | FY2021 | FY2022 | ratio rows | bases present | why no boundary comparison |
|---|---|---|---:|---|---|
| AIB Group (UK) p.l.c. | 11.26 |  | 1 | UNSPEC | FY2022 blank (no disclosure found) |
| Afin Bank Limited |  |  | 1 | EXCL | neither year populated |
| Aldermore Bank PLC |  | 8.1 | 1 | EXCL | FY2021 blank (no disclosure found) |
| Alpha Bank London Limited |  |  | 1 | UNSPEC | neither year populated |
| Arab Bank Europe Plc |  | 11.7 | 1 | EXCL | FY2021 blank (no disclosure found) |
| Arbuthnot Latham & Co., Limited |  | 6.0 | 3 | EXCL/INCL/UNSPEC | already split across labelled basis rows |
| Bank Mandiri (Europe) Limited |  |  | 1 | UNSPEC | neither year populated |
| Bank Saderat Plc |  |  | 1 | UNSPEC | neither year populated |
| Bank of Beirut (UK) Ltd |  | 22.88 | 1 | EXCL | FY2021 blank (no disclosure found) |
| Bank of Ceylon (UK) Limited | 46.2 |  | 1 | UNSPEC | FY2022 blank (no disclosure found) |
| Bank of Scotland plc |  | 4.5 | 1 | UNSPEC | FY2021 blank (no disclosure found) |
| Bank of the Philippine Islands (Europe) PLC |  |  | 1 | UNSPEC | neither year populated |
| Brown Shipley & Co. Limited |  |  | 1 | EXCL | neither year populated |
| Cater Allen Limited |  |  | 1 | UNSPEC | neither year populated |
| Charter Court Financial Services Limited |  | 7.9 | 1 | UNSPEC | FY2021 blank (no disclosure found) |
| Close Brothers Limited |  |  | 1 | UNSPEC | neither year populated |
| Coutts & Company |  | 7.7 | 1 | UNSPEC | FY2021 blank (no disclosure found) |
| Credit Suisse (UK) Limited |  |  | 1 | UNSPEC | neither year populated |
| EFG Private Bank Limited |  |  | 1 | EXCL | neither year populated |
| FCE Bank Plc |  | 13.23 | 1 | EXCL | FY2021 blank (no disclosure found) |
| FidBank UK Limited |  | 35.78 | 1 | UNSPEC | FY2021 blank (no disclosure found) |
| Griffin Bank Limited |  |  | 1 | EXCL | neither year populated |
| HSBC Innovation Bank Limited |  | 11.7 | 1 | UNSPEC | FY2021 blank (no disclosure found) |
| Hampden & Co Plc |  |  | 4 | EXCL/INCL/UNSPEC | already split across labelled basis rows |
| Handelsbanken plc | 7.3 |  | 2 | EXCL/UNSPEC | already split across labelled basis rows |
| Havin Bank Limited |  |  | 1 | UNSPEC | neither year populated |
| ICICI Bank UK Plc |  | 14.05 | 1 | EXCL | FY2021 blank (no disclosure found) |
| J.P. Morgan Europe Limited |  |  | 1 | UNSPEC | neither year populated |
| Kingdom Bank Limited | 10.4 |  | 1 | EXCL | FY2022 blank (no disclosure found) |
| LHV Bank Limited |  |  | 1 | UNSPEC | neither year populated |
| Marks and Spencer Financial Services plc |  |  | 1 | UNSPEC | neither year populated |
| Melli Bank plc |  |  | 1 | UNSPEC | neither year populated |
| Metro Bank PLC |  |  | 2 | EXCL/INCL | already split across labelled basis rows |
| Monzo | 29.3 |  | 3 | EXCL/INCL/UNSPEC | already split across labelled basis rows |
| Nomura Bank International plc |  |  | 1 | UNSPEC | neither year populated |
| Paragon Bank Plc |  |  | 1 | UNSPEC | neither year populated |
| Perenna Bank PLC |  | 91.05 | 1 | UNSPEC | FY2021 blank (no disclosure found) |
| Persia International Bank Plc | 53.32 |  | 1 | UNSPEC | FY2022 blank (no disclosure found) |
| Philippine National Bank (Europe) Plc |  |  | 1 | UNSPEC | neither year populated |
| RBC Europe Limited | 3.51 |  | 2 | EXCL/INCL | already split across labelled basis rows |
| RCI Bank UK Limited |  | 11.1 | 1 | EXCL | FY2021 blank (no disclosure found) |
| Rathbones Investment Management Limited |  |  | 1 | UNSPEC | neither year populated |
| Recognise Bank Limited |  | 34.3 | 1 | EXCL | FY2021 blank (no disclosure found) |
| Santander Financial Services plc |  |  | 1 | UNSPEC | neither year populated |
| Schroder & Co. Limited |  |  | 1 | UNSPEC | neither year populated |
| State Bank of India (UK) Limited |  | 14.25 | 3 | EXCL/UNSPEC | already split across labelled basis rows |
| StreamBank PLC |  |  | 2 | EXCL/INCL | already split across labelled basis rows |
| THIS BANK LIMITED |  |  | 1 | UNSPEC | neither year populated |
| TSB Bank plc |  |  | 3 | EXCL/INCL | already split across labelled basis rows |
| The Bank of London Group Limited |  |  | 1 | UNSPEC | neither year populated |
| The Bank of New York Mellon (International) Limited | 6.1 |  | 2 | EXCL/UNSPEC | already split across labelled basis rows |
| The Royal Bank of Scotland Public Limited Company |  | 6.4 | 2 | EXCL/INCL | already split across labelled basis rows |
| Turkish Bank (UK) Limited |  |  | 1 | INCL | neither year populated |
| Vida Bank Limited |  |  | 1 | EXCL | neither year populated |
| Zempler Bank Limited |  | 9.07 | 1 | UNSPEC | FY2021 blank (no disclosure found) |
| Zopa Bank Limited |  | 14.34 | 1 | EXCL | FY2021 blank (no disclosure found) |


## PHASE 2 — verification queue

Worked in this order. A jump is **not** proof: the bank may genuinely have
deleveraged, raised capital or shrunk. The decisive evidence is the **total
exposure measure** and the presence of UK KM1 row 14b ("leverage ratio including
claims on central banks") — row 14b only needs to exist once the exclusion
applies.

### Tier 1 — undocumented, material, with a decisive tell available

| Bank | Δ pp | Signal | Script | Status |
|---|---:|---|---|---|
| Bank of Ireland (UK) Plc | +1.90 | exposure measure −25.9% while ratio +26.4% | `build_bank_of_ireland.py` | pending |
| Crown Agents Bank Limited | +1.90 | 41% of assets are central-bank balances; no note | `build_crown_agents_bank.py` | pending |
| Northern Bank Ltd (Danske) | +2.50 | +59.5% relative, 25-33% reserves, **no note at all** | `build_northern_bank.py` | pending |
| NatWest Markets Plc | +1.10 | exposure measure −26.7% | `build_natwest_markets.py` | pending |
| HBL Bank UK Limited | +3.60 | +38.3% relative, residual +1.68 | `build_hbl_bank_uk.py` | pending |
| Julian Hodge Bank Limited | +2.60 | +31.3%, reserves 24%→6% | `build_julian_hodge_bank.py` | pending |
| Cynergy Bank Plc | +1.94 | +35.5% relative | `build_cynergy_bank.py` | pending |
| Weatherbys Bank Limited | +1.93 | +57.3% relative, no note | `build_weatherbys.py` | pending |
| J.P. Morgan Securities plc | +1.93 | +33.6%, exposure −11.0% | `build_jp_morgan_securities.py` | pending |
| Kuwait Finance House Plc | +1.80 | +17.1%, reserves 16% | `build_kuwait_finance_house.py` | pending |

### Tier 2 — the mirrored defect (new-basis label over old-basis figures)

41 banks carry an EXCL-labelled ratio row with pre-2022 values. For the large
UK ring-fenced/LREQ banks (Santander UK, Clydesdale, Standard Chartered,
Co-operative Bank, Barclays Bank UK, HSBC UK, NatWest) that is legitimate — the
UK leverage framework with the central-bank exclusion has applied to them since
2016/2018, so their series really is continuous. For the small non-LREQ banks it
is not, and these are the ones to check:

| Bank | EXCL label spans | Δ pp | Predicted | Script | Status |
|---|---|---:|---:|---|---|
| GB Bank Limited | FY2021 | +0.04 | +160.4 (63% reserves) | `build_gb_bank.py` | pending |
| National Bank of Kuwait (Intl) | FY2021 | +0.35 | +2.32 | `build_national_bank_of_kuwait_international.py` | pending |
| Cambridge & Counties (UNSPEC) | — | +1.02 | +3.39 | `build_cambridge_and_counties.py` | pending |
| DF Capital Bank Limited | FY2020-21 | −3.60 | +4.79 | `build_df_capital.py` | pending |
| Gatehouse Bank Plc | FY2017, FY2021 | −1.70 | — | `build_gatehouse.py` | pending |
| ABC International Bank plc | FY2017-FY2021 | −1.49 | — | `build_abc_international_bank.py` | pending |
| Oxbury Bank Plc | FY2021 | −2.83 | — | `build_oxbury.py` | pending |
| Reliance Bank Limited | FY2019-FY2021 | +3.10 | +2.57 | `build_reliance_bank.py` | pending |
| ICBC (London) plc (UNSPEC) | — | +1.00 | +2.30 | `build_icbc_london.py` | pending |
| Union Bancaire Privée (UK) | FY2021 | +0.20 | +1.06 | `build_union_bancaire_privee_uk.py` | **LOCKED** |

### Deferred — script locked by another agent (report only, do not edit)

Credit Suisse International (+5.04), FirstBank UK (+3.01), Itau BBA
International (−2.70), United National Bank (−2.54), Bank of Africa UK (+2.47),
Atom Bank (+2.70, documented), Vanquis (+2.90, documented), Chetwood (−8.82,
documented), SMBC (+4.70, documented + dual rows), HSBC UK (+1.70, documented),
Unity Trust (+1.49, documented), Zenith (−1.04, documented), United Trust Bank
(−0.20, documented), UBP UK (+0.20, undocumented), Methodist Chapel Aid (+0.44),
AIB Group UK (FY2022 blank), Melli / Philippine National Bank Europe / Arab Bank
Europe / Recognise / FCE / Hampden / NatWest Group scripts / TSB / GIB UK.

## PHASE 2/3 — verification and fixes (2026-09-16)

Seven banks taken all the way to primary documents. Every PDF was downloaded and
checked before reading: `%PDF` magic bytes, a real `pdfinfo` page count, and
none at the 1,048,576-byte Wayback truncation size. **Three-way split: 3 real
basis breaks, 2 genuine changes in the bank, 1 already-correct, plus 1 unrelated
defect found while checking.**

### VERDICT 1 — real basis break presented as a continuous series (3 banks, all fixed)

**Julian Hodge Bank Limited** — the cleanest case in the estate, and it is
demonstrated entirely by the Bank's own template. Its FY2022 and FY2023 Pillar 3
documents both print Template UK LRCom in full:

| 30 Sep | row 24 incl. CB | UK-24a excluded | UK-24b excl. CB | row 25 ratio excl. | UK-25c ratio incl. |
|---|---:|---:|---:|---:|---:|
| 2021 | 1,731 | (411) | 1,320 | 10.9% | 8.3% |
| 2022 | 1,852 / 1,851.6 | (228) / (228.4) | 1,624 / 1,623.2 | 10.9% | 9.6% |
| 2023 | 1,803.7 | (153.9) | 1,649.9 | 10.5% | 9.6% |

The workbook had FY2021 8.3% (incl.) and FY2022 10.9% (excl.) on ONE unlabelled
row — a 2.6pp "improvement" that is entirely the denominator. Held on either
basis consistently the ratio did not improve at all (10.9% → 10.9% excluding;
8.3% → 9.6% including). The Bank's own narrative states the cause: "The PRA's UK
Leverage Ratio framework that came into force from 1 January 2022, allows
institutions within its scope to exclude assets held with the Bank of England
from their leverage calculations." The workbook's existing note called the
1,320 vs 1,732.2 gap a "genuine cross-vintage restatement" without identifying
it — which is exactly how this defect hides.
*Fixed*: four labelled rows (excl. exposure/ratio, incl. exposure/ratio), full
note, Overview switched to the including-basis series (the only one comparable
across FY2016-FY2023) with its own note. `build_julian_hodge_bank.py`.

**Northern Bank Limited (trading as Danske Bank)** — the bank says it outright.
FY2022 Annual Report p.52: *"On 8 October 2021, the FPC and PRA jointly published
PS21/21 'The UK Leverage Ratio Framework', with an implementation date for
certain requirements of 1 January 2022… In addition, the leverage exposure
measure excludes central bank reserves and the government guaranteed lending
through Bounce Bank [sic] Loans (BBLs). **This has resulted in an increase in the
leverage ratio to 6.7% at 31 December 2022 (2021: 4.2%).**"* The workbook carried
5.2% / 4.2% / 6.7% / 7.4% / 7.2% / 6.4% as one row with **no note at all**.
Note the exclusion is two items, not one — BBL lending as well as reserves.
*Fixed*: two labelled rows (FY2020-FY2021 incl., FY2022-FY2025 excl.), note
quoting the Bank, Overview note added. `build_northern_bank.py`.

**Bank of Ireland (UK) Plc** — break proven, cause strongly indicated but NOT
stated by the Group. It publishes no Pillar 3 since FY2020, and its Annual
Reports print the same definition unchanged every year ("tier 1 capital divided
by total balance sheet assets and off balance sheet exposures"). That definition
cannot produce its own FY2022 and FY2023 numbers:

| | total assets | leverage exposure | exposure − assets | cash at central banks |
|---|---:|---:|---:|---:|
| FY2021 | 22,705 | 22,879 | **+174** | 3,456 |
| FY2022 | 18,871 | 16,948 | **−1,923** | 2,239 |
| FY2023 | 18,832 | 16,678 | **−2,154** | 2,213 |

Off-balance-sheet exposures cannot be negative, so something was removed from
FY2022. Subtracting the Group's own central bank balances reconciles both later
years to the same small positive adjustment FY2021 shows (18,871 − 2,239 =
16,632 vs 16,948 reported, +316; 18,832 − 2,213 = 16,619 vs 16,678, +59). The
ratio rose 7.2% → 9.1% while fully-loaded Tier 1 capital FELL, £1,647m → £1,544m.
There is also genuine deleveraging here (assets −17%) — both things are true.
*Fixed*: four labelled rows plus a note that states plainly which part is proven
(the break) and which is indicated (the central-bank cause), and that the Group
never says so. `build_bank_of_ireland.py`.

### VERDICT 2 — genuine change in the bank, no defect (2 banks, cleared and recorded)

**Crown Agents Bank Limited** (+1.90pp, 5.0% → 6.9%) — a false positive of the
reserve-intensity screen, and instructive as to why. CAB was ALREADY excluding
central bank claims before 2022: its FY2021 Pillar 3 Table LR Sum carries "Less:
central bank exposures (160,863)" for 2021 and "(125,844)" for 2020, citing
PS21/17 *UK leverage ratio: treatment of claims on central banks (October 2017)*.
Same basis both sides. The rise is real — Tier 1 up 59% (£56,595k → £89,871k)
against exposure up 13% — and the bank attributes it to "current year profit
being included in the Capital resources". **The screen also over-predicted
because the exclusion is capped at deposits in the same currency**: at 31 Dec
2022 CAB's BoE reserve account held £608,298k but only £189,334k was excluded.
Any reserve-share estimate that ignores that cap overstates the expected jump —
which is why GB Bank's "predicted +160pp" and Kroo's "+56.9pp" in the Phase 1
table are meaningless.
*Recorded*: a cleared-note added to the sheet so this is not "fixed" later.
`build_crown_agents_bank.py`.

**HBL Bank UK Limited** (+3.60pp, 9.41% → 13.01%) — also a capital increase. Both
Pillar 3 editions state the same CRR Article 451 definition with no
central-bank-exclusion line, and the exposure measure barely moved (£546,542k →
£543,633k, −0.5%); the FY2022 edition's FY2021 comparative is identical to
FY2021's own report, so there is no restatement. Tier 1 rose ~37%.
*Recorded*: cleared-note added. `build_hbl_bank_uk.py`.

### VERDICT 3 — already correct (1 bank)

**GB Bank Limited** — flagged by the screen as "flat when it should have jumped"
(Δ +0.04pp against a nonsense +160pp prediction). Not a defect: both FY2022 and
FY2021 come from the SAME UK KM1 table in the FY2022 Pillar 3 (p.11), under the
bank's own "excluding claims on central banks" heading — 23,445 / 17,606 and
94.25% / 94.21%. The workbook's EXCL label is the bank's own label from a single
template. No change made.

### An unrelated defect found while checking — Reliance Bank Limited

Not a basis break, but worse, and found only because this sweep opened the
documents. Two problems:
1. **The row label was simply wrong.** It read "Leverage ratio excluding claims
   on central banks". Neither located Pillar 3 edition (31 Mar 2022, 31 Mar 2023)
   uses that basis or wording — both print "Basel III Leverage Ratio" with no
   central-bank-exclusion line anywhere in the template.
2. **The Bank's own Pillar 3 series disagrees with the row, materially.** Pillar
   3 gives 4.45% (31 Mar 2021), 5.08% (31 Mar 2022), 7.90% (31 Mar 2023). The row
   shows 4.50%, 7.6%, 11.5% — figures that appear in neither document.

*Action*: the unsupported label was **withdrawn** (not replaced — the basis of
the Annual Report KPI figures is not established either way, and asserting the
opposite would repeat the error), and both problems recorded in full on the
sheet and on the Overview. **No figure was changed.** This needs its own pass to
establish which source feeds each year and to split the Pillar 3 series onto its
own row. `build_reliance_bank.py`.

### Files changed (6 scripts, all rebuilt, sheet count unchanged at 18)

`build_julian_hodge_bank.py`, `build_northern_bank.py`,
`build_bank_of_ireland.py`, `build_crown_agents_bank.py`,
`build_hbl_bank_uk.py`, `build_reliance_bank.py`. No commit made. `refresh_all.py`
NOT run, test suite NOT run, per the ticket.

## Correction to the Phase 1 headline counts

The "basis documented" column in the ranked table above is **too strict** — it
required the literal words "central bank". Re-run with a broader test (any of:
central bank / not comparable / basis break / methodology / predates / pre-2022 /
pre-KM1 / CRR leverage / UK leverage / leverage framework / as originally
reported / own basis):

| | banks |
|---|---:|
| Boundary-crossing | 89 |
| Sheet carries NO basis language at all | **23** (not 49) |
| …of those, material (>1.5pp or >25%) | 14 |

NatWest Markets and Crown Agents were both mis-flagged as undocumented by the
strict test; NatWest Markets in fact already carries "FY2021 uses the CRR
leverage ratio; FY2022 onward uses the PRA UK leverage-ratio presentation. These
bases are not directly comparable." **The estate is substantially better
documented than the ticket assumed.**

## Still open — ranked remainder of the queue

Not yet opened against primary documents. Highest value first:

| Bank | Δ pp | Why still interesting | Script |
|---|---:|---|---|
| Morgan Stanley Bank International | −11.60 | no basis language; but CB reserves ~1% of assets, so likely genuine | `build_morgan_stanley_bank_international.py` |
| KEXIM Bank (UK) | −6.30 | no basis language; sourced from the bank's own accounts table, not KM1 | `build_kexim_bank_uk.py` |
| Jordan International Bank | −4.10 | **no note of any kind on the sheet** | `build_jordan_international_bank.py` |
| Kuwait Finance House | +1.80 | FY2021+FY2022 both from ONE table (AR2022 p.72) — check if that comparative is restated | `build_kuwait_finance_house.py` |
| Cambridge & Counties | +1.02 | 21% reserves, jump smaller than expected | `build_cambridge_and_counties.py` |
| National Bank of Kuwait (Intl) | +0.35 | EXCL label on FY2021 from an ARCHIVED Pillar 3 — verify the label is the bank's | `build_national_bank_of_kuwait_international.py` |
| ICBC (London) | +1.00 | 7% reserves, no basis language | `build_icbc_london.py` |
| Co-operative Bank | +0.30 | EXCL label spans FY2014-FY2021; not an LREQ firm, so check | `build_coop_bank.py` |
| QIB (UK) / OneSavings / Gatehouse / ABC International / Oxbury / DF Capital | ≤3.6 | EXCL label over pre-2022 years at small non-LREQ banks (mirror shape) | various |

**Deferred — script locked by another agent, findings reported but NOT edited**:
Credit Suisse International (+5.04, no basis language), FirstBank UK (+3.01, no
basis language), Itau BBA International (−2.70, no basis language), United
National Bank (−2.54, no basis language), Bank of Africa UK (+2.47), UBP UK
(+0.20 against a predicted +1.06, EXCL label on FY2021), Methodist Chapel Aid
(+0.44), AIB Group UK (FY2022 blank). Atom, Vanquis, Chetwood, SMBC, HSBC UK,
Unity Trust, Zenith and United Trust Bank all already carry basis language and
need no work.

## Findings log
