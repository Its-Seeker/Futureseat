from pydantic import BaseModel
from typing import Optional


class CollegeBase(BaseModel):
    name:        str
    state:       Optional[str] = None
    type:        Optional[str] = None
    exam_type:   str
    course:      Optional[str] = None
    fees_lpa:    Optional[float] = None
    seats:       Optional[int] = None
    naac_grade:  Optional[str] = None

class CollegeCreate(CollegeBase):
    pass

class CollegeResponse(CollegeBase):
    id: int
    class Config:
        from_attributes = True



class CutoffResponse(BaseModel):
    id:           int
    college_id:   int
    quota:        Optional[str] = None
    category:     Optional[str] = None
    gender:       Optional[str] = None
    opening_rank: Optional[int] = None
    closing_rank: Optional[int] = None
    class Config:
        from_attributes = True


class PredictResult(BaseModel):
    college:      str
    state:        Optional[str] = None
    type:         Optional[str] = None
    course:       Optional[str] = None
    naac_grade:   Optional[str] = None
    fees_lpa:     Optional[float] = None
    seats:        Optional[int] = None
    quota:        Optional[str] = None
    category:     Optional[str] = None
    gender:       Optional[str] = None
    opening_rank: Optional[int] = None
    closing_rank: Optional[int] = None
    chance:       str                     # 'Safe' | 'Moderate' | 'Risky' :)

class PredictResponse(BaseModel):
    count: int
    safe:         list[PredictResult]
    moderate:     list[PredictResult]
    risky:        list[PredictResult]