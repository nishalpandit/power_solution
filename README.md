# Power Solution API

Minimal FastAPI backend structured like Django, using SQLite (`db.sqlite3`) for the Flutter mobile application.

## Project Structure

```text
Power_solution/
├── manage.py            # Django-style command runner (runserver)
├── core/
│   ├── __init__.py
│   ├── settings.py      # App & SQLite database settings
│   └── auth.py          # JWT authentication helpers
├── api/
│   ├── __init__.py
│   ├── models.py        # Database models (placeholders)
│   ├── schemas.py       # Pydantic JSON schemas (placeholders)
│   └── views.py         # API endpoints (empty router)
├── db.sqlite3           # SQLite Database
├── main.py              # Application entry point
└── requirements.txt     # Dependencies
```

## How to Run the Project

### Option 1: CLI Runner (manage.py)
```bash
# Start development server
python manage.py runserver

# Specify custom port
python manage.py runserver 8000

# Synchronize database tables (SQLAlchemy)
python manage.py migrate

# Check database connection & list tables
python manage.py checkdb

# Create an administrator account
python manage.py createsuperuser
```

### Option 2: Direct Python
```bash
python main.py
```

### Option 3: Standard Uvicorn
```bash
uvicorn main:app --reload
```

---

### Interactive Documentation
Once running, open your browser to:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
