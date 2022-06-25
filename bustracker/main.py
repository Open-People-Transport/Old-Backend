from typing import Any
from uuid import UUID

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from sqladmin import Admin
from sqlalchemy.orm import Session
from strawberry.fastapi import GraphQLRouter

from bustracker.admin_models import NodeAdmin  # type: ignore
from bustracker.admin_models import RouteAdmin  # type: ignore
from bustracker.admin_models import StopAdmin  # type: ignore
from bustracker.admin_models import TypeAdmin  # type: ignore
from bustracker.api.schemas import Node, Route, Stop, Type
from bustracker.api.services import (
    NodeService,
    ResourceNotFound,
    RouteService,
    StopService,
    TypeService,
)
from bustracker.database import engine, get_session

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


responses: dict[int | str, dict[str, Any]] = {
    404: {"description": "Resource not found"},
}


@app.exception_handler(ResourceNotFound)
async def resource_not_found_handler(request: Request, exc: ResourceNotFound):
    return JSONResponse(
        status_code=404,
        content={
            "detail": "Resource was not found",
            "type": str(exc.type.__name__),
            "identifier": str(exc.identifier),
        },
    )


@app.get("/types", response_model=list[Type])
def read_types(db: Session = Depends(get_session)):
    return TypeService(db).list()


@app.get("/types/{type_name}", response_model=Type, responses=responses)
def read_type(type_name: str, db: Session = Depends(get_session)):
    return TypeService(db).get(type_name)


@app.get("/routes", response_model=list[Route])
def read_routes(db: Session = Depends(get_session)):
    return RouteService(db).list()


@app.get("/routes/{route_id}", response_model=Route, responses=responses)
def read_route(route_id: UUID, db: Session = Depends(get_session)):
    return RouteService(db).get(route_id)


@app.get("/nodes", response_model=list[Node])
def read_nodes(db: Session = Depends(get_session)):
    return NodeService(db).list()


@app.get("/nodes/{node_id}", response_model=Node, responses=responses)
def read_node(node_id: UUID, db: Session = Depends(get_session)):
    return NodeService(db).get(node_id)


@app.get("/stops", response_model=list[Stop])
def read_stops(db: Session = Depends(get_session)):
    return StopService(db).list()


@app.get("/stops/{stop_id}", response_model=Stop, responses=responses)
def read_stop(stop_id: UUID, db: Session = Depends(get_session)):
    return StopService(db).get(stop_id)
