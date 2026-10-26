# TheBanks.eu Zopa FY2024 ROA/ROE methodology check

## Finding

The user's lead is substantively correct, but the current [TheBanks.eu Zopa Bank Limited profile](https://thebanks.eu/banks/19247) reports **0.42% return on assets** and **4.83% return on equity** for 2024, rather than 0.5%. The page identifies the exact UK bank entity, company number **10627575**, and separately displays 2024 annual profit of £21.78m, total assets of £6,229.05m and total equity of £497.29m.

These ratios are not KPIs published by Zopa. They can, however, be reproduced from audited line items in [Zopa Bank Limited's FY2024 Annual Report and Accounts](https://www.datocms-assets.com/23873/1747055131-zopa-bank-2024-annual-report-signed-web-based.pdf):

- Profit after tax: **£21.777m** (2023: £38.881m), statement of comprehensive income, printed p.108.
- Total assets: **£6,229.047m** (2023: £4,049.087m), statement of financial position, printed p.109.
- Total equity: **£497.291m** (2023: £404.415m), statement of financial position, printed p.109.

## Reproduction

The reported figures match profit after tax divided by the simple average of the opening and closing balance-sheet amount:

```text
Average assets = (£6,229.047m + £4,049.087m) / 2
               = £5,139.067m

ROA = £21.777m / £5,139.067m × 100
    = 0.423754%
    = 0.42% (two decimal places)

Average equity = (£497.291m + £404.415m) / 2
               = £450.853m

ROE = £21.777m / £450.853m × 100
    = 4.830177%
    = 4.83% (two decimal places)
```

This is also a useful methodology check: using only 2024 year-end assets would produce **0.35%**, and using only year-end equity would produce **4.38%**. The exact match to 0.42% and 4.83% therefore strongly indicates that TheBanks.eu uses simple opening/closing averages for these two denominators. TheBanks.eu does not state the formula on the Zopa profile, so this basis is an inference from the exact numerical reconciliation rather than a quoted site methodology.

## Why the project classified Zopa as `publishes_none`

The exact 188-page bank report does not contain “return on assets”, “return on equity”, “ROA” or “ROE”. Its dedicated KPI and alternative-performance-measure sections publish other measures, but not these ratios. Under the sweep's current convention—capture only an explicit ratio published by the bank and do not backsolve—Zopa is therefore correctly classified as `publishes_none`.

TheBanks.eu changes the evidence class: its values are **third-party calculated ratios from bank-published audited inputs**, not bank-published ratios. They are mathematically reproducible and entity-correct, but admitting them would require a deliberate extension of the project convention. If that extension is made, the records should preserve at least `calculated_by: TheBanks.eu`, `numerator: profit after tax`, `denominator: simple average total assets/equity`, and should not be mixed silently with bank-reported KPIs.
