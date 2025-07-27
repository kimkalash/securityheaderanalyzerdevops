from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.services import create_user, get_user_by_id
from app.schemas import UserCreate, UserResponse  # ✅ Import models from schemas.py

router = APIRouter()

@router.post("/", response_model=UserResponse)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    user = create_user(db, payload.username, payload.email, payload.password)
    return user

@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """Fetch a user by ID"""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
