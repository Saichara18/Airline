# Deployment Checklist for ProjectAir

## Pre-Deployment Verification ✅

### 1. Local Testing
- [ ] Run `pip install -r requirements.txt` successfully
- [ ] Run `python setup_database.py` - database initializes without errors
- [ ] Run `cd frontend && python app.py` - app starts without errors
- [ ] Test signup at `http://localhost:5000/signup`
- [ ] Test login at `http://localhost:5000/login`
- [ ] Test flight search functionality
- [ ] Test booking workflow
- [ ] Check database file `flight_db.sqlite` exists

### 2. Code Quality
- [ ] No MySQL imports remaining in app.py
- [ ] All database queries use SQLite syntax (? placeholders, not %s)
- [ ] All routes properly handle database connections (close them)
- [ ] No hardcoded database credentials
- [ ] `.env` file is in `.gitignore`

### 3. Environment Setup
- [ ] `.env.example` file exists with template variables
- [ ] `FLASK_ENV` is set to `production` in environment
- [ ] Generate strong `SECRET_KEY`:
```python
import secrets
print(secrets.token_hex(32))
```

### 4. File Structure Verification
- [ ] ✅ `setup_database.py` - uses SQLite
- [ ] ✅ `frontend/app.py` - uses SQLite
- [ ] ✅ `requirements.txt` - includes all dependencies
- [ ] ✅ `Procfile` - correct start command
- [ ] ✅ `render.yaml` - render deployment config
- [ ] ✅ `runtime.txt` - Python version specified
- [ ] ✅ `.gitignore` - excludes sensitive files
- [ ] ✅ `README.md` - deployment instructions

### 5. Git Repository
- [ ] Repository initialized: `git init`
- [ ] All files committed: `git add .`
- [ ] Meaningful commit message: `git commit -m "SQLite production ready"`
- [ ] Pushed to GitHub: `git push origin main`
- [ ] Verify files are visible on GitHub website

### 6. Render Setup
- [ ] Render account created at render.com
- [ ] GitHub repository connected to Render
- [ ] Web Service created with correct settings:
  - Runtime: Python 3.11
  - Build Command: `pip install -r requirements.txt && python setup_database.py`
  - Start Command: `cd frontend && gunicorn app:app`

### 7. Environment Variables on Render
Set in Render Dashboard → Environment:
- [ ] `FLASK_ENV` = `production`
- [ ] `SECRET_KEY` = (strong random value, NOT default)
- [ ] `DATABASE_URL` = `flight_db.sqlite`
- [ ] `PORT` = (leave empty, Render assigns it)

### 8. Deployment Verification
After deployment on Render:
- [ ] Visit your app URL
- [ ] Verify login page loads
- [ ] Test signup with new account
- [ ] Test login with created account
- [ ] Test flight search
- [ ] Check Render logs for errors: Render Dashboard → Logs
- [ ] Database file created: `flight_db.sqlite`

## Troubleshooting

### Build Fails
```
✗ Check build logs in Render dashboard
✗ Verify requirements.txt syntax
✗ Ensure no MySQL packages in requirements
✗ Check Python version compatibility
```

### App Won't Start
```
✗ Check app.py uses sqlite3, not mysql.connector
✗ Verify Procfile is in root directory
✗ Check SECRET_KEY is set in environment
✗ Look for import errors in logs
```

### Database Issues
```
✗ Verify setup_database.py is in root directory
✗ Check Procfile includes: release: python setup_database.py
✗ Ensure database path is correct in app.py
```

### Login/Users Not Working
```
✗ Clear session files: rm -rf flask_session/*
✗ Reinitialize database if needed
✗ Check user table exists: SELECT * FROM users;
```

## Production Security Checklist

- [ ] `SECRET_KEY` is strong random value (32+ characters)
- [ ] `FLASK_ENV=production`
- [ ] Database contains no test/default credentials
- [ ] HTTPS enabled (Render provides free SSL)
- [ ] Session cookies are secure (HTTPS only)
- [ ] No debug mode enabled in production
- [ ] Input validation on all forms
- [ ] SQL injection protection (parameterized queries ✓)
- [ ] CSRF protection if needed (add to forms later)

## Performance Optimization

- [ ] Use Render's paid tier for better reliability
- [ ] Consider PostgreSQL for better scalability
- [ ] Add caching headers for static files
- [ ] Enable compression for responses
- [ ] Monitor Render CPU/Memory usage

## Post-Deployment

- [ ] Monitor app logs for errors
- [ ] Test all critical user flows
- [ ] Have a rollback plan if issues occur
- [ ] Set up uptime monitoring
- [ ] Plan regular backups of SQLite database

## Quick Deployment Command Reference

```bash
# Local testing
python setup_database.py
cd frontend && python app.py

# Deployment
git add .
git commit -m "SQLite production ready"
git push origin main
# Then deploy on Render dashboard
```

---

✅ **All items checked?** You're ready to deploy! 🚀

### Need Help?
- Render Docs: https://render.com/docs
- Flask Docs: https://flask.palletsprojects.com/
- SQLite Docs: https://sqlite.org/
