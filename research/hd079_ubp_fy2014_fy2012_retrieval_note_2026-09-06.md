# HD-079 UBP UK FY2014–FY2012 retrieval note (2026-09-06)

## Result

No workbook changes were made in this band. The FY2014 and FY2013 statutory
statements are already populated in the UBP UK builder/workbook. The FY2012
filing is confirmed by the official Companies House filing history, but its PDF
could not be retrieved in this environment; therefore no FY2012 figures have
been transcribed or inferred.

## Primary-source filing evidence

Union Bancaire Privée (UK) Limited is Companies House company **00964058**.
The official filing history identifies:

| Financial year | Filing description | Filed | Document token | Official record |
|---|---|---:|---|---|
| FY2014 | Full accounts made up to 31 December 2014 | 2015 | Not re-retrieved in this pass | [Companies House filing history](https://find-and-update.company-information.service.gov.uk/company/00964058/filing-history?page=5) |
| FY2013 | Full accounts made up to 31 December 2013 | 11 April 2014 | `MzA5ODA4NzA3MmFkaXF6a2N4` | [Companies House filing history, page 6](https://find-and-update.company-information.service.gov.uk/company/00964058/filing-history?page=6) |
| FY2012 | Full accounts made up to 31 December 2012 | 1 May 2013 | `MzA3NzI3NTEyMGFkaXF6a2N4` | [Companies House filing history, page 6](https://find-and-update.company-information.service.gov.uk/company/00964058/filing-history?page=6) |

The official page describes the FY2013 filing as a 55-page full-accounts PDF
and the FY2012 filing as a 52-page full-accounts PDF. The direct official PDF
URLs are:

- FY2013: `https://find-and-update.company-information.service.gov.uk/company/00964058/filing-history/MzA5ODA4NzA3MmFkaXF6a2N4/document?format=pdf&download=0`
- FY2012: `https://find-and-update.company-information.service.gov.uk/company/00964058/filing-history/MzA3NzI3NTEyMGFkaXF6a2N4/document?format=pdf&download=0`

Both endpoints returned **Cache miss** through the available document reader.
The shell environment also cannot resolve the Companies House host, so a
second direct-download route was unavailable. No secondary source was used as
a substitute for statutory accounts.

## Scope and integration status

The intended extraction scope is the four statutory statements on the company
only basis: Balance Sheet, Profit and Loss Account, Statement of Changes in
Equity, and any separately presented Cash Flow Statement. The existing builder
records that FY2014 and FY2013 use the older UK-GAAP-style presentation and
that the bank claimed a cash-flow exemption under FRS 1 (Revised), so a FY2012
filing must be checked for its own accounting basis and exemption before any
values are added.

The FY2013 filing is useful as the FY2012 comparative source once retrieved,
but it must not be treated as proof of FY2012 values without reading the
printed comparative column and confirming entity basis, units, restatements,
and page references. The FY2014 filing's FY2013 restated comparative also
contains a known presentation/restatement discrepancy already documented in
the builder; it should not overwrite FY2013's own reported figures silently.

## Next action

Obtain the FY2012 Companies House PDF (52 pages), then transcribe all four
statement pages and cross-check every FY2012 value against the FY2013 filing's
FY2012 comparative column. Preserve blanks where the filing genuinely omits a
line or claims a cash-flow exemption. No safe FY2012 additions can be made
until that document is readable.
