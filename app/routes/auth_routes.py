from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.db import get_db
from app import services
from app.auth import hash_password, verify_password, create_access_token, get_current_user
from app.schemas import UserCreate, APIResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=APIResponse, summary="Register a new user")
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(services.User).filter(services.User.email == payload.email).first()
    if existing_user:
        return APIResponse(success=False, error={"message": "Email already registered"})

    hashed_pw = hash_password(payload.password)
    new_user = services.create_user(db, payload.username, payload.email, hashed_pw)
    return APIResponse(success=True, data={"id": new_user.id, "username": new_user.username, "email": new_user.email})

@router.post("/login", response_model=APIResponse, summary="Authenticate and get JWT token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(services.User).filter(services.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        return APIResponse(success=False, error={"message": "Invalid credentials"})

    token = create_access_token(data={"sub": str(user.id)})
    return APIResponse(success=True, data={"access_token": token, "token_type": "bearer"})

@router.get("/me", response_model=APIResponse, summary="Get current logged-in user")
def get_me(current_user=Depends(get_current_user)):
    return APIResponse(success=True, data={"id": current_user.id, "username": current_user.username, "email": current_user.email})
