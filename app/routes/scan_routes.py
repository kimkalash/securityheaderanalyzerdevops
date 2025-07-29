from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.services import create_scan, get_user_scans
from app.models import Scan
from pydantic import BaseModel
from app.auth import get_current_user

class ScanCreate(BaseModel):
    scan_url: str  # ✅ Removed user_id (use current_user.id instead)

router = APIRouter(prefix="/scans", tags=["Scans"])

@router.post("/", response_model=dict)
def new_scan(
    payload: ScanCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Create a scan for the logged-in user only."""
    scan = create_scan(db, user_id=current_user.id, scan_url=payload.scan_url)
    return {"id": scan.id, "scan_url": scan.scan_url}

@router.get("/", response_model=list[dict])
def list_my_scans(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """List scans that belong to the logged-in user."""
    scans = get_user_scans(db, current_user.id)
    return [{"id": s.id, "scan_url": s.scan_url} for s in scans]
