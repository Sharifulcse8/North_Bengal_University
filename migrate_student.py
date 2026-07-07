# migrate_student.py
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'instance', 'university.db')

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

try:
    cursor.execute('ALTER TABLE students ADD COLUMN image TEXT DEFAULT "student_default.jpg"')
    print("image column added successfully!")
except sqlite3.OperationalError as e:
    if 'duplicate column name' in str(e):
        print("ℹ image column already exists.")
    else:
        print(f"⚠️ Error: {e}")

conn.commit()
conn.close()