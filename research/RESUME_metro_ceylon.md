# RESUME — Metro Bank FY2019 Pillar 3 + Bank of Ceylon (UK) — 2026-09-15

Checkpoint file. Written as work proceeds so a rate-limit kill loses nothing.

## 1. METRO BANK PLC — FY2019 Pillar 3

**Script:** `scripts/build_metro_bank.py`
**Source:** `https://www.metrobankonline.co.uk/globalassets/documents/investor_documents/metro-bank-pillar-3-2019.pdf`
Fetched 200, 691,586 bytes, `application/pdf`, 54 pages, Adobe InDesign 14.0, created 2020-04-16.
Cover confirms "Pillar 3 2019", METRO BANK PLC, 31 December 2019. Has a real text layer
(`pdftotext -layout`) — no OCR needed.

### Status of the premise
The task briefing anticipated FY2019 might be marked "not disclosed" on the strength of the
missing index entry. **It is not.** The script already carries `P3_2019_HIST` as a URL constant
(line 36) and FY2019 figures are already transcribed across all the Pillar 3 metric sheets and
the RWA Breakdown. So there was no false "not disclosed" claim to correct.

### Verification result — every pre-existing FY2019 cell is CORRECT
Checked each against the PDF directly:

| Sheet | Script value | Document | Table / page |
|---|---|---|---|
| CET1 Capital | 1,427 | 1,427 | Table 3 Capital Composition, row 29, p.25 |
| CET1 Ratio | 15.6% | 15.6% | Table 2 Key Ratios, p.4; Table 3 row 61 |
| Tier 1 Capital | 1,427 | 1,427 | Table 3, row 45 |
| Tier 1 Ratio | 15.6% | 15.6% | Table 2; Table 3 row 62 |
| Total Capital | 1,676 | 1,676 | Table 3, row 59 |
| Total Capital Ratio | 18.3% | 18.3% | Table 2; Table 3 row 63 |
| Total RWAs | 9,147 | 9,147 | Table 1 RWA Summary p.4; Table 3 row 60; Table 8 EU OV1 row 29 |
| Leverage exposure | 21,506 | 21,506 | Table 5 LRSum row 8 / Table 6 LRCom row 21, p.28 |
| Leverage ratio | 6.6% | 6.6% | Table 6 LRCom row 22 |
| LCR HQLA | 3,356 | 3,356 | Table 26 EU LIQ1, p.46 |
| LCR net outflows | 1,708 | 1,708 | Table 26 |
| LCR ratio | 197% | 197% | Table 2 and Table 26 |
| MREL | 22.1% | 22.1% | Table 2 ("Total capital plus MREL ratio") AND s.3 p.25 ("interim MREL ratio") |
| RWA credit risk | 8,591 | 8,591 | Table 8 EU OV1 row 1 |
| RWA CCR | 5 | 5 | Table 8 row 6 |
| RWA market risk | 5 | 5 | Table 8 row 19 |
| RWA operational | 546 | 546 | Table 8 row 23 |

**Validation gate passed** — the document's own FY2018 comparative column reproduces every
FY2018 figure already in the workbook (CET1 1,171 / 13.1%; Total capital 1,420 / 15.9%;
RWA 8,936; leverage 21,704 / 5.4%; LCR 3,489 / 2,506 / 139%; OV1 8,560 / 2 / 4 / 370).
No conflicts, so nothing needed dual-row treatment.

### Cells ADDED this pass
1. RWA Breakdown — "Amounts below the thresholds for deduction (250% RW)": FY2019 **0**,
   FY2018 **0**. Table 8 EU OV1 row 27 shows an explicit en-dash for both years (a stated nil,
   not an absence), same convention as the FY2014 dashes already recorded as £0m in the P&L.
2. Asset Quality — "Total ECL allowance": FY2019 **-34**, FY2018 **-34**. Stated in the
   narrative under Table 16 (p.39): "At the end of 2019 we held an ECL provision of £34 million
   (31 December 2018: £34 million)", and corroborated by Table 18's 31 December total row.

### Deliberately NOT written
- **NSFR FY2019** — the word "NSFR"/"stable funding" as a ratio appears nowhere in the 54-page
  document. Structurally correct blank (UK NSFR disclosure began 1 Jan 2023). Left blank.
- **RWA Breakdown securitisation FY2019/FY2018** — Table 8 EU OV1 has NO securitisation row at
  all (rows run 1, 2, 6, 7, 12, 19, 20, 23, 24, 27, 29). Under the post-2018 template it is
  folded into credit risk. The existing blank is correct and the existing source note already
  says so. Not filled, not zeroed — a zero would be a false claim of nil securitisation RWA.
- **Asset Quality IFRS 9 Stage 1/2/3 gross carrying amounts FY2019** — Table 18 gives loss
  allowance BY STAGE (Stage 1 -9, Stage 2 -5, Stage 3 -20, POCI 0) but no gross carrying amount
  by stage anywhere in the document. Deriving the stage split or the coverage ratio would require
  back-solving. Left blank.
- **Coverage ratio FY2019** — would require ECL allowance / gross lending, i.e. a derivation from
  two numbers. Not written.
- **Table 17 EU CR1-A defaulted exposure (£92m FY2019 / £59m FY2018)** — a regulatory
  defaulted-exposure measure, NOT the same basis as the Annual Report's NPL table already in the
  Asset Quality sheet (£77m FY2019 / £21m FY2018). Different definitions; merging or overwriting
  would breach the entity/basis rule. Not written, recorded here instead.

### Corrections/clarifications made to notes
- `P3_SOURCES` FY2019 line previously said "Table 2 Key Ratios, KM1 and Table 8 EU OV1". **There
  is no KM1 template in the 2019 document** (KM1 arrives with the later UK/CRR2 template set).
  Replaced with the real table/page list.
- **LCR basis**: Table 26 EU LIQ1 is explicitly captioned "as at 31 December 2019" — a
  point-in-time figure, NOT the 12-month average that the later UK KM1 rows carry. The LCR sheet's
  row label says "average". Flagged in the LCR sheet note rather than silently merged.
- **MREL label**: the same 22.1% is captioned "Total capital plus MREL ratio" in Table 2 but
  called "Metro Bank's interim MREL ratio" in section 3 (p.25). Both labels recorded.

### REUSABLE METHOD NOTE (the point of this ticket)
Recorded in the script's `P3_SOURCES`. Nine URL paths built by permuting the neighbouring years'
filename patterns ALL returned 404 — including the `investor_documents` folder that serves the
2017 and 2018 Pillar 3 files, the same folder that in fact holds the 2019 file. Only a search on
the filename/bank name independent of the site's own index located
`metro-bank-pillar-3-2019.pdf`. The bank's IR index does not list it at all.
**Rule: a year missing from a bank's own document index is not closed until BOTH a direct fetch
AND a name search have failed. Permutation can only fail to find; it can never prove absence.**

---

## 2. BANK OF CEYLON (UK) LIMITED

**Script:** `scripts/build_bank_of_ceylon_uk.py` — rebuilt, 18 sheets.

### A. FY2022/FY2023 Pillar 3 — sourced negative, re-run with controls
Probed the site's one uniform naming pattern
(`/downloads/corporate/BOCUK_Pillar%203%20Disclosures%2031%20December%20<YYYY>.pdf`):

| Path | HTTP | Bytes | Content-Type | First bytes | md5 |
|---|---|---|---|---|---|
| 2021 (positive control) | 200 | 503,885 | application/pdf | `%PDF-` | 625c7412… |
| **2022 (test)** | **404** | **146** | text/html | `<html` | 8eec510e… |
| **2023 (test)** | **404** | **146** | text/html | `<html` | 8eec510e… |
| 2024 (positive control) | 200 | 978,715 | application/pdf | `%PDF-` | bebe2e5e… |
| `BOCUK_THIS_FILE_DOES_NOT_EXIST_CONTROL.pdf` (negative control) | 404 | 146 | text/html | `<html` | 8eec510e… |

The three 404 bodies are byte-identical (same md5) to the made-up control path — this host
returns genuine 404s, not soft-404s that could mask a file it holds. Combined with the bank's
own index (lists 2018/2019/2020/2021/2024/2025, skips 2022/2023) and the Wayback CDX sweep from
the earlier pass, the two editions were never published. Recorded in `p3_sources()`.

**Caveat recorded honestly, NOT used as evidence:** FS2022 p.23 audit committee focus list says
"Approved the Pillar 3 disclosures as 31 December 2021", and FS2023/FS2024/FS2025 carry no such
line. Since the 2024 and 2025 Pillar 3 editions demonstrably exist (both fetched, 200 + `%PDF`),
the absence of that line proves nothing. Written into the script as an explicit
"noted so a later pass does not mistake it for proof".

### B. FY2022 CAPITAL — four previously-blank cells filled, conflict documented not resolved
Source: FS2023 Strategic Report **p.8**, "CAPITAL" — the earlier pass searched the notes
(Note 32) and missed the Strategic Report narrative. The document is an image-only Xerox scan, so
every figure was OCR'd with tesseract **and** re-rendered at 400 dpi and read visually digit by
digit, per the project's OCR rule. Verbatim:

> "The Bank maintained a strong CET1 capital position of GBP 13,684,688 (2022- GBP 12,852,280)
> with a CET1 ratio of 43% (2022: 44 %) and a total capital of GBP 14,788,668 (2022-13,818,899)
> with a ratio of 46% at 31st of December 2023 (2022: 48%)."

**Validation gate PASSED on FY2023** — its 13,684,688 and 14,788,668 reproduce the FY2024
Pillar 3's own 2023 comparative column exactly (£13,685k / £14,789k), and 43%/46% are that
document's 42.5%/45.9% rounded to whole percents. So the sentence is being read correctly; only
its FY2022 comparative is irreconcilable.

**THE CONFLICT — three FY2022 CET1 figures, three bases, none preferred:**

| Basis | Figure | Source | Stated basis |
|---|---|---|---|
| (a) | GBP 13,958,648 → **£13,959k** | FS2022 Note 28 (p.60) | IFRS 9 **transitional** relief (FS2022 p.20: "CET1 addback percentage of 50%") |
| (b) | GBP 13,734,398 → **£13,734k** | FS2022 Note 28, same sentence | **fully loaded** |
| (c) | GBP 12,852,280 → **£12,852k** | FS2023 p.8, 2022 comparative | **NOT STATED** |

(c) is £1,106k below (a) and £882k below (b) — it is neither. FS2023 carries no restatement note
covering it and its Note 32 has no 2022 comparative, so the workbook cannot determine which.

**Reconciled with the earlier pass rather than overwriting it:** basis (a) £13,959k was already
on the primary CET1/Tier 1 rows. It is **unchanged**. (b) and (c) were added as separate rows
labelled "FY2022 alternative (b)…" and "FY2022 alternative (c)…". All three FS2022 digits
(13,958,648 / 13,734,398 / 13,425,750) re-verified visually at 400 dpi.

**Cells filled (all new, all on clearly-labelled separate rows, all basis (c)):**

| Sheet | Row | FY2022 |
|---|---|---|
| CET1 Capital | alternative (b), fully loaded | 13,734 |
| CET1 Capital | alternative (c), FS2023 comparative | 12,852 |
| CET1 Ratio | basis (c), whole percent as stated | 44% |
| Total Capital | basis (c) | 13,819 |
| Total Capital Ratio | basis (c), whole percent as stated | 48% |

Total Capital FY2022 was previously blank with a note claiming no FY2022 total capital is
disclosed anywhere — that claim was wrong and is corrected in place (the correction is written
into the sheet note so the error is traceable, not silently deleted). Note £13,819k − £12,852k =
£967k, which is **not** the FY2022 revaluation reserve of £820k, so the "Tier 2 = revaluation
reserve" pattern seen in other years does not hold on basis (c) — further evidence the basis
genuinely differs.

### C. THE LABEL TRAP — checked, and RESOLVED
FS2024 (text-layer PDF, no OCR involved) contains: *"The CET1 total capital ratio at the end of
2024 was 24% (2023 46%) see note 32."*

Verified against the **FY2024 Pillar 3 KM1** (section 1.1) and its section 6 capital table, which
independently agree: FY2024 CET1 **22.7%** / total capital **24.6%**; FY2023 CET1 **42.5%** /
total capital **45.9%**.
- 24% matches 24.6%, cannot be 22.7%.
- 46% matches 45.9% exactly (and FS2023's own 46% total capital ratio), nowhere near 43%/42.5%.

**Conclusion: both figures are TOTAL capital ratios mislabelled "CET1".** Neither was mapped to
any sheet — the workbook already carries the correct KM1 values for FY2024/FY2023 on both sheets,
so no cell changed. The trap is recorded in the Total Capital Ratio sheet note.

### D. Other conflicts flagged, not merged
- FS2024's FY2023 comparatives are unreliable: it gives FY2023 CET1 as GBP 14,573,608 and 45%,
  against FS2023's own 13,684,688 / 43% and the Pillar 3's £13,685k / 42.5%. Two independent
  sources agree, so the validation gate keeps the existing figure; FS2024 is the outlier.
- FS2024 gives FY2024 total capital as GBP 14,717,109 vs the Pillar 3 KM1's £15,076k. The KM1
  regulatory template is retained; the narrative figure is not blended in.
- FS2023 internal inconsistency: FY2023 CET1 is 13,684,**688** in the Strategic Report (p.8) and
  13,684,**668** in Note 32 (p.67) — a GBP 20 discrepancy inside one document. Both visually
  verified at 400 dpi. Both round to £13,685k, which is what the workbook holds. Noted, no change.

### E. Deliberately NOT written
- **FY2022 Total RWAs** — still blank. 12,852,280 / 0.44 ≈ £29.2m is a back-solve, and a
  whole-percent ratio spans roughly £28.9m–£29.9m of RWA anyway. Not derived. The Total RWAs
  sheet note's old claim that "no ratio is disclosed for FY2022 either" is corrected there.
- **FY2022 Leverage Ratio** — genuinely undisclosed in both FS2022 and FS2023.
- **FY2022 Total capital on bases (a)/(b)** — FS2022 states no Tier 2 figure at all. The
  13,959 + 820 = 14,779 pattern inference is recorded in the note as an observation only.
- **FY2022 Tier 1 Capital / Tier 1 Ratio alternative rows** — not mirrored from CET1. The Bank
  never states a Tier 1 figure on bases (b)/(c), and never captions 44% as a Tier 1 ratio;
  equating them would be the workbook's inference, not the Bank's statement. Cross-referenced
  in both sheets' notes instead.
- **Overview sheet FY2022 ratios** — deliberately left blank. 44%/48% belong to a different,
  unstated basis and are printed to whole percents; dropping them into the trend line would
  render a basis break as a movement. The Overview note now says so explicitly (and its old
  claim that all FY2022 ratios are "genuinely absent" is corrected).

---

## Rules observed throughout
No figure derived or back-solved. No parent/group figure used (BOC UK solo statements only;
Metro's Holdings-vs-PLC basis split left exactly as the script already documented it). Every
OCR'd figure visually verified at 400 dpi. Both scripts read from disk immediately before
editing. Both rebuilt (`METRO BANK FINANCIALS.xlsx` 19 sheets — 18 standard plus its
pre-existing "Interim Pillar 3"; `BANK OF CEYLON UK FINANCIALS.xlsx` 18 sheets).
`refresh_all.py` NOT run, test suite NOT run, nothing committed, no messages sent.
