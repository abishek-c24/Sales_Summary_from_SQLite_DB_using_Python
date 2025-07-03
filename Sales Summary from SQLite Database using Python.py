import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to SQLite database
conn = sqlite3.connect('sales_data.db')
cursor = conn.cursor()
print("✅ Connected to sales_data.db")

# Create sales table
cursor.execute('''
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL
)
''')
conn.commit()
print("✅ sales table is ready")

# Insert sample sales records
cursor.execute("SELECT COUNT(*) FROM sales")
count = cursor.fetchone()[0]

if count == 0:
    sample_data = [
        ('Apple', 10, 2.5),
        ('Banana', 20, 1.0),
        ('Orange', 15, 1.8),
        ('Grapes', 12, 3.0),
        ('Pineapple', 5, 4.0),
        ('Mango', 8, 3.5),
        ('Apple', 7, 2.5),
        ('Banana', 18, 1.0),
        ('Orange', 10, 1.8),
        ('Grapes', 14, 3.0),
        ('Pineapple', 6, 4.0),
        ('Mango', 9, 3.5),
        ('Apple', 11, 2.5),
        ('Banana', 13, 1.0),
        ('Orange', 12, 1.8),
    ]
    cursor.executemany(
        'INSERT INTO sales (product, quantity, price) VALUES (?, ?, ?)',
        sample_data
    )
    conn.commit()
    print("✅ 15 sample sales records inserted")
else:
    print("✅ sales table already has data")

# Run SQL query to summarize sales
query = '''
SELECT 
    product, 
    SUM(quantity) AS total_qty, 
    SUM(quantity * price) AS revenue
FROM sales
GROUP BY product
'''

df = pd.read_sql_query(query, conn)

print("\n✅ Sales Summary:")
print(df)

# Plot simple bar chart
plt.figure(figsize=(8, 6))
plt.bar(df['product'], df['revenue'], color='lightgreen')
plt.title('Revenue per Product')
plt.xlabel('Product')
plt.ylabel('Revenue ($)')
plt.tight_layout()
plt.savefig('sales_chart.png')
plt.show()

print("✅ sales_chart.png saved and displayed")

# Close connection
conn.close()
print("✅ Database connection closed")
