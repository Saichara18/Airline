# 🚀 ADMIN SETUP - QUICK START

## What Was Done ✅

1. **Database Updated**: Added `is_admin` column to users table
2. **Admin Routes Created**: New routes for admin dashboard and monitoring
3. **Admin Templates Created**: Beautiful dashboards for viewing bookings, users, and flights
4. **Admin Scripts Created**: Scripts to create and manage admin accounts

---

## 📋 Setup Steps (Quick)

### Step 1: Migrate Database
```powershell
cd f:\projectair
python migrate_database.py
```

### Step 2: Create Admin Account
```powershell
python create_admin.py
```

**Follow the prompts to:**
- Enter admin name
- Enter admin email
- Set a strong password
- (Optional) Add phone and location

### Step 3: Test the App
```powershell
cd frontend
python app.py
```

### Step 4: Login & Access Admin Panel
1. Go to `http://localhost:5000/login`
2. Login with your admin email and password
3. On dashboard, click **📊 Admin Panel** button
4. View bookings, users, and flights!

---

## 📊 Admin Features Available

### Dashboard
- View key statistics (total bookings, users, flights, seats)
- Quick navigation to all admin panels

### Bookings Monitor
- See ALL bookings from ALL users
- View customer details
- Check transaction IDs and payment status
- See all passengers on each booking

### Users Monitor
- View all registered customers
- See contact information
- Check how many bookings each user has

### Flights Monitor
- View all flights with occupancy rates
- See available seats
- Monitor flight popularity with visual bars

---

## 🔐 Login Credentials Example

```
Email: admin@projectair.com
Password: YourSecurePassword123
```

---

## ✨ What Changed in Code

### Files Modified:
1. **setup_database.py** - Added `is_admin INTEGER DEFAULT 0` to users table
2. **frontend/app.py** - Added admin routes and helper functions:
   - `/admin` - Admin dashboard
   - `/admin/bookings` - View all bookings
   - `/admin/users` - View all users
   - `/admin/flights` - View all flights
   - `is_admin()` - Helper to check if user is admin
3. **frontend/templates/dashboard.html** - Added "📊 Admin Panel" button for admins

### Files Created:
1. **create_admin.py** - Interactive script to create admin accounts
2. **migrate_database.py** - Adds is_admin column to existing database
3. **frontend/templates/admin_dashboard.html** - Admin dashboard UI
4. **frontend/templates/admin_bookings.html** - All bookings view
5. **frontend/templates/admin_users.html** - All users view
6. **frontend/templates/admin_flights.html** - All flights view
7. **ADMIN_SETUP.md** - Comprehensive admin setup guide
8. **QUICK_START.md** - This file!

---

## 🎯 Use Cases

### Use Case 1: Monitor Today's Bookings
1. Login as admin
2. Click "Admin Panel"
3. Click "📦 View All Bookings"
4. See all bookings with customer info and payment status

### Use Case 2: Check Flight Popularity
1. Login as admin
2. Click "Admin Panel"
3. Click "✈️ View All Flights"
4. View occupancy percentage and available seats
5. Identify which flights are fully booked

### Use Case 3: Monitor Customer Base
1. Login as admin
2. Click "Admin Panel"
3. Click "👥 View All Users"
4. See all registered customers and their total bookings
5. Identify frequent flyers

---

## 🆘 Troubleshooting

**Q: Admin button not showing?**
- Make sure you created admin account with `is_admin=1`
- Restart the app after creating admin

**Q: Can't access /admin route?**
- You must be logged in as admin user
- Regular users will get redirected

**Q: How to make existing user an admin?**
```python
import sqlite3
conn = sqlite3.connect('flight_db.sqlite')
cursor = conn.cursor()
cursor.execute("UPDATE users SET is_admin=1 WHERE email='user@email.com'")
conn.commit()
```

**Q: Forgot admin password?**
- Create a new admin account with a different email
- Or reset password using the forgot password feature on login page

---

## 🔗 Key Routes for Admin

| Route | Purpose |
|-------|---------|
| `/admin` | Admin Dashboard with statistics |
| `/admin/bookings` | View all bookings from all users |
| `/admin/users` | View all registered users |
| `/admin/flights` | View all flights with occupancy |

---

## 📈 Admin Features Summary

| Feature | Available |
|---------|-----------|
| View all bookings | ✅ Yes |
| View all users | ✅ Yes |
| View all flights | ✅ Yes |
| View booking statistics | ✅ Yes |
| View occupancy rates | ✅ Yes |
| Export data (CSV) | ⏳ Not yet (feature request) |
| Delete bookings | ⏳ Not yet (feature request) |
| Edit flight details | ⏳ Not yet (feature request) |

---

## 🚀 Next Steps

1. ✅ Create admin account
2. ✅ Test admin dashboard
3. ✅ Monitor bookings and users
4. ✅ Deploy to Render (admin account persists in database)

---

## 📞 Support

For more details, see: **ADMIN_SETUP.md**

Enjoy monitoring your flights! 🎉
