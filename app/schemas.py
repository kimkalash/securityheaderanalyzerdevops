from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Any, Optional



class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class ScanCreate(BaseModel):
    user_id: int
    scan_url: str

    model_config = ConfigDict(from_attributes=True)


class HeaderResultCreate(BaseModel):
    scan_id: int
    header_name: str
    header_value: str

    model_config = ConfigDict(from_attributes=True)

class APIResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[dict] = None
