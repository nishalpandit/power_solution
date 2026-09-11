import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Base Directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database Configuration (SQLite)
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite3')}")

# Connect args needed for SQLite when using multithreading in FastAPI and to avoid lock errors
connect_args = {"check_same_thread": False, "timeout": 30} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Security & JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "power-solution-secret-key-change-in-production-2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days for mobile session persistence


def ensure_database_schema():
    import api.models  # Register all models with Base.metadata
    Base.metadata.create_all(bind=engine)

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


# Database dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
