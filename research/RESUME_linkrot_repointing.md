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
| 2 | Rathbones | `scripts/build_rathbones.py` | DONE |
| 3 | UBA (UK) | `scripts/build_uba_uk.py` | DONE |
| 4 | Redwood Bank | `scripts/build_redwood_bank.py` | DONE |
| 5 | Alpha Bank London | `scripts/build_alpha_bank_london.py` | DONE |
| 6 | Persia International | `scripts/build_persia_international_bank.py` | DONE |
| 7 | Bank Sepah International | `scripts/build_bank_sepah_international.py` | DONE |

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

---

## 2. RATHBONES — DONE

- **Dead** (HTTP 404, confirmed 2026-09-15):
  `https://www.rathbones.com/sites/rathbones.com/files/results_and_presentations/files/31_december_2024_pillar_3_disclosures.pdf`
- **Replacement** (verified `%PDF`, 49 pp, cover "PILLAR 3 DISCLOSURES / 31 DECEMBER 2024 /
  RATHBONES GROUP PLC"):
  `https://www.rathbones.com/sites/main/files/results_and_presentations/files/31_december_2024_pillar_3_disclosures.pdf`
  Only the one path segment changed: `/sites/rathbones.com/` -> `/sites/main/`.

### Other URLs in the script — none exposed to the same rename
It is the **only** rathbones.com URL in the file. The other five sources are all Companies
House filing-history documents for company 01448919 (AR2021–AR2025). All five re-fetched
2026-09-15: HTTP 200 + `%PDF`. Nothing pre-emptive to fix.

### Figure reproduction — N/A, and this is the important finding
`PILLAR_URL` was **defined at line 12 and never referenced anywhere else in the script.**
It fed no citation. So no figure in the workbook ever came from it, and there is nothing to
reproduce. Its only role is evidentiary: `ENTITY_NOTE` asserts that Rathbones Group Plc's
Pillar 3 is consolidated-only and therefore entity-level Pillar 3 metrics are blank — but
it named the document without printing its URL on any sheet. That claim was effectively
uncited in the delivered workbook.

Fixed: re-pointed the URL **and wired it into `ENTITY_NOTE`**, so the claim now carries its
source. Verified the claim verbatim against the replacement document, p.6 (section 1,
Executive summary): *"Disclosures are made on a consolidated group level, as we have no
large subsidiaries meeting the requirements for individual disclosure under the definition
within CRR Article 4(146)."*

### Entity basis — checked, correct
Workbook entity is **Rathbones Investment Management Limited** (FRN 116316, company
01448919), entity-only accounts under the s.400 exemption. The replacement document is
**Rathbones Group Plc** — the parent. Per the standing rule I checked for a
significant-subsidiaries annex or solo-consolidation section that would legitimately carry
entity data. **There is none.** The one near-miss: the NSFR section (p.25) says Rathbones
"is required to calculate and monitor the ratio on a RIM-solo and group consolidated basis,
reporting the positions quarterly" — but it prints only group figures; UK KM1, UK LIQ1 and
UK LIQ2 are all group-level, and no RIM-solo number appears anywhere in the 49 pages.

So the Group document is cited **only as evidence of absence**. No Group figure sits in any
entity-level sheet. Added an explicit BASIS WARNING to the note saying exactly that, so a
future reader cannot mistake the Group citation for a Group data substitution.

### Deliberately NOT changed
- No figures touched.
- The five Companies House URLs (verified live).

Rebuilt: `python3 scripts/build_rathbones.py` → 18 sheets.

### Library change made here (affects other banks — backward-compatible)
`scripts/bank_workbook.py`: `add_not_disclosed_metric_sheets()` gained an optional
`source_height=150` kwarg, passed through to `add_metric_sheet`. It previously had no way
to set the citation-cell height, and that cell has a **fixed** height and silently clips
overflowing text. Rathbones' now-longer citation needed 430. Default is unchanged (150 =
`_write_source_cell`'s own default), so every existing caller behaves exactly as before.

---

## 3. UBA (UK) — DONE. The brief's diagnosis was wrong; the real cause was different.

The peer reported "the domain moved; the path is unchanged", dead
`ubagroup.com/.../UBA-UK-Ltd-Report-and-Accounts-31-Dec-2018.pdf` -> live
`ubauk.com/.../UBA-UK-Ltd-Report-and-Accounts-31-Dec-2018.pdf`.

**Two corrections to that.**

1. **The URL the peer called dead is not dead.** `ubagroup.com/uk/.../UBA-UK-Ltd-Report-and-
   Accounts-31-Dec-2018.pdf` returns HTTP 200 and a real PDF today. So does the FY2018
   Pillar 3 on ubagroup.com. The legacy host still serves.
2. **The URL actually in the script is a different string**, and it 404s for a **filename**
   reason, not a domain one. The script had `...Report-and-**Accts**-31-Dec-2018.pdf`
   (abbreviated); UBA published `...Report-and-**Accounts**-...` (spelled out). The
   abbreviated name 404s on **both** hosts — genuine 404 bodies (409 and 329 bytes of HTML),
   not soft-404s, not 403/blocks.

### What I changed

| Constant | Was | Now |
|---|---|---|
| `AR2018_URL` | `ubagroup.com/uk/.../UBA-UK-Ltd-Report-and-Accts-31-Dec-2018.pdf` (**404, both hosts**) | `ubauk.com/.../UBA-UK-Ltd-Report-and-Accounts-31-Dec-2018.pdf` |
| `P3_2018_URL` | `ubagroup.com/uk/.../UBA-UK-Pillar-3-Disclosures-31-Dec-2018-3.pdf` (**live**) | `ubauk.com/.../UBA-UK-Pillar-3-Disclosures-31-Dec-2018-3.pdf` |

The P3 move is **pre-emptive**, not a repair — recorded as such, since reporting a live URL
as dead would be wrong. Both dead/legacy strings kept as `AR2018_URL_DEAD` and
`P3_2018_URL_LEGACY`.

**No edition risk at all**, and this is provable rather than assumed: the ubagroup.com and
ubauk.com copies are **byte-identical**.
- AR2018 both hosts: MD5 `7e97b0f5364393ce657b0b796bb170b8`, 956,558 bytes, 52 pp.
- P3 2018 both hosts: MD5 `975b3403146028c16184ca72958332e8`, 363,778 bytes, 19 pp.

Other five URLs (AR2020/2022/2024, P3 2020/2022/2024) already on ubauk.com; all re-fetched
2026-09-15, HTTP 200 + `%PDF`. Nothing else exposed.

### Figure reproduction — ALL FY2018 figures reproduce exactly
Re-read from the recovered documents (both have a real text layer — **no OCR involved**, so
the `156,897,535`/`856,897,535` misread class of error cannot arise here):
- SoFP p.26: total assets $166,173k; equity $44,723k; loans from banks $110,774k; cash
  $25,260k. SoCI p.25: interest income $9,863k; loss after tax $(1,881)k.
- P3 s.3 p.7: TOTAL OWN FUNDS $42,697k. s.3.1 p.8: exposure value of assets $174,209k,
  leverage ratio 24%. s.4.4 p.9: credit $4,021k / market $231k / operational $805k /
  Minimum Capital Resource Requirement $5,057k. Liquidity table: LCR 466%, NSFR 113%.

All match the workbook. (Checked the £ conversion is genuinely applied — it is: the dict
literals are USD and `stock()` converts, e.g. FY2018 total assets $166,173k -> £130,127.6k
at the 1.2770 spot. The `£'000, conv. from USD` column labels are accurate.)

### A DATA GAP THIS CLOSED — not just a citation fix
The script contained this note: *"FY2018: no equivalent breakdown available — the FY2018
Annual Report's own source URL … now 404s and no archived copy could be located."* The
document was never lost; the cited filename was simply wrong. Recovering it recovers the
data. FY2018's Note 5.7.11 'Investment securities' (p.39) **does** disclose the
measurement-basis split, now transcribed onto the four existing sub-rows:

| Row | FY2018 (US$'000) |
|---|---|
| Debt securities at amortised cost (gross) | 34,516 |
| Less: ECL impairment provision | (546) |
| Debt securities at FVOCI (gross) | 27,784 |
| FVTPL / Collective Investment Undertaking | **left blank** — no such line in FY2018 |
| **Total investment securities (disclosed)** | **61,754** |

Foots exactly in USD: 34,516 − 546 + 27,784 = 61,754. Pure transcription, no derivation.
The FVTPL/CIU row is left **blank, not zero** (the BlackRock ICS US Treasury Fund holding
first appears FY2020) per the missing-data rule. FY2017 comparatives in the same note
($13,913k held-to-maturity, $19,955k available-for-sale) are outside the window and not
recorded. The stale "no copy could be located" note is replaced with the real citation.

Also corrected: the note claimed sub-rows "sum EXACTLY" to the total. True in US$; in the
converted £ columns FY2019 and FY2018 miss by £0.1k because each line is rounded
independently at that year's spot rate. That was already true of FY2019 before this change;
the note now says so rather than overclaiming.

### Deliberately NOT changed
- No Pillar 3 or statement figure touched — every FY2018 value reproduced as-is.
- The FY2018–FY2020 derived-RWA methodology (capital requirement ÷ 8%) and the derived
  pre-2021 capital ratios: pre-existing, explicitly documented, outside this task.

Rebuilt: `python3 scripts/build_uba_uk.py` → 18 sheets.

---

## 4. REDWOOD BANK — DONE (already fixed by a peer earlier today; verified, not re-done)

The FY2021 re-point was **already in the script** when I arrived, done by an earlier pass
today: `P3_2021_URL` is the `/media/u5sb3ky5/redwood-pillar-3-2021-1.pdf` replacement and
`P3_2021_OLD_URL` retains the dead `/getmedia/e38875ba-.../2021-Pillar-3_Redwood-Bank.pdf`,
with the reason recorded and printed in the citation. Nothing to repair.

### The brief's expectation did not hold
The brief said "the other 10 Redwood URLs resolve for now, but expect the remaining
`/getmedia/` URLs to die the same way. Check each one; where a `/getmedia/` URL still works,
find and record its `/media/` equivalent."

**There are no remaining `/getmedia/` URLs.** The retired FY2021 path is the only one left in
the file, and it is already dead and already replaced. Every other redwoodbank.co.uk citation
— all seven Pillar 3 PDFs and all four Annual Report PDFs — already uses the current
`/media/<shortid>/` convention. So there is nothing to pre-emptively re-point.

### Full sweep (16 URLs, all checked for `%PDF`, not just HTTP 200)
- 7 Pillar 3 PDFs (FY2017–FY2023): all 200 + `%PDF`.
- 4 Annual Report PDFs (FY2023/FY2024/FY2025): all 200 + `%PDF`.
- 5 Companies House filing-history documents (company 09872265): all 200 + `%PDF`.
- 1 dead `/getmedia/` FY2021 path: confirmed still 404.

### Figure reproduction — FY2021 replacement reproduces exactly
Re-read the `/media/` FY2021 edition (44 pp, cover "REDWOOD BANK LIMITED / PILLAR 3
DISCLOSURES / For the year ended 31 December 2021") to confirm it is the same edition rather
than a revision:
- KM1 Table 1, p.4: CET1 39,399,478; Tier 1 39,399,478; total regulatory capital 49,909,754;
  RWA 233,133,033; CET1 and Tier 1 ratio 16.9%; total capital ratio 21.4%; leverage exposure
  535,602,756; leverage ratio 7.4%; HQLA 111,539,577; net cash outflows 11,495,946; LCR 970.3%.
- Table 7, p.21: institutions 626,025; residential 68,247,424; CRE 137,862,947; past due
  5,461,469; other items 798,294; total credit risk 212,996,159; operational risk 20,136,875;
  Total Pillar 1 RWA 233,133,034.
- Section 8, p.28: NSFR 148.9% (2020: 150.5%).

Every value matches the workbook, **including the documented £1 KM1-vs-Table-7 disagreement**
(233,133,033 vs 233,133,034) and the £2 FY2020 one. No restatement.

### Protected, as instructed — verified still intact after rebuild
- FY2019 Total RWA remains **128,612,638** (not the 114,001,332 credit-risk subtotal).
- The KM1-row-4-is-wrong-in-FY2017/FY2018/FY2019 finding is untouched.

### What I changed
Citation prose only: added an "INDEPENDENT LINK SWEEP 2026-09-15 (third pass)" paragraph
recording the 16-URL check, the fact that no `/getmedia/` exposure remains, and the FY2021
figure-by-figure reproduction. **No URL and no figure changed.**

Rebuilt: `python3 scripts/build_redwood_bank.py` → 18 sheets.

---

## 5. ALPHA BANK LONDON — DONE

**Host behaviour first, because it determines what any result means.** curl gets HTTP 403
from alphabanklondon.co.uk on **every** path, live or not, whatever user-agent/headers are
sent. 403 = BLOCKED, not dead, and carries no information about whether a file exists. All
classifications below were made with WebFetch as the second client.

- **Dead** (WebFetch returns a genuine HTTP 404, not a block):
  `https://alphabanklondon.co.uk/wp-content/uploads/2020/05/ABL-Financial-Statements-2019-1.pdf`
- **Replacement** (verified `%PDF`, 72 pp, cover "ALPHA BANK LONDON LIMITED / Annual Report
  and Financial Statements / 31 December 2019", company 185070):
  `https://www.alphabanklondon.co.uk/sites/default/files/2025-10/ABL%20Financial%20Statements%202019.pdf`
- The FY2020 URL was **left unchanged** as instructed — and independently re-checked via
  WebFetch: real `%PDF`, cover "ALPHA BANK LONDON LIMITED … 31 December 2020". Fine.

Cause: WordPress (`/wp-content/uploads/<y>/<m>/`) -> Drupal (`/sites/default/files/<y>-<m>/`).

### Same orphan trap as Rathbones
`AR19_URL` was **defined and never referenced** — it fed no citation. FY2019 was sourced
only from the FY2020 report's comparative column, and a note in the script treated the
FY2019 report as unobtainable. Re-pointed **and wired into the citations** as FY2019's
standalone primary source.

### Validation gate — PASSED, exactly
FY2019 read directly from its own Note 33.6 "Capital management — Regulatory capital
analysis" (£000's, 2019 with 2018 comparative): share capital 30,000 (30,000); retained
earnings 23,510 (20,915); FVTOCI reserve (59) ((384)); intangible assets (15) ((57)); **Total
Tier 1 capital 53,436** (50,474); subordinated debt 10,000 (10,000); Total Tier 2 10,000
(10,000); **Total regulatory capital 63,436** (60,474). Balance sheet p.~40: total assets
627,764; total liabilities 574,313; total equity 53,451; due to customers 551,341; lease
liabilities 5,444.

Every FY2019 value matches what the workbook already carried from the FY2020 comparative, to
the pound. No restatement, nothing needed dual rows.

### Protected, as instructed — verified intact after rebuild
Total RWAs sheet still reads "Not publicly disclosed" for **all seven years**. The
back-solved figures stay withdrawn.

And the recovered FY2019 document **corroborates** that withdrawal independently: full-text
search for "risk-weighted"/"RWA" returns exactly one hit and it is narrative (the PRA ICG
sentence). No RWA amount is printed, and the "Capital adequacy ratio" KPI does not appear in
the FY2019 report at all — so FY2019 has no denominator either.

### A stale note that could have caused a regression — fixed
`RWA_BREAKDOWN_SOURCES` still read: *"Total RWAs (a single aggregate figure) is calculated on
the Total RWAs sheet from Total Capital ÷ Capital adequacy ratio, per that sheet's own
note."* That describes the **withdrawn** back-solve as if it were live — precisely the text
that would invite someone to reinstate it. Replaced with an explicit "STALE-TEXT CORRECTION …
Do NOT reinstate it" paragraph. No figure changed.

Also recorded in-script, permanently: how this host must be tested (403 ≠ dead), and that the
FY2021 citation's Wayback URL is a **firewall** workaround, not link rot.

Rebuilt: `python3 scripts/build_alpha_bank_london.py` → 18 sheets.

---

## RECONCILIATION AFTER RATE-LIMIT KILL (2026-09-16)

Session was killed by the usage limit; the user had been committing work mid-flight, so
`git status` showed clean for finished work. Re-established state **from the files on disk**,
not from git:

| Bank | Evidence on disk | State |
|---|---|---|
| Shawbrook | all 7 replacement media GUIDs present; `P3_DEAD` + `LINK_PROVENANCE` present | DONE (committed) |
| Rathbones | `sites/main/files` + `PILLAR_URL_DEAD` present | DONE (committed) |
| `bank_workbook.py` | `source_height=150):` kwarg present | DONE (committed) |
| UBA (UK) | `AR2018_URL_DEAD` + `P3_2018_URL_LEGACY` present | DONE (uncommitted) |
| Redwood | "INDEPENDENT LINK SWEEP" present | DONE (uncommitted) |
| Alpha Bank | `AR19_URL_DEAD` + `LINK_PROVENANCE` present | DONE (uncommitted) |

All five rebuilt workbooks confirmed at **18 sheets**. Remaining: Persia, Bank Sepah.

---

## 6. PERSIA INTERNATIONAL — DONE (two conventions fixed, no figure touched)

### (a) The scheme fix — https:// -> http://, with the cause pinned down
`PILLAR3_2021_URL` was `https://www.persiabank.co.uk/Pillar%203%202021%20v3.pdf`.

Diagnosed properly rather than just swapped. `curl -v` shows the TCP connection to
95.215.227.247:443 is **accepted**, then the server **resets during the TLS handshake**:
`Recv failure: Connection reset by peer` at Client hello. No certificate is ever presented,
so no https client of any kind can fetch it — not a user-agent or retry problem. Plain HTTP
serves it perfectly: **HTTP 200, `%PDF`, 1,382,251 bytes, 28 pages.**

Now cited as `http://...`; the failing https form is kept as
`PILLAR3_2021_URL_HTTPS_BROKEN`. Both the constant's comment and the printed citation say
**DO NOT UPGRADE THIS TO https** and why, so a later pass cannot "helpfully" revert it.

**Integrity check:** the live HTTP copy is byte-identical to the Internet Archive capture —
both MD5 `08b8d37ca13c50b214d275062ab119c3`. Same document either way; figures unaffected.

Also re-enumerated the live site over HTTP: it carries exactly **one** Pillar 3 document,
`Pillar 3 2021 v3.pdf`. The script's existing "no later edition" note is accurate.

### (b) Wayback `if_` -> `id_` — applied to FIVE, not two
The coordinator named two (FY2021, FY2020). The script actually had **five** Wayback
citations, all in `if_` form — FY2018, FY2016 and FY2015 too. Converting only two would have
left the same inconsistency behind, so all five were converted after verifying each.

Fetched every one under **both** modifiers:

| Year | Capture | Pages | Bytes | MD5 (`if_` and `id_` identical) |
|---|---|---|---|---|
| FY2021 | 20260110002617 | 28 | 1,382,251 | `08b8d37ca13c50b214d275062ab119c3` |
| FY2020 | 20220125010012 | 28 | 1,109,265 | `1016257632cab1c38991d1bb3dd10606` |
| FY2018 | 20180902131909 | 27 | 936,437 | `f2ba9c655e0d16e9d22889d93f33b6b7` |
| FY2016 | 20161024202355 | 21 | 965,006 | `dfcc56241e21d72f059f5e21e9749c88` |
| FY2015 | 20160316221826 | 18 | 994,951 | `16035cdfe27c311e39daa96e7fde9371` |

**All ten fetches returned HTTP 200 + `%PDF`, and `if_` and `id_` were byte-identical in
every case.** So this repaired nothing and changed no figure — it pins citations to the
canonical raw-bytes form. Recorded as such, honestly, rather than dressed up as a fix.

Two counts corroborate existing notes: FY2015 = 18 pages (the image-only scan the script
describes) and FY2020 = 28 pages (the complete **v7** capture, not the 1 MiB-truncated v6).

**The archived-side `http://` is preserved on all five**, as instructed — it is part of the
archived URL's identity, and rewriting it to https would address a key the Archive may hold
no capture for. Recorded in-script so nobody normalises it later.

### Stale prose that my own change would have made wrong — fixed
The RWA Breakdown citation read *"(original URL: {PILLAR3_2021_URL} — that HTTPS form still
fails the TLS handshake…)"*. Once the constant became the http form, that sentence would have
called an `http://` URL "that HTTPS form". Rewritten to name the live HTTP URL and the broken
https one separately.

### Verified in the built workbook
Zero `if_` strings remain anywhere; all five `id_` captures present; the only surviving
`https://www.persiabank.co.uk` string is the deliberately-retained broken-form record.

### Deliberately NOT changed
No figure, no Companies House URL (10 of them, untouched), no FY2015 credit-subtotal-as-total
caveat.

Rebuilt: `python3 scripts/build_persia_international_bank.py` → 18 sheets.

---

## 7. BANK SEPAH INTERNATIONAL — DONE. **No URL changed**, as instructed.

The certificate really has expired, and the files really are fine.

### Certificate, inspected rather than assumed (`openssl s_client` + `x509`, 2026-09-16)
- Subject: `CN=banksepah.co.uk`
- Issuer: `ZeroSSL RSA Domain Secure Site CA` (C=AT, O=ZeroSSL)
- Valid: **25 Jun 2025 -> 25 Jun 2026** — expired **83 days** before this check
- SANs: `DNS:banksepah.co.uk`, `DNS:www.banksepah.co.uk`

**Expiry is the ONLY defect.** The hostname matches, the root is trusted, it is not
self-signed — it is the right certificate for the right host, merely out of date. So the
documents are genuinely served by the Bank's own domain and remain sound primary sources.

### What the failure actually looks like (the trap this note exists to prevent)
A default curl returns **status `000`** and exits 60 (`SSL certificate problem: certificate
has expired`) — **no HTTP status at all, and specifically not a 404**. A status-code sweep
could easily log that as "dead" and trigger a pointless re-pointing exercise.

### Re-verified all five with validation bypassed (`-k`) — every one healthy
| Document | Bytes | Pages |
|---|---|---|
| Pillar 3 as at 31 March 2025 | 619,903 | 31 |
| Pillar 3 as at 31 March 2024 | 929,132 | 31 |
| Pillar 3 31 March 2023 | 613,571 | 32 |
| Pillar 3 31 March 2022 | 654,861 | 32 |
| Pillar 3 31 March 2021 | 644,221 | 32 |

All HTTP 200 + `%PDF` magic bytes; covers re-read, all headed "BANK SEPAH INTERNATIONAL plc
/ PILLAR 3 DISCLOSURES". The three Companies House URLs are a different host, unaffected,
re-checked the same day (200 + `%PDF`).

### What I changed — citation prose only
Expanded `P3_FETCH_NOTE` into an explicit **"EXPIRED CERTIFICATE — NOT A DEAD LINK. READ
THIS BEFORE 'FIXING' ANY banksepah.co.uk URL"** block carrying the certificate identity,
dates, SANs, the `000`-not-404 warning, the `-k` re-fetch recipe, and the 2026-09-16
sizes/page counts, plus: if the Bank renews, plain HTTPS resumes and nothing here changes.

Also **wired that note into `p3_sources()`**. It previously reached only the Leverage Ratio /
LCR / NSFR sheets; the other Pillar 3 metric sheets and RWA Breakdown carried only a passing
mention. All Pillar 3 sheets now carry the full warning.

Rebuilt: `python3 scripts/build_bank_sepah_international.py` → 18 sheets.

---

# BATCH COMPLETE — all 7 banks

| Bank | URLs re-pointed | Figures reproduced? |
|---|---|---|
| Shawbrook | 7 (FY2014–FY2020 Pillar 3) | Yes, all, exactly. No restatement. |
| Rathbones | 1 (+ wired an orphaned constant into citations) | N/A — fed no figure |
| UBA (UK) | 2 (1 genuinely dead, 1 pre-emptive) | Yes, all, exactly |
| Redwood | 0 — already fixed by a peer; verified | Yes, FY2021 exactly |
| Alpha Bank | 1 (+ wired an orphaned constant into citations) | Yes, exactly |
| Persia | 1 scheme fix + 5 Wayback `if_`->`id_` | Byte-identical (MD5) |
| Bank Sepah | **0 by design** — expired cert, note added | Yes, all 5 docs healthy |

**No figure was overwritten anywhere in this batch.** No validation-gate divergence arose, so
no dual labelled rows were needed. Every dead original is retained and labelled with the date
found dead. All seven workbooks rebuilt at 18 sheets.

Not run, per instructions: `refresh_all.py`, the test suite, any commit.
