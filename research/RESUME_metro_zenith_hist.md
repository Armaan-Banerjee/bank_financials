# RESUME — Metro Bank & Zenith Bank (UK) historical Pillar 3 transcription

Started 2026-09-15. Task: transcribe Wayback-recovered historical Pillar 3 editions
into `scripts/build_metro_bank.py` and `scripts/build_zenith.py`.

Rules in force: no fabrication/derivation/back-solving; Basel II figures must be
labelled as such and never continued into a CRR series; NSFR pre-2022 = "Not applicable";
prior-year comparatives validated against existing workbook values, divergences
documented on both rows, never silently overwritten; Overview sheets are copies.

## STATUS

- [x] Metro Bank — 4 documents downloaded, all text-extractable, cover dates confirmed
- [x] Metro Bank — transcribed
- [x] Metro Bank — rebuilt (19 sheets: the standard 18 + the pre-existing "Interim Pillar 3")

### Metro — what was written
- `PILLAR3_YEARS` un-pinned from FY2014-FY2025 to the full FY2010-FY2025 `YEARS` range.
- New `P3_{2010,2011,2013,2014}_HIST` timestamped Wayback URL constants + `HIST_P3_NOTE`
  (appended to `P3_SOURCES` and to the Asset Quality source cell).
- Tier 1 Capital / Total Capital: **new second row** carrying Basel II GENPRU capital
  (387.3 / 381.5 / FY2012 marker / 69.1 / 89.8). CRR row untouched — FY2014's 384 kept.
- Total RWAs: **new second row** carrying Basel II credit-risk-only RWA
  (1415.9 / 775.3 / marker / 93.2 / 19.0); CRR row FY2010-FY2014 set to
  "Not publicly disclosed" (was blank for FY2014).
- CET1 Capital, CET1 Ratio, Leverage, LCR, NSFR, MREL: FY2010-FY2013 explicit markers.
- Tier 1 Ratio, Total Capital Ratio: FY2010/11/13 "Not publicly disclosed" + FY2012 marker.
- RWA Breakdown: new labelled SECTION with 13 Basel II exposure-class rows + total.
- Asset Quality: new labelled SECTION with the incurred-loss provision + past-due rows.
- ENTITY_NOTE expanded with the LI3 evidence; Overview note records that nothing from
  the Basel II editions reaches the Overview (by design — they disclose no ratios).
- [ ] Zenith — documents downloaded
- [ ] Zenith — transcribed
- [ ] Zenith — rebuilt

Docs at: /private/tmp/claude-501/-Users-armaan-code-katalysis/20f20984-c24d-413e-b487-68c0d0793341/scratchpad/docs

## METRO — FINDINGS (all four docs read end to end)

Cover dates confirmed individually. FY2013 and FY2014 share the original URL but their
covers read "31st December 2013" (20 pages) and "31st December 2014" (21 pages) — the
shared-URL trap is resolved. ALWAYS cite the full timestamped Wayback URL.

All four are **Basel II** documents. NONE of them contains the strings leverage, LCR,
NSFR, MREL, CET1, Common Equity or Tier 2 (grep verified, zero hits in all four).
Each discloses exactly: (a) a Tier 1 / Total Regulatory Capital table, (b) a credit-risk
exposure table with an RWA column, (c) a one-line doubtful-debt provision. No capital
ratio is stated in any of the four. Operational risk uses the Basic Indicator Approach
(FY2011 onward) and is never quantified, so no total RWA exists in any edition.

Entity: FY2010 "The bank has no subsidiaries or joint ventures"; FY2013/FY2014 "a single
subsidiary, SME Invoice Finance (SMEIF), acquired in August 2013".

### Figures (source £'000; workbook sheets are £m)

| | FY2010 | FY2011 | FY2013 | FY2014 |
|---|---|---|---|---|
| Total Regulatory Capital (= Tier 1) | 89,811 | 69,090 | 381,530 | 387,261 |
| narrative text says | £89.8m | £69.090m | £382m | £388m |
| Share capital/premium line | 0 / 120,131 | 120,131 | 531,011 | 629,304 |
| Profit and loss reserve | -23,341 | -42,179 | -118,608 | -157,549 |
| Other Reserves | — | — | -7,520 | -4,314 |
| Intangible assets (and reserves) | -6,979 | -8,862 | -23,353 | -80,810 |
| Credit-risk RWA | 18,950 | 93,152 | 775,310 | 1,415,881 |
| Credit-risk exposure total | 119,117 | (n/d) | 2,076,992 | 3,896,820 |
| Doubtful debt provision | nil (explicit) | £186k | £1.09m | £3.5m |
| Past due >20% impaired secured | — | — | 1,093.08 | 2,165 |

RWA caption: FY2010 sits on the "Total assets" row; FY2011/FY2013 captioned "TOTAL Risk
Weighted Assets"; FY2014 captioned "TOTAL". All are credit-risk-only tables.

### Divergences to document (NOT overwrite)
1. **FY2014 capital**: workbook holds 384 (AR2015 Capital management note). FY2014
   Pillar 3 states 387,261 / "£388m". £3.3m apart, different sources/bases.
2. **FY2014 P3 table does not foot**: 629,304 - 157,549 - 4,314 - 80,810 = 386,631 but
   the stated total is 387,261. £630k unexplained *inside the source document*.
3. **FY2014 P&L reserve** -157,549 (contemporaneous) vs workbook -164 (AR2015 *restated*
   comparative). Corroborates the restatement flag already in the script.
4. **FY2013 share capital line** 531,011 vs workbook share premium 530.5.
5. **FY2011 P&L reserve** -42,179 vs workbook retained earnings -42.3.

### FY2012 — CLOSED, genuinely absent (per peer: CDX prefix scan + name search negative)

### ENTITY FINDING (asked for explicitly)
Boundary is exactly FY2022 → FY2023, matching the 19 May 2023 holding-company insertion
already in ENTITY_NOTE. Evidence gathered fresh this session:
- FY2010/11/13/14 covers: "METRO BANK PLC"
- FY2021 exec summary: "Metro Bank PLC's (Metro Bank or the Bank) 2021 Annual Report"
- FY2022 page header: "Metro Bank PLC Pillar 3 2022"
- FY2023 cover + every page header: "Metro Bank Holdings PLC | Pillar 3 2023"
- FY2023 §1: "In May 2023, Metro Bank completed the implementation of its holding company"
- FY2023 Table 3 UK LI3 names the consolidation group entity by entity: Metro Bank
  Holdings PLC (holding company), Metro Bank PLC (banking), RDM Factors Limited (dormant),
  SME Invoice Finance Limited, SME Asset Finance Limited — all full consolidation.
So FY2023-FY2025 ARE a holding-company basis. Already labelled on the sheets; this
session adds the LI3 evidence to the note.

All 10 live Metro Pillar 3 URLs in the script re-checked 2026-09-15: all HTTP 200.

### INCIDENTAL FINDING, not in brief (see report)
FY2023 Pillar 3 §1 states MREL ratios of **22.0% (Dec 2023)** and **17.7% (Dec 2022)**
directly, and the doc has a "Table 5 UK KM2 Key metrics – MREL". The workbook's MREL
sheet currently says "Not disclosed" for FY2022-FY2025.

## LOG
- 21:16 downloaded 4 Metro PDFs
- 21:30 all four read; figures tabulated above
