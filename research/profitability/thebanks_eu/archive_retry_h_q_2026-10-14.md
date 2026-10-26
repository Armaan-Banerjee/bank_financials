# TheBanks.eu historical archive retry: H–Q

Checked 2026-10-14. Scope: the 49 exact UK legal entities from **HABIB BANK
ZURICH** through **QIB UK** in
[`h_q_report.md`](./h_q_report.md), using the exact TheBanks.eu profile URLs
listed in [`archive_h_q_report.md`](./archive_h_q_report.md).

## Result

- **New qualifying historical bank-years recovered: 0.**
- No explicit FY2021 or FY2023 H–Q ROA/ROE value was recovered.
- No additional FY2022 value was recovered. The previously collected
  **Northern Bank Ltd FY2022 ROA 0.78% and ROE 13.04%** remains the only
  pre-FY2024 H–Q observation. It is explicit retained TheBanks.eu text from
  the exact entity's [`/financials` page](https://thebanks.eu/banks/14401/financials),
  not a replayed archive capture, and was not duplicated.
- No JSONL, worksheet, curated returns store, script, extract or downstream
  deliverable was changed by this retry.

The admission rule was unchanged: a value had to be an explicit ROA and/or
ROE percentage tied to the exact legal entity and an explicit displayed year.
No ratio was calculated from the balance sheet or profit, no year was inferred
from a crawl date, and no parent, branch or similarly named entity was used.

## Why Wayback was inaccessible

The retry confirms that the earlier problem was an **access-layer/network
restriction in this execution environment**, not evidence that the Internet
Archive has no captures for these pages.

### Web gateway tests

The following requests were made for the exact Investec Bank Plc profile as a
representative seed:

1. [CDX capture enumeration](https://web.archive.org/cdx/search/cdx?url=thebanks.eu%2Fbanks%2F14362&output=json&filter=statuscode%3A200&filter=mimetype%3Atext%2Fhtml&fl=timestamp%2Coriginal%2Cstatuscode%2Cdigest&collapse=digest)
2. [Timestamped replay](https://web.archive.org/web/20240101000000id_/https://thebanks.eu/banks/14362)
3. [Year/calendar replay](https://web.archive.org/web/2024/https://thebanks.eu/banks/14362)
4. [Wayback Availability API](https://archive.org/wayback/available?url=thebanks.eu%2Fbanks%2F14362&timestamp=20231231)
5. [Wayback calendar-capture endpoint](https://web.archive.org/__wb/calendarcaptures/2?url=thebanks.eu%2Fbanks%2F14362&date=2023&groupby=day)

Each request was rejected before capture metadata or replay content was
returned, with the gateway response saying that the URL was not accessible via
the tool. The HTTP variant was normalized to HTTPS and failed identically.

The command-line route failed one layer earlier: `curl` returned
`Could not resolve host` for `web.archive.org` and `archive.org`. The same DNS
failure occurred for `arquivo.pt`, so it is not a bank-specific or profile-ID
failure. Consequently, this run obtained **no Wayback capture timestamps** and
cannot classify any entity as having either captures or no captures.

This interpretation follows the Internet Archive's own
[Wayback guidance](https://archivesupport.zendesk.com/hc/en-us/articles/360004651732-Using-The-Wayback-Machine): an absent or broken replay can reflect crawl,
robots, JavaScript or resource-availability limitations. Here, however, the
requests did not reach the stage where archive availability could be assessed.

### Alternative archive-route tests

The following alternatives were also attempted with the same exact profile:

- [Arquivo.pt CDX](https://arquivo.pt/wayback/cdx?url=thebanks.eu%2Fbanks%2F14362&output=json)
- [Arquivo.pt version history](https://arquivo.pt/textsearch?versionHistory=thebanks.eu%2Fbanks%2F14362&maxItems=50)
- [Memento Time Travel](https://timetravel.mementoweb.org/api/json/20231231/https://thebanks.eu/banks/14362)

The web gateway rejected each route before returning metadata. Direct Arquivo
access additionally failed DNS resolution. These tests therefore supplied no
capture timestamp and no archived content.

## Search-index retry

Because replay remained unavailable, the usable fallback was retained search
index text. All 49 exact legal names and exact profile IDs were checked against
TheBanks.eu profile and common subpage routes, especially `/financials`, with
the site's performance wording (`return on assets`, `return on equity`, and
`showcasing`) and explicit 2021, 2022 and 2023 year terms.

The FY2023 sweep was performed entity by entity. The FY2022 and FY2021 sweeps
used grouped exact-name queries and were repeated with ROA/ROE wording. Results
fell into four non-qualifying categories:

1. current FY2024 profile text, for example
   [Investec Bank Plc](https://thebanks.eu/banks/14362),
   [Lloyds Bank Plc](https://thebanks.eu/banks/14376), and
   [QIB (UK) Plc](https://thebanks.eu/banks/14531);
2. current pages containing historical balance-sheet or market-share rows but
   no historical profitability ratio;
3. unrelated or similar-bank results;
4. the already-collected retained Northern Bank FY2022 result.

One useful negative-control result was the exact
[Northern Bank `/financials` page](https://thebanks.eu/banks/14401/financials),
whose search-index copy is reported as crawled about 1.3 years ago and still
contains the explicit FY2022 performance sentence. This demonstrates that the
indexed-subpage method can recover displaced ratios when a stale subpage copy
exists. Comparable qualifying stale text was not surfaced for the other 48
H–Q entities.

Search-index absence is not proof that TheBanks.eu never displayed a ratio.
It only means no qualifying retained text was exposed by the available index
on 2026-10-14.

## Exact-entity coverage audited

The retry covered the same 49 profile IDs documented in the prior report:

`18619, 18319, 14353, 19241, 14546, 14352, 14347, 14604, 19008,
14551, 14605, 14552, 18766, 14362, 17763, 14366, 14364, 14559,
14367, 14368, 14564, 19531, 14455, 18895, 14376, 18956, 14382,
14385, 14387, 14574, 14389, 19286, 18773, 14577, 14392, 14393,
14395, 14437, 14399, 14401, 18695, 14589, 19243, 18092, 19532,
14405, 14406, 14592, 14531`.

Every ID maps to `https://thebanks.eu/banks/<ID>`. Entity names and the
clickable URL for each ID are preserved in
[`archive_h_q_report.md`](./archive_h_q_report.md#exact-urls-left-for-retry).

## Practical next route

The blocker is not a missing candidate list but the inability to enumerate and
replay captures. A productive next retry needs working access to either the
Wayback CDX/replay services or an exported capture list/WARC. For each exact
URL, the first target windows remain mid/late 2022 for displayed FY2021, 2023
for FY2022, 2024 for FY2023, and 2025 for displaced FY2024 pages. Capture time
must remain discovery metadata; the financial year and ratio must be read from
the archived page itself.
