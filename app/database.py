from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .model import Base

SQLITE_DATABASE_URL = "sqlite:///./library.db"

engine = create_engine(
    SQLITE_DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Ensure models are imported

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
