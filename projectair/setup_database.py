import sqlite3
import os

def initialize_db():
    db_path = os.environ.get('DATABASE_URL', 'flight_db.sqlite')
    
    # Check if database already exists with data
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()
        
        # If tables already exist, don't reinitialize
        if tables:
            print(f"✅ Database '{db_path}' already exists with {len(tables)} tables. Skipping initialization.")
            return
    
    print(f"🗄️  Initializing new database: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        gender TEXT,
        location TEXT,
        dob TEXT,
        email TEXT UNIQUE NOT NULL,
        mobile TEXT,
        password TEXT NOT NULL
    )
    """)

    # Create flights table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS flights (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        flight_number TEXT NOT NULL,
        source TEXT NOT NULL,
        destination TEXT NOT NULL,
        departure_time TEXT,
        arrival_time TEXT,
        available_seats INTEGER,
        price REAL
    )
    """)

    # Create bookings table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        flight_id INTEGER NOT NULL,
        passenger_name TEXT NOT NULL,
        age INTEGER,
        nationality TEXT,
        gender TEXT,
        date TEXT,
        transaction_id TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id),
        FOREIGN KEY(flight_id) REFERENCES flights(id)
    )
    """)

    # Create support_chat table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS support_chat (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        message TEXT NOT NULL,
        timestamp TEXT NOT NULL
    )
    """)

    # Create flight_delays table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS flight_delays (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        flight_number TEXT NOT NULL,
        delay_minutes INTEGER,
        reason TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
    print(f"✅ Database '{db_path}' initialized successfully with all tables!")
    print(f"   - Users table")
    print(f"   - Flights table")
    print(f"   - Bookings table")
    print(f"   - Support chat table")
    print(f"   - Flight delays table")

if __name__ == '__main__':
    initialize_db()
