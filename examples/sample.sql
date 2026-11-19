-- Sample database for agent-sql-skills.
-- Create it with: sqlite3 shop.db < examples/sample.sql
CREATE TABLE products (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  price REAL NOT NULL,
  stock INTEGER NOT NULL
);
CREATE TABLE customers (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  city TEXT
);
INSERT INTO products (name, price, stock) VALUES
  ('Notebook', 12.50, 40),
  ('Pen set', 8.00, 120),
  ('Desk lamp', 24.99, 15),
  ('Mug', 9.50, 0);
INSERT INTO customers (name, city) VALUES
  ('Aisha Khan', 'Paris'),
  ('Liam Chen', 'London'),
  ('Maya Patel', 'Paris');
