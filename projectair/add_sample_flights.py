#!/usr/bin/env python3
"""
Add sample flights to database
"""

import sqlite3
import os
from datetime import datetime, timedelta

db_path = 'flight_db.sqlite'

if not os.path.exists(db_path):
    print("❌ Database not found")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Sample flights data
flights_data = [
    ('AI-101', 'Delhi', 'Mumbai', '09:00', '11:30', 50, 5000),
    ('AI-102', 'Delhi', 'Bangalore', '10:00', '12:30', 60, 6000),
    ('AI-103', 'Mumbai', 'Goa', '11:00', '12:45', 45, 3500),
    ('AI-104', 'Bangalore', 'Chennai', '13:00', '14:30', 55, 4500),
    ('AI-105', 'Delhi', 'Kolkata', '14:00', '17:00', 70, 7000),
    ('AI-106', 'Mumbai', 'Hyderabad', '15:00', '17:00', 50, 5500),
    ('AI-107', 'Delhi', 'Jaipur', '16:00', '17:30', 40, 2500),
    ('AI-108', 'Bangalore', 'Kerala', '08:00', '09:30', 65, 4000),
]

try:
    for flight in flights_data:
        cursor.execute("""
            INSERT INTO flights (flight_number, source, destination, departure_time, arrival_time, available_seats, price)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, flight)
    
    conn.commit()
    conn.close()
    
    print("✅ Sample flights added successfully!\n")
    print("Flights added:")
    print("=" * 80)
    for i, flight in enumerate(flights_data, 1):
        print(f"{i}. Flight: {flight[0]:<8} | Route: {flight[1]:<12} → {flight[2]:<12} | "
              f"Seats: {flight[5]:<3} | Price: ₹{flight[6]:<6}")
    print("=" * 80)
    print("\n✅ Now go to /admin/flights and you'll see the flights with occupancy!")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    conn.close()
    exit(1)
