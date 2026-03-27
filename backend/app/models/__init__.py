# Force SQLAlchemy to register all models

from app.models.college import College
from app.models.cutoff import Cutoff

__all__ = ["College", "Cutoff"]