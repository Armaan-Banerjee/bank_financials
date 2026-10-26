# TheBanks.eu historical archive retry: R–Z

Checked 14 October 2026. Scope: the 36 exact project entities from
RATHBONES INVESTMENT MANAGEMENT through ZOPA listed in
[`r_z_report.md`](r_z_report.md). This retry sought explicit TheBanks.eu ROA
and ROE values for FY2021–FY2023. Ratios were not calculated from the site's
balance-sheet or profit figures.

## Result

- New qualifying historical bank-years recovered: **0**.
- The previously collected R–Z history remains Tandem FY2023 ROA 0.12% and
  TD Bank Europe FY2023 ROA 0.26% / ROE 4.74%.
- No exact-entity FY2021 or FY2022 profitability sentence was recovered, and
  no additional FY2023 ratio qualified.
- No JSONL collection or worksheet was changed by this retry.

Every exact legal name and known profile ID was searched with explicit year,
`return on assets`, `return on equity`, `showcasing`, profile and
`/financials` terms. The available index normally returned the current FY2024
performance paragraph. Historical rows visible on those current pages were
balance-sheet or market-share comparatives, not historical ROA/ROE. Results
for similarly named entities and non-project banks were rejected.

This is a reach result, not evidence that TheBanks.eu never displayed older
ratios. The search-index method does preserve some displaced pages: the exact
[TD Bank Europe `/financials` page](https://thebanks.eu/banks/14432/financials)
still exposes FY2023 ROA 0.26% and ROE 4.74%, while retained text previously
exposed Tandem FY2023 ROA 0.12%. No comparable additional R–Z page surfaced.

## Why the archive still could not be tested

The failure occurs before capture availability can be determined:

- shell requests cannot resolve `web.archive.org`, `archive.org`,
  `index.commoncrawl.org` or `arquivo.pt`;
- the web gateway can open the ordinary Wayback and Arquivo.pt homepages, but
  returns an internal access error for CDX, timemap, calendar, Availability API
  and timestamped replay URLs;
- the same rejection occurred for the separate
  `archive.org/wayback/available` endpoint, Archive-It timemaps and Arquivo.pt
  version-history/CDX endpoints.

Representative exact-bank tests used the
[Tandem profile](https://thebanks.eu/banks/14356):

- [Wayback CDX](https://web.archive.org/cdx/search/cdx?url=thebanks.eu%2Fbanks%2F14356&output=json)
- [Wayback timestamp replay](https://web.archive.org/web/20230101000000id_/https://thebanks.eu/banks/14356)
- [Wayback Availability API](https://archive.org/wayback/available?url=thebanks.eu%2Fbanks%2F14356&timestamp=20231231)
- [Arquivo.pt version history](https://arquivo.pt/textsearch?versionHistory=thebanks.eu%2Fbanks%2F14356&maxItems=50)

None returned capture metadata or archived content in this environment. It is
therefore not valid to label any profile as having no capture. The practical
next step is to obtain a CDX/capture-list export from a network that can reach
Wayback, then inspect the archived page text for the displayed financial year
and explicit ratios.
