# Flight Booking System - ProjectAir

A Flask-based flight booking web application with SQLite database for fast, lightweight deployment.

## Features

- User authentication (signup, login, forgot password)
- Flight search and booking
- Booking management (view, cancel)
- Payment processing
- User profile management
- Customer support chat
- Flight delay tracking

## Technology Stack

- **Backend**: Flask, Python
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Render, Gunicorn

## Local Setup

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Installation

1. **Create and activate virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Initialize database:**
```bash
python setup_database.py
```

4. **Run the application:**
```bash
cd frontend
python app.py
```

The app will start at `http://localhost:5000`

## Production Deployment on Render

### Step 1: Prepare Your Code

1. **Copy `.env.example` to `.env` and update with your values:**
```bash
cp .env.example .env
```

2. **Commit all files to Git:**
```bash
git add .
git commit -m "Update to SQLite for production deployment"
git push
```

### Step 2: Create Render Service

1. Go to [Render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. **Configure:**
   - **Name**: projectair
   - **Runtime**: Python 3.11
   - **Build Command**: `pip install -r requirements.txt && python setup_database.py`
   - **Start Command**: `cd frontend && gunicorn app:app`
   - **Plan**: Free (or paid for better performance)

### Step 3: Set Environment Variables

In Render dashboard → Environment Variables:
```
FLASK_ENV = production
SECRET_KEY = (generate a strong key)
DATABASE_URL = flight_db.sqlite
PORT = (leave empty, Render assigns it)
```

### Step 4: Deploy

1. Click "Create Web Service"
2. Render will automatically deploy your app
3. Visit your app URL once deployment is complete

## Important Notes

### Database Persistence on Render

SQLite stores data in a single file (`flight_db.sqlite`). On Render's free tier:
- Data persists between deployments
- However, Render can restart your service, potentially causing brief downtime
- For production, consider upgrading to Render's paid tier for persistent disks

### For Production Grade with Persistent Database

If you need guaranteed persistence, consider:

1. **PostgreSQL** (recommended for production):
```bash
pip install psycopg2-binary
```
Update app.py to use PostgreSQL connection string

2. **Using Render Disk** (paid feature):
Configure persistent disk mount for SQLite files

## API Endpoints

### Authentication
- `POST /login` - User login
- `POST /signup` - User registration
- `GET /logout` - User logout

### Flight Booking
- `GET /search_flights` - Search flights
- `GET /book_ticket/<flight_id>` - Book ticket
- `POST /payment` - Process payment
- `GET /payment_success` - Payment confirmation

### Booking Management
- `GET /my_bookings` - View user bookings
- `GET /cancel_booking/<transaction_id>` - Cancel booking

### User Profile
- `GET/POST /manage_profile` - Manage user profile

### Support
- `GET/POST /customer_support` - Customer support chat
- `GET/POST /upload_delay` - Report flight delays

## File Structure

```
projectair/
├── frontend/
│   ├── app.py                 # Main Flask application
│   ├── templates/             # HTML templates
│   ├── static/                # CSS, JS, images
│   └── yes.py                 # Additional module
├── setup_database.py          # Database initialization
├── initialize_db.py           # (Empty, can be deleted)
├── requirements.txt           # Python dependencies
├── Procfile                   # Render deployment config
├── render.yaml               # Render service config
├── .env.example              # Environment variables template
├── .gitignore               # Git ignore file
└── README.md                # This file
```

## Environment Variables

Create a `.env` file with:
```
FLASK_ENV=production
SECRET_KEY=your_secret_key_here
DATABASE_URL=flight_db.sqlite
PORT=5000
```

## Troubleshooting

### Database Issues
- If tables don't exist, the app will auto-initialize on first run
- To reset database locally: delete `flight_db.sqlite` and restart app

### Import Errors
```bash
pip install --upgrade -r requirements.txt
```

### Port Already in Use
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :5000   # Windows
```

### Render Deployment Issues
1. Check build logs in Render dashboard
2. Ensure `Procfile` and `requirements.txt` are in root directory
3. Verify `FLASK_ENV` is set to `production`

## Security Notes

⚠️ **IMPORTANT**: Before deploying to production:

1. Change `SECRET_KEY` to a strong random value:
```python
import secrets
secrets.token_hex(32)  # Generate strong key
```

2. Set `FLASK_ENV=production` in Render environment variables

3. Enable HTTPS (Render provides free SSL)

4. Add input validation and sanitization

5. Use password hashing (already implemented with werkzeug)

## Future Improvements

- [ ] Add email verification on signup
- [ ] Implement real payment gateway (Stripe/PayPal)
- [ ] Add admin panel
- [ ] Implement email notifications
- [ ] Add two-factor authentication
- [ ] Migrate to PostgreSQL for better scalability
- [ ] Add automated backups

## Support

For issues or questions, please refer to:
- Flask Documentation: https://flask.palletsprojects.com/
- Render Documentation: https://render.com/docs
- SQLite Documentation: https://sqlite.org/docs.html

## License

This project is provided as-is for educational purposes.
