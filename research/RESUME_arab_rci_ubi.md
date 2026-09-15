# RESUME — Arab Bank Europe / RCI Bank UK / Union Bank of India (UK)

Batch started 2026-09-15. Checkpoint file: update after each bank, not at the end.

## Bank 1 — ARAB BANK EUROPE PLC (`scripts/build_arab_bank_europe.py`)

### URLs fetched and what they turned out to be
- `https://www.eabplc.com/downloads/Pillar3EAB_PLC_2024.pdf` — **DEAD**. HTTP 200 but
  `content_type: text/html`, 95,415 bytes, `url_effective` = `https://arabbankeurope.com/`.
  It is the Arab Bank Europe homepage, not a PDF. Same for
  `https://www.eabplc.com/downloads/Pillar3EABplc2023.pdf` — byte-identical 95,415-byte
  homepage HTML. Confirms the script's existing note; these two Google-indexed paths are
  not obtainable.
- Wayback CDX, full `eabplc.com` domain, unfiltered (1,546 rows), grepped for `pillar`:
  **12 Pillar 3 documents, all FY2020 or earlier except one**. Full list:
  2009, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, a v13 2010 file, and
  `https://www.eabplc.com/downloads/Pillar3.pdf` captured 2024-07-13 (the FY2022 edition,
  already cited in the script). **No FY2021, no FY2023, no FY2024 capture exists.**
- Wayback CDX, full `arabbankeurope.com` domain: only 20 rows, no PDFs at all.

### Determinations
- FY2021 Pillar 3: **enumerated absent**, not merely "not found". Wayback holds EAB's
  Pillar 3 series continuously 2009-2020 and then jumps to the FY2022 edition. FY2021's
  own edition was never archived. FY2021 capital/RWA/LCR are already sourced from the
  FY2022 edition's comparative column, so the loss is limited to FY2021 leverage/NSFR,
  which that edition itself flags `n/a` (templates only effective 1 Jan 2022) — structural.
- TRAP avoided: `arabbank.ae` "Pillar III Disclosures YE2021" = Arab Bank plc (Jordan),
  the parent. Not fetched, not used.

### BASIS DETERMINATION — resolved, quoted verbatim
Read the FY2022 Pillar 3's own Scope section (PDF p.5). Verbatim:
> "The EAB Group comprising EAB plc and its subsidiary, Europe Arab Bank SA ('EAB SA'),
> operates through offices in four European countries."
> "In line with the requirements of the UK CRR, Pillar 3 disclosures have been prepared on
> consolidated basis, and where relevant, provide quantitative disclosures for both, Group
> and EAB plc solo entity."
> "EAB Group is subject to consolidated supervision, with EAB plc also subject to solo
> regulatory supervision by the PRA."

So "EAB Group" IS the UK entity's own consolidated basis, not the Jordanian parent's —
usable. But the script already uses the stricter **EAB plc solo** column, which is better
and consistent with every other sheet. Kept solo. Bases differ materially at 31 Dec 2022:
Group CET1 EUR290m / RWA EUR1,810m / 16.0% / LCR 249% / NSFR 128% / lev 11.4%
Solo  CET1 EUR253m / RWA EUR1,631m / 15.5% / LCR 218% / NSFR 120% / lev 11.7%

### Validation gate — PASSED
Every figure already in the script reproduces the KM1 table exactly (EAB plc column):
CET1 253/252, Tier 1 253/252, Total capital 370/362, RWA 1,631/1,616, CET1 ratio
15.5%/15.6%, Total capital ratio 22.7%/22.4%, leverage 11.7%/n-a, LCR 218%/267%,
NSFR 120%/n-a. Nothing overwritten.

### Cells filled: ZERO — and that is the correct answer
The ~20 "gap" cells (Leverage/NSFR FY2021, FY2023, FY2024; CET1/Tier 1 Capital FY2023,
FY2024) are genuinely not disclosed anywhere obtainable. FY2021 leverage/NSFR are
STRUCTURAL: the FY2022 edition's own FY2021 comparative column prints `n/a` with the
footnote "These disclosures have been implemented from 1 January 2022... Prior periods,
'n/a' indicates that the disclosure is new or changed and no comparatives are being
provided." Nothing was derived or back-solved.

### Edits actually written to `scripts/build_arab_bank_europe.py`
1. New `BASIS_NOTE` constant — the verbatim Scope quotes above + the Group/solo figure
   contrast + why solo was chosen. Appended to `PILLAR3_SOURCES`, so it lands on every
   Pillar 3 sheet and the RWA Breakdown sheet.
2. New `SDDT_NOTE` constant — the NOT-SDDT-exempt finding (FRN 446951 has three PRA
   waiver rows, none of them Disclosure (CRR) Rule 3.1) plus the 2026-09-15 availability
   re-enumeration. This finding previously existed ONLY on the RWA Breakdown sheet; it
   now also reaches `NOT_DISCLOSED_NOTE` and `FY2324_ONLY_NOTE`, i.e. every blank Pillar 3
   metric sheet. That was the real correction: the blanks were reading as ordinary
   absence when they are a missing required disclosure.
3. LCR sheet — row relabelled "(12-month average basis)" and note now quotes the source
   footnote 3 ("simple average of the 12 preceding month-end observations") with the
   HQLA/net-outflow components, per the standing LCR-basis rule.
4. MREL sheet note — flags MREL as the ONE metric whose absence is plausibly structural,
   to stop the new SDDT_NOTE over-claiming across it.
Rebuilt: 18 sheets, OK.

---

## Bank 2 — RCI BANK UK LIMITED (`scripts/build_rci_bank_uk.py`)

### THE KEY TASK — VERIFIED. FY2020/FY2021/FY2022 are now a permanent SOURCED NEGATIVE.
Both PDFs downloaded clean (FY2024 786KB/27pp, FY2023 725KB). Verbatim, from matching
"Frequency of disclosures" paragraphs in each document's Scope section:

- **FY2023 edition, section 1.4 "Scope of the Report", printed p.9:**
  > "Our Pillar 3 Disclosures are published annually with this being the first iteration
  > of the document for MFS UK."
- **FY2024 edition, section 1.3 "Scope of the Report", PDF p.9 (printed p.8):**
  > "Our Pillar 3 Disclosures are published annually with this being the second iteration
  > of the document for RCI Bank UK."

Two independent, mutually corroborating self-descriptions. The FY2024 cover page also
carries "Version 2.0" separately. **No Pillar 3 disclosure was ever produced for any year
before FY2023.** FY2020-FY2022 capital amounts / RWAs are unobtainable permanently, not
"not yet found". Do not re-chase.

Corroborated by enumeration so it does not rest on the sentence alone:
- The bank's own index https://www.rcibank.co.uk/about-us/facts-and-figures scraped this
  session links exactly TWO Pillar 3 PDFs (FY2023, FY2024) and no earlier one.
- Wayback CDX over the whole rcibank.co.uk domain (6,645 unique captures) returns exactly
  three Pillar 3 URLs = those same two documents (FY2023 appears twice, once under an old
  /staging/import/ufile/ path).

### TRAP confirmed present and rejected
The same facts-and-figures page hosts `2021 RCI Business Report EN.pdf`,
`RCI_BANQUE_MOBILIZE_Business Report 2022.pdf`, `rci2020_business_report_2020_12.pdf`,
`RCI2023_MOBILIZE_RAPPORT_ACTIVITE_EN_MEL-2_2024_02_19.pdf` — all RCI Banque SA /
Mobilize FRENCH PARENT GROUP. Their year coverage looks exactly like the FY2020-FY2022
blanks, which is the trap. Not used; now documented in the script so a future pass
rejects them without re-opening them.

### Validation gate — PASSED, and one real bug found
FY2024 KM1 reproduces the script exactly: CET1 707/669, Tier 1 707/669, Total capital
809/774, RWA 5,247/4,842, CET1 ratio 13.46%/13.81%, Tier 1 13.46%/13.81%, TCR
15.42%/15.99%, leverage 10.6%/10.9% on exposure 6,642/6,148, LCR 287%/236% on HQLA
899/1,035 and net outflows 365/467, NSFR 126%/130% on ASF 6,115/5,622 and RSF 4,863/4,312.

**BUG: CET1 Ratio FY2024 was 13.69% while Tier 1 Ratio FY2024 was 13.46%.** That is
internally impossible — Tier 1 = CET1 + AT1, so the Tier 1 ratio can never be below the
CET1 ratio. Cause: CET1 was taken from the annual-report narrative, Tier 1 from the
Pillar 3 KM1. KM1 rows 5 and 6 both read 13.46%, and rows 1 and 2 both read GBP707m
(AT1 nil). Corrected to 13.46%; the superseded 13.69% preserved on its own labelled row
per the document-both rule. Overview updated too (it is a copy).

### Cells filled: 1 corrected (CET1 Ratio FY2024), 0 newly filled
Nothing was derivable. Not back-solved: FY2020-FY2022 capital amounts could have been
faked as ratio x RWA and were not.

### Edits written to `scripts/build_rci_bank_uk.py`
1. New `P3_NONEXISTENCE_NOTE` — both verbatim quotes with page refs, the two enumeration
   corroborations, and the parent-group trap. Appended to `P3_SOURCES`, so it lands on
   every Pillar 3 metric sheet.
2. `CET1_RATIO` / `CET1_RATIO_AR` / `CET1_RATIO_NOTE` — the correction above; CET1 Ratio
   sheet now has two labelled rows.
3. Tier 1 Ratio note rewritten to cross-reference the correction.
4. `SUFFIX` constant appended to the CET1 Capital / Tier 1 Capital / Total Capital notes
   marking FY2022-FY2020 as a permanent sourced negative, "do not re-chase".
Rebuilt: 18 sheets, OK.

---

## Bank 3 — UNION BANK OF INDIA (UK) LIMITED (`scripts/build_ubi_uk.py`)

Script filename is `build_ubi_uk.py` (NOT build_union_*). `build_union_bancaire_privee_uk.py`
is a different bank — not touched.

### URLs fetched
- Index `https://www.unionbankofindiauk.co.uk/disclosures/financial-reports` — 86KB HTML,
  parsed every PDF link. Carries exactly **11 Pillar 3 documents, unbroken annual series**:
  31-03-2015 through 31-03-2025. **No 31-03-2026.**
- `.../Portals/0/Annual%20Accounts%20UBIUK%202026%20Signed_1.pdf` — real 2.7MB PDF,
  FY2026 annual report. Already cited throughout the script for BS/P&L/equity/cash flow.
- `.../Portals/0/pdf/Final_Pillar_3_Disclosure-31-03-2025.pdf` — real 2.3MB PDF, FY2025.

### FY2026 — enumerated negative, RE-CHECKABLE (this is the distinction that matters)
The FY2026 **annual accounts are already on the index**, so the index is demonstrably
current for FY2026 — the Pillar 3 is simply behind it. And because the Pillar 3 series is
*unbroken* 2015-2025, its stopping point is informative: this bank does not skip Pillar 3
years, so FY2026's absence reads as not-yet-published, not a policy change or SDDT opt-in.
**Re-check trigger:** refetch the index and look for a "Pillar 3 Disclosure 31-03-2026"
entry; when it appears every FY2026 Pillar 3 cell becomes fillable in one pass.
Contrast with RCI FY2020-FY2022, which is *permanent* (never produced).

### FY2026 annual report re-read in full — nothing fillable
Full-text scan for CET1 / Tier 1 / Tier 2 / RWA / risk-weighted / own funds / capital
ratio / leverage ratio / LCR / NSFR / MREL returns **no quantitative disclosure of any**.
Only narrative: Strategic Report "Capital Adequacy Ratio remained well above regulatory
requirements", "both the Liquidity Coverage Ratio (LCR) and Net Stable Funding Ratio
(NSFR) remained well within Board-approved thresholds" — no figures. Capital Risk note
(p.67) says only that the Bank "has had surplus capital over and above the capital
required as per the ICG during the year" and "The Bank's regulatory capital is
categorised into Tier one capital, which includes ordinary share capital, and retained
earnings as shown in statement of change in equity."
**That last sentence is a trap**: it points at book equity. Reading a Tier 1 figure across
from equity would be a back-solve. NOT done.

### 31 March year-end
Confirmed and now stated at the top of the Pillar 3 source note. Did NOT change
`YEAR_LABEL` to embed "YE 31 Mar" in the column headers — column header strings are parsed
by the insights extraction pipeline and I was instructed not to run the test suite or
refresh_all.py, so changing them unverified would risk silent downstream breakage.
Recorded in prose instead.

### Cells filled: ZERO — correct answer; negative strengthened from description to count
### Edits written to `scripts/build_ubi_uk.py`
1. Year-end paragraph prepended to `p3_sources()` — 31 March, what each FY label means,
   and the cross-bank comparability caveat vs December-year-end banks.
2. "FOURTH INDEPENDENT CHECK" paragraph — the precise 11-document enumeration, the
   unbroken-series argument, the FY2026-accounts-present-but-P3-absent observation, the
   explicit re-check trigger, and the full-text-scan result with the equity-pointer trap
   called out.
Rebuilt: 18 sheets, OK.

---

## BATCH COMPLETE — all three rebuilt, 18 sheets each
`git diff --numstat`: build_arab_bank_europe.py +123/-7, build_rci_bank_uk.py +110/-11,
build_ubi_uk.py +161/-55. All three .xlsx regenerated.
Not run (per instructions): refresh_all.py, test suite. Not committed.
