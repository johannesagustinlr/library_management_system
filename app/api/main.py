from fastapi import APIRouter

from app.api.router import authors, books

api_router = APIRouter()
api_router.include_router(authors.router)
api_router.include_router(books.router)
