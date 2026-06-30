from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./flowerbed.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Database session dependency injector for FastAPI route handlers.
    Ensures safe transaction isolation and resource cleanup.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
