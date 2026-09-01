# Goldman Sachs International Bank revisit

## Investigation status

The official Goldman Sachs disclosure index is accessible. Its GSG UK archive links to quarterly Pillar 3 disclosures for 2021 onward:

- https://www.goldmansachs.com/disclosures
- https://www.goldmansachs.com/disclosures/european-disclosures-archive

The PDF links use Goldman Sachs' redirect wrapper when requested without a trailing slash. The underlying PDFs were retrievable by appending a trailing slash to the official PDF URL, for example:

- https://www.goldmansachs.com/disclosures/gsguk-q4-2025-pillar-3.pdf/
- https://www.goldmansachs.com/disclosures/gsguk-q4-2024-pillar-3.pdf/
- https://www.goldmansachs.com/disclosures/gsguk-q4-2023-pillar-3.pdf/
- https://www.goldmansachs.com/disclosures/gsguk-q4-2022-pillar-3.pdf/
- https://www.goldmansachs.com/disclosures/gsguk-q4-2021-pillar-3.pdf/

## Defensible GSIB breakout recovered

The prior conclusion that only parent-consolidated data was available is no longer correct. The annual GSG UK Pillar 3 PDFs explicitly include `GSIB` columns or tables alongside `GSGUK` and `GSI`.

- FY2021: the regulatory capital table explicitly presents GSGUK, GSI and GSIB capital and capital ratios; the report also contains GSIB RWA, LCR and leverage disclosures.
- FY2022: the Key Metrics table explicitly covers GSGUK, GSI and GSIB, and separate GSIB RWA, LCR and NSFR tables are present.
- FY2023: the Key Metrics table explicitly covers GSGUK, GSI and GSIB, with separate GSIB RWA, LCR and NSFR tables.
- FY2024: the Key Metrics table explicitly covers GSGUK, GSI and GSIB, with separate GSIB RWA, LCR and NSFR tables.
- FY2025: the Key Metrics table explicitly covers GSGUK, GSI and GSIB, with separate GSIB RWA, LCR and NSFR tables.

The reports also identify GSIB in the glossary as Goldman Sachs International Bank. This is an entity-level breakout within the GSG UK disclosure, not an unsupported substitution of GSG UK consolidated figures.

## Scope and caveats for a future rebuild

- Preserve the entity-level GSIB basis and do not use the GSGUK column where a GSIB column/table is available.
- Use annual December values from the Q4 report for consistency with the existing annual workbook. The reports also contain interim observations, but those would require a deliberate 14-sheet/interim layout decision.
- MREL appears to be disclosed primarily for GSGUK in the reviewed reports; do not infer a GSIB MREL value unless a GSIB-specific table or explicit statement is found.
- FY2021 uses an older table structure than FY2022–FY2025; map only fields that are explicitly labelled and document any unavailable metric.
- The reports are denominated in USD millions. Retain the existing builder's established GBP/USD conversion methodology if the workbook is rebuilt.

## Implemented status

The Goldman-specific builder and workbook have now been updated from the recovered GSIB breakout. Annual December GSIB values are populated for FY2021-FY2025 for CET1 capital, Tier 1 capital, Total capital, total RWA, leverage exposure, CET1/Tier 1/Total capital ratios, leverage ratio and LCR. NSFR is populated for FY2022-FY2025; FY2021 is explicitly marked unavailable because the FY2021 report does not show a GSIB NSFR table. MREL remains explicitly unavailable in every year because no GSIB-specific numeric value was shown.

The workbook continues to use the entity-level GSIB basis and converts USD-million amounts to GBP at the established year-end spot rates; reported percentages are retained as reported. The stale source and overview notes saying that the GSG UK source was inaccessible were removed.
