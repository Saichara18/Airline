#!/usr/bin/env python3
"""
Check Admin Accounts Script
View all users and their admin status
"""

import sqlite3
import os

db_path = 'flight_db.sqlite'

if not os.path.exists(db_path):
    print("❌ Database not found")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("\n" + "="*80)
print("👤 ALL USERS IN DATABASE")
print("="*80 + "\n")

# Get all users with their admin status
cursor.execute("""
    SELECT user_id, name, email, is_admin FROM users ORDER BY user_id
""")

users = cursor.fetchall()

if not users:
    print("❌ No users found in database\n")
    conn.close()
    exit(1)

print(f"{'ID':<5} {'Name':<20} {'Email':<30} {'Admin Status':<15}")
print("-" * 80)

admin_count = 0
user_count = 0

for user in users:
    user_id, name, email, is_admin = user
    
    if is_admin == 1:
        status = "✅ ADMIN"
        admin_count += 1
    else:
        status = "❌ Regular User"
        user_count += 1
    
    # Truncate long names/emails for display
    name_display = name[:18] if len(name) > 18 else name
    email_display = email[:28] if len(email) > 28 else email
    
    print(f"{user_id:<5} {name_display:<20} {email_display:<30} {status:<15}")

print("-" * 80)
print(f"\nSummary:")
print(f"  ✅ Admin users: {admin_count}")
print(f"  ❌ Regular users: {user_count}")
print(f"  📊 Total users: {len(users)}\n")

if admin_count == 0:
    print("⚠️  WARNING: No admin users found!")
    print("   Run: python create_admin.py\n")
else:
    print("✅ Admins can access: /admin, /admin/bookings, /admin/users, /admin/flights\n")

conn.close()
print("="*80)
