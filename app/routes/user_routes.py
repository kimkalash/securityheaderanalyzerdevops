from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.services import create_user, get_user_by_id
from app.schemas import UserCreate, UserResponse
from app.auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    hashed_password = payload.password  # Password will be hashed in auth routes
    user = create_user(db, payload.username, payload.email, hashed_password)
    return user

@router.get("/me", response_model=UserResponse)
def read_own_user(current_user=Depends(get_current_user)):
    """Fetch info of the logged-in user only."""
    return current_user

@router.get("/{user_id}", response_model=UserResponse)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Fetch a user by ID (accessible only to logged-in users)."""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

