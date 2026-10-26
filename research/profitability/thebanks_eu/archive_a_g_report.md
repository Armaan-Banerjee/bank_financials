# TheBanks.eu historical archive recovery: A–G

Collected 2026-10-13. Scope: the 60 project banks alphabetically from
`ABC INTERNATIONAL BANK` through `GULF INTERNATIONAL BANK UK`, inclusive.
This pass looked only for historic TheBanks.eu-calculated ROA/ROE and did not
change a worksheet, extract, script, curated store, sweep batch or deliverable.

## Outcome

- **3 exact-bank FY2023 observations recovered**: Bank Sepah International,
  FCE Bank and Ghana International Bank.
- Each recovered row contains both ROA and ROE; there are no partial rows.
- No FY2021, FY2022 or FY2025 observation was recoverable through the archive
  routes available in this environment.
- The three observations reproduce the existing independent audited-account
  calculations exactly to the displayed two decimal places. This is a
  reasonableness check only; the TheBanks.eu values remain a distinct
  third-party-calculated evidence class.

The machine-readable findings are in
[`archive_a_g.jsonl`](archive_a_g.jsonl). They are not silently merged into
the current-profile collection.

## Recovery evidence

| project bank | source year | ROA | ROE | indexed historic route |
|---|---:|---:|---:|---|
| BANK SEPAH INTERNATIONAL | 2023 | 0.35% | 0.70% | [market-share subpage](https://thebanks.eu/banks/14301/market_share) |
| FCE BANK | 2023 | 0.48% | 3.48% | [credit-ratings subpage](https://thebanks.eu/banks/14339/credit_ratings) |
| GHANA INTERNATIONAL BANK | 2023 | 0.37% | 1.94% | [market-share subpage](https://thebanks.eu/banks/14343/market_share) |

The search index described each of these routes as crawled about 1.3 years
before collection and retained an explicit 2023 performance sentence naming
the exact entity and giving the ratios. The underlying live routes now mix in
2024 content, so these rows are deliberately marked
`verification: archive_search_indexed`, not `wayback_snapshot`, and
`snapshot_timestamp` is `null` rather than an invented date.

## Archive method and access limitation

The pass attempted the normal public Internet Archive interfaces for each
exact profile: the [Wayback replay route](https://web.archive.org/) and the
[CDX capture index](https://web.archive.org/cdx/search/cdx). The browsing
gateway rejected both hosts/routes, while the shell environment could not
resolve them. Consequently, capture existence and timestamps could not be
verified directly. Ordinary web search was then used to look for retained
historic TheBanks.eu profile and subpage text. A row was accepted only where
the indexed text explicitly named the exact legal entity, labelled the source
year, and stated ROA and/or ROE; no ratio was inferred, calculated or
backsolved.

This limitation matters: **capture inaccessible** below means that this run
could not inspect Wayback, not that the Internet Archive has no capture.
Likewise, absence from `archive_a_g.jsonl` is not evidence that TheBanks.eu
never displayed a historic value.

## Requested archive-status categories

### Recovered (3)

- Bank Sepah International plc — FY2023, indexed historic market-share route.
- FCE Bank plc — FY2023, indexed historic credit-ratings route.
- Ghana International Bank Plc — FY2023, indexed historic market-share route.

### Capture inaccessible / no independently usable indexed historic ratio (57)

- ABC International Bank; Access Bank UK; AIB Group UK; Aldermore; Afin Bank;
  Allica; Alpha Bank London; Al Rayan Bank; Arab Bank Europe / Europe Arab
  Bank; Arbuthnot Latham; Atom Bank.
- Bank Mandiri Europe; Bank of Africa UK; Bank of Beirut UK; Bank of Ceylon UK;
  Bank of China UK; Bank of Ireland (UK); Bank of Scotland; Bank of the
  Philippine Islands Europe; Bank Saderat; Barclays Bank UK; Barclays Bank plc;
  Birmingham Bank; BLME; BNY Mellon International; British Arab Commercial
  Bank; Brown Shipley.
- C. Hoare & Co.; CAF Bank; Cambridge & Counties Bank; Castle Trust Capital;
  Cater Allen; Charity Bank; Charter Court Financial Services; Chetwood;
  Citibank UK; ClearBank; Close Brothers; Clydesdale; Co-operative Bank;
  Coutts; Credit Suisse International; Credit Suisse UK; Crown Agents Bank;
  Cynergy Bank.
- DB UK Bank; DF Capital Bank; EFG Private Bank; FCMB UK; FidBank UK;
  FirstBank UK; Gatehouse Bank; GB Bank; Goldman Sachs International Bank;
  Griffin Bank; Guaranty Trust Bank UK; Gulf International Bank UK.

### No captures (0 verified)

CDX was not reachable, so it would be unsound to classify any profile as
having no Internet Archive captures.

### Captured page but no usable historic ratio (0 verified)

No direct snapshot could be opened. Live/current pages that lacked a historic
ratio were not relabelled as archived captures.

## Validation

- JSONL parses successfully and has three unique `(bank, year)` keys.
- All entities match the exact project legal entity and all values preserve the
  source signs and percentage formatting.
- All three bank names occur in the 145-bank worklist and all three FY2023
  pairs equal the corresponding values in
  [`../extract_2026-10-11.json`](../extract_2026-10-11.json).

