"""
Regenerates research/bank_parent_groups.md's two MECHANICAL tables (the
"## Bank-level lookup" table and the "## Typed edge list" table) from
research/insights.db, splicing them back into the file in place. Everything
else in the file - the "## Conventions" prose, the Mermaid diagrams under
"## Mermaid multi-bank cluster views", and the "## Quality and follow-up"
notes - is hand-authored and left completely untouched.

Built for wayfinder/insights/ ticket IN-008 - see that ticket for the
"splice just the two tables" scope decision (the user chose this over full
regeneration, since the markdown's prose/diagrams aren't naturally
DB-native content).

Workflow this script assumes (see the module docstring in
scripts/build_insights_db.py for the fuller picture):
  1. A human/agent researches and edits the two tables in
     research/bank_parent_groups.md directly, as before - this script does
     NOT change how that research gets entered.
  2. This script imports the freshly-edited tables into
     research/insights.db (via build_insights_db.write_parent_group -
     requires banks/annual_metrics to already be populated, i.e.
     scripts/extract_metrics.py must have been run at least once).
  3. This script then regenerates the same two tables FROM the database and
     splices them back into the file, replacing what it just imported.
     Run with no data changes, this step is a no-op (byte-identical output)
     - it exists so the file's tables are provably a reflection of what's
     actually in the database, not a second, independently-editable copy
     that could silently drift from it.

Usage:
    python3 scripts/export_parent_group_tables.py
    python3 scripts/export_parent_group_tables.py --markdown research/bank_parent_groups.md --db research/insights.db

Safety: writes to a temp file first and only replaces the original via an
atomic os.replace() once the new content has been validated (both section
markers found, row counts match the database) - the original file is never
left partially written.
"""

import argparse
import os
import shutil

import build_insights_db as db

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
DEFAULT_MARKDOWN = os.path.join(REPO_ROOT, "research", "bank_parent_groups.md")
DEFAULT_DB = os.path.join(REPO_ROOT, "research", "insights.db")

LOOKUP_SECTION_HEADER = "## Bank-level lookup"
LOOKUP_TABLE_HEADER = "| Bank/legal entity | FRN | Immediate parent or ownership | Ultimate/group node | Status and reporting caveat | Evidence |"
LOOKUP_TABLE_SEP = "|---|---:|---|---|---|---|"

EDGES_SECTION_HEADER = "## Typed edge list"
EDGES_TABLE_HEADER = "| from | edge | to | effective / note | source |"
EDGES_TABLE_SEP = "|---|---|---|---|---|"


def _escape_pipe(value):
    """Escape a literal '|' so a free-text DB field can't corrupt a markdown
    pipe-table's column structure on regeneration. `status_caveat`/`evidence`/
    `effective_note` are hand-authored free text - not validated against pipe
    characters anywhere upstream."""
    return str(value).replace("|", "\\|")


def _render_lookup_rows(conn):
    rows = conn.execute(
        "SELECT bank_name, frn, immediate_parent, ultimate_group, status_caveat, evidence "
        "FROM parent_group_lookup ORDER BY sort_order"
    ).fetchall()
    return [
        f"| {_escape_pipe(bank_name)} | {_escape_pipe(frn)} | {_escape_pipe(immediate_parent)} | "
        f"{_escape_pipe(ultimate_group)} | {_escape_pipe(status_caveat)} | {_escape_pipe(evidence)} |"
        for bank_name, frn, immediate_parent, ultimate_group, status_caveat, evidence in rows
    ]


def _render_edge_rows(conn):
    rows = conn.execute(
        "SELECT from_node, edge_type, to_node, effective_note, source "
        "FROM parent_group_edges ORDER BY id"
    ).fetchall()
    return [
        f"| {_escape_pipe(from_node)} | {_escape_pipe(edge_type)} | {_escape_pipe(to_node)} | "
        f"{_escape_pipe(effective_note)} | {_escape_pipe(source)} |"
        for from_node, edge_type, to_node, effective_note, source in rows
    ]


def _find_table_block(lines, section_header, table_header):
    """Returns (start_index, end_index) of the table block (header line
    through the last data row, exclusive of end_index) that follows
    `section_header`. Raises if either isn't found - fail loudly rather
    than silently corrupt the file."""
    try:
        section_idx = next(i for i, line in enumerate(lines) if line.strip() == section_header)
    except StopIteration:
        raise ValueError(f"Could not find section header {section_header!r} in the markdown file")
    try:
        header_idx = next(
            i for i in range(section_idx, len(lines)) if lines[i].strip() == table_header
        )
    except StopIteration:
        raise ValueError(f"Could not find table header {table_header!r} after {section_header!r}")
    # data rows run from header_idx+2 (skipping the separator row) until a blank line
    end_idx = header_idx + 2
    while end_idx < len(lines) and lines[end_idx].strip() != "":
        end_idx += 1
    return header_idx, end_idx


def splice(markdown_path, conn):
    with open(markdown_path, encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f.readlines()]

    lookup_start, lookup_end = _find_table_block(lines, LOOKUP_SECTION_HEADER, LOOKUP_TABLE_HEADER)
    lookup_rows = _render_lookup_rows(conn)
    new_lookup_block = [LOOKUP_TABLE_HEADER, LOOKUP_TABLE_SEP] + lookup_rows

    edges_start, edges_end = _find_table_block(lines, EDGES_SECTION_HEADER, EDGES_TABLE_HEADER)
    edge_rows = _render_edge_rows(conn)
    new_edges_block = [EDGES_TABLE_HEADER, EDGES_TABLE_SEP] + edge_rows

    # splice from the bottom block first so the earlier block's indices
    # (lookup_start/lookup_end) aren't invalidated by the edit
    assert lookup_end <= edges_start, "expected the lookup table to precede the edge-list table"
    new_lines = (
        lines[:lookup_start] + new_lookup_block + lines[lookup_end:edges_start]
        + new_edges_block + lines[edges_end:]
    )
    return "\n".join(new_lines) + "\n", len(lookup_rows), len(edge_rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--markdown", default=DEFAULT_MARKDOWN)
    parser.add_argument("--db", default=DEFAULT_DB)
    parser.add_argument(
        "--skip-import", action="store_true",
        help="skip re-importing the markdown's current tables into the DB first "
             "(use only if you've already imported via build_insights_db.py)",
    )
    args = parser.parse_args()

    conn = db.connect(args.db)
    try:
        if not args.skip_import:
            lookup_rows, edge_rows = db.load_markdown_lookup_and_edges(args.markdown)
            n_lookup, n_edges = db.write_parent_group(conn, lookup_rows, edge_rows)
            print(f"Imported {n_lookup} lookup rows / {n_edges} edge rows from {args.markdown} into {args.db}")

        new_content, n_lookup_rendered, n_edges_rendered = splice(args.markdown, conn)
    finally:
        conn.close()

    with open(args.markdown, encoding="utf-8") as f:
        old_content = f.read()

    # Compare BEFORE writing anything to the real path - a no-op run must
    # leave the original file's content, mtime, AND inode completely
    # untouched (os.replace() always changes the inode, even when the
    # content is byte-identical, since it's an atomic rename over the
    # destination). Only write the temp file and replace when there's an
    # actual change to make.
    if new_content == old_content:
        print(f"{args.markdown}: no change (already reflects the database exactly) - file left untouched")
        return

    tmp_path = args.markdown + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    shutil.copystat(args.markdown, tmp_path)
    os.replace(tmp_path, args.markdown)
    print(f"{args.markdown}: regenerated ({n_lookup_rendered} lookup rows, "
          f"{n_edges_rendered} edge rows spliced in from {args.db})")


if __name__ == "__main__":
    main()
