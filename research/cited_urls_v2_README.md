# cited_urls_v2.tsv — read this before using the list

Every URL cited by any `scripts/build_*.py`, extracted 2026-09-16 by an AST parse with a
**module-level symbol table** (no execution, no fetching).

Columns: `url`, `kind` (live | archive), `is_pdf` (`pdf` if the path ends `.pdf`), `cited_by`
(`;`-separated `script:constant`, `-` where the URL was found in a literal rather than a named constant).

## It supersedes `cited_urls.tsv`

The earlier file reported **1,784 distinct URLs / 1,134 PDFs**. This one finds **2,207 URLs — 2,020 live,
187 archive**, and 1,191 live PDFs once Companies House is excluded.

**Both of our earlier attempts undercounted for the same reason**, one via regex and one via a naive AST
walk: a URL assembled from a variable is invisible unless the extractor resolves names.

```python
# returned "" for an ast.Name, so this yielded only the prefix:
AR2022_URL = "https://web.archive.org/web/20240714135652id_/" + ORIG_AR2022_URL
# dropped f-string FormattedValue nodes, so this yielded ".../company//filing-history/...":
f".../company/{COMPANY_NO}/filing-history/{DOC_ID}/document?format=pdf&download=0"
```

That produced two distinct harms. It **invented** addresses present in no script — which looked exactly
like a defect class of malformed citations, and nearly got reported as one. And it **silently missed**
real documents, biased toward small banks, because their Companies House company numbers are held in
variables while large banks tend to hardcode full URLs. The fix is a symbol table resolved iteratively
(constants may be defined in terms of other constants), plus handling `FormattedValue` in f-strings.

## Caveats — these change what the list means

- **It is not provably complete.** A URL built at runtime from a computed value, a loop, or a
  comprehension is still invisible to static resolution. Treat the count as a floor, not a total.
- **It includes URLs that are not documents.** Citation prose, landing pages and Companies House
  *filing-history* pages all appear. A `/company/<number>` page is a legitimate citation but not a
  fetchable PDF; CH documents need the `/document?format=pdf&download=0` suffix.
- **`is_pdf` is a filename test, not a content test.** Some entries ending `.pdf` serve HTML
  (soft-404s), and some documents without a `.pdf` suffix are real PDFs. Only a fetch settles it.
- **It records what the scripts CITE, not what is retrievable.** Liveness is the live-sweep's job.
- **Deduplicated by exact string.** The same document cited with and without a trailing slash, or via
  both a live and an archive URL, appears twice.

## Related

- `RESUME_peer_search.md` — the running log, including the live full-download sweep results.
- `nd_targets_README.md` — the same caution about a machine-readable list being over-trusted.
