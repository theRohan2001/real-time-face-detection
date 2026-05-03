from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import FaceROI
from schemas.roi import ROI
from typing import List

router = APIRouter()

@router.get("/roi", response_model=List[ROI])
def get_roi_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rois = db.query(FaceROI).order_by(FaceROI.timestamp.desc()).offset(skip).limit(limit).all()
    return rois
