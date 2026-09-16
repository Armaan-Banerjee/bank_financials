# RESUME — Entity-basis (group-contamination) sweep (2026-09-16)

Working checkpoint. Updated as each bank is settled. **Written before any repair.**

## Defect class
A parent/group consolidated figure must never enter an entity-level sheet.
Recognised exception: a significant-subsidiaries annex / solo-consolidation
section that names the entity explicitly. A *segmental* figure in a parent's
report is NOT the entity's statutory figure (pre-consolidation-adjustment).

## Scope
10 banks flagged by a peer sweep (24 assertions that Pillar 3 is published at
Group level): secure_trust (9), hsbc_uk_bank_plc (2), hsbc_bank_plc (2),
onesavings (2), shawbrook (2), vanquis (2), clearbank (1), arbuthnot_latham (1).

## Locked — report only, do NOT edit
build_arbuthnot_latham.py (also in RESUME_fx_scale_sweep.md), build_starling.py,
build_reliance_bank.py, build_hodge.py, build_julian_hodge_bank.py,
build_gulf_international_bank_uk.py, build_zenith.py, build_gatehouse.py,
build_lloyds_bank.py, + all of RESUME_fx_scale_sweep.md / RESUME_tieout_sweep.md.

---

## Status board (all 8 settled 2026-09-16)

| Bank | Basis established | Verdict | Repaired? |
|---|---|---|---|
| Secure Trust | Secure Trust Bank Plc + its own subsidiaries; STB PLC is the top of the group | CLEAN (9 false positives) | no change needed |
| HSBC UK Bank plc | HSBC UK Bank plc's OWN Pillar 3; "the group" = HSBC UK, "HSBC Group" = Holdings | CLEAN | no change needed |
| HSBC Bank plc | HSBC Bank plc's OWN Pillar 3 | CLEAN | no change needed |
| Shawbrook | Bank-level tables FY2014-FY2024; FY2025 from the Bank's own ARA | CLEAN | no change needed |
| OneSavings | OSB Group plc consolidated (incl. CCFSL) — declared in-script | DECLARED GROUP BASIS | escalated, not edited |
| Vanquis | Provident Financial plc / Vanquis Banking Group plc consolidated, ALL years | DECLARED GROUP BASIS | note strengthened |
| ClearBank | ClearBank Group Holdings Ltd consolidated (incl. ClearBank Europe N.V.) FY2023+ | MIS-DECLARED basis note | note corrected |
| Arbuthnot Latham | FY2017 statement defect already fixed; Pillar 3 = declared ABG PLC basis | LOCKED — report only | n/a |

### Proof summary (table-level, not cover-level)

- **Secure Trust** — Pillar 3 2017 §1.2: "This document sets out the Pillar 3 disclosures for
  Secure Trust Bank Plc and its subsidiaries (the Group)... The disclosures have been prepared
  for Secure Trust Bank Plc." Group == workbook entity's own consolidation. All 9 hits false.
- **HSBC UK Bank plc** — P3 2024 Presentation of information: "comprises the 2024 Pillar 3
  disclosures for HSBC UK Bank plc ('the bank') and its subsidiaries"; "'HSBC Group'... refer to
  HSBC Holdings plc". Workbook FY2024 CET1 15,059 / T1 17,307 / TC 20,500 / RWA 110,423 /
  CET1 13.6% match its own KM1 (p.5) exactly.
- **HSBC Bank plc** — P3 2021 own document; workbook FY2021 CET1 18,007 / T1 21,869 /
  TC 33,036 / CET1 17.3% and FY2020 18,042 / 22,165 / 33,438 / 14.7% match exactly.
- **Shawbrook** — DECISIVE DIVERGENCE, P3 2024: Group KM1 p.5 = CET1 1,293.1 / T1 1,416.2 /
  TC 1,579.8 / RWA 9,946.6 / T1 ratio 14.2%. Bank KM1 p.16 = 1,297.0 / 1,422.0 / 1,586.2 /
  9,952.2 / 14.3%. Workbook carries the BANK column. Bank-level section present in FY2021
  (Appendix 4), FY2022/FY2023/FY2024 (section 4 "Disclosures for Shawbrook Bank Limited").
  FY2025 contents list has ONE reporting section, "2. Disclosures for Shawbrook Group plc" —
  the Bank-level practice has CEASED. Script already refuses to substitute it.
- **Vanquis** — Provident/VBG P3 editions FY2014-FY2021 read in full: no Vanquis Bank Limited
  solo capital section in any of them. FY2017 §4.5: "The CET1 and total capital ratios... for
  the group are as follows". FY2021 Table 1 / Table 22 = Group. Workbook figures match the
  Group column in every year checked (FY2014 330.0, FY2015 386.0, FY2017 308.1, FY2018 621.9,
  FY2019 697.2, FY2020 674.8, FY2021 506.5).
- **OneSavings** — FY2022/FY2024 P3 Art. 436(h) section: "The Group and its two banking
  entities (OSB and CCFSL) are required to calculate and maintain capital on a consolidated
  basis as well on an individual basis" — the individual figures are NOT published. FY2025
  edition mentions "OneSavings Bank plc" zero times. Workbook FY2021-FY2025 = Group only.
- **ClearBank** — P3 2023 and P3 2025 "Scope of consolidation": the Group = ClearBank Group
  Holdings Limited + ClearBank Limited + ClearBank Europe N.V. (a fully regulated Netherlands
  bank). CBGH got PRA approval as a bank holding company in Q4 2023.

### PART 3 — Vanquis: the premise is DISPROVEN

The quoted FY2021 sentence sits in the **Remuneration Committee** paragraph (AR p.~13) and
its subject is the CRD V **Remuneration Code** annual disclosure statement, not the capital
Pillar 3: "Until 31 December 2019, the Company was required as part of the code to publish an
annual disclosure statement on an individual basis... Following the application of the CRD V
Remuneration Code on the Group on a consolidated basis... As a result, with effect from 31
December 2020 the Company's individual disclosures have been aggregated into the consolidated
Group Pillar 3 disclosures."

Corroborated by Wayback CDX on vanquis.co.uk: every "individual" Pillar III document the Bank
ever self-published is a *Remuneration Code* disclosure (2010, 2011, 2012, 2016, 2017, 2018) —
never a capital/RWA/leverage Pillar 3.

The same AR's risk section gives the real position (p.71): "the Group... is required to make
annual Pillar 3 disclosures... The Group's full Pillar 3 disclosures can be found on the
Group's website."

CONSEQUENCE: there is no FY2020/FY2021 boundary. Vanquis Bank Limited has never published an
entity-level capital Pillar 3 in any year of the window. Also: **build_vanquis.py contains zero
"Not publicly disclosed" cells** (verified by grep), so the instructed re-marking has no target.
Cells moved from "Not publicly disclosed" to "Not applicable": **0**.

---

## Findings log

### Read-of-script (pre-retrieval) signals, 2026-09-16

- **vanquis** — script `metric()` stamps every Pillar 3 sheet subtitle
  "Vanquis Banking Group consolidated basis"; P3 URLs are
  `Provident_Financial_plc_Pillar_3_Disclosures_*` /
  `Vanquis_Banking_Group_plc_Pillar_3_Disclosures_2024`. All 12 Pillar 3 years
  (FY2014-FY2025) are prima facie parent-group basis in an entity workbook
  (Vanquis Bank Limited, CH 02558509). Openly documented in ENTITY_NOTE, but
  documentation is not a cure. NEEDS DOCUMENT CHECK: do the pre-FY2021 Provident
  editions carry a Vanquis Bank Limited solo/individual section?
- **onesavings** — P3 URLs are `osbg-pillar-3-disclosure` / `osb-group-pillar-3`;
  `metric()` stamps "OSB Group consolidated basis". OSB Group plc (CH 11976839)
  is a different legal entity from OneSavings Bank plc (CH 07312896). Same
  prima-facie pattern as Vanquis. NEEDS DOCUMENT CHECK, esp. FY2019/FY2020 where
  the holdco was brand new.
- **shawbrook** — already extensively settled in-script. `ps` sources string
  names Bank-specific tables for every year FY2014-FY2024 and states FY2025
  Group-only data is NOT used (FY2025 comes from Shawbrook Bank Limited's own
  Annual Report and Accounts 2025). Spot-verify FY2024 + FY2025 only.
- **secure_trust** — "Group" here = Secure Trust Bank PLC consolidated; STB PLC
  is itself the LSE-listed parent, so Group == the workbook entity's own
  consolidation. Expect clean; verify no holdco above STB PLC.
- **hsbc_uk_bank_plc / hsbc_bank_plc** — P3 URLs are entity-scoped
  (`/hsbc-uk-bank-plc/`, `/hsbc-bank-plc/`), not HSBC Holdings. Expect clean.
- **clearbank** — "Group basis throughout"; a genuine entity-basis break noted at
  FY2023/FY2024 (ClearBank Group Holdings Ltd, CH 14254435, inserted above
  ClearBank Limited). NEEDS CHECK of what the FY2025 Pillar 3 covers.

---

---

## Repairs made (2026-09-16)

No FIGURE was changed anywhere in this sweep. Every figure checked against a
primary document matched the table it was cited to. Two basis-marking
corrections were made; both workbooks rebuilt, 18 sheets before and after, and
diffed cell-by-cell against git HEAD: **0 numeric diffs**, only source-citation
text cells changed (CLEARBANK 12 text cells, VANQUIS 11 text cells).

1. **build_clearbank.py** — `ENTITY_NOTE` asserted "the Group is essentially the
   Bank plus dormant/minor subsidiaries". FALSE from FY2023: the Pillar 3
   reporting entity became ClearBank Group Holdings Limited (CH 14254435),
   consolidating ClearBank Limited AND ClearBank Europe N.V., a separately and
   fully regulated Netherlands bank. Replaced with a "WHICH GROUP" note quoting
   both Pillar 3 editions' Scope of consolidation, and added a REPORTING ENTITY
   line to `p3_sources()` stating that FY2023-FY2025 are group-basis figures in
   an entity-level workbook and not a like-for-like continuation of
   FY2017-FY2022.
2. **build_vanquis.py** — added a "NO FY2020/FY2021 BOUNDARY" trap note to
   `ENTITY_NOTE` recording the remuneration-disclosure reading of the AR2021
   sentence, the Wayback corroboration, and the fact that no Provident/VBG
   edition FY2014-FY2025 contains a Vanquis Bank Limited solo capital section.

## Open items for a human decision (NOT actioned)

- **Whole-block declared group basis.** Vanquis (11 Pillar 3 sheets x FY2014-
  FY2025) and OneSavings (11 sheets x FY2021-FY2025) are entirely parent-group
  figures. They are correctly and prominently labelled as such in-script, but
  the sweep's rule "do not keep a Group figure because it is the only one
  available" would require withdrawing them. That is a project-wide editorial
  decision with coverage-denominator and insights.db consequences, not a
  transcription fix, so it was escalated rather than executed.
- **OneSavings entity-level LCR is sourceable.** The OSB Group Pillar 3 prints
  an OSB-solo LCR in narrative: FY2020 254.1% ("OSB solo has a Liquidity
  Coverage Ratio (LCR) of 254.1%", p.~13), FY2021 240.1%, FY2022 229% ("As at
  31 December 2022, OSB had a Liquidity Coverage Ratio (LCR) of 229% and CCFSL
  148%"). These are POINT-IN-TIME and must NOT be merged into the Group UK KM1
  12-month-average row (FY2022 197.0%, FY2021 195.5%) - they would need their
  own labelled row.
- **OneSavings FY2019/FY2020 Pillar 3 cells are blank.** The FY2019 document is
  titled "OneSavings Bank plc Pillar 3 Disclosures" and never says "OSB Group",
  but its CET1 of 1,339.6 (2018: 561.6) shows it already consolidates the
  Charter Court combination, so the title is not proof of solo basis. Needs a
  human read before anything is populated.
- **Arbuthnot Latham (LOCKED).** Its own Annual Report publishes Bank-level
  "Group Key Metrics" (FY2024 Tier 1 ratio 13.3%, Total capital ratio 15.4%,
  LCR 179%) which differ from the ABG PLC Pillar 3 figures the workbook uses
  (13.15% / 15.28% / 175%). Under this sweep's rule the entity figures should
  win; the script deliberately chose the parent's formal Pillar 3 instead. File
  is locked - reported, not touched.
