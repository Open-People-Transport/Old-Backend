from typing import Any
from uuid import UUID

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from sqladmin import Admin
from sqlalchemy.orm import Session
from strawberry.fastapi import GraphQLRouter
from uuid_extensions import uuid7

from bustracker.admin_models import NodeAdmin  # type: ignore
from bustracker.admin_models import RouteAdmin  # type: ignore
from bustracker.admin_models import StopAdmin  # type: ignore
from bustracker.admin_models import TypeAdmin  # type: ignore
from bustracker.api.exceptions import ResourceException
from bustracker.api.schemas import Node, Route, Stop, Type
from bustracker.api.services import NodeService, RouteService, StopService, TypeService
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


@app.get("/types", response_model=list[Type])
def read_types(db: Session = Depends(get_session)):
    return TypeService(db).list()


@app.put("/types/", response_model=Type)
def create_type(type: Type, db: Session = Depends(get_session)):
    return TypeService(db).create(type)


@app.get("/types/{type_name}", response_model=Type, responses=GET_RESPONSES)
def read_type(type_name: str, db: Session = Depends(get_session)):
    return TypeService(db).get(type_name)


@app.put("/types/{type_name}", response_model=Type)
def update_type(type_name: str, type: Type, db: Session = Depends(get_session)):
    return TypeService(db).update(type_name, type)


@app.delete("/types/{type_name}")
def delete_type(type_name: str, db: Session = Depends(get_session)):
    return TypeService(db).delete(type_name)


@app.get("/routes", response_model=list[Route])
def read_routes(db: Session = Depends(get_session)):
    return RouteService(db).list()


@app.put("/routes", response_model=Route)
def create_or_update_route(route: Route, db: Session = Depends(get_session)):
    return RouteService(db).update(route)


@app.get("/routes/{route_id}", response_model=Route, responses=GET_RESPONSES)
def read_route(route_id: UUID, db: Session = Depends(get_session)):
    return RouteService(db).get(route_id)


@app.delete("/routes/{route_id}")
def delete_route(route_id: UUID, db: Session = Depends(get_session)):
    return RouteService(db).delete(route_id)


@app.get("/nodes", response_model=list[Node])
def read_nodes(db: Session = Depends(get_session)):
    return NodeService(db).list()


@app.put("/nodes", response_model=Node)
def create_or_update_node(node: Node, db: Session = Depends(get_session)):
    return NodeService(db).update(node)


@app.get("/nodes/{node_id}", response_model=Node, responses=GET_RESPONSES)
def read_node(node_id: UUID, db: Session = Depends(get_session)):
    return NodeService(db).get(node_id)


@app.delete("/nodes/{node_id}")
def delete_node(node_id: UUID, db: Session = Depends(get_session)):
    return NodeService(db).delete(node_id)


@app.get("/stops", response_model=list[Stop])
def read_stops(db: Session = Depends(get_session)):
    return StopService(db).list()


@app.put("/stops", response_model=Stop)
def create_or_update_stop(stop: Stop, db: Session = Depends(get_session)):
    return StopService(db).update(stop)


@app.get("/stops/{stop_id}", response_model=Stop, responses=GET_RESPONSES)
def read_stop(stop_id: UUID, db: Session = Depends(get_session)):
    return StopService(db).get(stop_id)


@app.delete("/stops/{stop_id}")
def delete_stop(stop_id: UUID, db: Session = Depends(get_session)):
    return StopService(db).delete(stop_id)


@app.get("/uuid")
def get_random_uuid():
    return uuid7()
