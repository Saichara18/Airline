#!/bin/bash
# Deployment initialization script for Render

echo "🚀 Starting ProjectAir deployment..."

# Install Python dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Initialize database
echo "🗄️  Initializing database..."
python setup_database.py

# Add sample flight data (optional - comment out if not needed)
python -c "
import sqlite3
import os

db_path = os.environ.get('DATABASE_URL', 'flight_db.sqlite')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Add sample flights
sample_flights = [
    ('AI101', 'New York', 'London', '08:00', '20:00', 100, 599.99),
    ('BA202', 'London', 'Paris', '10:30', '12:30', 150, 99.99),
    ('LH303', 'Berlin', 'Tokyo', '14:00', '09:00+1', 80, 899.99),
    ('AF404', 'Paris', 'New York', '18:00', '00:00+1', 120, 649.99),
    ('EK505', 'Dubai', 'London', '22:00', '06:00+1', 200, 549.99),
]

for flight in sample_flights:
    cursor.execute('''
        SELECT COUNT(*) FROM flights WHERE flight_number = ?
    ''', (flight[0],))
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO flights (flight_number, source, destination, departure_time, arrival_time, available_seats, price)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', flight)
        print(f'Added flight: {flight[0]}')

conn.commit()
conn.close()
print('✅ Sample flights loaded successfully!')
"

echo "✅ Deployment initialization complete!"
echo "🌐 Your app is ready to deploy on Render"
