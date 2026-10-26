# TheBanks.eu historical archive recovery: R–Z

Collected 2026-10-13. Scope: the 36 project banks alphabetically from
`RATHBONES INVESTMENT MANAGEMENT` through `ZOPA`, inclusive. This is a
provenance-preserving staging pass only: no worksheet, existing store, extract,
script, sweep batch or deliverable was changed.

## Outcome

- **0 new bank-year observations recovered.**
- The indexed sweep rediscovered Tandem FY2023 ROA and TD Bank Europe FY2023
  ROA/ROE, but both keys already exist in
  [`r_z.jsonl`](r_z.jsonl), so they were deliberately not duplicated.
- No direct Internet Archive snapshot could be opened and no stronger evidence
  was available with which to replace an existing current-store record.
- [`archive_r_z.jsonl`](archive_r_z.jsonl) is therefore intentionally empty.

An empty archive partition does not mean that historic ratios do not exist. It
means this pass found no additional explicit ratio that met the project's
exact-entity, explicit-year and non-duplication rules.

## Method

The pass first attempted the ordinary public [Wayback replay
route](https://web.archive.org/) and [CDX capture
index](https://web.archive.org/cdx/search/cdx) for each exact TheBanks.eu
profile. The browsing gateway rejected both routes and the shell environment
could not resolve the archive hosts, so neither capture existence nor snapshot
timestamps could be verified.

As a fallback, ordinary search was used to look for historic exact-profile and
`/financials`, `/market_share`, `/credit_ratings`, and related subpage text.
Queries targeted FY2021–FY2023 first and then displaced FY2024/FY2025 text. A
candidate was acceptable only if the indexed TheBanks.eu text explicitly named
the exact legal entity, stated a financial year, and gave ROA and/or ROE. No
snapshot year was treated as a financial year, and no ratio was calculated,
backsolved or borrowed from a parent, branch, predecessor or similarly named
entity.

The fallback confirmed the two already-staged observations:

- [Tandem Bank Limited](https://thebanks.eu/banks/14356): FY2023 ROA 0.12%,
  already present in `r_z.jsonl`.
- [TD Bank Europe Limited financials](https://thebanks.eu/banks/14432/financials):
  FY2023 ROA 0.26% and ROE 4.74%, already present in `r_z.jsonl`.

Because these are search-indexed rather than directly replayed snapshots, they
do not supply a verifiable Wayback timestamp and do not strengthen the evidence
already stored.

## Requested archive-status categories

### Recovered as new archive rows (0)

No new `(bank, year)` key met the acceptance criteria.

### Capture inaccessible / no additional usable indexed historic ratio (36)

- Rathbones Investment Management; RBC Europe; Royal Bank of Scotland; RCI
  Bank UK; Recognise Bank; Redwood Bank; Reliance Bank.
- Santander UK; Santander Financial Services; Schroder; Secure Trust Bank;
  Shawbrook; SMBC Bank International; Standard Chartered Bank; Starling; State
  Bank of India UK; StreamBank.
- Tandem; TD Bank Europe; The Bank of London Group; THIS Bank; Triodos Bank UK;
  TSB; Turkish Bank UK.
- UBA UK; Union Bancaire Privée UK; Union Bank of India UK; United National;
  United Trust Bank; Unity Trust; Vanquis; Vida; Weatherbys; Zempler; Zenith;
  Zopa.

For Tandem and TD Bank Europe, “no additional” is important: the exact FY2023
indexed evidence exists but was already staged. For the other 34 banks, no new
explicit historic ratio was recoverable through the accessible indexed route.

### No captures (0 verified)

CDX was inaccessible. No profile is classified as having no Internet Archive
capture, because that conclusion could not be checked.

### Captured page but no usable historic ratio (0 verified)

No direct snapshot was accessible. Current/live pages without historic ratios
were not relabelled as archived captures.

## Validation

- The intentionally empty JSONL has zero parse errors and zero duplicate keys.
- Existing R–Z records were left unchanged; in particular, Tandem FY2023 and TD
  Bank Europe FY2023 were not duplicated.
- No parent or foreign branch was substituted for SMBC Bank International,
  State Bank of India (UK) or Turkish Bank (UK).

