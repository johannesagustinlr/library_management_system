from fastapi import APIRouter

router = APIRouter()


FAKE_ITEMS_DB = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"},
]


@router.get("/books", tags=["authors"])
def get_books():
    return FAKE_ITEMS_DB
