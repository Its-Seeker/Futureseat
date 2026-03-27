from app.models.college import College
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Cutoff(Base):
    __tablename__ = "cutoffs"
    id           = Column(Integer, primary_key=True, index=True)
    college_id   = Column(Integer, ForeignKey("colleges.id", ondelete="CASCADE"))
    quota        = Column(String(50))
    category     = Column(String(50))
    gender       = Column(String(10))
    special      = Column(String(50))
    opening_rank = Column(Integer)
    closing_rank = Column(Integer)
    year         = Column(Integer)
    college      = relationship("College", back_populates="cutoffs")
