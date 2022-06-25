from typing import Any

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from uuid_extensions import uuid7

from .graphql.context import get_context
from .graphql.schema import schema
from .routers import nodes, routes, stops, types

graphql_app = GraphQLRouter(schema, context_getter=get_context)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

app.include_router(types.router)
app.include_router(routes.router)
app.include_router(nodes.router)
app.include_router(stops.router)


@app.get("/uuid")
def get_random_uuid():
    return uuid7()
