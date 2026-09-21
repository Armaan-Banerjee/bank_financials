# Standard Chartered HY2026 and DBIGB 2023 Pillar 3 scope check

Checked 2026-09-21 against the two official reports supplied by the user and the corresponding bank builders.

## Standard Chartered PLC — HY2026

The HY2026 report is extensive and quarterly, but its main disclosures are Standard Chartered PLC Group figures, not Standard Chartered Bank standalone figures. The report defines “Group” as Standard Chartered PLC and its subsidiaries and says disclosures are at Group level unless otherwise specified (printed pp.3–4). The main UK KM1, OV1 and risk tables therefore do not replace Bank-basis figures.

One usable Bank-related solo-consolidation result appears in Annex 1, Table 75: Standard Chartered solo-consolidation leverage (printed p.81). At 30 June 2026 it gives a leverage exposure measure of $467,791m and ratio of 4.4%; the December 2025 comparative is $448,330m and 4.2%, matching the existing FY2025 entry. This can support an interim 2026 observation if interim columns are added, but it adds no new FY2021–FY2025 annual figure. The annex does not contain solo KM1, solo RWA, or solo LCR/NSFR tables. Table 8 (printed p.14) is Standard Chartered Bank-specific TLAC creditor ranking, not the Bank's MREL ratio. The report has no Bank solo balance sheet or P&L.

No workbook change is indicated under the current FY2021–FY2025 period and metric perimeter. Current builder treatment—use solo-consolidation data where expressly published, and do not substitute PLC Group KM1—is supported.

## Deutsche Bank UK — DB Investments (GB) Limited 2023

The supplied report is a genuine, detailed Pillar 3 report for the **DB Investments (GB) Limited UK Regulated Group (DBIGB Group)**. It explains that DB UK Bank Limited (DBUKB) is the regulated bank whose PRA disclosure obligation is met at the DBIGB Group UK consolidation-group level; that perimeter comprises DBUKB, Deutsche Trustee Company Limited, Deutsche Holdings Limited and DBIGB (printed p.4). It further states that these reports began in 2022 because the DB Group report no longer met the UK group's requirement after the Brexit transition period.

The FY2023 edition supplies the standard UK KM1 capital metrics and UK OV1 RWA breakdown for DBIGB Group, with FY2022 comparatives (printed pp.16–18), and quarterly-average LCR/NSFR information (printed pp.18–19). For example, group KM1 reports own funds of £555.107m, total RWA £510.264m and CET1 ratio 109% at 31 December 2023; the 2022 comparative is £537.779m, £681.128m and 79%. These are **group-consolidated**, not DBUKB standalone, figures.

This source was already captured in `scripts/build_db_uk_bank.py` alongside the 2024 and 2025 DBIGB reports. The builder deliberately records, but has not resolved, whether to put the four-company DBIGB Group figures into a workbook otherwise keyed to DBUKB standalone accounts. This report confirms the material available and that DBUKB's disclosure obligation is fulfilled at this consolidated perimeter; it does not by itself make those figures standalone DBUKB figures. No data were ingested or workbook cells changed in this source check.

## Schroder & Co. Limited — Schroders HY2026 Pillar 3

The target workbook entity is Schroder & Co. Limited, not Schroders plc. The repo's existing check of the parent disclosures found that the Schroders plc UK KM1 and other prudential tables are consolidated-group data, with no Schroder & Co. Limited column or block; the entity's own accounts also contain no capital ratio/RWA metrics. The new HY2026 document is an interim edition of that parent/group series, so it is not a basis to substitute group figures into Schroder & Co. Limited's workbook.

Access limitation: the supplied HY2026 PDF URL on `mybrand.schroders.com` could not be fetched by the research reader or the restricted shell session, and Schroders' public index page is client-rendered in the reader. Thus I could not directly verify the HY2026 PDF's exact template list or test for an entity-level exception. The existing repo evidence does establish that the Schroders P3 series is group-level through FY2025 and records HY2026 as the newer interim edition. No figures were added. The direct HY2026 PDF should be rechecked from a downloadable local copy if a row-level conclusion about that edition is required.

## Danske Bank A/S — Q2 2026 source index

The official investor-relations page lists a new “Additional Pillar 3 Disclosures Q2 2026” item dated 17 July 2026. The workbook target is Northern Bank Limited (trading as Danske Bank), not Danske Bank A/S. The builder's completed review of the parent's Q4 2025 disclosure workbook found Northern Bank only in the EU LI3 scope-of-consolidation list, not in any entity-specific capital template; the EU KM1 is a parent-group template in DKK. The parent disclosure therefore should not replace Northern Bank's own entity-level metrics.

Access limitation: the Q2 2026 item is served as an `.xls` file, which the web reader rejected as an unsupported content type; restricted-shell network access could not download it for local inspection. The index page confirms that the newer group workbook exists, but its contents have not been verified here. It is not treated as new Northern Bank data unless an inspectable copy reveals an explicit Northern Bank basis. No data were ingested and no workbook cells changed.

## Sources

- Standard Chartered PLC, [Half Year 2026 Pillar 3 Disclosures](https://www.sc.com/en/uploads/sites/66/content/docs/standard-chartered-plc-hy-2026-pillar-3-disclosure.pdf), printed pp.3–5, 14, 81.
- DB Investments (GB) Limited UK Regulated Group, [Pillar 3 Report 2023](https://wealth.db.com/dam/deutschewealth/location-assets/emea/uk/docs/2023-db-investments-gb-limited-pillar-3-report.pdf), printed pp.4, 16–19.
- Schroders, [Half-Year Pillar 3 2026 PDF supplied by the user](https://mybrand.schroders.com/asset/6ed82f01-b8e2-4c13-9836-9336b3620dcc/Schroders-Half-Year-Pillar-3-2026.pdf) (direct read blocked in this session); repo's prior scope evidence is in `scripts/build_schroder.py`.
- Danske Bank, [Reports and investor-relations index](https://danskebank.com/investor-relations/reports), which lists “Additional Pillar 3 Disclosures Q2 2026,” and [Q4 2025 Additional Pillar 3 workbook](https://danskebank.com/-/media/danske-bank-com/file-cloud/2026/2/additional-pillar-3-disclosures-q4-2025.xls) previously checked in `scripts/build_northern_bank.py`.
