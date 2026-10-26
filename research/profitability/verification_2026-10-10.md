# 300 dpi verification pass — 2026-10-10

Cleared the OCR-lead backlog in `published_returns.jsonl`. **9 figures
verified, 0 `ocr_lead` records remaining.** Renders were made at 300 dpi into
the session scratchpad and are deliberately NOT committed: the record is the
document and page cited below, from which any render can be reproduced.

Standard applied: `pdftoppm -r 300`, image read directly. OCR was used only to
locate the page.

## United Trust Bank — all six years, each from its OWN edition

| year | value | own-edition page | footnote |
|---|---|---|---|
| FY2020 | 15.9% | `utb_2020.pdf` PDF p.4 (printed 4) | 2 |
| FY2021 | 20.2% | `utb_2021.pdf` PDF p.3 (printed 3) | 3 |
| FY2022 | 21.7% | `utb_2022.pdf` PDF p.3 (printed 04) | 3 |
| FY2023 | 23.9% | `utb_2023.pdf` PDF p.4 (printed 04) | 3 |
| FY2024 | 20.1% | `utb_2024.pdf` PDF p.3 | 2 |
| FY2025 | 14.1% | `utb_2025.pdf` PDF p.3 | 2 |

Verifying each from its own edition rather than from one page of comparatives
was the point: **the own-edition rule applies to a published ratio exactly as
it applies to a transcribed figure.** Every value also cross-agrees with the
later editions' comparative columns, which is corroboration, not the source.

Footnote wording is IDENTICAL in all six: *"Return on Equity is calculated net
of the coupon paid on contingent convertible securities"*. The FY2020 and
FY2021 pages carry the entity name "UNITED TRUST BANK LIMITED" in the header,
which is what rules out UTB Partners Plc.

**New, previously unrecorded: FY2019 = 16.2%**, printed as the FY2020
edition's comparative. Outside the FY2021-FY2025 window so it does not reach
the deliverable grid.

## Coutts & Company — footnote (1) read for the first time

`coutts2025.pdf` PDF p.3 (printed 3), "Performance highlights and key metrics".
RoE **17.3%** (2024 **13.5%**). Footnote (1), verbatim:

> RoE is calculated using annual profit for the period divided by the average
> owner's equity, which at 31 December 2025 was £1.5 billion (2024 - £1.5
> billion).

**That is our definition.** Coutts is so far the only bank whose published
figure is directly comparable with the computed column, which is why
`comparable_with_computed` exists as a field. Ours 17.03% against their 17.3%;
259/0.173 implies £1,497m against their stated "£1.5 billion", so the residual
is denominator precision and the composition of "owner's equity", not basis.
Same table confirms: total income 990, operating profit before tax 346, tax
charge (87), profit for the year 259.

## Al Rayan Bank — definition now the bank's own words

`ar25.pdf` PDF p.9 (printed 8), "Key financial performance indicators (KPIs)".
Return on equity **10.47%** (2024 **11.40%**). The table carries a "Basis of
Calculation" column, so this is stated rather than inferred:

> The ratio of profit for the year (before tax) to average equity, expressed
> as a percentage.

Same page: PBT £23.59m, PAT £17.68m, cost:income 57%, CET1 15.41%, LCR 598%.

## Navigation recipe, worth reusing for the remaining sweep

These filings are scans with **no text layer at all** — `pdftotext` returns
zero bytes on every page. A grep that finds nothing is therefore NOT evidence
that a bank publishes no return, and treating it as such would have produced a
corpus-wide false negative. The working method:

1. render candidate pages at 150 dpi,
2. `tesseract` them purely to locate the KPI page,
3. render that one page at 300 dpi and read the image.

The KPI page was PDF page 3 or 4 in all six United Trust editions.
