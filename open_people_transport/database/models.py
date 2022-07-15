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
    id: str = Column(String(12), primary_key=True)  # type: ignore
    routes: list[Route] = relationship("Route", back_populates="type")  # type: ignore


class Route(BaseModel):
    id: UUID = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid7)  # type: ignore
    number: str = Column(String(6), nullable=False)  # type: ignore
    type_id: str = Column(String(12), ForeignKey(Type.id), nullable=False)  # type: ignore
    type: Type = relationship("Type", back_populates="routes")  # type: ignore
    route_stops: list[RouteStop] = relationship("RouteStop", back_populates="route")  # type: ignore


class Node(BaseModel):
    id: UUID = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid7)  # type: ignore
    name: str = Column(String(32), nullable=False)  # type: ignore
    stops: list[Stop] = relationship("Stop", back_populates="node")  # type: ignore


class Stop(BaseModel):
    id: UUID = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid7)  # type: ignore
    location: WKBElement = Column(
        Geography("POINT", srid=4326, spatial_index=False),
        nullable=False,
        unique=True,
    )  # type: ignore
    node_id: UUID = Column(ForeignKey(Node.id), nullable=False)  # type: ignore
    node: Node = relationship("Node", back_populates="stops")  # type: ignore
    route_stops: list[RouteStop] = relationship("RouteStop", back_populates="stop")  # type: ignore


class RouteStop(BaseModel):
    route_id: UUID = Column(
        postgresql.UUID(as_uuid=True), ForeignKey(Route.id), primary_key=True  # type: ignore
    )  # type: ignore
    stop_id: UUID = Column(
        postgresql.UUID(as_uuid=True), ForeignKey(Stop.id), primary_key=True  # type: ignore
    )  # type: ignore
    distance: int = Column(Integer, nullable=False)  # type: ignore
    route: Route = relationship("Route", back_populates="route_stops")  # type: ignore
    stop: Stop = relationship("Stop", back_populates="route_stops")  # type: ignore
