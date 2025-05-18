from sqlalchemy.orm import Session
from ..models.progress import Progress
from ..schemas.progress import ProgressCreate


def create_progress(db: Session, user_id: int, progress_in: ProgressCreate) -> Progress:
    db_prog = Progress(
        user_id=user_id,
        topic=progress_in.topic,
        status=progress_in.status,
    )
    db.add(db_prog)
    db.commit()
    db.refresh(db_prog)
    return db_prog


def get_progress_by_user(db: Session, user_id: int) -> list[Progress]:
    return db.query(Progress).filter(Progress.user_id == user_id).all()
