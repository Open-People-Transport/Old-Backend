from __future__ import annotations

import uuid
from typing import TypeAlias

from geoalchemy2 import Geography, WKBElement
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, String
from uuid_extensions import uuid7

from . import BaseModel

UUID: TypeAlias = postgresql.UUID | uuid.UUID


class Type(BaseModel):
    name: str = Column(String(12), primary_key=True)
    routes: list[Route] = relationship("Route", back_populates="type")


class Route(BaseModel):
    id: UUID = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid7)
    number: str = Column(String(6), nullable=False)
    type_name: str = Column(String(12), ForeignKey(Type.name), nullable=False)
    type: Type = relationship("Type", back_populates="routes")
    route_stops: list[RouteStop] = relationship("RouteStop", back_populates="route")


class Node(BaseModel):
    id: UUID = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid7)
    name: str = Column(String(32), nullable=False)
    stops: list[Stop] = relationship("Stop", back_populates="node")


class Stop(BaseModel):
    id: UUID = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid7)
    location: WKBElement = Column(
        Geography("POINT", srid=4326, spatial_index=False),
        nullable=False,
        unique=True,
    )
    node_id: UUID = Column(ForeignKey(Node.id), nullable=False)
    node: Node = relationship("Node", back_populates="stops")
    route_stops: list[RouteStop] = relationship("RouteStop", back_populates="stop")


class RouteStop(BaseModel):
    route_id: UUID = Column(postgresql.UUID, ForeignKey(Route.id), primary_key=True)
    stop_id: UUID = Column(postgresql.UUID, ForeignKey(Stop.id), primary_key=True)
    distance: int = Column(Integer, nullable=False)
    route: Route = relationship("Route", back_populates="route_stops")
    stop: Stop = relationship("Stop", back_populates="route_stops")
