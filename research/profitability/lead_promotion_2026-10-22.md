# Promoting the ocr_lead quarantine — 2026-10-22

40 `ocr_lead` records across 9 banks had sat outside the curated store since the
sweep. An `ocr_lead` is a **lead, not a finding**: the sweep agent found the
figure in a PDF's text layer but never rendered the page, so nobody had seen it.
`merge_sweep.py` quarantines them by design.

This pass fetched each cited document, proved it was a PDF, rendered the cited
page at 300 dpi and read it. Tool: `promote_leads.py --fetch`.

## Outcome

| | records |
|---|---|
| Lead confirmed exactly as recorded | 33 |
| **New records the leads never held** | **9** |
| Lead **refuted** | 2 |
| Still a lead (no document obtainable) | 2 |
| Recorded as `excluded` (wrong entity) | 1 |
| **Merged into the store** | **44** |

Store: **355 → 399 records, 138 → 145 banks** — every bank in the corpus now
carries at least one published-return record. Deliverable own-published column:
**181 → 205 bank-years across 75 banks** (was 72). Every one of those 205 cells
is `300dpi` or `press_release`; none is a lead.

`audit_gaps.py`-style census figures for the research deliverable, from
`coverage_ceiling.py`: ANY-return-any-source stays **710 of 725** and
unreachable stays **15**. The gain is in *evidence quality and own-published
coverage*, not in reachability — those bank-years already had a computed ratio.

## What each bank yielded

**BANK OF AFRICA UK** — 4/4 confirmed. Printed p.25 of AR2024. ROE FY2024
2.66% (FY2023 −19.90%), ROA FY2024 0.65% (FY2023 −3.96%), both on a post-tax /
average denominator — the project's own basis.

**BRITISH ARAB COMMERCIAL BANK** — 5/5 confirmed on one five-year chart,
printed p.6 of AR2025. "Return on initial invested capital" FY2021–FY2025
12.0 / 13.8 / 26.3 / 25.9 / 21.5%. **Not ROE**: the denominator is called-up
share capital plus the capital redemption reserve, so retained earnings are
excluded and the ratio runs far above a true ROE.

**ICBC (LONDON) PLC** — 4/4 confirmed, printed p.3 of AR2025. ROE 7.55%
(2024: 7.59%), RoA 2.52% (2024: 2.39%), post-tax over total average
shareholder funds / total average assets. The bank reports in **USD**; the
ratio is unit-free because both sides are USD, but the underlying amounts are
not sterling.

**SECURE TRUST BANK** — 12/12 confirmed, all in one table on printed p.197 of
AR2025. The bank prints **four** return-on-equity measures side by side (total
/ total adjusted / continuing / continuing adjusted); they are stored as four
separate claims. Basis difference worth carrying: average equity is the
average of **monthly** balances, where the computed ratio uses a two-point
opening/closing average.

**WEATHERBYS** — 2/2 confirmed, and the definition the leads lacked.
**The definition changed between editions**: FY2024's 20% is struck on profit
*before exceptional items and tax* (£26.7m); FY2023's 34.2% is struck on
profit *before tax* (£33.1m) with no exceptional-items adjustment. Both are
recorded as printed and are not reconciled. Neither is comparable with the
post-tax computed ROE.

**GHANA INTERNATIONAL BANK** — 2 confirmed **+ 3 new**. The quarantine held
FY2024 and FY2025; rendering the Financial Highlights page (printed p.04 of
AR2025) produced the bank's whole five-year series: FY2021 **−7.2%**, FY2022
**−2.1%**, FY2023 1.9%, FY2024 2.5%, FY2025 3.1%. The two oldest print in
parentheses — accounting notation for a negative — and are stored negative.
The report states no denominator basis, so `definition` is null rather than
guessed.

**ARAB BANK EUROPE (Europe Arab Bank plc)** — 4 confirmed **+ 4 new**, 2 still
leads. The bank's live site no longer serves its reports, so both editions came
from real Wayback captures and were rendered locally. FY2024 edition (printed
p.6): ROE 5.25% / 3.65%, ROA 0.68% / 0.50%. FY2022 edition (printed p.9), found
while chasing the missing document, adds two further in-window years.
**The label changed between editions**: FY2022 prints "Return on **opening**
equity" (FY2022 4.14%, FY2021 0.26%) where FY2024 prints plain "Return on
equity". Neither document says whether the basis changed with the label, so the
two labels are stored as separate series, not joined. FY2025's 4.82% / 0.61%
remain leads — no FY2025 report exists in any reachable source.

**HAMPSHIRE TRUST BANK — the quarantine was wrong to write this bank off.**
It recorded only the Group series (FY2022 11.9%, FY2023 14.1%, FY2024 14.9%)
and marked the bank unpromotable on entity grounds. The render shows the report
prints **Group and Bank columns side by side**, and the Bank column is the
workbook's perimeter: **FY2024 15.2%, FY2023 23.1%**, post-tax over average
equity — directly comparable with the computed ratio, and in no prior source.
The Group figure is kept as an `excluded` record so it is never substituted
into a Bank-only cell. Bank profit exceeds Group profit because the Bank column
includes dividends received from subsidiaries (11.0; 2023: 27.5 £m).

**EFG PRIVATE BANK — both leads refuted.** The leads recorded "Return on
assets = 9.0%" (FY2024) and "10.5%" (FY2023). The page prints **94.0** and
**105.0**, and the bank's own footnote defines the measure as *"operating
income over the simple average of opening and closing **AUM** booked in the
Company"* — operating income over assets under management, not profit over
balance-sheet assets. It is not ROA in this project's sense. The printed unit
is genuinely ambiguous (the column header says "GBP millions" but the same
column carries "Cost income ratio 83%"), and that ambiguity is **recorded, not
resolved**: 94.0 is most consistent with basis points, but that is an inference
and is not stored as a value. Recorded as `excluded` so nobody reads a decimal
out of it into an ROA cell.

## Why the originals stay quarantined

Batches 1–7 still carry all 40 `ocr_lead` records and `merge_sweep.py` still
reports them as quarantined. That is deliberate: the lead is the record of what
was believed before anyone looked, and for EFG and Hampshire Trust the
difference between the lead and the render is the finding. The promoted
records live in `sweep/batch_8_promoted_leads.jsonl`.

## Two bugs this pass found in its own tooling

1. **Render filename collision.** The first run keyed renders on bank + page,
   so Weatherbys' 2023 and 2024 editions — which both print the figure on PDF
   p.8 — wrote to the same path and the second silently overwrote the first.
   Same path, no error, one document lost. The stem now carries the document
   index.
2. **`URL_RE` required a `.pdf` extension.** Secure Trust serves its 206-page
   annual report from a path ending `...reports-and-accounts-2025-final-483796420288`
   with `Content-Type: application/pdf`. The extension-anchored regex skipped
   it and the tool reported "no URL cited in any of its 12 leads" when the
   citation was complete and correct. The regex now takes any http(s) URL and
   lets the magic-byte check decide — the only test that was ever load-bearing.

## Things seen that are worth not re-learning

- **A citation's "PDF p.N" was one short of the true PDF index in both cases
  where it appeared** (Bank of Africa, BACB). The *printed folio* in those
  citations was right. Trust the folio, verify the index.
- **`pdftotext` returning nothing does not mean a scan.** EFG's PDF is a Word
  export re-processed by PDFKit.NET: born-digital, renders perfectly, but its
  text layer yields only bullet glyphs. OCR was used for **navigation only**;
  every figure was read off the 300 dpi render.
- **The Internet Archive answered one CDX query with "Temporarily Offline"**
  while serving another normally. That is an instrument outage, not evidence
  of absence; the retry found Europe Arab Bank's reports immediately.
