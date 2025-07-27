from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.services import create_user, get_user_by_id
from pydantic import BaseModel, EmailStr


# Request schema
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password_hash: str


# Response schema
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


router = APIRouter()


@router.post("/", response_model=UserResponse)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    user = create_user(db, payload.username, payload.email, payload.password_hash)
    return user


@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
