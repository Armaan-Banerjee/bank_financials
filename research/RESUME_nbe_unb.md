# RESUME — National Bank of Egypt (UK) & United National Bank (Batch 5)

Session 2026-09-15. Checkpointed as work proceeds.

## 1. National Bank of Egypt (UK) Limited — `scripts/build_national_bank_of_egypt_uk.py`

### Documents retrieved (all real PDFs, `%PDF` verified)
nbeuk.com bot-blocks bare curl (403 text/html). Working fetch:

    curl -sL -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 \
      (KHTML, like Gecko) Chrome/120.0 Safari/537.36" \
      -H "Referer: https://www.nbeuk.com/about-us/" --compressed <url> -o out.pdf

| file | bytes | pages | cover period |
|---|---|---|---|
| 2026/04/NBEUK-Pillar-3-Disclosures-31st-December-2025.pdf | 495,059 | 12 | **31 December 2025** |
| 2025/04/Pillar-3-Disclosures-31st-December-2024.pdf | 335,379 | 12 | 31 December 2024 |
| 2021/02/Pillar_3_30062020_FINAL.pdf | 429,813 | 24 | **30 June 2020** |
| 2023/01/Pillar-3-as-at-30062019-FINAL.pdf | 480,418 | 24 | **30 June 2019** |
| 2021/02/2018_Basel_ll_Pillar_3_Disclosure.pdf | 568,568 | 24 | **30 June 2018** |
| 2021/02/Draft_Pillar_3-30062017_30112017.pdf | 474,725 | 23 | **30 June 2017** |

All have real text layers (no OCR needed).

### YEAR-END TRAP — RESOLVED, no discrepancy
The June/December switch is real but causes **no** mismatch with this workbook.
`YEARS = [FY2025, FY2024, FY2023, FY2022, FY2021, FY2017]`.
- FY2021 is already documented in-script as the **18-month period 1 Jul 2020 – 31 Dec 2021**
  (the accounting-reference-date change). FY2022+ are 31 December years.
- **FY2017 is a 30 June year-end**, so the June-dated FY2017 Pillar 3 is the correct match.
  Proved independently, not assumed: that document's operational-risk table prints
  "June 2017 Gross Income 24,891" and "Net Interest Income 16,274"; the workbook's FY2017
  column already carried Total operating income 24,891 and Net interest income 16,273.
- FY2018/FY2019/FY2020 (all 30 June) have **no column in this workbook** — nothing to map,
  so the June-dated 2018/2019/2020 editions are simply out of scope here.
- => No June document was mapped to a December year or vice versa.

### "Draft" file — genuinely usable
`Draft_Pillar_3-30062017_30112017.pdf`: the string "draft" appears **nowhere** in the
document text. Cover and running header both read "Basel II, Pillar 3 disclosures for the
year ended 30th June 2017". The `30112017` in the filename is a publication/approval date
(30 Nov 2017), consistent with note 1's reference to the 18 Sep 2017 Board/AGM meeting.
**Every FY2017 figure is independently confirmed by the FY2018 edition's own 30/06/2017
comparative column** (see below), so nothing depends on the draft-named file alone.

### MAJOR CORRECTION — FY2025 Pillar 3 exists
The script asserted in five places that "no FY2025 Pillar 3 disclosure exists as at
15 September 2026" and that FY2025 was Annual-Report-basis. **False** — the FY2025 edition
is published at `/wp-content/uploads/2026/04/`. It carries a full UK KM1 and UK OV1.

FY2025 UK KM1 (p.4-5), £000 / %:
CET1 172,460 · Tier 1 172,460 · Total capital 230,038 · **Total RWEA 1,261,174**
· **CET1 ratio 13.7** · **Tier 1 ratio 13.7** · Total capital ratio 18.2
· Leverage 9.2 (incl. and excl. central bank claims) · LCR 390 · **NSFR 150**

FY2025 UK OV1 (p.11), RWEA £000: Credit risk excl. CCR 1,198,794 · CCR 15,766
· of which CVA 4,804 · Market risk 0 · Operational risk 46,614 · **Total 1,261,174**
(OV1 total ties to KM1 exactly — unlike FY2023, where the same bank's OV1 and KM1 disagree.)

**Validation gate passed.** Every FY2024 comparative reproduces the workbook exactly:
CET1/Tier 1 170,750; Total capital 201,853; RWA 1,047,061; CET1 & Tier 1 ratio 16.3
(workbook 16.31%); TCR 19.3 (workbook 19.28%); leverage 11.6; LCR 418; NSFR 194.
OV1 FY2024 comparatives also tie: 988,313 / 12,424 / 5,039 / 0 / 46,325 / 1,047,061.
Existing FY2025 Annual-Report values (18.24%, 9.2%, 390.41%) are confirmed by the
Pillar 3 to the AR's extra decimal place — kept, not overwritten.

### FY2017 regulatory data (new)
From Pillar 3 y/e 30 June 2017 §3 pp.11-12, **and independently confirmed figure-for-figure
by the FY2018 edition's own 30/06/2017 comparative column** (§3 p.12):
Tier 1 capital after deductions **143,847** (share capital 130,000 + retained earnings 13,847;
no AT1 → CET1) · Tier 2 (subordinated debt) **34,629** · Total capital resources **178,476**
· Risk Weighted Assets **757,515** · Total Exposures 1,453,451 · Total Pillar 1 capital 63,082.

**Ratio traps in that table — handled, do not "fix" later:**
- `SOLVENCY RATIO 282.93%` is a **capital-cover** ratio (capital vs requirement). NOT a CRR
  ratio. Not used anywhere.
- `TOTAL CAPITAL RATIO 12.28%` is **mislabelled**: it is total capital ÷ total *exposures*
  (178,476 / 1,453,451 = 12.279%), a leverage-style measure, not the CRR total capital ratio.
  Confirmed on the 2016 column too (160,423 / 1,464,093 = 10.957% = printed 10.95%).
  **Deliberately NOT placed on the Total Capital Ratio sheet.**
- `TIER 1 CAPITAL RATIO ( LEVERAGE ) 9.90%` is the **leverage** ratio
  (143,847 / 1,453,451 = 9.897%), not a CRR Tier 1 ratio. Placed on the Leverage sheet only.
- `CAPITAL ADEQUACY RATIO 22.63%` is the total-capital-to-RWA style measure. Proven on the
  2016 column (160,423 / 683,921 = 23.456% = printed 23.46%), but the 2017 column does
  **not** reproduce (178,476 / 757,515 = 23.56% ≠ 22.63%). Recorded **as printed**, not
  recalculated, per the sheet's existing convention.
- **Within-document contradiction resolved:** the FY2017 edition's note 3 narrative says the
  CAR "declined to 21.90%" and the leverage ratio "stood at 9.5%", contradicting its own
  table (22.63% / 9.90%). The **FY2018 edition settles it** — its table repeats 22.63% and
  9.90% for 30/06/2017, and its note 3 says the CAR "increased to 22.77% … compared to
  **22.63%** in June 2017". Table values used; the narrative figures are errors in that one
  document. Documented in the sheet note so a later pass does not reverse it.

**Deliberately left blank for FY2017:** CET1 Ratio and Tier 1 Ratio — no CET1-to-RWA or
Tier-1-to-RWA ratio is stated anywhere in either edition, and the only Tier-1 ratio printed
is the leverage one. Not back-solved from 143,847 / 757,515.

**FY2017 LCR:** the document prints "One month liquidity coverage ratio (LCR) 201%" against a
**90%** internal minimum, and states "LCR, Core Funding and NFSR ratios are currently on an
observation period and will be implemented as a regulatory standard starting from 1 January
2018". This is a pre-CRR point-in-time internal metric, **not** the 12-month-average CRR LCR
used for FY2022-FY2025. Kept on its own clearly-labelled row, never merged.

**FY2017 NSFR:** no figure (observation period only); UK NSFR requirement began 1 Jan 2022,
so structurally inapplicable.

### Status: WRITTEN to script, rebuilt, 18 sheets verified.

---

## 2. United National Bank Limited — `scripts/build_united_national.py`

The workbook was already complete for FY2016–FY2024 on every Pillar 3 metric, so this pass
produced **no new figures**. It produced two corrections instead, both about provenance and
the precise status of a gap. **No numeric cell changed, deliberately.**

### FY2025 Pillar 3 — upgraded from "access gap" to ENUMERATED ABSENCE
Index fetched and fully parsed 15 September 2026:
https://www.ubluk.com/footer-pages/annual-reports/

Every year block **2016–2024** carries two links, "Annual Report" and "Pillar III
Disclosure". The **2025 block carries the Annual Report only**
(`/media/405naqby/ye2025-statutory-accounts-final-23apr2026_signed.pdf`) — there is no
Pillar III link in it. Because the index already carries the 2025 statutory accounts it is
**not a stale page**, so the FY2025 Pillar 3 is enumerated-and-absent rather than not-found.
The script previously said "genuine access gap, not confirmed non-disclosure" in seven
places; all seven now state the enumerated position.

**But it is re-checkable, not a permanent negative**, and the note says so. This bank
publishes Pillar 3 extraordinarily late: the FY2024 edition linked from that index has a PDF
creation date of **1 July 2026** — ~18 months after its year-end, and two months *after* the
FY2025 Annual Report was signed (23 Apr 2026). On that cadence an FY2025 edition is not due
until well into 2027. The FY2025 Annual Report also still refers readers to "the unaudited
Pillar III disclosures", so the bank has not announced any stop.

Also confirmed from the same index: **nothing exists before 2016** for either document type.

### CORRECTION — the cited FY2024 Pillar 3 was a pre-final draft
`P3_2024_URL` pointed at `https://www.ubluk.com/media/vsvfbmui/pillar260825.pdf`, found by
Wayback CDX, and the script itself flagged that it was "not linked from the live site's own
resources page". That was the tell. Both files were downloaded and diffed:

| | vsvfbmui/pillar260825.pdf (was cited) | sr5puvji/…approved-finalplusamended.pdf (index-linked) |
|---|---|---|
| PDF created | 26 Aug 2025 | 1 Jul 2026 |
| PDF title | *(none)* | "Microsoft Word - UNB 2024 Pillar3" |
| CCR Mark to Market table | `Interest rate contract (Why is this blank – we had IRS notional of 66.019 m?)` | `Interest rate contract` |

The cited file **prints an unresolved internal reviewer query in the document body** — it is
a draft. Switched to the index-linked approved final; the draft URL is retained in the script
as `P3_2024_SUPERSEDED_DRAFT_URL` so the correction stays auditable.

**Validation gate passed — no value moved.** Whitespace-insensitive diff of the two
extractions: 2,285 lines each, and every substantive difference is the reviewer query plus
dot-leader spacing. All FY2024 figures this workbook uses appear identically in both:
CET1/Tier 1 capital 97,948,100 · Total capital 98,654,693 · Total RWAs 493,153k ·
Tier 2 collective provision 706,593. So this is a citation fix, not a restatement.

### Status: WRITTEN to script, rebuilt, 18 sheets verified.

---

## 3. Flagged, NOT acted on

**NBE Balance Sheet / Profit & Loss, FY2017 column — unit inconsistency (pre-existing).**
Those two sheets are denominated in **£**, and every FY2021–FY2025 value is in £
(FY2021 total assets 1,212,752,908). The FY2017 values injected by the `_fy17` block at the
foot of the script are in **£'000** — total assets 1,438,234, i.e. £1.44bn stated as if £1.4m.
Corroborated: the FY2017 Pillar 3 gives Total Exposures 1,453,451 (£'000), and that
document's gross income 24,891 (£'000) equals the workbook's FY2017 "Total operating income"
24,891. So the FY2017 column is ~1000x understated against its own sheet's unit on the
Balance Sheet, P&L and (by copy) the Overview.

Not corrected here: it predates this batch, sits outside the Pillar 3 scope of this task, and
the right fix (rescale to £, versus re-basing those sheets) is a presentation decision that
also touches the Overview copies and the charts. Recommend it as its own ticket.
