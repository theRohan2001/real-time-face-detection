from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ROIBase(BaseModel):
    x_min: float
    y_min: float
    width: float
    height: float

class ROICreate(ROIBase):
    pass

class ROI(ROIBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
