from app.db.session import Base,engine
from app.db.models.user import User
from app.db.models.progress import Progress

def init_db():
    """
    Initialize the database by creating all tables.
    Should be called on application startup.
    """
    Base.metadata.create_all(bind=engine)
