import sqlite3

conn = sqlite3.connect('ecommerce.db')
cursor = conn.cursor()

# Get list of tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in the database:")
for table in tables:
    print(table[0])

# Get schema and top 5 rows for each table
for table in tables:
    print(f"\n{'-'*40}")
    print(f"Table: {table[0]}")
    print(f"{'-'*40}")
    
    # Schema
    cursor.execute(f"PRAGMA table_info({table[0]})")
    columns = cursor.fetchall()
    print("Schema:")
    for column in columns:
        print(f"  {column[1]} {column[2]}")
    
    # Top 5 rows
    cursor.execute(f"SELECT * FROM {table[0]} LIMIT 5")
    rows = cursor.fetchall()
    print("\nTop 5 rows:")
    for row in rows:
        print(row)

conn.close()