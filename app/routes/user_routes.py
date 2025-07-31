from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.services import create_user, get_user_by_id
from app.schemas import UserCreate, APIResponse
from app.auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=APIResponse, summary="Register a new user")
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    user = create_user(db, payload.username, payload.email, payload.password)
    return APIResponse(success=True, data={"id": user.id, "username": user.username, "email": user.email})

@router.get("/me", response_model=APIResponse, summary="Get current logged-in user")
def read_own_user(current_user=Depends(get_current_user)):
    """Fetch info of the logged-in user only."""
    return APIResponse(success=True, data={"id": current_user.id, "username": current_user.username, "email": current_user.email})

@router.get("/{user_id}", response_model=APIResponse, summary="Fetch a user by ID")
def read_user(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Fetch a user by ID (requires authentication)."""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return APIResponse(success=True, data={"id": user.id, "username": user.username, "email": user.email})

