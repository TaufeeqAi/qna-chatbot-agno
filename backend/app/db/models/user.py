from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.sql import func
from ..session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    interests = Column(JSON, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

#User.progress_entries = relationship("Progress", back_populates="user")