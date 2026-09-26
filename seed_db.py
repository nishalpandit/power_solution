import sys
import os

# Add current dir to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.models import Complaint
from core.settings import ensure_database_schema, get_db
from sqlalchemy.orm import Session
from datetime import datetime, timezone

def seed():
    ensure_database_schema()
    db = next(get_db())
    # Check if we have complaints
    existing = db.query(Complaint).count()
    if existing == 0:
        c1 = Complaint(
            product_category="Lift",
            description="Lift is making weird noise on 3rd floor.",
            complaint_date="18 May 2025",
            photo="/uploads/complaints/complaint_1234567890abcdef.jpg",
            status="Pending",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        db.add(c1)
        db.commit()
        print("Mock complaint inserted!")
    else:
        print("Complaints already exist.")

if __name__ == "__main__":
    seed()
