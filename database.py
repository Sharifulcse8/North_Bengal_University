import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'instance', 'university.db')

def get_db():
    """connection to database"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def add_short_desc_column():
    """Add short_desc column to notices table if not exists"""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        # Check if short_desc column exists
        cursor.execute("PRAGMA table_info(notices)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'short_desc' not in columns:
            print("📌 Adding short_desc column to notices table...")
            cursor.execute('ALTER TABLE notices ADD COLUMN short_desc TEXT DEFAULT ""')
            conn.commit()
            print("✅ short_desc column added successfully!")
        else:
            print("✅ short_desc column already exists.")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    conn.close()

def init_db():
    """create database tables if not exists"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_db()
    cursor = conn.cursor()
    
    # ===== NOTICES TABLE (with short_desc) =====
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            short_desc TEXT DEFAULT '',
            category TEXT DEFAULT 'General',
            image TEXT DEFAULT '',
            date_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active INTEGER DEFAULT 1
        )
    ''')
    
    # ===== TEACHERS TABLE =====
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            designation TEXT NOT NULL,
            department TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT DEFAULT '',
            image TEXT DEFAULT 'teacher_default.jpg',
            bio TEXT DEFAULT '',
            is_active INTEGER DEFAULT 1
        )
    ''')
    
    # ===== STUDENTS TABLE =====
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            student_id TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            session TEXT NOT NULL,
            cgpa REAL DEFAULT 0.0,
            email TEXT NOT NULL,
            phone TEXT DEFAULT '',
            image TEXT DEFAULT 'student_default.jpg',
            bio TEXT DEFAULT '',
            is_active INTEGER DEFAULT 1
        )
    ''')
    
    # ===== DEPARTMENTS TABLE =====
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            code TEXT,
            description TEXT,
            hod TEXT,
            is_active INTEGER DEFAULT 1
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")

if __name__ == '__main__':
    init_db()
    add_short_desc_column()  # Add short_desc column if not exists