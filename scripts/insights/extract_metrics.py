"""
Normalizes every "<BANK> FINANCIALS.xlsx" workbook in banks/ into one
long-format dataset for cross-bank analysis (clustering, trend-finding).
Built for wayfinder/insights/ ticket IN-001 - see that ticket and
wayfinder/insights/map.md for the destination this serves.

Re-run this any time banks/ changes; it always regenerates its output fresh
from whatever workbooks exist on disk, and does not modify any bank workbook.

Usage:
    python3 scripts/extract_metrics.py
    python3 scripts/extract_metrics.py --out research/bank_metrics.csv

Output: one CSV row per (identity_key, sheet, row_label, year) - unique on
that key, enforced (see "Deduplication" below), where identity_key is the
FRN when matched (see "Identity key" below) - covering every Cash Flow
Statement TOTAL row and every Pillar 3 metric-sheet data row across all
built banks. Columns:
    bank               filename-derived bank name (e.g. "BARCLAYS") - kept
                       for backward compatibility with existing consumers
                       (scripts/cluster_banks.py); NOT the dedup/identity
                       key any more (see "Identity key" below) since a
                       filename rename would silently change it
    canonical_bank     the Banks List 2608.xlsx official Firm Name when FRN
                       matching succeeded, else falls back to the same value
                       as `bank`. Prefer this for anything client-facing.
    source_filename_bank  identical to `bank` - present explicitly so a
                       consumer joining on `canonical_bank` can still recover
                       the original filename-derived name without relying on
                       `bank`'s meaning being "the filename one" implicitly.
    source_workbook    basename of the input .xlsx file this row was read
                       from (e.g. "BARCLAYS FINANCIALS.xlsx") - traces every
                       row back to its exact source file, independent of
                       `bank`/`canonical_bank` naming.
    frn               FCA/PRA Firm Reference Number, matched against
                       "Banks List 2608.xlsx" where possible (blank if not
                       matched - see the unmatched-name log printed at the end)
    workbook_kind      "full" (has a populated Cash Flow Statement) or
                       "pillar3_only" (FRS 101/102 cash-flow exemption)
    sheet             "Cash Flow Statement", "Interim Pillar 3", or one of
                       PILLAR3_SHEET_NAMES
    row_label         the line item / metric label as written in the workbook
    year              year key as it appears in the workbook's column header
                       (e.g. "FY2025") - NOT normalized across banks, since
                       fiscal year-ends and window start years genuinely
                       differ bank to bank; a consumer that wants aligned
                       calendar years must handle that itself
    value_raw         the cell value exactly as stored (number, percent
                       string like "82.94%", "Not publicly disclosed", or
                       blank/None for a genuinely missing year)
    value_numeric     value_raw parsed to a float where possible (percent
                       strings stripped of "%", plain numbers passed through),
                       else blank
    is_numeric        "1" if value_numeric was populated, else "0" - lets a
                       consumer filter out non-disclosed/non-numeric rows
                       without re-parsing value_raw
    basis_note        a best-effort currency/consolidation-basis flag for the
                       bank as a whole, taken from the Cash Flow Statement (or
                       first available Pillar 3 sheet) subtitle line - e.g.
                       "consolidated basis, £m", "Company-only, GBP'000". Not
                       guaranteed complete: see CLAUDE.md and
                       Build Effort Review.md for the fuller catalogue of
                       per-bank basis/FX/entity quirks this single flag can't
                       capture. Treat as a coarse filter, not a substitute for
                       reading a specific bank's own sheet notes.

Coverage/skip counts print to stdout at the end - the ticket asks for that
summary to be recorded in wayfinder/insights/tickets/IN-001.md's Progress
section after a run, not just left in the terminal.

Deduplication: 35 exact-duplicate rows were found in the first version of
this dataset - some workbooks' Cash Flow Statement restates "Cash and cash
equivalents at end of year" a second time as the total of a "...comprise"
breakdown section immediately below the main reconciliation, with identical
values both times (confirmed by inspection, e.g. ALLICA FINANCIALS.xlsx rows
52 and 56). Before writing output, rows are grouped by the identity key
below; an identical-valued duplicate group is collapsed to one row, and a
group with CONFLICTING values raises a hard error naming the identity key/
sheet/row/year and the conflicting values, rather than silently picking one.

Identity key: deduplication and any other per-bank grouping in this script
key on FRN, not on `bank` (the filename-derived name), because a workbook
filename could be renamed without the underlying entity changing - FRN is
the stable identity, exactly the reason IN-001 spent real effort resolving
it accurately (including disambiguating real sibling entities like Barclays
Bank PLC vs Barclays Bank UK PLC). The tiny number of rows where FRN
matching fails (`frn` blank) fall back to `bank` for grouping purposes only,
logged as a warning - there were zero such cases as of the last run.

Structural-omission warnings print to stderr (and are summarized at the end)
whenever a workbook's expected header can't be found, a recognised sheet
produces zero extractable rows, or a whole workbook produces zero output
rows. A Pillar-3-only bank's Cash Flow Statement sheet legitimately has zero
extractable TOTAL rows by design (that's how workbook_kind is determined) -
still warned on, per spec, but worded to say so rather than reading as a bug.

Schema version: SCHEMA_VERSION below is bumped on any column
addition/removal/rename or semantic change to an existing column. A
companion `<out>.schema.json` manifest is written alongside the CSV on every
run, listing the version, the exact column order, and a generation
timestamp, so a downstream script can assert on it before consuming the CSV
rather than silently breaking on a shape it didn't expect.
"""

import argparse
import csv
import glob
import json
import os
import re
import sys
from datetime import datetime, timezone

import openpyxl

# bank_workbook.py lives in scripts/ (shared with the bank-build scripts),
# one level up from this scripts/insights/ package.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from bank_workbook import PILLAR3_SHEET_NAMES
from in009_analysis import normalize_period

BANKS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "banks")
BANK_LIST_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "Banks List 2608.xlsx")
DEFAULT_OUT = os.path.join(os.path.dirname(__file__), "..", "..", "research", "bank_metrics.csv")

# Bump on any column addition/removal/rename or semantic change to an
# existing column - see the module docstring's "Schema version" note.
SCHEMA_VERSION = "1.2"  # interim extraction is staged separately from annual output
FIELDNAMES = [
    "bank", "canonical_bank", "source_filename_bank", "source_workbook",
    "frn", "workbook_kind", "sheet", "row_label", "year",
    "value_raw", "value_numeric", "is_numeric", "basis_note",
    "unit", "reporting_basis", "restatement_note", "source_note",
]

_PERCENT_RE = re.compile(r"^\s*(-?[\d,]+\.?\d*)\s*%\s*$")
_NUMERIC_STR_RE = re.compile(r"^\s*-?[\d,]+\.?\d*\s*$")
_SUFFIX_RE = re.compile(
    r"\b(PLC|LIMITED|LTD|PUBLIC|COMPANY|CO|AND|BANK|BANKING|GROUP|INC)\b"
)
# Deliberately NOT stripped: UK, EUROPE, INTERNATIONAL - these distinguish
# real sibling entities (e.g. Barclays Bank PLC vs Barclays Bank UK PLC,
# Credit Suisse UK vs Credit Suisse International), confirmed by the
# FRN-collision check run while building this tool.

# Well-known abbreviations that no amount of suffix-stripping/containment
# matching can derive from the official Banks List 2608.xlsx name - filled
# in as unmatched cases surfaced during IN-001 (wayfinder/insights/). Keyed
# by the filename-derived bank name (normalized full form).
_ALIASES = {
    "BLME": "BANK OF LONDON AND THE MIDDLE EAST",
    "BNY MELLON INTERNATIONAL": "THE BANK OF NEW YORK MELLON INTERNATIONAL LIMITED",
    "RBS": "THE ROYAL BANK OF SCOTLAND PUBLIC LIMITED COMPANY",
    "UBA UK": "UNITED BANK FOR AFRICA UK LIMITED",
}


def _strip_accents(s):
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def normalize_name(name):
    """Uppercase, strip accents/punctuation, and drop common corporate-form/
    generic words, for fuzzy bank-name matching. Deliberately lossy - used
    only to find candidate matches, with containment as a fallback, not as
    proof of identity. Periods are dropped without inserting a space so
    "J.P." normalizes to "JP", not "J P"."""
    n = _strip_accents(name).upper()
    n = n.replace(".", "")
    n = re.sub(r"[,()&']", " ", n)
    n = re.sub(r"\s+", " ", n).strip()
    core = _SUFFIX_RE.sub(" ", n)
    core = re.sub(r"\s+", " ", core).strip()
    return n, core


def load_bank_list():
    """Returns list of (firm_name, frn, normalized_full, normalized_core)."""
    wb = openpyxl.load_workbook(BANK_LIST_PATH, read_only=True)
    ws = wb.active
    entries = []
    header_row = None
    for r, row in enumerate(ws.iter_rows(min_row=1, max_row=20, values_only=True), start=1):
        if row[0] == "Firm Name":
            header_row = r
            break
    if header_row is None:
        raise RuntimeError("Could not find 'Firm Name' header row in Banks List 2608.xlsx")
    for row in ws.iter_rows(min_row=header_row + 1, values_only=True):
        firm_name, frn, lei = row[0], row[1], row[2]
        if not firm_name:
            continue
        full, core = normalize_name(str(firm_name))
        entries.append((str(firm_name), frn, full, core))
    return entries


def match_frn(bank_name, bank_list):
    full, core = normalize_name(bank_name)
    if full in _ALIASES:
        full, core = normalize_name(_ALIASES[full])
    for firm_name, frn, e_full, e_core in bank_list:
        if full == e_full or core == e_core:
            return frn, firm_name
    # containment fallback, either direction, on the core (suffix-stripped) form
    candidates = [
        (firm_name, frn)
        for firm_name, frn, e_full, e_core in bank_list
        if e_core and core and (core in e_core or e_core in core)
    ]
    if len(candidates) == 1:
        return candidates[0][1], candidates[0][0]
    return None, None


def is_bold(ws, row, col):
    cell = ws.cell(row=row, column=col)
    return bool(cell.font and cell.font.bold)


def find_header_row(ws, label_col_values, max_scan=6):
    """Find the row whose column-A value is one of label_col_values (e.g.
    'Line item' or 'Metric')."""
    for r in range(1, max_scan + 1):
        if ws.cell(row=r, column=1).value in label_col_values:
            return r
    return None


def parse_numeric(value):
    # bool is a subclass of int in Python, so isinstance(value, (int, float))
    # alone would silently parse a stray boolean cell as 1.0/0.0 - excluded
    # explicitly even though real spreadsheet cell values essentially never
    # hit this path.
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        m = _PERCENT_RE.match(value)
        if m:
            return float(m.group(1).replace(",", ""))
        if _NUMERIC_STR_RE.match(value):
            return float(value.replace(",", ""))
    return None


def _first_nonblank_after(ws, start_row, max_scan=10):
    """Scans forward from start_row for the first non-blank column-A cell
    (skipping blank rows), up to max_scan rows. Used to find the
    source-citation cell that follows a sheet's data (and optional Note:
    row), per bank_workbook.py's _write_source_cell convention."""
    for r in range(start_row, start_row + max_scan):
        value = ws.cell(row=r, column=1).value
        if value not in (None, ""):
            return value
    return None


def extract_cash_flow_totals(ws, header_row, years, ncols):
    """Mirrors verify_workbook.py's row_kind logic: bold col A + any data in
    the year columns => TOTAL row. Returns list of (label, {year: value})."""
    totals = []
    last_row = header_row
    for r in range(header_row + 1, ws.max_row + 1):
        if ws.cell(row=r, column=1).value in (None, ""):
            break
        last_row = r
    for r in range(header_row + 1, last_row + 1):
        a_bold = is_bold(ws, r, 1)
        label = ws.cell(row=r, column=1).value
        if not a_bold:
            continue
        row_values = {y: ws.cell(row=r, column=ci).value for ci, y in enumerate(years, start=2)}
        any_data = any(v is not None for v in row_values.values())
        if any_data:
            totals.append((label, row_values))
    return totals


def get_cash_flow_source_note(ws, header_row):
    """The Cash Flow Statement sheet doesn't have a separate 'Note:' row
    convention distinct from its citation cell (an entity/restatement note,
    when present, is usually folded into the one big citation cell itself -
    see e.g. ABC International Bank's ENTITY NOTE). So this captures just
    that one citation cell's full text as source_note; restatement_note is
    left None for Cash Flow Statement rows rather than guessing where a
    restatement note ends and the citation begins within one merged cell."""
    last_row = header_row
    for r in range(header_row + 1, ws.max_row + 1):
        if ws.cell(row=r, column=1).value in (None, ""):
            break
        last_row = r
    return _first_nonblank_after(ws, last_row + 1)


def extract_metric_rows(ws, years):
    """Metric sheets have header row fixed at 3 ('Metric', year...) per
    add_metric_sheet. Data rows follow until a blank row, a 'Note:' row, or
    the source-citation row. Thin wrapper over extract_metric_sheet_full()
    for callers that only want the rows."""
    header_row = find_header_row(ws, {"Metric"})
    if header_row is None:
        return []
    rows, _, _ = extract_metric_sheet_full(ws, years, header_row)
    return rows


def extract_metric_sheet_full(ws, years, header_row):
    """Returns (rows, restatement_note, source_note). `restatement_note` is
    the sheet's 'Note: ...' row text when present (a real, mechanically-
    extractable field - e.g. TSB's Leverage Ratio restatement explanation);
    `source_note` is the citation cell that always follows (per
    bank_workbook.py's _write_source_cell convention)."""
    rows = []
    r = header_row + 1
    restatement_note = None
    while r <= ws.max_row:
        label = ws.cell(row=r, column=1).value
        if label in (None, ""):
            break
        if isinstance(label, str) and label.startswith("Note:"):
            restatement_note = label[len("Note:"):].strip()
            r += 1
            break
        row_values = {y: ws.cell(row=r, column=ci).value for ci, y in enumerate(years, start=2)}
        rows.append((label, row_values))
        r += 1
    source_note = _first_nonblank_after(ws, r)
    return rows, restatement_note, source_note


def classify_interim_basis(text):
    """Return a conservative basis category for an interim row's Basis cell."""
    value = (text or "").lower()
    if re.search(r"\b(entity|standalone|solo|company[- ]only|bank \(solo\))\b", value):
        return "entity"
    if re.search(r"\b(consolidated|group|regulatory group)\b", value):
        return "consolidated_group"
    return None


def extract_interim_sheet(ws):
    """Extract the long-form ``Interim Pillar 3`` sheet.

    These sheets use columns Metric, Unit, Basis, followed by arbitrary
    quarter/half-year/date labels.  The period label is deliberately retained
    verbatim in ``year``; ``in009_analysis.normalize_period`` classifies it as
    non-annual rather than pretending it is an FY observation.
    """
    header_row = find_header_row(ws, {"Metric"})
    if header_row is None:
        return [], "Interim Pillar 3: expected header ('Metric') not found"
    periods = [ws.cell(row=header_row, column=c).value for c in range(4, ws.max_column + 1)]
    rows = []
    for r in range(header_row + 1, ws.max_row + 1):
        label = ws.cell(row=r, column=1).value
        if label in (None, "") or (isinstance(label, str) and label.startswith("Note:")):
            break
        unit = ws.cell(row=r, column=2).value
        basis = ws.cell(row=r, column=3).value
        # Some researched workbooks append a source register below the metric
        # table.  Its first column also contains dates, so the presence of a
        # real metric unit is the reliable boundary between observations and
        # provenance rows.  ``n/a`` rows are headings/notes, not observations.
        if unit in (None, ""):
            break
        if str(unit).strip().lower() in {"n/a", "na"}:
            continue
        for offset, period in enumerate(periods, start=4):
            if period in (None, ""):
                continue
            rows.append({
                "label": label,
                "period": str(period).strip(),
                "source_cell": f"{chr(64 + offset) if offset <= 26 else 'A'}{r}",
                "value": ws.cell(row=r, column=offset).value,
                "unit": str(unit).strip() if unit not in (None, "") else None,
                "basis": str(basis).strip() if basis not in (None, "") else None,
            })
    return rows, None


_INTERIM_METRIC_KEYS = {
    "cet1 capital": "capital.cet1", "common equity tier 1 (cet1) capital": "capital.cet1",
    "tier 1 capital": "capital.tier1", "total capital": "capital.total",
    "total risk-weighted exposure amount": "rwa.total", "total risk-weighted exposures": "rwa.total",
    "cet1 ratio": "ratio.cet1", "common equity tier 1 (cet1) ratio": "ratio.cet1",
    "tier 1 ratio": "ratio.tier1", "total capital ratio": "ratio.total_capital",
    "leverage ratio": "ratio.leverage", "net stable funding ratio (nsfr)": "ratio.nsfr",
    "nsfr": "ratio.nsfr", "liquidity coverage ratio (lcr)": "ratio.lcr", "lcr": "ratio.lcr",
}


def _interim_metric_key(label):
    key = re.sub(r"\s+", " ", str(label).strip().lower())
    return _INTERIM_METRIC_KEYS.get(key, None), "mapped" if key in _INTERIM_METRIC_KEYS else "unmapped"


def extract_interim_source_register(ws):
    """Keep the optional source register as evidence, not observations."""
    for r in range(1, ws.max_row + 1):
        if ws.cell(r, 1).value == "Period" and ws.cell(r, 2).value == "Disclosure type":
            result = []
            for rr in range(r + 1, ws.max_row + 1):
                period = ws.cell(rr, 1).value
                if period in (None, ""):
                    break
                document = ws.cell(rr, 3).value
                locator = ws.cell(rr, 4).value
                result.append({"registry_row": rr, "period_label_raw": str(period),
                               "disclosure_type_raw": ws.cell(rr, 2).value,
                               "source_document_raw": document, "source_locator_raw": locator,
                               "source_url": document if isinstance(document, str) and document.startswith("http") else None})
            return result
    return []


def build_interim_records(path, frn):
    """Build database-ready interim facts and source-register records."""
    wb = openpyxl.load_workbook(path, data_only=True)
    if "Interim Pillar 3" not in wb.sheetnames:
        wb.close()
        return [], []
    ws = wb["Interim Pillar 3"]
    rows, warning = extract_interim_sheet(ws)
    register = extract_interim_source_register(ws)
    source_workbook = os.path.basename(path)
    observations = []
    for row in rows:
        metadata = normalize_period(row["period"])
        metric_key, normalization_status = _interim_metric_key(row["label"])
        value_numeric = parse_numeric(row["value"])
        period_type = metadata["period_type"]
        observations.append({
            "frn": int(frn), "source_workbook": source_workbook, "source_sheet": "Interim Pillar 3",
            "source_cell": row["source_cell"],
            "row_label_raw": str(row["label"]), "metric_key": metric_key,
            "normalization_status": normalization_status, "unit_raw": row["unit"],
            "basis_raw": row["basis"], "reporting_basis": classify_interim_basis(row["basis"]),
            "period_label_raw": row["period"], "period_type": period_type,
            "period_end_date": metadata.get("period_end"),
            "period_precision": "exact" if metadata.get("period_end") and re.fullmatch(r"\d{4}-\d{2}-\d{2}", row["period"]) else "inferred_or_unknown",
            "period_end_year": metadata.get("fiscal_year"), "period_end_month": None,
            "period_sequence": None, "period_length_months": metadata.get("period_length_months"),
            "annual_status": "interim", "value_raw": "" if row["value"] is None else row["value"],
            "value_numeric": value_numeric, "is_numeric": int(value_numeric is not None),
            "sheet_note": warning,
        })
    for item in register:
        item.update({"frn": int(frn), "source_workbook": source_workbook,
                     "source_sheet": "Interim Pillar 3", "mapping_scope": "period_register"})
    wb.close()
    return observations, register


_UNIT_SUFFIX_RE = re.compile(r"\(([^)]*)\)\s*$")


def get_years(ws, header_row):
    ncols = ws.max_column
    raw_years = [ws.cell(row=header_row, column=c).value for c in range(2, ncols + 1)]
    # strip a trailing unit suffix like " (£m)" that add_cash_flow_sheet appends
    years = []
    for y in raw_years:
        if y is None:
            years.append(None)
            continue
        years.append(re.sub(r"\s*\([^)]*\)\s*$", "", str(y)).strip())
    return years, ncols


def get_cash_flow_unit(ws, header_row, ncols):
    """The Cash Flow Statement's year-column headers often carry a unit
    suffix get_years() strips for the `year` field itself (e.g. "FY2025
    (£m)") - captured here separately rather than discarded, since it's a
    genuine per-sheet unit. Pillar 3 ratio sheets don't get this: their
    values are already self-contained percentage strings ("14.5%"), so
    there's no separate unit to extract - unit stays None there, not
    guessed or forced. Returns the first suffix found among the year
    headers (they're consistent within a sheet in every workbook checked)."""
    for c in range(2, ncols + 1):
        value = ws.cell(row=header_row, column=c).value
        if value:
            match = _UNIT_SUFFIX_RE.search(str(value))
            if match:
                return match.group(1).strip()
    return None


def get_entity_title(wb):
    """Sheet A1 titles are written as "<Entity Name> - <Sheet Name>" (see
    bank_workbook.py's add_metric_sheet/add_cash_flow_sheet). Several banks
    share a near-identical filename-derived name with a legally distinct
    sibling entity (e.g. "BARCLAYS" -> Barclays Bank UK Group vs
    "BARCLAYS BANK PLC" -> Barclays Bank PLC; similarly the two Credit Suisse
    and two HSBC entities) - the sheet title is the disambiguating source,
    the filename alone is not."""
    for sheet_name in ["Cash Flow Statement"] + PILLAR3_SHEET_NAMES:
        if sheet_name in wb.sheetnames:
            title = wb[sheet_name].cell(row=1, column=1).value
            if title and " — " in str(title):
                return str(title).rsplit(" — ", 1)[0].strip()
    return None


def get_basis_note(wb):
    for sheet_name in ["Cash Flow Statement"] + PILLAR3_SHEET_NAMES:
        if sheet_name in wb.sheetnames:
            note = wb[sheet_name].cell(row=2, column=1).value
            if note:
                return str(note)
    return None


def process_workbook(path, bank_list):
    source_workbook = os.path.basename(path)
    bank_name = source_workbook.replace(" FINANCIALS.xlsx", "").strip()
    warnings = []
    wb = openpyxl.load_workbook(path, data_only=True)
    entity_title = get_entity_title(wb)
    frn, matched_name = (None, None)
    if entity_title:
        frn, matched_name = match_frn(entity_title, bank_list)
    if frn is None:
        frn, matched_name = match_frn(bank_name, bank_list)
    canonical_bank = matched_name if frn is not None else bank_name
    basis_note = get_basis_note(wb)

    rows_out = []
    workbook_kind = "pillar3_only"

    if "Cash Flow Statement" in wb.sheetnames:
        ws = wb["Cash Flow Statement"]
        header_row = find_header_row(ws, {"Line item"})
        if header_row is None:
            warnings.append("Cash Flow Statement: expected header ('Line item') not found")
        else:
            years, ncols = get_years(ws, header_row)
            totals = extract_cash_flow_totals(ws, header_row, years, ncols)
            cf_unit = get_cash_flow_unit(ws, header_row, ncols)
            cf_source_note = get_cash_flow_source_note(ws, header_row)
            if totals:
                workbook_kind = "full"
            else:
                warnings.append(
                    "Cash Flow Statement: no extractable TOTAL rows "
                    "(expected for a genuine Pillar-3-only bank; a bug otherwise)"
                )
            for label, values in totals:
                for y, v in values.items():
                    if y is None:
                        continue
                    rows_out.append(_row(
                        bank_name, canonical_bank, frn, source_workbook, workbook_kind,
                        "Cash Flow Statement", label, y, v, basis_note,
                        unit=cf_unit, reporting_basis=None,
                        restatement_note=None, source_note=cf_source_note,
                    ))

    for sheet_name in PILLAR3_SHEET_NAMES:
        if sheet_name not in wb.sheetnames:
            continue
        ws = wb[sheet_name]
        header_row = find_header_row(ws, {"Metric"})
        if header_row is None:
            warnings.append(f"{sheet_name}: expected header ('Metric') not found")
            continue
        years, ncols = get_years(ws, header_row)
        metric_rows, restatement_note, source_note = extract_metric_sheet_full(ws, years, header_row)
        if not metric_rows:
            warnings.append(f"{sheet_name}: no extractable rows")
        for label, values in metric_rows:
            for y, v in values.items():
                if y is None:
                    continue
                rows_out.append(_row(
                    bank_name, canonical_bank, frn, source_workbook, workbook_kind,
                    sheet_name, label, y, v, basis_note,
                    unit=None, reporting_basis=None,
                    restatement_note=restatement_note, source_note=source_note,
                ))

    if not rows_out:
        warnings.append("workbook produced ZERO output rows across every sheet")

    return bank_name, frn, matched_name, canonical_bank, workbook_kind, rows_out, warnings


def _row(bank, canonical_bank, frn, source_workbook, workbook_kind, sheet, label, year, value_raw, basis_note,
         unit=None, reporting_basis=None, restatement_note=None, source_note=None):
    value_numeric = parse_numeric(value_raw)
    return {
        "bank": bank,
        "canonical_bank": canonical_bank,
        "source_filename_bank": bank,
        "source_workbook": source_workbook,
        "frn": frn if frn is not None else "",
        "workbook_kind": workbook_kind,
        "sheet": sheet,
        "row_label": label,
        "year": year,
        "value_raw": "" if value_raw is None else value_raw,
        "value_numeric": "" if value_numeric is None else value_numeric,
        "is_numeric": "1" if value_numeric is not None else "0",
        "basis_note": basis_note or "",
        # Schema-completeness fields (item 5) - genuinely optional, "" (not
        # a fabricated value) when this sheet/row doesn't have one. See
        # get_cash_flow_unit()/extract_metric_sheet_full()'s own docstrings
        # for exactly what is and isn't attempted here.
        "unit": unit or "",
        "reporting_basis": reporting_basis or "",
        "restatement_note": restatement_note or "",
        "source_note": source_note or "",
    }


def deduplicate(rows):
    """Groups `rows` by identity key (FRN, falling back to `bank` when FRN
    is blank) + sheet + row_label + year. An identical-valued duplicate
    group collapses to one row; a group with conflicting `value_raw` values
    raises ValueError naming the key and the conflicting values. Returns
    (deduped_rows, n_duplicate_groups, fallback_identity_banks) - the third
    element is the set of `bank` values that had to fall back from FRN.
    Extracted as a standalone function so scripts/test_extract_metrics.py
    can exercise it directly without needing real workbook files."""
    fallback_identity_banks = set()

    def identity_key(r):
        if r["frn"] not in (None, ""):
            return r["frn"]
        fallback_identity_banks.add(r["bank"])
        return r["bank"]

    groups = {}
    for r in rows:
        key = (identity_key(r), r["sheet"], r["row_label"], r["year"])
        groups.setdefault(key, []).append(r)

    deduped_rows = []
    n_duplicate_groups = 0
    for key, group in groups.items():
        if len(group) == 1:
            deduped_rows.append(group[0])
            continue
        n_duplicate_groups += 1
        distinct_values = {r["value_raw"] for r in group}
        if len(distinct_values) > 1:
            ident, sheet, label, year = key
            raise ValueError(
                f"Conflicting duplicate rows for identity_key={ident!r} sheet={sheet!r} "
                f"row_label={label!r} year={year!r}: values={sorted(distinct_values)}"
            )
        # Rows agreeing on value_raw could still disagree on unit or
        # reporting_basis - silently collapsing to group[0] in that case
        # would hide exactly the field class already responsible for three
        # confirmed pipeline bugs (wrong unit/basis attribution). Treat it
        # with the same loud-failure discipline as a value conflict rather
        # than picking one silently.
        distinct_units = {r.get("unit", "") for r in group}
        distinct_bases = {r.get("reporting_basis", "") for r in group}
        if len(distinct_units) > 1 or len(distinct_bases) > 1:
            ident, sheet, label, year = key
            raise ValueError(
                f"Duplicate rows for identity_key={ident!r} sheet={sheet!r} "
                f"row_label={label!r} year={year!r} agree on value_raw but "
                f"disagree on unit={sorted(distinct_units)} or "
                f"reporting_basis={sorted(distinct_bases)}"
            )
        deduped_rows.append(group[0])

    return deduped_rows, n_duplicate_groups, fallback_identity_banks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=DEFAULT_OUT)
    parser.add_argument(
        "--db", default=os.path.join(os.path.dirname(__file__), "..", "..", "research", "insights.db"),
        help="SQLite database this script writes to as its primary output "
             "(source of truth, per wayfinder/insights/ ticket IN-008) - "
             "--out's CSV is then exported FROM this database, not written independently.",
    )
    parser.add_argument(
        "--banks-dir", default=BANKS_DIR,
        help="directory of *.xlsx workbooks to extract from (default: the real banks/ "
             "directory). Overridable so the per-workbook error-continuation path (a "
             "corrupt/unreadable file is caught, logged, and skipped rather than "
             "crashing the whole run) can be tested against a small fixture directory "
             "instead of the real, always-clean banks/ directory.",
    )
    args = parser.parse_args()

    bank_list = load_bank_list()
    paths = sorted(glob.glob(os.path.join(args.banks_dir, "*.xlsx")))

    all_rows = []
    all_interim = []
    all_interim_register = []
    unmatched = []
    kind_counts = {"full": 0, "pillar3_only": 0}
    errors = []
    all_warnings = []  # (bank_name, message)

    for path in paths:
        try:
            bank_name, frn, matched_name, canonical_bank, workbook_kind, rows, warnings = \
                process_workbook(path, bank_list)
        except Exception as exc:
            errors.append((path, str(exc)))
            print(f"  !! failed to process {path}: {exc}", file=sys.stderr)
            continue
        kind_counts[workbook_kind] += 1
        if frn is None:
            unmatched.append(bank_name)
        for msg in warnings:
            all_warnings.append((bank_name, msg))
            print(f"  !! {bank_name}: {msg}", file=sys.stderr)
        all_rows.extend(rows)
        if frn is not None:
            interim, register = build_interim_records(path, frn)
            all_interim.extend(interim)
            all_interim_register.extend(register)

    # -- deduplication on (identity_key, sheet, row_label, year) ------------
    # identity_key is FRN when matched - stable under a filename rename,
    # unlike `bank`. Falls back to `bank` only for the (currently zero) rows
    # where FRN matching failed, logged so the fallback isn't silent.
    all_rows, n_duplicate_groups, fallback_identity_banks = deduplicate(all_rows)
    if fallback_identity_banks:
        print(
            f"  !! deduplication fell back to `bank` (not FRN) for unmatched "
            f"banks: {sorted(fallback_identity_banks)}",
            file=sys.stderr,
        )

    # -- coverage stats computed AFTER deduplication -------------------------
    per_sheet_coverage = {}  # sheet -> [populated, missing, non_numeric]
    for r in all_rows:
        stats = per_sheet_coverage.setdefault(r["sheet"], [0, 0, 0])
        if r["value_raw"] == "":
            stats[1] += 1
        elif r["is_numeric"] == "1":
            stats[0] += 1
        else:
            stats[2] += 1

    # -- write to the database FIRST (source of truth, IN-008) --------------
    # then export the CSV by reading it back from the database, rather than
    # writing CSV independently from `all_rows` - this is what makes the
    # database authoritative rather than just "also populated": the CSV is
    # provably derived from it, not a second independent copy that could drift.
    import build_insights_db as _db
    conn = _db.connect(args.db)
    try:
        n_banks, n_metrics = _db.write_banks_and_metrics(
            conn, all_rows, metrics_source=f"{os.path.basename(__file__)} direct write"
        )
        n_interim, n_register = _db.write_interim_observations(
            conn, all_interim, all_interim_register
        )
        # A metrics refresh can temporarily coexist with an independently
        # refreshed parent map, but never report success while the database
        # contains orphaned relationships or malformed metric rows.
        # `expected_banks` must be a TRUE independent expectation (workbooks
        # actually found on disk, minus ones that already failed above), not
        # `n_banks` (the count this run just wrote) - checking a reduced
        # count against itself always "passes" even when a workbook silently
        # failed to parse, which is exactly the partial-extraction failure
        # this validation exists to catch.
        _db.validate(conn, expected_banks=len(paths) - len(errors), expected_metric_rows=n_metrics)
        os.makedirs(os.path.dirname(args.out), exist_ok=True)
        n_exported = _db.export_metrics_csv(conn, args.out)
    finally:
        conn.close()
    if n_exported != len(all_rows):
        raise AssertionError(
            f"Exported CSV row count ({n_exported}) does not match the "
            f"in-memory deduplicated row count ({len(all_rows)}) - the "
            f"database write or export step lost or duplicated rows."
        )

    schema_path = args.out + ".schema.json"
    with open(schema_path, "w", encoding="utf-8") as f:
        json.dump({
            "schema_version": SCHEMA_VERSION,
            "columns": FIELDNAMES,
            "identity_key": "frn (falls back to bank when frn is blank)",
            "row_count": n_exported,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "generator": "scripts/extract_metrics.py",
            "source_of_truth": "research/insights.db - this CSV is a generated export, see IN-008",
        }, f, indent=2)

    print(f"\nWrote {n_banks} banks / {n_metrics} annual_metrics rows to {args.db}")
    print(f"Wrote {n_interim} interim observations / {n_register} source-register rows to {args.db}")
    print(f"Exported {n_exported} rows for {len(paths)} workbooks to {args.out} (from the database)")
    print(f"Wrote schema manifest ({SCHEMA_VERSION}) to {schema_path}")
    print(f"Collapsed {n_duplicate_groups} exact-duplicate (identity_key, sheet, row_label, year) groups to 1 row each.")
    print(f"Workbook kinds: {kind_counts}")
    print(f"Banks with no FRN match ({len(unmatched)}): {unmatched}")
    if errors:
        print(f"Workbooks that failed to process ({len(errors)}): {errors}")
    print(f"Structural-omission warnings ({len(all_warnings)}):")
    for bank_name, msg in all_warnings:
        print(f"  - {bank_name}: {msg}")
    print("\nPer-sheet coverage, post-dedup (numeric / missing / non-numeric-string):")
    for sheet in ["Cash Flow Statement"] + PILLAR3_SHEET_NAMES:
        if sheet in per_sheet_coverage:
            numeric, missing, non_numeric = per_sheet_coverage[sheet]
            print(f"  {sheet:22s} numeric={numeric:5d}  missing={missing:5d}  non_numeric_string={non_numeric:5d}")


if __name__ == "__main__":
    main()
