# 🚀 QUICK START - COPY & PASTE COMMANDS

## For Windows Users

### 1️⃣ Initial Setup (One Time)
```powershell
# Open PowerShell in project directory
cd f:\projectair
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
python setup_database.py
```

### 2️⃣ Run Locally
```powershell
venv\Scripts\activate.bat
cd frontend
python app.py
# Visit: http://localhost:5000
```

### 3️⃣ Deploy to Render
```bash
git add .
git commit -m "SQLite production ready"
git push origin main
# Then go to Render.com and deploy from dashboard
```

---

## For Mac/Linux Users

### 1️⃣ Initial Setup (One Time)
```bash
cd ~/projectair
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python setup_database.py
```

### 2️⃣ Run Locally
```bash
source venv/bin/activate
cd frontend
python app.py
# Visit: http://localhost:5000
```

### 3️⃣ Deploy to Render
```bash
git add .
git commit -m "SQLite production ready"
git push origin main
# Then go to Render.com and deploy from dashboard
```

---

## Environment Variables for Render

```
FLASK_ENV=production
SECRET_KEY=your_random_secret_key_here
DATABASE_URL=flight_db.sqlite
```

To generate SECRET_KEY:
```python
import secrets
print(secrets.token_hex(32))
```

---

## File Changes Summary

**Updated (MySQL → SQLite):**
- ✅ frontend/app.py
- ✅ setup_database.py
- ✅ frontend/yes.py

**New (Production):**
- ✅ requirements.txt
- ✅ Procfile
- ✅ render.yaml
- ✅ runtime.txt
- ✅ config.py
- ✅ setup.bat
- ✅ deploy.sh
- ✅ .env.example
- ✅ .gitignore

**New (Documentation):**
- ✅ README.md
- ✅ PRODUCTION_GUIDE.md
- ✅ DEPLOYMENT_CHECKLIST.md
- ✅ CONVERSION_COMPLETE.md

---

## Test Commands

```bash
# Test database
python -c "from setup_database import initialize_db; initialize_db()"

# Check database tables
sqlite3 flight_db.sqlite ".tables"

# Test Flask app imports
python -c "from frontend.app import app; print('✅ App imports successfully')"

# Run test utility
python frontend/yes.py
```

---

## Troubleshooting Quick Fixes

```bash
# Clear python cache
find . -type d -name __pycache__ -exec rm -r {} +

# Delete database and reinit
rm flight_db.sqlite
python setup_database.py

# Update dependencies
pip install --upgrade -r requirements.txt

# Kill process on port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -ti:5000 | xargs kill -9
```

---

## Render Deployment Checklist

- [ ] `.env` file added to `.gitignore`
- [ ] `requirements.txt` in root directory
- [ ] `Procfile` in root directory
- [ ] `setup_database.py` in root directory
- [ ] `frontend/app.py` exists
- [ ] Repository pushed to GitHub
- [ ] Render account created
- [ ] Repository connected to Render
- [ ] Build command: `pip install -r requirements.txt && python setup_database.py`
- [ ] Start command: `cd frontend && gunicorn app:app`
- [ ] Environment variables set in Render
- [ ] Deploy button clicked
- [ ] App URL visits successfully

---

## Important Notes

1. **DELETE `initialize_db.py`** - It's no longer used
   ```bash
   rm initialize_db.py
   ```

2. **NEVER COMMIT `.env`** - Use `.env.example` instead
   ```bash
   cp .env.example .env
   ```

3. **Generate STRONG SECRET_KEY**:
   ```python
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

4. **Test Before Deploying**:
   - Run locally first
   - Test signup/login
   - Test flight search
   - Test booking flow

---

## Key Differences from MySQL

| MySQL | SQLite |
|-------|--------|
| `import mysql.connector` | `import sqlite3` |
| `cursor.execute(..., %s)` | `cursor.execute(..., ?)` |
| `cursor.fetchone()` returns tuple | `cursor.fetchone()` returns Row object |
| External server required | Single file database |
| production workaround | ✅ Production ready |

---

## Database Location

- **Local**: `flight_db.sqlite` (in project root)
- **Render**: `flight_db.sqlite` (in app container)

---

## Useful Links

- Create strong key: https://generate-random.org/
- Render docs: https://render.com/docs
- Flask docs: https://flask.palletsprojects.com/
- SQLite docs: https://sqlite.org/

---

## Still Having Issues?

1. Check **DEPLOYMENT_CHECKLIST.md**
2. Check **PRODUCTION_GUIDE.md**
3. Check **README.md** troubleshooting section
4. Review Render logs: Dashboard → Logs

---

**Ready to deploy? You've got this! 🚀**
