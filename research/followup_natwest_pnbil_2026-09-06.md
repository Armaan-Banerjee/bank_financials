# HD follow-up: NatWest plc and Punjab National Bank International

## Punjab National Bank (International) Limited

The Bank's own [Annual Report for the year ended 31 March 2021](https://www.pnbint.com/PNBIL/pdf/Financial%20Reports/Annual%20report%20%2031-03-21.pdf) was found on its Financial Reports page.  It is entity-level (company 05781326), and its statements give FY2021 total assets $1,082.747m, total liabilities $878.659m, total equity $204.088m (printed pp.24–28).  The same report gives the complete FY2021 cash-flow statement and equity roll-forward.

The accompanying [FY2021 Pillar 3 disclosure](https://www.pnbint.com/PNBIL/pdf/Financial_Reports/Basel%20III%20Pillar%203%20Disclosures%20%2031-03-2021.pdf) gives KM1 capital $134.4m CET1, $179.4m Tier 1, $206.6m total capital, $784.6m RWA and ratios 17.1%, 22.9%, 26.3%; leverage 17.3%, LCR 748%, and NSFR 146% (printed pp.3 and 10).  Its Pillar 1 table gives RWA after SME benefit: credit risk 728.7, market risk 11.0, operational risk 44.9 (printed p.7).

These values were added to the PNBIL build script and workbook, including FY2021 balance sheet, P&L/OCI, equity, cash flow, regulatory metrics and RWA breakdown.  The workbook rebuild succeeds; the verifier's cash-flow warnings are the existing translation/presentation heuristic limitation.

## NatWest plc (National Westminster Bank Plc)

The FY2014 £1,391m equity roll-forward difference was rechecked against the contemporaneous [NatWest Plc Pillar 3 Report 2014](https://investors.natwestgroup.com/~/media/Files/R/RBS-IR-V2/2014-reports/pillar-3-report-2014-v2.pdf).  Its capital-resources table independently reports NatWest Plc shareholders' equity of £13,312m and explicitly reports preference shares—equity as nil.  Therefore the earlier preference-share explanation is not supported.  The difference remains an unexplained source-presentation mismatch: the equity-statement components sum to £11,921m while the independently reported total is £13,312m.  No unverified £1,391m component was inserted.  The workbook source note now records this stronger cross-check and the workbook was rebuilt successfully.
