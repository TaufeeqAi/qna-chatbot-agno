# backend/app/db/schemas/progress.py

from pydantic import BaseModel
from datetime import datetime

class ProgressCreate(BaseModel):
    topic: str
    status: str

class ProgressOut(BaseModel):
    topic: str
    status: str
    updated_at: datetime

    class Config:
        orm_mode = True
