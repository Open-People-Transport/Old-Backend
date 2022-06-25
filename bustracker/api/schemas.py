from __future__ import annotations

from decimal import Decimal
from uuid import UUID

import pydantic
from pydantic import Field
from uuid_extensions import uuid7


class BaseModel(pydantic.BaseModel):
    class Config:
        orm_mode = True


class Type(BaseModel):
    """
    A type of public transportation (e.g. bus, train, etc.).
    """

    name: str = Field(max_length=12, example="bus")


class Route(BaseModel):
    """
    A transport route that passes through multiple stops and has vehicles going along
    itself.
    """

    id: UUID = Field(default_factory=uuid7)
    number: str = Field(max_length=6, example="1")
    type_name: str = Field(max_length=12, example="bus")


class Node(BaseModel):
    """
    A bunch of stops located closely together, with passengers able to change between
    them easily.
    """

    id: UUID = Field(default_factory=uuid7)
    name: str = Field(max_length=32, example="Example St.")


class Stop(BaseModel):
    """
    A single physical transport stop, which one or multiple routes can stop at.
    """

    id: UUID = Field(nullable=False, default_factory=uuid7)
    node_id: UUID
    lat: Decimal = Field(max_digits=9, decimal_places=7, example="89.1234567")
    lon: Decimal = Field(max_digits=10, decimal_places=7, example="179.1234567")

    class Config:
        orm_mode = False


class RouteStop(BaseModel):
    """
    A link between a route and a stop.
    """

    route_id: UUID
    stop_id: UUID
    distance: int = Field(
        example="100",
        description="Distance in meters from the start of the route to this stop",
    )
