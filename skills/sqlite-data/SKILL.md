---
name: sqlite-data
description: Explore SQLite schemas, run read-only queries, and export results to CSV, offline, with Python. Use when the user or agent wants to look inside a SQLite database or pull data out of it.
---

# SQLite Data

Look inside a SQLite database without a database app. List tables and
columns, run a query, or export the results to CSV.
No cloud, no upload. Files stay local.

## When to use

- "What tables are in this database?"
- "Show me the first 5 products"
- "Export the users table to CSV"

## Workflow

1. Check the file is a SQLite database. If it is not, say so and stop.
2. Explore the schema first:
   ```sh
   python tools/sqltool.py schema shop.db
   ```
   Report tables, columns, and row counts.
3. Run a query — read-only by default:
   ```sh
   python tools/sqltool.py query shop.db "SELECT * FROM products LIMIT 5"
   ```
   Only SELECT and WITH statements run. Anything else is refused unless the user adds `--write`.
4. Export results to CSV:
   ```sh
   python tools/sqltool.py export shop.db "SELECT * FROM products" products.csv
   ```
5. Report the rows returned and the output path. Never paste a whole table into a reply when a file is better.

## Examples

**What is in this database?**
```sh
python tools/sqltool.py schema shop.db
# Table: products (4 row(s))
#   id: INTEGER PRIMARY KEY
#   name: TEXT
```

**The five most expensive products**
```sh
python tools/sqltool.py query shop.db "SELECT name, price FROM products ORDER BY price DESC LIMIT 5"
# name | price
# Desk lamp | 24.99
```

**Customers in Paris, as a spreadsheet**
```sh
python tools/sqltool.py export shop.db "SELECT * FROM customers WHERE city = 'Paris'" paris.csv
# Exported 2 row(s). Saved: paris.csv
```

## Rules

- Queries are READ-ONLY by default. Never use `--write` unless the user explicitly asks to change data.
- Never run a DELETE or DROP without the user naming the exact table and confirming.
- Do not guess table or column names — use the schema output, or ask.
- If a query returns no rows, say so — do not invent data.
- The database file is never uploaded anywhere; all work happens locally.
