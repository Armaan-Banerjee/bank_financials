# GIB UK — sourcing FY2021/FY2022 from later editions' comparative columns

Started 2026-09-16. Context: GIB UK's FY2020 and FY2021 Pillar 3 editions are
unrecoverable (sole Wayback capture of each truncated at exactly 1,048,576
bytes; see `research/RESUME_linkrot_2b.md`). This work does NOT re-chase those.
It reads the two editions that DO exist and harvests their prior-year
comparative columns.

## Documents fetched and verified

| Edition | URL | Bytes | Pages | Entity on cover |
|---|---|---|---|---|
| FY2022 | `https://web.archive.org/web/20240223164517id_/https://gibam.com/assets/2022-GIBUK-Pillar-3-disclosures_VF.pdf` | 1,137,898 | 33 | GULF INTERNATIONAL BANK (UK) LTD — Pillar 3 disclosures, 31 December 2022 |
| FY2023 | `https://gib-am.files.svdcdn.com/production/documents/Fund-sustainability-related-documents/2023-GIBUK-Pillar-3-disclosures.pdf` | 530,545 | 33 | GULF INTERNATIONAL BANK (UK) LTD — Pillar 3 disclosures, 31 December 2023 |

Both are `%PDF`, neither is 1,048,576 bytes, both give a real `pdfinfo` page
count, both have a clean text layer (`pdftotext -layout`). Both are the UK
entity's OWN disclosure — not the Bahraini parent, not the KSA entity, not the
Abu Dhabi branch.

## Does each edition carry a comparative? YES — exactly one year back.

Both use the UK KM1 template with **two** columns only:
`T - Current year` and `T-4 - Prior year`. Same in UK OV1.

- **FY2022 edition** → `T-4 = 31-Dec-21`. Carries FY2021.
- **FY2023 edition** → `T-4 = 31-Dec-22`. Carries FY2022.

Neither reaches FY2020. Confirmed by grep: the only occurrence of "2020"
anywhere in the FY2022 edition is a stray CCyB narrative parenthesis
("weighted average CCyB rate of 0.08% (2020: 0%)"), not a metric column.

**FY2020 therefore remains unsourceable.** No figure was manufactured for it.

## FY2022 edition, p.6 (UK KM1), T-4 column = 31 Dec 2021

| KM1 row | Figure ($'000 / %) | vs. what was already on the sheet |
|---|---|---|
| 1/2/3 CET1 = Tier 1 = Total capital | 371,866 | MATCHES exactly |
| 4 Total RWEA | 1,932,234 | MATCHES exactly |
| 5/6/7 CET1 = T1 = Total capital ratio | 19.22% | MATCHES exactly |
| 13 Total exposure measure **excl. claims on central banks** | 5,268,295 | **DIFFERENT BASIS** — sheet has 10,573,209 |
| 14 Leverage ratio **excl. claims on central banks** | 7.06% | **DIFFERENT BASIS** — sheet has 3.52% |
| 15 Total HQLA (weighted value - average) | 6,737,809 | MATCHES exactly |
| UK 16a Cash outflows, total weighted value | 2,006,717 | not a row on this sheet |
| UK 16b Cash inflows, total weighted value | 603,374 | not a row on this sheet |
| 16 **Total net cash outflows (adjusted value)** | **1,403,343** | **WAS BLANK — now filled** |
| 17 LCR | 480.13% | MATCHES exactly |
| 18/19/20 NSFR ASF / RSF / ratio | **all blank in the T-4 column** | no comparative; FY2021 NSFR stays as-is |

FY2022 edition, pp.26-27 (UK OV1), T-4 column = 31 Dec 2021: credit risk excl.
CCR 1,633,319; CCR total 35,645 (of which CVA 12,553, other CCR 23,092); market
risk 166,380; operational risk 96,890; Total 1,932,234. **All match the RWA
Breakdown sheet exactly.**

### The one disagreement — a BASIS restatement, not an error

FY2021 leverage is printed on two different bases by two different documents:

- FY2021 edition (as originally reported, now unretrievable): exposure
  10,573,209, ratio 3.52%. 371,866 / 10,573,209 = 3.517% → ties to 3.52%.
- FY2022 edition's T-4 comparative: exposure **excluding claims on central
  banks** 5,268,295, ratio 7.06%. 371,866 / 5,268,295 = 7.058% → ties to 7.06%.

Both are internally consistent against the same FY2021 CET1 of 371,866, so
neither is miscast. The gap (10,573,209 − 5,268,295 = 5,304,914) is of the same
order as FY2021 cash and cash equivalents (5,599,337), i.e. central bank claims.
The FY2022 edition's own §6.6 says the UK Leverage Framework excluding
qualifying central bank claims applied to the Bank **from 1 January 2022** — so
the FY2022 edition has restated FY2021 onto the new basis for comparability.

Per the project's rule: **both recorded, on separate labelled rows. Not
reconciled, not overwritten.** This also upgrades the Leverage sheet's existing
note from "likely on an including-central-bank-claims basis" to confirmed.

## FY2023 edition, p.6 (UK KM1), T-4 column = 31 Dec 2022

Every FY2022 figure in the comparative column — CET1/T1/Total capital 368,416;
RWEA 1,557,567; ratios 23.65%; exposure measure 5,136,739; leverage 7.17%; HQLA
9,198,733; net cash outflows 2,597,379; LCR 354.15%; NSFR ASF 4,297,495 / RSF
1,031,978 / 416.49% — **matches the sheet exactly. No restatement.**
Same for the FY2023 edition's UK OV1 T-4 column (all six FY2022 RWA lines match).

### Missing for FY2023 itself — one row found

KM1 row **14b "Leverage ratio including claims on central banks (%)" = 1.92%**
for 31-Dec-23. This row is blank in the FY2022 edition. It is the only FY2023
datum in that document not already on the sheet; every other FY2023 KM1 and OV1
figure already matches.

## Secondary but material finding

Every FY2021 Pillar 3 figure on this workbook except leverage is now
**independently corroborated** by a second, fully retrievable document (the
FY2022 edition's comparative column). The FY2021 sheets no longer rest solely
on the truncated FY2021 capture.

## Edits made to `scripts/build_gulf_international_bank_uk.py`

1. New `P3_COMPARATIVE_NOTE` constant, appended to `p3_sources()` so it lands on
   all 11 Pillar 3 metric sheets. States the comparative-column basis, the
   pre-read PDF verification, and that FY2020 was not back-solved.
2. LCR sheet: FY2021 "Total net cash outflows, adjusted value" = $1,403,343k
   (was blank) → £1,037.9k at FY2021 spot 1.3521. Note rewritten to name the
   FY2022 edition, KM1 row 16, T-4 column as the source and record both
   cross-checks.
3. Leverage sheet: two new FY2021 rows for the excl.-central-banks restatement
   ($5,268,295k → £3,896.4k; 7.06%), plus one new FY2023 row for KM1 row 14b
   (1.92%, incl. central banks). Existing rows untouched. Note rewritten; the
   old "likely on an including-central-bank-claims basis" hedge is now
   confirmed.
4. `p3_sources()` FY2022 line: dropped the unverifiable "matches ... where both
   are legible" claim, since the match is now actually verified and recorded in
   `P3_COMPARATIVE_NOTE`.
5. Overview note extended to flag the FY2021/FY2023 leverage dual bases
   (Overview is a copy and does not inherit detail-sheet changes).
6. `metric()` helper `source_height` 140 → 320; at 140 the now-longer citation
   cell clipped.

NOT changed: `P3_2022_URL` left in its existing bare-playback form rather than
repointed to `id_`. The `id_` form is what was actually downloaded and read, and
`research/RESUME_linkrot_2b.md` lists this row for bare→`id_` conversion — but
that conversion is that ticket's, and another agent is editing this same file.
Both forms resolve to the same capture 20240223164517.

## Status

DONE. Script rebuilt; sheet count unchanged at 18. No commit made.
