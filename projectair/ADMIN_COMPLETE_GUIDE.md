# 🎯 COMPLETE ADMIN SETUP - STEP BY STEP

## What You Get ✨

With this admin system, you can now:
- ✅ **Monitor ALL flight bookings** made by all users
- ✅ **Check previous bookings** from all customers
- ✅ **View user details** and their booking history
- ✅ **Check flight occupancy** rates and available seats
- ✅ **Access beautiful dashboards** with statistics

---

## STEP 1: Update Your Database (First Time Only)

Run this command once to add the admin field to your database:

```powershell
cd f:\projectair
python migrate_database.py
```

**Expected output:**
```
📝 Adding 'is_admin' column to users table...
✅ Migration completed successfully!
   - Added 'is_admin' column to users table
   - Default value: 0 (regular user)

📝 Next step: Create admin account with: python create_admin.py
```

---

## STEP 2: Create Your Admin Account

Run the admin account creator:

```powershell
python create_admin.py
```

This will ask you questions. **Example output:**

```
============================================================
🔐 PROJECTAIR ADMIN ACCOUNT CREATOR
============================================================

Please provide admin account details:

👤 Admin Name: Flight Manager
📧 Email: admin@projectair.com
🔒 Password (min 6 characters): MySecure123!
🔒 Confirm Password: MySecure123!
📱 Mobile (optional, press Enter to skip): 9876543210
📍 Location (optional, press Enter to skip): Delhi

============================================================
✅ ADMIN ACCOUNT CREATED SUCCESSFULLY!
============================================================

📊 Admin Details:
   ID: 1
   Name: Flight Manager
   Email: admin@projectair.com
   Status: Active

🔗 Access Admin Panel:
   1. Login with the admin email and password
   2. Go to: /admin (or click Admin Dashboard)

📈 Admin Features:
   ✓ View all bookings from all users
   ✓ Monitor flight occupancy
   ✓ View all registered users
   ✓ Check booking statistics
```

---

## STEP 3: Test the Application

Start your app:

```powershell
cd frontend
python app.py
```

---

## STEP 4: Login as Admin

1. Open: `http://localhost:5000/login`
2. Enter:
   - **Email:** `admin@projectair.com` (your admin email)
   - **Password:** `MySecure123!` (your admin password)
3. Click **Login**
4. You'll see the dashboard

---

## STEP 5: Access Admin Panel

On the dashboard, you'll see:
- **Book Ticket** button (blue)
- **My Bookings** button (blue)
- **General Info** button (blue)
- **Upload Delay** button (blue)
- **📊 Admin Panel** button (RED - new!)

Click the **RED "📊 Admin Panel"** button.

---

## STEP 6: Use the Admin Dashboard

You'll see a beautiful dashboard showing:

### 📊 Statistics Cards:
- Total Bookings: X
- Completed Bookings: X
- Total Users: X
- Total Flights: X
- Available Seats: X

### 📋 Management Panels (Clickable):
- 📦 **View All Bookings** - See every booking made in the system
- 👥 **View All Users** - See every registered customer
- ✈️ **View All Flights** - See all flights with occupancy

---

## EXAMPLE WORKFLOWS

### Workflow 1: Check Today's Bookings

1. Login as admin → Click Admin Panel
2. Click **"📦 View All Bookings"**
3. See a table with:
   - Transaction ID (like `TXN123456`)
   - Customer Name
   - Customer Email
   - Flight Number
   - Route (e.g., "Delhi → Mumbai")
   - Passengers (list of all people on the booking)
   - Total Amount Paid
   - Date
   - Status (Completed/Pending)

**Example table row:**
```
TXN567890 | Raj Kumar | raj@email.com | AI-101 | Delhi → Mumbai | 
Raj Kumar (30, M), Priya Kumar (28, F) | ₹12,000.00 | 2026-03-28 | ✓ Completed
```

---

### Workflow 2: Monitor Flight Occupancy

1. Login as admin → Click Admin Panel
2. Click **"✈️ View All Flights"**
3. See a table with flights and occupancy bars:
   - Flight AI-101: [████████░░] 80% (40/50 seats)
   - Flight AI-102: [██░░░░░░░░] 20% (10/50 seats)
   - Flight AI-103: [██████████] 100% (FULL)

**This helps you:**
- Identify popular routes (high occupancy)
- Find seats to sell (low occupancy)
- Plan flights based on booking patterns

---

### Workflow 3: View All Customers

1. Login as admin → Click Admin Panel
2. Click **"👥 View All Users"**
3. See a table showing:
   - Name
   - Email
   - Phone
   - Location
   - Total Bookings (count)

**Example:**
```
Raj Kumar | raj@email.com | 9876543210 | Delhi | 5 bookings
Priya Sharma | priya@email.com | 9988776655 | Mumbai | 2 bookings
Arjun Singh | arjun@email.com | 9999888877 | Bangalore | 1 booking
```

---

## 🔒 SECURITY & ACCESS CONTROL

### Who Can Access Admin Panel?
- ✅ Users with `is_admin=1` (admin users)
- ❌ Regular users (`is_admin=0`) **CANNOT** access admin features

### What Happens if Regular User Tries to Access /admin?
- They get redirected to regular dashboard
- Error message: "Admin access required!"

### How to Make Another User Admin?
Using database directly:
```python
import sqlite3
conn = sqlite3.connect('flight_db.sqlite')
cursor = conn.cursor()
cursor.execute("UPDATE users SET is_admin=1 WHERE email='user@email.com'")
conn.commit()
```

---

## 📊 UNDERSTANDING THE DATA

### Booking Information
Each booking shows:
- **Transaction ID**: Unique payment confirmation
- **Passengers**: All people traveling (can be multiple)
- **Status**: 
  - Completed = Payment done (has transaction ID)
  - Pending = Payment not completed

### User Information
- **Total Bookings**: How many times this customer booked
- This includes both completed and pending bookings

### Flight Information
- **Occupancy**: Booked seats ÷ Total seats
  - High occupancy = Popular route
  - Low occupancy = Consider marketing

---

## 🚀 DEPLOYMENT TO RENDER

The admin account **persists** after deployment!

1. Create admin account locally (Step 2 above)
2. The admin is stored in `flight_db.sqlite`
3. Deploy to Render (database goes with deployment)
4. Login with same admin credentials on production

---

## ✅ VERIFICATION CHECKLIST

After setup, verify everything works:

- [ ] Database migration ran successfully
- [ ] Admin account created
- [ ] Can login with admin email and password
- [ ] "📊 Admin Panel" button visible on dashboard
- [ ] Can access `/admin/bookings` and see all bookings
- [ ] Can access `/admin/users` and see all users
- [ ] Can access `/admin/flights` and see flight occupancy
- [ ] Regular users cannot access admin routes
- [ ] Can logout from admin panel

---

## 🆘 TROUBLESHOOTING

### Problem: Admin Panel button not visible

**Solution 1**: Verify admin account was created
```python
import sqlite3
conn = sqlite3.connect('flight_db.sqlite')
cursor = conn.cursor()
cursor.execute("SELECT email, is_admin FROM users WHERE email='admin@projectair.com'")
print(cursor.fetchone())
```

Should show: `('admin@projectair.com', 1)`

**Solution 2**: Make sure you're logged in with admin account (not regular user)

**Solution 3**: Clear browser cache and refresh

---

### Problem: Database migration failed

**Reason**: Column already exists

**Solution**: This is okay! It means your database already has the column. Continue with Step 2.

---

### Problem: Can't create admin account - email already exists

**Solution 1**: Use a different email
```bash
python create_admin.py
# Use: admin2@projectair.com
```

**Solution 2**: Update existing user to admin:
```python
import sqlite3
from werkzeug.security import generate_password_hash

db_path = 'flight_db.sqlite'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Make existing user admin
cursor.execute("""
    UPDATE users SET is_admin=1 WHERE email='existing@email.com'
""")
conn.commit()
```

---

### Problem: Access denied when trying to view /admin

**Reason**: You're logged in as regular user, not admin

**Solution**:
1. Logout
2. Login with YOUR ADMIN email (e.g., admin@projectair.com)
3. Then click Admin Panel button

---

## 📝 USEFUL SQL QUERIES

Check your database:

```python
import sqlite3

conn = sqlite3.connect('flight_db.sqlite')
cursor = conn.cursor()

# List all admins
print("=== ADMINS ===")
cursor.execute("SELECT user_id, name, email FROM users WHERE is_admin=1")
for row in cursor.fetchall():
    print(f"ID: {row[0]}, Name: {row[1]}, Email: {row[2]}")

# Count total bookings
print("\n=== STATS ===")
cursor.execute("SELECT COUNT(*) FROM bookings")
print(f"Total Bookings: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM users WHERE is_admin=0")
print(f"Total Users: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM flights")
print(f"Total Flights: {cursor.fetchone()[0]}")

conn.close()
```

---

## 🎓 WHAT'S NEXT?

Future enhancements you could add:
- ✅ Export bookings to CSV
- ✅ Delete or edit bookings
- ✅ Generate revenue reports
- ✅ Email notifications for new bookings
- ✅ SMS alerts for flight changes
- ✅ Dashboard charts and graphs

---

## 📞 QUICK REFERENCE

| Action | Command |
|--------|---------|
| Migrate database | `python migrate_database.py` |
| Create admin | `python create_admin.py` |
| Start app | `cd frontend && python app.py` |
| Admin dashboard URL | `http://localhost:5000/admin` |
| All bookings URL | `http://localhost:5000/admin/bookings` |
| All users URL | `http://localhost:5000/admin/users` |
| All flights URL | `http://localhost:5000/admin/flights` |

---

**You're all set! Enjoy managing your flights! 🚀✈️**
