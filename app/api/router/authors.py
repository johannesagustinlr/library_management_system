from fastapi import APIRouter, status, Depends, HTTPException, Response
from app.schema import CreateAuthor, UpdateAuthor
from sqlalchemy.orm import Session
from app.database import get_db
from app.model import Authors

router = APIRouter()


@router.get("/authors", tags=["Authors"])
def get_all_author(db: Session = Depends(get_db)):
    authors_data = db.query(Authors).all()
    return {"data": authors_data}


@router.get("/authors/{id}", tags=["Authors"])
def get_an_author(id: int, db: Session = Depends(get_db)):
    author_data = db.query(Authors).filter(Authors.id == id).first()
    if not author_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"author_data with id = {id} was not found",
        )
    return {"data": author_data}


@router.post("/authors", status_code=status.HTTP_201_CREATED, tags=["Authors"])
def create_new_author(author: CreateAuthor, db: Session = Depends(get_db)):

    db_author_data = Authors(
        name=author.name,
        bio=author.bio,
        birth_date=author.birth_date.strftime("%m/%d/%Y"),
    )

    db.add(db_author_data)
    db.commit()
    db.refresh(db_author_data)
    return db_author_data


@router.patch("/authors/{id}", tags=["Authors"])
def update_author(
    id: int,
    updated_author: UpdateAuthor,
    db: Session = Depends(get_db),
):
    author_data = db.query(Authors).filter(Authors.id == id).first()

    if not author_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with id: {id} does not exist",
        )

    update_author_data = updated_author.model_dump(exclude_unset=True)
    for key, value in update_author_data.items():
        if value:
            setattr(author_data, key, value)
    db.add(author_data)
    db.commit()
    db.refresh(author_data)

    return author_data


@router.delete("/authors/{id}", tags=["Authors"])
def delete_an_author(id: int, db: Session = Depends(get_db)):
    author_data = db.query(Authors).filter(Authors.id == id).first()
    if not author_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"author with id = {id} was not found",
        )
    db.delete(author_data)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
