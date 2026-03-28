import sqlite3
import os

def connect_db():
    """Connect to SQLite database"""
    db_path = os.environ.get('DATABASE_URL', 'flight_db.sqlite')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


# Check Database Connection
def test_database_connection():
    """Test SQLite database connection"""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        # Run a simple query to check the connection
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        if result:
            print("✅ Database connection successful!")
            
            # Check tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"✅ Found {len(tables)} tables:")
            for table in tables:
                print(f"   - {table['name']}")
        else:
            print("❌ Database connection failed!")
        
        conn.close()
    except Exception as err:
        print(f"❌ Error: {err}")


if __name__ == "__main__":
    test_database_connection()
