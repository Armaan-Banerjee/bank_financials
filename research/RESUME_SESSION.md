# Session checkpoint — 2026-09-15, ~20:05 (usage limit, resets 8pm Europe/London)

**Read this file first. Then `RESUME_peer_search.md` in this same directory.**

Nothing is committed. 524 files in the working tree. The user has NOT authorised a commit.

---

## 1. Where coverage stands

| | value |
|---|---|
| Pillar 3 coverage, MREL excluded | **86.6%** (6,077 / 7,021) |
| Open cells | **944** |
| Excluded as structurally inapplicable | 79 (inside 5-year windows) |
| Banks | 145 |

Started the day at 79%. Progression: 79 → 81.7 → 83.2 → 83.6 → 85.4 → 86.6.

`refresh_all.py` ran clean and the 47-test suite passed (`Ran 47 tests / OK`) at ~19:50,
AFTER all earlier fork work landed. So the database and deliverable are consistent with
the scripts on disk as of that moment.

Gap register artifact (republished, same URL):
https://claude.ai/code/artifact/20a1ec6e-d815-41f4-ab25-03bc1e707750

---

## 2. TWO DECISIONS WAITING ON THE USER

Do not decide these autonomously. Both were deliberately escalated.

### 2a. Cater Allen — back-solved RWA sheet
`scripts/build_cater_allen.py` has four `RWA_CALC` values that are **capital ÷ CET1 ratio**
(e.g. 217373 / 0.7820 = 277,971). This is the same violation already withdrawn from
**Bank Mandiri** and **Alpha Bank** today. It is flagged in the script but NOT withdrawn,
because removing populated data is the user's call and their Mandiri instruction was
specific to Mandiri.

Recommendation given to the user: withdraw, consistently with the other two. Preserve the
values in the sheet note so the withdrawal stays auditable (see `build_bank_mandiri_europe.py`
for the exact pattern used).

### 2b. DB UK Bank — basis determination
The DBIGB "UK Regulated Group" Pillar 3 is DBUKB's own **PRA consolidation group** —
neither solo nor a plain parent. Figures are transcribed and waiting; **nothing was written
to the workbook**, correctly.

Decisive facts established:
- FY2023 edition, verbatim: *"DBUKB is required by PRA rules … to disclose key prudential
  and remuneration information at the level of their PRA UK consolidation group ("DBIGB
  Group"). DBIGB Group is made up of four companies – DBUKB, DTCL, Deutsche Holdings
  Limited ("DHL") … and DBIGB, a holding company, with DBIGB being the consolidating company."*
- DTCL was sold Nov 2025. **Only the FY2025 edition** adds *"DBUKB is the only operating
  entity in the DBIGB Group."* For FY2022–FY2024, DTCL was a second **trading** subsidiary
  (a UK regulated investment firm). So FY2025 is near-solo; earlier years are not.
- Group CET1 ≠ Company CET1 already in the workbook: FY2025 +0.1%, FY2024 −6.4%,
  FY2023 −9.3%, FY2022 −9.5%. **Ratios cannot be recomputed against the existing CET1 sheet.**
- No DBUKB solo figure appears anywhere in any edition; all templates are DBIGB Group.
- FY2021 unreachable on any basis. The FY2022 URL serves the WRONG FILE (a 21-page Wealth
  Management disclaimer PDF, 436,589 bytes, both live and in the 2026-01-24 Wayback capture).
  FY2022 exists only as the FY2023 edition's comparative column.

Figures that WOULD be written (DBIGB Group basis, £'000 / %):

| | FY2025 | FY2024 | FY2023 | FY2022 |
|---|---|---|---|---|
| CET1 = T1 = Total own funds | 604,018 | 571,967 | 555,107 | 537,779 |
| Total RWA | 710,583 | 595,777 | 510,264 | 681,128 |
| CET1 / T1 / Total capital ratio | 85% | 96% | 109% | 79% |
| Credit risk RWA | 577,952 | 480,687 | 440,893 | 612,901 |
| Counterparty credit risk RWA | 7,208 | 29,497 | 6,053 | 13,533 |
| Market risk RWA | 0 | 0 | 0 | 0 |
| Operational risk RWA | 125,423 | 85,593 | 63,318 | 54,694 |

---

## 3. WORK IN FLIGHT WHEN THE LIMIT HIT

Three agents were dispatched on the peer session's batch-3 URLs and **all three were killed
by the rate limit before writing anything to disk**. Verified: no `build_*.py` was modified
in that window. Their briefs are reproduced below and can be re-dispatched verbatim.
Little was lost — one had "Cynergy verified" in context, another was about to fetch CAF.

### Fork A — Arab Bank Europe, RCI Bank UK, Union Bank of India (UK)

**ARAB BANK EUROPE PLC** (`scripts/build_arab_bank_europe.py`) — renamed from Europe Arab
Bank plc, company no. 5575857; eabplc.com redirects to arabbankeurope.com.
- FY2024 P3: https://www.eabplc.com/downloads/Pillar3EAB_PLC_2024.pdf
- FY2023 P3: https://www.eabplc.com/downloads/Pillar3EABplc2023.pdf
- FY2025 AR: https://arabbankeurope.com/wp-content/uploads/202602_EABAnnualReport_v9.pdf
- FY2022 AR: https://www.eabplc.com/downloads/202304_EABAnnualReport_v7_144ppi.pdf
- **Basis**: both P3s cover "EAB Group" = EAB plc + French subsidiary Europe Arab Bank SA.
  That is the UK entity's OWN consolidated basis, not a parent's, so usable — but confirm
  the scope wording and label the sheets.
- FY2021 not found; try Wayback CDX on `eabplc.com/downloads/Pillar3EAB*`.
- **TRAP**: arabbank.ae hosts "Pillar III Disclosures YE2021" — that is Arab Bank PLC, the
  **Jordanian parent**. Not usable.
- This bank is **NOT SDDT-exempt** — obligation was live in the gap years.

**RCI BANK UK** (`scripts/build_rci_bank_uk.py`)
- FY2024 P3: https://www.rcibank.co.uk/sites/default/files/2025-12/Pillar%20III%20Disclosures%20FY%202024%20-%20External.pdf
- FY2023 P3: https://www.rcibank.co.uk/sites/default/files/2024-11/Pillar%20III%20Disclosures%20FY%202023%20-%20final%20(external%20version)%20signed%201_0.pdf
- **Highest-value item in the batch**: the FY2024 edition reportedly describes itself as the
  SECOND edition, with FY2023 the first. If verified, that converts FY2020–FY2022 from a
  recurring chase into a permanent **sourced negative**. Quote it verbatim with a page ref.
- **TRAP**: the site also hosts "RCI Banque" 2021/2022 reports — French parent group.

**UNION BANK OF INDIA (UK)** (check exact filename: `ls scripts/ | grep -i union`)
- Index (lists P3 FY2015–FY2025, **no FY2026**): https://www.unionbankofindiauk.co.uk/disclosures/financial-reports
- FY2025 P3: https://www.unionbankofindiauk.co.uk/Portals/0/pdf/Final_Pillar_3_Disclosure-31-03-2025.pdf
- FY2026 accounts: https://www.unionbankofindiauk.co.uk/Portals/0/Annual%20Accounts%20UBIUK%202026%20Signed_1.pdf
- Record FY2026 as an enumerated negative, citing the index + date checked, and note it is
  re-checkable (may simply not be published yet).

### Fork B — Cynergy, Hampden, Methodist Chapel Aid

**CYNERGY BANK PLC** (`scripts/build_cynergy_bank.py`) — **largest single haul left, 22 cells**
(Total Capital Ratio, Total RWAs, Leverage Ratio, LCR for FY2023/24/25). Contentful CDN:
- FY2023 P3: https://assets.ctfassets.net/xzmqg68ot16t/5lTzyJuIg2zRrc7GGyH6Gv/c3c522e29325d51066ee937f9989e0be/Cynergy_Bank_Pillar_3_Disclosures_2023.pdf
- FY2022 P3: https://assets.ctfassets.net/xzmqg68ot16t/3qKJzsAiu3dGAA2EQBSzPo/bbb85f662bef802d29fb7144d087c761/cynergy-bank-2022-pillar-3-disclosures.pdf
- FY2021 P3: https://assets.ctfassets.net/xzmqg68ot16t/2v6FmkY7vFJwKVYPsdkTkg/e0dbd1e8afcae76cb6124887a15b196f/cynergy-bank-pillar-3-2021.pdf
- FY2024 AR: https://assets.ctfassets.net/xzmqg68ot16t/2AeSbXsBP7fwKhngGTLWxb/83b43e8ab9ec77bc1ec46f72784e68de/Annual_Report_2024.pdf
- FY2025 AR: https://assets.ctfassets.net/xzmqg68ot16t/rxWLkUeh4mqenjFWMnSmF/20f0dbb97d9496cde7104ad5caa90334/Cynergy_Bank_-_Annual_Report_2025.pdf
- **DO THIS FIRST** — the Pillar 3 links on the index page are JavaScript-rendered, so a
  fetcher sees no href. Curl and grep instead; this enumerates every year Cynergy publishes
  and settles FY2024/FY2025 either way:
  `curl -sL https://www.cynergybank.co.uk/strong-and-prudent-management | grep -o 'assets\.ctfassets\.net[^"'"'"' ]*'`
- **Entity check**: the FY2023 AR is titled "Cynergy Bank **Limited**". Confirm same legal
  entity as the **Plc** in the workbook (company number) before using it.

**HAMPDEN & CO PLC** (`scripts/build_hampden_co.py`) — renamed **Hampden Bank**;
hampdenandco.com redirects to hampdenbank.com.
- Index (ARs 2017–2025, only the 2023 P3): https://www.hampdenbank.com/investors
- FY2023 P3: https://cdn.craft.cloud/019db931-b985-7148-ac09-8f1d1e20d1a6/assets/content/hampden/content/Hampden-Co-plc-2023-Pillar-3-Disclosures.pdf
- FY2022 P3: https://www.hampdenbank.com/content/hampden/content/Hampden-Co-2022-Pillar-3-Disclosures.pdf
- FY2025 AR: https://cdn.craft.cloud/019db931-b985-7148-ac09-8f1d1e20d1a6/assets/content/hampden/content/Hampden_Bank_Annual_Report_2025_2026-06-09-100801_cggc.pdf
- FY2024 AR: same CDN folder, `Hampden-Bank-Annual-Report-and-Financial-Statements-2024.pdf`
- FY2024/FY2025 P3 = enumerated negative per the index. Record the rename so a future pass
  does not search the dead domain.

**METHODIST CHAPEL AID** (`scripts/build_methodist_chapel_aid.py`)
- FY2023 P3: https://www.mcafundingforchurches.co.uk/media/ngqlqg5o/pillar-3-disclosures-2023.pdf
- Uses a **different filename style every year** (`pillar3disclosures2022.pdf`,
  `2021-pillar-3-disclosures.pdf`, now `/media/ngqlqg5o/pillar-3-disclosures-2023.pdf`).
  Permutation cannot find these — use Wayback CDX domain enumeration.
- Its `/about-us/financial-information/` page does NOT link the P3s, so it **cannot** prove absence.
- Do NOT "fix" the documented £48k discrepancy: FY2021 doc totals 26,321; FY2022 doc's Key
  Metrics comparative for the same date says 26,369. Real, and deliberately preserved.

### Fork C — Griffin, Turkish Bank, Oxbury, CAF Bank, StreamBank

**GRIFFIN BANK** (`scripts/build_griffin_bank.py`)
- Index: https://griffin.com/reports — ARs 2023–2025, exactly ONE P3 dated **30 Sept 2023**
- P3: https://cms.griffin.com/griffin-assets/Griffin_Bank_Ltd_Pillar_3_30_Sept_2023_df3ca44acc.pdf
- FY2024 AR: https://cms.griffin.com/griffin-assets/Griffin_Bank_Ltd_Annual_Report_2024_b98c8d4c38.pdf
- FY2025 AR: https://cms.griffin.com/griffin-assets/Griffin_Bank_Ltd_Annual_Report_2025_edeb37eca7.pdf
- Licence restricted Mar 2023, full Mar 2024. Note the **September** date — establish which
  financial year it maps to before transcribing.

**TURKISH BANK (UK)** (`scripts/build_turkish_bank.py`)
- Index: https://www.turkishbank.co.uk/reports/ — ARs 2007–2025, exactly ONE P3
- P3: https://www.turkishbank.co.uk/wp-content/uploads/2026/02/PILLAR-3-DISCLOSURE.pdf
- FY2025 AR: https://www.turkishbank.co.uk/wp-content/uploads/2026/04/Financial-Statements-TBUK-signed.pdf
- **CRITICAL, UNRESOLVED**: that P3 is labelled "2024" but was uploaded **Feb 2026**, and a
  search snippet says it was board-approved in 2025. Establish the real reporting date from
  the document's own content before mapping it to any year.
- Do NOT undo: the FY2022 AR capital note prints retained earnings £8,102k contradicting its
  own audited SOCIE (£8,019k); FY2023 restates to £25,939k. Documented deliberately.

**OXBURY BANK PLC** (`scripts/build_oxbury.py`)
- Index: https://www.oxbury.com/annual-reports/ — accounts 2019–2025, exactly ONE P3
- P3: https://www.oxbury.com/media/xttezclr/oxbury-bank-plc-pillar-3-2023-final.pdf
- Peer confirmed no off-domain copies. FY2021/FY2024/FY2025 = enumerated negative.
- **Oxbury is NOT SDDT-exempt** — its modification is a `Ru 2.1(9)` **eligibility-criterion**
  waiver, not disclosure relief. If the script still claims exemption, correct it.

**CAF BANK** (`scripts/build_caf_bank.py`) — 30 **April** year-ends
- FY2025 sourced negative: https://www.cafonline.org/home/caf-bank/about-us/legal-information/pillar-3-disclosure
  states CAF Bank "is not required to publish a Pillar 3 report" (SDDT, non-listed). Quote verbatim.
- 30 Apr 2024: https://www.cafonline.org/docs/default-source/annual-reports/caf-bank-pillar-3-disclosure-2023_2024.pdf
- 30 Apr 2023: https://www.cafonline.org/docs/default-source/about-us-governance/caf_bank_pillar_ar_2023.pdf
- 30 Apr 2022: https://www.cafonline.org/docs/default-source/about-us-governance/caf_bank_pillar3_2022.pdf
- 30 Apr 2021: https://www.cafonline.org/docs/default-source/about-us-governance/caf_bank_pillar3_2021.pdf
- 30 Apr 2020: https://www.cafonline.org/docs/default-source/about-us-about-caf-bank/cafbank_pillar3_disclosure_2645d_web_230719.pdf
- OCR warning: tesseract previously misread this bank's "6 35%" as "6.15%". Verify digits visually.

**STREAMBANK PLC** (`scripts/build_streambank.py`)
- FY2025 P3: https://streambank.co.uk/pdf/March-2025-Pillar-3-Disclosures.pdf — states
  *"In January 2025, the Bank applied and has since been confirmed as a SDDT regime institution."*
- FY2023 AR: https://streambank.co.uk/pdf/StreamBank-Plc-Financial-Statements-31-March-2023-Signed.pdf
- **UNRESOLVED**: verify that SDDT claim against the PRA waivers register — need the **rule
  number** and its **start date**, and confirm the start date actually covers FY2026.
- Do NOT undo: FY2021 cells were marked "Not applicable" today (no licence until Jun 2022).

---

## 4. Peer session collaboration (`katalysis-d7`)

Address: `uds:/tmp/cc-socks/5809.sock`. Division of labour, deliberate, to avoid concurrent
edits to the same build scripts:
- **Peer does WebSearch discovery and returns URLs only. It edits no repo files.**
- **This session does retrieval, verification and transcription.**

This session's WebSearch is **exhausted (200/200)**, so discovery is entirely the peer's.

Its checkpoint is `research/RESUME_peer_search.md` (15.9 KB, written 20:04) — batch-4 results
for all 7 targets with URLs, years, entity/basis notes, a "searched and found nothing" list,
and batch 2–3 caveats. Headlines from its last message:
- **Nomura — CORRECTED, do not expect ~20 cells.** The NEHS Group Pillar 3 names NBI only
  **up to FY2021**. From FY2022 it **explicitly excludes** it: "Scope of Application" (p.5)
  says NBI, NFPE and the other regulated subsidiaries *"are not considered to be large
  subsidiaries as at 31st March 20YY and are therefore not disclosed in this document"*, and
  the FY2022 edition adds that they *"were previously considered significant subsidiaries and
  previously disclosed"*. Templates cover Group and NIP only. FY2025/FY2026 404 under both
  the `/public/` and `/login/` prefixes, and are not worth a Wayback hunt.
  - **FY2021 edition does carry NBI**, limited to Article 437 own funds: p.7 "CC1: Composition
    of Regulatory Capital" has Group/NIP/NBI/NFPE columns (Mar-21, $m) with CET1, Total
    Capital, CET1 Ratio and Total Capital Ratio rows; footnote 6 states the Tier 1 ratio
    equals the CET1 ratio. p.9 has "LI1: Reconciliation of NBI Own Funds". No NBI RWA,
    leverage or LCR. URL uses the `/login/` prefix: `.../nomura-europe-holdings-plc-annual-pillar-3-disclosures-310321.pdf`
  - **Solo fallback FY2022–FY2026**: NBI's own annual reports (co. no. 1981122), note
    "CAPITAL MANAGEMENT POLICY / UK Regulatory Capital" — note 16 in FY2022/23, note 15 in
    FY2025/26 (p.79 FY2025, p.84 FY2026). Gives **only** "Tier 1 capital" and "Total capital
    resources" ($'000, with prior-year comparative), plus *"The Bank does not currently
    maintain Tier 2 capital"*. FY2026 footnote: *"Tier 1 capital is not subject to audit"*.
    URLs `.../NBI-Annual-Report-3103{22,23,24,25,26}.pdf`
  - **DERIVATION RULING**: do NOT write CET1 = Tier 1 for those years. "No Tier 2" establishes
    Total capital = Tier 1 and may be noted; it does **not** establish CET1 = Tier 1, which
    would additionally require the absence of Additional Tier 1 — stated nowhere. CET1 stays
    blank with a note recording what the documents do and do not say.
  - **Pattern worth reusing**: "was a significant subsidiary, then ceased to be one" explains
    a disclosure series simply stopping. Expect this shape at other group-owned entities.
- **Paragon**: group-consolidated basis only.
- **Recognise**: Pillar 3 only from March 2023.
- Index pages that enumerate their years: ICICI UK (Basel II from FY2007-08), Julian Hodge
  (2010–2023; FY2024/25 absent), Metro (from 2016, 2019 missing), Vanquis (2021+, group basis),
  Zenith UK (2021+).
- **Clydesdale FY2009–13**: sourced parent-basis negative — it relied on NAB's consolidated Pillar 3.
- **Secure Trust — RESOLVED, and a good find.** Annual Pillar 3 exists for **every** year
  FY2015–FY2025 (nothing before FY2015), enumerated from the paginated results index
  (`.../financial-results` with `?start=0/6/12/18/24`). **SLUG TRAP**: 2015–2019 editions end
  in `-annual`, not `-final`, which is why every `-final` permutation 404s. Example:
  `https://www.securetrustbank.com/investor-relations/document-library/pillar-3-disclosure-2019-annual`
  (2018/2017/2016/2015 follow the same pattern; quarterlies are `-q1|q2|q3`). The slugs are
  HTML landing pages with the PDF linked inside.
- **Recognise — enumerated negative FY2018–FY2020.** `recognisebank.co.uk/investors/` lists
  Pillar 3 only for 2023–2026. New FY2026 P3:
  `https://recognisebank.co.uk/wp-content/uploads/Pillar-3-disclosure-March-2026-RBL-v1.1-To-BAC-updated_-1-1.pdf`
- Every batch-4 target now has a status in the peer's file. Remaining open threads there:
  **Nomura FY2022/23/25/26 annual editions**, and **Aldermore FY2011/FY2013**.

---

## 5. Scratchpad tooling

**Now living in `research/coverage_tools/`** (copied out of the session scratchpad and
repointed at repo paths, 2026-09-15 — all three verified running from there). See that
directory's `README.md` for usage and for what counts as a gap.
- `coverage.py` — headline coverage. MREL excluded; spine = years with real Balance Sheet
  data; window = last 5 years desc.
- `by_metric.py` — per-metric bank/year breakdown → `by_metric.json`. Includes an `"ever"`
  field (every year a bank HAS disclosed a metric), which drives the "Disclosed before" filter.
- `gen_page.py` — emits the artifact HTML. **Header stats are hardcoded** — update them
  (currently 944 / 86.6%) whenever republishing.

**Measurement fix made today** (in both `coverage.py` and `by_metric.py`): cells reading
"Not applicable" were being counted as chaseable gaps. They are now excluded from the
denominator entirely rather than counted as filled — counting them either way distorts the
rate. This alone moved the headline 85.4% → 86.2%. Distinguish from "not publicly disclosed",
which IS a real coverage limitation and still counts as a gap.

---

## 6. Standing rules (apply to every agent dispatched on this work)

1. **NEVER fabricate, derive or back-solve.** No RWA from capital ÷ ratio. No ratio from two
   other numbers. Transcribe only what a document states directly.
2. **Entity basis.** A parent/group consolidated figure must never be substituted into an
   entity-level sheet. **Exception**: a group Pillar 3's "significant subsidiaries" annex or
   **solo-consolidation section** naming the entity IS entity data (this unlocked 48 cells
   wrongly blanked for Standard Chartered Bank).
3. **Validation gate.** A new source's prior-year comparative must reproduce the figures
   already in the workbook. If it does not, do NOT overwrite — document both on separate rows.
4. **LCR basis.** UK KM1 = 12-month average; annual reports = point-in-time. Different series;
   never merge into one row. Divergences seen today: 89pp (Shawbrook), 470pp (Redwood FY2021),
   831bp (QIB), 365.6% vs 275.5% (Access Bank FY2023).
5. **SDDT.** Only PRA **Rule 3.1** removes the Pillar 3 duty. **Article 433b** merely reduces
   it; **Ru 2.1(9)** is an eligibility-criterion waiver with no disclosure effect. Conflating
   these caused three separate errors in this project.
6. **NSFR pre-2022 blanks are structural** (PRA PS17/21 — requirement began 1 Jan 2022, and
   the four-quarter-average rule pushes first disclosures to after 1 Jan 2023, so many FY2022
   blanks are structural too, non-December year-ends especially).
7. **"Not applicable" vs empty.** Structurally inapplicable years must be marked explicitly.
   Convention: `build_vida.py` / `build_afin_bank.py` (a `PRE_LICENCE_YEARS` list injected as
   defaults in the local `metric()` wrapper). An empty cell is indistinguishable from an
   unresearched gap and gets re-chased forever.
8. **Overview sheets are copies** — editing a detail sheet does NOT reach them.
9. Read each script from disk immediately before editing (uncommitted changes exist).
10. Rebuild with `python3 scripts/build_<name>.py`, expect 18 sheets.
11. `refresh_all.py` and the test suite are **central-only** — one run after all agents land,
    never per-agent. Tests: `cd scripts/insights && python3 -m unittest test_build_deliverable
    test_extract_metrics` → expect `Ran 47 tests / OK`.
12. **Never commit** unless the user asks.
13. **Dispatch preamble that works.** Forks repeatedly returned orchestrator-voice summaries
    instead of executing (4 instances today, graded not binary — one did nothing, others did
    4/7, 9/13, 1/5). Every redispatch carrying this preamble executed correctly:
    *"EXECUTE THIS YOURSELF. Do not summarise, do not report on other agents' work, do not
    produce a status table, do not delegate onward. Your output is verified against `git diff`
    on the exact file paths named below."* Always verify with `git diff --numstat` + mtimes.
14. **Long tasks must carry checkpoint instructions** — write partial results to disk as you
    go. Today three agents were killed by a rate limit and lost everything in context.

---

## 7. Method notes that earned their keep today

- **Enumeration beats permutation.** Permutation can only fail to find, never prove absence.
  What works: unfiltered Wayback CDX
  (`http://web.archive.org/cdx/search/cdx?url=<domain>&output=json&matchType=domain&collapse=urlkey&limit=5000`),
  WordPress REST media (`/wp-json/wp/v2/media?mime_type=application/pdf&per_page=100`),
  `/sitemap.xml` + child sitemaps, Contentful asset spaces, and scraping real links.
- **A bank's own document index page is worth more than any single PDF hit** — it converts
  "not found" into "enumerated and absent", which is the difference between a gap re-chased
  forever and one that can be closed. Three cases today where an index succeeded exactly
  where permutation could not, all structurally unguessable:
  - **Secure Trust** — the FY2015–FY2019 slugs end in `-annual` while later years end in
    `-final`, so every `-final` variant 404s no matter how many are tried. Only the
    paginated results index revealed it.
  - **Havin** — every page is `document.write()` of a URL-escaped string; decoding it
    exposed a plain document index listing everything the bank has published.
  - **Methodist Chapel Aid** — a different filename style every single year
    (`pillar3disclosures2022.pdf`, `2021-pillar-3-disclosures.pdf`,
    `/media/ngqlqg5o/pillar-3-disclosures-2023.pdf`).
- **Off-domain hosting is the biggest systematic blind spot**: Havin on Squarespace's CDN,
  Castle Trust on a press-release host, NBK International on a sibling bank's Iraqi domain,
  Cynergy and Monument on Contentful, Hampden and Griffin on Craft/CMS CDNs, Brown Shipley
  linked from no page on its own site. **Search the filename and bank name independently of
  the bank's domain.**
- **JavaScript-rendered links defeat fetchers.** Curl + grep the raw HTML instead. Havin's
  whole site is `document.write()` of a URL-escaped string; decoding it exposed the index.
- **Filenames lie — check cover dates and the entity name inside.** Two parent-entity traps
  today: a file named `Pillar III Disclosures 2023.pdf` that is **NBK France SA** in euros,
  and `arabbank.ae`'s YE2021 file which is the **Jordanian parent**. Birmingham's FY2022
  filename now serves the FY2023 document (only Wayback reaches the real one). DB serves a
  Wealth Management disclaimer PDF at its FY2022 Pillar 3 URL.
- **"Already audited" is never a reason to skip re-auditing.** Every re-examination today
  found real data, and several found *wrong* data — worse than absent data. In two of four
  cases the document was already cited in the script and simply had never been opened for
  the metric in question.
- **Watch for "capital cover" ratios** (capital against the capital *requirement*, often
  200–500%) being mistaken for CRR ratios. Caught three times today: Bank Saderat (313–349%),
  Monument (FY2021 529%, FY2020 359%), Alpha Bank (shareholders' funds ÷ RWA).
- Cookie challenges: `curl -c jar -b jar` defeated a host misdiagnosed for months as
  geo-blocking (KEXIM). Soft-404 traps exist — check content, not status code or size.
- Scanned PDFs: `pdftotext -layout` empty → `pdftoppm -png -r 250` → `tesseract`, and
  **verify OCR visually** (misreads today: `6 35%`→`6.15%`, `156,897,535`→`856,897,535`).

---

## 8. Corrections made today that must NOT be re-litigated or undone

- **Redwood** — FY2019 Total RWA corrected 114,001,332 → **128,612,638** (the old value was
  the credit-risk subtotal; an 11% understatement). Redwood's own KM1 row 4 is wrong in its
  FY2017/18/19 editions; its printed ratios prove it (25,830,817 / 128,612,638 = 20.08%).
  Also: Tier 1 Ratio, Total RWAs, Leverage and NSFR had read "Not publicly disclosed" for
  *every* year despite full KM1 tables published since FY2017. FY2018 AR "23.18%" is total
  equity ÷ RWA, not a regulatory ratio.
- **Standard Chartered** — all metrics had been blanked on inverted reasoning; solo
  consolidation IS the entity's own PRA basis. 48 cells restored. FY2024 RWA differs by $8m
  between Table 112 and Table 136 of the same document — documented with a do-not-reconcile
  warning, deliberately not forced to agree.
- **Bank Saderat** — ratio sheets carried "Capital Cover" (313–349%) instead of real CRR
  ratios (86.62% / 90.31% / 83.57%). The 2019 edition computes CET1 on share capital alone;
  the 2020 edition contradicts itself on operational risk (€7,839k vs €8,715k — only the
  latter foots).
- **Monument** — Total Capital Ratio FY2021 529% → **108.99%** (= 32,643,538 / 29,951,235);
  FY2020 359% withdrawn (no P3, no RWA, no licence until Nov 2021). FY2022 onward "TCR"
  reverts to the CRR meaning, so FY2022's 44% was always right. Two divergences kept separate,
  not merged: FY2023 RWAs P3 126,733 vs AR 126,528; FY2023 NSFR P3 237.48% vs AR 228%.
- **Reliance** — FY2026 AR contradicts itself on LCR: Strategic Report p.5 says 228%,
  Liquidity Risk note p.68 says 247%. The note is provably stale. **228% is correct** —
  documented so a future pass does not "fix" it upward.
- **Access Bank / Zenith** — LCR rows silently mixed 12-month average with point-in-time
  (Zenith's Overview duplicated it).
- **FidBank** FY2025 capital ratio 21.46% → **21.99%**. **Gatehouse** note wrongly claimed no
  Tier 2 in any year (£18,939k exists). **Habib Bank Zurich** note wrongly claimed no RWA
  split (FY2022–24 carry one). **HSBC Innovation** source note said FY2024 RWAs 8,276,302 vs
  data 8,276,902 — data right, prose wrong. **Birmingham** ratios 91%/97% → 90%/96%.
- **Withdrawn back-solved RWA**: Bank Mandiri (4 values, user-authorised), Alpha Bank.
  **Cater Allen still pending** — see §2a.
- **Classification overturns**: Griffin (evidence mis-dated five months before opt-in);
  **Arab Bank Europe and Oxbury are NOT SDDT-exempt**; Kingdom Bank's Pillar 3 practice did
  not lapse after 2015.
- **Vida** — basis confirmed correct: VGHL is *"a CRR consolidation entity"* and *"Regulatory
  ratios are presented on a Group-basis only"*; no VBL-solo ratio exists. Sheets already
  carried the basis subtitle. 30 pre-licence cells marked "Not applicable".
- **Perenna and StreamBank** — FY2021 cells marked "Not applicable" (no banking licence:
  Perenna restricted Aug 2022 / full 2023; StreamBank restricted Jun 2022 / full Feb 2023).
  The reasoning was already in their notes but the cells were blank.

---

## 8a. OPEN DEFECT — Zenith 1000x scale error, IN THE LIVE WINDOW

**Every absolute-amount cell on Zenith's Pillar 3 and RWA Breakdown sheets is 1000x too
small for its `£'000` label** — they are effectively £m. Proof from the workbook's own
sheets: Balance Sheet FY2024 Total equity **305,356.2** against CET1 Capital sheet FY2024
**302.3**, both labelled `£'000`.

**Diagnosis (verified 2026-09-15):** `stock()` and `flow()` in `scripts/build_zenith.py`
(lines ~81-88) divide by both the FX rate and 1,000. That is correct for the Balance
Sheet / P&L dicts, which hold **raw USD**. It is wrong for the Pillar 3 dicts, which
already hold **US$'000** — e.g. `CET1_TIER1_TOTAL_USD["FY2024"] = 378325`. Those need
`v / FX_SPOT[y]` with **no** `/1000`.

Ratios are unaffected and every printed ratio still reproduces, which is why this survived
undetected. Unlike the NBE defect below, this one sits **inside the current five-year
window** and reaches the Overview copies and the insights DB.

A dispatched agent entered FY2011 as 43.6/40.0 to match the sheet's existing (wrong) scale
rather than create a mixed-unit defect within one sheet, preserving the true £'000 figures
in the note. **If the scale is fixed, that FY2011 row must be rescaled with everything else.**

---

## 8b. OPEN DEFECT — not fixed, needs its own ticket

**National Bank of Egypt (UK): FY2017 Balance Sheet and P&L column is in £'000 while those
sheets are in £.** Total assets read 1,438,234 for FY2017 alongside 1,212,752,908 for FY2021,
so FY2017 is understated by ~1000x on those sheets and in the Overview copies.

Pre-existing, found 2026-09-15 while filling that bank's Pillar 3 gaps. Deliberately NOT
fixed in that pass because it is outside Pillar 3 scope and the correction touches the charts
and the Overview copies as well as the detail sheets. Worth checking whether any other bank
has the same mixed-units defect before fixing this one in isolation.

---

## 9. Suggested first moves on resume

1. Read `research/RESUME_peer_search.md` for the peer's batch-4 URLs.
2. Put the two decisions in §2 to the user.
3. Re-dispatch Forks A/B/C from §3 verbatim (add the §6.14 checkpoint instruction this time).
4. Highest expected yield: **Cynergy** (22 cells), then **RCI** (converts 3 years to a
   permanent sourced negative), then **Nomura** (20 cells, via the NEHS material-subsidiaries
   section the peer found).
5. After all agents land: one central `refresh_all.py`, then the 47 tests, then recompute
   coverage, update the hardcoded header stats in `gen_page.py`, and republish the artifact
   to the **same URL**.
