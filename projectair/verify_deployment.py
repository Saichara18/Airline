#!/usr/bin/env python3
"""
Deployment Verification Script
Checks if everything is ready for production deployment
"""

import os
import sqlite3

print("\n" + "="*80)
print("🚀 DEPLOYMENT VERIFICATION CHECKLIST")
print("="*80 + "\n")

checks_passed = 0
checks_failed = 0

# Check 1: Database exists
print("1️⃣  Checking database...")
if os.path.exists('flight_db.sqlite'):
    print("   ✅ Database exists: flight_db.sqlite")
    checks_passed += 1
else:
    print("   ❌ Database NOT found")
    checks_failed += 1

# Check 2: Admin account exists
print("\n2️⃣  Checking admin account...")
try:
    conn = sqlite3.connect('flight_db.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE is_admin=1")
    admin_count = cursor.fetchone()[0]
    if admin_count > 0:
        print(f"   ✅ Admin accounts found: {admin_count}")
        checks_passed += 1
        # Show admin details
        cursor.execute("SELECT name, email FROM users WHERE is_admin=1")
        for admin in cursor.fetchall():
            print(f"      • {admin[0]} ({admin[1]})")
    else:
        print("   ❌ No admin accounts found")
        checks_failed += 1
    conn.close()
except Exception as e:
    print(f"   ❌ Error checking admin: {str(e)}")
    checks_failed += 1

# Check 3: Flights exist
print("\n3️⃣  Checking flights...")
try:
    conn = sqlite3.connect('flight_db.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM flights")
    flight_count = cursor.fetchone()[0]
    if flight_count > 0:
        print(f"   ✅ Flights found: {flight_count}")
        checks_passed += 1
    else:
        print("   ⚠️  No flights found (users can add them)")
        checks_passed += 1
    conn.close()
except Exception as e:
    print(f"   ❌ Error checking flights: {str(e)}")
    checks_failed += 1

# Check 4: Key files exist
print("\n4️⃣  Checking key files...")
required_files = [
    'frontend/app.py',
    'setup_database.py',
    'requirements.txt',
    'Procfile',
    'render.yaml',
    'runtime.txt'
]

files_ok = 0
for file in required_files:
    if os.path.exists(file):
        print(f"   ✅ {file}")
        files_ok += 1
    else:
        print(f"   ❌ {file} NOT found")

if files_ok == len(required_files):
    checks_passed += 1
else:
    checks_failed += 1

# Check 5: Templates exist
print("\n5️⃣  Checking admin templates...")
templates = [
    'frontend/templates/admin_dashboard.html',
    'frontend/templates/admin_bookings.html',
    'frontend/templates/admin_users.html',
    'frontend/templates/admin_flights.html',
]

templates_ok = 0
for template in templates:
    if os.path.exists(template):
        print(f"   ✅ {template}")
        templates_ok += 1
    else:
        print(f"   ❌ {template} NOT found")

if templates_ok == len(templates):
    checks_passed += 1
else:
    checks_failed += 1

# Summary
print("\n" + "="*80)
print("📊 SUMMARY")
print("="*80)
print(f"✅ Checks Passed: {checks_passed}")
print(f"❌ Checks Failed: {checks_failed}")

if checks_failed == 0:
    print("\n🎉 ALL SYSTEMS GO! Ready for deployment!\n")
    print("📋 Next Steps:")
    print("   1. Commit changes: git add .")
    print("   2. Commit: git commit -m 'Production ready with admin system'")
    print("   3. Push: git push origin main")
    print("   4. Deploy on Render dashboard")
    print("\n🌐 Production URL: https://your-app.onrender.com")
    exit(0)
else:
    print(f"\n⚠️  Fix {checks_failed} issue(s) before deployment\n")
    exit(1)
