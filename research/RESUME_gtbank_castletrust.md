# RESUME — GTBank UK + Castle Trust (2026-09-15)

Scratchpad PDFs: `/private/tmp/claude-501/-Users-armaan-code-katalysis/20f20984-c24d-413e-b487-68c0d0793341/scratchpad/pdfs/`

## Status

- [x] URL verification (all 9 URLs return `%PDF`)
- [x] **GTBank UK — DONE**, script edited and rebuilt (18 sheets). See below.
- [x] **Castle Trust — DONE**, script edited and rebuilt (18 sheets). See below.

## GTBank UK — completed 2026-09-15

Rebuilt `banks/GUARANTY TRUST BANK UK FINANCIALS.xlsx`, 18 sheets.

The FY2025 column and the FY2023 Pillar 3 citation were ALREADY in the script from an
earlier pass today; all FY2025 figures re-verified against the primary PDF and found correct
(Table 2 key metrics, Table 4 available capital 54,604, Table 5 MCR 7,857/22/4,027/11,906).

### New cells written
- **NSFR FY2022 = 253%** (ASF 214,036 / RSF 84,527, FY2023 edition's comparative column).
  The FY2022 edition never mentions NSFR at all. Previously blank.
- **Total RWAs FY2023 restated row = 108,387** (FY2024 edition), alongside the
  as-first-published 105,275.
- **CET1 / Tier 1 / Total Capital Ratio FY2023 headline changed 32.30% -> 32.34%** (the
  FY2023 report's own table), with 32.30% kept on a restated row.
- **Leverage FY2023**: headline changed 8.30% -> **8.29%** (FY2023 report s.7.6, shows its
  working: 39,390,993 / 475,263,939). 8.30% kept on a restated row (FY2024/FY2025 editions
  restate footings to 474,761,920). Third row added for the FY2023 KM table's **6.00%**.
- LCR note corrected: FY2023 HQLA is 230,533 in the FY2023 report (197,710 is the FY2024
  restatement).

### Verified against primary, unchanged
Tier 1 / Total capital 39,391 ('000; s.7.6 gives exact GBP39,390,993), CET1 row printed as
37,000 (known share-capital error), RWA 105,275, LCR 250%, NSFR 310% (194,572/62,864),
buffers 2.50%/2.00%, FY2022 comparatives 187,034 / 20.68% / 274% / 4.38%.

### Deliberately NOT written
**FY2023 RWA breakdown.** The FY2023 Pillar 3 publishes NO RWA split by risk type anywhere:
s.6.4 "Risk-Weighted Assets" (p.15) is prose only, the KM table gives one aggregate, and the
only category-level figures in the document are capital requirements (s.7.3 p.17:
5,712 / 13 / 2,643). So the "disclosed breakdown" the task expected does not exist. Recorded
in the sheet's sources note, including the finding that the x12.5 identity DOES reconcile
exactly on the FY2024 edition's restated basis (8,671 x 12.5 = 108,387.5 vs 108,387) but not
on the original (8,368 x 12.5 = 104,600 vs 105,275) — left out because adding it would mix
the restated basis into a column whose Total RWA row is as-first-published.

Second FY2023 copy `GTBUK-Pillar-3-2023.pdf` recorded in the script as `P3_2023_ALT_URL`:
identical content, full numeric diff of extracted text shows no differing value; 27 pages
vs 26. All page refs are to the 26-page edition.

## URL verification (done)

GTBank UK — all live:
| file | bytes |
|---|---|
| `GTBank-UK-Pillar-3-2023.pdf` | 513,082 |
| `GTBUK-Pillar-3-2023.pdf` (second copy) | 592,553 |
| `GTBank-UK-Pillar-3-Disclosure-2025.pdf` | 1,017,116 |

Castle Trust — all six live under `https://www.castletrust.co.uk/wp-content/uploads/`:
| file | bytes | md5 |
|---|---|---|
| `fy-30_sept-2025-ctb-pillar-3-disclosures.pdf` | 1,907,264 | a41f3330… |
| `fy-30_sept-2024-ctb-pillar-3-disclosures.pdf` | 1,434,534 | 284d09c5… |
| `fy-30-sept-2023-ctb-pillar-3-disclosures.pdf` | 1,426,032 | 23100e95… |
| `fy-30-sept-2022-ctb-pillar-3-disclosures.pdf` | 1,263,921 | 40e5026a… |
| `fy-30-sept-2021-ctb-pillar-3-disclosures.pdf` | 1,743,521 | ec309419… |
| `fy-30-sept-2020-ctb-pillar-3-disclosures.pdf` | 1,559,393 | 0e59bc33… |

`2025/05/Pillar-3-Document.pdf` md5 `284d09c5…` = **byte-identical duplicate of the FY2024
file**. Not a separate edition.

---

## Castle Trust — completed 2026-09-15

Rebuilt `banks/CASTLE TRUST CAPITAL FINANCIALS.xlsx`, 18 sheets.

### The FY2023 URL is NOT a soft-404 any more
The script already cites `fy-30-sept-2023-ctb-pillar-3-disclosures.pdf`, which fetches a real
1.4MB PDF with a text layer whose cover and scope both read "30 September 2023". An earlier
pass today must have already replaced the bad URL. All five cited URLs re-verified.

### Entity determination — BANK column, confirmed across all six editions
- Cover "Registered No: 12161224" = Castle Trust **Holdings** Ltd, the publisher — not the
  basis. The closing legal line of the FY2021/FY2022/FY2024/FY2025 editions reads "Castle
  Trust Bank means Castle Trust Capital plc… company number **07454474**", i.e. the
  document's own "the Bank" IS our workbook entity.
- **Separate Bank and Group presentations in every edition**, in two formats:
  - FY2022–FY2025: two full KM1 tables, "Key Metrics for the Group" (p.5) and "Key Metrics
    for the Bank" (p.6). FY2025 adds "Overview of RWEAs for Group/Bank" (p.7).
  - FY2020–FY2021: main body Group-only; Bank confined to "Appendix 4. Bank Disclosures".
    FY2021 Appendix 4: "capital reporting disclosures for Castle Trust Capital plc ('the
    Bank') as a **standalone solo legal entity**."
- The script uses the Bank column in every year. Verified figure-by-figure against all six
  primaries; every existing value was already correct.
- **No Holdings-basis figure is in any sheet.** Group values (never used): FY2025
  114,327/792,429/14.43%; FY2024 105,358/667,960/15.77%; FY2023 99,699/592,678/16.82%;
  FY2022 92,572/530,968/17.43%; FY2021 85,310/494,624/17.25%; FY2020 81,994/477,452/17.17%.
- Basis caveat inside the Bank column: FY2020's Bank figures also incorporate Castle Trust
  Capital Management Ltd and Castle Trust Direct plc; FY2021 onward is CTC plc solo. FY2020
  is outside the window so no cell is affected.

### New material written
- `FY2021` cross-edition divergence now carried on labelled second rows on CET1 Capital,
  CET1 Ratio, Tier 1 Capital, Tier 1 Ratio, Total Capital, Total Capital Ratio, Leverage
  Ratio: FY2021 edition Appendix 4 says **71,677 / 20.0% / 11.1%**; the FY2022 edition's
  FY2021 comparative restates to **71,644 / 19.94% / 11.07%**. RWA (359,249) and leverage
  exposure (647,358) are identical in both.
- `ENTITY_BASIS_NOTE` with the verbatim scope quotes, in every Pillar 3 sheet's citation.
- `URL_PROVENANCE_NOTE`: the `30_sept` vs `30-sept` separator split (FY2020–23 hyphen,
  FY2024–25 underscore), all six verified `%PDF`, and `2025/05/Pillar-3-Document.pdf`
  recorded as a byte-identical duplicate of FY2024.
- `P3_2020_URL` added as a recorded sixth edition (outside the FY2021–FY2025 window).

### Deliberately NOT written
- FY2020 column (outside the workbook's five-year window, and on a different Bank basis).
- FY2022/FY2023 RWA breakdown — re-confirmed absent (both documents are 8 pages, KM1 only).
- SDDT: existing note verified correct. Rule 3.1 starts 06/01/2026; the only gap year is
  FY2021 (y/e 30 Sep 2021), four years earlier. No year marked exempt.
