import argparse
import csv
import sys
from app.db.session import SessionLocal
from app.models.college import College
from app.models.cutoff import Cutoff

parser = argparse.ArgumentParser()
parser.add_argument("--csv", required=True)
parser.add_argument("--exam-type", required=True)
args = parser.parse_args()
exam_type = args.exam_type.upper()

db = SessionLocal()
loaded_colleges = 0
loaded_cutoffs  = 0

try:
    existing = db.query(College).filter(College.exam_type == exam_type).all()
    for col in existing:
        db.query(Cutoff).filter(Cutoff.college_id == col.id).delete()
    db.query(College).filter(College.exam_type == exam_type).delete()
    db.commit()
    print(f"Cleared old {exam_type} data")

    with open(args.csv, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        
        for i, row in enumerate(reader):
            try:
                lower_row = {k.lower().strip() if k else '': v for k, v in row.items()}
                
                name = (lower_row.get("college") or lower_row.get("institute") or "").strip()
                if not name:
                    continue

                course = (lower_row.get("branch") or lower_row.get("course") or "").strip()
                category = (lower_row.get("category") or "GEN").upper().strip()
                gender = (lower_row.get("gender") or "ANY").upper().strip()
                
                # ---------------------------------------------------------
                # CRITICAL FIX: Force women's colleges to be "FEMALE"
                # This overrides the incorrect "Male" data in the CSV
                # ---------------------------------------------------------
                if "IGDTUW" in name.upper() or "WOMEN" in name.upper():
                    gender = "FEMALE"
                
                special = (lower_row.get("special") or "").strip()
                if special.lower() in ["nan", "none", ""]:
                    special = None

                opening_raw = (lower_row.get("opening rank") or lower_row.get("opening_rank") or "").strip()
                closing_raw = (lower_row.get("closing rank") or lower_row.get("closing_rank") or "").strip()
                
                opening = int(float(opening_raw.replace(",", ""))) if opening_raw and opening_raw.lower() != "nan" else None
                closing = int(float(closing_raw.replace(",", ""))) if closing_raw and closing_raw.lower() != "nan" else None

                if not closing:
                    continue 

                college = College(
                    name=name, 
                    state=lower_row.get("state"), 
                    type=lower_row.get("type"),
                    exam_type=exam_type, 
                    course=course,
                )
                db.add(college)
                db.flush()
                loaded_colleges += 1

                cutoff = Cutoff(
                    college_id=college.id, 
                    quota=lower_row.get("quota"),
                    category=category, 
                    gender=gender,
                    special=special, 
                    opening_rank=opening, 
                    closing_rank=closing,
                )
                db.add(cutoff)
                db.flush()
                loaded_cutoffs += 1

            except Exception as row_err:
                print(f"  Row {i+1} skipped due to error: {row_err}")
                continue

    db.commit()
    print(f"\nSUCCESS! Loaded {loaded_colleges} Colleges and {loaded_cutoffs} Cutoffs.")

except Exception as e:
    db.rollback()
    print(f"Fatal error: {e}")
finally:
    db.close()