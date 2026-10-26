# TheBanks.eu coverage audit of the 65 `publishes_none` banks — 2026-10-13

## Corrected result

The earlier conclusion that TheBanks.eu filled only nine of the 65 banks was
incorrect. It counted only the project's existing sampled
`agent_findings/thebanks_eu.jsonl` file; that file was never an exhaustive
census of TheBanks.eu.

An entity-by-entity audit of all 65 banks finds that TheBanks.eu publishes at
least one FY2024 calculated return ratio for **63** of them. Therefore, when a
bank is treated as covered if it has either a bank-published return in the
project or an entity-matched TheBanks.eu FY2024 ratio, only **2 of the project's
140 banks remain without a return measure from either source**:

- **Afin Bank Limited** — its [TheBanks.eu profile](https://thebanks.eu/banks/19654)
  identifies the exact entity (company 13090556) and its October 2024 banking
  start date, but contains no financial/performance section or ROA/ROE.
- **J.P. Morgan Europe Limited** — no current UK entity profile or FY2024
  ROA/ROE could be found on TheBanks.eu. Search results only expose its closed
  Belgian branch and other J.P. Morgan entities; none is an acceptable entity
  substitute. The exact UK entity is company 00938937 in the project's source
  work.

This is an exhaustive finding for the named 65-bank list: every name was
searched individually, entity identity was checked, and the exact profile was
opened where necessary. No case is being classified as missing merely because
it was absent from the old sampled JSONL file. There were no blocked or
unsearched names.

## Tandem correction and reconciliation

The user's Tandem lead is correct, with an important year distinction. The
[exact Tandem Bank Limited profile](https://thebanks.eu/banks/14356) identifies
company **00955491** and reports:

- FY2024 ROA **0.33%** and ROE **6.89%**;
- FY2023 ROA **0.12%** (the figure raised by the user).

The ratios reconcile to the exact-bank audited accounts listed on
[Companies House](https://find-and-update.company-information.service.gov.uk/company/00955491/filing-history):

```text
FY2023 ROA = £3.600m / ((£1,926.197m + £3,859.400m) / 2) = 0.1244% = 0.12%
FY2024 ROA = £11.512m / ((£3,859.400m + £3,155.197m) / 2) = 0.3282% = 0.33%
FY2024 ROE = £11.512m / ((£156.571m + £177.679m) / 2) = 6.8881% = 6.89%
```

This also confirms the same inferred methodology found in the earlier Zopa
check: profit after tax divided by the simple average of opening and closing
total assets/equity.

## The 63 newly covered banks

All figures below are TheBanks.eu's FY2024 values. A dash means that the profile
publishes ROA but not ROE; the bank still counts as covered because the agreed
test is at least one ROA, ROE or RoTE measure.

| exact project bank / matched profile | ROA | ROE |
|---|---:|---:|
| [AIB Group (UK) Plc](https://thebanks.eu/banks/14287) | 1.90% | 10.04% |
| [Aldermore Bank Plc](https://thebanks.eu/banks/14456) | 0.83% | 12.51% |
| [Allica Bank Ltd](https://thebanks.eu/banks/19236) | 0.75% | 8.85% |
| [Arbuthnot Latham & Co Limited](https://thebanks.eu/banks/14291) | 0.66% | 11.15% |
| [Bank of Ceylon (UK) Ltd](https://thebanks.eu/banks/14482) | 0.22% | 2.39% |
| [Bank of China (UK) Ltd](https://thebanks.eu/banks/14483) | 3.81% | 19.81% |
| [Bank of the Philippine Islands (Europe) PLC](https://thebanks.eu/banks/14489) | -0.28% | -0.49% |
| [Bank Saderat plc](https://thebanks.eu/banks/14300) | 0.72% | 0.83% |
| [Birmingham Bank Limited](https://thebanks.eu/banks/14463) | -12.00% | -38.00% |
| [The Bank of New York Mellon (International) Limited](https://thebanks.eu/banks/14617) | 1.36% | 11.30% |
| [Brown Shipley & Co Limited](https://thebanks.eu/banks/14310) | 0.30% | 3.12% |
| [C Hoare & Co](https://thebanks.eu/banks/14312) | 0.96% | 13.50% |
| [CAF Bank Ltd](https://thebanks.eu/banks/14502) | 0.88% | 23.38% |
| [Castle Trust Capital PLC](https://thebanks.eu/banks/19238) | 0.02% | 0.23% |
| [Cater Allen Limited](https://thebanks.eu/banks/14318) | 2.21% | 31.46% |
| [The Charity Bank Limited](https://thebanks.eu/banks/14619) | 1.17% | 11.92% |
| [Chetwood Financial Limited](https://thebanks.eu/banks/18877) | -0.39% | -6.67% |
| [ClearBank Limited](https://thebanks.eu/banks/19239) | 0.08% | 4.71% |
| [Clydesdale Bank plc](https://thebanks.eu/banks/14321) | 0.17% | 2.67% |
| [The Co-operative Bank plc](https://thebanks.eu/banks/14436) | 0.18% | 3.48% |
| [Credit Suisse (UK) Limited](https://thebanks.eu/banks/14519) | 0.33% | 2.33% |
| [Crown Agents Bank Ltd](https://thebanks.eu/banks/14521) | 0.86% | 10.81% |
| [FCMB Bank (UK) Limited](https://thebanks.eu/banks/18084) | 0.50% | 4.29% |
| [GB Bank Limited](https://thebanks.eu/banks/19415) | -0.77% | -13.02% |
| [Goldman Sachs International Bank](https://thebanks.eu/banks/14344) | 0.51% | 10.69% |
| [Gulf International Bank (UK) Limited](https://thebanks.eu/banks/14345) | 0.13% | 5.23% |
| [Hampden & Co Plc](https://thebanks.eu/banks/18319) | 0.90% | 10.56% |
| [HBL Bank UK Limited](https://thebanks.eu/banks/14352) | 1.88% | 12.59% |
| [HSBC Innovation Bank Limited](https://thebanks.eu/banks/14604) | 1.59% | 10.23% |
| [ICICI Bank UK Plc](https://thebanks.eu/banks/14552) | 1.32% | 8.78% |
| [iFAST Global Bank Limited](https://thebanks.eu/banks/18766) | -0.50% | -4.21% |
| [Julian Hodge Bank Limited](https://thebanks.eu/banks/14367) | -0.09% | -0.93% |
| [KEXIM Bank (UK) Ltd](https://thebanks.eu/banks/14368) | 0.50% | 2.73% |
| [Kingdom Bank Ltd](https://thebanks.eu/banks/14564) | 0.22% | 2.20% |
| [Kroo Bank Limited](https://thebanks.eu/banks/19531) | -2.08% | -194.60% |
| [Melli Bank plc](https://thebanks.eu/banks/14385) | 0.64% | 0.91% |
| [Mizuho International plc](https://thebanks.eu/banks/14389) | 0.05% | 1.89% |
| [Monzo Bank Ltd](https://thebanks.eu/banks/18773) | 0.09% | 1.74% |
| [National Westminster Bank](https://thebanks.eu/banks/14395) | 0.82% | 16.58% |
| [NatWest Markets Plc](https://thebanks.eu/banks/14437) | 0.04% | 0.96% |
| [Nomura Bank International plc](https://thebanks.eu/banks/14399) | 0.12% | 2.24% |
| [Northern Bank Ltd](https://thebanks.eu/banks/14401) | 1.32% | 19.80% |
| [Oxbury Bank PLC](https://thebanks.eu/banks/19243) | 0.32% | 4.97% |
| [Perenna Bank PLC](https://thebanks.eu/banks/19532) | -33.09% | — |
| [Persia International Bank plc](https://thebanks.eu/banks/14405) | -2.01% | -2.99% |
| [Punjab National Bank (International) Limited](https://thebanks.eu/banks/14592) | 0.57% | 2.90% |
| [The Royal Bank of Scotland Plc](https://thebanks.eu/banks/19244) | 1.30% | 37.15% |
| [RCI Bank UK Limited](https://thebanks.eu/banks/19127) | 0.37% | 3.75% |
| [Recognise Bank Limited](https://thebanks.eu/banks/19356) | -2.45% | -15.97% |
| [Redwood Bank Limited](https://thebanks.eu/banks/18889) | 0.30% | 3.77% |
| [Reliance Bank Ltd](https://thebanks.eu/banks/14412) | 0.70% | 8.37% |
| [Santander Financial Services plc](https://thebanks.eu/banks/14454) | -0.39% | -7.82% |
| [Schroder & Co Ltd](https://thebanks.eu/banks/14415) | 2.07% | 23.82% |
| [StreamBank PLC](https://thebanks.eu/banks/19533) | -2.03% | -7.08% |
| [Tandem Bank Limited](https://thebanks.eu/banks/14356) | 0.33% | 6.89% |
| [TD Bank Europe Limited](https://thebanks.eu/banks/14432) | 0.21% | 3.69% |
| [The Bank of London Group Limited](https://thebanks.eu/banks/19413) | -4.40% | — |
| [THIS BANK LIMITED](https://thebanks.eu/banks/19242) | -4.80% | -127.81% |
| [Union Bancaire Privée (UK) Limited](https://thebanks.eu/banks/14598) | 0.19% | 2.46% |
| [Union Bank of India (UK) Limited](https://thebanks.eu/banks/18086) | 0.30% | 1.29% |
| [Vanquis Bank Limited](https://thebanks.eu/banks/14638) | 0.27% | 1.99% |
| [Vida Bank Limited](https://thebanks.eu/banks/19655) | 0.33% | 4.48% |
| [Zopa Bank Limited](https://thebanks.eu/banks/19247) | 0.42% | 4.83% |

## Interpretation and data-handling boundary

These values do not overturn the 65 banks' `publishes_none` classification:
that classification means the exact bank report did not explicitly publish an
eligible ratio. TheBanks.eu ratios are a separate, third-party calculated
evidence class. They should be stored with explicit provenance and should not
be silently relabelled as bank-published KPIs.

No JSONL dataset, worksheet, curated store, extract or deliverable was changed
as part of this audit.
