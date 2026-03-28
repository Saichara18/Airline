#!/usr/bin/env python3
"""
Test script to check database content
"""

import sqlite3
import os

db_path = 'flight_db.sqlite'

if not os.path.exists(db_path):
    print("❌ Database not found")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check flights
print("\n🛫 FLIGHTS IN DATABASE:")
print("=" * 60)
cursor.execute("SELECT id, flight_number, source, destination, available_seats, price FROM flights")
flights = cursor.fetchall()

if flights:
    for flight in flights:
        print(f"ID: {flight[0]}, Flight: {flight[1]}, {flight[2]} → {flight[3]}, Seats: {flight[4]}, Price: ₹{flight[5]}")
    print(f"\n✅ Total flights: {len(flights)}")
else:
    print("❌ NO FLIGHTS FOUND in database!")
    print("\n📝 You need to add flights first. Here are some sample flights you can add:\n")
    
    # Sample insert commands
    print("INSERT INTO flights (flight_number, source, destination, departure_time, arrival_time, available_seats, price)")
    print("VALUES ('AI-101', 'Delhi', 'Mumbai', '09:00', '11:30', 50, 5000);")
    print("\nINSERT INTO flights (flight_number, source, destination, departure_time, arrival_time, available_seats, price)")
    print("VALUES ('AI-102', 'Delhi', 'Bangalore', '10:00', '12:30', 60, 6000);")
    print("\nINSERT INTO flights (flight_number, source, destination, departure_time, arrival_time, available_seats, price)")
    print("VALUES ('AI-103', 'Mumbai', 'Goa', '11:00', '12:45', 45, 3500);\n")

# Check bookings
print("\n📦 BOOKINGS IN DATABASE:")
print("=" * 60)
cursor.execute("SELECT COUNT(*) FROM bookings")
booking_count = cursor.fetchone()[0]
print(f"Total bookings: {booking_count}")

# Check users
print("\n👥 USERS IN DATABASE:")
print("=" * 60)
cursor.execute("SELECT COUNT(*) FROM users WHERE is_admin=0")
user_count = cursor.fetchone()[0]
print(f"Regular users: {user_count}")

cursor.execute("SELECT COUNT(*) FROM users WHERE is_admin=1")
admin_count = cursor.fetchone()[0]
print(f"Admin users: {admin_count}")

conn.close()
print("\n" + "=" * 60)
