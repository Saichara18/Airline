# Admin Account Setup Guide

## 🔐 Creating an Admin Account

### Method 1: Using the Admin Creator Script (RECOMMENDED)

1. **Navigate to project root:**
   ```bash
   cd f:\projectair
   ```

2. **Run the admin creator script:**
   
   **On Windows (PowerShell):**
   ```powershell
   python create_admin.py
   ```
   
   **On Windows (Command Prompt):**
   ```cmd
   python create_admin.py
   ```

3. **Follow the interactive prompts:**
   - Enter admin name
   - Enter email (must be unique)
   - Enter password (minimum 6 characters)
   - Confirm password
   - Enter optional details (mobile, location)

4. **Account created!** 🎉
   - You'll see confirmation with the admin ID
   - You can now login with the admin email and password

### Method 2: Direct Database Insertion (Advanced)

If you prefer to directly insert into the database:

```python
import sqlite3
from werkzeug.security import generate_password_hash

db_path = 'flight_db.sqlite'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Hash your password
hashed_pwd = generate_password_hash('your_password_here')

# Insert admin user
cursor.execute("""
    INSERT INTO users (name, email, mobile, location, password, is_admin)
    VALUES (?, ?, ?, ?, ?, ?)
""", ('Admin Name', 'admin@email.com', '9999999999', 'City', hashed_pwd, 1))

conn.commit()
conn.close()
print("✅ Admin account created!")
```

---

## 📊 Accessing the Admin Dashboard

### Login Process:
1. Go to `http://localhost:5000/login` (local) or your deployed URL
2. Enter your admin email and password
3. Click "Login"
4. On the dashboard, click the **📊 Admin Panel** button (red button, only visible for admins)
5. You'll be redirected to the Admin Dashboard

### Admin Panel URL:
- Direct access: `/admin`
- Example: `http://localhost:5000/admin`

**Note:** Only users with `is_admin=1` can access admin routes. Regular users will be redirected with an error message.

---

## 🎯 Admin Features

### 1. **Admin Dashboard** (`/admin`)
View key metrics:
- Total Bookings
- Completed Bookings  
- Total Users
- Total Flights
- Available Seats Across All Flights
- Quick navigation to all management panels

### 2. **View All Bookings** (`/admin/bookings`)
Monitor every booking in the system:
- Transaction ID
- Customer name and email
- Flight details (number, route)
- All passengers on the booking
- Booking date
- Total amount paid
- Status (Completed/Pending)
- **Group bookings by transaction** - see all passengers under one transaction

### 3. **View All Users** (`/admin/users`)
See all registered customers:
- Name
- Email
- Phone number
- Location
- Date of birth
- Total bookings count per user

### 4. **View All Flights** (`/admin/flights`)
Monitor flight status and occupancy:
- Flight number
- Route (source → destination)
- Departure & arrival times
- **Occupancy percentage** with visual bar
- Available seats count
- Price per ticket

---

## 📈 Monitoring & Analytics

### Key Metrics to Monitor:

1. **Occupancy Rate**: Check flights tab to see which flights are fully booked
   - High occupancy = Popular route
   - Low occupancy = Consider promotions

2. **User Activity**: View users tab to see who has bookings
   - Total bookings per user
   - Identify frequent flyers

3. **Booking Revenue**: In bookings tab, sum up total amounts
   - Track revenue per route
   - Identify peak booking periods

4. **Pending Bookings**: Look for "PENDING" status bookings
   - May indicate incomplete transactions
   - Follow up with customers if needed

---

## 🔧 Database Schema Changes

The users table has been updated with:
```sql
ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0;
```

- `is_admin = 0`: Regular user (cannot access admin features)
- `is_admin = 1`: Admin user (can access admin dashboard and all features)

---

## 🔒 Security Notes

1. **Admin Password**: Use strong passwords (12+ characters with mixed case, numbers, symbols)
2. **Email Uniqueness**: Admin email must be unique in the system
3. **Admin Access**: Only users with `is_admin=1` can access admin routes
4. **Session Security**: Admin session is same as user session - logout clears it
5. **No Delete Permission**: Currently, admins can VIEW data but cannot delete
   - Future enhancement: Add delete/edit capabilities as needed

---

## ✅ Verification Checklist

- [ ] Admin account created using create_admin.py
- [ ] Can login with admin email and password
- [ ] Admin Dashboard button appears on user dashboard
- [ ] Can access /admin/bookings and see all bookings
- [ ] Can access /admin/users and see all users
- [ ] Can access /admin/flights and see flight occupancy
- [ ] Can logout from admin panel
- [ ] Regular user cannot access admin routes

---

## 🚀 Deployment Notes

### For Render Deployment:

1. **Before deploying**: Create admin account locally
   ```bash
   python create_admin.py
   ```

2. **The admin account will persist** in the SQLite database file once created

3. **First login after deployment**:
   - Use your admin credentials to login
   - Navigate to `/admin` to access admin dashboard

4. **If you need to create admin on production**:
   - Connect via SSH or use Render's database access
   - Run the create_admin.py script or use direct database insertion

---

## 🐛 Troubleshooting

### Admin button not showing on dashboard?
✅ Solution: Check if `is_admin` column exists in database
```sql
PRAGMA table_info(users);
```

### Cannot access admin routes?
✅ Solution: Verify user has `is_admin=1`
```sql
SELECT user_id, name, email, is_admin FROM users WHERE email='admin@email.com';
```

### Database doesn't have `is_admin` column?
✅ Solution: Manually add the column
```sql
ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0;
```

### Script says email already exists?
✅ Solution: Use a different email or update existing user to admin:
```sql
UPDATE users SET is_admin=1 WHERE email='existing@email.com';
```

---

## 📝 Example Workflow

**Scenario**: You want to monitor today's bookings

1. Login with admin account
2. Click "📊 Admin Panel" button
3. Check the statistics (total bookings, completed, available seats)
4. Click "📦 View All Bookings"
5. See all bookings with customer names, flight routes, passengers, and amounts
6. Identify any pending bookings that need follow-up
7. Click "✈️ View All Flights" to check occupancy
8. Go back and click "👥 View All Users" to see active customers

---

## 🎓 Next Steps

Some features you might want to add later:

- ✅ Export bookings to CSV/Excel
- ✅ Delete/Edit bookings (admin function)
- ✅ Generate revenue reports
- ✅ Add multiple admin accounts with different permissions
- ✅ Email notifications for new bookings
- ✅ SMS alerts for flight changes
- ✅ Dashboard charts and graphs

---

**Need help?** Check the troubleshooting section or review the app.py admin routes code!
