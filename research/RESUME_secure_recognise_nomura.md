# RESUME — Secure Trust / Recognise / Nomura Bank International (2026-09-15)

Working checkpoint. Updated after each bank. Retrieval + transcription session.

---

## 1. SECURE TRUST BANK PLC — `scripts/build_secure_trust.py`

### Retrieval
The document-library slugs are NOT HTML landing pages — they 302 straight to the PDF
bytes (`curl -sL` returns `%PDF-1.5`). Slug trap confirmed: FY2015–FY2019 end `-annual`,
FY2020 onward `-final`.

- FY2017: `.../document-library/pillar-3-disclosure-2017-annual` — 37pp, cover
  "Pillar 3 disclosures for the year ended 31 December 2017"
- FY2018: `.../pillar-3-disclosure-2018-annual` — 28pp, y/e 31 Dec 2018
- FY2019: `.../pillar-3-disclosure-2019-annual` — 24pp, y/e 31 Dec 2019
- FY2020: `.../pillar-3-disclosure-2020-final` — 36pp, y/e 31 Dec 2020

All four have readable text layers; no OCR needed.

### Figures transcribed (each year from its OWN edition)

| | FY2020 | FY2019 | FY2018 | FY2017 |
|---|---|---|---|---|
| CET1 capital (£m) | 283.7 | 268.0 | 251.8 | 238.9 |
| Tier 1 capital (£m) | 283.7 | 268.0 | 251.8 | 238.9 |
| Total capital (£m) | 328.8 | 318.0 | 297.5 | 243.3 |
| Total RWA (£m) | 2,001.5 | 2,118.1 | 1,824.6 | 1,446.1 |
| CET1 ratio | 14.2% | 12.7% | 13.8% | 16.5% |
| Tier 1 ratio | 14.2% | 12.7% | 13.8% | 16.5% |
| Total capital ratio | 16.4% | 15.0% | 16.3% | 16.8% |
| Basel III leverage ratio | 10.4% | 9.8% | 10.4% | 12.3% |
| LCR (Basel III KM1) | n/d | n/d | 623.2% | 736.4% |
| NSFR | n/d | n/d | 147.4% | not yet required |

Sources: FY2020 §2 p.4 + §4.4 CC1 row 60 p.13 + App. B LRCom row 22 p.32;
FY2019 §2 p.5 + CC1 row 60 p.7 + LRCom row 22 p.22; FY2018 §2.2 "Key Metrics
(at consolidated group level)" p.4 col a; FY2017 §2.2 p.5 col a.

RWA breakdown (Pillar 1 exposure-class tables):
- FY2020 §4.5 p.14: Credit SA 1,758.1 / CCR 2.6 / Op 240.8 / Total 2,001.5
- FY2019 §4.4 p.10: Credit SA 1,905.0 / CCR 1.7 / Op 211.4 / Total 2,118.1
- FY2018 §2.3 OV1 p.5: Credit 1,653.5 / CCR nil / Op 171.1 / Total 1,824.6
- FY2017 §2.7 OV1 p.7: Credit 1,278.6 / CCR nil / Op 167.5 / Total 1,446.1

### Basis breaks recorded, NOT merged
1. **Leverage ratio.** FY2017–FY2020 are the *Basel III / CRR* leverage ratio
   (denominator includes claims on central banks). FY2021+ already in the workbook is
   the *UK* leverage ratio *excluding* claims on central banks. Different series →
   separate labelled row.
2. **LCR.** FY2017/FY2018 are Basel III KM1 period-end LCRs (736.4% / 623.2%).
   FY2022–FY2025 already in the workbook are UK KM1 **12-month averages**. Separate
   labelled row per standing rule 4.
3. **FY2018 restatement.** The FY2019 Pillar 3 restates its FY2018 comparatives:
   CET1 240.0 (vs 251.8), Total capital 285.7 (vs 297.5), ratios 13.2%/13.2%/15.7%
   (vs 13.8%/13.8%/16.3%), leverage exposure 2,539.0 and leverage ratio 9.5% (vs
   2,432.8 / 10.4%). Total RWA 1,824.6 is unchanged in both. Validation gate →
   FY2018 column keeps AR/P3-2018's own originally-published figures (the convention
   this script already states for the Balance Sheet) and the restatement is documented
   in the source notes rather than overwritten.
4. **FY2019 leverage restatement.** The FY2020 Pillar 3 footnotes FY2019 leverage as
   "Previously disclosed as 9.8%, which has been restated" → 9.7% (exposure 2,772.7
   vs the 2,740.8 in FY2019's own edition). Own-year 9.8% kept; restatement noted.
5. **FY2017 "TRE" footnote.** Both the FY2017 and FY2018 editions state that row 4
   reports Total Risk Exposure ("RWA plus the Operational Risk component") rather than
   RWA. Transcribed as stated; noted.

### Not written, and why
- FY2019/FY2020 LCR and NSFR: those two editions contain no LCR or NSFR figure at all
  (zero hits for "LCR"/"NSFR"/"Liquidity Coverage"/"Net Stable Funding"). FY2020 §10
  cross-refers to AR note 37 instead. No annual-report point-in-time proxy substituted.
- FY2017 NSFR: structurally not required — the FY2018 edition states "The Net Stable
  Funding Ratio (NSFR) is required to be disclosed from 30 June 2018 onwards".
- MREL FY2017–FY2020: no quantitative ratio. All four editions state the Group's TLAC
  equals its Pillar 1+2A capital requirement and that "The Group is not required by the
  PRA to hold a MREL recapitalisation reserve". Recorded as a sourced negative in the
  MREL note.

**STATUS: figures written into `scripts/build_secure_trust.py`; workbook rebuilt.**

---

## 2. RECOGNISE BANK LIMITED — `scripts/build_recognise_bank.py`

**Outcome: zero new figures — correctly so. The value added is turning blanks into a
sourced, dated, explicit negative so the gap stops being re-chased.**

### Enumerated negative (re-verified 2026-09-15)
`https://recognisebank.co.uk/investors/` fetched and its document list read in full.
Pillar 3 offered for **2023, 2024, 2025, 2026 only**; Annual Report & Accounts for
**2022–2026 only**. The page's Pillar 3 PDF hrefs are exactly:
`/wp-content/uploads/2024/03/Pillar-3-disclosures-March-2023-RBL.pdf`,
`.../Pillar-3-disclosure-March-2024-RBL.pdf`, `.../Pillar-3-disclosure-March-2025.pdf`,
`.../Pillar-3-disclosure-March-2026-RBL-v1.1-To-BAC-updated_-1-1.pdf`. Nothing for
FY2018–FY2021.

### FY2026 Pillar 3 checked for backfill — yields nothing
Downloaded (5pp) and read. Table 1 UK KM1 (printed p.4) has five columns, Mar-26 →
Mar-22. Every value matches the workbook already. No MREL row. Does not reach FY2021
or earlier.

### Authorisation date established → "Not applicable" applied
From Recognise's own FY2022 Annual Report (AR22_URL):
- PDF p.23, going-concern note: "After receiving its Authorisation with Restrictions
  (AwR) in November 2020, Recognise Bank became fully authorised in September 2021 and
  was able to accept savings deposits."
- PDF p.45, note 1: "became fully authorised in September 2021 when restrictions set by
  the PRA were lifted after all mobilisation conditions were met".

So FY2018, FY2019, FY2020 (31 March year-ends) are entirely pre-authorisation →
**all 11 Pillar 3 metric sheets + RWA Breakdown now read "Not applicable"** for those
three years, via a `PRE_AUTHORISATION_YEARS` default injected in the local `metric()`
wrapper (build_vida.py / build_afin_bank.py convention).

**FY2021 deliberately NOT marked "Not applicable"** — AwR was already in force at the
31 Mar 2021 year-end, so the Bank *was* a PRA-authorised firm. Its remaining blanks
(Total RWAs, Leverage, LCR, NSFR, MREL) are genuine non-disclosure and must stay
distinguishable from the structural ones.

**STATUS: written and rebuilt — 18 sheets.**

## 3. NOMURA BANK INTERNATIONAL PLC — `scripts/build_nomura_bank_international.py`

**Outcome: zero new figures. The brief's premise ("~20 cells") was wrong, AND the
recoverable cells had already been recovered by a 2026-09-12/15 pass. What was added is
verification, one corrected citation, and the written-down derivation refusal.**

### The FY2022-onward exclusion — verified first-hand, not taken on trust
Documents re-downloaded and re-read on 2026-09-15:
- **31 Mar 2022** (91pp): Scope of Application, PDF p.6 — "NBI and NFPE were previously
  considered 'significant subsidiaries' and previously disclosed. However, along with
  the other regulated subsidiaries, they are not considered to be large subsidiaries as
  at 31st March 2022 and are therefore not disclosed in this document." CC1 headed
  "Composition of regulatory own funds for **the Group and NIP**" (PDF p.13).
- **31 Mar 2024** (120pp) — *this was the peer's open question, now closed*: PDF p.6 —
  "Other regulated subsidiaries included in the Group are Nomura Bank International Plc
  ('NBI'), … They are not considered to be large subsidiaries as at 31st March 2024 and
  are therefore not disclosed in this document." CC1 likewise Group + NIP only (PDF p.16).
- **FY2025 / FY2026**: `...-310325.pdf` and `...-310326.pdf` return **404 under both**
  `/portal/site/public/` and `/portal/site/login/` (all four combinations tested). No
  group document exists to exclude NBI from.

So: FY2022–FY2024 = sourced structural negative; FY2025–FY2026 = enumerated negative.

### FY2021 CC1 — verified, and one citation corrected
NEHS 31 Mar 2021 edition, CC1 "Composition of Regulatory Capital", NBI column, at
**printed p.7 / PDF p.11 of 76** — the script had cited "p.16", now corrected (figures
unaffected). NBI column reads: CET1 267, Total Capital 267, CET1 Ratio 279.68%, Total
Capital as % of total Risk Exposure amounts 279.68%, Tier 2 "-" ($m). Footnote 6: "Tier 1
capital ratio is equal to the Common Equity Tier 1 ratio". Scope of Application p.1:
"NBI is a United Kingdom ('UK') regulated bank but its Risk Weighted Assets ('RWA') are
immaterial to the Group. Therefore NBI disclosures have been made for article 437 (Own
Funds) with no other disclosures relevant to significant subsidiary requirements."
All of this matches what the script already held.

### Annual-report Tier 1 / Total capital — full comparative chain re-verified
"UK Regulatory Capital" table in the Capital Management Policy note (note 16 in FY2022/23,
note 15 from FY2024). AR2022 p.89: 287,698 (2021 comp. 276,772). AR2023 p.86: 280,841
(287,698). AR2024 p.86: 281,296 (280,841). AR2025 p.80: 281,414 (281,296). AR2026 p.85:
281,438 (281,414). Every comparative reproduces the prior edition exactly — validation
gate passes on all five links, no restatement. AR2026 footnote: "Tier 1 capital is not
subject to audit." No CET1 line, no ratio, no RWA in any year.

### Deliberately NOT written
- **CET1 for FY2022–FY2026.** "The Bank does not currently maintain Tier 2 capital"
  establishes Total capital = Tier 1 (which is why the Total Capital sheet carries the
  same figures). It does NOT establish CET1 = Tier 1: that needs the absence of AT1,
  which no document states. Corroborating evidence that the two genuinely differ for this
  entity — at 31 Mar 2021, CC1 CET1 $267m vs the accounts note's Tier 1 $276,772k, a
  $9.8m prudential-filter gap. Refusal written into the CET1 sheet's note.
- **FY2021 RWA (~$95m).** Back-solvable from $267m at 279.68%; the script already refuses
  it explicitly and that refusal is left standing.

**STATUS: script updated and rebuilt — 19 sheets (standard 18 + this bank's pre-existing
Interim Pillar 3).**
