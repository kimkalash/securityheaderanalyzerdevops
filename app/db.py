from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

engine = create_engine('sqlite:///../database.db', connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Provide a database session for FastAPI routes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
