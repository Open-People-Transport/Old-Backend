import strawberry
from fastapi import Depends, FastAPI
from sqladmin import Admin
from sqlmodel import Session
from strawberry.fastapi import BaseContext, GraphQLRouter

from .admin_models import NodeAdmin, RouteAdmin, StopAdmin, TypeAdmin  # type: ignore
from .database import engine, get_session
from .schemas import Query


class Context(BaseContext):
    def __init__(self, session: Session):
        self.session = session


async def get_context(session=Depends(get_session)):
    return Context(session)


schema = strawberry.Schema(Query)
graphql_app = GraphQLRouter(schema, context_getter=get_context)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
admin = Admin(app, engine)


admin.register_model(TypeAdmin)
admin.register_model(RouteAdmin)
admin.register_model(NodeAdmin)
admin.register_model(StopAdmin)
