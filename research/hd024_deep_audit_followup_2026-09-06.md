# HD-024 deep audit follow-up — 2026-09-06

Reviewed all 18 worksheets and historical columns for Lloyds Bank Corporate Markets, Monzo, and State Bank of India (UK), with particular attention to blanks in regulatory metric and RWA sheets.

## Finding

Monzo's FY2020 regulatory figures had been incorrectly marked unavailable. Monzo's own Pillar 3 disclosure is still hosted at [monzo.com/documents/pillar_3_2020.pdf](https://monzo.com/documents/pillar_3_2020.pdf). It reports:

- CET1, Tier 1 and total capital: £142,642k (pp. 9, 13, 21–22)
- Total RWA: £202,708k (p. 11, Table d; p. 13)
- RWA breakdown: credit risk £157,594k and operational risk £45,114k (p. 11, Table d)
- Leverage exposure: £1,764,243k and leverage ratio 8.1% (pp. 10, 13, 26–28)
- LCR liquidity buffer £1,415,419k, net outflow £183,675k, and LCR 771% (p. 15, Table i)

These values were added to `scripts/build_monzo.py`, the Monzo workbook was rebuilt, and the 18-sheet structural verifier passed. FY2018–FY2019 blanks remain supported by the source review; FY2020 NSFR remains undisclosed.

Lloyds Bank Corporate Markets and State Bank of India (UK) were also rechecked. Their remaining blanks correspond to source presentation changes, years without the relevant disclosure, or genuinely absent categories; no further verified additions were identified.

