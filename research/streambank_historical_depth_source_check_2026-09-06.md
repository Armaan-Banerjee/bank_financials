# StreamBank historical-depth source check

Research date: 2026-09-06. Objective: determine whether recoverable entity-level FY2019 and FY2020 figures exist for the StreamBank workbook (HD-059), and whether the Companies House records establish the entity's status and accounting periods.

## Conclusion

StreamBank PLC is the same legal entity as the company incorporated as ActivTrades Loans PLC on 14 May 2019 (Companies House no. 11995458), renamed StreamBank PLC on 19 July 2022. Companies House lists exact accounts for the periods ended 31 December 2019 and 31 December 2020, and classifies both filings as **accounts for a dormant company**. The filing history does not show an operating annual report or bank financial statements for either period. The two filings are each only two pages, and their PDF/iXBRL document endpoints were not retrievable in this environment (the Companies House page confirms their existence but the document fetch returned a cache miss). No FY2019/FY2020 entity-level figures can therefore be safely added.

The conclusion is consistent with StreamBank's own later Pillar 3 disclosure: it says the entity was established in May 2019 and obtained its unrestricted banking licence in February 2023. StreamBank's official annual-report archive begins with later reports (FY2023 onward), so it does not provide an alternative FY2019/FY2020 operating-account source.

## Primary-source findings

### Companies House identity and name history

The official company overview identifies company number 11995458, incorporation on 14 May 2019, active public-company status, SIC 64191 (banks), and the previous name ActivTrades Loans PLC from 14 May 2019 to 19 July 2022. This establishes that the 2019/2020 filings belong to the same legal entity as today's StreamBank PLC: [Companies House company overview](https://find-and-update.company-information.service.gov.uk/company/11995458).

### FY2019 and FY2020 filings

The second page of the official filing history lists:

- 4 June 2020 — “Accounts for a dormant company made up to 31 December 2019”, two pages.
- 12 May 2021 — “Accounts for a dormant company made up to 31 December 2020”, two pages.

It also shows the accounting period was shortened from 31 May 2020 to 31 December 2019, which explains why the first filing is a short initial period rather than a normal March/December operating year: [Companies House filing history, page 2](https://find-and-update.company-information.service.gov.uk/company/11995458/filing-history?page=2).

The filing-history page exposes both the PDF and iXBRL links, but direct retrieval of the two documents returned cache-miss errors in this research run. The existence, filing dates, accounting dates, and dormant classification are nevertheless explicit on the official page. No figures have been inferred from the filing metadata.

### Official StreamBank disclosure

StreamBank's official FY2024 Pillar 3 disclosure states that StreamBank PLC was established in May 2019, obtained its banking licence without restriction in February 2023, has no subsidiaries, and is authorised by the PRA and regulated by the FCA and PRA: [StreamBank FY2024 Pillar 3 disclosure](https://streambank.co.uk/pdf/FY24-Pillar-3-StreamBank-PLC.pdf). This supports treating the 2019/2020 dormant filings as pre-operating/pre-bank periods rather than substituting later operating figures.

StreamBank's official FY2023 accounts are for the same registered number 11995458 and provide the earliest operating-era annual-report material located in the bank's own archive: [StreamBank FY2023 financial statements](https://streambank.co.uk/pdf/StreamBank-Plc-Financial-Statements-31-March-2023-Signed.pdf).

## Regulatory-register check

Searches of the FCA public register for StreamBank and FRN 954876 did not produce a retrievable historical 2019/2020 financial statement or capital disclosure. The official StreamBank Pillar 3 disclosure is the stronger primary source for the licence timing and regulatory status, and places unrestricted banking authorisation in February 2023.

## Decision for HD-059

Retain FY2019 and FY2020 as individually self-skipped in the StreamBank workbook. The skips are source-availability decisions, not evidence that figures were zero: Companies House confirms dormant filings existed, but the underlying two-page documents could not be retrieved for transcription. Do not populate statements, ratios, RWA, or asset-quality figures for those years from later reports or group-level material.
