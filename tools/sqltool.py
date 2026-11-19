#!/usr/bin/env python3
"""sqltool.py — tiny offline SQLite CLI for agent-sql-skills.

Stdlib only. No dependencies, no network, no cloud.
Explores schemas, runs queries, and exports results to CSV.

Safety: queries are READ-ONLY by default. Only SELECT and
WITH statements run unless --write is given.

Usage:
  python tools/sqltool.py schema shop.db
  python tools/sqltool.py query shop.db "SELECT * FROM products LIMIT 5"
  python tools/sqltool.py export shop.db "SELECT * FROM products" out.csv
"""
import argparse
import csv
import os
import sqlite3
import sys

READ_ONLY_PREFIXES = ("select", "with", "pragma", "explain")


def fail(msg):
    print(f"sqltool: error: {msg}", file=sys.stderr)
    return 2


def open_db(path):
    if not os.path.isfile(path):
        print(f"sqltool: error: database not found: {path}", file=sys.stderr)
        return None
    try:
        conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"sqltool: error: cannot open {path}: {e}", file=sys.stderr)
        return None


def open_db_writable(path):
    if not os.path.isfile(path):
        print(f"sqltool: error: database not found: {path}", file=sys.stderr)
        return None
    try:
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"sqltool: error: cannot open {path}: {e}", file=sys.stderr)
        return None


def is_read_only(sql):
    stripped = sql.strip().lower()
    return stripped.startswith(READ_ONLY_PREFIXES)


def cmd_schema(a):
    conn = open_db(a.database)
    if conn is None:
        return 2
    try:
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
        ).fetchall()
        if not tables:
            print(f"No tables in {a.database}.")
            return 0
        print(f"Database: {a.database} ({len(tables)} table(s))\n")
        for (name,) in tables:
            count = conn.execute(f'SELECT COUNT(*) FROM "{name}"').fetchone()[0]
            print(f"Table: {name} ({count} row(s))")
            cols = conn.execute(f'PRAGMA table_info("{name}")').fetchall()
            for col in cols:
                pk = " PRIMARY KEY" if col["pk"] else ""
                print(f"  {col['name']}: {col['type']}{pk}")
            print()
        return 0
    except sqlite3.Error as e:
        return fail(str(e))
    finally:
        conn.close()


def run_query(conn, sql):
    cur = conn.execute(sql)
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description] if cur.description else []
    return cols, rows


def cmd_query(a):
    if not a.write and not is_read_only(a.sql):
        return fail("refused: only SELECT/WITH queries run by default. Add --write to allow changes.")
    conn = open_db_writable(a.database) if a.write else open_db(a.database)
    if conn is None:
        return 2
    try:
        cols, rows = run_query(conn, a.sql)
        if a.write:
            conn.commit()
        if not cols:
            print(f"Done. {conn.total_changes} row(s) changed.")
            return 0
        print(" | ".join(cols))
        print("-+-".join("-" * len(c) for c in cols))
        for row in rows[:a.limit]:
            print(" | ".join("" if v is None else str(v) for v in row))
        if len(rows) > a.limit:
            print(f"... and {len(rows) - a.limit} more row(s)")
        print(f"\n{len(rows)} row(s).")
        return 0
    except sqlite3.Error as e:
        return fail(str(e))
    finally:
        conn.close()


def cmd_export(a):
    if not is_read_only(a.sql):
        return fail("export only runs SELECT/WITH queries.")
    conn = open_db(a.database)
    if conn is None:
        return 2
    try:
        cols, rows = run_query(conn, a.sql)
        if not cols:
            return fail("query returned no columns to export.")
        parent = os.path.dirname(os.path.abspath(a.output))
        os.makedirs(parent, exist_ok=True)
        with open(a.output, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(cols)
            for row in rows:
                w.writerow(["" if v is None else v for v in row])
        print(f"Exported {len(rows)} row(s). Saved: {a.output}")
        return 0
    except sqlite3.Error as e:
        return fail(str(e))
    finally:
        conn.close()


def main(argv=None):
    p = argparse.ArgumentParser(prog="sqltool", description="Tiny offline SQLite CLI (stdlib only).")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("schema", help="List tables, columns, and row counts")
    s.add_argument("database")
    s.set_defaults(fn=cmd_schema)

    s = sub.add_parser("query", help="Run a query (read-only by default)")
    s.add_argument("database"); s.add_argument("sql")
    s.add_argument("--limit", type=int, default=20)
    s.add_argument("--write", action="store_true", help="Allow INSERT/UPDATE/DELETE")
    s.set_defaults(fn=cmd_query)

    s = sub.add_parser("export", help="Run a SELECT query and export results to CSV")
    s.add_argument("database"); s.add_argument("sql"); s.add_argument("output")
    s.set_defaults(fn=cmd_export)

    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    raise SystemExit(main())
