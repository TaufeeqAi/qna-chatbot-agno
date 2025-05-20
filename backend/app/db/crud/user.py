from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import Optional
from ..models.user import User
from ..schemas.user import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def create_user(
    db: Session, 
    email: str, 
    password: Optional[str] = None, 
    interests: Optional[list] = None, 
    oauth_provider: Optional[str] = None, 
    oauth_account_id: Optional[str] = None
) -> User:
    hashed_password = pwd_context.hash(password) if password else None
    db_user = User(
        email=email,
        hashed_password=hashed_password,
        interests=interests if interests else [],
        oauth_provider=oauth_provider,
        oauth_account_id=oauth_account_id,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_oauth(
    db: Session, 
    user_id: int, 
    oauth_provider: str, 
    oauth_account_id: str
) -> Optional[User]:
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.oauth_provider = oauth_provider
        db_user.oauth_account_id = oauth_account_id
        db.commit()
        db.refresh(db_user)
    return db_user


def get_user_by_oauth(db: Session, oauth_provider: str, oauth_account_id: str) -> Optional[User]:
    return db.query(User).filter(
        User.oauth_provider == oauth_provider, 
        User.oauth_account_id == oauth_account_id
    ).first()


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email)
    if not user or not user.hashed_password:  # Ensure user exists and has a password (not an OAuth user)
        return None
    if not pwd_context.verify(password, user.hashed_password):
        return None
    return user
