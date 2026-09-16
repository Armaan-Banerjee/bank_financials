# Wayback `id_` conversion — application pass

Applying the peer-verified conversion list in `research/RESUME_linkrot_2b.md`
to the build scripts. Worked 2026-09-16.

Rule applied: insert `id_` after the 14-digit timestamp; remove any existing
`if_`. Everything after the timestamp stays byte-for-byte identical — scheme,
URL-encoding (`%20`, `%203%20`), `:80` ports and all. The Wayback host's own
scheme (`http://web.archive.org` vs `https://`) is also left exactly as found;
Zenith's two rows are `http://` on both sides and stayed that way.

**Verification standard** (per coordinator correction): a `%PDF` header is NOT
sufficient — a 1 MiB Wayback truncation still begins `%PDF`. Every check below
is a **full download** + `pdfinfo` page count + a size that is not exactly
1,048,576 bytes. Helper: `scratchpad/vfy.sh` (browser UA, 8 retries, 12s
backoff; HTTP 5xx / "Temporarily Offline" treated as throttling, never absence).

**No figure was changed anywhere in this pass.**

OUT OF SCOPE, untouched (other agents): `build_arab_bank_europe.py`,
`build_persia_international_bank.py`, `build_itau_bba_international.py`.

---

## Summary

| Script | Converted | Deliberately not converted |
|---|---|---|
| build_atom_bank.py | 4 | — |
| build_bank_of_africa_uk.py | 0 | 2 — repointed to live URLs instead |
| build_chetwood.py | 7 (8 textual occurrences) | — |
| build_credit_suisse_international.py | 6 | 2 year-only `/web/2024id_/` rows, already `id_` |
| build_fce_bank.py | 16 | 1 (20240723091812, not on the peer's list) |
| build_gulf_international_bank_uk.py | 1 | 2 — capture truncated, see below |
| build_hampden_co.py | 1 | — |
| build_hsbc_uk_bank_plc.py | 2 | — |
| build_methodist_chapel_aid.py | 0 | 4 — already `id_` on disk before this pass |
| build_national_westminster_bank.py | 1 (2 textual occurrences) | — |
| build_recognise_bank.py | 1 | — |
| build_smbc.py | 9 | — |
| build_union_bancaire_privee_uk.py | 2 | — |
| build_united_national.py | 7 (`if_` → `id_`) | — |
| build_unity_trust.py | 1 | — |
| build_vanquis.py | 6 | — |
| build_zenith.py | 2 | 2 already `id_` |

**64 citations converted.** Every edited script rebuilt; sheet lists compared
against `git show HEAD:` for each workbook — all identical, no sheet added,
removed or renamed.

---

## Per script

### build_atom_bank.py — DONE
4 rows, lines 23-26, bare → `id_`. All 4 fetched:
18-19 `20221005205114` 455,311B/53pp · 17-18 `20221005211108` 6,202,886B/52pp ·
16-17 `20221005211125` 2,328,199B/22pp · 19-20 `20221005223922` 251,842B/60pp.
All page counts matched the peer's. Rebuilt, 18 sheets.

### build_chetwood.py — DONE (checked exhaustively)
7 citations converted. The `20200929085826` timestamp matched in **two** places:
the `P3_20_URL` constant and the same URL spelled across two f-string fragments
in the FY2024 gap note. Both converted — same citation.

All 7 fetched in full, because Chetwood's filenames are undated and repeat
across editions:

| document | ts | bytes | pages | expected |
|---|---|---|---|---|
| P3 FY2020 | 20200929085826 | 767,512 | 23 | 23 |
| P3 FY2021 | 20211128171331 | 425,422 | 29 | 29 |
| P3 FY2022 | 20230131235943 | 755,204 | 41 | 41 |
| P3 FY2023 | 20240315022245 | 764,030 | 34 | 34 |
| AR 2021 | 20210830132929 | 3,518,647 | 82 | 82 |
| AR 2022 | 20230131231341 | 692,880 | 60 | 60 |
| AR 2024 | 20240920030034 | 10,751,242 | 61 | 61 |

Edition check (the Metro trap) — every Pillar 3 cover and internal "as at" line
read directly. All four distinct, all matching the year the script assigns:
June 2020 / as at 31st March 2020; August 2021 / 31st March 2021; October 2022 /
31st March 2022; January 2024 / 31st March 2023. No cross-year mis-citation.

**Discrepancy found and corrected (not a figure).** The script called the FY2020
capture an "8-page" PDF, in a comment AND in the FY2020 citation prose that
reaches the workbook. It is 23 pages (the 767KB size it quoted was right). The
same sheet cites "Section 5.2 (Liquidity ratios, p.18)", impossible in an 8-page
document, so the count was simply mis-recorded. Corrected to 23 in both places
with a dated note. Rebuilt, 18 sheets.

### build_credit_suisse_international.py — DONE
6 rows, lines 108-113, `if_` → `id_`. The two year-only `/web/2024id_/` rows
(FY2021, FY2022) left alone — already `id_` and resolving, per the peer's note.
All 6 fetched: 2015 1,076,363B/50pp · 2016 1,157,724B/48pp · 2017 838,666B/74pp ·
2018 837,245B/78pp · 2019 1,127,119B/84pp · 2020 5,025,906B/84pp. All matched.
Rebuilt, 18 sheets.

### build_fce_bank.py — DONE (all 16 checked)
16 rows converted, all bare → `id_`. All 16 fetched in full; every one `%PDF`,
every page count exact, none at 1,048,576 bytes:

2014 Pillar 3 479,795B/37pp · AR2006 2,502,084B/100pp · AR2007 4,418,334B/128pp ·
AR2008 1,352,362B/140pp · AR2009 1,237,529B/127pp · AR2010 1,266,731B/129pp ·
AR2011 2,826,873B/131pp · AR2012 3,888,123B/133pp · AR2013 3,365,008B/134pp ·
AR2014 1,925,001B/122pp · AR2015 3,778,297B/167pp · AR2016 2,785,858B/167pp ·
AR2017 3,113,014B/131pp · AR2018 3,925,679B/149pp · AR2019 3,536,466B/167pp ·
AR2020 2,603,938B/178pp.

This mattered more than usual: the script's own comments record that the FIRST
crawl of every one of these URLs hit the 1 MiB truncation and that the
2022-06-15 / 06-20 re-crawl was substituted. The full-download check confirms
the substituted timestamps are the untruncated ones.

**Left unconverted, flagged for a follow-up pass:** capture `20240723091812` of
`…/investor_center/2022/FCE Bank PLC - Annual Pillar 3  Report.pdf`, cited in
bare form inside the FY2022 prose note. It is not on the peer's list so it was
out of my scope, but I fetched it anyway: 1,657,641 bytes / 56 pages, healthy
and not truncated. It would convert cleanly if someone is authorised to.
Rebuilt, 18 sheets.

### build_bank_of_africa_uk.py — DONE (live URLs, no conversion)
Neither Wayback row converted. Both repointed to the live site, as briefed.
Fetched both live URLs myself in full:
- FY2017 `…/pdfs/finances/BMCE___Pillar_III_VF___31122017.pdf` — 1,164,813
  bytes, 32pp, cover "2017 PILLAR III DISCLOSURES".
- FY2015 `…/pdfs/finances/BMCE___Pillar_3_disclosures____2015.pdf` — 430,862
  bytes, 5pp, cover "BMCE BANK INTERNATIONAL plc PILLAR 3 DISCLOSURES FOR THE
  YEAR 2015".
Both bear "Company Registration N°5321714 (England and Wales)" — the UK entity,
not the Moroccan parent. Exactly as the peer described.

Wayback URLs kept (never deleted) as labelled archival fallbacks, and now
written into the Pillar 3 citation text so the provenance chain is readable on
the sheet:
- FY2015 fallback converted to `id_` and verified — 430,862 bytes / 5pp,
  identical in size to the live file.
- FY2017 fallback left **bare** deliberately. I re-tested all three playback
  forms: bare, `if_` and `id_` each return exactly 1,048,576 bytes against the
  live file's 1,164,813 — the capture itself is truncated, so no form is a
  contract and converting would only make a corrupt file look authoritative.
  Recorded in the script as "provenance only, do not promote".
Rebuilt, 18 sheets.

### build_gulf_international_bank_uk.py — DONE, with a finding
FY2022 row `20240223164517` converted; verified 1,137,898 bytes / 33pp. ✅
FY2020 `20220518000354` and FY2021 `20230329132856` left unconverted, correctly.

I independently reproduced the truncation: downloaded **all three playback forms
of both URLs** — six files, every one exactly 1,048,576 bytes, md5-identical per
URL (`edfe2438dbff06fdc617e6a38efb6059` FY2020,
`32d6206989581714144f61ffc6982ab5` FY2021), no `pdfinfo` page count.

**But "unrecoverable" is too strong, and I could not reproduce it.** The
coordinator's note said Ghostscript yields a 2,431-byte blank page and the files
are dead. In my hands:

```
gs -o out.pdf -sDEVICE=pdfwrite gib_<ts>.pdf
```
- FY2020 → 795,035 bytes, **38 pages**, cover "GIB (UK) Ltd : Pillar 3
  Disclosures / 31.12.2020"
- FY2021 → 697,523 bytes, **30 pages**, cover "GULF INTERNATIONAL BANK (UK) LTD
  / Pillar 3 disclosures / 31 December 2021"

Text extracts on every page through the last (last-8-page character counts are
all 380-2,600, not zero). The truncation removed the trailing cross-reference
table, not the page content streams. `qpdf` is the unreliable route here — it
reports "can't find startxref" and reconstructs; Ghostscript's object scan is
what reproduces the full page count. This **corroborates the script's own
pre-existing FY2020 note** (a prior session repaired it with qpdf and read it)
rather than the "dead files" account.

Figures spot-checked against the rebuilt documents, and they tie:
FY2020 leverage 4.61% and Total Capital ratio 26.48%; FY2021 CET1 capital
$371,866k, CET1/Total capital ratio 19.22%, leverage 3.52%, with the FY2021
edition's own prior-year column showing $378,549k / 26.04%. The workbook
already carries leverage 3.52% (FY2021) and 4.61% (FY2020). **No figure
touched.**

Wrote a new `P3_CAPTURE_INTEGRITY_NOTE`, appended to every Pillar 3 metric
sheet's citation, recording: the truncation and md5s; why `id_` is deliberately
NOT applied to these two; the working Ghostscript recovery recipe; the
exhausted search (one 200 capture per URL in CDX, gibam.com 404s on 2020/2021/
2022 paths and has no disclosures index, the svdcdn CDN holds 2023-2024 only,
~10 permutations 404, Memento/Common Crawl/archive.today empty); and the
**entity-basis trap** — gib.com is REACHABLE (200 to browser headers; the
earlier 403 is withdrawn, it is not a blocked host) and hosts many Pillar 3
PDFs, but every one belongs to GIB B.S.C. (Bahrain), the KSA entity or the Abu
Dhabi branch, and all were examined and rejected on entity basis.

Note a separate agent had already added a `P3_COMPARATIVE_NOTE` to this script
describing FY2020/FY2021 as "unretrievable". I did not touch it — it is that
agent's work and its comparative-column findings stand — but my note sits
alongside it and the two disagree on that one word. A human should reconcile.
Rebuilt, 18 sheets.

### build_hampden_co.py — DONE
1 row `20220518033330`. Verified 485,478B / 37pp. Rebuilt, 18 sheets.

### build_hsbc_uk_bank_plc.py — DONE
2 rows. FY2019 `20221014171921` 584,379B/46pp; FY2020 `20240527084156`
471,031B/57pp. Rebuilt, 19 sheets (this bank legitimately carries an extra
"Interim Pillar 3" sheet — unchanged from HEAD).

### build_methodist_chapel_aid.py — NOTHING TO DO
All 4 listed rows were **already** in `id_` form on disk before this pass (as is
a 5th, the FY2022 row `20240517201255`). The peer's list was evidently taken
from an earlier revision. 0 conversions, script not modified.
I still verified all 4: FY2019 287,814B/20pp · FY2020 311,788B/19pp ·
FY2021 319,857B/20pp · FY2023 318,898B/22pp — all matching the peer's counts.
The workbook was rebuilt during checking and then restored from HEAD, since the
script did not change (`git checkout -- "banks/METHODIST CHAPEL AID …"`).

### build_national_westminster_bank.py — DONE
1 citation, `20220218072522`, appearing **twice** — once in the sourcing comment
at line ~756 and once in the `NWH_P3_2021_URL` constant. Both converted.
Verified 1,001,072B / 144pp. Rebuilt, 19 sheets (unchanged from HEAD).

### build_recognise_bank.py — DONE
1 row `20231210004904` (`http://` Wayback host preserved). Verified
353,559B / 7pp. Rebuilt, 18 sheets.

### build_union_bancaire_privee_uk.py — DONE
2 rows. FY2019 `20210918132915` 416,201B/4pp; FY2021 `20240706060918`
132,721B/3pp. Rebuilt, 18 sheets.

### build_united_national.py — DONE
7 rows, all `if_` → `id_`. All 7 fetched:
2016 943,754B/62pp · 2017 1,621,689B/62pp · 2018 1,586,319B/63pp ·
2019 1,965,359B/63pp · 2020 1,934,840B/64pp · 2021 1,945,080B/65pp ·
2022 1,030,848B/66pp. All matched. Rebuilt, 18 sheets.

### build_unity_trust.py — DONE
1 row `20221124023931`. Verified 594,340B / 22pp. Rebuilt, 18 sheets.

### build_vanquis.py — DONE
6 rows, all fetched:
2015 574,702B/23pp · 2016 559,563B/22pp · 2017 362,119B/28pp ·
2018 377,462B/31pp · 2019 510,363B/34pp · 2020 354,489B/32pp. All matched.
Rebuilt, 18 sheets.

### build_zenith.py — DONE
2 rows, `20160826052010` and `20161128044735`. **`http://` preserved on both
sides** — Wayback host and original URL alike — since changing the scheme
changes the URL's identity in the archive. Verified: 2014 176,943B/19pp;
2015 196,633B/18pp. The script's two other Wayback URLs were already `id_` and
were not touched. Rebuilt, 18 sheets.
Caution for a successor: this script was already modified in the working tree by
another agent (a scale fix, `RESUME_zenith_scale.md`) when I edited it. My change
is confined to the two URL string literals on lines 188-189.

### build_smbc.py — DONE
9 rows converted, all fetched (note the `%20`-encoded path on the 2022 row,
preserved exactly):
FY2014 `20240701160935` 1,163,361B/41pp · FY2015 `20240527065243` 823,966B/39pp ·
FY2016 `20240527070848` 839,697B/45pp · FY2017 `20230330205458` 975,843B/50pp ·
FY2018 `20240527071821` 948,716B/63pp · FY2019 `20240527071944` 582,846B/66pp ·
FY2020 `20240527071545` 839,296B/60pp · AR2021 `20240612221125` 1,862,545B/144pp ·
FY2022 `20240712094621` 1,827,783B/53pp. All matched. Rebuilt, 19 sheets
(unchanged from HEAD).

---

## Fetch verification tally

**68 full downloads** across this pass (64 converted citations + the 2 Bank of
Africa live URLs + the FY2015 Wayback fallback + the out-of-scope FCE capture),
plus 6 downloads of the GIB UK truncated captures and 4 re-checks of the
already-converted Methodist rows.

- Every converted URL that was fetched returned `%PDF`, a `pdfinfo` page count,
  and a size ≠ 1,048,576.
- **Every page count matched the peer's stated count. No mismatches.**
- No fetch returned a dead result. No 5xx/"Temporarily Offline" retry loop was
  needed beyond one transient connect timeout on the Chetwood AR2024 download,
  which succeeded on a second attempt (10,751,242B/61pp).

## Open items for a human

1. **GIB UK "unretrievable" wording.** My Ghostscript recovery contradicts the
   coordinator's "dead files" account and matches the script's own older note.
   The `P3_COMPARATIVE_NOTE` another agent added still says the FY2020/FY2021
   editions are "unretrievable"; my `P3_CAPTURE_INTEGRITY_NOTE` says truncated
   but recoverable, and gives the recipe. One word needs reconciling; I left
   the other agent's text alone.
2. **FCE `20240723091812`** — healthy (1,657,641B/56pp), still bare, eligible
   for conversion but outside the briefed 16.
3. **Chetwood FY2020 page count** was wrong in the workbook prose (8 → 23);
   corrected. Worth a glance in case the same "8-page" figure was copied into
   any insights deliverable.
