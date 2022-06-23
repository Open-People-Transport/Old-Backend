from __future__ import annotations

from typing import Any
from uuid import UUID

import geoalchemy2.shape
import shapely.geometry.point
import strawberry
from bustracker.models import Node as NodeModel
from bustracker.models import Route as RouteModel
from bustracker.models import RouteStop as RouteStopModel
from bustracker.models import Stop as StopModel
from bustracker.models import Type as TypeModel
from sqlmodel import select
from strawberry import Private, Schema
from strawberry.types import Info

from .context import Context


@strawberry.type
class Type:
    name: str

    model: Private[TypeModel]

    @strawberry.field
    def routes(self) -> list[Route]:
        return list(map(Route.from_model, self.model.routes))

    @classmethod
    def from_model(cls, model: TypeModel):
        return cls(
            model=model,
            name=model.name,
        )


@strawberry.type
class Route:
    id: UUID
    number: str

    model: Private[RouteModel]

    @strawberry.field
    def type(self) -> Type:
        return Type.from_model(self.model.type)

    @strawberry.field
    def route_stops(self) -> list[RouteStop]:
        return list(map(RouteStop.from_model, self.model.route_stops))

    @classmethod
    def from_model(cls, model: RouteModel):
        return cls(
            model=model,
            id=model.id,
            number=model.number,
        )


@strawberry.type
class Node:
    id: UUID
    name: str

    model: Private[NodeModel]

    @strawberry.field
    def stops(self) -> list[Stop]:
        return list(map(Stop.from_model, self.model.stops))

    @classmethod
    def from_model(cls, model: NodeModel):
        return cls(
            model=model,
            id=model.id,
            name=model.name,
        )


@strawberry.type
class Stop:
    id: UUID
    lat: float
    lng: float

    model: Private[StopModel]

    @strawberry.field
    def node(self) -> Node:
        return Node.from_model(self.model.node)

    @strawberry.field
    def route_stops(self) -> list[RouteStop]:
        return list(map(RouteStop.from_model, self.model.route_stops))

    @classmethod
    def from_model(cls, model: StopModel):
        shape = geoalchemy2.shape.to_shape(model.location)
        if not isinstance(shape, shapely.geometry.point.Point):
            raise RuntimeError("Could not parse a Point from WKB")
        return cls(
            model=model,
            id=model.id,
            lat=shape.x,
            lng=shape.y,
        )


@strawberry.type
class RouteStop:
    distance: int

    model: Private[RouteStopModel]

    @strawberry.field
    def route(self) -> Route:
        return Route.from_model(self.model.route)

    @strawberry.field
    def stop(self) -> Stop:
        return Stop.from_model(self.model.stop)

    @classmethod
    def from_model(cls, model: RouteStopModel):
        return cls(
            model=model,
            distance=model.distance,
        )


@strawberry.type
class Query:
    @strawberry.field
    def types(self, info: Info[Context, Any]) -> list[Type]:
        statement = select(TypeModel)
        values = info.context.session.exec(statement).all()
        return list(map(Type.from_model, values))

    @strawberry.field
    def routes(self, info: Info[Context, Any]) -> list[Route]:
        statement = select(RouteModel)
        values = info.context.session.exec(statement).all()
        return list(map(Route.from_model, values))

    @strawberry.field
    def nodes(self, info: Info[Context, Any]) -> list[Node]:
        statement = select(NodeModel)
        values = info.context.session.exec(statement).all()
        return list(map(Node.from_model, values))

    @strawberry.field
    def stops(self, info: Info[Context, Any]) -> list[Stop]:
        statement = select(StopModel)
        values = info.context.session.exec(statement).all()
        return list(map(Stop.from_model, values))

    @strawberry.field
    def route_stops(self, info: Info[Context, Any]) -> list[RouteStop]:
        statement = select(RouteStopModel)
        values = info.context.session.exec(statement).all()
        return list(map(RouteStop.from_model, values))


schema = Schema(Query)
