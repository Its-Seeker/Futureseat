from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional

from app.db.session import get_db
from app.models.college import College
from app.models.cutoff import Cutoff
from app.schemas.college import (
    CollegeCreate,
    CollegeResponse,
    PredictResult,
    PredictResponse,
)

router = APIRouter()


def to_predict_result(college: College, cutoff: Cutoff, rank: int) -> PredictResult:
    if cutoff.closing_rank and rank <= (cutoff.opening_rank or 0):
        chance = "Safe"
    elif cutoff.closing_rank and rank <= cutoff.closing_rank:
        chance = "Moderate"
    else:
        chance = "Risky"

    course_display = college.course
    if cutoff.special and str(cutoff.special).strip().lower() not in ["", "nan", "none", "null"]:
        course_display = f"{college.course} ({cutoff.special})"

    return PredictResult(
        college      = college.name,
        state        = college.state,
        type         = college.type,
        course       = course_display,
        naac_grade   = college.naac_grade,
        fees_lpa     = college.fees_lpa,
        seats        = college.seats,
        quota        = cutoff.quota,
        category     = cutoff.category,
        gender       = cutoff.gender,
        opening_rank = cutoff.opening_rank,
        closing_rank = cutoff.closing_rank,
        chance       = chance,
    )

@router.get("/colleges", response_model=list[CollegeResponse])
def get_colleges(
    exam_type: Optional[str] = None, state: Optional[str] = None, 
    course: Optional[str] = None, limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    query = db.query(College)
    if exam_type: query = query.filter(College.exam_type == exam_type.upper())
    if state: query = query.filter(College.state == state)
    if course: query = query.filter(College.course == course)
    return query.order_by(College.name.asc()).limit(limit).all()

@router.post("/colleges", response_model=CollegeResponse)
def create_college(payload: CollegeCreate, db: Session = Depends(get_db)):
    college = College(**payload.model_dump())
    db.add(college)
    db.commit()
    db.refresh(college)
    return college


@router.get("/predict/neet", response_model=PredictResponse)
def predict_neet(
    rank: int = Query(...), quota: Optional[str] = Query(None),
    state: Optional[str] = Query(None), col_type: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(College, Cutoff).join(Cutoff, Cutoff.college_id == College.id)\
              .filter(College.exam_type == "NEET").filter(Cutoff.closing_rank >= rank)
    if quota: query = query.filter(Cutoff.quota == quota)
    if state: query = query.filter(College.state == state)
    if col_type: query = query.filter(College.type == col_type)

    rows = query.order_by(Cutoff.closing_rank.asc()).all()
    results = [to_predict_result(c, co, rank) for c, co in rows]
    
    return PredictResponse(
        count=len(results),
        safe=[r for r in results if r.chance == "Safe"],
        moderate=[r for r in results if r.chance == "Moderate"],
        risky=[r for r in results if r.chance == "Risky"],
    )


@router.get("/predict/btech", response_model=PredictResponse)
def predict_btech(
    rank:     int            = Query(..., description="Your JEE rank"),
    category: str            = Query("GEN", description="GEN / OBC / SC / ST / EWS"),
    gender:   str            = Query("Male", description="Male or Female"),
    special:  Optional[str]  = Query(None, description="PwD, Sports, or CW"),
    branch:   Optional[str]  = Query(None, description="CSE, ECE, Mechanical etc."),
    db:       Session        = Depends(get_db),
):
    query = (
        db.query(College, Cutoff)
        .join(Cutoff, Cutoff.college_id == College.id)
        .filter(College.exam_type == "BTECH")
        .filter(Cutoff.closing_rank >= rank)
        .filter(Cutoff.category == category.upper())
    )
    
    allowed_genders = [gender.upper(), "ANY", "GENDER-NEUTRAL", "NEUTRAL", ""]
    query = query.filter(Cutoff.gender.in_(allowed_genders))
    
    if special and special.upper() != "NONE":
        query = query.filter(
            or_(
                Cutoff.special.ilike(f"%{special}%"),
                Cutoff.special.is_(None),            
                Cutoff.special == "",
                Cutoff.special.ilike("nan"),
                Cutoff.special.ilike("none")
            )
        )
    else:
        query = query.filter(
            or_(
                Cutoff.special.is_(None),
                Cutoff.special == "",
                Cutoff.special.ilike("nan"),
                Cutoff.special.ilike("none")
            )
        )

    if branch:
        query = query.filter(College.course.ilike(f"%{branch}%"))

    rows = query.order_by(Cutoff.closing_rank.asc()).all()
    results = [to_predict_result(c, co, rank) for c, co in rows]

    return PredictResponse(
        count    = len(results),
        safe     = [r for r in results if r.chance == "Safe"],
        moderate = [r for r in results if r.chance == "Moderate"],
        risky    = [r for r in results if r.chance == "Risky"],
    )