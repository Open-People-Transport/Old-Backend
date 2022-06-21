from fastapi import FastAPI
from sqladmin import Admin  # type: ignore

from .admin_models import TypeAdmin
from .database import engine

app = FastAPI()
admin = Admin(app, engine)


admin.register_model(TypeAdmin)
