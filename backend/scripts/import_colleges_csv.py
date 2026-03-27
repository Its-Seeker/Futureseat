import argparse
import csv
import sys
from app.db.session import SessionLocal
from app.models.college import College
from app.models.cutoff import Cutoff

parser = argparse.ArgumentParser()
parser.add_argument("--csv",       required=True)
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

    with open(args.csv, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        print(f"Columns: {reader.fieldnames}")

        for i, row in enumerate(reader):
            try:
                if exam_type == "NEET":
                    name      = (row.get("College") or "").strip()
                    state     = (row.get("State")   or "").strip() or None
                    ctype     = (row.get("Type")     or "").strip() or None
                    course    = (row.get("Course")   or "MBBS").strip()
                    fees_raw  = (row.get("Fees (L/yr)") or "").strip()
                    seats_raw = (row.get("Seats")    or "").strip()
                    naac      = (row.get("NAAC")     or "").strip() or None
                    quota     = (row.get("Quota")    or "").strip() or None
                    category  = None
                    gender    = None
                    special   = None
                else:
                    name      = (row.get("college")  or "").strip()
                    state     = None
                    ctype     = None
                    course    = (row.get("branch")   or "").strip()
                    fees_raw  = ""
                    seats_raw = ""
                    naac      = None
                    quota     = None
                    category  = (row.get("category") or "GEN").upper().strip()
                    gender    = (row.get("gender")   or "ANY").upper().strip()
                    special   = (row.get("special")  or "").strip() or None

                if not name:
                    print(f"  Row {i+1}: skipped (empty name)")
                    continue

                fees  = float(fees_raw)  if fees_raw  else None
                seats = int(seats_raw)   if seats_raw else None

                college = College(
                    name=name, state=state, type=ctype,
                    exam_type=exam_type, course=course or None,
                    fees_lpa=fees, seats=seats, naac_grade=naac,
                )
                db.add(college)
                db.flush()
                db.refresh(college)

                if not college.id:
                    print(f"  Row {i+1}: ERROR - college.id is None")
                    continue

                loaded_colleges += 1

                opening_raw = (row.get("Opening Rank") or row.get("opening_rank") or "").strip()
                closing_raw = (row.get("Closing Rank") or row.get("closing_rank") or "").strip()
                opening = int(opening_raw.replace(",", "")) if opening_raw else None
                closing = int(closing_raw.replace(",", "")) if closing_raw else None

                cutoff = Cutoff(
                    college_id=college.id, quota=quota,
                    category=category, gender=gender,
                    opening_rank=opening, closing_rank=closing,
                )
                db.add(cutoff)
                db.flush()
                loaded_cutoffs += 1

            except Exception as row_err:
                print(f"  Row {i+1} error: {row_err}")
                continue

    db.commit()
    print(f"\nDone! Colleges: {loaded_colleges}, Cutoffs: {loaded_cutoffs}")

except FileNotFoundError:
    print(f"File not found: {args.csv}")
    sys.exit(1)
except Exception as e:
    db.rollback()
    print(f"Fatal error: {e}")
    import traceback; traceback.print_exc()
    sys.exit(1)
finally:
    db.close()
