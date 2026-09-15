# IN-009 core-ratio quality and screening report

Source database: `/Users/armaan/code/katalysis/scripts/insights/../../research/insights.db`

## Coverage

| Metric | Mode | Observations | Banks | Years | Exclusions |
|---|---|---:|---:|---|---|
| CET1 Ratio | broad | 960 | 138 | 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026 | missing: 135, non_numeric_disclosure: 61 |
| CET1 Ratio | strict | 425 | 61 | 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026 | basis_mismatch: 239, missing: 135, non_numeric_disclosure: 61, unknown_basis: 296 |
| Tier 1 Ratio | broad | 920 | 135 | 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026 | missing: 141, non_numeric_disclosure: 76 |
| Tier 1 Ratio | strict | 404 | 60 | 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026 | basis_mismatch: 234, missing: 141, non_numeric_disclosure: 76, unknown_basis: 282 |
| Total Capital Ratio | broad | 947 | 138 | 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026 | missing: 139, non_numeric_disclosure: 56 |
| Total Capital Ratio | strict | 403 | 60 | 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026 | basis_mismatch: 236, missing: 139, non_numeric_disclosure: 56, unknown_basis: 308 |
| Leverage Ratio | broad | 1336 | 131 | 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026 | missing: 627, non_numeric_disclosure: 115 |
| Leverage Ratio | strict | 567 | 61 | 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026 | basis_mismatch: 358, missing: 627, non_numeric_disclosure: 115, unknown_basis: 411 |

Strict mode includes numeric annual observations with an explicitly classified reporting basis.
Broad mode includes numeric annual observations with a 12-month annual period; unknown basis is retained.

## Outliers

| Mode | Metric | FRN | Bank | Year | Value | Reasons |
|---|---|---:|---|---:|---:|---|
| broad | CET1 Ratio | 1004742 | AFIN BANK | 2024 | 418.5 | level above 95th percentile; robust level score at least 3.5 |
| broad | CET1 Ratio | 114276 | STANDARD CHARTERED BANK | 2025 | 11.1 | level below 5th percentile |
| broad | CET1 Ratio | 114724 | RBS | 2025 | 11.0 | level below 5th percentile |
| broad | CET1 Ratio | 121878 | NATIONAL WESTMINSTER BANK PLC | 2025 | 11.2 | level below 5th percentile |
| broad | CET1 Ratio | 122287 | COUTTS | 2025 | 11.4 | level below 5th percentile |
| broad | CET1 Ratio | 124269 | CREDIT SUISSE UK | 2025 | 191.0 | level above 95th percentile; robust level score at least 3.5; year-over-year movement above 95th percentile |
| broad | CET1 Ratio | 124579 | JP MORGAN EUROPE | 2025 | 249.23 | level above 95th percentile; robust level score at least 3.5; year-over-year movement above 95th percentile |
| broad | CET1 Ratio | 124823 | ICBC STANDARD BANK PLC | 2025 | 12.2 | level below 5th percentile |
| broad | CET1 Ratio | 146702 | CREDIT SUISSE INTERNATIONAL | 2025 | 146.9 | level above 95th percentile; robust level score at least 3.5; year-over-year movement above 95th percentile |
| broad | CET1 Ratio | 165556 | TD BANK EUROPE | 2025 | 158.0 | level above 95th percentile; robust level score at least 3.5 |
| broad | CET1 Ratio | 178737 | CATER ALLEN | 2025 | 78.2 | robust level score at least 3.5 |
| broad | CET1 Ratio | 183100 | BNY MELLON INTERNATIONAL | 2025 | 104.22 | robust level score at least 3.5 |
| broad | CET1 Ratio | 195430 | MORGAN STANLEY BANK INTERNATIONAL | 2025 | 42.6 | robust level score at least 3.5 |
| broad | CET1 Ratio | 204419 | NOMURA BANK INTERNATIONAL | 2021 | 279.68 | level above 95th percentile; robust level score at least 3.5 |
| broad | CET1 Ratio | 204478 | BIRMINGHAM BANK | 2024 | 76.0 | robust level score at least 3.5; year-over-year movement above 95th percentile |
| broad | CET1 Ratio | 204488 | BANK SADERAT | 2025 | 331.0 | level above 95th percentile; robust level score at least 3.5 |
| broad | CET1 Ratio | 204508 | METHODIST CHAPEL AID | 2023 | 52.88 | robust level score at least 3.5 |
| broad | CET1 Ratio | 204532 | PHILIPPINE NATIONAL BANK EUROPE | 2025 | 127.55 | robust level score at least 3.5 |
| broad | CET1 Ratio | 204574 | SHAWBROOK | 2025 | 12.4 | level below 5th percentile |
| broad | CET1 Ratio | 207380 | MELLI BANK | 2025 | 56.0 | robust level score at least 3.5 |
| broad | CET1 Ratio | 208019 | BANK SEPAH INTERNATIONAL | 2025 | 102.7 | robust level score at least 3.5 |
| broad | CET1 Ratio | 222030 | ICBC (LONDON) PLC | 2025 | 81.09 | robust level score at least 3.5 |
| broad | CET1 Ratio | 400712 | FIDBANK UK | 2024 | 41.28 | year-over-year movement above 95th percentile |
| broad | CET1 Ratio | 455378 | BANK OF THE PHILIPPINE ISLANDS EUROPE | 2025 | 56.29 | robust level score at least 3.5 |
| broad | CET1 Ratio | 488982 | METRO BANK | 2025 | 12.5 | level below 5th percentile |
| broad | CET1 Ratio | 695048 | UBA UK | 2024 | 49.04 | robust level score at least 3.5 |
| broad | CET1 Ratio | 730427 | MONZO | 2025 | 55.92 | robust level score at least 3.5 |
| broad | CET1 Ratio | 754568 | CLEARBANK | 2025 | 49.75 | robust level score at least 3.5 |
| broad | CET1 Ratio | 805574 | CITIBANK UK | 2023 | 72.7 | robust level score at least 3.5 |
| broad | CET1 Ratio | 850286 | GB BANK | 2025 | 19.14 | year-over-year movement above 95th percentile |
| broad | CET1 Ratio | 930379 | THE BANK OF LONDON GROUP | 2025 | 82.94 | robust level score at least 3.5 |
| broad | CET1 Ratio | 956138 | PERENNA | 2025 | 48.0 | robust level score at least 3.5; year-over-year movement above 95th percentile |
| broad | CET1 Ratio | 970920 | GRIFFIN BANK | 2025 | 112.0 | robust level score at least 3.5; year-over-year movement above 95th percentile |
| broad | Tier 1 Ratio | 1004742 | AFIN BANK | 2024 | 418.5 | level above 95th percentile; robust level score at least 3.5 |
| broad | Tier 1 Ratio | 121878 | NATIONAL WESTMINSTER BANK PLC | 2025 | 13.4 | level below 5th percentile |
| broad | Tier 1 Ratio | 124269 | CREDIT SUISSE UK | 2025 | 191.0 | level above 95th percentile; robust level score at least 3.5; year-over-year movement above 95th percentile |
| broad | Tier 1 Ratio | 124579 | JP MORGAN EUROPE | 2025 | 249.23 | level above 95th percentile; robust level score at least 3.5; year-over-year movement above 95th percentile |
| broad | Tier 1 Ratio | 124823 | ICBC STANDARD BANK PLC | 2025 | 13.3 | level below 5th percentile |
| broad | Tier 1 Ratio | 143336 | ARBUTHNOT LATHAM | 2025 | 13.26 | level below 5th percentile |
| broad | Tier 1 Ratio | 146702 | CREDIT SUISSE INTERNATIONAL | 2025 | 146.9 | robust level score at least 3.5; year-over-year movement above 95th percentile |
| broad | Tier 1 Ratio | 165556 | TD BANK EUROPE | 2025 | 158.0 | level above 95th percentile; robust level score at least 3.5 |
| broad | Tier 1 Ratio | 178737 | CATER ALLEN | 2025 | 78.2 | robust level score at least 3.5 |
| broad | Tier 1 Ratio | 183100 | BNY MELLON INTERNATIONAL | 2025 | 104.22 | robust level score at least 3.5 |
| broad | Tier 1 Ratio | 195430 | MORGAN STANLEY BANK INTERNATIONAL | 2025 | 42.6 | robust level score at least 3.5 |
| broad | Tier 1 Ratio | 204419 | NOMURA BANK INTERNATIONAL | 2021 | 279.68 | level above 95th percentile; robust level score at least 3.5 |
| broad | Tier 1 Ratio | 204478 | BIRMINGHAM BANK | 2024 | 76.0 | robust level score at least 3.5; year-over-year movement above 95th percentile |
| broad | Tier 1 Ratio | 204488 | BANK SADERAT | 2025 | 331.0 | level above 95th percentile; robust level score at least 3.5 |
| broad | Tier 1 Ratio | 204508 | METHODIST CHAPEL AID | 2023 | 52.88 | robust level score at least 3.5 |
| broad | Tier 1 Ratio | 204532 | PHILIPPINE NATIONAL BANK EUROPE | 2025 | 127.55 | robust level score at least 3.5 |
| broad | Tier 1 Ratio | 204550 | SECURE TRUST BANK | 2025 | 12.9 | level below 5th percentile |
| broad | Tier 1 Ratio | 207380 | MELLI BANK | 2025 | 56.0 | robust level score at least 3.5 |
| broad | Tier 1 Ratio | 208019 | BANK SEPAH INTERNATIONAL | 2025 | 102.7 | robust level score at least 3.5 |
| broad | Tier 1 Ratio | 208020 | PERSIA INTERNATIONAL BANK | 2021 | 40.99 | robust level score at least 3.5 |
| broad | Tier 1 Ratio | 222030 | ICBC (LONDON) PLC | 2025 | 81.09 | robust level score at least 3.5 |
| broad | Tier 1 Ratio | 400712 | FIDBANK UK | 2024 | 41.28 | robust level score at least 3.5; year-over-year movement above 95th percentile |
| broad | Tier 1 Ratio | 455378 | BANK OF THE PHILIPPINE ISLANDS EUROPE | 2025 | 56.29 | robust level score at least 3.5 |
| broad | Tier 1 Ratio | 541910 | CASTLE TRUST CAPITAL | 2025 | 13.35 | level below 5th percentile |
| broad | Tier 1 Ratio | 604551 | PARAGON | 2025 | 12.6 | level below 5th percentile |
| broad | Tier 1 Ratio | 695048 | UBA UK | 2024 | 49.04 | robust level score at least 3.5 |
| broad | Tier 1 Ratio | 730427 | MONZO | 2025 | 55.92 | robust level score at least 3.5 |
| broad | Tier 1 Ratio | 754568 | CLEARBANK | 2025 | 49.75 | robust level score at least 3.5 |
| broad | Tier 1 Ratio | 805574 | CITIBANK UK | 2023 | 81.8 | robust level score at least 3.5 |
| broad | Tier 1 Ratio | 815220 | RCI BANK UK | 2024 | 13.46 | level below 5th percentile |
| broad | Tier 1 Ratio | 850286 | GB BANK | 2025 | 19.14 | year-over-year movement above 95th percentile |
| broad | Tier 1 Ratio | 970920 | GRIFFIN BANK | 2023 | 456.0 | level above 95th percentile; robust level score at least 3.5 |
| broad | Total Capital Ratio | 1004742 | AFIN BANK | 2024 | 418.5 | level above 95th percentile; robust level score at least 3.5 |
| broad | Total Capital Ratio | 124269 | CREDIT SUISSE UK | 2025 | 191.1 | level above 95th percentile; robust level score at least 3.5; year-over-year movement above 95th percentile |
| broad | Total Capital Ratio | 124579 | JP MORGAN EUROPE | 2025 | 249.23 | level above 95th percentile; robust level score at least 3.5; year-over-year movement above 95th percentile |
| broad | Total Capital Ratio | 124823 | ICBC STANDARD BANK PLC | 2025 | 15.0 | level below 5th percentile |
| broad | Total Capital Ratio | 140848 | DB UK BANK | 2025 | 536.0 | level above 95th percentile; robust level score at least 3.5; year-over-year movement above 95th percentile |
| broad | Total Capital Ratio | 143336 | ARBUTHNOT LATHAM | 2025 | 15.38 | level below 5th percentile |
| broad | Total Capital Ratio | 146702 | CREDIT SUISSE INTERNATIONAL | 2025 | 146.9 | robust level score at least 3.5; year-over-year movement above 95th percentile |
| broad | Total Capital Ratio | 165556 | TD BANK EUROPE | 2025 | 158.0 | robust level score at least 3.5 |
| broad | Total Capital Ratio | 178737 | CATER ALLEN | 2025 | 78.2 | robust level score at least 3.5 |
| broad | Total Capital Ratio | 183100 | BNY MELLON INTERNATIONAL | 2025 | 104.22 | robust level score at least 3.5 |
| broad | Total Capital Ratio | 195430 | MORGAN STANLEY BANK INTERNATIONAL | 2025 | 58.9 | robust level score at least 3.5 |
| broad | Total Capital Ratio | 204419 | NOMURA BANK INTERNATIONAL | 2021 | 279.68 | level above 95th percentile; robust level score at least 3.5 |
| broad | Total Capital Ratio | 204478 | BIRMINGHAM BANK | 2024 | 76.0 | robust level score at least 3.5; year-over-year movement above 95th percentile |
| broad | Total Capital Ratio | 204488 | BANK SADERAT | 2025 | 331.0 | level above 95th percentile; robust level score at least 3.5 |
| broad | Total Capital Ratio | 204508 | METHODIST CHAPEL AID | 2023 | 52.88 | robust level score at least 3.5 |
| broad | Total Capital Ratio | 204532 | PHILIPPINE NATIONAL BANK EUROPE | 2025 | 127.55 | robust level score at least 3.5 |
| broad | Total Capital Ratio | 204550 | SECURE TRUST BANK | 2025 | 15.2 | level below 5th percentile |
| broad | Total Capital Ratio | 204571 | WEATHERBYS | 2025 | 15.3 | level below 5th percentile |
| broad | Total Capital Ratio | 204574 | SHAWBROOK | 2025 | 14.9 | level below 5th percentile |
| broad | Total Capital Ratio | 207380 | MELLI BANK | 2025 | 56.0 | robust level score at least 3.5 |
| broad | Total Capital Ratio | 208019 | BANK SEPAH INTERNATIONAL | 2025 | 102.7 | robust level score at least 3.5 |
| broad | Total Capital Ratio | 208020 | PERSIA INTERNATIONAL BANK | 2021 | 40.99 | robust level score at least 3.5 |
| broad | Total Capital Ratio | 219523 | BANK OF BEIRUT UK | 2025 | 41.93 | robust level score at least 3.5 |
| broad | Total Capital Ratio | 222030 | ICBC (LONDON) PLC | 2025 | 81.09 | robust level score at least 3.5 |
| broad | Total Capital Ratio | 455378 | BANK OF THE PHILIPPINE ISLANDS EUROPE | 2025 | 56.29 | robust level score at least 3.5 |
| broad | Total Capital Ratio | 604551 | PARAGON | 2025 | 14.3 | level below 5th percentile |
| broad | Total Capital Ratio | 695048 | UBA UK | 2024 | 49.04 | robust level score at least 3.5 |
| broad | Total Capital Ratio | 730427 | MONZO | 2025 | 56.67 | robust level score at least 3.5 |
| broad | Total Capital Ratio | 740551 | CHETWOOD | 2025 | 15.2 | level below 5th percentile |
| broad | Total Capital Ratio | 754568 | CLEARBANK | 2025 | 49.75 | robust level score at least 3.5 |
| broad | Total Capital Ratio | 805574 | CITIBANK UK | 2024 | 138.6 | robust level score at least 3.5; year-over-year movement above 95th percentile |
| broad | Total Capital Ratio | 850286 | GB BANK | 2025 | 19.14 | year-over-year movement above 95th percentile |
| broad | Total Capital Ratio | 970920 | GRIFFIN BANK | 2023 | 456.0 | level above 95th percentile; robust level score at least 3.5 |
| broad | Leverage Ratio | 1004742 | AFIN BANK | 2024 | 87.4 | level above 95th percentile; robust level score at least 3.5 |
| broad | Leverage Ratio | 114216 | HSBC BANK PLC | 2025 | 4.5 | level below 5th percentile |
| broad | Leverage Ratio | 114276 | STANDARD CHARTERED BANK | 2025 | 4.2 | level below 5th percentile |
| broad | Leverage Ratio | 119256 | MIZUHO INTERNATIONAL | 2025 | 4.2 | level below 5th percentile |
| broad | Leverage Ratio | 121878 | NATIONAL WESTMINSTER BANK PLC | 2025 | 4.2 | level below 5th percentile |
| broad | Leverage Ratio | 121885 | CO-OPERATIVE BANK | 2024 | 4.0 | level below 5th percentile |
| broad | Leverage Ratio | 124269 | CREDIT SUISSE UK | 2025 | 87.0 | level above 95th percentile; robust level score at least 3.5; year-over-year movement above 95th percentile |
| broad | Leverage Ratio | 124579 | JP MORGAN EUROPE | 2025 | 94.12 | level above 95th percentile; robust level score at least 3.5 |
| broad | Leverage Ratio | 146702 | CREDIT SUISSE INTERNATIONAL | 2025 | 53.08 | robust level score at least 3.5; year-over-year movement above 95th percentile |
| broad | Leverage Ratio | 169628 | BANK OF SCOTLAND | 2025 | 4.3 | level below 5th percentile |
| broad | Leverage Ratio | 204478 | BIRMINGHAM BANK | 2024 | 24.0 | year-over-year movement above 95th percentile |
| broad | Leverage Ratio | 204508 | METHODIST CHAPEL AID | 2023 | 35.4 | robust level score at least 3.5 |
| broad | Leverage Ratio | 208019 | BANK SEPAH INTERNATIONAL | 2025 | 55.0 | level above 95th percentile; robust level score at least 3.5 |
| broad | Leverage Ratio | 208020 | PERSIA INTERNATIONAL BANK | 2021 | 53.32 | level above 95th percentile; robust level score at least 3.5; year-over-year movement above 95th percentile |
| broad | Leverage Ratio | 222030 | ICBC (LONDON) PLC | 2025 | 47.48 | robust level score at least 3.5; year-over-year movement above 95th percentile |
| broad | Leverage Ratio | 455378 | BANK OF THE PHILIPPINE ISLANDS EUROPE | 2025 | 51.22 | robust level score at least 3.5 |
| broad | Leverage Ratio | 805574 | CITIBANK UK | 2024 | 76.67 | level above 95th percentile; robust level score at least 3.5; year-over-year movement above 95th percentile |
| broad | Leverage Ratio | 849724 | MONUMENT BANK | 2024 | 3.9 | level below 5th percentile |
| broad | Leverage Ratio | 953772 | KROO BANK | 2024 | 21.2 | year-over-year movement above 95th percentile |
| broad | Leverage Ratio | 956138 | PERENNA | 2025 | 21.47 | year-over-year movement above 95th percentile |
| broad | Leverage Ratio | 970920 | GRIFFIN BANK | 2023 | 91.0 | level above 95th percentile; robust level score at least 3.5 |
| strict | CET1 Ratio | 114276 | STANDARD CHARTERED BANK | 2025 | 11.1 | level below 5th percentile |
| strict | CET1 Ratio | 114724 | RBS | 2025 | 11.0 | level below 5th percentile |
| strict | CET1 Ratio | 121878 | NATIONAL WESTMINSTER BANK PLC | 2025 | 11.2 | level below 5th percentile |
| strict | CET1 Ratio | 124269 | CREDIT SUISSE UK | 2025 | 191.0 | level above 95th percentile; robust level score at least 3.5; year-over-year movement above 95th percentile |
| strict | CET1 Ratio | 178737 | CATER ALLEN | 2025 | 78.2 | robust level score at least 3.5 |
| strict | CET1 Ratio | 195430 | MORGAN STANLEY BANK INTERNATIONAL | 2025 | 42.6 | robust level score at least 3.5 |
| strict | CET1 Ratio | 204419 | NOMURA BANK INTERNATIONAL | 2021 | 279.68 | level above 95th percentile; robust level score at least 3.5 |
| strict | CET1 Ratio | 204478 | BIRMINGHAM BANK | 2024 | 76.0 | robust level score at least 3.5; year-over-year movement above 95th percentile |
| strict | CET1 Ratio | 204508 | METHODIST CHAPEL AID | 2023 | 52.88 | robust level score at least 3.5 |
| strict | CET1 Ratio | 207380 | MELLI BANK | 2025 | 56.0 | robust level score at least 3.5 |
| strict | CET1 Ratio | 208019 | BANK SEPAH INTERNATIONAL | 2025 | 102.7 | level above 95th percentile; robust level score at least 3.5 |
| strict | CET1 Ratio | 208020 | PERSIA INTERNATIONAL BANK | 2021 | 40.99 | robust level score at least 3.5 |
| strict | CET1 Ratio | 219523 | BANK OF BEIRUT UK | 2025 | 37.49 | robust level score at least 3.5 |
| strict | CET1 Ratio | 222030 | ICBC (LONDON) PLC | 2025 | 81.09 | robust level score at least 3.5 |
| strict | CET1 Ratio | 850286 | GB BANK | 2025 | 19.14 | year-over-year movement above 95th percentile |
| strict | CET1 Ratio | 956138 | PERENNA | 2025 | 48.0 | robust level score at least 3.5; year-over-year movement above 95th percentile |
| strict | Tier 1 Ratio | 121878 | NATIONAL WESTMINSTER BANK PLC | 2025 | 13.4 | level below 5th percentile |
| strict | Tier 1 Ratio | 124269 | CREDIT SUISSE UK | 2025 | 191.0 | level above 95th percentile; robust level score at least 3.5; year-over-year movement above 95th percentile |
| strict | Tier 1 Ratio | 178737 | CATER ALLEN | 2025 | 78.2 | robust level score at least 3.5 |
| strict | Tier 1 Ratio | 195430 | MORGAN STANLEY BANK INTERNATIONAL | 2025 | 42.6 | robust level score at least 3.5 |
| strict | Tier 1 Ratio | 204419 | NOMURA BANK INTERNATIONAL | 2021 | 279.68 | level above 95th percentile; robust level score at least 3.5 |
| strict | Tier 1 Ratio | 204478 | BIRMINGHAM BANK | 2024 | 76.0 | robust level score at least 3.5; year-over-year movement above 95th percentile |
| strict | Tier 1 Ratio | 204508 | METHODIST CHAPEL AID | 2023 | 52.88 | robust level score at least 3.5 |
| strict | Tier 1 Ratio | 207380 | MELLI BANK | 2025 | 56.0 | robust level score at least 3.5 |
| strict | Tier 1 Ratio | 208019 | BANK SEPAH INTERNATIONAL | 2025 | 102.7 | level above 95th percentile; robust level score at least 3.5 |
| strict | Tier 1 Ratio | 208020 | PERSIA INTERNATIONAL BANK | 2021 | 40.99 | robust level score at least 3.5 |
| strict | Tier 1 Ratio | 222030 | ICBC (LONDON) PLC | 2025 | 81.09 | robust level score at least 3.5 |
| strict | Tier 1 Ratio | 541910 | CASTLE TRUST CAPITAL | 2025 | 13.35 | level below 5th percentile |
| strict | Tier 1 Ratio | 850286 | GB BANK | 2025 | 19.14 | year-over-year movement above 95th percentile |
| strict | Total Capital Ratio | 124269 | CREDIT SUISSE UK | 2025 | 191.1 | level above 95th percentile; robust level score at least 3.5; year-over-year movement above 95th percentile |
| strict | Total Capital Ratio | 178737 | CATER ALLEN | 2025 | 78.2 | robust level score at least 3.5 |
| strict | Total Capital Ratio | 195430 | MORGAN STANLEY BANK INTERNATIONAL | 2025 | 58.9 | robust level score at least 3.5 |
| strict | Total Capital Ratio | 204419 | NOMURA BANK INTERNATIONAL | 2021 | 279.68 | level above 95th percentile; robust level score at least 3.5 |
| strict | Total Capital Ratio | 204478 | BIRMINGHAM BANK | 2024 | 76.0 | robust level score at least 3.5; year-over-year movement above 95th percentile |
| strict | Total Capital Ratio | 204508 | METHODIST CHAPEL AID | 2023 | 52.88 | robust level score at least 3.5 |
| strict | Total Capital Ratio | 204574 | SHAWBROOK | 2025 | 14.9 | level below 5th percentile |
| strict | Total Capital Ratio | 207380 | MELLI BANK | 2025 | 56.0 | robust level score at least 3.5 |
| strict | Total Capital Ratio | 208019 | BANK SEPAH INTERNATIONAL | 2025 | 102.7 | level above 95th percentile; robust level score at least 3.5 |
| strict | Total Capital Ratio | 208020 | PERSIA INTERNATIONAL BANK | 2021 | 40.99 | robust level score at least 3.5 |
| strict | Total Capital Ratio | 219523 | BANK OF BEIRUT UK | 2025 | 41.93 | robust level score at least 3.5 |
| strict | Total Capital Ratio | 222030 | ICBC (LONDON) PLC | 2025 | 81.09 | robust level score at least 3.5 |
| strict | Total Capital Ratio | 541910 | CASTLE TRUST CAPITAL | 2025 | 15.72 | level below 5th percentile |
| strict | Total Capital Ratio | 740551 | CHETWOOD | 2025 | 15.2 | level below 5th percentile |
| strict | Total Capital Ratio | 850286 | GB BANK | 2025 | 19.14 | year-over-year movement above 95th percentile |
| strict | Leverage Ratio | 121885 | CO-OPERATIVE BANK | 2024 | 4.0 | level below 5th percentile |
| strict | Leverage Ratio | 124269 | CREDIT SUISSE UK | 2025 | 87.0 | level above 95th percentile; robust level score at least 3.5; year-over-year movement above 95th percentile |
| strict | Leverage Ratio | 204478 | BIRMINGHAM BANK | 2024 | 24.0 | year-over-year movement above 95th percentile |
| strict | Leverage Ratio | 204508 | METHODIST CHAPEL AID | 2023 | 35.4 | robust level score at least 3.5 |
| strict | Leverage Ratio | 208019 | BANK SEPAH INTERNATIONAL | 2025 | 55.0 | level above 95th percentile; robust level score at least 3.5 |
| strict | Leverage Ratio | 208020 | PERSIA INTERNATIONAL BANK | 2021 | 53.32 | level above 95th percentile; robust level score at least 3.5; year-over-year movement above 95th percentile |
| strict | Leverage Ratio | 222030 | ICBC (LONDON) PLC | 2025 | 47.48 | robust level score at least 3.5 |
| strict | Leverage Ratio | 849724 | MONUMENT BANK | 2024 | 3.9 | level below 5th percentile |
| strict | Leverage Ratio | 956138 | PERENNA | 2025 | 21.47 | year-over-year movement above 95th percentile |

## Method

Levels are flagged below the 5th or above the 95th percentile, or at a robust score of at least 3.5.
Year-over-year movement is flagged above the 95th percentile of observed absolute movements.
Special or non-standard disclosures are surfaced as domain flags and are not silently discarded.
