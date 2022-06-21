from fastapi import FastAPI
from sqladmin import Admin

from .admin_models import NodeAdmin, RouteAdmin, StopAdmin, TypeAdmin  # type: ignore
from .database import engine

app = FastAPI()
admin = Admin(app, engine)


admin.register_model(TypeAdmin)
admin.register_model(RouteAdmin)
admin.register_model(NodeAdmin)
admin.register_model(StopAdmin)
