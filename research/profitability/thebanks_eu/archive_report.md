# TheBanks.eu historical archive follow-up

> **Archive retry, 14 October 2026:** All 145 exact entities and the archive
> access routes were retested. No additional qualifying TheBanks.eu history
> was recovered; Wayback capture metadata and replay remain inaccessible from
> this execution environment. See
> [`archive_retry_2026-10-14.md`](archive_retry_2026-10-14.md) for the access
> diagnosis and the exact-bank annual-report leads kept outside this store.

> **FY2024 follow-up, 14 October 2026:** A later targeted pass recovered J.P.
> Morgan Europe Limited FY2024 (ROA 0.12%, ROE 1.43%) from retained indexed
> TheBanks.eu text and Turkish Bank (UK) Ltd FY2024 (ROA 0.43%, ROE 2.62%)
> from its live profile. The expanded view now contains 149 observations across
> 141 entities, including 141 FY2024 observations; four FY2024 entities remain
> unresolved. See [`fy2024_gap_followup_2026-10-14.md`](fy2024_gap_followup_2026-10-14.md).

Collected 13 October 2026. This pass retried the missing FY2021–FY2023 years
and displaced FY2024/FY2025 pages for all 145 project banks. It preserved the
same exact-entity and no-calculation rules as the live-profile collection and
did not change any bank worksheet or curated bank-published-return store.

## Result

Three new exact-bank FY2023 observations were recovered from historic
TheBanks.eu text retained in the search index:

| Project bank | ROA | ROE | Retained TheBanks.eu route |
|---|---:|---:|---|
| BANK SEPAH INTERNATIONAL | 0.35% | 0.70% | [market-share subpage](https://thebanks.eu/banks/14301/market_share) |
| FCE BANK | 0.48% | 3.48% | [credit-ratings subpage](https://thebanks.eu/banks/14339/credit_ratings) |
| GHANA INTERNATIONAL BANK | 0.37% | 1.94% | [market-share subpage](https://thebanks.eu/banks/14343/market_share) |

Each indexed result explicitly named the exact bank, labelled 2023 and stated
both percentages. All six values also equal the independently computed audited
account figures already in the project to two decimal places. That comparison
is a reasonableness check, not the source of the recovered values.

No additional H–Q or R–Z bank-year qualified. Targeted searches of exact
profile IDs and `/financials`, `/market_share` and `/credit_ratings` routes
either returned current FY2024/FY2025 text, balance-sheet or market-share
comparatives without profitability ratios, unrelated entities, or values
already present. Tandem FY2023, TD Bank Europe FY2023 and Northern Bank FY2022
were rediscovered but not duplicated.

## Archive access limitation

The intended primary route was the Internet Archive: enumerate captures via
the [CDX index](https://web.archive.org/cdx/search/cdx), then inspect dated
[Wayback replays](https://web.archive.org/) and accept a row only when the
archived page itself stated the financial year and ratio. The web gateway
blocked CDX, Availability API, calendar and replay requests, and the shell
could not resolve the archive host. The per-URL indexes for the dated
[Common Crawl collections](https://index.commoncrawl.org/collinfo.json) were
also inaccessible even though their public collection catalogue was readable.

Therefore:

- no record is labelled `wayback_snapshot`;
- no snapshot timestamp or archive URL was invented;
- the three new records use `verification: archive_search_indexed`, a null
  `archive_url` and `snapshot_timestamp`, and a separate `indexed_url`;
- all other banks remain **archive-access-unverified**, not “no captures”; and
- zero banks were classified as verified no-capture or as an accessible
  archived page with no usable ratio.

## Coverage after the 13 October archive pass

The non-destructive combined view is
[`thebanks_eu_returns_with_archives.jsonl`](thebanks_eu_returns_with_archives.jsonl).
The new-only supplement is
[`thebanks_eu_archive_returns.jsonl`](thebanks_eu_archive_returns.jsonl).

| Financial year | Observations | Missing bank-years |
|---|---:|---:|
| FY2021 | 0 | 145 |
| FY2022 | 1 | 144 |
| FY2023 | 5 | 140 |
| FY2024 | 139 | 6 |
| FY2025 | 2 | 143 |
| **Total** | **147** | **578** |

ROA is present in all 147 observations; ROE is present in 142. Coverage remains
140 of 145 exact entities because the archive supplement added years for banks
already present rather than adding a new entity.

Partition evidence and retry URL manifests are in
[`archive_a_g_report.md`](archive_a_g_report.md),
[`archive_h_q_report.md`](archive_h_q_report.md), and
[`archive_r_z_report.md`](archive_r_z_report.md).

## Validation of the 13 October archive pass

- All JSONL files parse and the combined view has 147 unique `(bank, year)`
  keys.
- All record bank names occur in the 145-bank worklist; the only absent banks
  remain Afin Bank, Bank of Ireland UK, SMBC, State Bank of India UK and
  Turkish Bank UK.
- Years are restricted to FY2021–FY2025, entity matches are explicit and
  percentage strings preserve source signs.
- At that stage, the original 144-record current/indexed store was not
  overwritten. The later 14 October FY2024 pass described at the top added two
  qualifying observations to that separate store.
- No workbook, build script, sweep batch, audited extract, CSV/XLSX or
  downstream deliverable was changed.
