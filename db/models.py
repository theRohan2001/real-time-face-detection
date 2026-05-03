from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime, timezone
from .database import Base

class FaceROI(Base):
    __tablename__ = "face_roi"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    x_min = Column(Float, nullable=False)
    y_min = Column(Float, nullable=False)
    width = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
