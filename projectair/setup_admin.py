#!/usr/bin/env python3
"""
Create Admin Account with Provided Details
"""

import sqlite3
import os
from werkzeug.security import generate_password_hash

db_path = 'flight_db.sqlite'

if not os.path.exists(db_path):
    print("❌ Database not found")
    exit(1)

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Admin details
    name = "saicharan"
    email = "balugusaicharan@gmail.com"
    password = "Saicharan@2005"
    phone = "8688789323"
    location = "hyderabad"
    
    # Hash password
    hashed_password = generate_password_hash(password)
    
    # Check if email already exists
    cursor.execute("SELECT user_id FROM users WHERE LOWER(email) = ?", (email.lower(),))
    existing = cursor.fetchone()
    
    if existing:
        print(f"\n⚠️  Email already exists! Updating to admin...\n")
        # Update existing user to admin
        cursor.execute("""
            UPDATE users 
            SET name=?, mobile=?, location=?, password=?, is_admin=1
            WHERE LOWER(email)=?
        """, (name, phone, location, hashed_password, email.lower()))
    else:
        print(f"\n📝 Creating new admin account...\n")
        # Create new admin
        cursor.execute("""
            INSERT INTO users (name, email, mobile, location, password, is_admin)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, email, phone, location, hashed_password, 1))
    
    conn.commit()
    conn.close()
    
    print("="*70)
    print("✅ ADMIN ACCOUNT CREATED/UPDATED SUCCESSFULLY!")
    print("="*70)
    print(f"\n📊 Admin Details:")
    print(f"   Name: {name}")
    print(f"   Email: {email}")
    print(f"   Phone: {phone}")
    print(f"   Location: {location}")
    print(f"   Status: ✅ ADMIN")
    print(f"\n🔗 Login Instructions:")
    print(f"   1. Go to: http://localhost:5000/login")
    print(f"   2. Email: {email}")
    print(f"   3. Password: {password}")
    print(f"   4. Click 'Login'")
    print(f"   5. Click RED '📊 Admin Panel' button")
    print(f"\n✨ Features Available:")
    print(f"   ✓ View all bookings")
    print(f"   ✓ Monitor all users")
    print(f"   ✓ Check flight occupancy")
    print(f"   ✓ Upload flight delays")
    print(f"\n" + "="*70 + "\n")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    exit(1)
