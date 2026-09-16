# GIB UK — FY2020/FY2021 Pillar 3 recovery from the truncated Wayback captures

Started 2026-09-16. This SUPERSEDES the "FY2020 is permanently unsourceable"
conclusion in `research/RESUME_gib_comparatives.md` and the "no working form
exists" conclusion in `research/RESUME_linkrot_2b.md`. Both were wrong: the
1,048,576-byte truncation destroys only the PDF cross-reference table (which
lives at the END of the file), not the page objects.

## Step 1 — recovery: DONE, reproduced exactly

```
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
curl -sSL -A "$UA" -o raw.pdf "https://web.archive.org/web/<TS>id_/https://gibam.com/assets/<FILE>"
gs -o fixed.pdf -sDEVICE=pdfwrite raw.pdf
```

| Year | Capture | Raw bytes | md5 (raw) | Rebuilt bytes | Pages |
|---|---|---|---|---|---|
| FY2020 | 20220518000354 / `2020-GIBUK-Pillar-3_Final.pdf` | 1,048,576 | `edfe2438dbff06fdc617e6a38efb6059` | 795,035 | **38** |
| FY2021 | 20230329132856 / `2021-GIBUK-Pillar-3_Final.pdf` | 1,048,576 | `32d6206989581714144f61ffc6982ab5` | 697,523 | **30** |

Ghostscript emits `no startxref token found` / `xref table was repaired` /
`error reading a stream` and completes. Page counts and byte counts match the
brief exactly.

Covers:
- FY2020 p.1 — "GULF INTERNATIONAL BANK (UK) LTD / Basel II Pillar 3 Disclosures / 31 December 2020"
- FY2021 p.1 — "GULF INTERNATIONAL BANK (UK) LTD / Pillar 3 disclosures / 31 December 2021"

Both are the UK entity. Neither is Bahrain B.S.C., KSA or Abu Dhabi.

## Step 2 — recovery-loss check: NOTHING LOST

Every page has extractable text (`pdftotext -layout`); zero zero-length pages
in either document.

**FY2020.** Front matter numbered i/ii/iii on PDF pages 1-3; body numbering
resumes at 4 and runs **printed page N = PDF page N** all the way to 38. The
TOC's last entry is "10.6 Material Risk Takers ... 38"; PDF page 38 is printed
page 38 and carries §10.5 (aggregate remuneration table) and §10.6 in full,
ending on the document's own closing paragraph. **Complete.**

**FY2021.** Cover unnumbered; **printed page N = PDF page N+1**. TOC's last
entry is "6.6 Material Risk Takers ... 28" = PDF p.29; PDF p.30 = printed p.29
carries the tail of §6.6 and ends on its closing paragraph. **Complete.**

No table straddles a damaged region — the damage is confined to the trailing
xref, which carries no content.

One genuine legibility defect, NOT caused by the truncation: FY2020 printed
p.16, the caption under §4.5 and the two buffer sub-headings in §4.6, render as
garbled non-Latin glyphs (a broken font cmap in the original). The §4.6 buffer
figures themselves are in plain prose and legible. No figure used in this
workbook comes from the garbled text.

## Step 3 — what the FY2021 edition says about FY2020 (the big finding)

The FY2021 edition carries a **full prior-year (2020) comparative column**, on
the CRR/CRD V basis. It disagrees with the FY2020 edition's own Basel II-era
figures on capital, capital ratio and leverage, and it supplies FY2020 NSFR and
a FY2020 CVA RWA that the FY2020 edition does not disclose at all.

FY2021 edition printed p.6 (PDF 7), "Key ratios", 2020 column ($'000):
CET1 = Tier 1 = Total capital **378,549**; RWEA **1,482,468**; all three ratios
**26.04%**; leverage exposure **10,426,834**; leverage ratio **3.63%**.

FY2021 edition printed p.23 (PDF 24), §4.1/4.2 own-funds reconciliation, 2020
column: Total equity 392,596 − pension asset net of DTL 13,932 − intangibles 0
− prudent valuation adjustment 115 = **CET1 378,549**. Ties exactly, and the
392,596 ties to this workbook's own Balance Sheet Total equity for FY2020.

FY2021 edition printed p.24-25 (PDF 25-26), §5.2 Pillar 1 capital requirements,
2020 column ($'000 RWA): credit and counterparty risk **1,206,179**; market
risk **142,838**; operational risk **128,538**; CVA risk **4,913**; total
**1,482,468**. Four components sum to the total EXACTLY.

FY2021 edition printed p.7 (PDF 8), quarterly liquidity table, 2020 row:
Q4 2020 average LCR **291.28%**, average liquid assets buffer **6,237,113**,
average outflows 3,085,596, average inflows 944,309, average net flows
**2,141,287**; NSFR **103.23%**, ASF **10,463,760**, RSF **10,136,594**.

## Step 4 — FY2020 edition's own figures, re-verified

All already on the sheets; all confirmed, with two page references corrected.

- §3.1 p.13: Total regulatory capital $393m (Tier 1 250 + 143, no Tier 2).
- §4.1 p.14: credit risk RWA 1,206 ($m); §4.2 p.14: market risk RWA 143.75;
  §4.3 p.15: operational risk capital requirement $10.3m.
- §4.5 table on **p.16** (the script said p.15 — §4.5's heading is on p.15, the
  table overleaf): Total RWAs 1,482; Capital base 393; Tier 1 393; Tier 1 ratio
  26.48%; Total Capital ratio 26.48%.
- §5.3 p.27: Liquidity Buffer 5,860; Total Net cash outflows 2,019; LCR excl.
  PRA Scalar 290% (footnote: 153% incl. a 5% PRA Scalar add-on). Stated "as
  reported to the regulator **as at 31 December 2020**" — point-in-time.
- §7 table on **p.35** (the script said p.34 — §7's heading is on p.34): Total
  assets 10,463 − SFT adj 1,928 + derivative add-ons 25 + other −35 = exposure
  8,524; Tier 1 393; Leverage Ratio **4.61%**.
- Confirmed absent by full-text search: no NSFR ratio (only a forward-looking
  "binding NSFR measure of 100%" mention), no MREL of any kind, no CVA, no
  "CET1" by name.

## Step 5 — edits to `scripts/build_gulf_international_bank_uk.py`

STATUS: DONE. See the script. Summary:
1. CET1/Tier 1/Total Capital sheets — added a labelled FY2020 row 378,549.
2. CET1/Tier 1/Total Capital Ratio sheets — added a labelled FY2020 row 26.04%.
3. Total RWAs — added a labelled FY2020 row 1,482,468.
4. Leverage — added labelled FY2020 rows 10,426,834 / 3.63%.
5. LCR — added labelled FY2020 Q4-average rows 6,237,113 / 2,141,287 / 291.28%.
6. NSFR — FY2020 **filled** (was blank) at 10,463,760 / 10,136,594 / 103.23%,
   same Q4 basis as the FY2021 figures already on that sheet.
7. RWA Breakdown — added a labelled FY2020 restated block; the previously
   flagged $3.5m unexplained gap is now EXPLAINED and closed.
8. Citation notes reconciled into one account (`P3_CAPTURE_NOTE`), replacing
   the contradictory `P3_COMPARATIVE_NOTE` + `P3_CAPTURE_INTEGRITY_NOTE`.
9. Overview note updated (Overview is a copy); Overview NSFR row gains FY2020.
10. `P3_2020_URL`/`P3_2021_URL` converted to the `id_` playback form, reversing
    the "do not convert" decision in `RESUME_linkrot_2b.md` — that rested on the
    files being dead, and `id_` is the form the recovery recipe needs.
11. Page references corrected: capital-adequacy table is on printed p.16 (not
    p.15 — §4.5's heading is on p.15, the table overleaf); leverage
    reconciliation table is on printed p.35 (not p.34, same pattern).
12. LCR note: the FY2021 edition's own Q4 2021 "Average net flows" is
    $1,403,343k, identical to the FY2022 edition's KM1 row 16 figure already on
    the sheet, and its Q4 outflows/inflows match KM1 UK 16a/16b exactly. The
    earlier agent's caption hesitation is resolved and recorded.
13. Row heights raised to 409 (Excel's maximum) on every sheet whose citation
    grew, and metric `note_height` 60 -> 200. The Pillar 3 citation is now
    ~12,700 characters, so even at the maximum the cell cannot display it all
    at once — the text is complete, only the default display is short.

Rebuilt with `python3 scripts/build_gulf_international_bank_uk.py`; **18 sheets**.
No commit made. `refresh_all.py` and the test suite were NOT run, per brief.

## Rules honoured

- Nothing derived or back-solved. Every figure added is printed in a document.
- No figure overwritten. Every disagreement is on its own labelled row.
- FY2021 leverage 3.52% (as reported) and 7.06% (restated excl. central bank
  claims) remain on separate rows. The recovered FY2021 edition prints 3.52%
  at printed p.6, which **confirms** the as-reported row and does not touch the
  restated one.
- Entity basis: gib.com's many Pillar 3 PDFs are Bahrain/KSA/Abu Dhabi and stay
  rejected.

## Known defect found but deliberately NOT touched (out of scope)

`stock()`/`flow()` divide $'000 inputs by the FX rate and then by 1000, so every
converted figure in this workbook is in £ MILLIONS while labelled `£'000` — a
1000x labelling error affecting every sheet, not just FY2020. Pre-existing and
workbook-wide. New rows added here follow the same convention so they stay
consistent with their neighbours. Needs its own ticket.
