from fastapi import FastAPI

from .database import create_db_tables

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_tables()
