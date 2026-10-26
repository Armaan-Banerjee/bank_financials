# FY2024 TheBanks.eu gap follow-up

Checked 14 October 2026. This pass retested the six exact entities that lacked
an FY2024 TheBanks.eu ROA/ROE observation after the first full collection. It
accepted only an explicit numeric ratio tied to the exact legal entity and
displayed year. No ratio was calculated from profit, assets or equity, and no
parent, group, branch or similarly named bank was substituted.

## Result

Two of the six gaps were recovered:

| Project bank | Exact entity | FY2024 ROA | FY2024 ROE | Evidence |
|---|---|---:|---:|---|
| JP MORGAN EUROPE | J.P. Morgan Europe Limited, company 00938937 | 0.12% | 1.43% | Explicit historic text retained for the exact [TheBanks.eu profile](https://thebanks.eu/banks/14364); `search_indexed` because the live profile now displays FY2025 |
| TURKISH BANK UK | Turkish Bank (UK) Ltd, company 02643004 | 0.43% | 2.62% | Exact [live TheBanks.eu profile](https://thebanks.eu/banks/14440); `thebanks_profile` |

Both pairs exactly match the project's independently audited average-assets
and average-equity calculations. This is a reasonableness check only; the
ratios were accepted because TheBanks.eu explicitly stated them. Turkish Bank
UK's own FY2024 ROE of 2.61% uses year-end equity and remains a separate
bank-published evidence class.

Four FY2024 TheBanks.eu bank-years remain unresolved:

| Project bank | Exact profile | Outcome |
|---|---|---|
| AFIN BANK | [Afin Bank Limited](https://thebanks.eu/banks/19654), company 13090556 | The profile has no Performance or Financials section; no explicit FY2024 ratio recovered |
| BANK OF IRELAND UK | [Bank of Ireland (UK) Plc](https://thebanks.eu/banks/14486), company 07022885 | No Performance or Financials section; no exact-entity indexed FY2024 ratio recovered |
| SMBC | [SMBC Bank International plc](https://thebanks.eu/banks/19245), company 04684034 | Exact UK profile found, but no explicit FY2024 ROA/ROE text recovered |
| STATE BANK OF INDIA UK | [State Bank Of India (UK) Limited](https://thebanks.eu/banks/14606) | Profile has no qualifying performance ratios; parent and branch figures were rejected |

These are unresolved, not zero values and not evidence that an archive capture
does not exist. Wayback/CDX and Common Crawl per-URL archive queries remained
inaccessible in this environment, so no capture status or timestamp was
invented.

Detailed source checks are in [`fy2024_gap_check_1.md`](fy2024_gap_check_1.md)
and [`fy2024_gap_check_2.md`](fy2024_gap_check_2.md).

## Coverage impact

- The live/search-indexed collection now has 146 observations across 141 exact
  entities, including 141 FY2024 observations.
- Adding the three earlier FY2023 archive-search supplements gives 149 unique
  bank-years across the same 141 entities.
- FY2024 gaps fall from six to four; total five-year gaps fall from 578 to 576
  in the expanded view.
- No worksheet, bank-published-return store, build script, audited extract or
  downstream deliverable was changed.
