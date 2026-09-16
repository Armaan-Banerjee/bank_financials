# RESUME — ICICI Bank UK Plc Pillar 3 series (session started 2026-09-16)

Target script: `scripts/build_icici_bank_uk.py`
Workbook: `banks/ICICI BANK UK FINANCIALS.xlsx`
Entity: **ICICI Bank UK PLC** (Companies House 04663024, FRN 223268). NOT ICICI Bank Limited.
Year-end: **31 MARCH**. Reporting currency: **USD**.
Index page: `https://www.icicibank.co.uk/personal/basel-disclosures` (200, text/html).

Predecessor session's notes: `research/RESUME_icici.md` (2026-09-15) — still valid; this file
supersedes it only on the Total RWA question.

## 1. INDEX ENUMERATION (done 2026-09-16)

The index carries **27 `.pdf` links**, of which **19 are Basel Pillar 3 editions**. The other 8
are not Pillar 3 key-metric documents:

- `Remuneration_Policy_Disclosure_2015.pdf` / `_2014.pdf` / `Remuneration-Policy-Disclosure-2013.pdf` /
  `Remuneration_Policy_Disclosure_Nov8_2012.pdf` — Pillar 3 remuneration only, no capital/RWA.
- `REP020.pdf` (index label "REP020 2026"), `Climate-Change-Updated.pdf`,
  `anti_money_laundering.pdf`, `Libor_Transition_faqs.pdf` — not Pillar 3.

**All 27 verified live on 2026-09-16: HTTP 200, `Content-Type: application/pdf`, `%PDF` magic
bytes, non-zero `pdfinfo` page count. No 401/403/429/503, no soft-404.** Byte sizes returned by
the server match the locally-held copies exactly for all 19 Pillar 3 editions.

### ADDITIONAL FINDING — 11 non-PDF links the index also carries

The index has 11 further "Click here" links that are **HTML popups, not PDFs**, and so do not
appear in any `.pdf` link count:

| path | label |
|---|---|
| `/personal/basel_disclosures_popup` | "Basel Disclosures for FY 2008-2025" |
| `/personal/basel-capital-resource-popup-march2019` | Capital Resources as of March 31, 2019 |
| `/personal/basel-capital-resource-popup-march2018` | …2018 |
| `/personal/basel-capital-resource-popup-march2017` | …2017 |
| `/personal/basel-capital-resource-popup-march2016` | …2016 |
| `/personal/basel_capital_resource_popup_march2015` | …2015 |
| `/personal/basel_capital_resource_popup_march2014` | …2014 |
| `/personal/basel_capital_resource_popup_march2013` | …2013 |
| `/personal/basel_capital_resource_popup_march2012` | …2012 |
| `/personal/basel_capital_resource_popup_march2011` | …2011 |
| `/personal/basel_capital_resource_popup` | …2010 |

All 11 fetched 2026-09-16, all HTTP 200 text/html. They contain a **"Composition of Regulatory
Capital as at March 31, YYYY"** table in USD'000 — capital only. **None contains any RWA,
risk-weighted exposure, or capital-ratio figure.** They are a useful independent corroboration of
the capital numbers (see §4) but cannot supply the missing RWA.

## 2. EDITION -> FINANCIAL YEAR MAPPING (dated from the COVER of each document)

Convention in this workbook: **FY<N> = the year ENDED 31 March <N>.**

| # | file basename | index label says | COVER says (verbatim) | => FY | regime per cover |
|---|---|---|---|---|---|
| 1 | `basel2_disclosures_FY2008.pdf` | "Basel II … for 2007- 2008" | "Basel II - Pillar 3 disclosures for the year ended 31 March 2008" | **FY2008** | Basel II |
| 2 | `Basel_II_p3_Disclosure_Statement.pdf` | "…for 2008- 2009" | "BaseI II - Pillar 3 disclosures for the year ended 31 March 2009" | **FY2009** | Basel II |
| 3 | `basel2_disclosures_FY09_10.pdf` | "…for 2009- 2010" | "…for the year ended 31 March 2010" | **FY2010** | Basel II |
| 4 | `basel2_disclosures_FY10_11.pdf` | "…for 2010- 2011" | "…for the year ended 31 March 2011" | **FY2011** | Basel II |
| 5 | `basel2_disclosures_March31_11.pdf` | "…for 2011- 2012" | **"…for the year ended March 31, 2012"** | **FY2012** | Basel II |
| 6 | `disclosures2012-13.pdf` | "Basel II … for 2012-2013" | "…for the year ended 31 March 2013" | **FY2013** | Basel II |
| 7 | `disclosures2013-14.pdf` | **"Basel II** Pillar 3 Disclosures for 2013-2014" | "Pillar 3 disclosures for the year ended March 31, 2014" / running head **"Basel III – Pillar 3 Disclosures / 31 March 2014"** | **FY2014** | **Basel III / CRD IV** |
| 8 | `basel3-disclosures-FY14-15.pdf` | "Basel III … for 2014-2015" | "…year ended March 31, 2015" | **FY2015** | Basel III |
| 9 | `basel3-disclosures-FY15-16.pdf` | "…for 2015-2016" | "…year ended March 31, 2016" | **FY2016** | Basel III |
| 10 | `basel3-disclosures-FY16-17.pdf` | "…for 2016-2017" | "…year ended March 31, 2017" | **FY2017** | Basel III |
| 11 | `basel3-disclosures-FY17-18.pdf` | "…for 2017-2018" | "…year ended March 31, 2018" | **FY2018** | Basel III |
| 12 | `ICICI_Bank_UK_Pillar3_disclosures_FY2018-19.pdf` | "…for 2018-2019" | "…year ended March 31, 2019" | **FY2019** | Basel III |
| 13 | `ICICI_Bank_UK_Pillar3_disclosures_FY2019-20.pdf` | "…for 2019-2020" | "…year ended March 31, 2020" | **FY2020** | Basel III |
| 14 | `ICICI-Bank-UK-Plc-Pillar3-disclosures-FY2020-21.pdf` | "…for 2020-2021" | "…year ended March 31, 2021" | **FY2021** | Basel III |
| 15 | `ICICI-Bank-UK-Plc-Pillar3-disclosures-FY2021-22.pdf` | "…for 2021-2022" | "…year ended March 31, 2022" | **FY2022** | Basel III / UK KM1 |
| 16 | `icici-bank-uk-plc-pillar-3-disclosures-FY2022-23.pdf` | "…for 2022-2023" | "…year ended March 31, 2023" | **FY2023** | UK KM1 |
| 17 | `basel-pillar-3-disclosures-FY2023-24.pdf` | "…for 2023-2024" | "…year ended March 31, 2024" | **FY2024** | UK KM1 |
| 18 | `basel-pillar-3-disclosures-FY2024-25.pdf` | "…for 2024-2025" | "…year ended March 31, 2025" | **FY2025** | UK KM1 |
| 19 | `basel-pillar-3-disclosures-FY2026.pdf` | "…for 2025-2026" | "…year ended March 31, 2026" | **FY2026** | UK KM1 |

Page counts (`pdfinfo`, all `%PDF`): 10/10/10/10/10/10/21/22/26/44/43/46/57/59/65/69/63/64/64 —
identical to the counts in the dispatch brief.

### Disagreements between cover, filename and index label

1. **`basel2_disclosures_March31_11.pdf` — FILENAME IS WRONG.** Cover: "year ended March 31,
   2012". Index label: "2011- 2012". **Index label and cover AGREE; only the filename is wrong.**
   The FY2011 edition is the separate file `basel2_disclosures_FY10_11.pdf` ("year ended 31 March
   2011"). Confirms the predecessor session's finding and the project's standing note.
2. **`disclosures2013-14.pdf` — INDEX LABEL IS WRONG ON REGIME.** The index calls it "**Basel
   II** Pillar 3 Disclosures for 2013-2014", but the document's own cover and every page's
   running head say "**Basel III** – Pillar 3 Disclosures / 31 March 2014", and §2 of the text
   describes implementing CRD IV from 1 January 2014. The period (year ended 31 March 2014) is
   right; the regime label is wrong. This matters: FY2014 is the FIRST CRD IV year, not a Basel
   II year, and the script already treats it correctly.
3. Every other file's basename follows the "FY<start>-<end>" span convention and agrees with both
   cover and index label. The two single-year names (`basel2_disclosures_FY2008.pdf`,
   `basel-pillar-3-disclosures-FY2026.pdf`) use the ENDING year, and both agree with their cover.

### Entity check

Every one of the 19 opens "ICICI Bank UK PLC ('the Bank') … a wholly owned subsidiary of ICICI
Bank Limited" and states the disclosures are prepared for ICICI Bank UK PLC, expressly
distinguishing itself from the parent's own consolidated disclosures. **No ICICI Bank Limited
(parent) figure enters this workbook.** Note that the FY2024 edition is hosted on an
`/content/dam/icicibank/india/managed-assets/…` path — a hosting-path artefact only; the document
itself is the UK entity's (verified on its own cover and Overview section).

## 3. THE BACK-SOLVED FY2014 / FY2015 / FY2016 TOTAL RWAs — RESOLVED

**Answer: the documents do NOT disclose Total RWAs for these three years. The derived figures are
therefore WITHDRAWN and the cells left blank.**

Evidence — the FY2014, FY2015 and FY2016 editions were read in full. Each has exactly four
capital-related tables, and none of them is an RWA table:

- §3.1 Capital ratios (Core Tier 1 / Tier 1 / Total capital, as a %)
- §3.2 Available capital (Tier I / Tier II / Total available capital, USD million)
- §3.3 Composition of Tier 1 capital
- §3.4 Composition of Tier 2 capital
- §4 "Minimum Capital Requirement: Pillar 1" — a **capital requirement** table by risk type

§4's printed table, verbatim caption "The following table summarises the Bank's Pillar 1 capital
requirement for various risk types", USD million:

| | Credit Risk | Market Risk | Operational Risk | **Total Capital Resource requirement under Pillar 1** |
|---|---|---|---|---|
| FY2014 | 282.3 | 2.9 | 13.8 | **299.0** |
| FY2015 | 281.8 | 0.0 | 13.0 | **294.8** |
| FY2016 | 313.5 | 0.0 | 14.0 | **327.5** |

A full-text search of all three for `risk[- ]weight|RWA|risk weighted|exposure amount` returns
only prose ("…risk-weighted assets are determined according to specified requirements…") and the
per-CQS "Risk weight" columns of the credit-risk exposure tables. **No total.** The
"Total risk exposure amount (RWAs)" line first appears in the FY2017 edition (Annexure III,
countercyclical buffer Table 2, 3,356.0) and the transitional own funds template row 60 "Total
risk-weighted assets" likewise first appears in FY2017. Neither carries a prior-year comparative
column — the FY2017 edition is single-column — so **no later edition supplies FY2014-FY2016
either.**

### Validation gate — did the derived values agree?

The derivation was `Total Capital Resource requirement under Pillar 1 ÷ 8%`:

| FY | derived (was in workbook) | = printed total ÷ 8% | disclosed figure | verdict |
|---|---|---|---|---|
| FY2014 | 3,737.5 | 299.0 / 0.08 = 3,737.5 | **none exists** | withdrawn |
| FY2015 | 3,685.0 | 294.8 / 0.08 = 3,685.0 | **none exists** | withdrawn |
| FY2016 | 4,093.8 | 327.5 / 0.08 = 4,093.75 | **none exists** | withdrawn |

There is **no disclosed figure to agree or disagree with**, so the method is neither vindicated
nor falsified by a disclosed comparison. It IS internally consistent with the printed ratios
(814.4 / 3,737.5 = 21.79% vs printed 21.8%; 623.8 / 3,737.5 = 16.69% vs printed 16.7%; FY2015
707.0 / 3,685.0 = 19.19% vs 19.2%, 538.8 / 3,685.0 = 14.62% vs 14.6%; FY2016 684.3 / 4,093.8 =
16.72% vs 16.7%, 537.6 / 4,093.8 = 13.13% vs 13.1%) — i.e. the arithmetic was right. It is
withdrawn anyway, because it is computed and this project transcribes.

### Consequence for the RWA Breakdown sheet

The same `÷ 8%` conversion produces the FY2014-FY2020 Credit / Market / Operational risk rows of
the RWA Breakdown sheet. For FY2017-FY2020 the Total RWA row is a genuine disclosed COREP figure
and only the components are converted. For **FY2014-FY2016 every cell on that sheet is
converted**, so the whole FY2014/FY2015/FY2016 column is withdrawn there too and replaced with
the printed capital requirements on their own clearly-labelled rows (a printed figure on an
honestly-captioned row, rather than a converted figure on an RWA row).

## 4. CROSS-CHECKS PERFORMED

- Capital-resource popups vs Pillar 3 §3.2, USD: FY2014 Tier1 623,794 -> 623.8 ✓, total 814,419
  -> 814.4 ✓; FY2015 538,819 -> 538.8 ✓, 707,047 -> 707.0 ✓; FY2016 537,633 -> 537.6 ✓,
  684,316 -> 684.3 ✓. Independent second source agrees with the workbook's existing capital
  figures to the rounding.
- Printed-ratio reproduction check (capital ÷ RWA vs printed ratio) for FY2017-FY2026: see §6.

## 5. PROGRESS LOG

- [x] Index fetched, 27 PDF links + 11 HTML popups enumerated, all 200/application-pdf/%PDF
- [x] All 19 editions cover-dated; mapping table above written to disk
- [x] FY2014/FY2015/FY2016 Total RWA question resolved — NOT DISCLOSED, withdraw
- [x] Capital-resource popups checked for an RWA — none present
- [x] Coverage sweep of the 19 editions for currently-blank/undisclosed cells
- [x] Script edited, rebuilt, sheet count confirmed unchanged (18)

## 6. COVERAGE SWEEP RESULTS

The Pillar 3 sheets span `Y_CORE` = FY2026..FY2014 (13 years). Every cell in that window that was
blank or "Not publicly disclosed" was chased back into the editions themselves. **Result: all of
them are genuine, enumerated absences. Nothing new could honestly be filled.**

| sheet | blank/undisclosed cells | chased how | outcome |
|---|---|---|---|
| MREL Ratio | 13 bank-years (all) | full-text search of **all 19 editions** for `MREL`, `minimum requirement for own funds and eligible liabilities`, `loss-absorbing capacity` | 1 hit in 19 documents, and it is the FY2017 leverage narrative's phrase "loss absorbing capacity in times of a stress" — **not** an MREL disclosure. Stays undisclosed; note strengthened to record the search. |
| LCR | FY2014, FY2015, FY2016, FY2017 | full-text search for `LCR`, `liquidity coverage` | FY2014/FY2015: term absent entirely. FY2016/FY2017: exactly one mention each, identical prose — "Additionally, from October 1, 2015 the Bank maintains Liquidity Coverage Ratio (LCR) as stipulated by the PRA" — **with no number attached anywhere in either document**. Stays blank; note strengthened. |
| Leverage Ratio | FY2014, FY2015, FY2016 | full-text search for `leverage` | The word does not appear at all in the FY2014, FY2015 or FY2016 edition. First leverage disclosure is FY2017 §10 ("At March 31, 2017, the Bank's leverage ratio was 13.97%"). Stays blank; note strengthened. |
| Total RWAs | FY2014-FY2016 | see §3 | **Changed from derived-value to blank.** |
| RWA Breakdown — CCR / Securitisation / below-thresholds | FY2014-FY2020 | read the CCR sections of FY2017-FY2020 in full | Those editions print counterparty **exposure** values (e.g. FY2019: gross positive fair value 29.2 + potential credit exposure 30.4 = CCR exposure 59.6 USD million) and a CVA **capital requirement** (FY2019 0.9, FY2020 1.3, FY2021 1.3), but **no CCR risk-weighted amount**. Turning an exposure into an RWA needs risk weights that are not published. Stays blank. |
| NSFR | FY2014-FY2021 | already established 2026-09-15 | Correctly "Not applicable" — the PRA introduced the UK NSFR only from 1 January 2022. Unchanged. |

**Net new cells filled: 0.** Every candidate turned out to be a real absence in the source
documents. The coverage work is therefore recorded as strengthened notes (so the same gaps are
not re-chased by a later session) rather than as new figures.

## 7. CELLS CHANGED (2026-09-16)

| sheet | cells | change |
|---|---|---|
| Total RWAs | FY2014, FY2015, FY2016 | 3,737.5 / 3,685.0 / 4,093.8 **withdrawn -> blank** |
| RWA Breakdown ("Total RWA" TOTAL row) | FY2014, FY2015, FY2016 | same three values **withdrawn -> blank** |

Those are the only value changes. Everything else changed is note/citation text:

- Total RWAs row caption and note fully rewritten: the derivation and its caveat are gone; the
  note now records the withdrawal, the evidence of non-disclosure, the printed Pillar 1
  capital-requirement figures those editions DO give (preserved for traceability, not converted),
  and the fact that the withdrawn values were arithmetically correct but computed.
- RWA Breakdown subtitle rewritten for the same reason, and explains why the FY2014-FY2016
  Credit/Market/Operational component rows are retained (documented uniform unit conversion,
  captioned as such, anchored to specific printed per-risk-type figures, and not presented as a
  headline metric anywhere else) while the Total row is not.
- New `SERIES_VERIFICATION_NOTE`: the 2026-09-16 index re-enumeration, the 27/19 split, the
  live-link verification, the page counts, both cover-vs-filename-vs-index-label disagreements,
  the entity re-confirmation including the FY2024 India hosting-path artefact, and the
  printed-total sanity check.
- New `CAPITAL_RESOURCES_URLS` + `CAPITAL_RESOURCES_NOTE`: the ten previously-unrecorded
  "Composition of Regulatory Capital" HTML disclosures, what they corroborate, and that they
  contain no RWA.
- MREL / Leverage / LCR notes each gained an "enumerated absence" paragraph.
- `BASEL2_NOTE`'s justification for not converting the Basel II credit-risk requirement updated:
  it previously leaned on the FY2014-FY2020 conversion as an accepted precedent, which is no
  longer the case for the Total row.

**No URL was deleted.** Every previously-cited URL is still cited and every one of them was
re-verified live on 2026-09-16, so no archive/fallback URL was needed.

## 8. BASEL II (AND OTHER) FIGURES DELIBERATELY NOT MAPPED

- **FY2008-FY2013 credit-risk-only Pillar 1 capital requirement** (FY2008 335.02 … FY2013 241.69
  USD million). Basel II "Tier 1" is not CET1 and these documents have no capital, ratio, RWA,
  leverage, LCR or NSFR figure at all. Kept in `BASEL2_NOTE`, mapped to no sheet.
- **FY2014-FY2016 Pillar 1 capital requirement by risk type** (Credit / Market / Operational /
  Total). Printed, and now preserved in the Total RWAs note, but **not** converted into an RWA on
  the Total row.
- **FY2017-FY2021 CVA Pillar 1 capital requirement** (0.9 / 1.3 / 1.3 USD million) and the
  **CCR exposure values** (e.g. FY2019 59.6). Exposure and capital-requirement measures, not RWA;
  no honest home on the current sheets.
- **FY2018 Pillar 2A requirement, 3.12% of Total Risk Exposure Amount.** A Pillar 2 add-on, not
  one of the 11 Pillar 3 key metrics; mapping it onto a Pillar 1 capital-ratio sheet would be
  wrong.
- The pre-CRD IV **"Upper tier two" / "Lower tier two"** split in the Composition of Regulatory
  Capital web pages: a different vintage's taxonomy from the CRD IV Tier 2 on the metric sheets.
  Only the totals, which are identical either way, were used as corroboration.

## 9. DOWNSTREAM FLAG (not actioned, per brief)

Withdrawing three Total RWA values will change what `scripts/insights/extract_metrics.py` pulls
into `research/insights.db` for ICICI FY2014-FY2016. `refresh_all.py` was **not** run, the test
suite was **not** run and nothing was committed, per the dispatch brief. Anyone running the next
full refresh should expect ICICI's Total RWA coverage to drop by three bank-years — that is the
intended correction, not a regression.
