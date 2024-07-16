from fastapi import APIRouter

router = APIRouter()


FAKE_ITEMS_DB = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"},
]


@router.get("/authors", tags=["authors"])
def get_authors():
    return FAKE_ITEMS_DB
