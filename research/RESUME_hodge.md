# RESUME — Julian Hodge Bank Limited (FRN 204439, company 00743437)

Session 2026-09-16. Script: `scripts/build_julian_hodge_bank.py`.
Workbook: `banks/JULIAN HODGE BANK FINANCIALS.xlsx`.

## Headline

The earlier in-script note asserting the historical Pillar 3 URLs were a
**soft-404 was testing the wrong paths**. It checked `/wp-content/uploads/2019/01/`,
`/2019/04/`, `/2020/02/` and `/2021/02/` — those really are dead (honest 404 /
a genuine soft-404 landing page), so that half of the note was correct. But the
whole historical series was **re-uploaded on 2024-07-25 to
`/wp-content/uploads/2024/07/`**, where it is live and genuine. The note's
conclusion ("DO NOT RESTORE THE ABOVE TO LIVE hodgebank.co.uk URLs") was
therefore wrong and had to be corrected.

## Verification method (every file)

HTTP status + `Content-Type: application/pdf` + `%PDF` magic bytes +
`pdfinfo` page count + cover text read. Host uses a `www` -> apex **301**, so
`curl` without `-L` returns 301/162 bytes and looks like a failure — that is
almost certainly what tripped an earlier check.

**The soft-404 on this host is PER-FILENAME, not per-directory.** Do not
generalise a negative control to a whole directory. Measured:

| URL | Result |
|---|---|
| `/2020/02/FINAL-Julian-Hodge-Bank-Limited-FY18.pdf` | 200 **text/html** 108,306 B — SOFT-404 landing page (md5 `c69229b0d911df8ea64ada86d57738a2`) |
| `/2020/02/zzz-nonexistent-control.pdf` | honest 404, text/html, 146 B |
| `/2021/02/2.-JHB-Pillar-III.pdf` | 200 **text/html** 108,306 B — same SOFT-404 page |
| `/2021/02/zzz-control.pdf` | honest 404, 146 B |
| `/2019/01/jhb-pillar3-2014.pdf` | honest 404, 146 B |
| `/2024/07/zzz-nonexistent-control.pdf` | honest 404, 146 B |

WordPress serves that one landing page for certain **known old attachment
slugs**; an unknown name in the very same directory 404s honestly. So a
negative control proves nothing about a *different filename* in that directory.

**The decisive test is per-URL `Content-Type` + `%PDF` magic bytes**, which was
run on every file below. A 200 with `text/html` is a soft-404 no matter where it
sits; a 200 with `application/pdf` + `%PDF` is genuine. Never classify on status
code alone.

## Editions found — continuous FY2010–FY2023 (14), all live

Base: `https://hodgebank.co.uk/wp-content/uploads/2024/07/`

| FY | Filename | Bytes | Pages | Cover reads |
|----|----------|-------|-------|-------------|
| 2010 | jhb-pillar3-2010.pdf | 299,440 | 27 | "Julian Hodge Bank Limited / Pillar 3 disclosures / as at 31 October 2010" |
| 2011 | jhb-pillar3-2011.pdf | 303,361 | 28 | "... as at 31 October 2011" |
| 2012 | jhb-pillar3-2012.pdf | 320,097 | 21 | "... as at 31 October 2012" |
| 2013 | jhb-pillar3-2013.pdf | 309,101 | 23 | "... as at 31 October 2013" |
| 2014 | jhb-pillar3-2014.pdf | 351,821 | 23 | "... as at 31 October 2014" |
| 2015 | jhb-pillar3-2015.pdf | 289,203 | 23 | "... as at 31 October 2015" |
| 2016 | jhb-pillar3-2016.pdf | 774,618 | 34 | "... as at 31 October 2016" |
| 2017 | jhb-pillar3-2017.pdf | 598,871 | 34 | "... as at 31 October 2017" |
| 2018 | jhb-pillar3-2018.pdf | 876,285 | 37 | "BANK / Pillar 3 Disclosures / Year ended 31 October 2018" |
| 2019 | Pillar-3-Disclosure-FY19-FINAL.pdf | 695,975 | 36 | (FY19 per filename + content) |
| 2020 | 2.-JHB-Pillar-III.pdf | 2,416,601 | 54 | "Hodge Bank / Pillar 3 Disclosures / Period ended 30 September 2020" |
| 2021 | Hodge-Pillar-3-Document-2020_2021.pdf | 1,318,364 | 58 | "... 30 September 2021 / Registered number 00743437" |
| 2022 | Hodge-pillar-3-19.06.23.pdf | 19,873,168 | 41 | "... 30 September 2022" |
| 2023 | Hodge-pillar-3-11.03.24.pdf | 17,008,649 | 39 | "... 30 September 2023" |

**Filename never equals period**: `Hodge-pillar-3-19.06.23.pdf` is a 2023
*publication* date on the **FY2022** edition. Cover is the only trustworthy source.

**Year-end moves mid-series**: 31 October through FY2019; 30 September from
FY2021 (FY2020 = 11-month transition period). Confirmed off each cover.

## Enumeration sources used

1. Filename permutation `jhb-pillar3-<year>.pdf`, 2008–2023, at `/2024/07/`
   (2008, 2009, 2019–2023 return honest 404).
2. WP REST media API, full library enumerated (66 items, 2 pages, complete) —
   caught the five irregular names permutation can never find.
3. Wayback CDX — **BLOCKED**, Internet Archive returned 503/504
   ("temporarily offline") for both `hodgebank.co.uk` and `julianhodgebank.co.uk`.
   Recorded as unknown, not as an absence. Worth a re-run when IA is back,
   though the media API is already a complete listing of the WP library.

Caveat: the media API is not an exhaustive file listing — two Annual Report
PDFs (below) return 200 `application/pdf` at `/2024/07/` without appearing in it.

## FY2024 / FY2025 — settled, do not re-hunt

No FY2024 or FY2025 Pillar 3 edition exists. PRA waivers register, FRN 204439:
Rule 3.1 (the SDDT opt-in that actually removes the Pillar 3 duty) from
**18/02/2025**; Rules 1.2 & 2.1(9) (eligibility only) from 11/02/2025.
- **FY2025** (y/e 30 Sep 2025) falls inside the exemption -> **"Not applicable"**.
- **FY2024** (y/e 30 Sep 2024) ended before it -> ordinary open gap, stays blank.

## Pre-CRD IV content (FY2010–FY2013) — what is actually transcribable

All four are **Basel II / BIPRU**. Grep for "risk[- ]weighted" returns **zero
hits in all four** — no RWA figure exists, so no ratio denominator exists and
no capital ratio is printed. Nothing is derived.

Capital resources table (section 4) and Pillar 1 requirement table (section 5.1):

| FY | PDF p. (cap) | Total Tier 1 | Total capital resources | PDF p. (P1) | Pillar 1 capital req. |
|----|----|----|----|----|----|
| 2010 | 13 of 27 | 108.1 | **114.7** | 15 | 41.5 (credit 40.2 + op 1.3) |
| 2011 | 13 of 28 | 109.7 | **114.8** | 15 | 38.9 (credit 37.7 + op 1.2) |
| 2012 | 11 of 21 | 111.1 | **114.1** | 12 | 36.8 (credit 36.0 + op 0.8) |
| 2013 | 12 of 23 | 113.7 | **114.3** | 13 | 35.3 (credit 34.9 + op 0.4) |

Only **Total capital resources** goes into a data column, on the Total Capital
sheet — matching this script's own existing FY2014 (118.8) / FY2015 (122.4)
treatment. Basel II Total Tier 1 and the Pillar 1 requirement are recorded in
sheet notes only, never as data, exactly as the script already does for
FY2014/FY2015. Precedent for this shape across the project: `build_aldermore.py`
(`P3_DISCLOSURE_YEARS`, Basel II columns, RWA blank by design, capital
requirement never x12.5'd).

## Repointing (old URL always kept as labelled fallback, never deleted)

Live copies are **byte-identical (md5)** to the Wayback copies the script cited
for FY2014–FY2018 and FY2019, so existing transcriptions remain valid:

| Doc | md5 live | md5 Wayback | Match |
|---|---|---|---|
| P3 FY2018 | addbb5d0301b1b2349dbd9b05d3b3dfc | same | yes |
| P3 FY2017 | b76617584f830bf3f6dbb68720744fdd | same | yes |
| P3 FY2016 | 0bd97d21c8ebd0972d5e96be8c6c1d9b | same | yes |
| P3 FY2015 | c448471eea12e998bbfb104e3074d3cc | same | yes |
| P3 FY2014 | 5318b684c1a1d4ef8e84d62a4ba055a4 | same | yes |
| AR FY2019 | 36e033ef90beb287bdc316602bbdda77 | same | yes |

**AR FY2018 — a claim I made and then disproved. The cited Wayback capture is
exactly 1,048,576 bytes but is INTACT, not truncated.** 1 MiB is a *signature*,
not proof. The decisive test is whether the **last** page carries text
(truncation removes the end of a file, so page 1 proves nothing; and a
linearized PDF keeps its page-count hint at the start, so a page count can lie
too). Tested: page 86 of 86 carries real text ending naturally on "38 Ultimate
parent undertaking … Cardiff, CF14 3UZ." — byte-for-byte the same last page as
the live copy. The 114KB size difference is compression, not missing content.
No Ghostscript repair needed or done. **The existing AR2018 Wayback citation is
correct and is left alone.**

Annual Reports: `FINAL-Julian-Hodge-Bank-Limited-FY18.pdf` and
`Julian-Hodge-Bank-Limited-Master-FINAL-EY-Signed-FY19.pdf` do return genuine
PDFs at `/2024/07/` (verified `application/pdf` + `%PDF` + last page), though
they soft-404 at their old `/2020/02/` path. Since both cited Wayback captures
are intact and md5- or content-equivalent, the AR citations are **left on
Wayback** and the live `/2024/07/` alternates are recorded in the script note as
additional sources — no citation churn for zero gain. The older
`jhb-financial-statements-*.pdf` (FY2010–FY2017) and `1.-JHB-Financial-Statements.pdf`
(FY2020) are genuinely 404 everywhere — those stay on Wayback.

## Leverage Ratio sheet — not touched by this session

A concurrent leverage-basis sweep split that sheet into dual labelled rows
(excluding vs including claims on central banks, UK change effective
1 Jan 2022). **This session added nothing to it and collapsed nothing.** The
four Basel II editions print no leverage value at all: grep for "leverage" is
nil in FY2010/FY2011/FY2012, and FY2013's single hit is forward-looking prose
about CRD IV ("enhanced reporting requirements include the introduction of a
leverage ratio…"). Basel III leverage was not a UK disclosure requirement then,
so those years belong on neither row.

## Outcome

Rebuilt; **18 sheets, unchanged**. New third year axis `P3_DISCLOSURE_YEARS`
(= `PILLAR3_YEARS` + FY2013–FY2010) drives the 11 capital metric sheets, now 16
columns. Asset Quality and RWA Breakdown deliberately stay at 12 columns.

Cells filled — **four**, all on Total Capital, each a directly stated total
(and each printed twice in its own document, in section 4 and again in the
section 5.1 table, agreeing both times):

| Year | Total capital resources | Source |
|---|---|---|
| FY2013 | 114.3 | jhb-pillar3-2013.pdf, s.4, PDF p.12 of 23 |
| FY2012 | 114.1 | jhb-pillar3-2012.pdf, s.4, PDF p.11 of 21 |
| FY2011 | 114.8 | jhb-pillar3-2011.pdf, s.4, PDF p.13 of 28 |
| FY2010 | 114.7 | jhb-pillar3-2010.pdf, s.4, PDF p.13 of 27 |

Left out deliberately (recorded in prose, never as data): Basel II Total Tier 1
(113.7 / 111.1 / 109.7 / 108.1) — matching the treatment FY2015/FY2014 already
had; and the Pillar 1 capital requirement (35.3 / 36.8 / 38.9 / 41.5), kept as
capital and never multiplied by 12.5. Every ratio sheet is blank for these four
years because no RWA denominator exists in any of the documents.

MREL FY2025 changed from "Not publicly disclosed" to **"Not applicable"**;
FY2024 left as an ordinary negative. `_parse_percent` in `bank_workbook.py`
returns None for non-numeric strings, so this is chart-safe.

All 36 PDF URLs in the script re-verified: 200 + `application/pdf` + `%PDF`.

## Status

- [x] Enumerate back catalogue (IA CDX blocked; media API complete)
- [x] Confirm year-ends off covers
- [x] Establish what is missing
- [x] Transcribe FY2010–FY2013 Total capital resources
- [x] Repoint dead/archive citations, keep fallbacks
- [x] Delete the false soft-404 note
- [x] Rebuild, sheet count unchanged (18)
