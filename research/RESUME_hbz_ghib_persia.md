# HBZ / GHIB / Persia — batch working file (started 2026-09-15)

Working file for the three-bank batch: Habib Bank Zurich plc (UK), Ghana International
Bank plc, Persia International Bank plc. Written incrementally so a rate-limit kill
leaves resumable state.

Status key: TODO / IN PROGRESS / DONE (written into the build script).

---

## 1. Habib Bank Zurich plc (UK) — `scripts/build_habib_bank_zurich.py`

### Sourcing — RESOLVED, complete Pillar 3 run FY2016–FY2025, no gaps

- **The real index is https://habibbank.com/gb/about-us/** — Pillar 3 2016–2025 and
  Annual Reports 2016–2025, no gaps. Nothing earlier than 2016 is listed (the Bank only
  began trading 1 April 2016 via a Part VII transfer, so 2016 is a genuine floor).
- **`https://habibbank.com/gb/financial-information/` is STALE — it stops at 2022.**
  Recorded here so a future pass does not mistake it for the index and re-derive a false
  "no FY2023–FY2025 edition" negative.
- **Filename trap: the upload-year directory does not match the reporting year**, so paths
  cannot be permuted. The FY2023 edition lives under a **2024/10** directory with a
  different filename stem (`UK-Pillar-3-Disclosure-2023.pdf`, not `Pillar-3-Disclosures-2023.pdf`).
- Entity confirmed **inside every one of the ten PDFs**: cover/running header reads
  "Habib Bank Zurich Plc – Pillar 3 Disclosures", and each states its own 31 December
  reporting date in §1.2/§1 narrative. **Not** HBL Bank UK (hblbankuk.com), a different bank.
- All ten verified as real PDFs (`%PDF` magic bytes) and all are text-extractable with
  `pdftotext -layout` — **no OCR was needed anywhere in this bank**, so no OCR risk.

Paths, all under `https://habibbank.com/gb/wp-content/uploads/sites/7/`:

| FY | path |
|---|---|
| 2025 | `2026/09/Pillar-3-Disclosures-2025.pdf` |
| 2024 | `2025/08/Pillar-3-Disclosure-2024.pdf` (singular "Disclosure") |
| 2023 | `2024/10/UK-Pillar-3-Disclosure-2023.pdf` (**upload year ≠ reporting year**) |
| 2016–2022 | `2024/05/Pillar-3-Disclosures-<YYYY>.pdf` |

### The prior script's claims that are now DISPROVEN

1. `P3_BASE = "https://www.habibbank.com/uk/downloads/financials"` with FY2019–FY2023
   only — **wrong host and wrong range**. Replaced.
2. "the Bank publishes NO Pillar 3 edition for FY2024 or FY2025" — **false**, both exist.
3. The `UNRESOLVED DISCREPANCY` block in `p3_sources()` — **now resolved**, see below.
4. RWA Breakdown subtitle: "FY2016–FY2021 do not [have a category split] … a genuine gap
   for those years, not an access gap" — **false**. Every edition 2016–2025 carries a
   credit/operational/market split in its "Own Funds Requirements" table.

### Resolution of the flagged UNRESOLVED DISCREPANCY

The workbook's FY2022–FY2024 ratios came from the **FY2024 edition's KM1**, whose URL had
never been recorded. Confirmed: FY2024 ed KM1 prints CET1 ratio 17.36% / 16.67% / 15.03%
and Capital Adequacy Ratio 20.41% / 20.13% / 18.55% for FY2024/23/22 — exactly the
workbook's Tier 1 Ratio and Total Capital Ratio rows.

**Row-naming trap in HBZ's own KM1** (this is what caused the confusion):
- `CET 1 ratio (%)` — the CET1 ratio.
- `Total capital ratio (%) – (CET 1 + Tier 1)` — despite the name, the parenthetical says
  CET1+Tier 1, i.e. this is the **Tier 1 ratio**, NOT the CRR total capital ratio.
- `Capital Adequacy Ratio (CET 1 + Tier 1 + Tier 2)` — **this** is the CRR total capital
  ratio (own funds ÷ RWA), and it is the row this workbook's Total Capital Ratio uses.
  Verified by arithmetic in the FY2024 and FY2025 editions (both internally tie exactly).

### KM1 / capital data captured (all transcribed, none derived)

Total RWAs, £'000 — consistent across every edition that reports them:
2017 359,941 · 2018 387,179 · 2019 442,493 · 2020 513,951 · 2021 547,938 ·
2022 575,205 · 2023 587,448 · 2024 664,889 · **2025 773,493** ·
2016 336,541 (FY2016 ed §5.2)

RWA category split (each year's own edition's "Own Funds Requirements" table), £'000:

| FY | Credit | Operational | Market (incl CVA where stated) | Total |
|---|---|---|---|---|
| 2016 | 310,219 | 25,183 | 1,139 | 336,541 |
| 2017 | 330,001 | 29,497 | 443 | 359,941 |
| 2018 | 353,393 | 33,470 | 316 | 387,179 |
| 2019 | 407,459 | 34,540 | 494 | 442,493 |
| 2020 | 477,272 | 35,898 | 781 | 513,951 |
| 2021 | 512,151 | 35,091 | 696 | 547,938 |
| 2022 | 538,880 | 36,011 | 313 | 575,204 |
| 2023 | 547,178 | 40,092 | 179 | 587,449 |
| 2025 | 709,091 | 63,924 | 478 | 773,493 |

FY2024 edition alone uses an OV1 form splitting CCR out:
FY2024 Credit excl CCR 611,684 / CCR incl CVA 1,895 / Market 42 / Op 51,268 / Total 664,889;
FY2023 Credit excl CCR 547,178 / CCR incl CVA 137 / Market 42 / Op 40,092 / Total 587,449.
**Note the existing workbook row put FY2022's 313 on the "Counterparty credit risk incl CVA"
row; per the FY2022 and FY2023 editions' own tables that 313 is "Market Risk including CVA".**

FY2025 edition KM1 (the big gap-fill): CET1 after deductions 117,764 · Total Own Funds
137,764 · RWAs 773,493 · CET1 ratio 15.22% · Capital Adequacy Ratio 17.81% ·
leverage 9.26% (excl central bank claims; 7.80% including them) · LCR 180% ·
NSFR 133%.

NSFR from the Pillar 3 KM1 (HBZ disclosed it voluntarily well before the UK mandate):
2017 139.68% · 2018 136.70% · 2019 135.76% · 2020 134.19% · 2021 130.16% · 2022 127% ·
2023 136% · 2024 137% · **2025 133%**. No NSFR in the FY2016 edition (it has no KM1 table).

Leverage: FY2016 edition gives a narrative figure only — "As at 31 December 2016 Bank has
a leverage ratio of **9.6%**" (§7). This closes the one cell the script had marked a genuine
FY2016 gap.

### Cross-edition restatements — DOCUMENTED, NOT OVERWRITTEN (validation gate)

HBZ restates prior-year capital in almost every new edition. Divergences found:

- **CET1 capital FY2024**: FY2024 ed 115,427 vs FY2025 ed 109,883 — difference 5,544 =
  exactly the FY2024 proposed dividend. The FY2025 edition introduced a "Proposed dividend
  for the year" regulatory deduction and restated comparatives onto it.
  Same pattern FY2023: 97,919 vs 93,777, difference 4,142 = the FY2023 proposed dividend.
- **CET1 capital FY2022**: three different published values — 81,361 (FY2022 ed),
  90,610 (FY2023 ed), 86,426 (FY2024 ed).
- **CET1 ratio FY2021**: 15.75% (FY2021 ed) vs 14.93% (FY2022 and FY2023 eds).
- **CET1 ratio FY2017/FY2018**: 18.73%/18.14% (FY2018 ed, each year's own edition — and the
  values the workbook carries) vs 18.64%/18.00% (FY2019 ed onward, after a retained-earnings
  restatement of 323k/546k).
- **Capital Adequacy Ratio FY2021**: 19.47% (FY2021 ed) vs 18.65% (FY2022/FY2023 eds, and
  the workbook's value).
- **Leverage FY2019**: 10.03% (FY2019 ed) vs 9.03% (FY2020/FY2021 eds) vs 9.49% (AR KPI
  table, the workbook's value) — three published values.
- **Leverage FY2024**: 10.18% (FY2024 ed, the workbook's value) vs 9.69% excl central bank
  claims / 8.41% incl them (FY2025 ed). Basis change plus restatement.
- **Total RWAs FY2019**: 461,590 (FY2019 AR KPI table, the workbook's value) vs 442,493
  (FY2019/FY2020/FY2021 Pillar 3 AND the FY2020 AR's own comparative). Two-to-one against
  the workbook value but it is that year's own AR figure — kept, both documented.
- **Total RWAs FY2016**: 336,350 (AR KPI) vs 336,541 (FY2016 Pillar 3 §5.2).

Per the standing validation gate none of these were force-reconciled; the workbook keeps
each year's own originally-published figure and the divergence is recorded in the source
citation.

### LCR — kept on separate rows, never merged

The workbook's LCR row is the Annual Report's **average-for-the-period** series. The Pillar 3
KM1's LCR is the **point-in-time 31 December** figure (confirmed: the script's own pre-existing
note said "As-at-31-December figures are higher every year (e.g. FY2025 180%, FY2024 243%)",
and the FY2025/FY2024 Pillar 3 KM1s print exactly 180% and 243%). Added as a **second,
separately labelled row**, per the LCR standing rule. Pillar 3 KM1 series:
2017 235.82% · 2018 198.04% · 2019 159.81% · 2020 226.83% · 2021 153% · 2022 405% ·
2023 286% · 2024 243% · 2025 180%. (The FY2025 edition restates FY2024 to 250%.)

**STATUS: DONE** — written into `scripts/build_habib_bank_zurich.py`, rebuilt, 18 sheets.

---

## 2. Ghana International Bank plc — `scripts/build_ghana_international_bank.py`

**STATUS: DONE** — written into the build script, rebuilt, 18 sheets.

- **No enumerating index exists.** https://www.ghanabank.co.uk/about-us/ links only the
  latest set (AR 2024, AR 2025, summary FS 2025, 5-year financials 2025, P3 2024). It is
  not a history, so it cannot produce enumerated negatives. Every path below came from
  **search**, which means both negatives here are **weak negatives** and are recorded in
  the script as explicitly re-checkable, with a note telling a future pass not to promote
  them to permanent without an index or a statement from the Bank.
- **ghanabank.co.uk fails TLS verification for WebFetch; use curl.** Recorded in the
  script too, since a fetch failure here is a transport problem, not a missing document.
- Continuous Pillar 3 run FY2019–FY2024, under `https://www.ghanabank.co.uk/app/uploads/`:
  2019 `2020/11/GHIB-2019-Pillar-3-Disclosures_FINAL_publish-on-website.pdf` ·
  2020 `2021/06/Pillar-3-Disclosures-2020.pdf` ·
  2021 `2022/10/GHIB-2021-Pillar-3-Disclosures.pdf` ·
  2022 `2023/09/GHIB-2022-Pillar-3-Disclosures.pdf` ·
  2023 `2024/11/GHIB-2023-Pillar-3-Disclosures.pdf` ·
  2024 `2025/11/GHIB-2024-Pillar-3-Disclosures.pdf`
- Nothing before 2019 found by search. **Weak negative, re-checkable.**
- No FY2025 Pillar 3 posted yet (the FY2025 AR is, Apr 2026). **Weak negative, re-checkable.**

### What the script previously had, and what changed

The script already cited FY2021–FY2024. It had **no Pillar 3 source at all for FY2019 or
FY2020** — FY2020 fell back to the Annual Report (CET1 ratio "35.3%", LCR "310%") and
FY2019 was blank across every metric. Both editions are now sourced and read.

Cells filled (all transcribed, none derived):

| metric | FY2019 | FY2020 |
|---|---|---|
| CET1 / Tier 1 / Total Capital (£'000) | 137,828 | 131,539 |
| CET1 / Tier 1 / Total Capital Ratio | 41.86% | 35.33% (was "35.3%") |
| Total RWAs (£'000) | 329,260 — see below | 372,287 |
| Leverage Ratio | 20.06% | 17.14% |
| LCR | 278.41% | 310.06% (was "310%") |
| NSFR | none in that edition | 198% |

Plus **FY2021 NSFR = 195%**, which had been blank — found in the FY2021 edition's Table 1
(image, read visually) and corroborated by that document's own narrative.
Plus the **RWA Breakdown sheet gained FY2019 and FY2020** exposure-class columns, including
an "Exposures in Default" class that only the FY2019 table carries.

### FY2019 Total RWA — the Redwood defect again

The FY2019 edition's Table 1 prints "Total Risk-Weighted Assets 281,553". That is the
**credit-risk subtotal**, not total RWAs. Three independent proofs, all inside the documents:
1. The same Table 1 prints CET1 137,828 and a CET1 ratio of 41.86%; 137,828/281,553 = 48.95%.
2. FY2019 Table 2 shows 281,553 as the total of the credit-risk exposure-class rows only,
   with operational risk (cap. req. 3,731) and market risk (85) listed *below* that total.
3. The FY2020 edition's narrative states RWAs went "£329.26m in 2019 to £372.29m in 2020".

Carried 329,260 (transcribed from proof 3 — **not** back-solved from the ratio), with the
as-printed 281,553 preserved on its own labelled second row. The RWA Breakdown sheet's
component sum for FY2019 comes to 329,254, corroborating. FY2020 has no such defect
(325,809 + 45,813 + 675 = 372,297 vs 372,287 printed).

### Other things corrected or flagged, not overwritten

- **NSFR note was wrong.** It read "NSFR only reported from FY2022 onward - the Bank states
  comparable figures for earlier periods are not available". The Bank does say that (about
  CRR2 comparability), but it had in fact published an NSFR in FY2020 and FY2021. The two
  claims were being conflated; the note now separates them.
- **Leverage basis differs across editions.** FY2019/FY2020 head the line "Basel III
  leverage ratio" (and mislabel it "exposure measure (%)" when the value is a ratio);
  FY2021+ head it "UK leverage ratio", which is the measure that excludes central bank
  claims and is what the sheet's row title asserts. FY2019/FY2020 may therefore sit on the
  wider denominator. Flagged as unstated basis, not force-fitted.
- **FY2021 leverage** — Table 1 says 15.20% (carried), narrative says 15.18%. As printed.
- FY2019's Table 1 and Table 2 are **images**; both were read **visually** from rendered
  pages rather than OCR'd, per the project rule. Same for FY2021's Table 1.

---

## 3. Persia International Bank plc — `scripts/build_persia_international_bank.py`

**STATUS: DONE** — written into the build script, rebuilt, 18 sheets. No cells filled, as
intended; this was a negative-recording task.

### What the script already had (and was left alone)

The script's `P3_CESSATION_NOTE` already carried most of the sourced negative: the "available
on request" wording, the site's one-Pillar-3 enumerated negative, the Wayback CDX enumeration,
the Companies House Active status, and the sanctions notice. FY2021's CET1/Tier 1/Total
Capital ratios of 40.99% from the 2021 Pillar 3 were left untouched, as instructed.

### What was added or corrected this pass

1. **OCR re-verified visually.** Every one of these filings is a scanned image with no text
   layer, and the p.8 paragraphs had only been OCR'd. The FY2022 and FY2025 pages were
   re-rendered and read by eye. Both quotations confirmed word-for-word:
   - FY2022 p.8: *"Pillar 3 disclosures are made separately and are published on the Bank's
     web site at www.persiabank.co.uk."*
   - FY2025 p.8 of 82: *"Pillar 3 disclosures are made separately and can be made available
     on request."*
2. **Correction:** the section is the **Strategic Report**, not the Directors'/corporate
   governance report as the script previously recorded.
3. **FY2022 separated from FY2023–FY2025** as a different kind of negative. FY2023–25 are a
   declared non-publication (complete answer, do not re-chase). FY2022 is
   published-then-removed — asserted as published at the time, absent from the site now and
   never captured by the Internet Archive — so it is the one year of the four where a copy
   might still be findable.
4. **Going-concern context added**, read visually. FY2025 auditor's report p.24 of 82 carries
   "Material uncertainty related to going concern" citing note 2.2, US sanctions on Iran, the
   Iran-Israel war and correspondent-banking/clearing difficulties, ending *"Our opinion is
   not modified in respect of this matter"*. The FY2022 report (p.19) carries the equivalent.
   Recorded with the not-modified qualifier explicit, so it reads as disclosed uncertainty
   rather than an adverse opinion — and as further proof the entity has not wound down.

### Original brief, retained for reference

Task is to record a **sourced negative of the "available on request" shape** — a complete
answer, not an open gap. Do NOT expect to fill cells.

- **NOT wound down.** Companies House 04218020 shows it **Active**, full accounts filed to
  31 Mar 2025 (filed 2 Sep 2025, 82pp).
- Own site (`http://www.persiabank.co.uk/` — **https resets the connection**) links exactly
  ONE Pillar 3: `http://www.persiabank.co.uk/Pillar%203%202021%20v3.pdf` (31 Mar 2021,
  28pp). That is an **enumerated negative** for FY2022–FY2025 on its own site.
- **Decisive evidence** — Directors' report p.8 "Pillar 3 Disclosures" paragraph:
  - FY2022 accounts: *"Pillar 3 disclosures are made separately and are published on the
    Bank's web site"* — claimed published, but no longer on the site → published-then-removed.
  - FY2023, FY2024, FY2025 accounts: *"Pillar 3 disclosures are made separately and can be
    made available on request."* → sourced "not publicly disclosed, available on request",
    the same shape as Havin.
  - Source pages are **scanned images**; the peer OCR'd them. **Re-verify any digits visually.**
- Material context to record: site notice says Persia "has been made subject to financial
  sanctions by the UK Government and the European Union as of 29 September 2025" (OFSI
  General Licence INT/2025/7345464); the FY2022 and FY2025 auditor's reports both carry a
  going-concern material uncertainty.
- **Do not disturb**: an earlier pass today already filled FY2021 CET1/Tier 1/Total Capital
  ratios (40.99%) from the 2021 Pillar 3 §3.4.
- Accounts on Companies House, prefix
  `https://find-and-update.company-information.service.gov.uk`:
  - FY2025 `/company/04218020/filing-history/MzQ3OTMzNTI0NWFkaXF6a2N4/document?format=pdf&download=0`
  - FY2024 `/company/04218020/filing-history/MzQzMzA4NzcwMWFkaXF6a2N4/document?format=pdf&download=0`
  - FY2023 `/company/04218020/filing-history/MzM4OTExNTc1NmFkaXF6a2N4/document?format=pdf&download=0`
  - FY2022 `/company/04218020/filing-history/MzM1NTU5ODQzNmFkaXF6a2N4/document?format=pdf&download=0`
  - FY2021 `/company/04218020/filing-history/MzMxMTg0NDU2NWFkaXF6a2N4/document?format=pdf&download=0`
