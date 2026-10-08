# Adding ROE / ROA / NIM / Cost of Risk / Cost of Funds — feasibility

Assessed 2026-10-08 (katalysis-49), from the two research workbooks plus a
measurement of all 145 delivered workbooks. Every number below is measured, not
estimated; the scripts used are inline in the session and the per-bank input map
is at `scratchpad/metric_inputs.json`.

## 1. What the two files actually contain

**`UK_Banks_Key_Metrics.xlsx`** — 145 banks × 5 metrics (Cost of Risk, Cost of
Funds, NIM, ROE/RoTE, ROA). **Every data cell reads `n/d`.** It is a populated
*template*, not populated *data*. Its "Notes & Methodology" sheet is genuinely
useful (definitions, caveats, a source list for the large banks), but there are
zero figures to import.

**`UK_banks_ROE_research.xlsx`** — 146 rows (the ALLICA duplicate is known and
deliberate), 6 year columns, each with its own "measure" label.

| | |
|---|---|
| banks marked "Located" | 78 of 146 |
| ROE values present | **97** |
| …of which year 2024 | 73 |
| 2025 / 2026 | 6 / 1 |
| 2023 / 2022 / 2021 | 10 / 4 / 3 |
| banks with 0 years | **72** |
| banks with 1 year | 63 |
| banks with ≥2 years | 11 |

Measure labels: 83 `ROE`, 6 `RoTE`, 3 `ROAE`, 2 `PBT ROE`, 2 `Underlying RoTE`,
1 `Reported ROE`. The file is honest about this and labels each one — good.

## 2. The finding that changes the question

**For ROE and ROA you do not mostly need to *find* anything. The inputs are
already transcribed in our own workbooks.**

Measured across all 145 workbooks, matching real row labels (banks write
"Profit on ordinary activities after taxation", "Owners' equity",
"Shareholder's funds", not one canonical phrase):

| metric | banks | bank-years |
|---|---:|---:|
| ROA (profit ÷ year-end total assets) | **138 / 145** | **1,195** |
| ROE (profit ÷ year-end equity) | **127 / 145** | **1,069** |
| ROE (profit ÷ *average* equity — needs two consecutive years) | — | **940** |
| NII present (NIM numerator) | 135 / 145 | 1,119 |
| Impairment charge present (Cost of Risk numerator) | 101 / 145 | 733 |

Against the research file's **97 values, 74 banks, mostly one year** — computing
from what we hold is roughly a **10× increase in coverage**, across the full
5–10 year span each workbook already carries rather than a single 2024 snapshot.

Scale is not an obstacle: a ratio of two figures from the same workbook cancels
the unit, and the year-column headers already declare it per sheet (`FY2024
(£m)`, `FY2024 (£'000s)`, `FY2024 (£'000, conv. from USD)`).

## 3. Does the computed figure reproduce the published one?

63 banks appear in both the research file (2024) and our workbooks with both
inputs. Computing profit ÷ average equity:

- **median |Δ| = 0.00pp**
- **50 of 63 within 0.5pp**, 52 within 1.0pp

**Read that agreement carefully — it is partly circular.** So many exact
0.00 hits suggest the research file's own values were computed the same way
(profit ÷ average equity), most likely by TheBanks.eu, which its method note
names as the source for most smaller-bank 2024 figures. It confirms our
transcriptions are consistent with that aggregator; it does **not** independently
confirm either against the banks' own published ROE.

The 13 divergences are the interesting part, and they fall into two groups:

**(a) A different measure, as labelled** — the non-ROE labels cluster here:
| bank | published | computed | Δ | label |
|---|---:|---:|---:|---|
| METRO BANK | −23.00 | +3.61 | **+26.6** | RoTE |
| SECURE TRUST BANK | 14.60 | 5.59 | −9.0 | ROAE |
| SHAWBROOK | 17.00 | 14.65 | −2.4 | Underlying RoTE |
| CLOSE BROTHERS | 9.30 | 8.60 | −0.7 | RoTE |

**(b) Unexplained — these are real leads:**
| bank | published | computed | Δ |
|---|---:|---:|---:|
| UNITED TRUST BANK | 20.10 | 1.79 | **−18.3** |
| GATEHOUSE BANK | 3.64 | −1.20 | −4.8 (**sign flip**) |
| ALRAYAN BANK | 11.40 | 8.61 | −2.8 |
| SHAWBROOK / NORTHERN BANK | 17.00 / 19.80 | 14.65 / 17.67 | −2.4 / −2.1 |
| NATIONAL BANK OF KUWAIT INTL | 6.29 | 8.44 | +2.2 |
| VANQUIS | 1.99 | 0.34 | −1.7 |
| COUTTS | 14.20 | 12.71 | −1.5 |

Each needs one document read. A sign flip (Gatehouse) and an 18pp gap (United
Trust) are the kind of thing that is either a defect in our transcription or a
defect in the aggregator — and under this project's rules we would record both
and reconcile neither.

## 4. Difficulty, metric by metric

| metric | difficulty | why |
|---|---|---|
| **ROA** | **easy** | 138/145 banks, 1,195 bank-years, inputs already held |
| **ROE** | **easy** | 127/145, 940 bank-years on an average-equity basis |
| **NIM** | **medium** | numerator present for 135 banks, but the correct denominator is *average interest-earning assets*, which most UK banks do not print. Total assets is a different metric and must be labelled as such, not called NIM |
| **Cost of Risk** | **medium–hard** | impairment charge present for only 101/145, and the denominator is *average gross loans*, which lives on the Asset Quality sheet with its own label variance |
| **Cost of Funds** | **hard / mostly impossible** | the Key Metrics notes are right: UK banks almost never disclose it. Derivable only as interest expense ÷ average interest-bearing liabilities, and most of these banks do not print the liability split that denominator needs |

## 5. The 14 banks with no matched ROE pair

`BANK OF CEYLON UK, BNY MELLON INTERNATIONAL, CASTLE TRUST CAPITAL, CITIBANK UK,
EFG PRIVATE BANK, ICBC (LONDON) PLC, ICBC STANDARD BANK PLC, KUWAIT FINANCE
HOUSE, METHODIST CHAPEL AID, MORGAN STANLEY BANK INTERNATIONAL, NATIONAL BANK OF
EGYPT UK, RBC EUROPE, RELIANCE BANK, UNION BANCAIRE PRIVEE UK`

Most are label variants my matcher did not cover and will resolve with the
normalisation module. **At least one is genuine**: CITIBANK UK's balance sheet
prints `Total liabilities (incl. equity - see sources)` — no separate equity
line, so its ROE cannot be computed without going back to the filing.

## 6. What the work actually is

Not document-hunting. Three things:

1. **A label-normalisation module** — the bulk of it. Same pattern the repo
   already uses for IFRS 9 stage categories and RWA categories in
   `scripts/insights/in040_risk_metrics.py`. Map the many printed spellings of
   "profit after tax" / "total equity" / "total assets" onto canonical inputs,
   per bank, with the unmatched ones listed rather than silently dropped.
2. **Two decisions for the user** (§7).
3. **Reading one document each for the ~13 divergences**, recording both sides.

## 7. Decisions needed before anything is built

1. **Average or year-end denominator?** Average equity is the standard
   definition and reproduces published ROE far better (median 0.00pp vs a
   consistent downward bias at year-end). It costs the oldest year of every
   bank: 1,069 bank-years → 940. Recommendation: **average, with the oldest year
   left blank rather than computed on a year-end basis**, since mixing the two
   in one row is exactly the mixed-basis trap this project documents elsewhere.
2. **Derived figures in a workbook built from transcribed ones.** The repo
   already permits this where it is labelled — UBP's NPL ratio, Bank of Africa's,
   RCI's are all derived from printed inputs — but a derived ROE must be
   visibly distinct from one the bank itself published, or the two bases merge
   invisibly. Recommendation: where the bank prints its own ROE, carry **both**,
   on separate rows, and never reconcile them.
3. **Entity vs group.** `UK_Banks_Key_Metrics.xlsx` caveat 4 states that for
   Lloyds, NatWest, Barclays, HSBC and Santander the figures shown are **GROUP**
   figures. That is directly contrary to this project's standing entity rule.
   Any import from that file must be rejected for those banks; computing from
   our own workbooks avoids the problem entirely, because those workbooks are
   already on the correct entity perimeter.
4. **Where do they live?** A new sheet, or added to `Overview`? This affects all
   145 workbooks and the insights pipeline.

## 8. Bottom line

Finding the remaining data is **not** the hard part, and the research files
overstate how much is missing. For ROE and ROA about 90% of the corpus is
already computable from figures we have transcribed and verified, at roughly 10×
the coverage of the research file and across every year rather than 2024 alone.
The genuine work is label normalisation, two basis decisions, and ~13 documents
to adjudicate. NIM and Cost of Risk are a step harder because their correct
denominators are often not printed. Cost of Funds should be expected to stay
mostly `n/d` — that is a fact about UK bank disclosure, not a gap in our reach.
