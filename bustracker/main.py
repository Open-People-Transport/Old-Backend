from fastapi import FastAPI
from sqladmin import Admin
from strawberry.fastapi import GraphQLRouter

from .admin_models import NodeAdmin, RouteAdmin, StopAdmin, TypeAdmin  # type: ignore
from .database import engine
from .graphql.context import get_context
from .graphql.schema import schema

graphql_app = GraphQLRouter(schema, context_getter=get_context)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

admin = Admin(app, engine)
admin.register_model(TypeAdmin)
admin.register_model(RouteAdmin)
admin.register_model(NodeAdmin)
admin.register_model(StopAdmin)
