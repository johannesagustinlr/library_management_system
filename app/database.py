from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .model import Base
import os


engine = create_engine(
    os.getenv("DATABASE_URL"),
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
