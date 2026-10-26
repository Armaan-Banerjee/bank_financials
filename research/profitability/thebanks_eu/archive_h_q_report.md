# TheBanks.eu archive recovery: H–Q

Collected 2026-10-13. Scope: the 49 exact project entities from **HABIB BANK
ZURICH** through **QIB UK** listed in [`h_q_report.md`](./h_q_report.md).

## Result

- Recovered: **0 bank-years**.
- Recovered through retained search-indexed profile/subpage text: **0
  bank-years**.
- Confirmed no captures: **0 banks**.
- Capture exists but page is inaccessible: **0 banks confirmed**.
- Captured page accessible but no usable historic ratio: **0 banks confirmed**.
- Archive availability/content inaccessible and therefore unverified: **49 banks**.

[`archive_h_q.jsonl`](./archive_h_q.jsonl) is intentionally empty. The
collection rule admits only an archived exact-entity page that explicitly
states a financial year and ROA and/or ROE percentage. No value was inferred
from a snapshot date, calculated from accounts, copied from a live page, or
substituted from a parent/group entity.

## Method and access outcome

The exact TheBanks.eu profile URLs in [`h_q.jsonl`](./h_q.jsonl) were the URL
seeds. The intended workflow was:

1. enumerate successful HTML captures using the Internet Archive CDX service;
2. inspect captures near the publication windows for 2021, 2022 and 2023;
3. inspect older 2024 pages where a live profile had advanced to 2025; and
4. accept a record only when the replayed page itself supplied the entity,
   displayed year and numeric ratio.

The [Internet Archive's Wayback guidance](https://archivesupport.zendesk.com/hc/en-us/articles/360004651732-Using-The-Wayback-Machine)
confirms that a specific URL must be checked and that missing/broken captures
can result from crawl, robots, JavaScript or resource-availability limits. Its
[Availability API documentation](https://doc-tools.readthedocs.io/en/ia-test-gsod/tutorial-get-snapshot-wayback.html)
also distinguishes an available capture from an empty archive result.

In this run, normal CDX, Availability API, calendar and timestamped replay
requests were all blocked at the access layer before capture metadata or page
content was returned. Direct command-line requests additionally failed DNS
resolution for `web.archive.org`. Search-engine queries for exact archived
profile URLs returned no indexed snapshot URLs, but that is not evidence that
the archive has no captures. A known, unrelated timestamped Wayback URL already
stored in this repository failed through the same replay route, confirming that
the failure was systemic rather than evidence about any particular bank.

Accordingly, all 49 banks remain in an **archive access unverified** category.
They must not be reclassified as “no captures” or “no historic ratios.”

## Search-indexed supplement

A second targeted pass searched every exact H–Q entity and profile ID together
with the TheBanks.eu profile and common subpage routes (`/financials`,
`/market_share` and `/credit_ratings`), the 2021–2023 year labels, and the ROA
and ROE performance wording used by the site. This was intended to recover
older sentences retained by a search index even though Wayback replay was
unavailable.

No qualifying historic H–Q observation was found. Results were current FY2024
or FY2025 profile text, balance-sheet comparative years, historic market-share
tables without profitability ratios, or unrelated banks surfaced through
similar-bank links. None simultaneously supplied the exact H–Q entity, a
FY2021–FY2023 label, and a numeric ROA and/or ROE. Consequently no
`archive_search_indexed` row was added. The already-collected Northern Bank
FY2022 indexed observation remains in the current-profile store and was not
duplicated here.

## Exact URLs left for retry

| Project bank | Exact profile URL |
|---|---|
| HABIB BANK ZURICH | https://thebanks.eu/banks/18619 |
| HAMPDEN & CO | https://thebanks.eu/banks/18319 |
| HAMPSHIRE TRUST BANK | https://thebanks.eu/banks/14353 |
| HANDELSBANKEN | https://thebanks.eu/banks/19241 |
| HAVIN BANK | https://thebanks.eu/banks/14546 |
| HBL BANK UK | https://thebanks.eu/banks/14352 |
| HSBC BANK PLC | https://thebanks.eu/banks/14347 |
| HSBC INNOVATION BANK | https://thebanks.eu/banks/14604 |
| HSBC UK BANK PLC | https://thebanks.eu/banks/19008 |
| ICBC (LONDON) PLC | https://thebanks.eu/banks/14551 |
| ICBC STANDARD BANK PLC | https://thebanks.eu/banks/14605 |
| ICICI BANK UK | https://thebanks.eu/banks/14552 |
| IFAST GLOBAL BANK LIMITED | https://thebanks.eu/banks/18766 |
| INVESTEC BANK PLC | https://thebanks.eu/banks/14362 |
| ITAU BBA INTERNATIONAL | https://thebanks.eu/banks/17763 |
| JORDAN INTERNATIONAL BANK | https://thebanks.eu/banks/14366 |
| JP MORGAN EUROPE | https://thebanks.eu/banks/14364 |
| JP MORGAN SECURITIES | https://thebanks.eu/banks/14559 |
| JULIAN HODGE BANK | https://thebanks.eu/banks/14367 |
| KEXIM BANK UK | https://thebanks.eu/banks/14368 |
| KINGDOM BANK | https://thebanks.eu/banks/14564 |
| KROO BANK | https://thebanks.eu/banks/19531 |
| KUWAIT FINANCE HOUSE | https://thebanks.eu/banks/14455 |
| LHV | https://thebanks.eu/banks/18895 |
| LLOYDS BANK | https://thebanks.eu/banks/14376 |
| LLOYDS BANK CORPORATE MARKETS | https://thebanks.eu/banks/18956 |
| MARKS AND SPENCER FINANCIAL SERVICES | https://thebanks.eu/banks/14382 |
| MELLI BANK | https://thebanks.eu/banks/14385 |
| METHODIST CHAPEL AID | https://thebanks.eu/banks/14387 |
| METRO BANK | https://thebanks.eu/banks/14574 |
| MIZUHO INTERNATIONAL | https://thebanks.eu/banks/14389 |
| MONUMENT BANK | https://thebanks.eu/banks/19286 |
| MONZO | https://thebanks.eu/banks/18773 |
| MORGAN STANLEY BANK INTERNATIONAL | https://thebanks.eu/banks/14577 |
| NATIONAL BANK OF EGYPT UK | https://thebanks.eu/banks/14392 |
| NATIONAL BANK OF KUWAIT INTERNATIONAL | https://thebanks.eu/banks/14393 |
| NATIONAL WESTMINSTER BANK PLC | https://thebanks.eu/banks/14395 |
| NATWEST MARKETS | https://thebanks.eu/banks/14437 |
| NOMURA BANK INTERNATIONAL | https://thebanks.eu/banks/14399 |
| NORTHERN BANK | https://thebanks.eu/banks/14401 |
| OAKNORTH BANK | https://thebanks.eu/banks/18695 |
| ONESAVINGS | https://thebanks.eu/banks/14589 |
| OXBURY | https://thebanks.eu/banks/19243 |
| PARAGON | https://thebanks.eu/banks/18092 |
| PERENNA | https://thebanks.eu/banks/19532 |
| PERSIA INTERNATIONAL BANK | https://thebanks.eu/banks/14405 |
| PHILIPPINE NATIONAL BANK EUROPE | https://thebanks.eu/banks/14406 |
| PUNJAB NATIONAL BANK INTERNATIONAL | https://thebanks.eu/banks/14592 |
| QIB UK | https://thebanks.eu/banks/14531 |

## Retry priority

Once the archive routes are reachable, use one target timestamp per likely
publication window first (mid/late 2022 for FY2021, 2023 for FY2022, 2024 for
FY2023, and 2025 for FY2024), then enumerate CDX history around any successful
capture. The snapshot timestamp is discovery metadata only; the financial year
must still be read from the archived page.

No worksheet, current TheBanks.eu store, sweep batch, extract, script or
downstream deliverable was changed.
