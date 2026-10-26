# TheBanks.eu calculated-return collection: A–G

Collected 2026-10-13. Scope: the 60 project banks alphabetically from
`ABC INTERNATIONAL BANK` through `GULF INTERNATIONAL BANK UK`, inclusive.

## Outcome

- **60 exact project entities audited**.
- **58 banks / 58 numeric bank-year records collected**.
- All numeric records currently exposed by the normal indexed profile route
  carry the site's source-year label **2024**.
- **57** records contain both ROA and ROE; **Citibank UK** contains ROA only.
- **2** banks have an exact site profile but no financial/performance section
  and therefore no numeric return for any requested year: Afin Bank and Bank
  of Ireland (UK).
- No parent, group, branch or similarly named bank was substituted. In
  particular, Barclays Bank UK and Barclays Bank plc, the two Credit Suisse
  entities, and Goldman Sachs International Bank were kept distinct.

The machine-readable records, including a direct profile URL on every row, are
in [`a_g.jsonl`](a_g.jsonl). The site's profile format presents the ratio in a
sentence such as the [ABC International Bank profile](https://thebanks.eu/banks/14281),
which labels the performance year and states ROA and ROE. The collection used
only ordinary search/profile routes; no Cloudflare control was bypassed.

## Year coverage and explicit gaps

| requested year | banks with a numeric site figure | banks without a numeric site figure |
|---|---:|---:|
| FY2021 | 0 | 60 |
| FY2022 | 0 | 60 |
| FY2023 | 0 | 60 |
| FY2024 | 58 | 2 |
| FY2025 | 0 | 60 |

“Without” means no numeric ROA/ROE for that source-year was exposed by the
normal profile/search routes during this collection. It does not mean that the
ratio could not be calculated independently from accounts. The live UK
directory has begun showing some newer balance-sheet totals, but the accessible
indexed performance statements for these exact entities remain labelled 2024;
no FY2025 ratio was inferred from balance-sheet or profit data.

For each of the following 58 banks, **FY2024 is present and FY2021, FY2022,
FY2023 and FY2025 are absent**:

- ABC International Bank; Access Bank UK; AIB Group UK; Aldermore; Allica;
  Alpha Bank London; Al Rayan Bank; Arab Bank Europe / Europe Arab Bank;
  Arbuthnot Latham; Atom Bank.
- Bank Mandiri Europe; Bank of Africa UK; Bank of Beirut UK; Bank of Ceylon
  UK; Bank of China UK; Bank of Scotland; Bank of the Philippine Islands
  Europe; Bank Saderat; Bank Sepah International; Barclays Bank UK; Barclays
  Bank plc; Birmingham Bank; BLME; BNY Mellon International; British Arab
  Commercial Bank; Brown Shipley.
- C. Hoare & Co.; CAF Bank; Cambridge & Counties Bank; Castle Trust Capital;
  Cater Allen; Charity Bank; Charter Court Financial Services; Chetwood;
  Citibank UK; ClearBank; Close Brothers; Clydesdale; Co-operative Bank;
  Coutts; Credit Suisse International; Credit Suisse UK; Crown Agents Bank;
  Cynergy Bank.
- DB UK Bank; DF Capital Bank; EFG Private Bank; FCE Bank; FCMB UK; FidBank
  UK; FirstBank UK; Gatehouse Bank; GB Bank; Ghana International Bank; Goldman
  Sachs International Bank; Griffin Bank; Guaranty Trust Bank UK; Gulf
  International Bank UK.

For the following two banks, **all five requested years are absent**:

- [Afin Bank Limited](https://thebanks.eu/banks/19654): exact company
  13090556 profile, but it has no financial/performance section. The site says
  banking activity began in October 2024.
- [Bank of Ireland (UK) Plc](https://thebanks.eu/banks/14486): exact company
  07022885 profile, but it has no financial/performance section and the site
  categorises it as a branch despite also identifying the incorporated UK
  entity. Parent Bank of Ireland figures were not substituted.

## Entity controls

- `BARCLAYS` uses [Barclays Bank UK Plc](https://thebanks.eu/banks/18886),
  while `BARCLAYS BANK PLC` uses the distinct
  [Barclays Bank Plc](https://thebanks.eu/banks/14496).
- `CREDIT SUISSE INTERNATIONAL` uses
  [Credit Suisse International](https://thebanks.eu/banks/14520), while
  `CREDIT SUISSE UK` uses
  [Credit Suisse (UK) Limited](https://thebanks.eu/banks/14519).
- `GOLDMAN SACHS INTERNATIONAL BANK` uses
  [Goldman Sachs International Bank](https://thebanks.eu/banks/14344), not
  Goldman Sachs International or a wider Goldman Sachs group figure.
- The project's `ARAB BANK EUROPE` label maps to
  [EUROPE ARAB BANK PLC](https://thebanks.eu/banks/14530), the same continuing
  UK legal entity under the site's current name.
- The site values for Bank Saderat, FCMB UK and Gulf International Bank UK are
  retained even though their profile financial statements are presented in
  EUR or USD; ratios are dimensionless and the currency-basis note is preserved
  in the JSONL.

## Suspicious-value checks

The site's ratios were retained verbatim, not silently corrected.

- **Birmingham Bank:** the published -12.00% ROA and -38.00% ROE reproduce
  from audited workbook inputs using FY2024 loss after tax of £10.844m and
  simple opening/closing average assets/equity.
- **Cater Allen:** the unusually high 31.46% ROE and 2.21% ROA reproduce from
  audited inputs: £121.588m profit divided by average equity of £386.455m and
  average assets of £5,505.128m. The high ROE is therefore not a transcription
  error.
- **Griffin Bank:** the [profile](https://thebanks.eu/banks/19556) reports
  -88.98% ROA and -107.64% ROE. The exact-bank audited inputs produce about
  -89.03% and -107.72% using simple opening/closing averages. The small
  differences are consistent with source precision; the site values remain
  unchanged and are flagged as start-up-period/basis-sensitive.
- **Citibank UK:** the [profile](https://thebanks.eu/banks/19130) publishes
  FY2024 ROA of -2.73% without an ROE. The JSONL preserves `roe_pct: null`.

## Data boundary

This is a separate third-party-calculated evidence class. No worksheet, batch
file, curated profitability store, deliverable, or existing
`agent_findings/thebanks_eu.jsonl` file was changed.
