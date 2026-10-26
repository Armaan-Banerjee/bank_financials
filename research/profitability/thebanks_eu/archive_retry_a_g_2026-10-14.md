# TheBanks.eu archive retry: A–G

Collected 14 October 2026. Scope: the 60 exact project entities from `ABC
INTERNATIONAL BANK` through `GULF INTERNATIONAL BANK UK`. This retry looked
for explicit TheBanks.eu-calculated ROA and ROE for FY2021–FY2023, plus any
displaced FY2024 observation. It did not calculate ratios and did not modify a
worksheet or any existing JSONL store.

## Result

No additional qualifying A–G TheBanks.eu bank-year was recovered beyond the
three FY2023 observations already preserved in
[`archive_a_g.jsonl`](archive_a_g.jsonl):

| Exact entity | Year | ROA | ROE | Retained indexed route |
|---|---:|---:|---:|---|
| Bank Sepah International plc | 2023 | 0.35% | 0.70% | [market-share page](https://thebanks.eu/banks/14301/market_share) |
| FCE Bank plc | 2023 | 0.48% | 3.48% | [credit-ratings page](https://thebanks.eu/banks/14339/credit_ratings) |
| Ghana International Bank Plc | 2023 | 0.37% | 1.94% | [market-share page](https://thebanks.eu/banks/14343/market_share) |

The retry searched the exact legal-entity names and exact profile IDs for the
60 banks, including the profile, `/financials`, `/market_share`,
`/credit_ratings` and `/bank_identifiers` routes where indexed. Searches were
run separately for 2021, 2022 and 2023 and required the result itself to state
the exact entity, displayed year and percentage. FY2021 and FY2022 returned no
qualifying historical TheBanks.eu performance sentence. FY2023 rediscovered
the three rows above but produced no new exact-entity row. Current 2024 pages,
historical balance-sheet/market-share tables, similarly named entities and
bank-published ratios were excluded.

## Why Wayback was inaccessible

The prior wording should be read as **inaccessible from this execution
environment**, not “the Wayback Machine was down” and not “there were no
captures.” The same failure reproduced on 14 October 2026:

- The browsing gateway returned `URL ... is not accessible via this tool` for
  the public [CDX endpoint](https://web.archive.org/cdx/search/cdx),
  [Availability API](https://archive.org/wayback/available), Wayback calendar
  and timestamped replay URLs. Both HTTPS and HTTP inputs ended at the same
  rejection.
- The sandboxed shell could not resolve `web.archive.org` or `archive.org` and
  returned `curl: (6) Could not resolve host: web.archive.org`. It also could
  not resolve `thebanks.eu` or `index.commoncrawl.org`, showing that this is
  the shell's network/DNS restriction rather than a host-specific no-capture
  result.
- Text-mirror requests for CDX/replay were rejected by the browsing gateway as
  inaccessible as well. No archive timestamp or capture status could therefore
  be verified through a mirror.

Accordingly, this pass still cannot classify any profile as “no captures.” It
can only say that direct capture metadata and replay were unavailable through
the tools assigned to this workspace.

## Alternative archives tested

- [Common Crawl's collection catalogue](https://index.commoncrawl.org/collinfo.json)
  is discoverable, but per-URL index requests were not accessible through the
  gateway and the shell cannot resolve the host.
- The [Arquivo.pt URL-history API](https://arquivo.pt/textsearch) and its
  public [Memento/TimeMap interface](https://arquivo.pt/wayback/) were tested
  as independent archive routes. Direct query URLs were likewise rejected as
  inaccessible by the gateway; the shell also cannot resolve `arquivo.pt`.
- Ordinary indexed search remains usable and was therefore the only route
  capable of exposing historical TheBanks.eu text in this run. Its retained
  snippets support the three existing FY2023 rows, but an absent search result
  is not evidence that an archived page or historical value does not exist.

## Exact-entity primary-source leads kept separate

Search also surfaced explicit ratios in bank-owned annual reports. They are
useful profitability evidence, but they are **not TheBanks.eu-calculated
figures** and therefore were not added to this collection:

- [FirstBank UK 2023 annual report](https://www.fbnbank.co.uk/wp-content/uploads/2019/06/FirstBank-UK_2023_AR.pdf):
  ROA 0.7%, 1.3%, 1.2% and ROE 9.4%, 15.8%, 11.4% for 2021, 2022 and 2023,
  respectively.
- [Bank of Africa UK 2024 annual report](https://www.bankofafricaunitedkingdom.co.uk/pdfs/finances/BOA%20UK%20Annual%20Report%202024.pdf):
  the exact entity reports 2023 ROA -3.96% and ROE -19.90% as comparatives.
- [Europe Arab Bank 2024 annual report](https://www.eabplc.com/downloads/202502_EABAnnualReport_v3.pdf):
  the exact entity reports 2023 ROA 0.50% and ROE 3.65% as comparatives.
- [Credit Suisse International 2023 annual report](https://www.ubs.com/global/en/collections/credit-suisse/investment-bank/regulatory-directory/international.html):
  the exact entity's KPI table reports return on total assets of -2.2%, -0.2%
  and -1.4% for 2021, 2022 and 2023. No corresponding ROE was accepted from
  the accessible result.

These leads should remain in the bank-published evidence class if used later;
mixing them into the TheBanks.eu archive supplement would obscure source and
methodology differences.

## Status

- New qualifying TheBanks.eu rows: **0**.
- Existing A–G archive supplements reconfirmed: **3 FY2023 bank-years**.
- Verified Wayback/Arquivo.pt captures: **0**, because metadata and replay
  remained inaccessible.
- Verified no-capture determinations: **0**.
- Files intentionally unchanged: all JSONL stores, worksheets, extracts,
  scripts and downstream deliverables.
