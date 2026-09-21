# Santander Financial Services: Annual Report prudential disclosures

Checked 2026-09-21 against Santander Financial Services plc's official 2024 Annual Report, prompted by the discovery that the report contains Pillar 3-like information.

## Finding

The FY2024 Annual Report contains selected entity-level prudential disclosures, so describing SFS as publishing “no Pillar 3 at all” is too broad if that means it publishes no prudential information. It does not, however, contain a standalone Pillar 3 report or a UK KM1 template. The appropriate classification is: **selected prudential disclosure in the Annual Report; no standalone SFS Pillar 3/KM1 publication.**

The report's Risk review states that SFS is subject to PRA capital requirements on a standalone basis (printed p.37). It reports LCR of 186% and NSFR of 149% (printed p.36), and an audited SFS regulatory-capital table with FY2024 CET1 capital £266m, AT1 £50m, and total regulatory capital £316m (printed p.38; FY2023 comparatives are included). It says that the main capital-risk metrics include the CET1 ratio but does not give the ratio as a figure. For CRD IV exposure measurement, it directs readers to Banco Santander's Pillar 3 report (printed p.37).

The report therefore supplies useful prudential data already reflected in SFS's capital/liquidity metrics, but no KM1 template, RWA breakdown, or standalone SFS capital-ratio figures. It does not alter the workbook's no-KM1 / no-standalone-Pillar-3 classification; it narrows the wording and is not a newly discovered source for a missing KM1 or RWA figure.

## Repo bookkeeping

Updated `scripts/build_santander_financial_services.py` and `wayfinder/km1/tickets/KM1-026.md` to distinguish “no standalone Pillar 3/KM1” from “no prudential disclosure.” The existing entity capital amounts already cite SFS Annual Reports. No numeric workbook cells were changed by this finding.

## Source

- Santander Financial Services plc, *2024 Annual Report*, Risk review, printed pp.36–38: [official PDF](https://www.santander.co.uk/assets/s3fs-public/documents/Santander%20Financial%20Services%20plc%202024%20Annual%20Report.pdf).
