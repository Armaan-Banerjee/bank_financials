# Corpus-wide arithmetic tie-out sweep — RESUME checkpoint

Started 2026-09-16. Follow-up to `research/RESUME_posthoc_columns.md`, whose
closing conclusion was:

> "The cheapest test is arithmetic, not provenance. Every one of the three
> defects was visible from the column's own internal sums before any document
> was opened. A 'does each historical column tie to its own printed totals?'
> check would have caught all three."

This sweep builds that check and runs it over every bank, every
statement-shaped sheet, every year column.

## The checker

`scripts/insights/tieout_check.py` (+ `scripts/insights/tieout_report.py`).
Reads the **workbooks on disk**, not `research/insights.db` — the database was
a day stale during the leverage sweep, with 50 workbooks rebuilt since.

Row kinds are recovered from the saved file exactly as
`bank_workbook._add_statement_sheet` writes them: SECTION = bold in column 1
only, TOTAL = bold in every column, DATA = not bold.

Scope: 145 workbooks × 5 sheets (Balance Sheet, Profit & Loss, Cash Flow
Statement, Asset Quality, RWA Breakdown) × every year column × every
TOTAL-tagged row.

### Legitimate non-ties the checker is built to recognise, not flag

A naive "sum every DATA row since the last divider" rule is useless on this
corpus — the first draft produced 1,990 flags, almost all spurious. Each TOTAL
is therefore tested against several candidate compositions and only reported
when none fits:

| id | composition | the case it exists for |
|---|---|---|
| A | DATA rows since the last boundary (SECTION or TOTAL) | the default reading |
| B | DATA rows since the last SECTION, ignoring nested TOTALs | flat statements |
| C | the last preceding TOTAL + the DATA rows after it | `Total equity = Equity attributable to owners + NCI` |
| D | any small subset of preceding TOTAL rows (+ trailing DATA) | `Total equity and liabilities = Total liabilities + Total equity` |
| E | signed combinations — differences, not sums | `Net carrying amount = Total gross − Total ECL`; `Net fee income = income − expense` |

On top of that:

- **Nested subtotals.** Handled by A/C/D above. This is the NBE shape the
  brief warned about, and it was the single largest false-positive source:
  a breakdown block carrying both its category rows *and* its own total, all
  tagged DATA (Aldermore's `Total debt securities` over six FVOCI/amortised-cost
  lines produced a spurious 13% gap in Total assets). `mark_breakdown_children`
  detects these **arithmetically** — a contiguous run of DATA rows that sums to
  the DATA row next to it, in *every* year the two share — rather than by
  label, so it catches breakdowns whose parent isn't called "Total …". Two
  shared years are required before a run is written off as a breakdown, so a
  genuine peer line item can't be silently swallowed by one coincidental match.
- **"Of which" rows** are subsets of the line above and are never summed in
  (`of which` / `o/w` / `thereof` / `including` / `comprising`).
- **Rounding.** Tolerance is half a unit per summed row, floor 1.0, plus a
  0.05% relative allowance for a source printed in a coarser unit than the
  sheet (£m source on a £'000 sheet).
- **Sign conventions.** A source printing expenses positive under a negative
  total is recorded as `TIES_SIGN`, not a defect.
- **Bolded leaf line items.** A source sometimes emphasises an ordinary line
  (FCE Bank's `Operating expenses` sits *between* `Allowance for ECL` and
  `Profit before tax` and is a peer of both, not their subtotal). Tagged TOTAL
  it guarantees a false positive AND breaks the subtotal below it. 52 such
  rows are demoted corpus-wide before checking.
- **Sparse columns.** Every finding carries a `blanks` count: DATA rows in the
  span that hold no figure that year. A high blank count means the column is
  merely incomplete; **`blanks = 0` with a material residual is the Gatehouse
  shape** — every row populated and the column still doesn't add up.

### Checker validation

Reverting the 2026-09-16 Gatehouse fix on a scratch copy (deleting the
`Due from financial institutions` row and blanking the FY2017 derivative
liability) reproduces the defect exactly:

```
MISMATCH   Total assets       tot=280,526  sum=203,274  resid=77,252  pct=27.54%  blanks=0
MISMATCH   Total liabilities  tot=153,065  sum=152,558  resid=507     pct=0.33%   blanks=0
```

27.54% at the top of the ranking, as the brief predicted.

## PHASE 1 — full ranked results

## Status counts (bank / sheet / year / total-row checks)

| status | checks |
|---|---:|
| TIES | 10,693 |
| TIES_NESTED | 8,832 |
| MISMATCH | 931 |
| TIES_ROUNDING | 917 |
| STRUCTURE_UNCLEAR | 604 |
| NO_COMPONENTS | 366 |
| TIES_NESTED_SIGN | 49 |
| TIES_SIGN | 28 |
| **total** | **22,420** |

### MISMATCH — no sane composition fits — 302 signatures, ranked by worst-year %

| % | abs residual | yrs | bank | sheet | worst year | TOTAL row | total | sum of DATA | blanks |
|---:|---:|---:|---|---|---|---|---:|---:|---:|
| 100.00% | 61,740 | 3 | HAMPDEN & CO | Cash Flow Statement | FY2021 (£'000) | Net cash from/(used in) operating activities | 61,740 | 0 | 0 |
| 100.00% | 5,422,322 | 7 | RBC EUROPE | Cash Flow Statement | FY2022 (£'000) | Net decrease/increase in cash and cash equivalents before exchange-rat | 5,422,322 | 0 | 0 |
| 99.99% | 33,144 | 9 | ABC INTERNATIONAL BANK | Profit & Loss | FY2017 (£'000) | Total comprehensive income for the year attributable to owners | 19,965 | 2 | 4 |
| 99.91% | 11,425 | 7 | C HOARE AND CO | Profit & Loss | FY2025 (£'000) | Net fees and commissions income | 9,631 | 19,253 | 0 |
| 99.64% | 832 | 1 | BANK OF SCOTLAND | Profit & Loss | FY2024 (£m) | Total comprehensive income for the year, net of tax | 835 | 3 | 0 |
| 99.53% | 30,771.7 | 4 | TSB | Asset Quality | FY2016 (£m) | Total gross customer lending balances | 29,492.8 | 140 | 4 |
| 99.48% | 8,499 | 2 | RBC EUROPE | Asset Quality | FY2023 (£'000) | Closing balance | 8,543 | 44 | 1 |
| 99.48% | 158,671.6 | 5 | BANK SEPAH INTERNATIONAL | Cash Flow Statement | FY2021 (£'000, conv. from EUR) | Cash and cash equivalents at the end of the year | 159,502.1 | 830.5 | 2 |
| 99.32% | 9,551 | 5 | THIS BANK | Profit & Loss | FY2025 (£'000) | Loss before tax | -9,616 | -19,167 | 0 |
| 99.32% | 9,551 | 5 | THIS BANK | Profit & Loss | FY2025 (£'000) | Total comprehensive loss for the year, net of tax | -9,616 | -19,167 | 0 |
| 99.30% | 288 | 16 | FCE BANK | Profit & Loss | FY2023 (£m) | Operating expenses | -287 | -2 | 0 |
| 99.22% | 7,267 | 1 | ITAU BBA INTERNATIONAL | Cash Flow Statement | FY2016 (USD'000) | Increase/(decrease) in cash and cash equivalents | 7,324 | 57 | 0 |
| 98.02% | 39,845 | 1 | ALPHA BANK LONDON | Cash Flow Statement | FY2022 (£'000) | Net cash flows used in operating activities | -40,650 | -805 | 0 |
| 97.96% | 108,848 | 1 | CYNERGY BANK | Cash Flow Statement | FY2015 (£'000) | Net (decrease)/increase in cash and cash equivalents for the year | -111,119 | -2,271 | 0 |
| 97.82% | 12,054,488 | 9 | METHODIST CHAPEL AID | Balance Sheet | FY2016 (£) | Net Assets | 11,071,512 | 21,901,157 | 0 |
| 97.44% | 27,855 | 2 | HAMPSHIRE TRUST BANK | Profit & Loss | FY2019 (£'000) | Administrative expenses | -28,587 | -732 | 0 |
| 97.44% | 6,734,056 | 1 | UNITED NATIONAL | Profit & Loss | FY2023 (£) | Profit before tax on ordinary activities | 6,911,228 | 177,172 | 1 |
| 97.42% | 247,058 | 2 | FIRSTBANK UK | Cash Flow Statement | FY2021 ($'000, FY2021 conv. from £) | Net increase/(decrease) in cash and cash equivalents | -253,589 | -6,531 | 0 |
| 96.67% | 4,706,175 | 12 | UNION BANCAIRE PRIVEE UK | Balance Sheet | FY1985 (£'000) | Total liabilities and equity | 2,756,321 | 91,781 | 0 |
| 96.12% | 7,466 | 2 | COUTTS | Cash Flow Statement | FY2024 (£m) | Changes in operating assets and liabilities | 7,767 | 301 | 10 |
| 95.95% | 30,361 | 1 | VIDA | Profit & Loss | FY2019 (£'000) | Administrative expenses | -31,642 | -1,281 | 0 |
| 95.62% | 809,123.9 | 2 | ARAB BANK EUROPE | Asset Quality | FY2024 (£'000, conv. from EUR) | Net loans and advances to customers | 846,188.9 | 37,065 | 0 |
| 95.58% | 99.4 | 9 | SECURE TRUST BANK | Profit & Loss | FY2021 (£m) | Operating expenses | -104 | -4.6 | 1 |
| 95.27% | 994,268 | 3 | NORTHERN BANK | Cash Flow Statement | FY2022 (£'000) | Net change in cash and cash equivalents | -1,043,645 | -49,377 | 0 |
| 94.97% | 5,528 | 1 | JORDAN INTERNATIONAL BANK | Profit & Loss | FY2016 (£'000) | Profit before taxation | 5,821 | 293 | 1 |
| 94.87% | 41,511,790 | 1 | GHANA INTERNATIONAL BANK | Cash Flow Statement | FY2019 (£) | (Decrease)/increase in cash and cash equivalents | -43,756,973 | -2,245,183 | 0 |
| 94.74% | 6,816,158 | 6 | CITIBANK UK | Balance Sheet | FY2021 (£'000) | Total liabilities (incl. equity - see sources) | 7,194,284 | 378,126 | 0 |
| 94.20% | 6.5 | 1 | ALLICA | Profit & Loss | FY2025 (£m) | Net fee and commission income/(expense) | -6.9 | -0.4 | 0 |
| 93.99% | 344,186,215 | 2 | GHANA INTERNATIONAL BANK | Balance Sheet | FY2024 (£) | Total government and other securities | 366,183,607 | 710,369,822 | 0 |
| 93.81% | 1,028.3 | 1 | TSB | Profit & Loss | FY2017 (£m) | Total income | 1,096.1 | 67.8 | 0 |
| 93.77% | 353,180.9 | 1 | ACCESS BANK UK | Cash Flow Statement | FY2019 (£'000, conv. from USD) | Cash and cash equivalents at the end of the year | 376,653.1 | 23,472.2 | 2 |
| 93.48% | 12.9 | 1 | SMBC | Profit & Loss | FY2026 (£m, conv. from USD) | Other comprehensive income, net of tax | -13.8 | -0.9 | 2 |
| 92.70% | 66,318 | 2 | RBC EUROPE | Cash Flow Statement | FY2018 (£'000) | Net cash inflow/(outflow) from financing activities | 71,542 | 137,860 | 4 |
| 92.65% | 19,103.6 | 1 | ALDERMORE | Balance Sheet | FY2025 (y/e 30 Jun 25) (£m) | Total liabilities and equity | 20,618.2 | 1,514.6 | 0 |
| 92.26% | 1,518,932 | 1 | UNITED TRUST BANK | Asset Quality | FY2020 (£'000) | Net loans and advances to customers | 1,646,322 | 127,390 | 3 |
| 92.26% | 1,527,058 | 1 | UNITED TRUST BANK | Asset Quality | FY2020 (£'000) | Gross loans and advances to customers | 1,655,224 | 128,166 | 3 |
| 91.28% | 8,126 | 1 | UNITED TRUST BANK | Asset Quality | FY2020 (£'000) | Total provision for impairment losses | -8,902 | -776 | 3 |
| 91.26% | 129,268 | 1 | ITAU BBA INTERNATIONAL | Cash Flow Statement | FY2017 (USD'000) | Cash and cash equivalents at end of year | 141,646 | 270,914 | 0 |
| 90.94% | 261 | 1 | FCE BANK | Profit & Loss | FY2022 (£m) | Profit for the period | 287 | 26 | 1 |
| 90.39% | 4,523.4 | 8 | CO-OPERATIVE BANK | RWA Breakdown | FY2018 (£m) | Total | 5,004.3 | 480.9 | 5 |
| 90.30% | 703.7 | 1 | MIZUHO INTERNATIONAL | Cash Flow Statement | FY2021 (£m) | Cash and cash equivalents at beginning of the period | 779.3 | 75.6 | 0 |
| 89.96% | 61,070 | 5 | FIRSTBANK UK | Cash Flow Statement | FY2025 ($'000, FY2021 conv. from £) | Operating cash flow before changes in operating assets/liabilities | 60,231 | 6,048 | 0 |
| 89.76% | 7,885 | 3 | CLEARBANK | Profit & Loss | FY2020 (£'000) | Net fee income | 8,785 | 900 | 2 |
| 89.68% | 5,229.2 | 2 | PERSIA INTERNATIONAL BANK | Profit & Loss | FY2021 (£'000, conv. from EUR) | Total operating expenses | -5,830.8 | -601.6 | 1 |
| 89.38% | 527,571.4 | 5 | ACCESS BANK UK | Balance Sheet | FY2022 (£'000, conv. from USD) | Total investment securities | 590,237.8 | 1,117,809.2 | 2 |
| 89.28% | 92,427 | 4 | HBL BANK UK | Cash Flow Statement | FY2025 (£'000) | Net cash flows generated from/(used in) operating activities | -103,530 | -11,103 | 0 |
| 89.09% | 106,511,170 | 3 | GRIFFIN BANK | Balance Sheet | FY2025 (£) | Total assets | 119,551,420 | 226,062,590 | 0 |
| 88.08% | 72,536 | 4 | BANK OF SCOTLAND | RWA Breakdown | FY2025 (£m) | Total risk-weighted assets | 82,357 | 9,821 | 0 |
| 87.76% | 95,156 | 7 | UNION BANCAIRE PRIVEE UK | Profit & Loss | FY2001 (£'000) | Total operating income | 13,749 | 1,683 | 10 |
| 87.66% | 348 | 1 | LLOYDS BANK CORPORATE MARKETS | Profit & Loss | FY2019 (£m) | Profit for the year (Bank) | 397 | 745 | 0 |
| 87.53% | 423,569.2 | 1 | PUNJAB NATIONAL BANK INTERNATIONAL | Asset Quality | FY2017 (£'000, conv. from USD) | Net loans and advances to customers | 483,890.6 | 907,459.8 | 0 |
| 87.23% | 41 | 4 | SANTANDER FINANCIAL SERVICES | Cash Flow Statement | FY2022 (£m) | Net cash flows from operating activities | -47 | -88 | 0 |
| 85.97% | 1,034,860.9 | 15 | PUNJAB NATIONAL BANK INTERNATIONAL | Balance Sheet | FY2012 (£'000, conv. from USD) | Total assets | 749,172.1 | 105,085.4 | 4 |
| 85.09% | 13,927 | 4 | BARCLAYS BANK PLC | Cash Flow Statement | FY2023 (£m) | Net cash from operating activities | 16,367 | 2,440 | 0 |
| 83.54% | 22,844 | 1 | HAMPSHIRE TRUST BANK | Profit & Loss | FY2021 (£'000) | Profit before tax | 27,346 | 4,502 | 1 |
| 83.46% | 2,243,888 | 3 | RELIANCE BANK | Profit & Loss | FY2021 (£) | Operating income | 2,688,469 | 444,581 | 0 |
| 83.10% | 4,795 | 1 | GB BANK | Profit & Loss | FY2024 (£'000) | Profit/(loss) for the year/period | -5,770 | -10,565 | 1 |
| 81.62% | 3,309,782 | 7 | BNY MELLON INTERNATIONAL | Balance Sheet | FY2022 (£'000s) | Total investment securities | 4,054,942 | 7,364,724 | 0 |
| 81.24% | 28,054 | 5 | ZEMPLER | Asset Quality | FY2025 (£'000) | Net loans and advances to customers | 25,452 | 4,776 | 0 |
| 81.08% | 121,135 | 16 | BANK OF CHINA UK | Cash Flow Statement | FY2025 (£'000) | Net cash generated from operating activities | 111,252 | 21,045 | 5 |
| 78.81% | 35,366 | 6 | BRITISH ARAB COMMERCIAL BANK | Cash Flow Statement | FY2014 (£'000) | Non-cash items included in net profit | 6,993 | 12,504 | 3 |
| 76.28% | 2,612 | 4 | SANTANDER | Cash Flow Statement | FY2024 (£m) | Net cash flows from operating activities | -3,331 | -5,872 | 0 |
| 76.21% | 6,644 | 1 | IFAST GLOBAL BANK LIMITED | Profit & Loss | FY2022 (£'000) | Profit/(loss) from continuing operations | -8,718 | -15,362 | 0 |
| 75.97% | 5,701 | 5 | HSBC BANK PLC | Cash Flow Statement | FY2018 (£m) | Changes in operating assets and liabilities - subtotal | -670 | -161 | 1 |
| 75.97% | 7,071 | 5 | IFAST GLOBAL BANK LIMITED | Cash Flow Statement | FY2022 (£'000) | Net inflows/(outflows) from operating activities | -9,308 | -2,237 | 2 |
| 74.71% | 106,208 | 5 | STANDARD CHARTERED BANK | RWA Breakdown | FY2021 ($m) | Total risk weighted assets | 142,161 | 35,953 | 0 |
| 73.52% | 189,300 | 2 | UNION BANCAIRE PRIVEE UK | Balance Sheet | FY2006 (£'000) | Equity attributable to owners of the Company | 257,491 | 68,191 | 5 |
| 73.15% | 585 | 5 | LLOYDS BANK | Cash Flow Statement | FY2022 (£m) | Net cash used in financing activities | -406 | -109 | 0 |
| 72.88% | 215.5 | 6 | CO-OPERATIVE BANK | Profit & Loss | FY2021 (£m) | Total comprehensive income/(expense) for the year, net of tax | 295.7 | 80.2 | 0 |
| 71.48% | 10,085 | 3 | HAMPDEN & CO | Cash Flow Statement | FY2023 (£'000) | Cash generated from/(used in) operating activities | -14,109 | -24,194 | 0 |
| 70.35% | 72,374 | 3 | CYNERGY BANK | Cash Flow Statement | FY2014 (£'000) | Net cash flow generated from/(used in) operating activities | -85,437 | -25,329 | 2 |
| 68.75% | 312,867 | 2 | GHANA INTERNATIONAL BANK | Profit & Loss | FY2020 (£) | Total other comprehensive income/(loss) | 276,374 | 86,374 | 0 |
| 68.11% | 227.2 | 5 | TSB | Cash Flow Statement | FY2023 (£m) | Change in operating assets and liabilities (as reported) | 333.6 | 560.8 | 14 |
| 63.25% | 1,577.7 | 12 | SMBC | Cash Flow Statement | FY2021 (£m, conv. from USD) | Net cash from/(used in) operating activities | -2,494.4 | -4,072.1 | 4 |
| 61.75% | 1,396,719 | 4 | EFG PRIVATE BANK | Balance Sheet | FY2021 (£'000) | Total investment securities | 852,764 | 1,379,340 | 0 |
| 60.02% | 11,359 | 1 | EFG PRIVATE BANK | Profit & Loss | FY2023 (£'000) | Total other comprehensive income/(expense) for the year | 18,924 | 30,283 | 3 |
| 59.34% | 5,615.2 | 4 | STREAMBANK | Profit & Loss | FY2026 (£'000) | Total operating expenses (sum of Staff costs + Other operating expense | -9,462.4 | -3,847.2 | 0 |
| 57.69% | 43,646 | 9 | JORDAN INTERNATIONAL BANK | Cash Flow Statement | FY2016 (£'000) | Cash and cash equivalents at end of year | 75,659 | 119,305 | 0 |
| 57.01% | 19.1 | 1 | JULIAN HODGE BANK | Profit & Loss | FY2016 (£m) | Net operating income | 33.5 | 14.4 | 3 |
| 56.32% | 2,287 | 1 | OAKNORTH BANK | Cash Flow Statement | FY2015 (£'000) | Net cash flows generated from operating activities | -4,061 | -6,348 | 12 |
| 55.98% | 6,644 | 1 | IFAST GLOBAL BANK LIMITED | Profit & Loss | FY2022 (£'000) | Profit/(loss) for the year | -11,868 | -18,512 | 1 |
| 55.97% | 6,327 | 5 | HSBC UK BANK PLC | Cash Flow Statement | FY2022 (£m) | Net cash from operating activities | -9,692 | -15,117 | 0 |
| 55.61% | 70,254 | 1 | VIDA | Cash Flow Statement | FY2024 (£'000) | Net increase/(decrease) in cash and cash equivalents | 126,324 | 56,070 | 0 |
| 55.14% | 5,719 | 4 | BARCLAYS | Cash Flow Statement | FY2025 (£m) | Net cash from operating activities | -7,860 | -12,194 | 4 |
| 54.08% | 2,843 | 3 | RBS | Cash Flow Statement | FY2023 (£m) | Net cash flows from operating activities | -5,257 | -8,100 | 0 |
| 53.93% | 488.4 | 1 | TSB | Profit & Loss | FY2018 (£m) | Total operating expenses | -905.7 | -417.3 | 1 |
| 52.20% | 39,873 | 12 | ICBC (LONDON) PLC | Cash Flow Statement | FY2016 ($'000) | Net cash used in operating activities | -7,467 | -11,365 | 3 |
| 52.12% | 1.9 | 1 | CO-OPERATIVE BANK | Profit & Loss | FY1978 (£m) | Profit before taxation (and extraordinary item, FY1974) | 3.6 | 5.4 | 2 |
| 49.13% | 51.3 | 6 | ALLICA | Cash Flow Statement | FY2020 (£m) | Net cash from/(used in) operating activities | 40.2 | 59.9 | 6 |
| 46.50% | 2,797 | 2 | OXBURY | Profit & Loss | FY2020 (£'000) | Total Comprehensive Profit/(Loss) | -4,056 | -2,170 | 0 |

### STRUCTURE_UNCLEAR — needs a human read — 145 signatures, ranked by worst-year %

| % | abs residual | yrs | bank | sheet | worst year | TOTAL row | total | sum of DATA | blanks |
|---:|---:|---:|---|---|---|---|---:|---:|---:|
| 425964.33% | 4,813,630 | 8 | ITAU BBA INTERNATIONAL | Asset Quality | FY2025 (USD'000) | Total ECL provisions | -1,071 | 4,561,007 | 0 |
| 414737.00% | 4,825,425 | 8 | ITAU BBA INTERNATIONAL | Asset Quality | FY2025 (USD'000) | Total cash collateral | -1,100 | 4,561,007 | 0 |
| 412817.65% | 436,520 | 14 | NATIONAL WESTMINSTER BANK PLC | Balance Sheet | FY2015 (£m) | Other financial assets | 51 | 210,588 | 4 |
| 371018.18% | 579,400 | 4 | CITIBANK UK | Asset Quality | FY2023 (£'000) | Total ECL allowance, closing balance | -11 | 40,801 | 2 |
| 70718.60% | 140,991 | 10 | CREDIT SUISSE UK | Profit & Loss | FY2016 (£'000) | Total comprehensive income/(loss) for the year | -129 | -91,356 | 0 |
| 35922.06% | 533,039 | 4 | DF CAPITAL BANK | RWA Breakdown | FY2022 (£'000) | Counterparty credit risk (CCR), total | 1,029 | 370,667 | 0 |
| 32321.38% | 9,513,907 | 3 | BNY MELLON INTERNATIONAL | Balance Sheet | FY2016 (£'000s) | Total investment securities | 20,353 | 6,598,723 | 0 |
| 32001.47% | 1,766,745 | 6 | VIDA | Cash Flow Statement | FY2018 (£'000) | Net increase/(decrease) in cash and cash equivalents | -2,389 | 762,126 | 0 |
| 23268.17% | 294,575 | 5 | HBL BANK UK | Asset Quality | FY2025 (£'000) | Total provision for loan losses | 1,266 | 295,841 | 0 |
| 21130.62% | 26,780.6 | 4 | CO-OPERATIVE BANK | Asset Quality | FY2017 (£m) | Total allowance for losses (Impaired/Not impaired basis) | -80 | 16,824.5 | 0 |
| 18340.20% | 459,520.1 | 2 | UBA UK | Asset Quality | FY2024 (£'000, conv. from USD) | Total ECL allowance | 1,907.3 | 351,709.9 | 0 |
| 16780.51% | 32,722 | 5 | CLYDESDALE | Asset Quality | FY2018 (£m) | Total impairment provisions on credit exposures | 195 | 32,917 | 2 |
| 6177.78% | 143.9 | 4 | MIZUHO INTERNATIONAL | Cash Flow Statement | FY2025 (£m) | Effects of exchange rates on cash and cash equivalents | -0.9 | -56.5 | 0 |
| 5437.01% | 6.9 | 1 | ALLICA | Profit & Loss | FY2023 (£m) | Net fee and commission income/(expense) | -0.1 | 6.8 | 0 |
| 5144.44% | 556 | 7 | LLOYDS BANK CORPORATE MARKETS | Profit & Loss | FY2020 (£m) | Profit for the year (Bank) | 9 | 472 | 0 |
| 5071.05% | 622.7 | 14 | VANQUIS | Profit & Loss | FY2023 (£m) | Profit for the year | 7.6 | -377.8 | 1 |
| 5004.76% | 2,741 | 15 | CLYDESDALE | Profit & Loss | FY2011 (£m) | Profit on ordinary activities before tax | 21 | -1,030 | 2 |
| 4873.00% | 83,457 | 5 | STANDARD CHARTERED BANK | Asset Quality | FY2025 ($m) | Total expected credit loss | -1,678 | 80,091 | 0 |
| 4556.50% | 15,643.9 | 6 | UNION BANK OF INDIA UK | Cash Flow Statement | FY2018 (£'000, conv. from USD) | Cash flows before changes in working capital (excl. profit before tax  | 104.6 | 4,870.7 | 9 |
| 3817.01% | 18,755 | 4 | THE BANK OF LONDON GROUP | Asset Quality | FY2023 (£'000) | Total ECL provision (credit loss allowance) | -488 | 18,139 | 0 |
| 3476.93% | 834,115.9 | 5 | PUNJAB NATIONAL BANK INTERNATIONAL | Asset Quality | FY2014 (£'000, conv. from USD) | Total impairment provision | 20,789.9 | 743,640 | 0 |
| 3470.44% | 7,757.2 | 6 | PUNJAB NATIONAL BANK INTERNATIONAL | Profit & Loss | FY2024 (£'000, conv. from USD) | Other comprehensive income for the year, net of tax | 142.4 | 5,084.3 | 3 |
| 2710.17% | 14,899.7 | 9 | CREDIT SUISSE INTERNATIONAL | Cash Flow Statement | FY2025 (£m, conv. from USD) | Cash and cash equivalents at end of period | 265.5 | -6,930 | 0 |
| 2613.57% | 38,209 | 7 | BRITISH ARAB COMMERCIAL BANK | Cash Flow Statement | FY2023 (£'000) | Non-cash items included in net profit | 1,393 | 37,800 | 1 |
| 2600.41% | 568,425 | 10 | CYNERGY BANK | Cash Flow Statement | FY2025 (£'000) | Net cash flow generated from/(used in) operating activities | -17,143 | 428,646 | 2 |
| 1781.14% | 140,322 | 4 | OXBURY | Profit & Loss | FY2024 (£'000) | Total Comprehensive Profit/(Loss) | 5,863 | -98,565 | 0 |
| 1566.79% | 56,039 | 5 | DF CAPITAL BANK | Profit & Loss | FY2022 (£'000) | Profit/(loss) before taxation | 1,304 | -19,127 | 0 |
| 1528.49% | 692,927 | 5 | CHETWOOD | Balance Sheet | FY2022 (£'000) | Investment in debt securities - total | 4,883 | 79,519 | 0 |
| 1514.28% | 130,388 | 8 | UNION BANCAIRE PRIVEE UK | Profit & Loss | FY1996 (£'000) | Profit before income tax | -6,469 | -104,428 | 0 |
| 1457.72% | 157,769 | 1 | RBC EUROPE | Cash Flow Statement | FY2019 (£'000) | Net cash inflow/(outflow) from financing activities | -10,823 | 146,946 | 4 |


## PHASE 2 / PHASE 3 — verification and repair

(filled in below, one finding at a time, worst first)

