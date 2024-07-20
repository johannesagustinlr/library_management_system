from fastapi import APIRouter

from app.api.router import authors, books, associations

api_router = APIRouter()
api_router.include_router(authors.router)
api_router.include_router(books.router)
api_router.include_router(associations.router)
