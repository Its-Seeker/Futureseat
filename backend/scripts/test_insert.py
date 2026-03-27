import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.session import SessionLocal
from app.models.college import College

db = SessionLocal()

college = College(
    name="Test College",
    state="Test State",
    type="Govt",
    exam_type="NEET",
    course="MBBS",
    fees_lpa=1.0,
    seats=100,
    naac_grade="A"
)

db.add(college)
db.commit()

print("Inserted test row!")