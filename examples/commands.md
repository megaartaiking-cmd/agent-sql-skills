# Example commands

```sh
# Create the sample database from the SQL script
sqlite3 shop.db < examples/sample.sql

# Explore the schema: tables, columns, row counts
python tools/sqltool.py schema shop.db

# Run a read-only query
python tools/sqltool.py query shop.db "SELECT * FROM products LIMIT 5"
python tools/sqltool.py query shop.db "SELECT name, price FROM products WHERE stock > 0"

# Export query results to CSV
python tools/sqltool.py export shop.db "SELECT * FROM products" products.csv
python tools/sqltool.py export shop.db "SELECT * FROM customers WHERE city = 'Paris'" paris.csv
```

Queries are read-only by default. Only SELECT and WITH run unless `--write` is given.
