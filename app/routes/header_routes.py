from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.services import create_header_result
from app.models import HeaderResult
from pydantic import BaseModel


# Request schema
class HeaderCreate(BaseModel):
    scan_id: int
    header_name: str
    header_value: str


# Response schema
class HeaderResponse(BaseModel):
    id: int
    header_name: str
    header_value: str

    class Config:
        from_attributes = True  # For Pydantic v2


router = APIRouter()


@router.post("/", response_model=HeaderResponse)
def add_header(payload: HeaderCreate, db: Session = Depends(get_db)):
    header: HeaderResult = create_header_result(
        db, payload.scan_id, payload.header_name, payload.header_value
    )
    return header

