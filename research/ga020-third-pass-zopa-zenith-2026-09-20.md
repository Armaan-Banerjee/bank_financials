# GA-020 third-pass source check: Zopa and Zenith (2026-09-20)

This was a bounded check of the `unreached3` worklists for Zopa and Zenith, with attention to the leads in `wayfinder/gaps/ga020/NEXT_LEADS.md`. No build scripts, workbooks, or checkpoint JSONL files were changed.

## Zopa

The official [Zopa Bank Limited Pillar 3 Disclosures, 31 December 2020](https://www.datocms-assets.com/23873/1658745471-2020-zopa-pillar-3-disclosures.pdf) is available through Zopa's DatoCMS asset host and search indexing exposes its “Key ratios” table. Printed p.4 (PDF p.3) has separate 2020 and 2019 columns: CET1, Tier 1 and total capital ratios 29.5% / 25.1%; RWA £390.9m / £52.9m; leverage 38.1% / 54.3%; LCR 13,597% / 10,059%. The document's printed p.15 (“Capital composition”) also reports CET1 capital £115.4m / £13.3m. The search-indexed PDF confirms the entity is Zopa Bank Limited and says the disclosure is prepared only for that Bank (printed p.4).

Important verification limitation: the web PDF parser exposed the table text, but its page-image screenshot failed with a cache miss, and shell retrieval is blocked by DNS resolution in this environment. Therefore these figures have **not** met the project rule requiring reading figures from page images and are leads, not ingestion-ready transcriptions. The specific FY2019 leverage (54.3%) and LCR (10,059%) are already represented in `build_zopa.py` on the separate year-end/Annual Report-basis rows; do not duplicate them onto the KM1 average-basis rows. The FY2020 P3 values (£390.9m and 29.5%) differ from the currently recorded FY2020 FY2021-ARA comparative (£390.5m and 29%). Preserve the two source statements as a discrepancy; do not silently overwrite or reconcile.

For the two remaining MREL cells (FY2018 and FY2019), the worklist's prior searches already enumerate Zopa's DatoCMS folder and `cdn.zopa.com`. The FY2020 P3 remains a further official document reviewed by indexed text; it does not establish a pre-2020 edition or resolve MREL for those years. No new evidence supports reclassifying either cell.

## Zenith

The missing FY2019 cells remain unresolved. The UK bank's currently indexed [Pillar 3 page](https://www.zenith-bank.co.uk/pillar-3/) lists FY2021–FY2025, not the missing 2019 PDF. A new search route surfaced the parent's official [Zenith Bank Plc December 2019 Pillar 3 report](https://www.zenithbank.com/media/1nppdrns/pillar3-disclosures-report-december-2019.pdf). Its indexed text describes Zenith Bank (UK) Limited as a subsidiary, but supplies no separately labelled FY2019 UK-entity CET1/Tier 1/total capital ratio, RWA, leverage, LCR or MREL figure. Parent/group metrics cannot stand in for the UK entity. This route therefore produces no usable figure and does not repair the lost FY2019 UK Pillar 3 PDF.

The Zenith search result is consistent with the existing distinction: the FY2019 UK Pillar 3 edition was named in the UK bank's archived index, but its PDF remains inaccessible; FY2019/FY2020 Annual Reports were already checked for comparatives. No newly found UK-entity edition, mirror, or labelled UK-entity prudential table was identified in this pass.

## Outcome

- Zopa: no change to the FY2018/FY2019 MREL `Unreached today` cells. The FY2020 official P3 comparative table is a promising source for figures already noted above, but image verification remains outstanding; the FY2020 own-year RWA/CET1 figures conflict with the existing FY2021 Annual Report comparative and should be retained as a documented source disagreement if later verified.
- Zenith: all eight FY2019 `Unreached today` cells stay unreached; the newly surfaced parent report does not give separate UK-entity prudential figures.
- No workbook or checkpoint edits were made.

## Philippine National Bank Europe

The Bank's official [Pillar 3 Disclosures for 31 December 2016 (April 2017)](https://www.pnb.com.ph/europe/images/stories/docs/Pillar3_Disclosures_for_2016.pdf) was recovered through the indexed PDF despite the host's direct-fetch block. The 13-page report is explicitly for Philippine National Bank (Europe) Plc. It contains capital and risk-weighted-asset tables (printed pp.6-9), but its Liquidity Risk section (printed p.11) is qualitative only. Full indexed text has no leverage, LCR, Liquidity Coverage, NSFR, Net Stable Funding, or MREL matches. No ratio figures were transcribed from extracted text.

This closes four FY2016 `Unreached today` cells (Leverage Ratio, LCR, NSFR, MREL Ratio) as `Not published` in the bank's FY2016 Pillar 3. The FY2015 report had been similarly reviewed in this pass. FY2018 and FY2022 remain `Unreached today` because no usable report surfaced; FY2025 remains an unresolved retrieval state. No numerical data were added.
