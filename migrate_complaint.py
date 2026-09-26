import sqlite3

def migrate():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE complaints ADD COLUMN customer_name VARCHAR(150)")
        cursor.execute("ALTER TABLE complaints ADD COLUMN phone VARCHAR(20)")
        cursor.execute("ALTER TABLE complaints ADD COLUMN email VARCHAR(120)")
        conn.commit()
        print("Migration successful: added customer_name, phone, email to complaints table.")
    except Exception as e:
        conn.rollback()
        print(f"Migration failed (maybe already migrated?): {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
