# backend/app/db/schemas/user.py

from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UserBase(BaseModel):
    email: EmailStr
    interests: Optional[List[str]] = None

class UserCreate(UserBase):
    password: Optional[str] = None  # Password is now optional
    oauth_provider: Optional[str] = None
    oauth_account_id: Optional[str] = None

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserOut(UserBase):
    id: int
    oauth_provider: Optional[str] = None
    # oauth_account_id: Optional[str] = None # Usually not exposed

    class Config:
        orm_mode = True
