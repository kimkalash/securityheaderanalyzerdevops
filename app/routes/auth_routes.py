from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.db import get_db
from app import services
from app.auth import hash_password, verify_password, create_access_token, get_current_user
from app.schemas import UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ✅ 1. REGISTER ROUTE
@router.post("/register", response_model=UserResponse)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    """
    Creates a new user:
    1. Hashes password
    2. Calls create_user service
    """
    # Check if email already exists
    existing_user = db.query(services.User).filter(services.User.email == payload.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(payload.password)
    new_user = services.create_user(db, payload.username, payload.email, hashed_pw)
    return new_user


# ✅ 2. LOGIN ROUTE
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticates user:
    1. Verifies email/username
    2. Verifies password
    3. Returns JWT token
    """
    # OAuth2PasswordRequestForm sends 'username' field (can be email)
    user = db.query(services.User).filter(services.User.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Create token with user ID in the 'sub' field
    token = create_access_token(data={"sub": str(user.id)})

    return {"access_token": token, "token_type": "bearer"}


# ✅ 3. GET CURRENT USER
@router.get("/me", response_model=UserResponse)
def get_me(current_user=Depends(get_current_user)):
    """
    Protected route:
    1. Verifies token
    2. Returns user info
    """
    return current_user
