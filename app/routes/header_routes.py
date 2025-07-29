from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.services import create_header_result, Scan
from app.models import HeaderResult
from pydantic import BaseModel
from app.auth import get_current_user

class HeaderCreate(BaseModel):
    scan_id: int
    header_name: str
    header_value: str

router = APIRouter(prefix="/headers", tags=["Headers"])

@router.post("/", response_model=dict)
def add_header(
    payload: HeaderCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Add a header result only to scans owned by the logged-in user."""
    scan = db.query(Scan).filter(
        Scan.id == payload.scan_id,
        Scan.user_id == current_user.id
    ).first()

    if not scan:
        raise HTTPException(status_code=403, detail="Not allowed to add headers to this scan")

    header = create_header_result(db, payload.scan_id, payload.header_name, payload.header_value)
    return {
        "id": header.id,
        "header_name": header.header_name,
        "header_value": header.header_value,
    }
