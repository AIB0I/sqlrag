import sqlite3
import random
from datetime import datetime, timedelta

# Connect to the SQLite database (creates it if it doesn't exist)
conn = sqlite3.connect('ecommerce.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price DECIMAL(10, 2) NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id INTEGER,
    quantity INTEGER NOT NULL,
    order_date DATE NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
    FOREIGN KEY (product_id) REFERENCES products (product_id)
)
''')

# Sample data
products = [
    ('Laptop', 999.99),
    ('Smartphone', 599.99),
    ('Headphones', 149.99),
    ('Tablet', 399.99),
    ('Smartwatch', 249.99),
    ('Camera', 799.99),
    ('Gaming Console', 499.99),
    ('Bluetooth Speaker', 79.99),
    ('Fitness Tracker', 129.99),
    ('External Hard Drive', 89.99)
]

customers = [
    ('John Doe', 'john@example.com'),
    ('Jane Smith', 'jane@example.com'),
    ('Bob Johnson', 'bob@example.com'),
    ('Alice Brown', 'alice@example.com'),
    ('Charlie Davis', 'charlie@example.com')
]

# Insert sample data
cursor.executemany('INSERT INTO products (name, price) VALUES (?, ?)', products)
cursor.executemany('INSERT INTO customers (name, email) VALUES (?, ?)', customers)

# Generate random orders
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)

for _ in range(1000):  # Generate 1000 random orders
    customer_id = random.randint(1, 5)
    product_id = random.randint(1, 10)
    quantity = random.randint(1, 5)
    order_date = start_date + timedelta(days=random.randint(0, 364))
    
    cursor.execute('''
    INSERT INTO orders (customer_id, product_id, quantity, order_date)
    VALUES (?, ?, ?, ?)
    ''', (customer_id, product_id, quantity, order_date))

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database created and populated with sample data.")