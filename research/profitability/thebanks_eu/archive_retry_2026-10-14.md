# TheBanks.eu historical archive retry

Checked 14 October 2026 across all 145 exact project entities. This was a
fresh attempt to recover explicit TheBanks.eu ROA and ROE for FY2021–FY2023
and any displaced FY2024 page. It retained the existing exact-entity,
displayed-year and no-calculation rules.

## Outcome

No additional qualifying TheBanks.eu bank-year was recovered. The historical
collection therefore remains:

- FY2021: none;
- FY2022: Northern Bank — ROA 0.78%, ROE 13.04%;
- FY2023: Bank Sepah International — 0.35%, 0.70%; FCE Bank — 0.48%,
  3.48%; Ghana International Bank — 0.37%, 1.94%; Tandem — ROA 0.12% only;
  and TD Bank Europe — 0.26%, 4.74%.

The three partition retries are documented in:

- [`archive_retry_a_g_2026-10-14.md`](archive_retry_a_g_2026-10-14.md)
- [`archive_retry_h_q_2026-10-14.md`](archive_retry_h_q_2026-10-14.md)
- [`archive_retry_r_z_2026-10-14.md`](archive_retry_r_z_2026-10-14.md)

## Why Wayback was inaccessible

“Inaccessible” means inaccessible from this execution environment. It does
not mean Wayback was offline, and it does not establish that a URL has no
captures.

Two independent access paths failed at different layers:

1. The sandboxed shell cannot resolve external archive hosts. `curl` returned
   `Could not resolve host` for `web.archive.org`, `archive.org`,
   `index.commoncrawl.org` and `arquivo.pt`.
2. The browsing gateway can read the ordinary Wayback and Arquivo.pt
   homepages, but returned an internal access error for every dynamic archive
   route tested: CDX enumeration, timestamped replay, calendar capture data,
   the separate `archive.org/wayback/available` API, Archive-It timemaps,
   Arquivo.pt CDX/version history and Memento Time Travel.

Because no endpoint returned capture metadata, the retry could not determine
which TheBanks.eu profile URLs have captures, select capture timestamps or
inspect archived page text. The correct status for all remaining profiles is
**archive-access-unverified**, not “no capture.”

## What the usable fallback established

Ordinary search-index queries were repeated for every exact legal name and
profile ID, separately targeting 2021, 2022 and 2023 and the site's standard
performance wording. They rediscovered the six historical bank-years above
but exposed no additional explicit ratio. Current pages often show historical
balance-sheet and market-share rows; those are not historical ROA/ROE and were
not used to calculate a replacement.

The stale Northern Bank, Bank Sepah, FCE Bank, Ghana International Bank,
Tandem and TD Bank Europe results demonstrate that displaced TheBanks.eu text
can survive in search indexes. Absence from the accessible index is still not
proof that TheBanks.eu never displayed the value.

## Separate exact-bank leads

The retry also surfaced historical profitability ratios in bank-owned annual
reports. They are not TheBanks.eu calculations and were therefore not added to
the aggregator collection:

- FirstBank UK: FY2021–FY2023 ROA 0.7%, 1.3%, 1.2%; ROE 9.4%, 15.8%, 11.4%.
- Bank of Africa UK: FY2023 ROA -3.96%, ROE -19.90%.
- Europe Arab Bank: FY2023 ROA 0.50%, ROE 3.65%.
- Credit Suisse International: FY2021–FY2023 return on total assets -2.2%,
  -0.2%, -1.4%; no corresponding ROE accepted from the accessible result.

The source links and entity checks for these leads are in the A–G report.
They should remain in the bank-published evidence class if later adopted.

No JSONL collection, worksheet, curated return store, extract, script or
downstream deliverable was changed by this retry.
