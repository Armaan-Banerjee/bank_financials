# Link-rot remediation — peer session `katalysis-d7` findings, batches 2a + 2b

Recorded 2026-09-02, ~22:0x, immediately after three agents died on a session
limit (resets 1am Europe/London). **None of the work below has been applied to
any build script yet.** This file is the only copy.

Peer's verification method, so it does not have to be repeated: each `id_` URL
was downloaded **in full**, one at a time, and required to be `%PDF`, to yield a
`pdfinfo` page count, and to have a size that is **not exactly 1,048,576 bytes**
(the Wayback truncation signature).

> **METHOD NOTE — a `%PDF` check is necessary but NOT sufficient.** It reads
> ~2 KB and cannot see a truncation 1 MiB in. The three rejected rows below
> passed an earlier stage-3 sweep *precisely because* their first bytes are
> `%PDF`. For an archived PDF the real test is **full download + `pdfinfo` page
> count**, with exactly 1,048,576 bytes as the truncation signature. 3 of ~84
> failed this way; all were invisible to the header check.

---

## Why `id_` at all

`https://web.archive.org/web/<ts>id_/<original>` returns the original bytes.
The bare `/web/<ts>/` form returns the Wayback **viewer**, whose output is a
rendering decision the Internet Archive can change under us. Of 99 cited Wayback
URLs, only 19 used `id_`. 84 were candidates for conversion; **81 convert
cleanly, 3 must not.**

Conversion is mechanical: insert `id_` after the 14-digit timestamp, and where a
row is marked `[if_]`, remove the existing `if_`.

---

## DO NOT CONVERT — truncated at exactly 1 MiB

| Script | Timestamp | File |
|---|---|---|
| `build_bank_of_africa_uk.py` | 20220519120942 | `BMCE___Pillar_III_VF___31122017.pdf` |
| `build_gulf_international_bank_uk.py` | 20220518000354 | `2020-GIBUK-Pillar-3_Final.pdf` |
| `build_gulf_international_bank_uk.py` | 20230329132856 | `2021-GIBUK-Pillar-3_Final.pdf` |

**Bank of Africa UK is better solved live** — both its Wayback Pillar 3 citations
can become live URLs. The site moved these from `/assets/<n>/` to
`/pdfs/finances/`. Verified `%PDF`, covers read:

- FY2017 → `https://www.bankofafricaunitedkingdom.co.uk/pdfs/finances/BMCE___Pillar_III_VF___31122017.pdf`
  (32pp, cover "2017 PILLAR III DISCLOSURES", Company Registration No 5321714)
- FY2015 → `https://www.bankofafricaunitedkingdom.co.uk/pdfs/finances/BMCE___Pillar_3_disclosures____2015.pdf`
  (5pp, cover "BMCE BANK INTERNATIONAL plc PILLAR 3 DISCLOSURES FOR THE YEAR 2015", same registration)

The FY2015 row was converting fine; the live URL is simply better than an archive one.

**GIB UK 2020/2021 — SUPERSEDED 2026-09-16, see below.** (Original note: "both
404 live, leave in bare form, the bare form has not been found truncated." The
second clause is disproved.)

### GIB UK FY2020/FY2021 — NO WORKING FORM EXISTS

The peer downloaded **every** playback form of both URLs — bare (the cited
form), `if_` and `id_`. All six return exactly **1,048,576 bytes** and `pdfinfo`
reports no page count. The **capture itself** is truncated at the 1 MiB
boundary, so playback form is irrelevant.

- CDX holds exactly **ONE** 200 capture per URL (the two cited). Every other
  capture of those paths is a 404 — there is no second capture to switch to.
- Live is not an option: `gibam.com` now 404s on the 2020, **2021 and 2022**
  asset paths, has no disclosures index page, and `gibuk.com` does not resolve.
- `gib.com` returns 403 to **both** curl and WebFetch → **BLOCKED, not dead.**
  Not to be written up as a negative.

**Consequence**: FY2020 and FY2021 figures on those sheets cannot be re-verified
from their cited source. Do not convert, but do not leave silently either — the
citation text must say the source is unretrievable and that this was
investigated to exhaustion, so a later pass does not re-chase it or "fix" it.

The FY2022 row is fine: 20240223164517 → `id_`, 33pp.

---

## Credit Suisse year-only timestamps — no action

Both `/web/2024id_/` rows resolve correctly: `csi-pillar-3-disclosures-2021.pdf`
85pp and `-2022.pdf` 71pp, covers "Credit Suisse International / Basel III /
<year> Pillar 3". A pinned 14-digit timestamp would be more stable than a
year-only one, but nothing is broken.

---

## The conversion list (timestamp, original URL, verified page count)

### build_arab_bank_europe.py (1)
- 20240714131343 [bare] `https://www.eabplc.com/downloads/Pillar3.pdf` (35pp)

### build_atom_bank.py (4) — `https://www.atombank.co.uk/~/docs/`
- 20221005205114 [bare] `pillar-3-disclosures-18-19.pdf` (53pp)
- 20221005211108 [bare] `pillar-3-disclosures-17-18.pdf` (52pp)
- 20221005211125 [bare] `pillar-3-disclosures-16-17.pdf` (22pp)
- 20221005223922 [bare] `pillar-3-disclosures-19-20.pdf` (60pp)

### build_bank_of_africa_uk.py (2)
See above — use the live URLs instead.

### build_chetwood.py (7) — `https://chetwood.co/static/<hash>/`
- 20200929085826 [bare] `ea27728be3ae831ddb0ef7888e332546/Pillar3Disclosures.pdf` (23pp)
- 20211128171331 [bare] `221a3946677e4d8c49c5525d22f9b534/Pillar3Disclosures.pdf` (29pp)
- 20230131235943 [bare] `815e2dd174c4655ddf55a93ca1029ce3/Pillar3Disclosures.pdf` (41pp)
- 20240315022245 [bare] `330c40d433df90b83d3b3e5c673e21cc/Pillar3Disclosures.pdf` (34pp)
- 20210830132929 [bare] `3d0ade6e892213e246ca03dc1d84b417/AnnualReport.pdf` (82pp)
- 20230131231341 [bare] `7fbc3d1ed9c0913dca3435f640a5a570/AnnualReport.pdf` (60pp)
- 20240920030034 [bare] `97d26e488d5277699e5b9a9983db4d5b/AnnualReport.pdf` (61pp)

**Chetwood's filenames are undated and repeat across editions**, so the timestamp
is doing all the work. `id_` is worth more than usual on these 7.

### build_credit_suisse_international.py (6, all `[if_]`)
- 20170629113020 `csi-pillar-3-disclosures-2016.pdf` (48pp)
- 20210627075342 `csi-pillar-3-disclosures-2015.pdf` (50pp)
- 20210627075328 `.../regulatory-disclosures-subsidiaries/csi-pillar-3-disclosures-2017.pdf` (74pp)
- 20210627075317 `csi-pillar-3-disclosures-2018.pdf` (78pp)
- 20210627075339 `csi-pillar-3-disclosures-2019.pdf` (84pp)
- 20210627075334 `csi-pillar-3-disclosures-2020.pdf` (84pp)

### build_fce_bank.py (16, all `[bare]`, all `https://www.fcebank.com/pdf/investor_center/`)
- 20211015234304 `2014_Pillar_3_Disclosure.pdf` (37pp)
- 20220615085005 `2011_Annual_FCEReport.pdf` (131pp)
- 20220615085008 `2017_Annual_Report.pdf` (131pp)
- 20220615085018 `2015_annual_report.pdf` (167pp)
- 20220615085021 `2014_annual_accts.pdf` (122pp)
- 20220615085027 `2016_annual_report.pdf` (167pp)
- 20220615085039 `2010_Annual_FCEReport.pdf` (129pp)
- 20220615085046 `2006_Annual_FCEReport.pdf` (100pp)
- 20220615085056 `2009_Annual_FCEReport.pdf` (127pp)
- 20220615085100 `2008_Annual_FCEReport.pdf` (140pp)
- 20220615085110 `2018_Annual_Report.pdf` (149pp)
- 20220615085139 `2013_annual_accts.pdf` (134pp)
- 20220615085141 `2019_Annual_Report.pdf` (167pp)
- 20220615085155 `2007_Annual_FCEReport.pdf` (128pp)
- 20220615085358 `2020_Annual_Report.pdf` (178pp)
- 20220620211159 `2012_annual_report_account.pdf` (133pp)

### build_gulf_international_bank_uk.py (1 of 3)
- 20240223164517 [bare] `https://gibam.com/assets/2022-GIBUK-Pillar-3-disclosures_VF.pdf` (33pp) — converts fine
- 2020 and 2021 rows: **do not convert**, see above.

### build_hampden_co.py (1)
- 20220518033330 [bare] `https://hampdenandco.com/content/hampden/content/Hampden-Co-Pillar-3-disclosures-2020-for-Web.pdf` (37pp)

### build_hsbc_uk_bank_plc.py (2, `[bare]`)
- 20221014171921 `.../2019/annual/pdfs/hsbc-uk-bank-plc/200218-pillar-3-disclosures-31-december-2019.pdf` (46pp)
- 20240527084156 `.../2020/annual/pdfs/hsbc-uk-bank-plc/210223-pillar-3-disclosures-at-31-december-2020.pdf` (57pp)

### build_itau_bba_international.py (3, `[bare]`)
Same captures as the BLOCKED-host fallbacks in batch 2a.
- 20230502062443 `Pillar-3-2021.pdf` (54pp)
- 20230502054346 `Pillar-3-2022.pdf` (67pp)
- 20240812211731 `Pillar-3-2023.pdf` (62pp)

### build_methodist_chapel_aid.py (4, `[bare]`)
- 20200930032441 `pillar3disclosures2019.pdf` (20pp)
- 20210515024743 `pillar3disclosures2020.pdf` (19pp)
- 20220625084136 `2021-pillar-3-disclosures.pdf` (20pp)
- 20250407005711 `media/ngqlqg5o/pillar-3-disclosures-2023.pdf` (22pp)

### build_national_westminster_bank.py (1)
- 20220218072522 [bare] `.../18022022/nwh-pillar-3-supplement-fy-2021.pdf` (144pp)

### build_persia_international_bank.py (2, `[if_]`)
- 20220125010012 `http://www.persiabank.co.uk/Pillar%203%202020%20v7.pdf` (28pp)
- 20260110002617 `http://www.persiabank.co.uk/Pillar%203%202021%20v3.pdf` (28pp)

### build_recognise_bank.py (1)
- 20231210004904 [bare] `.../2023/10/Pillar-3-disclosures-March-2023-RBL.pdf` (7pp)

### build_smbc.py (9, all `[bare]`)
- 20230330205458 `pillar3disclosures310317.pdf` (50pp)
- 20240527065243 `pillar3-31-03-15.pdf` (39pp)
- 20240527070848 `pillar3disclosures310316.pdf` (45pp)
- 20240527071545 `smbce-pillar3-2020.pdf` (60pp)
- 20240527071821 `smbce-pillar3-20180331.pdf` (63pp)
- 20240527071944 `smbce-pillar3-2019.pdf` (66pp)
- 20240612221125 `smbcbi-annual-report-2021.pdf` (144pp)
- 20240701160935 `pillar3-31mar14.pdf` (41pp)
- 20240712094621 `.../Corporate%20Disclosures/smbcbi-pillar3-2022.pdf` (53pp)

### build_union_bancaire_privee_uk.py (2, `[bare]`, kleinworthambros.com)
- 20210918132915 `2019_Pillar_3_Disclosure_KH.pdf` (4pp)
- 20240706060918 `Important_information/2021_KH_Pillar_3_Disclosure.pdf` (3pp)

### build_united_national.py (7, all `[if_]`, ubluk.com)
- 20230923163742 `media/1368/ubl-2022-pillar-3-final-published.pdf` (66pp)
- 20250726151714 `media/pqqda2ng/pillar-iii-disclosure-2021.pdf` (65pp)
- 20250802155220 `media/o0bp44wd/pillar-iii-disclosure-2017.pdf` (62pp)
- 20250803030355 `media/xq1lvuuj/pillar-iii-disclosure-2020.pdf` (64pp)
- 20250804025501 `media/sqgdszjz/pillar-iii-disclosure-2019.pdf` (63pp)
- 20250804031750 `media/5avboizc/pillar-iii-disclosure-2018.pdf` (63pp)
- 20250805064645 `media/sp5brt0v/pillar-iii-disclosure-2016.pdf` (62pp)

### build_unity_trust.py (1)
- 20221124023931 [bare] `https://assets.unity.co.uk/2022/08/PILLAR3-2020-Final.pdf` (22pp)

### build_vanquis.py (6, all `[bare]`, providentfinancial.com)
- 20220703022837 `provident-financial-plc-pillar-3-disclosures-2019.pdf` (34pp)
- 20220703024108 `pfg_pillar_3_report-2017.pdf` (28pp)
- 20220703025345 `2015-pillar-iii-disclosures-april-2015.pdf` (23pp)
- 20220703030203 `22746_pfg_pillar_3_report_2018-2.pdf` (31pp)
- 20220703030607 `Provident_Financial_plc_Pillar_3_Disclosures_2020.pdf` (32pp)
- 20220703055435 `pf-plc-2016-pillar-3-disclosures.pdf` (22pp)

### build_zenith.py (2, `[bare]`, `http://` on both sides)
- 20160826052010 `http://www.zenith-bank.co.uk/uploads/ZBL_Pillar_3_Disclosure_Document_2014.pdf` (19pp)
- 20161128044735 `http://www.zenith-bank.co.uk/uploads/ZBL_Pillar_3_Disclosure_Document_2015.pdf` (18pp)

---

## Batch 2a — replacements for DEAD URLs (not yet applied)

Standing pattern: **keep the dead original recorded and labelled as dead with
today's date, add the working replacement alongside.** Never delete a dead URL —
the provenance chain must stay readable.

### Arab Bank Europe — HIGHEST PRIORITY (had a live disclosure obligation in its gap years; not SDDT-exempt)
- `202304_EABAnnualReport_v7_144ppi.pdf` → `https://web.archive.org/web/20240714135652id_/https://www.eabplc.com/downloads/202304_EABAnnualReport_v7_144ppi.pdf` (98pp)
- `202502_EABAnnualReport_v3.pdf` → `https://web.archive.org/web/20250805183352id_/https://www.eabplc.com/downloads/202502_EABAnnualReport_v3.pdf` (100pp)
- `Pillar3.pdf` → `https://web.archive.org/web/20240714131343id_/https://www.eabplc.com/downloads/Pillar3.pdf` (35pp, 3,074,106 bytes)
- `Pillar3EAB_PLC_2024.pdf` — **no capture** at the exact URL. The CDX query succeeded, so this is a real absence, not throttling.

**Edition worry RESOLVED**: capture 20240714131343 and the newest 20250505164839
are **byte-identical** (same md5, 35pp). But the CDX digest history shows two
genuinely different versions at that URL — 20240713003435 has a different digest
and is ~1 MB against ~2.5 MB — so **keep the 14 July timestamp** rather than
letting anything re-resolve to "newest". `Pillar3.pdf` is an undated filename;
this is the Metro trap.

**EAB published standalone Pillar 3s for 2012–2020**, at a path earlier checks
never probed: `/files/PDFs/` and `/files/PDFs/Pillar 3/`, not `/downloads/`. All
archived as 200 `application/pdf` — e.g. "EAB 2019 Pillar 3.pdf" (20210918015853),
"EAB 2020 Pillar 3.pdf" (20210918020429), "Pillar III Disclosure 2018.pdf"
(20210918014555), "EAB 2016 Pillar 3 - CRDIV_FINAL.pdf" (20220707074618), plus
2012/2013/2014/2015 and a 2009/2010 pair. Does not affect the FY2021–FY2024
workbook, **but the script's "stopped publishing" note is wrong as worded**, and
this matters for any year extension. `arabbankeurope.com` has no archived Pillar 3
captures at all.

### FirstBank UK — all six Pillar 3 URLs dead
All under `https://web.archive.org/web/<ts>id_/https://www.fbnbank.co.uk/wp-content/uploads/`:
- `2019/06/FBNUK-Pillar-3-Dec-19-FINAL-Published_v3.pdf` → 20200918094410 (27pp)
- `2019/06/FBNUK_Pillar-3-Disclosures_2020.pdf` → 20231206074745 (36pp)
- `2019/06/FBNUK-Pillar-3-Disclosures_-2021.pdf` → 20240718195901 (39pp)
- `2019/06/FirstBank-UK-Pillar-3-Dec-2022-V1.0.pdf` → 20240219211830 (39pp)
- `2019/06/FirstBank-UK-Pillar-3-Dec-2023.pdf` → 20240527034030 (33pp)
- `2025/09/FirstBank-UK-Pillar-3-Dec-2024-1.pdf` → 20251203042809 (39pp)

The upload directory is `2019/06` for five of six **regardless of reporting
year** — do not infer year from path.

### United Trust Bank
- `UTB-Partners-Pillar-3-Disclosure-2024.pdf` → `https://web.archive.org/web/20250913035253id_/https://www.utbank.co.uk/wp-content/uploads/2025/03/UTB-Partners-Pillar-3-Disclosure-2024.pdf` (13pp)
- The live site now lists only the 2025 edition. If a 2025 edition exists and the script lacks it, that is an unfilled gap.

### TSB
- `TSB-Significant-Subsidiary-Disclosures-2015.pdf` → `https://web.archive.org/web/20221214093332id_/https://www.tsb.co.uk/investors/results-and-reports/TSB-Significant-Subsidiary-Disclosures-2015.pdf` (37pp)
- 2016 edition is live: `https://www.tsb.co.uk/content/dam/tsb-public/documents/investors/financial-results-and-reports/2016/tsb-material-subsidiary-2016.pdf`
- Document type note: "Significant Subsidiary Disclosures" is the
  significant-subsidiaries annex form, which under this project's entity-basis
  rule **IS** entity data. Confirm the script treats it so and labels the basis.

### BLOCKED hosts — add Wayback as a LABELLED FALLBACK, keep the live URL cited
403/WAF is BLOCKED (unknown), **not** dead. Do not replace the live citation.
- `build_itau_bba_international.py`: 2021 → 20230502062443 (54pp); 2022 → 20230502054346 (67pp); 2023 → 20240812211731 (62pp)
- `build_philippine_national_bank_europe.py`: 2017 → `https://web.archive.org/web/20240712011133id_/https://www.pnb.com.ph/europe/images/stories/docs/Pillar3_Disclosures_for_2017.pdf` (13pp); 2019 → `https://web.archive.org/web/20240711230833id_/https://www.pnb.com.ph/europe/images/stories/docs/Pillar3_Disclosures_for_2019.pdf` (13pp)
- **No capture, remain BLOCKED with no fallback** (an unresolved state, explicitly
  not a negative): PNB 2015, PNB 2016, the PNB `storage/asset-libraries/` file,
  Starling AR 2019-18, QIB UK ARs 2017–2020.

### Hodge
Every old Pillar 3 is **LIVE again** under `hodgebank.co.uk/wp-content/uploads/2024/07/`.

### AIB Group (UK) — an ACCESS REVERSAL
The script says the FY2021 Annual Financial Report "could not be fetched"
(aibgb.co.uk 403s) and falls back on the FY2022 edition's comparative column.
The document is on Companies House, company **NI018800**:
`https://find-and-update.company-information.service.gov.uk/company/NI018800/filing-history/MzMzMjQ0MDUyOWFkaXF6a2N4/document?format=pdf&download=0`
Verified `%PDF`, 168 pages, filed 11 March 2022. **Scanned filing — OCR required,
verify every digit visually.** Tesseract misread digits twice in this project
today ("6 35%" as "6.15%", "156,897,535" as "856,897,535").

Validation gate: current FY2021 values came from the FY2022 comparative column.
If the primary agrees, upgrade the citation. If it disagrees, that is a
restatement — document both on separate labelled rows, do not overwrite.

---

## Melli Bank — what it ever published

**Two Pillar 3 editions survive**, both for the UK entity (Registered number
4152338 — confirms entity basis, not the Iranian parent):
- FY2014: `https://web.archive.org/web/20170407223115id_/http://mellibank.com/PDFs/Melli%20Bank%20P3%20Disclosures%20as%20at%2031%20December%202014%20FINAL.pdf`
  (16pp, cover "Pillar 3 Disclosures / As at 31st December 2014")
- FY2016: `https://web.archive.org/web/20190405190315id_/http://mellibank.com/File/DownloadReportFiles?filename=Melli%20Bank%20-%20Pillar%203%20%20Disclosures%202016%20-%20Final.pdf`
  (23pp, "As at 31st December 2016")
- The FY2014 document is also archived on the old domain `mellibank.co.uk` (20160221234533).

**Directors' report wording, FY2013–FY2025** (OCR'd from all 13 Companies House
annual reports, company 04152338):

| Years | Wording |
|---|---|
| FY2013–FY2015 | "will be posted to the Bank's website, www.mellibank.com" (FY2013 adds "after the agreement of the capital planning buffer with the PRA") |
| FY2016–FY2019 | "have been posted to the Bank's website" |
| FY2020–FY2022 | "available on request from the Bank" |
| **FY2023** | "The Pillar 3 disclosure is available on the Bank's website (www.mellibank.com)" — **reverses to website publication for one year** |
| FY2024–FY2025 | "available on request". FY2025 also records the 29 Sept 2025 sanctions designation. |

**No Pillar 3 later than the FY2016 edition is archived anywhere on
mellibank.com**, despite captures continuing into May 2026 — so this absence is
**evidenced, not a crawl gap**. The `DownloadReportFiles` index holds Annual
Reports 2002–2008 and 2016, plus the FY2016 Pillar 3, and nothing else.
mellibank.com now resolves (62.232.194.164) but times out on both ports,
consistent with the Sept 2025 designation.

**The FY2023 claim is CONTRADICTED, not merely uncorroborated** (sharpened
2026-09-16). The peer read the archived `/reports` page across five captures —
Sept 2021, April 2023, June 2023, June 2025, Feb 2026, May 2026. **Every one**
says: *"Financial Statements and Pillar 3 Disclosures are available on request."*
So throughout the period in which the FY2023 Annual Report claimed the document
was on the website, the website itself said it was available on request. The
tension is between two of the bank's **own** statements — an Annual Report and
its own web page — not between a claim and an archival gap. Record it in those
terms; do not resolve it in either direction.

Other working access routes for Melli, non-obvious and worth not rediscovering:
Companies House (company 04152338) for annual reports, and the **Hong Kong
Monetary Authority public register**, which hosts readable copies —
`https://vpr.hkma.gov.hk/statics/assets/doc/100273/ar_23/ar_23_eng.pdf` (FY2023)
and `.../ar_22/ar_22_eng.pdf` (FY2022).

Consequences to capture in the script:
- FY2013–FY2019 and FY2023: the bank states the documents **were** published.
  Published-then-lost, not never-published — a materially different and stronger
  statement, and the Wayback route above partly redeems it (FY2014, FY2016).
- FY2020–FY2022 and FY2024–FY2025: a **declared non-publication** — the Havin
  shape, a complete answer, not to be re-chased.

---

## Stage-3 priority rows from batch 2a — RESOLVED, no action needed

The 8 rows left hanging by batch 2a failed **only on archive connection
timeouts**, not link rot. Each now has a working `id_` form **at the same
timestamp already cited**, verified by full download with a `pdfinfo` page count:

- `build_fce_bank.py` (4): 20220615085027 `2016_annual_report.pdf` (167pp);
  20220615085039 `2010_Annual_FCEReport.pdf` (129pp); 20220615085046
  `2006_Annual_FCEReport.pdf` (100pp); 20220615085100 `2008_Annual_FCEReport.pdf` (140pp)
- `build_vanquis.py` (1): 20220703024108 `pfg_pillar_3_report-2017.pdf` (28pp)
- `build_smbc.py` (2): 20240527065243 `pillar3-31-03-15.pdf` (39pp);
  20240527071545 `smbce-pillar3-2020.pdf` (60pp)
- `build_united_national.py` (1): 20250804031750 `pillar-iii-disclosure-2018.pdf` (63pp)

**All 8 are already inside the 81-row conversion list above** (FCE 16, SMBC 9,
Vanquis 6, UBL 7), so the conversion agent covers them. Nothing extra to dispatch.

## Still open on the peer's side
- An untruncated capture for GIB UK 2020/2021 — see the superseded-instruction
  section above; current state is **no working form in any variant**.
