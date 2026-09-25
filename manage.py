import os
import sys

# Ensure current project directory is on sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


def mask_db_url(url: str) -> str:
    """Mask sensitive password in DB connection string for safe printing."""
    if "@" in url and "://" in url:
        prefix, rest = url.split("://", 1)
        if ":" in rest.split("@")[0]:
            user_info, host_info = rest.split("@", 1)
            user = user_info.split(":")[0]
            return f"{prefix}://{user}:******@{host_info}"
    return url


def run_migrate():
    print("\n==========================================")
    print("  Power Solution - Database Migration     ")
    print("==========================================")
    try:
        import sqlalchemy
        from core.settings import DATABASE_URL, engine, ensure_database_schema

        print(f"[*] Database URL: {mask_db_url(DATABASE_URL)}")
        print("[*] Synchronizing database tables...")
        ensure_database_schema()

        inspector = sqlalchemy.inspect(engine)
        tables = inspector.get_table_names()
        print(f"[SUCCESS] All database tables are synchronized ({len(tables)} tables verified):")
        for table in sorted(tables):
            print(f"  + {table}")
        print("\nDatabase is ready!\n")
    except Exception as e:
        print(f"\n[ERROR] Database migration failed: {e}\n")
        sys.exit(1)


def run_makemigrations():
    print("\n[INFO] Notice: Power Solution is built using FastAPI + SQLAlchemy (not Django).")
    print("[INFO] Schema migrations are declarative via models in 'api/models.py'.")
    print("[INFO] Dedicated migration files are not required. Synchronizing schema directly...")
    run_migrate()


def run_checkdb():
    print("\n==========================================")
    print("  Power Solution - Database Status Check  ")
    print("==========================================")
    try:
        import sqlalchemy
        from core.settings import DATABASE_URL, engine

        print(f"[*] Database URL: {mask_db_url(DATABASE_URL)}")
        inspector = sqlalchemy.inspect(engine)
        tables = inspector.get_table_names()
        print(f"[SUCCESS] Connection established! Found {len(tables)} tables:")
        for table in sorted(tables):
            print(f"  + {table}")
        print()
    except Exception as e:
        print(f"\n[ERROR] Database connection failed: {e}\n")
        sys.exit(1)


def run_createsuperuser():
    import getpass
    print("\n==========================================")
    print("  Power Solution - Create Admin User      ")
    print("==========================================")
    try:
        from core.settings import SessionLocal, ensure_database_schema
        from core.auth import hash_password
        from api.models import User

        ensure_database_schema()
        db = SessionLocal()

        full_name = input("Full Name [Admin]: ").strip() or "Admin"
        email = input("Email address: ").strip().lower()
        if not email:
            print("[ERROR] Email cannot be empty.")
            return

        existing = db.query(User).filter(User.email == email).first()
        if existing:
            print(f"[ERROR] User with email '{email}' already exists.")
            return

        phone_number = input("Phone Number [0000000000]: ").strip() or "0000000000"
        password = getpass.getpass("Password: ")
        if not password:
            print("[ERROR] Password cannot be empty.")
            return
        confirm = getpass.getpass("Confirm Password: ")
        if password != confirm:
            print("[ERROR] Passwords do not match.")
            return

        new_user = User(
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            password_hash=hash_password(password),
            role="admin",
            is_active=True,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(f"\n[SUCCESS] Superuser '{email}' (role: admin, id: {new_user.id}) created successfully!\n")
    except Exception as e:
        print(f"\n[ERROR] Failed to create user: {e}\n")
    finally:
        try:
            db.close()
        except Exception:
            pass


def run_server(args):
    # Auto-detect venv if running in an environment without uvicorn
    try:
        import uvicorn
    except ImportError:
        for venv_name in ["venv", "env"]:
            for sub in [os.path.join("Scripts", "python.exe"), os.path.join("bin", "python")]:
                candidate = os.path.join(BASE_DIR, venv_name, sub)
                if os.path.exists(candidate) and sys.executable.lower() != os.path.abspath(candidate).lower():
                    import subprocess
                    result = subprocess.run([candidate] + sys.argv)
                    sys.exit(result.returncode)

        print("\n[ERROR] 'uvicorn' is not installed in your active Python environment.")
        print("Please activate your virtual environment or install dependencies:")
        print("    pip install -r requirements.txt\n")
        sys.exit(1)

    host = "127.0.0.1"
    port = 8000

    if len(args) > 1:
        arg = args[1]
        if ":" in arg:
            host, port_str = arg.split(":", 1)
            port = int(port_str)
        else:
            try:
                port = int(arg)
            except ValueError:
                print(f"Invalid port: {arg}")
                return

    print(f"\nPower Solution API running at: http://{host}:{port}")
    print(f"Interactive API Docs available at: http://{host}:{port}/docs\n")
    uvicorn.run("main:app", host=host, port=port, reload=True)


def print_help():
    print("""
Power Solution CLI Management Tool

Available commands:
  migrate             Synchronize/create all database tables via SQLAlchemy
  makemigrations      Inspect models and apply schema updates
  checkdb             Verify database connectivity and list existing tables
  createsuperuser     Create an administrative user in the database
  runserver [port]    Run the development server (default: 8000, e.g. 8000 or 0.0.0.0:8000)

Note for cPanel:
  In cPanel, FastAPI runs automatically via Phusion Passenger (passenger_wsgi.py).
  Database tables are automatically created whenever the app starts up!
""")


def main():
    args = sys.argv[1:]
    command = args[0].lower() if args else "help"

    if command == "runserver":
        run_server(args)
    elif command in ("migrate", "initdb"):
        run_migrate()
    elif command == "makemigrations":
        run_makemigrations()
    elif command in ("checkdb", "status", "tables"):
        run_checkdb()
    elif command in ("createsuperuser", "createadmin"):
        run_createsuperuser()
    elif command in ("help", "--help", "-h"):
        print_help()
    else:
        print(f"\nUnknown command: '{command}'")
        print_help()


if __name__ == "__main__":
    main()

