from __future__ import annotations

from typing import Any, Optional, TypeAlias
from uuid import UUID

import geoalchemy2.shape
import shapely.geometry.point
import strawberry
import strawberry.types
from open_people_transport.database.models import Node as SQLNode
from open_people_transport.database.models import Route as SQLRoute
from open_people_transport.database.models import RouteStop as SQLRouteStop
from open_people_transport.database.models import Stop as SQLStop
from open_people_transport.database.models import Type as SQLType
from sqlalchemy import desc, select
from sqlalchemy.exc import IntegrityError
from strawberry import Private, Schema

from .context import Context

Info: TypeAlias = strawberry.types.Info[Context, Any]


@strawberry.type
class Type:
    name: str

    model: Private[SQLType]

    @strawberry.field
    def routes(self) -> list[Route]:
        return list(map(Route.from_model, self.model.routes))

    @classmethod
    def from_model(cls, model: SQLType):
        return cls(
            model=model,
            name=model.name,
        )


@strawberry.type
class Route:
    id: UUID
    number: str

    model: Private[SQLRoute]

    @strawberry.field
    def type(self) -> Type:
        return Type.from_model(self.model.type)

    @strawberry.field
    def route_stops(self) -> list[RouteStop]:
        return list(map(RouteStop.from_model, self.model.route_stops))

    @classmethod
    def from_model(cls, model: SQLRoute):
        return cls(
            model=model,
            id=model.id,
            number=model.number,
        )


@strawberry.type
class Node:
    id: UUID
    name: str

    model: Private[SQLNode]

    @strawberry.field
    def stops(self) -> list[Stop]:
        return list(map(Stop.from_model, self.model.stops))

    @classmethod
    def from_model(cls, model: SQLNode):
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

    model: Private[SQLStop]

    @strawberry.field
    def node(self) -> Node:
        return Node.from_model(self.model.node)

    @strawberry.field
    def route_stops(self) -> list[RouteStop]:
        return list(map(RouteStop.from_model, self.model.route_stops))

    @classmethod
    def from_model(cls, model: SQLStop):
        shape = geoalchemy2.shape.to_shape(model.location)
        if not isinstance(shape, shapely.geometry.point.Point):
            raise RuntimeError("Could not parse a Point from WKB")
        return cls(
            model=model,
            id=model.id,
            lat=shape.x,
            lng=shape.y,
        )


@strawberry.input
class StopInput:
    lat: float
    lng: float


@strawberry.type
class RouteStop:
    distance: int

    model: Private[SQLRouteStop]

    @strawberry.field
    def route(self) -> Route:
        return Route.from_model(self.model.route)

    @strawberry.field
    def stop(self) -> Stop:
        return Stop.from_model(self.model.stop)

    @classmethod
    def from_model(cls, model: SQLRouteStop):
        return cls(
            model=model,
            distance=model.distance,
        )


@strawberry.type
class Query:
    @strawberry.field
    def types(self, info: Info) -> list[Type]:
        statement = select(SQLType)
        values = info.context.session.execute(statement).scalars().all()
        return list(map(Type.from_model, values))

    @strawberry.field
    def routes(self, info: Info) -> list[Route]:
        statement = select(SQLRoute)
        values = info.context.session.execute(statement).scalars().all()
        return list(map(Route.from_model, values))

    @strawberry.field
    def nodes(self, info: Info) -> list[Node]:
        statement = select(SQLNode)
        values = info.context.session.execute(statement).scalars().all()
        return list(map(Node.from_model, values))

    @strawberry.field
    def stops(self, info: Info) -> list[Stop]:
        statement = select(SQLStop)
        values = info.context.session.execute(statement).scalars().all()
        return list(map(Stop.from_model, values))

    @strawberry.field
    def route_stops(self, info: Info) -> list[RouteStop]:
        statement = select(SQLRouteStop)
        values = info.context.session.execute(statement).scalars().all()
        return list(map(RouteStop.from_model, values))


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_type(self, info: Info, name: str) -> Type:
        model = SQLType(name=name)
        info.context.session.add(model)
        try:
            info.context.session.commit()
        except IntegrityError:
            raise RuntimeError("Type with this name already exists")
        return Type.from_model(model)

    @strawberry.mutation
    def add_route(
        self,
        info: Info,
        number: str,
        type_name: str,
        stops: Optional[list[UUID]] = None,
    ) -> Route:
        model = SQLRoute(number=number, type_name=type_name)
        info.context.session.add(model)
        if stops:
            for i, stop_id in enumerate(stops):
                route_stop = SQLRouteStop(
                    distance=i * 100, route_id=model.id, stop_id=stop_id
                )
                info.context.session.add(route_stop)
        try:
            info.context.session.commit()
        except IntegrityError:
            raise RuntimeError("Invalid or conflicting mutation arguments")
        info.context.session.refresh(model)
        return Route.from_model(model)

    @strawberry.mutation
    def add_node(
        self,
        info: Info,
        name: str,
        stops: Optional[list[StopInput]] = None,
    ) -> Node:
        model = SQLNode(name=name)
        info.context.session.add(model)
        if stops:
            for stop in stops:
                point = shapely.geometry.point.Point(stop.lng, stop.lat)
                location = geoalchemy2.shape.from_shape(point)
                stop_model = SQLStop(location=location, node_id=model.id)
                info.context.session.add(stop_model)
        try:
            info.context.session.commit()
        except IntegrityError:
            raise RuntimeError("Invalid or conflicting mutation arguments")
        info.context.session.refresh(model)
        return Node.from_model(model)

    @strawberry.mutation
    def add_stop(
        self,
        info: Info,
        node_id: UUID,
        lat: float,
        lng: float,
    ) -> Stop:
        point = shapely.geometry.point.Point(lng, lat)
        location = geoalchemy2.shape.from_shape(point)
        model = SQLStop(location=location, node_id=node_id)
        info.context.session.add(model)
        try:
            info.context.session.commit()
        except IntegrityError:
            raise RuntimeError("Invalid or conflicting mutation arguments")
        info.context.session.refresh(model)
        return Stop.from_model(model)

    @strawberry.mutation
    def add_route_stop(
        self,
        info: Info,
        route_id: UUID,
        stop_id: UUID,
    ) -> RouteStop:
        statement = (
            select(SQLRouteStop)
            .where(SQLRouteStop.route_id == route_id)
            .order_by(desc(SQLRouteStop.distance))
        )
        last_stop = info.context.session.execute(statement).scalars().first()
        distance = last_stop.distance + 100 if last_stop else 0
        model = SQLRouteStop(route_id=route_id, stop_id=stop_id, distance=distance)
        info.context.session.add(model)
        try:
            info.context.session.commit()
        except IntegrityError:
            raise RuntimeError("Invalid or conflicting mutation arguments")
        info.context.session.refresh(model)
        return RouteStop.from_model(model)

    @strawberry.mutation
    def delete_unique(self, info: Info, uuid: UUID) -> None:
        for ModelType in (SQLRoute, SQLNode, SQLStop):  # type: ignore
            if model := info.context.session.get(ModelType, uuid):  # type: ignore
                info.context.session.delete(model)
                try:
                    info.context.session.commit()
                except IntegrityError:
                    raise RuntimeError("Found, but could not delete the unit")
                return
        raise RuntimeError("Unique unit not found")


schema = Schema(Query, Mutation)
