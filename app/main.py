from fastapi import FastAPI
from app.api.main import api_router

DESCRIPTION = """
Library Management System

You will be able to:


"""


app = FastAPI(
    title="Library Management System API",
    description=DESCRIPTION,
)


@app.get("/")
def root():
    return {"message": "Hello World"}


app.include_router(api_router)
