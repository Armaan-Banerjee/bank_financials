# FY2024 TheBanks.eu gap check: SMBC, SBI UK and Turkish Bank UK

Checked 14 October 2026. This note covers only the following workbook legal
entities:

- **SMBC Bank International plc** (company 04684034)
- **State Bank of India (UK) Limited** (company 10436460)
- **Turkish Bank (UK) Limited** (company 02643004)

## Result

**One qualifying FY2024 TheBanks.eu observation was recovered.** The exact
[Turkish Bank (UK) Ltd profile](https://thebanks.eu/banks/14440) states FY2024
ROA of **0.43%** and ROE of **2.62%**. SMBC Bank International plc and State
Bank of India (UK) Limited remain unresolved; they are missing observations,
not zero-valued observations.

| Project bank | Exact entity | FY2024 TheBanks.eu ROA | FY2024 TheBanks.eu ROE | Outcome |
|---|---|---:|---:|---|
| SMBC | SMBC Bank International plc | not found | not found | No exact-entity TheBanks.eu profile or indexed performance text located |
| STATE BANK OF INDIA UK | State Bank of India (UK) Limited | not found | not found | Parent-bank and UK-branch material rejected; no exact-subsidiary TheBanks.eu ratio located |
| TURKISH BANK UK | [Turkish Bank (UK) Ltd](https://thebanks.eu/banks/14440) | **0.43%** | **2.62%** | Exact live profile, displayed year 2024 |

There is therefore **one new exact-bank FY2024 observation** available for
later staging. The profile identifies the entity with BIC **TUBAGB2LXXX**,
company number **02643004**, and LEI **213800UHJUCFNA7KY464**, which matches the
workbook perimeter.

## Routes checked and acceptance test

For each exact legal name, searches targeted the ordinary
[TheBanks.eu bank-profile namespace](https://thebanks.eu/banks), including
profile, `/financials`, `/market_share` and `/credit_ratings` results. Searches
also used abbreviated and punctuation variants, and SMBC's former name,
“Sumitomo Mitsui Banking Corporation Europe Limited”. Results were accepted
only when retained TheBanks.eu text explicitly stated all of the following:

1. the exact workbook legal entity;
2. financial year 2024; and
3. a numeric Return on Assets and/or Return on Equity.

The ordinary [Wayback replay](https://web.archive.org/) and
[CDX index](https://web.archive.org/cdx/search/cdx) routes, and the public
[Common Crawl indexes](https://index.commoncrawl.org/), were also retried.
The browsing gateway returned no usable page or index result and the shell
environment could not resolve those hosts. Consequently, this check cannot
classify any candidate as “no archive capture”; archive existence remains
unverified. No snapshot timestamp, profile ID or archived URL has been
inferred.

The Turkish Bank live profile met the entity, year and numeric-ratio test. No
such result was recovered for SMBC or State Bank of India (UK). Results for a
foreign parent, a UK branch of a foreign bank, or a similarly named entity were
excluded. Figures were not calculated from profit, assets or equity.

## Exact-entity reasonableness controls (not TheBanks.eu evidence)

The banks' own accounts confirm both the intended legal perimeters and that
FY2024 profitability figures exist outside TheBanks.eu. These controls prevent
a false conclusion that a parent or branch result is an acceptable substitute:

- **SMBC Bank International plc:** its [official FY2025 annual
  report](https://www.smbcgroup.com/emea/getmedia/28eec268-62ab-4d64-b597-02b7f918c767/smbcbi-annual-report-2025.pdf)
  gives FY2024 comparative ROE of **7.5%** for the exact entity. This is a
  bank-published KPI, not a TheBanks.eu-calculated ratio, and so it is not a
  qualifying result here.
- **State Bank of India (UK) Limited:** its [official FY2024 annual
  report](https://sbiuk.statebank/documents/274771/0/SBIUK%2BLtd%2B-%2BAnnual%2BReport%2B%2B%2B2024.pdf/80699e7d-ba2e-8cc6-6726-f8bc7058261f?t=1730125796286)
  gives FY2024 ROE of **9.25%** and ROA of **1.27%**. Its stated ROA denominator
  is average interest-generating assets, so these values must not be silently
  relabelled as TheBanks.eu figures.
- **Turkish Bank (UK) Limited:** its [official FY2025 annual
  report](https://www.turkishbank.co.uk/wp-content/uploads/2026/04/Financial-Statements-TBUK-signed.pdf)
  gives FY2024 comparative ROE of **2.61%**. That is the bank's distinct
  year-end-equity KPI, while TheBanks.eu's **2.62%** agrees exactly with the
  project's audited average-equity calculation. TheBanks.eu's **0.43%** ROA
  also agrees exactly with the project's audited average-assets calculation.
  This reconciliation is only a reasonableness check; the live TheBanks.eu
  profile remains the source of both recovered ratios.

## Disposition

Turkish Bank (UK) Limited is recovered; SMBC Bank International plc and State
Bank of India (UK) Limited remain unresolved. For those two banks, the finding
is specifically “no qualifying result through accessible live/index/archive
routes”, not evidence that TheBanks.eu never displayed the ratios. The
qualifying Turkish Bank result was subsequently added to the standalone
TheBanks.eu JSONL collection. No worksheet, bank-published-return store,
script, extract or downstream deliverable was modified.
