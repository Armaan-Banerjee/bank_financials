# HD-022 deep-audit follow-up (2026-09-06)

## Philippine National Bank Europe

The renewed check found that the Bank's historical document host still serves the
FY2015 and FY2016 Pillar 3 disclosures, contrary to the earlier ticket conclusion
that those years were unobtainable:

- [FY2015 Pillar 3 disclosure](https://www.pnb.com.ph/europe/images/stories/docs/Pillar3_Disclosures_for_2015.pdf), pp. 5–8: Total Capital/Tier 1 £11,197k; the report uses the older Basel II/BIPRU framework and does not state a CET1 ratio.
- [FY2016 Pillar 3 disclosure](https://www.pnb.com.ph/europe/images/stories/docs/Pillar3_Disclosures_for_2016.pdf), pp. 5–9: Total/CET1/Tier 1 capital £11,228k; CET1 ratio 92.23%; RWA components credit £7,635k, market £351k, operational £4,188k; total £12,174k.

The build script and workbook were updated with these values. FY2015 remains blank for
CET1 and capital ratios because the source does not disclose those modern measures.
FY2018, FY2020–FY2022 remain self-skipped after the live-host and Wayback checks.

## Weatherbys Bank

The official [FY2020 Pillar 3 disclosure](https://www.weatherbys.bank/app/uploads/2021/08/Pillar3-2020.pdf), pp. 13–14, explicitly reports FY2019 comparative liquidity metrics in Table 10: LCR 586% and NSFR 207.6%. These were previously blank and are now populated. No FY2019 capital/RWA/leverage figures are supplied by that comparative table, so those remain blank.

Both workbooks were rebuilt and `verify_workbook.py` completed successfully. The
remaining verifier warnings are the known historical cash-flow rounding/source-footing
warnings documented in the Weatherbys build notes.
