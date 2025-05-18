from sqlalchemy.orm import Session
from app.db.crud import user as crud_user, progress as crud_progress
from app.db.session import SessionLocal

class ProfileAgent:
    """
    Updates user profile metadata:
      - Research interests
      - Progress tracking
    """

    @staticmethod
    def update_interests(user_id: int, interests: list):
        db: Session = SessionLocal()
        user = crud_user.get_user_by_id(db, user_id)
        user.interests = interests
        db.commit()
        db.close()

    @staticmethod
    def log_progress(user_id: int, topic: str, status: str):
        db: Session = SessionLocal()
        crud_progress.create_progress(db, user_id, topic, status)
        db.close()

    @staticmethod
    def get_progress(user_id: int):
        db: Session = SessionLocal()
        records = crud_progress.get_progress_for_user(db, user_id)
        db.close()
        return records
