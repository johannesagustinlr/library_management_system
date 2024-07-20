from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.model import Books

router = APIRouter()


@router.get("/authors/{id}/books", tags=["Authors"])
def get_all_author(id: int, db: Session = Depends(get_db)):
    books_data = db.query(Books).filter(Books.author_id == id).all()
    return books_data
