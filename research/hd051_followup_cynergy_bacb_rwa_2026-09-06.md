# HD-051 follow-up: Cynergy Bank and BACB RWA gaps

Date: 2026-09-06

## Cynergy Bank FY2020

The bank's own [Pillar 3 Disclosures for the year ended 31 December 2020](https://assets.ctfassets.net/xzmqg68ot16t/6UrOmWW2bF1uUTP86Lupt7/f5bdc5b8300ed876a513bb2232c3b4f8/pillar-3-disclosures-2020.pdf), p.25, contains a previously omitted “Summary of On Balance Sheet Credit Risk Exposure”. The table reports RWA (£m) by exposure class:

| Exposure class | Source RWA (£m) | Workbook (£'000) |
|---|---:|---:|
| Central governments or central banks | – | 0 |
| Institutions | 9 | 9,000 |
| Corporates | 401 | 401,000 |
| Retail | 74 | 74,000 |
| Secured by mortgages on immovable property | 638 | 638,000 |
| Exposures in default | 30 | 30,000 |
| Items associated with particularly high risk | 24 | 24,000 |
| Other items | 19 | 19,000 |
| **Total credit-risk RWA** | **1,195** | **1,195,000** |

The same source separately gives total eligible capital £182,844k and the workbook's total RWA £1,294,931k. The new table is therefore recorded as a separate credit-risk section, not incorrectly used as the complete Pillar 1 total. The workbook was rebuilt and `verify_workbook.py` completed with the repository's existing cash-flow heuristic warnings only.

## British Arab Commercial Bank FY2024–FY2025

BACB's [FY2024 Pillar 3 disclosure](https://files.bacb.co.uk/production/files/BACB_Pillar3_YE2024web-05.pdf?dm=1748534514), section 4.2 (p.20), was checked directly. The report describes the risk-weighted-assets framework and provides aggregate regulatory metrics, but does not provide an exposure-class RWA table. BACB is a single UK entity with no prudential consolidation (p.5), so there is no alternate subsidiary table to substitute.

The bank's FY2025 own Pillar 3 source, cited in the workbook as [BACB_Pillar3_YE2025web-03.pdf](https://files.bacb.co.uk/production/files/BACB_Pillar3_YE2025web-03.pdf), was checked for the corresponding RWA section. It likewise provides aggregate capital/RWA metrics and no exposure-class breakdown. The FY2024–FY2025 blanks remain a confirmed non-disclosure at this granularity; no workbook change was made.

