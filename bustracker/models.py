from typing import Any
from uuid import UUID, uuid4

from geoalchemy2 import Geography
from sqlmodel import Column, Field, Relationship

from .database import BaseModel


def example(value: Any) -> dict[str, Any]:
    return {"example": value}


class Type(BaseModel, table=True):
    """
    A type of public transportation (e.g. bus, train, etc.).
    """

    name: str = Field(
        description="The name of the type, in lowercase",
        primary_key=True,
        max_length=12,
        schema_extra=example("bus"),
    )
    routes: list["Route"] = Relationship(back_populates="type")


class Route(BaseModel, table=True):
    """
    A transport route that passes through multiple stops
    and has vehicles going along itself.
    """

    id: UUID = Field(primary_key=True, nullable=False, default_factory=uuid4)
    number: str = Field(max_length=6, schema_extra=example("1"))
    type_name: str = Field(foreign_key=Type.name)
    type: Type = Relationship(back_populates="routes")
    route_stops: list["RouteStop"] = Relationship(back_populates="route")


class Node(BaseModel, table=True):
    """
    A bunch of stops located closely together,
    with passengers able to change between them easily.
    """

    id: UUID = Field(primary_key=True, nullable=False, default_factory=uuid4)
    name: str = Field(max_length=32, schema_extra=example("Example St."))
    stops: list["Stop"] = Relationship(back_populates="node")


class Stop(BaseModel, table=True):
    """
    A single physical transport stop, which one or multiple routes can stop at.
    """

    id: UUID = Field(primary_key=True, nullable=False, default_factory=uuid4)
    location: Any = Field(
        sa_column=Column(
            Geography("POINT", srid=4326, spatial_index=False),
            nullable=False,
            unique=True,
        )
    )
    node_id: UUID = Field(foreign_key=Node.id)
    node: Node = Relationship(back_populates="stops")
    route_stops: list["RouteStop"] = Relationship(back_populates="stop")


class RouteStop(BaseModel, table=True):
    """
    A link between a route and a stop.
    """

    route_id: UUID = Field(primary_key=True, foreign_key=Route.id)
    route: Route = Relationship(back_populates="route_stops")
    stop_id: UUID = Field(primary_key=True, foreign_key=Stop.id)
    stop: Stop = Relationship(back_populates="route_stops")
    distance: int = Field(
        primary_key=True,
        schema_extra=example("100"),
        description="Distance in meters from the start of the route to this stop",
    )
