#!/usr/bin/env python3
"""
Database Migration Script
Adds the is_admin column to the users table if it doesn't exist
Run this if you're updating an existing database
"""

import sqlite3
import os

def migrate_database():
    db_path = os.environ.get('DATABASE_URL', 'flight_db.sqlite')
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if is_admin column exists
        cursor.execute("PRAGMA table_info(users);")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'is_admin' in columns:
            print("✅ Column 'is_admin' already exists in users table")
            conn.close()
            return True
        
        print("📝 Adding 'is_admin' column to users table...")
        
        # Add is_admin column
        cursor.execute("""
            ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0
        """)
        
        conn.commit()
        conn.close()
        
        print("✅ Migration completed successfully!")
        print("   - Added 'is_admin' column to users table")
        print("   - Default value: 0 (regular user)")
        print("\n📝 Next step: Create admin account with: python create_admin.py\n")
        
        return True
        
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("✅ Column 'is_admin' already exists")
            return True
        else:
            print(f"❌ Database error: {str(e)}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == '__main__':
    success = migrate_database()
    exit(0 if success else 1)
