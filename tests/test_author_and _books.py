import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app  # Assuming your FastAPI instance is in app.main
from app.database import Base, get_db

# Setting up a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///tests/library_test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# Override the get_db dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)  # Create the tables
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)  # Drop the tables


@pytest.fixture(scope="module")
def db_session():
    db = TestingSessionLocal()
    yield db
    db.close()


def test_create_author(client):
    response = client.post(
        "/authors",
        json=[
            {
                "name": "John Doe",
                "bio": "Author bio",
                "birth_date": "1980-01-31",
            },
        ],
    )
    assert response.status_code == 201
    assert response.json()[0]["name"] == "John Doe"


def test_get_all_authors(client, db_session):
    response = client.get("/authors")
    assert response.status_code == 200
    assert response.json() == {
        "data": [
            {
                "name": "John Doe",
                "bio": "Author bio",
                "birth_date": "01/31/1980",
                "id": 1,
            }
        ]
    }


def test_create_books(client):
    response = client.post(
        "/books",
        json=[
            {
                "title": "Title 1",
                "description": "Description 1",
                "publish_date": "1983-11-14",
                "author_id": 1,
            },
        ],
    )
    assert response.status_code == 201
    assert response.json()[0]["title"] == "Title 1"


def test_get_an_author(client):
    response = client.get("/authors/1")
    assert response.status_code == 200
    assert response.json()["data"]["name"] == "John Doe"


def test_get_a_books(client):
    response = client.get("/books/1")
    assert response.status_code == 200
    assert response.json()["data"]["title"] == "Title 1"


def test_update_author(client):
    response = client.patch("/authors/1", json={"name": "Jane Doe"})
    assert response.status_code == 200
    assert response.json()["name"] == "Jane Doe"


def test_update_books(client):
    response = client.patch("/books/1", json={"title": "New title for book1"})
    assert response.status_code == 200
    assert response.json()["title"] == "New title for book1"


def test_get_associations(client):
    response = client.get(
        "/authors/1/books",
    )
    assert response.status_code == 200
    assert response.json()[0]["title"] == "New title for book1"


def test_delete_author_and_check_cascade(client):
    response_author = client.delete("/authors/1")
    response_books = client.get("/books/1")

    assert response_author.status_code == 204
    assert response_books.status_code == 404


def test_get_an_author_not_found(client):
    response = client.get("/authors/999")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "author_data with id = 999 was not found",
    }
