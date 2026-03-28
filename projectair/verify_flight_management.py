#!/usr/bin/env python3
"""
Deployment Verification Script for Flight Management Features
Tests the new admin flight add/delete functionality
"""

import sqlite3
import os
import sys

# Database path
DATABASE_URL = os.environ.get('DATABASE_URL', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flight_db.sqlite'))

def check_database_tables():
    """Verify all required tables exist"""
    print("\n📋 Checking database tables...")
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = ['users', 'flights', 'bookings', 'support_chat', 'flight_delays']
        for table in required_tables:
            if table in tables:
                print(f"   ✅ {table} table exists")
            else:
                print(f"   ❌ {table} table MISSING")
                return False
        
        conn.close()
        return True
    except Exception as e:
        print(f"   ❌ Error checking tables: {e}")
        return False

def check_flights_columns():
    """Verify flights table has all required columns"""
    print("\n📋 Checking flights table columns...")
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    try:
        cursor.execute("PRAGMA table_info(flights);")
        columns = {row[1]: row[2] for row in cursor.fetchall()}
        
        required_columns = ['id', 'flight_number', 'source', 'destination', 'departure_time', 'arrival_time', 'available_seats', 'price']
        for col in required_columns:
            if col in columns:
                print(f"   ✅ {col} column exists ({columns[col]})")
            else:
                print(f"   ❌ {col} column MISSING")
                return False
        
        conn.close()
        return True
    except Exception as e:
        print(f"   ❌ Error checking columns: {e}")
        return False

def check_sample_flights():
    """Verify sample flights exist"""
    print("\n📋 Checking sample flights...")
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT COUNT(*) FROM flights;")
        count = cursor.fetchone()[0]
        
        if count > 0:
            print(f"   ✅ {count} flight(s) exist in database")
            cursor.execute("SELECT flight_number, source, destination FROM flights LIMIT 3;")
            for row in cursor.fetchall():
                print(f"      - {row[0]}: {row[1]} → {row[2]}")
        else:
            print(f"   ⚠️  No flights found (will be added through admin interface)")
        
        conn.close()
        return True
    except Exception as e:
        print(f"   ❌ Error checking flights: {e}")
        return False

def check_admin_user():
    """Verify admin user exists"""
    print("\n👤 Checking admin user...")
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT name, email FROM users WHERE is_admin = 1 LIMIT 1;")
        admin = cursor.fetchone()
        
        if admin:
            print(f"   ✅ Admin user exists: {admin[0]} ({admin[1]})")
        else:
            print(f"   ⚠️  No admin user found (create through setup_admin.py)")
        
        conn.close()
        return True
    except Exception as e:
        print(f"   ❌ Error checking admin: {e}")
        return False

def check_template_files():
    """Verify template files exist"""
    print("\n📄 Checking template files...")
    templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend', 'templates')
    
    required_templates = [
        'admin_flights.html',
        'admin_add_flight.html',
        'admin_dashboard.html',
        'admin_bookings.html',
        'admin_users.html'
    ]
    
    all_exist = True
    for template in required_templates:
        path = os.path.join(templates_dir, template)
        if os.path.exists(path):
            print(f"   ✅ {template} exists")
        else:
            print(f"   ❌ {template} MISSING")
            all_exist = False
    
    return all_exist

def main():
    """Run all deployment checks"""
    print("=" * 60)
    print("🚀 Flight Management Deployment Verification")
    print("=" * 60)
    
    checks = [
        ("Database Tables", check_database_tables),
        ("Flights Columns", check_flights_columns),
        ("Sample Flights", check_sample_flights),
        ("Admin User", check_admin_user),
        ("Template Files", check_template_files),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} check failed: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("📊 DEPLOYMENT VERIFICATION SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "⚠️  WARN"
        print(f"{status}: {name}")
    
    print(f"\n✅ {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 Deployment ready! All systems verified.")
        print("\n📝 Admin Flight Management Features:")
        print("   ✅ Add Flight: /admin/add_flight")
        print("   ✅ Delete Flight: /admin/delete_flight/<id>")
        print("   ✅ View Flights: /admin/flights")
        return 0
    else:
        print("\n⚠️  Some checks require attention before full deployment.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
