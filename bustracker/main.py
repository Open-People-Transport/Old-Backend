from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqladmin import Admin
from strawberry.fastapi import GraphQLRouter
from uuid_extensions import uuid7

import bustracker
from bustracker.admin_models import NodeAdmin  # type: ignore
from bustracker.admin_models import RouteAdmin  # type: ignore
from bustracker.admin_models import StopAdmin  # type: ignore
from bustracker.admin_models import TypeAdmin  # type: ignore
from bustracker.api.exceptions import ResourceException
from bustracker.database import engine

from .graphql.context import get_context
from .graphql.schema import schema
from .routers import nodes, routes, stops, types

graphql_app = GraphQLRouter(schema, context_getter=get_context)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

admin = Admin(app, engine)
admin.register_model(TypeAdmin)
admin.register_model(RouteAdmin)
admin.register_model(NodeAdmin)
admin.register_model(StopAdmin)


GET_RESPONSES: dict[int | str, dict[str, Any]] = {
    404: {"description": "Resource not found"},
}

POST_RESPONSES: dict[int | str, dict[str, Any]] = {}


PUT_RESPONSES: dict[int | str, dict[str, Any]] = {
    404: {"description": "Resource not found"},
}


# TODO Sort out exceptions
@app.exception_handler(ResourceException)
async def resource_exception_handler(request: Request, exc: ResourceException):
    return JSONResponse(
        status_code=404,
        content={
            "error": exc.__class__.__name__,
            "type": str(exc.type.__name__),
            "identifier": str(exc.identifier),
            "detail": str(exc.detail),
        },
    )


app.include_router(types.router)
app.include_router(routes.router)
app.include_router(nodes.router)
app.include_router(stops.router)


@app.get("/uuid")
def get_random_uuid():
    return uuid7()
