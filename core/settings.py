import os
import urllib.parse
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# ── Base Directory ──────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from a .env file in the project root.
load_dotenv(BASE_DIR / '.env')

# ── Security ────────────────────────────────────────────────────────────────
SECRET_KEY = os.environ.get('SECRET_KEY', os.environ.get('SESSION_SECRET', 'power-solution-secret-key-change-in-production-2026'))
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True').lower() in ('true', '1', 'yes')

ALLOWED_HOSTS = ['*']

ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days for mobile session persistence

# ── Internationalization & Timezone ─────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = os.environ.get('TIME_ZONE', 'Asia/Kolkata')
USE_I18N = True
USE_TZ = False

# ── Static & Media files ────────────────────────────────────────────────────
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/uploads/'
MEDIA_ROOT = BASE_DIR / 'uploads'

# ── Database ────────────────────────────────────────────────────────────────
# Configured for both cPanel MySQL and local SQLite fallback.
MYSQL_DB = os.environ.get('MYSQL_DATABASE', '')
MYSQL_USER = os.environ.get('MYSQL_USER', '')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
MYSQL_PORT = os.environ.get('MYSQL_PORT', '3306')

if MYSQL_DB:
    # URL-encode password in case it contains special characters
    encoded_pass = urllib.parse.quote_plus(MYSQL_PASSWORD)
    user_part = f"{MYSQL_USER}:{encoded_pass}@" if MYSQL_USER else ""
    DATABASE_URL = f"mysql+pymysql://{user_part}{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8mb4"
    connect_args = {
        "init_command": "SET time_zone = '+05:30'",
        "charset": "utf8mb4",
    }
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': MYSQL_DB,
            'USER': MYSQL_USER,
            'PASSWORD': MYSQL_PASSWORD,
            'HOST': MYSQL_HOST,
            'PORT': MYSQL_PORT,
            'OPTIONS': {
                'charset': 'utf8mb4',
                'init_command': "SET time_zone = '+05:30'",
            },
        }
    }
else:
    DATABASE_URL = os.environ.get('DATABASE_URL', f"sqlite:///{BASE_DIR / 'db.sqlite3'}")
    connect_args = {"check_same_thread": False, "timeout": 30} if DATABASE_URL.startswith("sqlite") else {}
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3' if DATABASE_URL.startswith("sqlite") else 'django.db.backends.mysql',
            'NAME': str(BASE_DIR / 'db.sqlite3') if DATABASE_URL.startswith("sqlite") else 'power_solution',
        }
    }

# SQLAlchemy engine & session for FastAPI backend
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_recycle=3600 if not DATABASE_URL.startswith("sqlite") else -1,
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ── Database Dependency & Schema Initializer ────────────────────────────────
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def ensure_database_schema():
    import api.models  # Register all models with Base.metadata
    Base.metadata.create_all(bind=engine)

    # SQLite-specific WAL mode and legacy schema checks
    if not DATABASE_URL.startswith("sqlite"):
        return

    with engine.begin() as connection:
        connection.exec_driver_sql("PRAGMA journal_mode=WAL")

        table_exists = connection.exec_driver_sql(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
        ).fetchone()

        if not table_exists:
            return

        columns = connection.exec_driver_sql("PRAGMA table_info(users)").fetchall()
        existing_columns = {column[1] for column in columns}

        if "full_name" not in existing_columns:
            connection.exec_driver_sql(
                "ALTER TABLE users ADD COLUMN full_name VARCHAR(100) NOT NULL DEFAULT ''"
            )
        if "phone_number" not in existing_columns:
            connection.exec_driver_sql(
                "ALTER TABLE users ADD COLUMN phone_number VARCHAR(20) NOT NULL DEFAULT ''"
            )
        if "is_active" not in existing_columns:
            connection.exec_driver_sql(
                "ALTER TABLE users ADD COLUMN is_active BOOLEAN NOT NULL DEFAULT 1"
            )
        if "updated_at" not in existing_columns:
            connection.exec_driver_sql(
                "ALTER TABLE users ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
            )
        if "username" not in existing_columns:
            connection.exec_driver_sql(
                "ALTER TABLE users ADD COLUMN username VARCHAR(80)"
            )

        if "username" in existing_columns:
            legacy_table = connection.exec_driver_sql(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='users_legacy'"
            ).fetchone()
            if legacy_table:
                connection.exec_driver_sql("DROP TABLE users_legacy")

            if "full_name" not in existing_columns:
                connection.exec_driver_sql("ALTER TABLE users RENAME TO users_legacy")
                Base.metadata.tables["users"].create(bind=engine)
                connection.exec_driver_sql(
                    """
                    INSERT INTO users (id, full_name, email, phone_number, password_hash, role, is_active, created_at, updated_at)
                    SELECT id, COALESCE(username, ''), email, '', password_hash, role, 1, created_at, CURRENT_TIMESTAMP
                    FROM users_legacy
                    """
                )
                connection.exec_driver_sql("DROP TABLE users_legacy")
                return

        # Check and migrate invoices columns
        inv_table = connection.exec_driver_sql(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='invoices'"
        ).fetchone()
        if inv_table:
            inv_cols = {col[1] for col in connection.exec_driver_sql("PRAGMA table_info(invoices)").fetchall()}
            if "category" not in inv_cols:
                connection.exec_driver_sql("ALTER TABLE invoices ADD COLUMN category VARCHAR(100) DEFAULT 'Lift'")
            if "invoice_type" not in inv_cols:
                connection.exec_driver_sql("ALTER TABLE invoices ADD COLUMN invoice_type VARCHAR(50) DEFAULT 'Sales'")
            if "user_id" not in inv_cols:
                connection.exec_driver_sql("ALTER TABLE invoices ADD COLUMN user_id INTEGER REFERENCES users(id)")

        # Check and migrate payments columns
        pay_table = connection.exec_driver_sql(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='payments'"
        ).fetchone()
        if pay_table:
            pay_cols = {col[1] for col in connection.exec_driver_sql("PRAGMA table_info(payments)").fetchall()}
            if "payment_no" not in pay_cols:
                connection.exec_driver_sql("ALTER TABLE payments ADD COLUMN payment_no VARCHAR(60)")
            if "user_id" not in pay_cols:
                connection.exec_driver_sql("ALTER TABLE payments ADD COLUMN user_id INTEGER REFERENCES users(id)")
            if "invoice_id" not in pay_cols:
                connection.exec_driver_sql("ALTER TABLE payments ADD COLUMN invoice_id INTEGER REFERENCES invoices(id)")
            if "invoice_desc" not in pay_cols:
                connection.exec_driver_sql("ALTER TABLE payments ADD COLUMN invoice_desc VARCHAR(150)")
            if "category" not in pay_cols:
                connection.exec_driver_sql("ALTER TABLE payments ADD COLUMN category VARCHAR(100)")
            if "payment_time" not in pay_cols:
                connection.exec_driver_sql("ALTER TABLE payments ADD COLUMN payment_time VARCHAR(50)")
