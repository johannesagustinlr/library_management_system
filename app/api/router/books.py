from fastapi import APIRouter, status, Depends, HTTPException
from app.schema import UpdateBook, CreateBook
from sqlalchemy.orm import Session
from app.database import get_db
from app.model import Books
from typing import List

router = APIRouter()


@router.get("/books", tags=["Books"])
def get_all_books(db: Session = Depends(get_db)):
    authors_data = db.query(Books).all()
    return {"data": authors_data}


@router.get("/books/{id}", tags=["Books"])
def get_a_books(id: int, db: Session = Depends(get_db)):
    book_data = db.query(Books).filter(Books.id == id).first()
    if not book_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id = {id} was not found",
        )
    return {"data": book_data}


@router.post("/books", status_code=status.HTTP_201_CREATED, tags=["Books"])
def create_new_book(books: List[CreateBook], db: Session = Depends(get_db)):
    db_book_data_list = []
    for book in books:
        db_book_data = Books(
            title=book.title,
            description=book.description,
            publish_date=book.publish_date.strftime("%m/%d/%Y"),
            author_id=book.author_id,
        )

        db.add(db_book_data)
        db.commit()
        db.refresh(db_book_data)
        db_book_data_list.append(db_book_data)
    return db_book_data_list


@router.patch("/books/{id}", tags=["Books"])
def update_books(
    id: int,
    updated_book: UpdateBook,
    db: Session = Depends(get_db),
):
    book_data = db.query(Books).filter(Books.id == id).first()

    if not book_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id: {id} does not exist",
        )

    update_book_data = updated_book.model_dump(exclude_unset=True)
    for key, value in update_book_data.items():
        if value:
            setattr(book_data, key, value)
    db.add(book_data)
    db.commit()
    db.refresh(book_data)

    return book_data


@router.delete("/books/{id}", tags=["Books"])
def delete_a_book(id: int, db: Session = Depends(get_db)):
    book_data = db.query(Books).filter(Books.id == id).first()
    if not book_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id = {id} was not found",
        )
    db.delete(book_data)
    db.commit()
    return {"data": book_data}
