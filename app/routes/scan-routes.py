from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.services import create_scan, get_user_scans
from app.models import Scan
from pydantic import BaseModel


# Request schema
class ScanCreate(BaseModel):
    user_id: int
    scan_url: str


# Response schema
class ScanResponse(BaseModel):
    id: int
    scan_url: str

    class Config:
        from_attributes = True


router = APIRouter()


@router.post("/", response_model=ScanResponse)
def new_scan(payload: ScanCreate, db: Session = Depends(get_db)):
    scan: Scan = create_scan(db, payload.user_id, payload.scan_url)
    return scan


@router.get("/{user_id}", response_model=list[ScanResponse])
def list_scans(user_id: int, db: Session = Depends(get_db)):
    scans = get_user_scans(db, user_id)
    return scans

