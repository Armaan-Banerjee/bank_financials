# Link-rot re-pointing batch — 2026-09-15

Re-pointing citations whose source PDF URLs died, per the peer session's sweep of all
1,134 cited PDF URLs. Standing pattern: **keep the dead original recorded** (labelled as
the dead original, with the date found dead) and add the working replacement alongside.
Never delete a dead URL — the provenance chain must stay readable.

Every replacement is verified by fetching it and confirming `%PDF` magic bytes (NOT merely
HTTP 200 — soft-404s returning 200 with HTML have been hit repeatedly), then reading the
cover to confirm year and entity.

| # | Bank | Script | Status |
|---|------|--------|--------|
| 1 | Shawbrook | `scripts/build_shawbrook.py` | DONE |
| 2 | Rathbones | `scripts/build_rathbones.py` | in progress |
| 3 | UBA (UK) | `scripts/build_uba_uk.py` | pending |
| 4 | Redwood Bank | `scripts/build_redwood_bank.py` | pending |
| 5 | Alpha Bank London | `scripts/build_alpha_bank_london.py` | pending |
| 6 | Persia International | `scripts/build_persia_international_bank.py` | pending |
| 7 | Bank Sepah International | `scripts/build_bank_sepah_international.py` | pending |

---

## 1. SHAWBROOK — DONE

Seven dead Pillar 3 URLs (FY2014–FY2020), all confirmed **HTTP 404** (not 403/blocked, not
soft-404). shawbrook.co.uk relocated investor documents to
`/about-us/investors/results-centre/` and re-issued the Umbraco media GUIDs.

| Year | Dead original (404 as at 2026-09-15) | Replacement (verified %PDF) | pp |
|---|---|---|---|
| FY2014 | `/media/qsxpg41l/shawbrook-pillar-3-disclosures-2014.pdf` | `https://www.shawbrook.co.uk/media/cc5dq5j0/pillar-3-2014.pdf` | 48 |
| FY2015 | `/media/wdvhqxsn/shawbrook-pillar-3-disclosures-2015.pdf` | `https://www.shawbrook.co.uk/media/4galhsik/pillar-3-2015.pdf` | 42 |
| FY2016 | `/media/1lhngswy/shawbrook-pillar-3-disclosures-2016.pdf` | `https://www.shawbrook.co.uk/media/koignkmo/pillar-3-2016.pdf` | 57 |
| FY2017 | `/media/3lifgtxe/shawbrook-pillar-3-disclosures-2017.pdf` | `https://www.shawbrook.co.uk/media/3wefl2tu/pillar-3-2017.pdf` | 55 |
| FY2018 | `/media/kfnfg0oe/shawbrook-pillar-3-disclosures-2018.pdf` | `https://www.shawbrook.co.uk/media/vypjeoat/pillar-3-2018.pdf` | 50 |
| FY2019 | `/media/2azlz2vz/shawbrook-pillar-3-disclosures-2019.pdf` | `https://www.shawbrook.co.uk/media/yhdl0kcs/pillar-3-2019.pdf` | 44 |
| FY2020 | `/media/xexpjjkq/shawbrook-pillar-3-disclosures-2020.pdf` | `https://www.shawbrook.co.uk/media/zlibpqlt/pillar-3-2020.pdf` | 61 |

### (a) Figure reproduction — ALL REPRODUCE EXACTLY. No restatement between editions.

The peer matched replacements on year+entity WITHOUT byte-comparing, so every FY2014–FY2020
figure was re-read from the replacement documents:

- **FY2020 / FY2019** — P3 2020 Appendix 1 "Key risk metrics for Shawbrook Bank Limited"
  (printed p.47): CET1 663.8 / 594.4, T1 788.8 / 719.4, Total capital 883.8 / 814.3,
  RWA 5,268.4 / 4,972.5, ratios 12.6/15.0/16.8 and 12.0/14.5/16.4. LRCom (p.49) leverage
  8.6% / 8.6%. RWA-by-category table (printed p.**50**): credit 4,748.0 / 4,519.0; CVA
  2.6 / 3.8; securitisation 15.9 / –; operational 501.9 / 449.7; totals 5,268.4 / 4,972.5.
  All identical to the workbook.
- **FY2018 / FY2017** — P3 2018 Appendix 1 capital composition (p.33): CET1 514.4 / 431.4,
  T1 639.4 / 556.4, Total 714.4 / 642.4. Bank LRCom leverage 9.2% / 9.5%. All identical.
- **FY2016** — P3 2016 Appendix 1: CET1 367.6, T1 367.6 (no AT1), Total 452.4, leverage
  7.7%. Cross-checked against the FY2016 comparative in P3 2017 Appendix 1 — agrees exactly.
- **FY2015** — P3 2015 Appendix 1 (pp.33–35): CET1 308.6, T1 308.6, Total 388.2, T1 ratio
  14.2%, total capital ratio 17.9%, leverage 6.9%; Pillar 1 credit risk 164.1, operational
  9.8; countercyclical-buffer table "Total risk exposure amount 2,175,860" (= £2,175.9m).
  All identical.
- **FY2014** — P3 2014 Appendix 1 (pp.39–40): CET1 168.4, T1 168.4, Total 202.2, T1 ratio
  11.5%, total capital ratio 13.8%, leverage 6.1%; credit risk 112.4, operational 4.4.
  All identical.

No validation-gate divergence anywhere; nothing needed dual labelled rows.

### (b) ENTITY RISK — CHECKED, NO DEFECT FOUND

All seven covers do read **Shawbrook Group plc**. But every figure the script takes is read
from the Bank-level section, **"Appendix 1: Disclosures for Shawbrook Bank Limited"** — the
Article 13 CRR reduced disclosure of Shawbrook Bank Limited as the Group's significant
subsidiary. Appendix 1 is present in the 2014, 2015, 2016, 2017, 2018 **and 2020** editions
(the peer only spotted 2017/2018). The 2019 edition is the one without a Bank appendix,
which is exactly why the script already sources FY2019 from the FY2020 edition's
comparative column.

Proof the script is on Bank basis, not Group: the 2018 edition prints a **Group** leverage
ratio of 9.2% (2017: **9.4%**) and a **Bank** Appendix 1 leverage of 9.2% (2017: **9.5%**).
The workbook records 9.2% / **9.5%** — the Bank figures. Likewise the 2018 Group key-metrics
table shows RWAs 4,206.8 / 3,361.7 and ratios 15.2/17.0, none of which appear anywhere in
the workbook.

**No Group figure sits in any entity-level sheet.** No defect.

### (c) Things changed beyond the URLs — all prose, no figures

1. Added `P3_DEAD` dict + `LINK_PROVENANCE` block, wired into the Pillar 3 metric-sheet
   citations and the RWA Breakdown citation. Records each dead URL, the date found dead,
   the replacement, the reproduction check and the entity-basis check.
2. **Corrected a stale note that contradicted the data.** The script's note claimed
   "FY2015's derived total (£2,173.8m) is used in preference to the £2,175.9m 'Total risk
   exposure amount'". Backwards: the workbook has always carried **2175.9**, the directly
   disclosed figure. Prose corrected to match the data; **no figure was changed**. FY2014
   (£1,460.0m) really is the one derived value — no directly stated total exists for 2014.
3. Consequence now stated instead of contradicted: FY2015's RWA Breakdown category rows
   (2,051.3 + 122.5 = 2,173.8) fall £2.1m short of the disclosed 2,175.9 total — a rounding
   artefact of grossing £0.1m-precision capital requirements up at 8%. The subtitle
   previously claimed all populated years foot exactly; now excepts FY2015.

### (d) Deliberately NOT changed
- The 12 other Shawbrook URLs (FY2021–FY2025 P3, FY2019–FY2025 AR) — all re-verified live
  and serving `%PDF` on 2026-09-15.
- Minor pre-existing citation-page drift: the RWA-by-category table is on printed p.**50**
  of P3 2020, cited as p.49. Left as found; flagged only.

Rebuilt: `python3 scripts/build_shawbrook.py` → 18 sheets.
