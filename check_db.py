
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'instance', 'university.db')

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# teachers table এর schema দেখো
cursor.execute("PRAGMA table_info(teachers)")
columns = cursor.fetchall()

print("=== Teachers Table Columns ===")
for col in columns:
    print(f"  {col[1]} ({col[2]})")

cursor.execute("SELECT id, name, image FROM teachers LIMIT 5")
rows = cursor.fetchall()

print("\n=== Sample Teachers Data ===")
for row in rows:
    print(f"  ID: {row[0]}, Name: {row[1]}, Image: {row[2]}")

conn.close()