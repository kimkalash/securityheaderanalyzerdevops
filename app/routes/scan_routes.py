from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.services import create_scan, get_user_scans
from app.auth import get_current_user
from app.schemas import APIResponse
from pydantic import BaseModel

class ScanCreate(BaseModel):
    scan_url: str

router = APIRouter(prefix="/scans", tags=["Scans"])

@router.post("/", response_model=APIResponse, summary="Create a new scan")
def new_scan(payload: ScanCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    scan = create_scan(db, user_id=current_user.id, scan_url=payload.scan_url)
    return APIResponse(success=True, data={"id": scan.id, "scan_url": scan.scan_url})

@router.get("/", response_model=APIResponse, summary="List all scans of current user")
def list_my_scans(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    scans = get_user_scans(db, current_user.id)
    return APIResponse(
        success=True,
        data=[{"id": s.id, "scan_url": s.scan_url, "scan_date": str(s.scan_date)} for s in scans]
    )


