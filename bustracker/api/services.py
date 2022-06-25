from uuid import UUID

import geoalchemy2.shape
import shapely
from bustracker import api
from bustracker import database as db
from bustracker.api import ResourceNotFound
from sqlalchemy import select
from sqlalchemy.orm import Session


class Service:
    def __init__(self, db: Session) -> None:
        self.db = db


class TypeService(Service):
    def list(self) -> list[api.Type]:
        query = select(db.Type)
        values = self.db.scalars(query).all()
        result = list(map(api.Type.from_orm, values))
        return result

    def get(self, name: str) -> api.Type:
        value = self.db.get(db.Type, name)
        if value is None:
            raise ResourceNotFound(api.Type, name)
        return api.Type.from_orm(value)


class RouteService(Service):
    def list(self) -> list[api.Route]:
        query = select(db.Route)
        values = self.db.scalars(query).all()
        result = list(map(api.Route.from_orm, values))
        return result

    def get(self, id: UUID) -> api.Route:
        value = self.db.get(db.Route, id)
        if value is None:
            raise ResourceNotFound(api.Route, id)
        return api.Route.from_orm(value)


class NodeService(Service):
    def list(self) -> list[api.Node]:
        query = select(db.Node)
        values = self.db.scalars(query).all()
        result = list(map(api.Node.from_orm, values))
        return result

    def get(self, id: UUID) -> api.Node:
        value = self.db.get(db.Node, id)
        if value is None:
            raise ResourceNotFound(api.Node, id)
        return api.Node.from_orm(value)


class StopService(Service):
    def list(self) -> list[api.Stop]:
        query = select(db.Stop)
        values = self.db.scalars(query).all()
        result = list(map(self.model_to_schema, values))
        return result

    def get(self, id: UUID) -> api.Stop:
        value = self.db.get(db.Stop, id)
        if value is None:
            raise ResourceNotFound(api.Stop, id)
        return self.model_to_schema(value)

    @staticmethod
    def model_to_schema(model: db.Stop) -> api.Stop:
        shape = geoalchemy2.shape.to_shape(model.location)
        if not isinstance(shape, shapely.geometry.point.Point):
            raise RuntimeError("Could not parse a Point from WKB")
        return api.Stop(
            id=model.id,
            lat=shape.y,
            lon=shape.x,
            node_id=model.node_id,
        )


class RouteStopService(Service):
    def list(self) -> list[api.RouteStop]:
        query = select(db.RouteStop)
        values = self.db.scalars(query).all()
        result = list(map(api.RouteStop.from_orm, values))
        return result

    def get(self, route_id: UUID, stop_id: UUID) -> api.RouteStop:
        value = self.db.get(db.RouteStop, (route_id, stop_id))
        if value is None:
            raise ResourceNotFound(api.RouteStop, (route_id, stop_id))
        return api.RouteStop.from_orm(value)
