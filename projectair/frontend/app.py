from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session
import sqlite3
import os
import sys
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import random
import uuid

# Add parent directory to path so we can import setup_database
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your_secret_key_here_change_in_production')

# Session configuration
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Database path - relative to parent directory
DATABASE_URL = os.environ.get('DATABASE_URL', os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'flight_db.sqlite'))

# Initialize database when app starts (works with both local dev and gunicorn/production)
print(f"Initializing database at: {DATABASE_URL}")
from setup_database import initialize_db
if not os.path.exists(DATABASE_URL):
    print("Creating new database...")
    initialize_db()
else:
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()
    if not tables:
        print("Database exists but empty. Initializing tables...")
        initialize_db()
    else:
        print(f"✅ Database ready with {len(tables)} tables.")


# ============= DATABASE UTILITIES =============
def connect_db():
    """Create database connection with row factory"""
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    return conn


# Initialize database on startup
def init_db():
    """Initialize database tables only if database doesn't exist"""
    if not os.path.exists(DATABASE_URL):
        print(f"🗄️  Database file not found. Creating: {DATABASE_URL}")
        from setup_database import initialize_db
        initialize_db()
    else:
        # Verify tables exist
        conn = sqlite3.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()
        
        if not tables:
            print(f"⚠️  Database exists but no tables found. Initializing...")
            from setup_database import initialize_db
            initialize_db()
        else:
            print(f"✅ Database ready with {len(tables)} tables. No reinitialization needed.")


# ============= AUTHENTICATION ROUTES =============
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, name, password FROM users WHERE LOWER(email)=?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session.permanent = True
            session['user_id'] = user['user_id']
            session['username'] = user['name']
            return redirect(url_for('dashboard'))

        flash("Invalid credentials", "error")
        return render_template('login.html', error="Invalid credentials")

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name     = request.form['name']
        gender   = request.form.get('gender', '')
        location = request.form.get('location', '')
        dob      = request.form.get('dob', '')
        email    = request.form['email'].strip().lower()
        mobile   = request.form.get('mobile', '')
        pwd      = request.form['password']

        hashed = generate_password_hash(pwd)

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (name, gender, location, dob, email, mobile, password)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, gender, location, dob, email, mobile, hashed))
            conn.commit()
            conn.close()
            
            flash("Signup successful! Please log in.", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Email already exists!", "error")
            return render_template('signup.html')

    return render_template('signup.html')


@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        pwd   = request.form['password']
        hashed = generate_password_hash(pwd)

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password=? WHERE email=?", (hashed, email))
        conn.commit()
        conn.close()

        flash("Password reset successful! Please log in.", "success")
        return redirect(url_for('login'))
    
    return render_template('forgot.html')


# ============= MAIN APPLICATION ROUTES =============
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    first_letter = username[0].upper() if username else 'U'
    return render_template('dashboard.html', username=username, first_letter=first_letter)


@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for('login'))


@app.route('/general')
def general_info():
    return render_template('general.html')


# ============= FLIGHT BOOKING ROUTES =============
@app.route('/book_ticket', methods=['GET', 'POST'])
def book_ticket():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        src = request.form['source']
        dst = request.form['destination']
        dt  = request.form['date']
        return redirect(url_for('search_flights', source=src, destination=dst, date=dt))
    
    return render_template('book_ticket.html')


@app.route('/search_flights', methods=['GET'])
def search_flights():
    source      = request.args.get('source', '')
    destination = request.args.get('destination', '')
    date        = request.args.get('date', '')

    flights = []
    if source and destination:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, flight_number, departure_time, arrival_time, available_seats, price
            FROM flights
            WHERE source = ? AND destination = ?
        """, (source, destination))
        flights = cursor.fetchall()
        conn.close()

    return render_template('search_flights.html',
                           flights=flights,
                           source=source,
                           destination=destination,
                           selected_date=date)


@app.route('/book_ticket/<int:flight_id>', methods=['GET', 'POST'])
def booking(flight_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = connect_db()
    cursor = conn.cursor()

    # Fetch flight details
    cursor.execute("SELECT flight_number, source, destination, price FROM flights WHERE id=?", (flight_id,))
    flight = cursor.fetchone()

    if not flight:
        conn.close()
        return "Flight not found", 404

    flight_number = flight['flight_number']
    source = flight['source']
    destination = flight['destination']
    price = flight['price']

    if request.method == 'POST':
        date = request.form['date']
        passenger_count = int(request.form.get('passenger_count', 1))
        passengers = []

        for i in range(1, passenger_count + 1):
            name = request.form.get(f'name{i}')
            age = request.form.get(f'age{i}')
            nationality = request.form.get(f'nationality{i}')
            gender = request.form.get(f'gender{i}')

            if name and age and nationality and gender:
                cursor.execute("""
                    INSERT INTO bookings (user_id, flight_id, passenger_name, age, nationality, gender, date)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (session['user_id'], flight_id, name, age, nationality, gender, date))

                passengers.append({
                    'name': name,
                    'age': age,
                    'nationality': nationality,
                    'gender': gender
                })

        cursor.execute("UPDATE flights SET available_seats = available_seats - ? WHERE id = ?",
                       (passenger_count, flight_id))
        conn.commit()
        conn.close()

        session['booking_details'] = {
            'flight_number': flight_number,
            'id': flight_id,
            'source': source,
            'destination': destination,
            'selected_date': date,
            'passengers': passengers,
            'price': price,
            'total_amount': passenger_count * price
        }

        return redirect(url_for('payment'))

    conn.close()
    date = request.args.get('date', '')

    return render_template("booking.html",
                           flight_id=flight_id,
                           flight_number=flight_number,
                           date=date,
                           source=source,
                           destination=destination)


# ============= PAYMENT ROUTES =============
@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    booking = session.get('booking_details')
    if not booking:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        transaction_id = "TXN" + str(random.randint(100000, 999999))
        payment_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE bookings
            SET transaction_id = ?
            WHERE user_id = ? AND flight_id = ? AND transaction_id IS NULL
        """, (transaction_id, session['user_id'], booking['id']))
        conn.commit()
        conn.close()

        booking['transaction_id'] = transaction_id
        booking['payment_time'] = payment_time
        session['booking_details'] = booking

        flash("Payment successful!", "success")
        return redirect(url_for('payment_success'))

    return render_template("payment.html", total_amount=booking['total_amount'])


@app.route('/payment_success')
def payment_success():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    booking = session.get('booking_details')
    if not booking:
        return redirect(url_for('dashboard'))

    return render_template('payment_success.html',
                           transaction_id=booking['transaction_id'],
                           payment_time=booking['payment_time'],
                           total_amount=booking['total_amount'],
                           passengers=booking['passengers'],
                           flight_number=booking['flight_number'],
                           source=booking['source'],
                           destination=booking['destination'],
                           selected_date=booking['selected_date'])


# ============= BOOKING MANAGEMENT ROUTES =============
@app.route('/my_bookings')
def my_bookings():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT b.transaction_id, b.date AS selected_date, f.flight_number, f.source, f.destination, f.price,
               b.passenger_name AS name, b.age, b.gender, b.nationality
        FROM bookings b
        JOIN flights f ON b.flight_id = f.id
        WHERE b.user_id = ? AND b.transaction_id IS NOT NULL
        ORDER BY b.transaction_id DESC, b.id
    """, (session['user_id'],))

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return render_template('my_bookings.html', bookings=[])

    grouped_bookings = {}
    for row in rows:
        txn = row['transaction_id']
        if txn not in grouped_bookings:
            grouped_bookings[txn] = {
                'transaction_id': txn,
                'selected_date': row['selected_date'],
                'flight_number': row['flight_number'],
                'source': row['source'],
                'destination': row['destination'],
                'total_amount': 0,
                'passengers': []
            }
        grouped_bookings[txn]['passengers'].append({
            'name': row['name'],
            'age': row['age'],
            'gender': row['gender'],
            'nationality': row['nationality']
        })
        grouped_bookings[txn]['total_amount'] += row['price']

    return render_template('my_bookings.html', bookings=list(grouped_bookings.values()))


@app.route('/cancel_booking/<transaction_id>', methods=['GET', 'POST'])
def cancel_booking(transaction_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = connect_db()
    cursor = conn.cursor()

    # Get all bookings for this transaction
    cursor.execute("""
        SELECT b.id, b.flight_id
        FROM bookings b
        WHERE b.transaction_id = ? AND b.user_id = ?
    """, (transaction_id, session['user_id']))

    bookings = cursor.fetchall()

    if not bookings:
        conn.close()
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        # Refund seats and delete bookings
        for booking in bookings:
            cursor.execute("""
                UPDATE flights
                SET available_seats = available_seats + 1
                WHERE id = ?
            """, (booking['flight_id'],))

        cursor.execute("""
            DELETE FROM bookings
            WHERE transaction_id = ? AND user_id = ?
        """, (transaction_id, session['user_id']))

        conn.commit()
        conn.close()

        flash("Booking successfully cancelled and refund initiated!", "success")
        cancel_message = "Booking successfully cancelled and refund initiated!"
        return render_template('cancel_booking.html', transaction_id=transaction_id, cancel_message=cancel_message)

    conn.close()
    return render_template('cancel_booking.html', transaction_id=transaction_id)


# ============= PROFILE MANAGEMENT ROUTES =============
@app.route('/manage_profile', methods=['GET', 'POST'])
def manage_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = connect_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        gender = request.form.get('gender', '')
        location = request.form.get('location', '')
        dob = request.form.get('dob', '')
        mobile = request.form.get('mobile', '')
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if password:
            if password == confirm_password:
                hashed_password = generate_password_hash(password)
                cursor.execute("""
                    UPDATE users
                    SET name=?, gender=?, location=?, dob=?, mobile=?, password=?
                    WHERE user_id=?
                """, (name, gender, location, dob, mobile, hashed_password, user_id))
            else:
                conn.close()
                flash("Passwords do not match!", "error")
                return redirect(url_for('manage_profile'))
        else:
            cursor.execute("""
                UPDATE users
                SET name=?, gender=?, location=?, dob=?, mobile=?
                WHERE user_id=?
            """, (name, gender, location, dob, mobile, user_id))

        conn.commit()
        conn.close()

        session['username'] = name
        flash("Profile updated successfully!", "success")
        return redirect(url_for('dashboard'))

    # GET method - fetch existing user data
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()

    return render_template('manage_profile.html', user=user)


# ============= CUSTOMER SUPPORT ROUTES =============
@app.route('/customer_support', methods=['GET', 'POST'])
def customer_support():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = connect_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        message = request.form['message'].strip()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if message:
            # Insert user message
            cursor.execute("""
                INSERT INTO support_chat (user_id, message, timestamp)
                VALUES (?, ?, ?)
            """, (user_id, message, timestamp))

            # Simulated bot response
            bot_response = "Thank you for your message! Our support team will assist you shortly."
            cursor.execute("""
                INSERT INTO support_chat (user_id, message, timestamp)
                VALUES (?, ?, ?)
            """, (0, bot_response, timestamp))

            conn.commit()

    # Fetch chat history
    cursor.execute("""
        SELECT * FROM support_chat
        WHERE user_id = ? OR user_id = 0
        ORDER BY timestamp
    """, (user_id,))

    chat_history = cursor.fetchall()
    conn.close()

    return render_template('customer_support.html', chat_history=chat_history)


# ============= FLIGHT DELAY ROUTES =============
@app.route("/upload_delay", methods=["GET", "POST"])
def upload_delay():
    conn = connect_db()
    cursor = conn.cursor()

    if request.method == "POST":
        flight_number = request.form["flight_number"]
        delay_minutes = int(request.form.get("delay_minutes", 0))
        reason = request.form.get("reason", "")
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            cursor.execute("""
                INSERT INTO flight_delays (flight_number, delay_minutes, reason, created_at)
                VALUES (?, ?, ?, ?)
            """, (flight_number, delay_minutes, reason, created_at))
            conn.commit()
            flash("Flight delay recorded successfully!", "success")
        except Exception as e:
            flash(f"Error recording delay: {str(e)}", "error")

    # Fetch delay data
    cursor.execute("SELECT * FROM flight_delays ORDER BY id DESC")
    delays = cursor.fetchall()

    conn.close()

    return render_template("upload_delay.html", delays=delays)


# ============= ERROR HANDLERS =============
@app.errorhandler(404)
def not_found(error):
    return render_template('general.html'), 404


@app.errorhandler(500)
def server_error(error):
    flash("Internal server error. Please try again.", "error")
    return redirect(url_for('dashboard')), 500


if __name__ == "__main__":
    # Run app (local development only - gunicorn handles production)
    debug = os.environ.get('FLASK_ENV') == 'development'
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=debug)
