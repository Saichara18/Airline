#!/usr/bin/env python3
"""
Admin Account Creator Script
Run this to create an admin account for monitoring flights and bookings
"""

import sqlite3
import os
from werkzeug.security import generate_password_hash

def create_admin_account():
    db_path = os.environ.get('DATABASE_URL', 'flight_db.sqlite')
    
    # Check if database exists
    if not os.path.exists(db_path):
        print(f"❌ Database not found at: {db_path}")
        print("Please run setup_database.py first!")
        return False
    
    print("\n" + "="*60)
    print("🔐 PROJECTAIR ADMIN ACCOUNT CREATOR")
    print("="*60 + "\n")
    
    # Get admin details
    print("Please provide admin account details:\n")
    
    name = input("👤 Admin Name: ").strip()
    if not name:
        print("❌ Name cannot be empty!")
        return False
    
    email = input("📧 Email: ").strip().lower()
    if not email:
        print("❌ Email cannot be empty!")
        return False
    
    while True:
        password = input("🔒 Password (min 6 characters): ").strip()
        if len(password) < 6:
            print("⚠️  Password must be at least 6 characters!")
            continue
        
        confirm = input("🔒 Confirm Password: ").strip()
        if password != confirm:
            print("⚠️  Passwords don't match!")
            continue
        break
    
    mobile = input("📱 Mobile (optional, press Enter to skip): ").strip() or None
    location = input("📍 Location (optional, press Enter to skip): ").strip() or None
    
    # Hash password
    hashed_password = generate_password_hash(password)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if email already exists
        cursor.execute("SELECT user_id FROM users WHERE LOWER(email) = ?", (email.lower(),))
        if cursor.fetchone():
            print("\n❌ Email already exists! Please use a different email.")
            conn.close()
            return False
        
        # Create admin account
        cursor.execute("""
            INSERT INTO users (name, email, mobile, location, password, is_admin)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, email, mobile, location, hashed_password, 1))
        
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        
        print("\n" + "="*60)
        print("✅ ADMIN ACCOUNT CREATED SUCCESSFULLY!")
        print("="*60)
        print(f"\n📊 Admin Details:")
        print(f"   ID: {user_id}")
        print(f"   Name: {name}")
        print(f"   Email: {email}")
        print(f"   Status: Active")
        print(f"\n🔗 Access Admin Panel:")
        print(f"   1. Login with the admin email and password")
        print(f"   2. Go to: /admin (or click Admin Dashboard)")
        print(f"\n📈 Admin Features:")
        print(f"   ✓ View all bookings from all users")
        print(f"   ✓ Monitor flight occupancy")
        print(f"   ✓ View all registered users")
        print(f"   ✓ Check booking statistics")
        print("\n" + "="*60 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error creating admin account: {str(e)}")
        return False


if __name__ == '__main__':
    success = create_admin_account()
    exit(0 if success else 1)
