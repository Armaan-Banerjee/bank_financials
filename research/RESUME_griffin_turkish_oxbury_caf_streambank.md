# Fork C resume log — Griffin / Turkish Bank / Oxbury / CAF Bank / StreamBank

Started 2026-09-15. Written incrementally, one bank at a time, so a rate-limit
kill loses at most one bank's worth of work.

Mandate: convert weak "not found" claims into **sourced negatives** (specific
URL + verbatim quote + date checked), fill any cell that is genuinely
retrievable, and correct SDDT misclassifications.

---

## 1. GRIFFIN BANK LTD — `scripts/build_griffin_bank.py`

**Status: DONE** — rebuilt, 18 sheets.

### Verified independently 2026-09-15 (not taken on trust from the script)

- `https://griffin.com/reports` re-fetched and every `.pdf` href enumerated.
  Exactly **six** PDFs, complete list:
  - `Annual_Impact_Report_2025_2026_b1148509e9.pdf`
  - `Griffin_Bank_Annual_Impact_Report_20242025_24581e59c2.pdf`
  - `Griffin_Bank_Ltd_2023_Annual_Report_and_Financial_Statements_9c92dd2876.pdf`
  - `Griffin_Bank_Ltd_Annual_Report_2024_b98c8d4c38.pdf`
  - `Griffin_Bank_Ltd_Annual_Report_2025_edeb37eca7.pdf`
  - `Griffin_Bank_Ltd_Pillar_3_30_Sept_2023_df3ca44acc.pdf`
  **Exactly one Pillar 3 document exists, and it is dated 30 Sept 2023.**

- **Year mapping of the 30 September 2023 Pillar 3 — RESOLVED.** The document's
  own Introduction (p.2) reads: *"Griffin) as of 30 September 2023."* and
  *"This Pillar 3 document should be read in conjunction with the 2023 Annual
  Report and Financial Statements for the period ended 30th September 2023"*.
  Griffin's accounting reference date **is** 30 September (it moved from 30 June
  during mobilisation, which is why FY2023 is a 15-month period, 1 Jul 2022 –
  30 Sep 2023). So the P3 maps to **FY2023**, the same reference date as the
  FY2023 Annual Report. It is NOT a stub period and NOT a December year-end.
  The script already had this right.

- KM1 (p.21/22 of the P3) transcribed figures re-checked against the PDF text,
  all exact: CET1/Tier 1/Total capital £8,564k; Total RWEA £1,879k; CET1/Tier 1/
  Total capital ratio 456%; leverage ratio excl. central banks 91%; LCR 2,675%
  (footnote 3: *"average of eight months reported LCR (post-authorisation)"*);
  NSFR 1,034% (footnote 4, same 8-month basis). OV1: credit risk 706 +
  operational risk 1,174 (the documented £1k rounding gap against KM1's 1,879
  is real and is preserved).
  KM1 footnote 1 verbatim: *"We were authorised as a bank by the PRA (with
  restrictions) in 2023, and so we do not provide comparative information for
  the prior period."*

### Finding on FY2024/FY2025

The prose negative in `p3_sources()` was already strong (PRA register row for
FRN 970920, SDDT Regime Rule 3.1, waiver ref A00007614P.pdf, start 05/03/2024,
no end date — and Griffin's 30 Sep year-end puts both FY2024 and FY2025 after
that start date). **What was missing was the cells themselves**: every affected
metric sheet left FY2024/FY2025 *blank*, which per standing rule 7 is
indistinguishable from an unresearched gap and gets re-chased forever.

### Edits made to `scripts/build_griffin_bank.py`

1. Added `SDDT_EXEMPT_YEARS = ["FY2025", "FY2024"]` / `SDDT_CELL = "Not required
   (SDDT)"` and made the local `metric()` wrapper inject that as a default for
   those two years (explicit values still override — the CET1 Ratio sheet keeps
   its 112% / 64% from the Annual Report narrative). Follows the
   `build_vida.py` / `build_afin_bank.py` `PRE_LICENCE_YEARS` convention, with
   the cell text matching `build_secure_trust.py`'s existing
   `"Not required (SDDT)"`.
2. `RWA Breakdown` rows marked the same way for FY2024/FY2025.
3. Overview `ratios` block synced (Overview is a copy — editing detail sheets
   does not reach it). It previously showed FY2023 only; it now carries the
   FY2024/FY2025 SDDT markers, and CET1 Ratio now shows 112% / 64%, which the
   detail sheet already had but the Overview did not.
4. Added two paragraphs to `p3_sources()`: the cell convention, and a
   source-date restatement recording the P3's own "as of 30 September 2023"
   wording and why it maps to FY2023.

**Cells converted from blank to explicit sourced negative: 16** (8 metric
sheets × FY2024/FY2025 — CET1 Capital, Tier 1 Capital, Tier 1 Ratio, Total
Capital, Total Capital Ratio, Total RWAs, Leverage Ratio, LCR, NSFR, minus
overlap) plus 6 RWA Breakdown cells and 10 Overview cells.

**Deliberately NOT written**: no FY2024/FY2025 CET1/Tier 1/Total Capital
*amount*, no RWA figure, no leverage/LCR/NSFR value. They do not exist in any
public document, and the CET1 ratio alone cannot yield them without back-solving.

---

## 2. TURKISH BANK (UK) LIMITED — `scripts/build_turkish_bank.py`

**Status: DONE** — rebuilt, 18 sheets
(`banks/TURKISH BANK UK FINANCIALS.xlsx`, note the filename has no parens).

### THE CRITICAL UNRESOLVED ITEM — RESOLVED

The sole Pillar 3 PDF is labelled "2024" on the index, sits at a **February
2026** WordPress upload path, and a search snippet called it board-approved in
2025. The PDF was downloaded and read. **Its reference date is 31 December
2024**, stated in three independent places:

- Cover: *"Turkish Bank (UK) Limited / PILLAR 3 DISCLOSURE / As of 31 December
  2024 (the "Reference Date")"*
- §1 Introduction: *"...is based on the Bank's financial situation as of 31
  December 2024 (the "Reference Date")."*
- §2.1 Basis of Disclosure: *"This document sets out the P3D of the Bank as of
  31 December 2024..."*

Appendix 1 Key Metrics is columned `31 Dec 24` / `31 Dec 23`. **It maps to
FY2024 with FY2023 as comparative — which is how the workbook already had it.**

**Where the "2025" came from** — §2.3 Verification, verbatim, *including the
unfilled placeholder*: **"The Pillar 3 disclosures were reviewed and approved
by the Bank's Board of Directors on xx 2025."** The literal characters `xx`
were left in the published PDF. That line is about **board approval**, not the
reference date. A FY2024 report approved during 2025 and uploaded Feb 2026 is
just a ~14-month lag, not a mislabelled FY2025 document.

**Column-header defect recorded**: Appendix 1's comparative column is headed
`T-4 - Prior Year` where UK KM1 calls for T-1. The date beneath it says
`31 Dec 23` and the figures tie to the FY2023 AR, so it is a template slip.

Also captured verbatim: §2.2 *"The Pillar 3 Disclosures are prepared annually
..."* (the bank asserts an annual cadence it has not met — so the other years
are a publication failure, not an exemption) and §3 *"Its accounting and
disclosures are on a solo basis. The Bank does not have any subsidiary
undertakings..."* (confirms the entity basis).

All KM1 figures already in the workbook were re-checked line by line against
the PDF — **every one exact** (CET1/T1/TC 28,884 / 28,099; TREA 111,235 /
99,516; ratios 25.97% / 28.24%; leverage 15.9% / 15.2% with exposure 181,556 /
185,406; LCR 606% / 739%; NSFR 195.34% / 192.58%).

### Sourced negative for FY2021 / FY2022 / FY2025 ratios

Two independent enumerations, both done this session:

1. `https://www.turkishbank.co.uk/reports/` fetched, every PDF href extracted
   and de-duplicated: **exactly one Pillar 3 item on the page**, the FY2024
   edition. No P3 exists for any of the three gap years.
2. The Annual Reports covering those years were **opened and read**:
   - FY2022 AR (covers FY2022 **and** FY2021), text-native, 237,194 extracted
     chars — full-text search for `capital ratio`, `Tier 1`, `CET1`,
     `leverage ratio`, `liquidity coverage`, `net stable` returns **zero
     occurrences of any of them**. Its Note 38 prints a components table
     totalling `Total regulatory capital 26,022 / 24,681` — an amount, no ratio.
   - FY2025 AR is a 66-page scanned Acrobat Sign filing with **no text layer**;
     rendered at 200dpi and OCR'd, and Note 37 read off the page image. It
     prints `Total regulatory capital 27,379 / 29,678`, `Capital surplus taking
     into account buffers 13,307 / 15,240`, and the RWA breakdown
     (`Total risk weighted assets 103,473 / 111,235`). **No capital ratio, no
     leverage ratio, no LCR, no NSFR.** (FY2024 RWA 111,235 here ties exactly to
     the P3 KM1 TREA — independent confirmation of the RWA basis.)

Also quoted verbatim in the script so it is not over-read: the FY2024 P3's §2.1
records an exemption from **remuneration** disclosures only (PRA PS16/23, small
non-listed CRR firm). That does **not** touch the key-metrics templates. **This
bank is not Pillar-3-exempt.**

### Edits made

- New `PILLAR3_REFERENCE_DATE_NOTE`, prepended to `PILLAR3_NOTE`, carrying all
  of the above verbatim quotes.
- New `RATIO_GAP_NEGATIVE` + `ratio_sources()` + `ratio_row()` helpers.
- CET1 Ratio, Tier 1 Ratio, Total Capital Ratio, Leverage Ratio (both rows),
  LCR (all three rows) now write **"Not publicly disclosed"** into
  FY2025/FY2022/FY2021 instead of leaving them blank. Per-sheet notes rewritten.
- **NSFR handled separately and deliberately differently**: FY2025/FY2022 read
  "Not publicly disclosed", but **FY2021 reads "Not applicable"** — the UK NSFR
  requirement began 1 Jan 2022 (PRA PS17/21), so there was nothing to disclose
  at a 31 Dec 2021 reference date. Conflating the two would misrepresent a
  regulatory boundary as a publication failure.
- Overview `ratios` block synced (it is a copy) and its note rewritten.

**Cells converted from blank to explicit sourced negative: 24 on the metric
sheets + 18 on the Overview.**

### Deliberately NOT written

- **No ratio was computed for FY2021/FY2022/FY2025**, even though the workbook
  holds both a capital amount and Total RWAs for each of those years. That would
  be back-solving, and it would also mix bases — the only capital amount
  available for those years is the Annual Report figure, which runs
  £794k–£1,097k *above* the Pillar 3 KM1 CET1 on the two dates where both are
  observable, so any quotient would be materially overstated and would sit
  next to genuine FY2023/FY2024 ratios as if comparable.
- **DID NOT UNDO** the deliberate FY2022 retained-earnings discrepancy. Verified
  still present and still correct as documented: the FY2022 AR's Note 38 prints
  retained earnings **£8,102k** against its own audited SOCIE's **£8,019k**, and
  the memo capital row uses the FY2023 restatement **£25,939k**. Left exactly as
  found.
## 3. OXBURY BANK PLC — `scripts/build_oxbury.py`

**Status: DONE** — rebuilt, 18 sheets. **This was the big one.**

### THE HEADLINE: the brief's premise was wrong, and so was the script

The brief (and three earlier passes, with increasing confidence) said Oxbury had
published **exactly ONE** Pillar 3 document ever, and that FY2024/FY2025 were an
unmet obligation to be recorded as a permanent negative.

Re-fetching `https://www.oxbury.com/annual-reports/` on 2026-09-15 and
extracting every href from the raw HTML returns **THREE** Pillar 3 PDFs:

- `/media/xttezclr/oxbury-bank-plc-pillar-3-2023-final.pdf` (Dec 2023, known)
- `/media/3yknkp3i/oxbury-bank-plc-pillar-3-2024.pdf` — **NEW**
- `/media/yqqdu010/oxbury-bank-plc-pillar-3-2025.pdf` — **NEW**

Both new files downloaded: full text-native Pillar 3 reports, same structure as
the 2023 edition (1.23MB / 1.26MB, 163k / 167k extracted chars), cover pages
reading *"Oxbury Bank Plc / Pillar 3 Disclosures / December 2024"* and
*"... December 2025"*, each with complete UK KM1, OV1, CC1, LIQ1, LIQ2.

**Why earlier passes missed them** — worth generalising: Oxbury's media URLs use
opaque random slugs, so permutation from the known 2023 filename cannot reach
them; and the Wayback CDX sweep that returned "195 PDFs, exactly one Pillar 3"
was *accurate about the archive* — the archive just had not captured these yet.
**An absence in Wayback is not an absence on the live site, and a negative
established against a document index expires — re-fetch the index.**

### Cells filled (previously blank)

| Sheet | FY2025 | FY2024 |
|---|---|---|
| CET1 Capital | 192,855 | 142,312 |
| Tier 1 Capital | 192,855 | 142,312 |
| Total Capital | 226,552 | 159,812 |
| Total Capital — of which Tier 2 | 33,697 | 17,500 |
| Total RWAs | 1,168,300 | 684,357 |
| CET1 Ratio | 16.51% | 20.79% |
| Tier 1 Ratio | 16.51% | 20.79% |
| NSFR | 160.6% | 262.7% |
| NSFR ASF / RSF | 2,947,068 / 1,835,204 | 2,272,844 / 865,058 |
| LCR (P3 average) | 340.1% | 465.3% |
| LCR HQLA / net outflow | 1,512,803 / 444,827 | 1,510,275 / 324,591 |
| Leverage exposure measure | 2,050,662 | 1,077,236 |
| RWA Breakdown credit / CCR / op | 1,168,300 / 0 / 35,232 | 684,357 / 0 / 15,763 |

Values **replaced** (rounded AR KPI → Pillar 3 template, same measure):
Total Capital Ratio FY2025 18.8%→**19.39%**, FY2024 22.5%→**23.35%**;
Leverage FY2025 9.2%→**9.40%**, FY2024 12.7%→**12.66%**.

FY2024 has **two independent sources** (its own Dec-2024 edition and the
Dec-2025 edition's comparative) which agree on every line.

### Validation gate — passed, with one documented exception

Dec-2024 edition's FY2023 comparative vs the Dec-2023 edition's own FY2023 and
vs the workbook: CET1/T1 68,026; Tier 2 14,188; total reg capital 82,214; RWA
426,705; CET1 ratio 15.94%; TCR 19.27%; leverage 10.69%; NSFR 201.1%; OV1 credit
426,705 / operational 18,622 — **all reproduce exactly**. Nothing was overwritten
on an unverified source.

**The exception, NOT reconciled**: FY2023 LCR is **545.2%** in the Dec-2023
edition's own column but **529.9%** in the Dec-2024 edition's comparative for the
same date on the same stated basis. 15.3pp, unexplained in either. Workbook keeps
the own-year 545.2% per convention and records 529.9% in the source note.
**Do not "fix" this.**

### Corrections made

1. **KM1 "Total capital" row is defective in all three editions** — it repeats
   the CET1 figure and omits Tier 2. The Bank's own printed Total capital ratio
   proves which line is right: 226,552/1,168,300 = 19.39%, 159,812/684,357 =
   23.35%, 82,214/426,705 = 19.27%, 53,057/282,001 = 18.81% — all four match the
   printed percentages to the decimal, the KM1 numerators do not. The **CC1
   "Total regulatory capital"** line is used throughout. Not a back-solve: those
   are printed figures (CET1 + printed Tier 2).
2. **LCR was silently mixing two bases** — FY2025/FY2024 held the AR's
   point-in-time KPI while FY2023/FY2022 held the Pillar 3 weighted average, in
   one row. Now **two labelled rows**. The gap is 44pp in FY2025, not rounding.
   AR footnote confirms the KPI basis; P3 HQLA line is labelled
   *"Weighted value-average"*.
3. **OV1 "Total" = Credit Risk alone** (excludes operational risk) in *all three*
   editions — previously logged as a possible one-off slip, now confirmed as a
   settled template feature. Reproduce-as-disclosed decision confirmed, with the
   reason strengthened: the Total ties to KM1, to CC1, and is the denominator
   that reproduces the printed ratios.
4. The FY2025 AR Note 18 "£220m (2024 £136m)" puzzle is now **moot** — audited
   template figures exist. Neither number is reproduced on any sheet.
5. Withdrew the stale "USER-ACTIONABLE: request the FY2024/FY2025 editions from
   the Bank" item — they are published.

### SDDT — the brief was right, and the script already was too

Verified and preserved verbatim in the script. PRA register, FRN 834822: three
rows — Article 26(3) CRR (31/01/2020), Capital Buffers 5.1–5.3 (20/01/2025), and
**`Ru 2.1(9)`**, ref `A00012298P.pdf`, start **20/05/2026**. That is an
**eligibility-criterion** modification (waives the UK-parent test so the firm may
*qualify* as an SDDT) with **no disclosure effect**. Oxbury holds **no Ru 3.1
row**. And 20/05/2026 post-dates every year in the workbook anyway. **Oxbury was
under a live Pillar 3 obligation throughout** — which is precisely why the
missing editions should have been treated as a search failure, not a structural
absence. That reasoning is now written into the script explicitly.

### FY2021 — converted to a sourced negative

No Pillar 3 edition reaches FY2021 (earliest is Dec 2023, comparative FY2022).
Both ARs covering FY2021 were **opened and read**: Note 18 "Capital Management"
is **purely narrative** in each. Verbatim, that is the whole of what either says
about quantum: *"At the end of the financial year, Oxbury held Common Equity
Tier 1 capital, compromised of relevant share capital and retained earnings"*
(2021, spelling as printed) / *"...comprising of relevant share capital and
retained earnings"* (2022), then *"The comparison of the available and required
capital positions are reviewed on a monthly basis."* **No amount, no RWA, no
own-funds table, no OV1 anywhere in either document.**

So FY2021 CET1 Capital / Tier 1 Capital / Total Capital / Total RWAs / LCR-average
/ leverage exposure now read **"Not publicly disclosed"**; NSFR FY2021 reads
**"Not applicable"** (UK NSFR began 1 Jan 2022, PRA PS17/21).

Also recorded: FY2021 KPI ratio divergence — own-year AR says **23%**, the FY2022
AR's comparative says **25%**. Own-year used. And the FY2022 AR prints its own
FY2022 leverage as "152%", a misplaced decimal for 15.2%, used nowhere.

### Deliberately NOT written

- No FY2021 capital amount or RWA back-solved from the FY2021 KPI ratios.
- The AR's £220m / £136m narrative figures are not placed on any sheet — they
  tie cleanly to neither Pillar 3 basis.
- FY2023 LCR not reconciled between the two editions.
- OV1 component rows not summed to "fix" the Total.
## 4. CAF BANK LIMITED — `scripts/build_caf_bank.py`

**Status: DONE** — rebuilt, 18 sheets. 30 April year-ends throughout.

### The SDDT claim, fetched and quoted verbatim

`https://www.cafonline.org/home/caf-bank/about-us/legal-information/pillar-3-disclosure`
fetched 2026-09-15. The **entire substantive content of the page** is one
sentence:

> "CAF Bank has become part of the PRA's SDDT ("Small Domestic Deposit Taker")
> regime under which, as a non-listed institution, the Bank is not required to
> publish a Pillar 3 report."

**What the page does not do**: no date of its own, no effective date, no rule
number. That is exactly why the register — not this page — is the evidence.

### Cross-check against the PRA waivers register — and it does NOT clear FY2025

Register downloaded fresh 2026-09-15 (UTF-16 LE, tab-separated despite the .csv
extension, 2,919 data rows). **CAF BANK LIMITED, FRN 204451** holds five rows:

| Rule | Sub rule | Ref | Start | End |
|---|---|---|---|---|
| **SDDT Regime – General Application** | **Ru 3.1** | **A00010742P.pdf** | **08/08/2025** | none |
| Capital Requirements Regulation | Ar 26(3) | A3908085P.pdf | 18/01/2017 | none |
| Permissions and Waivers (CRR Firms) | CA.BU.5.1-5.3 | 00007843.pdf | 10/05/2024 | none |
| Capital Requirements Regulation (interim profits) | Ar 26(2) | A00008787P.pdf | 03/10/2024 | 01/11/2026 |
| Capital Requirements Regulation (CET1 classification) | Ar 26(3) | A00005546P.pdf | 03/11/2022 | none |

Only the first touches disclosure. It is **Rule 3.1** (the real opt-in), and CAF
holds no eligibility-criteria-only row.

**THE DATE PROBLEM — and it is not resolved, deliberately.** The Rule 3.1
modification **starts 08/08/2025**. CAF's **FY2025 ended 30 April 2025 — three
months earlier.** So:

- On a **reference-date** reading, FY2025 predates the relief; the Bank still
  owed a Pillar 3 report for that year and the blanks are a genuine gap.
- On a **publication-date** reading, an FY2025 report would not have fallen due
  until after 08/08/2025, by which point the duty was disapplied. CAF's own page
  asserts this reading in substance.

The script already carried this "SDDT DATE TEST" as UNDETERMINED; my independent
register pull confirms the 08/08/2025 date to the character and adds the waiver
ref. **The cells are blank either way — only the LABEL is at stake — so FY2025
is labelled "Not publicly disclosed", NOT "SDDT-exempt".** A note now says
explicitly that this must not be "tidied up" in either direction.

Unambiguous either way: **FY2026 onward IS structurally exempt** (year ending 30
April 2026 is after 08/08/2025); **FY2024 and earlier unambiguously predate it**,
consistent with real standalone Pillar 3 PDFs existing for FY2020–FY2024.

### Cells converted from blank to explicit

- FY2025 on CET1 Capital, CET1 Ratio, Tier 1 Capital, Tier 1 Ratio, Total
  Capital, Total RWAs, and all four RWA Breakdown rows → "Not publicly disclosed"
- Leverage "including claims on central banks" FY2025 **and FY2024** → "Not
  publicly disclosed" (FY2024's own P3 gives the exposure measure with no
  accompanying %, a real reduction in granularity — not calculated)
- LCR HQLA / net-outflow / ratio FY2021 and FY2020 → "Not publicly disclosed"
  (those years' own P3s predate the LIQ1/KM1 templates)
- **NSFR FY2021 and FY2020 → "Not applicable"**, a deliberately *different*
  label: the UK NSFR requirement began 1 Jan 2022 (PRA PS17/21) and CAF's
  30 April year-end puts both reference dates before it. FY2022 (30 Apr 2022) is
  after the boundary and CAF *did* disclose 804% — which confirms the boundary
  falls exactly where stated.
- Overview ratios block synced (it is a copy) and its note substantially
  rewritten.

### Deliberately NOT touched

- **The Leverage Ratio FY2025 6.35% was left exactly as found.** The brief's OCR
  warning is real and already documented in the script: tesseract reads "6.15%"
  at both 250 and 450 DPI, a magnified visual read of the page image shows
  "6 35%", and 6.35% is correct. **I did not OCR CAF this pass** (the data was
  already complete), so nothing could have re-corrupted it — but recording that
  I checked and left it alone.
- FY2021 LCR **not** back-filled from the FY2022 document's 268% comparative —
  FY2021's own document never published an LCR, and project convention is each
  year's own originally-published figure.
- The FY2021 restatement pairs (RWA £127,881k own-year vs £127,844k later
  comparative; leverage 2.72% vs 2.74%) left as they were.
## 5. STREAMBANK PLC — `scripts/build_streambank.py`

**Status: DONE** — rebuilt, 18 sheets.

### The unresolved task, resolved

**Rule number and start date, from a fresh download of the PRA consolidated
waivers register (2026-09-15):** StreamBank PLC, **FRN 954876** —
*"Modification by Consent - PRA Rulebook- CRR Firms- Rule 3.1 of the SDDT Regime
- General Application Part 3.1"*, rule `SDDT Regime - General Application`, sub
rule **`Ru 3.1`**, waiver ref **`A00007820P.pdf`**, **start date 04/05/2024**,
**no end date**. (Its two other rows are Capital Buffers 5.1-5.3 and an Ar 26(3)
CET1 permission, both from 28/06/2022 — neither touches disclosure.)

**Does the start date cover FY2026?** StreamBank's year-end is 31 March, so
FY2026 ran 1 Apr 2025 – 31 Mar 2026. **On a pure date test, yes** — 04/05/2024
precedes it comfortably.

**But FY2026 is NOT recorded as structurally exempt, and that is the right call**
(the script already reached it; I verified it independently):
- StreamBank **published a full Pillar 3 disclosure for FY2025** — the year ended
  31 March 2025, *eleven months after* the 04/05/2024 start date, Board-approved
  18 September 2025. A firm that had actually dropped the obligation would not
  have produced that document.
- Its own FY2025 Pillar 3 p.3 says: *"In January 2025, the Bank applied, and has
  since been confirmed, as a SDDT regime institution. Final implementation of
  these changes has been delayed until 1 January 2027."* Two conflicts with the
  register in one sentence: it dates its **application to January 2025**, eight
  months after the register's 04/05/2024 start; and it says it regards the
  changes as **not implemented until 1 January 2027**, i.e. by its own account it
  remained subject to Pillar 3 throughout FY2025 and FY2026. Neither fact is
  discarded.
- FY2026's gap is most likely **publication lag** (FY2025's edition appeared ~6
  months after year-end, so an FY2026 one would only be due around Sept 2026 —
  exactly when this check ran). Worth **one** re-check, not closure as structural.
- **FY2021 and FY2023 are untouched by SDDT** — both pre-date 04/05/2024 by
  years and have their own established causes.

### The methodological win: enumeration instead of permutation

streambank.co.uk is a **Laravel/Inertia SPA**. Every URL — homepage, `/legal/`,
`/about-us/`, even `/sitemap.xml` — returns the *same* 25,989-byte shell at
HTTP 200. Soft-404s are indistinguishable from real pages by status or size, and
all document links are rendered client-side. **Permutation against this site can
only fail to find; it can never prove absence.**

Solution: downloaded the compiled bundle `https://streambank.co.uk/js/app.js`
(930,330 bytes) and extracted every `.pdf` string. That is the **complete** set
of documents the site can link to — **exactly six**:

```
/pdf/StreamBank-Plc-Financial-Statements-31-March-2023-Signed.pdf  FY2023 AR
/pdf/StreamBank-Plc-FY24-Live-PwC-Signed.pdf                       FY2024 AR
/pdf/FY24-Pillar-3-StreamBank-PLC.pdf                              FY2024 P3
/pdf/March-2025-Annual-Report-2025.pdf                             FY2025 AR
/pdf/March-2025-Pillar-3-Disclosures.pdf                           FY2025 P3
/pdf/StreamBank-PLC-Annual-Report-and-Financial-Statements.pdf     FY2026 AR  <- NEW
```

**Exactly two Pillar 3 documents exist, FY2024 and FY2025 only.** No FY2026
edition, no FY2023 edition — *enumerated and absent*. Wayback is useless here and
its silence proves nothing: a CDX domain sweep returns only 11 PDF captures, of
which one is a bank report, so the archive has never captured either Pillar 3
file or four of the six documents that demonstrably exist live.

### Bonus find: a text-native FY2026 Annual Report

The last file in that list was **not in the script**. It is the Bank's own copy
of the FY2026 Annual Report — the same document as the Companies House filing
already cited, but **text-native (232,811 chars)** instead of a 79-page scan that
yields 79 characters and has to be OCR'd. Added as `AR2026_SITE_URL`.

Every FY2026 negative was re-established against that native text, replacing an
OCR-dependent finding. Exact whole-document counts: `SDDT` 0, `Small Domestic` 0,
`Strong and Simple` 0, `Pillar 3` 0, `NSFR` 0, `net stable` 0, `LCR` 0,
`exposure measure` 0, `high quality liquid` 0. Near-misses read in context, none
a figure: `Liquidity Coverage` once, purely qualitative, no number; `HQLA` once,
in a committee's duties; `risk weighted` twice, both as *definitions* of the CET1
ratio with no RWA amount.

**Trap recorded for future passes**: grepping this document for `RWA` returns
**six hits, every one of them inside "forward" / "forward-looking"** — not the
acronym at all. A naive substring search would conclude RWAs are disclosed.

### The pseudo-leverage ratio — quarantined, not discarded

The script already correctly *excluded* the AR's headline "Leverage ratio"; I
confirmed it independently from the native text and went one step further by
preserving it on a labelled memo row. Both ARs footnote the measure as **"CET1
capital divided by liabilities"** — capital over *liabilities*, not over a
regulatory exposure measure. The **FY2023 figure of 182.3% is the giveaway**: a
CRR leverage ratio above 100% is arithmetically impossible, and it arises only
because at 31 Mar 2023 the Bank held £32.2m of capital against £17.3m of
liabilities, capitalised well ahead of taking deposits.

Leverage Ratio sheet now has **three rows**: CRR excl. central-bank claims
(20.4% / 21.0%), CRR incl. central-bank claims (16.6% / 17.3% — added, the P3
reports both and the workbook was hiding one), and the quarantined memo row
(FY2026 19.2%, FY2025 19.5%, FY2023 182.3%) labelled *"NOT a CRR leverage ratio -
do not compare"*. Keeping these on one row would have shown leverage "falling"
21.0% → 19.2% on a silently-changed definition.

### Cells converted from blank to explicit

FY2026 and FY2023 on Total RWAs, RWA Breakdown (3 rows), Leverage Ratio (2 CRR
rows), LCR, NSFR → **"Not publicly disclosed"**; FY2021 on the newly-added rows →
**"Not applicable"**. Overview ratios synced and its note rewritten.

### DID NOT UNDO

**FY2021 "Not applicable" preserved exactly** — the `PRE_LICENCE_YEARS =
["FY2021"]` mechanism is untouched, and every row I added inherits it. StreamBank
held no banking licence until June 2022 (restricted) / February 2023 (full).

Also untouched: the deliberate FY2026-vs-FY2025 basis warning (FY2026 capital is
Annual Report basis, CET1 34,182.8 / 24.1% comparative vs the Pillar 3 35,066.3 /
24.8% retained for FY2025 — **not** overwritten).

---

## Cross-bank notes worth keeping

1. **A negative established against a document index expires.** Oxbury's index
   gained two Pillar 3 editions since the last check. Re-fetch the index; never
   carry a previous session's enumeration forward as still-true.
2. **An absence in Wayback is not an absence on the live site.** It burned the
   Oxbury pass ("195 PDFs, exactly one Pillar 3" — accurate about the archive,
   wrong about reality) and would have burned StreamBank too.
3. **For JS-rendered sites, the compiled JS bundle is the document index.**
   Worked decisively on StreamBank where every HTTP route returns an identical
   shell.
4. **Check the printed definition before trusting a ratio.** Three of these five
   banks print something labelled "leverage ratio" or "capital ratio" that is not
   the CRR measure.
