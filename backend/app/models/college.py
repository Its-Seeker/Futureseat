from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.db.base_class import Base  # single Base

class College(Base):
    __tablename__ = "colleges"
    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String, nullable=False)
    state       = Column(String)
    type        = Column(String)
    exam_type   = Column(String, nullable=False)
    course      = Column(String)
    fees_lpa    = Column(Float)
    seats       = Column(Integer)
    naac_grade  = Column(String)
    cutoffs     = relationship("Cutoff", back_populates="college", cascade="all, delete")