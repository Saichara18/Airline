"""
Quick test to verify SQLite database persistence
Run this multiple times to confirm data persists!
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = 'flight_db.sqlite'

def main():
    print("\n" + "="*50)
    print("🧪 DATABASE PERSISTENCE TEST")
    print("="*50)
    print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
    print(f"Database: {DB_PATH}")
    print("-"*50)
    
    # Check if database exists
    if not os.path.exists(DB_PATH):
        print("❌ Database file doesn't exist yet")
        print("   Run 'python setup_database.py' first")
        return
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"✅ Database found with {len(tables)} tables")
        
        # Count flights
        cursor.execute("SELECT COUNT(*) FROM flights")
        flight_count = cursor.fetchone()[0]
        print(f"   Flights in database: {flight_count}")
        
        # Count users
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        print(f"   Users in database: {user_count}")
        
        # Count bookings
        cursor.execute("SELECT COUNT(*) FROM bookings")
        booking_count = cursor.fetchone()[0]
        print(f"   Bookings in database: {booking_count}")
        
        conn.close()
        
        print("-"*50)
        print("✅ All tables accessible!")
        print("\n💡 TIP: Run this script again to verify data persists!")
        print("   If counts stay the same (or increase if you add data),")
        print("   then persistence is working! ✅")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure database exists: python setup_database.py")
        print("2. Check file permissions")
        print("3. Ensure database isn't locked by another process")

if __name__ == "__main__":
    main()
    print("="*50 + "\n")
