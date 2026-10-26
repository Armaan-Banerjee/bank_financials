# FY2024 TheBanks.eu gap check: Afin, Bank of Ireland UK and J.P. Morgan Europe

Checked 14 October 2026. This note is limited to explicit TheBanks.eu-calculated
FY2024 return on assets (ROA) and return on equity (ROE) for the exact UK legal
entities assigned. It does not calculate, infer or backsolve a missing ratio and
does not substitute a parent, group, branch, predecessor or similarly named
bank.

## Result

| Project bank | Exact legal entity | FY2024 TheBanks.eu ROA | FY2024 TheBanks.eu ROE | Outcome |
|---|---|---:|---:|---|
| JP MORGAN EUROPE | J.P. Morgan Europe Limited, company 00938937 | **0.12%** | **1.43%** | Recovered from retained search-indexed TheBanks.eu profile text |
| AFIN BANK | Afin Bank Limited, company 13090556 | — | — | No explicit TheBanks.eu FY2024 ratio recovered |
| BANK OF IRELAND UK | Bank of Ireland (UK) Plc, company 07022885 | — | — | No explicit TheBanks.eu FY2024 ratio recovered |

Only the J.P. Morgan observation qualifies for collation.

## Qualifying evidence

### J.P. Morgan Europe Limited

The retained indexed result for the exact [TheBanks.eu profile
14364](https://thebanks.eu/banks/14364) explicitly states that in **2024**
J.P. Morgan Europe Limited showed **0.12% return on assets** and **1.43% return
on equity**. The same retained result identifies 2024 total assets of USD
25,449.94 million and annual profit of USD 26.78 million, and describes the
entity as the United Kingdom bank. This is direct ratio evidence; those
financial amounts were not used to derive either percentage.

Entity identity is unambiguous. The profile gives company number **00938937**,
LEI 549300EJYMJS22ND8Y17 and BIC CHASGB22PLC. The independent official
[Companies House filing history](https://find-and-update.company-information.service.gov.uk/company/00938937/filing-history)
identifies J.P. Morgan Europe Limited under the same company number and records
full accounts made up to 31 December 2024, filed 27 May 2025. JPMorgan's own
[UK statutory-financial-statements directory](https://jpmorganchaseco.gcs-web.com/ir/sec-other-filings/european-union-eu-disclosures-country/)
also lists the 2024 J.P. Morgan Europe Limited statements. These official
sources are identity and reasonableness evidence only; they are not the source
of the ratios.

Verification route: `search_indexed`. The live profile had advanced to FY2025
when checked and now displays FY2025 ROA 0.42% and ROE 4.65%. The older FY2024
text remains separately retrievable by searching the exact profile URL together
with either quoted percentage. It must not be labelled a verified Wayback or
Common Crawl snapshot because no replay was accessible.

## Non-qualifying entities

### Afin Bank Limited

The exact [TheBanks.eu profile 19654](https://thebanks.eu/banks/19654) identifies
Afin Bank Limited, company **13090556**, and says its banking start date was
October 2024. Its navigation contains Overview, Bank Identifiers and Similar
Banks only: there is no Performance or Financials section and no displayed ROA
or ROE. Searches of the exact profile ID and its prospective `/financials`,
`/market_share` and `/credit_ratings` routes produced no indexed exact-entity
FY2024 return text.

Afin's own [annual-report library](https://afinbank.com/about/annual-reports-and-disclosures/)
links its 2024 report and confirms company number 13090556; the
[2024 report](https://afinbank.com/wp-content/uploads/2025/09/Afin-Bank-Ltd-Year-End-Accounts-FV24-FINAL-SIGNED.pdf)
states that the entity received its banking licence on 18 October 2024 and was
renamed Afin Bank Limited on 22 October 2024. This supports the identity and
very short operating history, but does not supply a TheBanks.eu-calculated
ratio. No annual-account value was converted into one.

Outcome: unresolved for TheBanks.eu FY2024 ROA and ROE; this is not a zero and
does not prove that no historic capture exists.

### Bank of Ireland (UK) Plc

The exact [TheBanks.eu profile 14486](https://thebanks.eu/banks/14486) identifies
company **07022885**, LEI 213800OOT97XZGKQPY40 and BIC BOFIGB2BXXX. The live
page contains Overview, Products and Services, Credit Ratings, Bank Identifiers
and Similar Banks, but no Performance or Financials section and no displayed
ROA or ROE. The site confusingly categorises the separately incorporated UK
entity as a foreign-bank branch; this does not justify substituting The Governor
and Company of the Bank of Ireland or any Irish parent figure. Searches of the
exact profile ID and prospective financial, market-share and credit-rating
subpages returned no indexed exact-entity FY2024 ratio.

The bank's official [2024 annual report](https://www.bankofirelanduk.com/app/uploads/Annual-Report-UK-2024-web-version_.pdf)
is explicitly addressed to the members of Bank of Ireland (UK) plc. It is valid
identity/reasonableness evidence, but any bank-published FY2024 return shown
there is a different source class and is deliberately not reported here as a
TheBanks.eu figure.

Outcome: unresolved for TheBanks.eu FY2024 ROA and ROE; this is not a zero and
does not prove that no historic capture exists.

## Archive and search routes checked

- Exact TheBanks.eu profile URLs and the `/financials`, `/market_share` and
  `/credit_ratings` variants were checked directly and through targeted indexed
  searches using the exact entity name, profile ID, FY2024 and the phrases
  “return on assets” and “return on equity”.
- The normal [Internet Archive CDX endpoint](https://web.archive.org/cdx/search/cdx)
  was attempted separately for all three profile URLs, but capture enumeration
  and replay were inaccessible through the available web gateway. No capture
  timestamp or archive URL has therefore been asserted.
- The [Common Crawl collection catalogue](https://index.commoncrawl.org/collinfo.json)
  was accessible and confirms the relevant 2024–2026 indexes, but per-URL CDX
  index queries were inaccessible. No Common Crawl capture has been claimed.

The archive failures mean Afin and Bank of Ireland UK remain
**archive-access-unverified**, not verified no-capture cases. The J.P. Morgan
record is supported by explicit historic TheBanks.eu text retained by the
search index, so its appropriate provenance is `search_indexed`, not
`wayback_snapshot`.

