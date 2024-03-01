from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.adapters.database.settings import settings

engine = create_engine(settings.SQLALCHEMY_DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
