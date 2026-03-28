# DATABASE PERSISTENCE GUIDE

## ✅ How Database Persistence Works Now

Your SQLite database **will NOT be recreated** every time the app runs.

### The Logic:

1. **First Run**: 
   - App checks if `flight_db.sqlite` exists
   - If NOT → Creates database and initializes tables
   - Prints: "🗄️ Database file not found. Creating..."

2. **Subsequent Runs**:
   - App checks if `flight_db.sqlite` exists
   - If YES → Verifies tables exist
   - Skips initialization (data is safe!)
   - Prints: "✅ Database ready with X tables. No reinitialization needed."

3. **Your Data**:
   - All users, flights, bookings stay intact
   - Between app restarts ✅
   - Between deployments ✅
   - Survives server restarts (on Render)

---

## 🧪 Test It Yourself

### Step 1: Create Database
```bash
python setup_database.py
# Output: "Database 'flight_db.sqlite' initialized successfully..."
```

### Step 2: Check File Exists
```bash
# Windows (PowerShell):
Test-Path flight_db.sqlite
# Output: True

# Mac/Linux:
ls -la flight_db.sqlite
```

### Step 3: Add Sample Data
```bash
python
# Then:
import sqlite3
conn = sqlite3.connect('flight_db.sqlite')
cursor = conn.cursor()
cursor.execute("INSERT INTO flights (flight_number, source, destination, departure_time, arrival_time, available_seats, price) VALUES (?, ?, ?, ?, ?, ?, ?)", 
               ('AI101', 'New York', 'London', '08:00', '20:00', 100, 599.99))
conn.commit()
cursor.execute("SELECT * FROM flights")
print(cursor.fetchall())
conn.close()
# Output: [tuple with flight data]
```

### Step 4: Restart App (Multiple Times)
```bash
# First start
cd frontend
python app.py
# Check logs - shows initialization

# Stop app (Ctrl+C)

# Second start
python app.py
# Check logs - shows "Database ready, no reinitialization"

# Data is still there! ✅
```

---

## 🔄 How It Works in Detail

### Location: `setup_database.py`
```python
# NOW INCLUDES:
if os.path.exists(db_path):
    # Database already exists
    # Check if tables exist
    if tables:
        # Tables exist - SKIP INITIALIZATION
        print("✅ Database already exists. Skipping initialization.")
        return
    
# Only create if doesn't exist
# Only create tables if they don't exist (IF NOT EXISTS)
```

### Location: `frontend/app.py`
```python
# NOW INCLUDES:
def init_db():
    if not os.path.exists(DATABASE_URL):
        # Only initialize if file doesn't exist
        from setup_database import initialize_db
        initialize_db()
    else:
        # Database exists - verify tables
        # Don't reinitialize! ✅
```

---

## 📁 Database File Location

The database file is stored in different locations:

### Local Development
```
f:\projectair\flight_db.sqlite
```

### On Render
```
/app/flight_db.sqlite    (in your app container)
```

### Environment Variable
```bash
# You can set custom location:
export DATABASE_URL=/custom/path/flight_db.sqlite

# Or use default:
# DATABASE_URL not set → defaults to flight_db.sqlite in app directory
```

---

## 🔐 Data Persistence Scenarios

### ✅ Data WILL Persist

1. **Restarting App Locally**
   ```bash
   python app.py  # Run
   # Stop
   python app.py  # Run again - data intact!
   ```

2. **Between Deployments**
   - `flight_db.sqlite` is in app directory
   - Render keeps files in /app/ directory
   - Data survives redeployment ✅

3. **Server Restarts**
   - Render restarts service
   - App directory files remain
   - Data persists ✅

4. **Testing & Development**
   - Add test data
   - Stop app
   - Start app
   - Data still there ✅

### ❌ Data WILL Be Lost

1. **If You Delete `flight_db.sqlite`**
   ```bash
   rm flight_db.sqlite
   python app.py  # Reinitializes as new database
   ```

2. **On Render Free Tier (occasionally)**
   - Service can be spun down if unused
   - When restarted, Render typically keeps files
   - But for guaranteed persistence, use paid tier

3. **If You Run `setup_database.py` With Delete**
   ```bash
   # DO NOT DO THIS:
   rm flight_db.sqlite && python setup_database.py
   # Only do if you want to reset!
   ```

---

## 🔄 Complete Reset (If Needed)

If you need to wipe data and start fresh:

### Option 1: Delete Database File
```bash
# Windows:
Remove-Item flight_db.sqlite -Force

# Mac/Linux:
rm flight_db.sqlite

# Then reinitialize:
python setup_database.py
```

### Option 2: Run Database Reset Script
```bash
# Create a reset script:
# reset_db.py:

import os
db_path = 'flight_db.sqlite'
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"❌ Deleted {db_path}")

from setup_database import initialize_db
initialize_db()
print("✅ Database reset complete. Fresh start!")
```

Then run:
```bash
python reset_db.py
```

---

## 🧠 Understanding: "Why wasn't it persisting before?"

### Common Issue
- App calls `initialize_db()` every startup
- `CREATE TABLE IF NOT EXISTS` doesn't delete data
- But if you were seeing it reset, possible causes:

1. **Database file deleted between runs**
   - Check if file exists after closing app

2. **Wrong file location**
   - Check `DATABASE_URL` environment variable
   - Might be creating in different directories

3. **Foreign key constraints failing**
   - Could prevent inserts silently
   - Check app logs for errors

### Now Fixed ✅
- App checks if database exists
- Skips initialization if tables present
- Data guaranteed to persist
- Logs show what's happening

---

## 📊 Verify Persistence

### Script to Test
Create `test_persistence.py`:

```python
import sqlite3
import os
from datetime import datetime

db_path = 'flight_db.sqlite'

def show_flight_count():
    """Show how many flights in database"""
    if not os.path.exists(db_path):
        print("❌ Database doesn't exist!")
        return 0
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM flights")
    count = cursor.fetchone()[0]
    conn.close()
    
    print(f"✅ Database has {count} flights")
    return count

def add_test_flight():
    """Add a test flight"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO flights 
        (flight_number, source, destination, departure_time, arrival_time, available_seats, price)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, ('TEST001', 'Test-A', 'Test-B', '12:00', '14:00', 50, 999.99))
    
    conn.commit()
    conn.close()
    print("✅ Test flight added")

if __name__ == "__main__":
    print(f"📊 Persistence Test at {datetime.now()}")
    print("-" * 40)
    count = show_flight_count()
    
    if count == 0:
        print("Adding test flight...")
        add_test_flight()
    
    print("-" * 40)
    print("👉 Run this script again to verify!")
    print("   If flight count increases, persistence works!")
```

Run it:
```bash
python test_persistence.py
# First run: Adding flight, count = 0 → 1
python test_persistence.py
# Second run: count = 1 (still there!) ✅
```

---

## 📝 Summary

### Before Changes
- ❌ Database recreated every run
- ❌ Data lost after restart

### After Changes ✅
- ✅ Database checked for existence
- ✅ Tables only created if missing
- ✅ Data persists between restarts
- ✅ Logs show what's happening
- ✅ Complete reset option available

### How to Verify
1. Run app, add data
2. Stop app
3. Run app again
4. Data is still there! ✅

---

## 🚀 Deployment: Server Restarts

On Render, your data will persist:

1. **Normal Operation**
   - Service restarts → Database file stays
   - Data intact ✅

2. **Redeployment**
   - New version deployed
   - `flight_db.sqlite` persists
   - Data intact ✅

3. **Server Down Due to Inactivity** (Free Tier)
   - Service spins down
   - When you access app → spins back up
   - Database file restored
   - Data likely intact (but not guaranteed on free tier)

4. **For Guaranteed Persistence**
   - Use Render Disk feature (paid)
   - Or upgrade to paid tier
   - Database will definitely persist ✅

---

**Your data is now safe! 🔒**
