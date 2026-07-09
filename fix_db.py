import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'instance', 'university.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def add_missing_columns():
    """Add missing columns to notices table"""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        # Check existing columns
        cursor.execute("PRAGMA table_info(notices)")
        columns = [col[1] for col in cursor.fetchall()]
        
        # Add image column if not exists
        if 'image' not in columns:
            print("📌 Adding 'image' column to notices table...")
            cursor.execute('ALTER TABLE notices ADD COLUMN image TEXT DEFAULT ""')
            conn.commit()
            print("✅ 'image' column added successfully!")
        else:
            print("✅ 'image' column already exists.")
        
        # Add short_desc column if not exists
        if 'short_desc' not in columns:
            print("📌 Adding 'short_desc' column to notices table...")
            cursor.execute('ALTER TABLE notices ADD COLUMN short_desc TEXT DEFAULT ""')
            conn.commit()
            print("✅ 'short_desc' column added successfully!")
        else:
            print("✅ 'short_desc' column already exists.")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    conn.close()

if __name__ == '__main__':
    add_missing_columns()
    print("✅ Database updated successfully!")