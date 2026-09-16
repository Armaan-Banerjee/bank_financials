# RESUME — Reliance Bank Limited, Leverage Ratio sheet (untraceable-figure pass)

Opened 2026-09-16. Follows the "unrelated defect" flagged in
`RESUME_leverage_basis_sweep.md` (§ "An unrelated defect found while checking —
Reliance Bank Limited"). Entity: Reliance Bank Limited, Companies House 00068835,
FRN 204537, year end 31 March. Script: `scripts/build_reliance_bank.py`.

## STATUS: RESOLVED. Every figure on the sheet is traceable. Nothing blanked.

The sweep's premise — that 4.50 / 7.6 / 11.5 "appear in neither document" — was
correct as far as it went (they are in neither **Pillar 3** edition) but the
conclusion drawn from it was wrong. **All three come from the Bank's own Annual
Reports**, which the sweep did not re-read. The withdrawn
"excluding claims on central banks" label was, for FY2022 onward, the Bank's
**own wording** and should not have been withdrawn wholesale — it was wrong only
because it had been applied to the whole row, including the pre-2022 years.

## 1. Full documentary record (all verified 2026-09-16)

Every URL below: HTTP 200, `Content-Type: application/pdf`, `%PDF` magic bytes,
real `pdfinfo` page count, cover page read. None at 1,048,576 bytes. A negative
control against `wp-content/uploads/2023/10/` returned an honest `404
text/html`, so 200s from that host are real files, not soft-404s.

### Pillar 3 — exactly two editions exist

Re-confirmed by re-enumerating the entire WordPress media library
(`/wp-json/wp/v2/media?mime_type=application/pdf`, 6 pages, **600 PDFs**). Only
two match `pillar`:

| Edition | URL | pages | text layer |
|---|---|---:|---|
| 31 Mar 2022 | `.../2023/04/RBL-Pillar-3-Disclosures-31-March-2022-final-post-Board.pdf` | 14 | yes (29,732 ch) |
| 31 Mar 2023 | `.../2023/10/RBL-Pillar-3-Disclosures-31-March-2023-for-website-30Oct2023.pdf` | 13 | yes (30,004 ch) |

Consistent with the existing SDDT finding (Rule 3.1 modification by consent from
05/04/2024 removes the obligation for FY2025/FY2026; FY2024 remains a genuine gap).

### Annual Reports — TWO NEW SOURCES FOUND

The script cited image-only Companies House scans for FY2022 and FY2023. The
Bank's own website carries **text-layer copies of both**, not previously cited:

| Year | Website URL (NEW for FY2022/FY2023) | pages | chars |
|---|---|---:|---:|
| FY2022 | `.../2023/04/Reliance-Bank-Report-and-Accounts-31-March-2022.pdf` | 54 | 186,383 |
| FY2023 | `.../2023/10/Reliance-Bank-Report-and-Accounts-2023-Final-for-website-30Oct2023.pdf` | 54 | 190,629 |

Already-cited website copies: FY2026 (71pp), FY2025 (62pp), FY2024 (64pp),
FY2021 (55pp), FY2020 (52pp) — all with text layers.

All five Companies House filings (FY2022–FY2026) confirmed image-only
(`Producer: libtiff / tiff2pdf`; 54/54/63/62/71 pages; 1 char/page). **Text
search returns nothing from those and that is not evidence of absence** — the
two figures that matter were therefore also read **visually from rendered
Companies House pages at 170 dpi**, not OCR'd, and match the website copies
digit for digit.

## 2. Where 4.50 / 7.6 / 11.5 came from — ANSWERED

They are Annual Report Strategic Report figures. Not derived, not transcription
errors, not fabricated.

| Fig | Document | Printed page | Exact wording |
|---|---|---:|---|
| 4.50% | FY2021 AR, KPI table (2021 column) | 11 | "Leverage Ratio 4.50% / 5.45%" — commentary "Capital as a % of total assets (not risk weighted)" |
| 4.5% | FY2021 AR, Capital narrative | 12 | "the Bank's Leverage Ratio (capital as a percentage of total exposures) reduced to 4.5% (2020: 5.45%)" |
| 7.6% | FY2022 AR, Strategic Report → CAPITAL | 10 | "As at 31 March 2022, the Bank's Leverage Ratio (capital as a percentage of total exposures) increased to 7.6% (2021: 4.5%)" |
| 11.5% | FY2023 AR, Strategic Report → CAPITAL | 10 | "As at 31 March 2023, the Bank's Leverage Ratio (**excluding claims on central banks**) increased to 11.5% (2022: 7.6%)" |

Also traced: 10.8% (FY2024 AR p.11), 11.0% (FY2025 AR p.14, printed "11%"),
13.3% (FY2026 AR p.15), 5.45%/6.12% (FY2020 AR p.10 KPI table + p.11 narrative).
FY2024/FY2025/FY2026 **all use the phrase "excluding claims on central banks"**.

## 3. Did the years line up? YES — but one real trap was found

Checked explicitly, because three values against three values proves nothing.

- **Pillar 3 columns are explicitly headed.** 31 Mar 2022 edition: `2022 | 2021`
  → 5.08% | 4.45%. 31 Mar 2023 edition: `2023 | 2022` → 7.90% | 5.08%. The 5.08%
  overlap across the two editions confirms the alignment. Year end is 31 March
  and stable, so FY2023 = 31 Mar 2023. No misalignment.
- **TRAP — the FY2020 Annual Report's KPI table headers are off by one year.**
  The table on p.10 is headed `2019` and `2018 (as stated)` but holds the FY2020
  and FY2019 figures. Proof, from the same document: the Capital narrative
  immediately below says "as at 31 March 2020 … 17.7% (2019: 20.2%)" while the
  table's "2019" column shows 17.7% and its "2018 (as stated)" column 20.2%; the
  p.11 narrative says "As at 31 March 2020 … was 5.45% (2019: 6.12%)". Independently
  corroborated by the FY2021 AR's KPI table (correctly headed `2021 | 2020`),
  which shows 15.7%/17.7% and 4.50%/5.45%. **The workbook's assignment
  (FY2020 = 5.45%, FY2019 = 6.12%) is correct.** Recorded so a future pass does
  not "fix" the series by one year off the table headers.

## 4. The basis question — resolved from documents

**The Annual Report series contains a real basis break; the Pillar 3 series does not.**

- Pillar 3 prints "Basel III Leverage Ratio" / "Total Basel III leverage ratio
  exposure measure". **No central-bank-exclusion line, and no UK KM1 row 14b, in
  either edition** — the Bank uses its own "Summary of Key Metrics" table, not
  the UK KM1 template. Both editions carry only the boilerplate "Changes
  effective from 1 January 2022 include revisions to the leverage ratio…".
- **Decisive denominator evidence.** Exposure measure 265,321 / 274,521 /
  267,687 (£k) for FY2021/FY2022/FY2023 against total assets 244,326 / 251,247 /
  252,188. The exposure measure *exceeds* total assets in every year (off-balance-
  sheet commitments) and never falls sharply. Central-bank balances were
  £73.9m / £91.3m / £83.3m; an exclusion would have pushed the denominator to
  roughly £191m / £183m / £184m. It did not. **The Pillar 3 series includes
  claims on central banks throughout, one continuous basis.**
- **The Annual Report series breaks at FY2021 → FY2022 in the figures, but the
  Bank's wording only catches up at FY2023.** FY2021 AR 4.50% ≈ Pillar 3 4.45%
  (same date, both including central banks — they agree). From FY2022 the two
  diverge hard: AR 7.6% vs Pillar 3 5.08%; AR 11.5% vs Pillar 3 7.90%. The
  FY2022 AR still carries the stale parenthetical "capital as a percentage of
  total exposures", but **the FY2023 AR re-presents that identical 7.6% as its
  2022 comparative under the heading "excluding claims on central banks"** — the
  Bank's own later and explicit statement of the basis. FY2022 is therefore
  placed on the exclusion row, with the FY2022 AR's conflicting parenthetical
  recorded in full on the sheet rather than suppressed.

This matches the 1 January 2022 UK framework change exactly, and vindicates the
sweep's original FY2021→FY2022 flag (+3.10pp) as the right boundary.

## 5. Final state of the sheet

`Leverage Ratio`, unit `£'000 / %`, four rows (Starling-style dual-basis layout):

| Row | FY2026 | FY2025 | FY2024 | FY2023 | FY2022 | FY2021 | FY2020 | FY2019 |
|---|---|---|---|---|---|---|---|---|
| AR — excluding claims on central banks | 13.3% | 11.0% | 10.8% | 11.5% | 7.6% | | | |
| AR — capital as % of total exposures, INCLUDING central banks (pre-2022) | | | | | | 4.50% | 5.45% | 6.12% |
| Pillar 3 — Basel III leverage ratio, including central banks | | | | 7.90% | 5.08% | 4.45% | | |
| Pillar 3 — total Basel III leverage ratio exposure measure (£'000) | | | | 267,687 | 274,521 | 265,321 | | |

No row carries two bases. No figure was derived, reconciled or back-solved.
Nothing was blanked. Overview sheet updated to match (it is a copy).

## 6. Other sheets — same untraceable-figure pattern?

Every ratio on every other sheet was grepped against all nine text-layer
documents. Result:

- **CET1 Ratio** (21.8 / 19.9 / 20.7 / 23.1 / 18.2 / 15.7 / 17.7 / 20.2) — all
  eight trace to an Annual Report. Clean.
- **LCR** (228 / 247 / 408 / 315 / 605 / 986 / 690 / 1,100) — all eight trace.
  Clean.
- **Total Capital Ratio FY2023 25.5% and FY2022 19.7% — appear in NO document.**
  They are derived (21,218/83,146 = 25.52%; 14,137/71,782 = 19.69%) from two
  Pillar 3 rows. **Unlike the leverage row, the sheet's own note already declares
  them derived**, so this is a disclosed derivation, not an untraceable figure.
  Left unchanged — no primary document proves a different value. Flagged for a
  future ruling on whether disclosed derivations are permitted at all.
- Capital amounts, RWAs, Tier 1 rows all tie to the Pillar 3 tables. Clean.

### Separate finding — sourced FY2021 comparatives are being left blank

The 31 Mar 2022 Pillar 3 discloses a full **31 March 2021 comparative column**
that four sheets currently leave blank: CET1 Resources **£11,799k**, Risk
Weighted Assets **£71,451k**, CET1 ratio **15.45%** (§2 Summary of Key Metrics,
p.3) and Total Capital **£11,953k** (§3 Capital Resources, p.3). These are
printed figures, not derivations. Not actioned here (out of this ticket's
scope, and the affected sheets' notes would need rewriting), but they are
document-proven and worth a follow-up ticket.

Note also that the Bank's two Pillar 3 tables disagree with each other on
capital: CET1 Resources 20,965 / 13,952 / 11,799 vs Total Capital 21,218 /
14,137 / 11,953. The workbook already carries both on separate sheets, which is
the correct treatment — do not reconcile.

## Rules observed

`refresh_all.py` NOT run. Test suite NOT run. No commit. No messages to other
sessions. Sheet count verified at 18.
