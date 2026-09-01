# IN-004 trend-selection exception review

This report lists same-FRN/same-fiscal-year rows where more than one
label or period variant was available. It is the manual-review queue
for deciding whether the current explicit priorities are appropriate.
Rows are from `research/insights.db` (source of truth); no workbook was read or changed.

## Leverage ratio (25 FRN-year collisions)

| FRN | Bank | Year | Candidate label | Value | Basis note |
|---:|---|---:|---|---:|---|
| 106054 | SANTANDER | 2021 | Leverage ratio excluding claims on central banks (%) | 5.3 | Santander UK Plc Group (consolidated basis), £m. See source note at bottom re: a cash-equivalents definition change. |
| 106054 | SANTANDER | 2021 | Leverage ratio including claims on central banks (%) | 4.3 | Santander UK Plc Group (consolidated basis), £m. See source note at bottom re: a cash-equivalents definition change. |
| 106054 | SANTANDER | 2022 | Leverage ratio excluding claims on central banks (%) | 5.2 | Santander UK Plc Group (consolidated basis), £m. See source note at bottom re: a cash-equivalents definition change. |
| 106054 | SANTANDER | 2022 | Leverage ratio including claims on central banks (%) | 4.4 | Santander UK Plc Group (consolidated basis), £m. See source note at bottom re: a cash-equivalents definition change. |
| 106054 | SANTANDER | 2023 | Leverage ratio excluding claims on central banks (%) | 5.1 | Santander UK Plc Group (consolidated basis), £m. See source note at bottom re: a cash-equivalents definition change. |
| 106054 | SANTANDER | 2023 | Leverage ratio including claims on central banks (%) | 4.4 | Santander UK Plc Group (consolidated basis), £m. See source note at bottom re: a cash-equivalents definition change. |
| 106054 | SANTANDER | 2024 | Leverage ratio excluding claims on central banks (%) | 4.9 | Santander UK Plc Group (consolidated basis), £m. See source note at bottom re: a cash-equivalents definition change. |
| 106054 | SANTANDER | 2024 | Leverage ratio including claims on central banks (%) | 4.3 | Santander UK Plc Group (consolidated basis), £m. See source note at bottom re: a cash-equivalents definition change. |
| 106054 | SANTANDER | 2025 | Leverage ratio excluding claims on central banks (%) | 5.0 | Santander UK Plc Group (consolidated basis), £m. See source note at bottom re: a cash-equivalents definition change. |
| 106054 | SANTANDER | 2025 | Leverage ratio including claims on central banks (%) | 4.5 | Santander UK Plc Group (consolidated basis), £m. See source note at bottom re: a cash-equivalents definition change. |
| 121873 | CLYDESDALE | 2022 | Leverage ratio excluding claims on central banks (%) | 5.1 | Clydesdale Bank (CB) Group (consolidated basis), £m unless stated. FY2026 blank - see source note at bottom. |
| 121873 | CLYDESDALE | 2022 | Leverage ratio including claims on central banks (%) | 4.5 | Clydesdale Bank (CB) Group (consolidated basis), £m unless stated. FY2026 blank - see source note at bottom. |
| 121873 | CLYDESDALE | 2023 | Leverage ratio excluding claims on central banks (%) | 4.9 | Clydesdale Bank (CB) Group (consolidated basis), £m unless stated. FY2026 blank - see source note at bottom. |
| 121873 | CLYDESDALE | 2023 | Leverage ratio including claims on central banks (%) | 4.5 | Clydesdale Bank (CB) Group (consolidated basis), £m unless stated. FY2026 blank - see source note at bottom. |
| 121873 | CLYDESDALE | 2025 | Leverage ratio excluding claims on central banks (%) | 5.5 | Clydesdale Bank (CB) Group (consolidated basis), £m unless stated. FY2026 blank - see source note at bottom. |
| 121873 | CLYDESDALE | 2025 | Leverage ratio including claims on central banks (%) | 5.0 | Clydesdale Bank (CB) Group (consolidated basis), £m unless stated. FY2026 blank - see source note at bottom. |
| 121873 | CLYDESDALE | 2026 | Leverage ratio excluding claims on central banks (%) | 6.3 | Clydesdale Bank (CB) Group (consolidated basis), £m unless stated. FY2026 blank - see source note at bottom. |
| 121873 | CLYDESDALE | 2026 | Leverage ratio including claims on central banks (%) | 5.3 | Clydesdale Bank (CB) Group (consolidated basis), £m unless stated. FY2026 blank - see source note at bottom. |
| 191240 | TSB | 2021 | Leverage ratio excluding claims on central banks (%) | 4.0 | Bank (Consolidated) basis, £ million unless stated. See source note at bottom (incl. an FY2021/FY2022 restatement break). |
| 191240 | TSB | 2021 | Leverage ratio including claims on central banks (%) (FY2021 as originally reported, pre-2022 PRA methodology) | 3.6 | Bank (Consolidated) basis, £ million unless stated. See source note at bottom (incl. an FY2021/FY2022 restatement break). |
| 204570 | UNITY TRUST | 2024 | Basel III leverage ratio, incl. temporary central bank reserves exemption (%) | 11.05 | Extended entity basis (Bank + Unity EBT Limited), £'000 |
| 204570 | UNITY TRUST | 2024 | UK leverage ratio, excl. temporary central bank reserves exemption (%) | 15.97 | Extended entity basis (Bank + Unity EBT Limited), £'000 |
| 204570 | UNITY TRUST | 2025 | Basel III leverage ratio, incl. temporary central bank reserves exemption (%) | 11.45 | Extended entity basis (Bank + Unity EBT Limited), £'000 |
| 204570 | UNITY TRUST | 2025 | UK leverage ratio, excl. temporary central bank reserves exemption (%) | 12.67 | Extended entity basis (Bank + Unity EBT Limited), £'000 |
| 223304 | SMBC | 2023 | Leverage ratio excluding claims on central banks (%) | 13.8 | £m, converted from USD - see source note at bottom for FX methodology and rates used. |
| 223304 | SMBC | 2023 | Leverage ratio including claims on central banks (%) | 8.2 | £m, converted from USD - see source note at bottom for FX methodology and rates used. |
| 223304 | SMBC | 2024 | Leverage ratio excluding claims on central banks (%) | 14.8 | £m, converted from USD - see source note at bottom for FX methodology and rates used. |
| 223304 | SMBC | 2024 | Leverage ratio including claims on central banks (%) | 9.2 | £m, converted from USD - see source note at bottom for FX methodology and rates used. |
| 223304 | SMBC | 2025 | Leverage ratio excluding claims on central banks (%) | 10.1 | £m, converted from USD - see source note at bottom for FX methodology and rates used. |
| 223304 | SMBC | 2025 | Leverage ratio including claims on central banks (%) | 7.0 | £m, converted from USD - see source note at bottom for FX methodology and rates used. |
| 629564 | OAKNORTH BANK | 2023 | Leverage ratio excluding central banks | 19.1 | Bank Group basis for FY2022–FY2025; standalone Bank basis for FY2021, £'000 |
| 629564 | OAKNORTH BANK | 2023 | Leverage ratio including central banks | 14.0 | Bank Group basis for FY2022–FY2025; standalone Bank basis for FY2021, £'000 |
| 629564 | OAKNORTH BANK | 2024 | Leverage ratio excluding central banks | 18.1 | Bank Group basis for FY2022–FY2025; standalone Bank basis for FY2021, £'000 |
| 629564 | OAKNORTH BANK | 2024 | Leverage ratio including central banks | 12.0 | Bank Group basis for FY2022–FY2025; standalone Bank basis for FY2021, £'000 |
| 629564 | OAKNORTH BANK | 2025 | Leverage ratio excluding central banks | 16.0 | Bank Group basis for FY2022–FY2025; standalone Bank basis for FY2021, £'000 |
| 629564 | OAKNORTH BANK | 2025 | Leverage ratio including central banks | 11.8 | Bank Group basis for FY2022–FY2025; standalone Bank basis for FY2021, £'000 |
| 730166 | STARLING | 2021 | Leverage ratio excluding claims on central banks / UK leverage ratio (%) | 5.4 | Group/consolidated basis, £'000. FY2021: 16-month period (†). FY2026: Starling Group Holdings Limited (‡). See source note at bottom. |
| 730166 | STARLING | 2021 | Leverage ratio including claims on central banks / CRR (EU) leverage ratio (%) (FY2021 only, pre-KM1 template) | 1.9 | Group/consolidated basis, £'000. FY2021: 16-month period (†). FY2026: Starling Group Holdings Limited (‡). See source note at bottom. |
| 730427 | MONZO | 2021 | Leverage ratio excluding claims on central banks (%) | 29.3 | £'000 unless stated. FY2025/24 = Monzo Bank Holding Group Limited; FY2023-21 = Monzo Bank Limited. See source note at bottom. |
| 730427 | MONZO | 2021 | Leverage ratio including claims on central banks (%) (CRR basis, retired from FY2022) | 6.4 | £'000 unless stated. FY2025/24 = Monzo Bank Holding Group Limited; FY2023-21 = Monzo Bank Limited. See source note at bottom. |
| 759676 | BARCLAYS | 2021 | Leverage ratio excluding claims on central banks (%) | 5.6 | Barclays Bank UK Group (consolidated basis), £m unless stated |
| 759676 | BARCLAYS | 2021 | Leverage ratio including claims on central banks (%) | 4.1 | Barclays Bank UK Group (consolidated basis), £m unless stated |
| 759676 | BARCLAYS | 2022 | Leverage ratio excluding claims on central banks (%) | 5.3 | Barclays Bank UK Group (consolidated basis), £m unless stated |
| 759676 | BARCLAYS | 2022 | Leverage ratio including claims on central banks (%) | 4.3 | Barclays Bank UK Group (consolidated basis), £m unless stated |
| 759676 | BARCLAYS | 2023 | Leverage ratio excluding claims on central banks (%) | 5.2 | Barclays Bank UK Group (consolidated basis), £m unless stated |
| 759676 | BARCLAYS | 2023 | Leverage ratio including claims on central banks (%) | 4.5 | Barclays Bank UK Group (consolidated basis), £m unless stated |
| 759676 | BARCLAYS | 2024 | Leverage ratio excluding claims on central banks (%) | 5.3 | Barclays Bank UK Group (consolidated basis), £m unless stated |
| 759676 | BARCLAYS | 2024 | Leverage ratio including claims on central banks (%) | 4.7 | Barclays Bank UK Group (consolidated basis), £m unless stated |
| 759676 | BARCLAYS | 2025 | Leverage ratio excluding claims on central banks (%) | 5.2 | Barclays Bank UK Group (consolidated basis), £m unless stated |
| 759676 | BARCLAYS | 2025 | Leverage ratio including claims on central banks (%) | 4.8 | Barclays Bank UK Group (consolidated basis), £m unless stated |

## Operating cash flow (8 FRN-year collisions)

| FRN | Bank | Year | Candidate label | Value | Basis note |
|---:|---|---:|---|---:|---|
| 494549 | CHARTER COURT FINANCIAL SERVICES | 2021 | Cash generated from/(used in) operating activities | 59.6 | Entity (Company) basis, £m. See source note at bottom. |
| 494549 | CHARTER COURT FINANCIAL SERVICES | 2021 | Net cash generated from/(used in) operating activities | 12.5 | Entity (Company) basis, £m. See source note at bottom. |
| 494549 | CHARTER COURT FINANCIAL SERVICES | 2022 | Cash generated from/(used in) operating activities | -125.8 | Entity (Company) basis, £m. See source note at bottom. |
| 494549 | CHARTER COURT FINANCIAL SERVICES | 2022 | Net cash generated from/(used in) operating activities | -195.1 | Entity (Company) basis, £m. See source note at bottom. |
| 494549 | CHARTER COURT FINANCIAL SERVICES | 2023 | Cash generated from/(used in) operating activities | 315.0 | Entity (Company) basis, £m. See source note at bottom. |
| 494549 | CHARTER COURT FINANCIAL SERVICES | 2023 | Net cash generated from/(used in) operating activities | 279.1 | Entity (Company) basis, £m. See source note at bottom. |
| 494549 | CHARTER COURT FINANCIAL SERVICES | 2024 | Cash generated from/(used in) operating activities | 1388.7 | Entity (Company) basis, £m. See source note at bottom. |
| 494549 | CHARTER COURT FINANCIAL SERVICES | 2024 | Net cash generated from/(used in) operating activities | 1335.4 | Entity (Company) basis, £m. See source note at bottom. |
| 494549 | CHARTER COURT FINANCIAL SERVICES | 2025 | Cash generated from/(used in) operating activities | 757.7 | Entity (Company) basis, £m. See source note at bottom. |
| 494549 | CHARTER COURT FINANCIAL SERVICES | 2025 | Net cash generated from/(used in) operating activities | 717.4 | Entity (Company) basis, £m. See source note at bottom. |
| 606934 | HAMPDEN & CO | 2023 | Cash generated from/(used in) operating activities | -14109.0 | Company-only statement, as filed with Companies House |
| 606934 | HAMPDEN & CO | 2023 | Net cash from/(used in) operating activities | -14109.0 | Company-only statement, as filed with Companies House |
| 606934 | HAMPDEN & CO | 2024 | Cash generated from/(used in) operating activities | 86746.0 | Company-only statement, as filed with Companies House |
| 606934 | HAMPDEN & CO | 2024 | Net cash from/(used in) operating activities | 85876.0 | Company-only statement, as filed with Companies House |
| 606934 | HAMPDEN & CO | 2025 | Cash generated from/(used in) operating activities | 175165.0 | Company-only statement, as filed with Companies House |
| 606934 | HAMPDEN & CO | 2025 | Net cash from/(used in) operating activities | 175034.0 | Company-only statement, as filed with Companies House |

## How to review

For each FRN-year, confirm whether the unqualified `FY####` row is the
intended annual series. If not, note the preferred label and reporting
basis. Pay particular attention to central-bank-claims variants in
leverage and group-versus-bank or restatement variants in cash flow.
The aggregate trend counts should not be treated as final for affected
metrics until material exceptions are resolved.

Total exception groups: 33.
