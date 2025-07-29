from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.db import get_db
from app import services
from app.auth import hash_password, verify_password, create_access_token, get_current_user
from app.schemas import UserCreate, UserResponse, APIResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

# ✅ Register Route
@router.post("/register", response_model=APIResponse)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    """Register a new user with hashed password."""
    existing_user = db.query(services.User).filter(services.User.email == payload.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(payload.password)
    new_user = services.create_user(db, payload.username, payload.email, hashed_pw)
    return APIResponse(success=True, data=new_user)

# ✅ Login Route
@router.post("/login", response_model=APIResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Authenticate user and return JWT token."""
    user = db.query(services.User).filter(services.User.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(data={"sub": str(user.id)})
    return APIResponse(success=True, data={"access_token": token, "token_type": "bearer"})

# ✅ Get Current User
@router.get("/me", response_model=APIResponse)
def get_me(current_user=Depends(get_current_user)):
    """Return the current logged-in user's info."""
    return APIResponse(success=True, data=current_user)
