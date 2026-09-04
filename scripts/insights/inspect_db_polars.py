"""Read-only Polars explorer for the insights SQLite database.

Examples:
    python3 scripts/insights/inspect_db_polars.py
    python3 scripts/insights/inspect_db_polars.py --table banks --limit 20
    python3 scripts/insights/inspect_db_polars.py --table annual_metrics \
        --where "sheet = 'CET1 Ratio' AND year = 'FY2025'" --describe
    python3 scripts/insights/inspect_db_polars.py --sql \
        "SELECT sheet, COUNT(*) AS rows FROM annual_metrics GROUP BY sheet"

The database is opened through SQLite's read-only URI mode. This utility does
not call refresh scripts and does not depend on any deliverable code.
"""

import argparse
import sqlite3
from pathlib import Path


DEFAULT_DB = Path(__file__).resolve().parents[2] / "research" / "insights.db"


def _identifier(value):
    """Quote a SQLite identifier after validating it is a simple name."""
    if not value or not value.replace("_", "").isalnum() or not value[0].isalpha():
        raise ValueError(f"invalid table name: {value!r}")
    return '"' + value.replace('"', '""') + '"'


def _tables(connection):
    return [
        row[0]
        for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
        )
    ]


def _schema(connection, table):
    return list(connection.execute(f"PRAGMA table_info({_identifier(table)})"))


def _query(table, where, limit):
    query = f"SELECT * FROM {_identifier(table)}"
    if where:
        query += f" WHERE {where}"
    query += " LIMIT ?"
    return query, (limit,)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=DEFAULT_DB,
        help="SQLite database (default: research/insights.db)",
    )
    parser.add_argument("--table", help="table to preview; omit to list tables")
    parser.add_argument("--sql", help="read-only SQL query instead of --table preview")
    parser.add_argument("--where", help="SQL WHERE expression for a table preview")
    parser.add_argument(
        "--limit", type=int, default=20, help="maximum preview rows (default: 20)"
    )
    parser.add_argument(
        "--describe", action="store_true", help="print Polars descriptive statistics"
    )
    parser.add_argument(
        "--schema", action="store_true", help="print the selected table schema"
    )
    parser.add_argument(
        "--export", type=Path, help="write the result to .csv or .parquet"
    )
    args = parser.parse_args(argv)

    if args.limit < 1:
        parser.error("--limit must be positive")
    if args.sql and (args.table or args.where):
        parser.error("--sql cannot be combined with --table or --where")
    if not args.db.is_file():
        parser.error(f"database not found: {args.db}")
    try:
        import polars as pl
    except ModuleNotFoundError as error:
        raise SystemExit(
            "Polars is required. Use `uv run --with polars python3 "
            "scripts/insights/inspect_db_polars.py ...` or install Polars in "
            "your project environment."
        ) from error

    read_uri = f"file:{args.db.resolve()}?mode=ro"
    with sqlite3.connect(read_uri, uri=True) as connection:
        tables = _tables(connection)
        if args.sql:
            query, parameters = args.sql, ()
            selected_table = None
        elif args.table:
            if args.table not in tables:
                parser.error(
                    f"unknown table {args.table!r}; choose from: {', '.join(tables)}"
                )
            selected_table = args.table
            query, parameters = _query(args.table, args.where, args.limit)
        else:
            print(f"Database: {args.db}")
            print("Tables:")
            for table in tables:
                count = connection.execute(
                    f"SELECT COUNT(*) FROM {_identifier(table)}"
                ).fetchone()[0]
                print(f"  {table}: {count:,} rows")
            return

        if args.schema:
            if not selected_table:
                parser.error("--schema requires --table")
            print(f"Schema: {selected_table}")
            for _cid, name, kind, not_null, default, primary_key in _schema(
                connection, selected_table
            ):
                print(
                    f"  {name}: {kind or 'ANY'}"
                    + (" NOT NULL" if not_null else "")
                    + (" PRIMARY KEY" if primary_key else "")
                )

        frame = pl.read_database(
            query, connection, execute_options={"parameters": parameters}
        )
        print(frame)
        if args.describe:
            print("Descriptive statistics:")
            print(frame.describe())
        if args.export:
            suffix = args.export.suffix.lower()
            if suffix == ".csv":
                frame.write_csv(args.export)
            elif suffix == ".parquet":
                frame.write_parquet(args.export)
            else:
                parser.error("--export must end in .csv or .parquet")
            print(
                f"Wrote {args.export} ({frame.height:,} rows × {frame.width:,} columns)"
            )


if __name__ == "__main__":
    main()
