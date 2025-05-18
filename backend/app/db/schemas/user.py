# backend/app/db/schemas/user.py

from pydantic import BaseModel, EmailStr
from typing import List

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    interests: List[str]

    class Config:
        orm_mode = True
