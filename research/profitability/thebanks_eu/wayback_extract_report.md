# Wayback extraction — thebanks.eu captures

Generated 2026-10-16 by `extract_wayback.py` from 143 captures in `wayback_downloads/html/`.
Output: `wayback_returns.jsonl`.

## Yield

| | count |
|---|---|
| captures | 143 |
| unreadable | 0 |
| not markup | 0 |
| unmapped profile | 0 |
| ratio records | 41 |
| inputs only records | 97 |
| distinct (bank, year) with a RATIO | **40** |
| of those NOT already in the collection | **29** |
| new and inside FY2021-FY2025 | **29** |

## Ratio bank-years by period

| year | extracted | new vs collection |
|---|---|---|
| FY2022 | 14 | 13 |
| FY2023 | 16 | 16 |
| FY2024 | 10 | 0 |

thebanks.eu lags, so a capture's own date is NOT the period — a December
2024 capture typically reports 2023. The year in the page's sentence is used.

## New in-window bank-years

| bank | year |
|---|---|
| ABC INTERNATIONAL BANK | FY2023 |
| ARAB BANK EUROPE | FY2023 |
| ATOM BANK | FY2022 |
| BANK OF BEIRUT UK | FY2023 |
| BANK OF CEYLON UK | FY2023 |
| BANK OF SCOTLAND | FY2022 |
| BRITISH ARAB COMMERCIAL BANK | FY2023 |
| C HOARE AND CO | FY2023 |
| CASTLE TRUST CAPITAL | FY2022 |
| CHARITY BANK | FY2022 |
| CLYDESDALE | FY2022 |
| CYNERGY BANK | FY2023 |
| DF CAPITAL BANK | FY2023 |
| GATEHOUSE BANK | FY2022 |
| GB BANK | FY2023 |
| HABIB BANK ZURICH | FY2022 |
| HAMPSHIRE TRUST BANK | FY2023 |
| HAVIN BANK | FY2023 |
| ICBC STANDARD BANK PLC | FY2023 |
| IFAST GLOBAL BANK LIMITED | FY2023 |
| INVESTEC BANK PLC | FY2022 |
| LHV | FY2023 |
| LLOYDS BANK CORPORATE MARKETS | FY2023 |
| MARKS AND SPENCER FINANCIAL SERVICES | FY2022 |
| MORGAN STANLEY BANK INTERNATIONAL | FY2022 |
| RBS | FY2023 |
| RECOGNISE BANK | FY2022 |
| TURKISH BANK UK | FY2022 |
| ZENITH | FY2022 |

## Captures holding no figures at all

**19 of 143 captures** are navigation-only shells: real HTML, 3-6k of text,
no headline block and no ratio sentence. This is a property of what Wayback
captured, not of the extractor - and it is the honest reason some banks gain
nothing here, so it must not be read as a parsing failure.

| bank (or profile id) | empty captures |
|---|---|
| IFAST GLOBAL BANK LIMITED | 4 |
| SMBC | 4 |
| ICBC STANDARD BANK PLC | 3 |
| STATE BANK OF INDIA UK | 2 |
| ATOM BANK | 1 |
| BANK OF SCOTLAND | 1 |
| BARCLAYS BANK PLC | 1 |
| CLYDESDALE | 1 |
| GATEHOUSE BANK | 1 |
| INVESTEC BANK PLC | 1 |

Notably **SMBC** and **STATE BANK OF INDIA UK** are empty in the archive too.
The live collection found no numeric return for either, and the archive now
CORROBORATES that rather than leaving it untested.

## Positive control against the live collection

Where a capture and the live/search-indexed collection describe the same
(bank, year) they must agree, and this is the only check that can tell a
parse from a MISPARSE. It caught a dropped minus sign on the first run:
Griffin Bank FY2024 is -107.64%% ROE and was extracted as +107.64%%.

- agree exactly: **11**
- disagree: **0**

## Standing limits

- These are AGGREGATOR figures and belong in their own column. They are not
  the bank's own published return and not our computed ratio.
- No ratio was computed from the `site_inputs` figures.
- `site_inputs` is thebanks.eu's own transcription of the balance sheet, so it
  is an independent CROSS-CHECK on our inputs, not a replacement for them.

## Cross-check: thebanks.eu Total Assets vs ours

An INDEPENDENT reading of the same documents. No existing axis compares
our inputs against an outside source — `verify_workbook.py` only asks
whether two of our own transcriptions agree.

| | count |
|---|---|
| comparable bank-years | **60** |
| agree within 2% | 57 |
| agree within 10% | 58 |
| **diverge by more than 10%** | **2** |

Skipped rather than coerced (a ratio cancels its unit only if both sides
share it): converted (FX) 1, site not GBP 25

### Divergences over 10%% — LEADS, not errors

thebanks.eu is documented as mixing bases (README trap 5: Group profit
over Bank-only denominators for Lloyds), so a gap here is as likely to
be their perimeter as our transcription. Settle each against the document.

| bank | year | thebanks.eu (m) | ours (m) | theirs/ours | our unit |
|---|---|---|---|---|---|
| ABC INTERNATIONAL BANK | FY2023 | 1397.3 | 3197.3 | 0.437 | £'000 |
| LLOYDS BANK | FY2021 | 411820.0 | 602849.0 | 0.683 | £m |

