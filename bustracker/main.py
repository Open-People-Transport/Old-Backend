from fastapi import FastAPI
from sqladmin import Admin  # type: ignore

from .database import engine

app = FastAPI()
admin = Admin(app, engine)
