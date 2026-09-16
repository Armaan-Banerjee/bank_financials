# `km1_inventory.jsonl` — what it is, and what it is not

One JSON object per cited Pillar 3 PDF URL: **does this document print a KM1, which rows, and which
columns.** It is a *finding aid*, not a transcription. No figure from any table is recorded,
deliberately.

**Transcribe from the PDF, never from this file.** Every field below is a locator or a floor.

Built 2026-09-16 by the survey session (`katalysis-d7`). 785 rows, one per distinct URL, across
**114 banks**. 740 rows carry the current detector version; 45 are carried forward (see §5).

## 1. How a document got here

`research/cited_urls_v2.tsv`, filtered to `is_pdf == "pdf"` and a Pillar 3 URL pattern after
**double `unquote()`** (a single pass leaves `Pillar%25203`; not decoding at all missed 8 banks whose
filenames spell the space `%20`). Each PDF is fetched once into a content-addressed cache and read
with `pdftotext` in **both** `-layout` and raw reading-order modes, unioned — Crown Agents' rows
appear only in raw, and Secure Trust's `UK 11a` survives only the union.

## 2. Headline numbers

| verdict | n |
|---|---|
| `KM1_PRESENT` | 335 |
| `NO_KM1_FOUND` | 317 |
| `KM1_PRESENT_NO_TEXT_LAYER` | 1 |
| `UNFETCHED` | 45 |
| `KM1_CANDIDATE_UNLOCATED` | 42 |
| `KM1_CANDIDATE_BANK_STYLED` | 37 |
| `NO_TEXT_LAYER` | 8 |

`KM1_PRESENT` by template: **UK_KM1 254, UNPREFIXED_NUMBERED 79, EU_KM1 2.**

**Denominator, stated honestly: 732 readable documents** (785 less 8 `NO_TEXT_LAYER` and 45
`UNFETCHED`). 335 of 732 = **46%** print a KM1. Column headers captured for **311 of 335 (93%)**.
`entity_row` populated on **25** documents. Restatement asterisks on **22**. Zero/dash glyphs
recorded on **394**.

**86 of 114 banks** have at least one `KM1_PRESENT` edition. 28 do not — see §6, which is the part
most likely to be misread.

## 3. Verdict vocabulary

| verdict | meaning |
|---|---|
| `KM1_PRESENT` + `UK_KM1` | ≥3 letter-suffixed UK KM1 row tokens (`UK 7a`, `UK 16b`). The strong test. |
| `KM1_PRESENT` + `EU_KM1` | same, EU-prefixed. |
| `KM1_PRESENT` + `UNPREFIXED_NUMBERED` | Basel/EU-era bare numbering: ≥8 KM1 row numbers **and** a locatable table. |
| `KM1_CANDIDATE_UNLOCATED` | bare-numbered signal present but **no KM1 table could be located**. Weakest basis; confirm by eye. |
| `KM1_CANDIDATE_BANK_STYLED` | ≥6 KM1 label families, no template numbering: a bank's own key-metrics table, or narrative. |
| `NO_KM1_FOUND` | no KM1 signal. Expected pre-2021 (see §4). |
| `NO_TEXT_LAYER` | scanned image. **Says nothing about whether a KM1 exists — excluded from every denominator.** |
| `UNFETCHED` | never retrieved. Not evidence about the document. See §5. |
| `KM1_PRESENT_NO_TEXT_LAYER` + `IMAGE_ONLY` | **Added 2026-09-16 by KM1-003, and not produced by the detector.** The document prints the template but the TABLE ITSELF is an embedded image, so no extraction mode can see it. Applied by hand, with the reason in the row's `correction` field. |

**The correction that created that token, and why it should worry you.** The Access Bank UK FY2021
edition was recorded `NO_KM1_FOUND`. It is not. Page 7 prints the heading "KM1 - Key metrics
template" and, below it, the sentence "It should be noted that the above ratios are calculated after
taking into account the audited profits for the respective years" — and between the two, where the
table belongs, sits an 861×637 **image**. Both `-layout` and raw reading-order return the heading and
the trailing note with nothing in between. The document as a whole never tripped `NO_TEXT_LAYER`
because the *rest* of it is ordinary text: that same edition's CC1 and LR2 tables extract fine. The
figures were recovered by rendering the page at 300dpi and reading it, transcribed twice from two
independent renderings that agree digit for digit, and are now in `scripts/build_access_bank.py`.

**This was found by opening one document by hand, not by any systematic check, so assume there are
others.** The failure mode — a text-native PDF with one table pasted in as a picture — is invisible
to every test in this survey: the row tokens are absent, the title may be absent too, and the
document-level `NO_TEXT_LAYER` guard does not fire. A cheap detector for it would be "a page whose
text contains a KM1-ish heading but no FIGURE within N lines, and which carries an embedded image",
and no such pass has been run. Until one is, a `NO_KM1_FOUND` on a bank that plainly should have a
KM1 deserves a rendered look before it is believed.

**Why row tokens and not the title.** Keying on "Key metrics" matches prose ("regular reporting of
key metrics") and finds the *wrong table in the right document* — C. Hoare prints its own
"Table 3: Key Metrics" summary **and**, separately, a real UK KM1. Letter-suffixed row tokens cannot
collide with a country row (`UK 2,522,829` has no letter). Tokens are further restricted to the KM1
template's own lettered rows, because a document-wide scan also picks up `UK 22a`/`UK 23b`, which
belong to CR/LIQ templates.

**The counterexample to keep in mind (thanks to the KM1-004 session): ALLICA.** Its report is an
Article 433b small-and-non-complex disclosure, headed "Key metrics", and the string "KM1" **never
appears in it**. Any detector keyed on that token reports absence for a bank that has one. This
detector catches Allica on `UK 7a/7b/7c/7d` alone — FY2022–FY2025 all `KM1_PRESENT`, FY2020
`NO_KM1_FOUND`, which matches that session's independent hand transcription exactly.

## 4. Template drift by edition year

Year inferred from the **filename**, which is not the reporting period (FirstBank's `2019/06/` upload
path holds 2020–2024 documents). Read this as a shape, not a fact.

| year | UK_KM1 | UNPREFIXED | NO_KM1 | BANK_STYLED | UNLOCATED |
|---|---|---|---|---|---|
| ≤2018 | 0 | 3 | 63 | 0 | 4 |
| 2019 | 0 | 5 | 27 | 0 | 3 |
| 2020 | 0 | 4 | 30 | 0 | 3 |
| 2021 | 2 | 9 | 46 | 0 | 11 |
| 2022 | 37 | 14 | 47 | 7 | 7 |
| 2023 | 53 | 13 | 22 | 8 | 6 |
| 2024 | 65 | 10 | 43 | 9 | 6 |
| 2025 | 57 | 15 | 19 | 7 | 2 |
| 2026 | 20 | 1 | 4 | 0 | 0 |

The UK template appears from ~2021 with the Disclosure (CRR) Part of the PRA Rulebook. **A pre-2021
`NO_KM1_FOUND` is the expected result, not a gap.**

## 5. The 45 `UNFETCHED` rows are not one thing

Carried forward from an earlier detector because no cached PDF exists to re-read (tagged
`carried_forward`). They break into four classes, and reading them as "45 unavailable documents"
would be wrong in most cases:

- **19 BLOCKED by the host (403)** — nbeuk (8), pnb (4), itau (3), ubs (3), eabplc (2). **Blocked is
  not dead** and must not be resolved by guessing filenames.
- **13 documented dead originals** — Shawbrook (7) and FirstBank (6). These are provenance constants
  (`P3_DEAD`, `ORIG_P3_*`) deliberately retained in the build scripts; their **live replacements are
  cited separately and were surveyed successfully** (Shawbrook: 12 other readable rows, 7 of them
  `KM1_PRESENT`).
- **1 transport, not host** — persiabank returns `status=000` over `https://` but the host is alive
  over `http://` (TLS handshake failure, which `-k` does not rescue).
- **12 candidate genuine rot** — kingdom.bank (4), methodist_chapel_aid (4), redwood, rathbones,
  united_trust, mca. Two of these URLs end **mid-filename** in our own TSV
  (`…approved-14-`, `…31_december_2024_pillar_3_`), i.e. extractor truncation rather than a dead
  document. Needs a look before any is called link rot.

## 6. The 28 banks with no `KM1_PRESENT` — read this before writing any "Not applicable" sheet

**This list is not "banks that publish no KM1".** It is "banks with no KM1 in the editions *we cite*".
Only **12 of 28** are pure `NO_KM1_FOUND` with no candidates and no fetch problems:
`bank_mandiri_europe, bank_of_africa_uk, bank_saderat, bank_sepah_international, birmingham_bank,
fcmb_uk, ghana_international_bank, hbl_bank_uk, state_bank_of_india_uk, tsb, united_national,
weatherbys`.

The other 16 carry candidates or fetch failures. The sharpest case is **`national_bank_of_egypt_uk`:
7 URLs blocked by 403, 2 scanned with no text layer, 1 readable.** That bank is effectively
**unsurveyed** — marking it "Not applicable" would be a fabrication, not a finding.

### SDDT (PRA Rule 3.1) does **not** explain this list

Rule 3.1 is the opt-in that removes the Pillar 3 duty (1.2 / 2.1(9) / 2.6 are eligibility criteria
only; the register spells values `Ru 3.1`, not `3.1`). 10 of the 28 have a candidate Rule 3.1 row —
**but every start date falls in 2024–2026** (Kroo 17/05/2024, Reliance 05/04/2024, Methodist Chapel
Aid 11/04/2024, Cynergy 17/01/2025, Triodos 11/03/2025, Weatherbys 02/04/2025, PNB Europe
10/11/2025, HSBC Innovation 04/12/2025, Birmingham 14/04/2026, Vida 03/04/2026). **Date-fitted, that
explains at most the most recent edition year or two and nothing before it**, while most of these
banks' absences sit in 2019–2023.

And it is not a predictor in either direction: **Secure Trust (09/07/2024), C. Hoare (09/12/2025),
Cambridge & Counties (20/02/2025) and Monument (15/01/2025) all hold Rule 3.1 waivers and all print
full KM1 tables in this corpus.** Rule 3.1 removes a duty; it does not mean a bank stopped
publishing.

Name matching against the register is **strict and review-only**: a loose matcher produced three
cross-entity false hits earlier (Cambridge Building Society → `cambridge_and_counties`), and in this
very join `hsbc_innovation_bank` matched three firms (HSBC Bank Plc, HSBC UK Bank Plc, HSBC
Innovation Bank Limited) of which only the last is the right entity.

## 7. Fields, and the trap in each

- **`uk_rows` / `eu_rows` / `bare_rows`** — **a FLOOR, never a complete row set.** `pdftotext` splits
  some cells across lines; Secure Trust FY2024 prints `UK 11a` and it is absent from *both* extraction
  modes. A missing row is **not** evidence the bank did not disclose it. (Used well, though, the field
  detects real drift: `8a/9a/10a` appear in Allica's FY2022–23 editions and vanish in FY2024–25,
  independently reproducing that session's hand-transcribed finding.)
- **`other_uk_template_rows`** — non-KM1 UK rows seen. Evidence of template *era* only.
- **`column_headers`** — **locators, not parsed dates.**
  1. *Not deduplicated.* Monzo FY2024 prints `2024 2024 2023` — three columns, two sharing a year
     because they are different **entities**. Collapsing repeats destroys exactly that distinction.
  2. *Sometimes fragments.* Aldermore prints the day (`30-`) on one line and `Jun-26` on the next.
     Read `header_block` for the real header.
  3. **The column set is a property of the TABLE, not the bank.** KM1 is a five-column template
     (T, T-1, T-2, T-3, T-4 — ICBC London prints that row explicitly). A quarterly filer populates all
     five; Alrayan prints the column letters `a e` above two dates, filing the same five-column
     template while populating only a and e. So "2 columns" and "5 columns" can be the same template,
     and a count inferred from how many dates are visible is wrong in both directions. A table may
     also be two entity blocks side by side: Aldermore is Group a/b/c + Bank a/b/c = six genuine
     columns with six distinct figures per row.
- **`entity_row`** — the line above the dates when it names ≥2 entities (`Group Bank Bank`).
  **Empty means "no multi-entity row found", NEVER "one entity"** — single-entity tables usually print
  no entity row at all.
- **`header_block`** — lines around the column header, whitespace-collapsed, verbatim. This is where
  the entity call gets made, and it often carries the **unit/currency** line. Check it: **ICBC London's
  KM1 is denominated in USD**, not sterling; Alrayan's is in £m, not £'000.
- **`anchor_tier` / `anchor_line`** — which rule located the table, and the line it located.
  `anchor_tier: null` means **the table was not located**, so empty `column_headers` means "nowhere to
  look", not "no columns". **Read `anchor_line` before trusting anything derived from it**: a wrong
  anchor is invisible in its own output, because a foreign table still yields plausible dates. This
  field exists because earlier detector versions reported **OV1's** columns (ICBC London), **CC1's**
  (Provident, Metro) and a **contents page's** (`1 Introduction 1`) under confident `KM1_PRESENT`
  verdicts.
- **`zero_glyphs`** — counts of `—`, `–`, `-`, `0%`, `0.00%`, `nil`, `n/a` within 80 lines of the
  anchor. Recorded, never normalised: **a dash stays blank and a printed zero stays zero.** Corpus
  spread: `hyphen_cell` 380, `zero_pct` 327, `en_dash` 197, `zero_2dp_pct` 36, `em_dash` 31, `nil` 15,
  `n/a` 15. Counts are regional — treat as "this edition's house style", not a per-row map.
- **`rows_marked_restated` / `restated_mentioned`** — row tokens followed by `*`, and whether
  "restat" appears near the table. Monzo FY2024 asterisks eight rows restated for FY2023.
- **`table_page`** — form-feed count to the anchor. A locator, not a citation.
- **`carried_forward`** — kept from an older detector because no cached PDF existed. **Not a
  current-version finding.**

## 8. Known limits

1. **Rows are a floor.** The single most important caveat in the file.
2. **`NO_TEXT_LAYER` is excluded from denominators.** It is a fact about the PDF's text layer, not the
   document's content.
3. **Coverage is of URLs this project already cites** — a fact about our citation list, not about what
   a bank has published. The project was a full year stale on Monzo; Aldermore's own index carries
   three Pillar 3 editions (FY2020, FY2021, FY2023) that we have never cited. **Staleness must be
   answered against each bank's own disclosure index**, which is step 1 of every rollout ticket.
4. **A split header defeats column extraction** on some editions; `header_block` shows the split
   rather than silently repairing it.
