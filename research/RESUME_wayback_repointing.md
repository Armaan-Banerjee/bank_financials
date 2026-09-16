# RESUME — Wayback repointing of dead cited PDF URLs

Started 2026-09-15. Task: for cited PDF URLs a peer session's sweep found DEAD,
keep the dead original recorded and labelled dead (with today's date) and add the
working Wayback replacement alongside. Never delete a dead URL. Always use the
`id_` form (`https://web.archive.org/web/<ts>id_/<original>`), which is a contract
to return the original bytes rather than the Wayback viewer.

Verification standard applied to every fetch: body must begin `%PDF`, page count
must match the expected value, and byte count must not be exactly 1 MiB (the
known truncation failure mode).

Fetch note: web.archive.org returned intermittent HTTP 500/503 ("Internet Archive:
Temporarily Offline") throughout. A retry loop with a browser User-Agent
(`scratchpad/wbfetch.sh`) got every file eventually. **A 500/503 is throttling,
never evidence a capture is absent** — absence is only ever asserted from a
successful CDX query returning `[]`.

---

## 1. ARAB BANK EUROPE — `scripts/build_arab_bank_europe.py` — DONE

Status: **complete**, rebuilt, 18 sheets.

All three URLs were already cited in bare `/web/<ts>/` viewer form; all three were
converted to `id_` form. Fetch verification:

| file | ts | bytes | pages |
|---|---|---|---|
| `202304_EABAnnualReport_v7_144ppi.pdf` | 20240714135652 | 1,951,936 | 98 |
| `202502_EABAnnualReport_v3.pdf` | 20250805183352 | 14,927,337 | 100 |
| `Pillar3.pdf` | 20240714131343 | 3,074,106 | 35 |

### `Pillar3.pdf` — financial year CONFIRMED, ambiguity closed
The undated filename risk (the Metro Bank trap) is now closed on evidence, not
judgement:

- Opened the fetched file. Page 1, verbatim: *"This document comprises EAB Group's
  ("the Group") Pillar 3 disclosures as at 31 DEC 2022."*
- Internal PDF `Title` metadata: `Microsoft Word - Draft Pillar
  3_EAB_consolidated_DEC22_Board approved_final_for publication`.
- **Confirmed edition: FY2022 (as at 31 December 2022), with a 31 December 2021
  comparative.** This matches what the script already asserted.

The newer capture `20250505164839` is **not** a risk after all. The CDX index gives
both captures the identical content digest
`MJ7ZTRM4IN3H5WCITTWXRFZGO2EVRAJL` (both 2,537,938 compressed) — they are
byte-identical, i.e. the same FY2022 edition. The *earlier* capture
`20240713003435` has a different digest (`IFQXMT5C…`, 1,036,749) and is almost
certainly the truncated/corrupt copy earlier sessions kept hitting. Timestamp
`20240714131343` was used as instructed and the confirmed year is now recorded
explicitly in the citation text so this can never recur.

### `Pillar3EAB_PLC_2024.pdf` — real absence, recorded
CDX queried directly and succeeded, returning `[]` for both
`Pillar3EAB_PLC_2024.pdf` and `Pillar3EABplc2023.pdf`. A domain-wide CDX scan of
`eabplc.com` returned a full result set (so the query path works) containing no
2023 or 2024 Pillar 3 file. Recorded in the script as an enumerated absence, not
a fetch failure.

### Deliberately NOT changed
- Domain-wide CDX also surfaced `EAB 2019 Pillar 3.pdf` and `EAB 2020 Pillar 3.pdf`
  under `/files/PDFs/`. Out of scope: this workbook's `YEARS` is FY2021–FY2024 and
  this task is citation repair, not year extension. Flagged only.
- No figure was touched.

---

## 2. FIRSTBANK UK — `scripts/build_firstbank_uk.py` — DONE

Status: **complete**, rebuilt, 18 sheets.

All six Pillar 3 URLs repointed to `id_`-form Wayback snapshots. Dead originals kept
as new `ORIG_P3_*` constants and quoted in a new `P3_DEAD_URL_NOTE`, wired into both
`p3_sources()` (so every Pillar 3 metric sheet carries it) and
`RWA_BREAKDOWN_SOURCES`.

Deadness proven, not assumed: all six live URLs re-fetched 2026-09-16, every one
HTTP **404** with `text/html` (~363KB WordPress not-found page). No 403 anywhere.

| year | ts | bytes | pages | cover says |
|---|---|---|---|---|
| FY2019 | 20200918094410 | 650,322 | 27 | "FBN Bank (UK) Limited … As at 31st December 2019" v2.2 |
| FY2020 | 20231206074745 | 974,989 | 36 | "FBN Bank (UK) Limited … 31st December 2020" v2.0 |
| FY2021 | 20240718195901 | 832,706 | 39 | "FBN Bank (UK) Limited … 31st December 2021" v1.0 |
| FY2022 | 20240219211830 | 785,557 | 39 | "FirstBank UK Limited … 31st December 2022" v1.0 |
| FY2023 | 20240527034030 | 705,562 | 33 | "FirstBank UK Limited … 31st December 2023" v1.0 |
| FY2024 | 20251203042809 | 764,866 | 39 | "FirstBank UK Limited … 31st December 2024" |

Page counts match the brief exactly on all six. **The path trap was handled by
evidence**: five of six sit under `/wp-content/uploads/2019/06/` regardless of
reporting year, so every cover was read rather than inferred — all six matched
their intended year. The covers also independently corroborate the entity rename
already documented in the script (FY2022 is the first edition headed "FirstBank UK
Limited"). No figure changed.

## 3. UNITED TRUST BANK — `scripts/build_united_trust_bank.py` — DONE

Status: **complete**, rebuilt, 18 sheets.

FY2024 repointed to `20250913035253id_` (215,127 bytes, **13pp** as briefed; cover
"UTB Partners Plc / Pillar 3 disclosures / as at 31 December 2024"). Dead original
kept as `ORIG_P3_2024`; new `P3_DEAD_URL_NOTE` wired into `sources()`.

**The brief's premise was too pessimistic — checked rather than assumed.** All six
Pillar 3 URLs were re-tested: FY2024 is the *only* dead one (404). FY2025, FY2023,
FY2022, FY2021 and FY2020 all still return 200 `application/pdf` from the publisher
and were deliberately left cited live — an archive is not substituted for a document
the publisher still serves.

**The 2025 edition is not a gap**: the script already carries FY2025
(`…/uploads/2026/03/…-2025.pdf`, live, 216,894 bytes). Nothing to add.

## 4. TSB — `scripts/build_tsb.py` — DONE

Status: **complete**, rebuilt, 18 sheets.

FY2015 repointed to `20221214093332id_` (440,862 bytes, **37pp** as briefed). Dead
original kept as `ORIG_P3_15_URL`; new `P3_15_DEAD_URL_NOTE` wired into the Pillar 3
sources block. FY2016 (`tsb-material-subsidiary-2016.pdf`) and FY2014 re-checked:
**both live**, left pointing at the publisher.

### Basis — confirmed correct, and sharper than the brief assumed
The brief said Significant Subsidiary Disclosures is the significant-subsidiaries
annex form and IS entity data. Confirmed by reading the document's Introduction —
but with a distinction that matters: the named subsidiary is **TSB Banking GROUP
plc** (the UK consolidated sub-group inside Banco de Sabadell), *not* TSB Bank plc
solo. Verbatim: *"the Pillar III Significant Subsidiary Disclosures at 31 December
2015 relating to TSB Banking Group plc (TSB Group) as part of the Banco de Sabadell
Group … TSB is not required to produce and publish full Pillar III disclosures."*

The script was **already** labelling the sheets exactly that way ("TSB Banking Group
plc consolidated Pillar 3/capital disclosure basis"), consistent with the FY2016 and
FY2019–FY2025 disclosures either side. No relabelling needed.

### Validation gate passed
Recovered document's key metrics reproduce the workbook's FY2015 exactly: CET1
£1.7bn vs £1,672,458k; CET1 ratio 17.8%; Total capital £2.1bn vs £2,055,971k; Total
capital ratio 21.9%; RWAs £9.4bn vs £9,402,364k; total assets £31.6bn vs £31,618.0m.
Same edition, not a restatement. No figure changed.

### One finding worth keeping
The document also discloses a **Basel III leverage ratio of 5.2% (2015) / 5.8%
(2014)** while the Leverage Ratio sheet leaves those years blank. That blank is
**correct, not an unresearched gap**: the sheet's row is "Leverage ratio *excluding
claims on central banks*" (the UK exclusion basis used FY2019+), whereas 5.2% is the
original Basel III measure whose exposure includes central-bank claims — a different
series, not mergeable (same discipline as point-in-time vs 12-month-average LCR).
Recorded in the script note rather than written into the sheet, so it is not
re-chased forever.

## 5. BLOCKED HOSTS (labelled fallback, live URL kept) — DONE

All live URLs re-tested first and confirmed **403 / WAF**, never dead. Live citations
kept as primary everywhere; archives added only as labelled fallbacks.

### Itaú BBA International — `scripts/build_itau_bba_international.py` — rebuilt, 18 sheets
Live URLs 403 (~438–458 byte Cloudflare bodies). The script already had
`*_WAYBACK` constants; upgraded from bare `http://…/web/<ts>/` to
`https://…/web/<ts>id_/`, and added `BLOCKED_HOST_NOTE`. Verified: FY2021
1,803,996 B / **54pp**, FY2022 1,036,900 B / **67pp**, FY2023 1,144,738 B / **62pp**
— all match the brief; covers name "Itau BBA International plc" and the right year;
**final page renders in all three**, so the near-1 MiB FY2022 file is not truncated.

### PNB (Europe) — `scripts/build_philippine_national_bank_europe.py` — rebuilt, 18 sheets
FY2017/FY2019 fallbacks to `id_` form (766,945 B / **13pp**; 454,728 B / **13pp**),
FY2023 also upgraded (441,290 B / 12pp — its filename `Pillar3_Disclosures.pdf` is
undated and was later overwritten by FY2024, so the year is now recorded explicitly).
Added `BLOCKED_HOST_NOTE`.

**FY2019 timestamp changed** from the script's `20200922133733` to the brief's
`20240711230833` — safe: CDX gives both the identical digest
`VKQ52WNFALNSEOZOMIKKAWQ44KFF5FV5` (byte-identical).

**No-fallback cases recorded as unresolved, not negative**: PNB FY2015, FY2016 and
the FY2025 `storage/asset-libraries/` file — CDX returned `[]` for each (archive
absence enumerated), but the live host still 403s, so the *documents* are unexamined,
not absent.

### Starling — `scripts/build_starling.py` — rebuilt, 18 sheets
AR 2019-18: live URL 403 (~49KB bot page); CDX `[]`. Recorded as BLOCKED with no
fallback, left cited live.

### QIB UK — `scripts/build_qib_uk.py` — rebuilt, 18 sheets
ARs FY2017–FY2020. **Trap worth remembering**: these return HTTP **200**, but the
body is a 247-byte "Request Rejected … Your support ID is:" F5 WAF page. A
status-code check reads these as working. CDX `[]` for all four. Recorded as BLOCKED
with no fallback, left cited live.

---

## 6. HODGE (coordinator addition (a)) — CHECKED, DELIBERATELY NOT REPOINTED

Script is `scripts/build_julian_hodge_bank.py`. Rebuilt, 18 sheets (note added only).

**The report that the old Pillar 3s are live again does NOT hold up, and acting on it
would have replaced working citations with broken ones.** Tested URL by URL:

- `/uploads/2021/02/2.-JHB-Pillar-III.pdf` and
  `/uploads/2020/02/Pillar-3-Disclosure-FY19-FINAL.pdf` → HTTP **200 but text/html**,
  108,306 bytes each. **Soft-404s** serving the "Financial Information – Hodge Bank"
  landing page. Proof they are a generic fallback, not documents: the two responses
  are byte-identical, md5 `c69229b0d911df8ea64ada86d57738a2`.
- `/uploads/2019/04/jhb-pillar3-2018.pdf` and all `/uploads/2019/01/jhb-pillar3-YYYY.pdf`
  (2014–2017) → honest 404, 548 bytes.
- The only live Pillar 3 PDFs under `/uploads/2024/07/` are the FY2021–FY2023 files
  **already cited live** in the script (e.g. `Hodge-pillar-3-11.03.24.pdf`, 200,
  application/pdf, 17,008,649 B) — almost certainly what the report conflated with
  the older series.

The existing `id_` citations were re-verified and still return the real documents
(P3_2020 2,416,601 B / 54pp, cover "Hodge Bank / Pillar 3 Disclosures / Period ended
30 September 2020"; P3_2019 695,975 B / 36pp). Left unchanged; a comment now records
the finding so this is not "fixed" wrongly later.

---

## 7. ARAB BANK EUROPE follow-up (coordinator addition (b)) — DONE

Wording only, as instructed. `YEARS` unchanged (FY2021–FY2024), no figures transcribed.

The script's claim "stopped publishing Pillar 3 after the FY2022 edition" was checked
and is **accurate as worded** — and `SDDT_NOTE` already enumerated the 2009–2020
series. What was missing was the *path*, now recorded so a future year extension does
not rediscover it: the 2009–2020 series is under `/files/PDFs/` and
`/files/PDFs/Pillar%203/`, **not** `/downloads/` — which is exactly why permutation
under `/downloads/` kept missing it. Capture timestamps for 2012–2020 recorded
individually. Characterisation sharpened to: published for roughly nine years, then
stopped after FY2022 — not "rarely published".

---

## Standing conclusions worth carrying forward

1. **HTTP 200 does not mean a PDF.** Three separate soft-404/WAF-in-disguise cases
   today (Hodge 200+html, QIB 200+"Request Rejected", plus EAB's 200+homepage already
   on record). Always check `%PDF` and Content-Type.
2. **CDX content digests settle "same edition or not"** far faster than reading two
   PDFs — used for EAB `Pillar3.pdf` and PNB FY2019.
3. **A brief's premise is a hypothesis.** UTB "only 2025 remains" was wrong (only
   FY2024 was dead); Hodge "all live again" was wrong. Re-test before editing.
