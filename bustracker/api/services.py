from uuid import UUID

import geoalchemy2.shape
import shapely.geometry.point
from bustracker import api
from bustracker import database as db
from fastapi import HTTPException
from sqlalchemy import asc, desc, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT


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
            raise HTTPException(HTTP_404_NOT_FOUND)
        return api.Type.from_orm(value)

    def create(self, new: api.Type) -> api.Type:
        if new in self:
            raise HTTPException(HTTP_409_CONFLICT)
        row = db.Type(name=new.name)
        self.db.add(row)
        self.db.commit()
        # No refresh needed
        return api.Type.from_orm(row)

    def update(self, name: str, new: api.Type) -> api.Type:
        row = self.db.get(db.Type, name)
        if row is None:
            raise HTTPException(HTTP_404_NOT_FOUND)
        row.name = new.name
        try:
            self.db.commit()
        except IntegrityError as exc:
            raise HTTPException(HTTP_409_CONFLICT, str(exc.orig))
        self.db.refresh(row)
        return api.Type.from_orm(row)

    def delete(self, name: str) -> None:
        row = self.db.get(db.Type, name)
        if row is None:
            raise HTTPException(HTTP_404_NOT_FOUND)
        self.db.delete(row)
        try:
            self.db.commit()
        except IntegrityError as exc:
            raise HTTPException(HTTP_409_CONFLICT, str(exc.orig))

    def __contains__(self, item: api.Type):
        row = self.db.get(db.Type, item.name)
        return row is not None


class RouteService(Service):
    def list(self) -> list[api.Route]:
        query = select(db.Route)
        values = self.db.scalars(query).all()
        result = list(map(api.Route.from_orm, values))
        return result

    def get(self, id: UUID) -> api.Route:
        value = self.db.get(db.Route, id)
        if value is None:
            raise HTTPException(HTTP_404_NOT_FOUND)
        return api.Route.from_orm(value)

    def update(self, new: api.Route) -> api.Route:
        row = self.db.get(db.Route, new.id)
        if row is None:
            row = db.Route(id=new.id)
            self.db.add(row)
        row.number = new.number
        row.type_name = new.type_name
        self.db.commit()
        self.db.refresh(row)
        return api.Route.from_orm(row)

    def delete(self, id: UUID) -> None:
        row = self.db.get(db.Route, id)
        if not row:
            raise HTTPException(HTTP_404_NOT_FOUND)
        self.db.delete(row)
        try:
            self.db.commit()
        except IntegrityError as exc:
            raise HTTPException(HTTP_409_CONFLICT, str(exc.orig))


class NodeService(Service):
    def list(self) -> list[api.Node]:
        query = select(db.Node)
        values = self.db.scalars(query).all()
        result = list(map(api.Node.from_orm, values))
        return result

    def get(self, id: UUID) -> api.Node:
        value = self.db.get(db.Node, id)
        if value is None:
            raise HTTPException(HTTP_404_NOT_FOUND)
        return api.Node.from_orm(value)

    def update(self, new: api.Node) -> api.Node:
        row = self.db.get(db.Node, new.id)
        if row is None:
            row = db.Node(id=new.id)
            self.db.add(row)
        row.name = new.name
        self.db.commit()
        self.db.refresh(row)
        return api.Node.from_orm(row)

    def delete(self, id: UUID) -> None:
        row = self.db.get(db.Node, id)
        if not row:
            raise HTTPException(HTTP_404_NOT_FOUND)
        self.db.delete(row)
        try:
            self.db.commit()
        except IntegrityError as exc:
            raise HTTPException(HTTP_409_CONFLICT, str(exc.orig))


class StopService(Service):
    def list(self) -> list[api.Stop]:
        query = select(db.Stop)
        values = self.db.scalars(query).all()
        result = list(map(self.model_to_schema, values))
        return result

    def get(self, id: UUID) -> api.Stop:
        value = self.db.get(db.Stop, id)
        if value is None:
            raise HTTPException(HTTP_404_NOT_FOUND)
        return self.model_to_schema(value)

    def update(self, new: api.Stop) -> api.Stop:
        row = self.db.get(db.Stop, new.id)
        if row is None:
            row = db.Stop(id=new.id)
            self.db.add(row)
        row.node_id = new.node_id
        shape = shapely.geometry.point.Point(new.lon, new.lat)
        row.location = geoalchemy2.shape.from_shape(shape)
        self.db.commit()
        self.db.refresh(row)
        return api.Stop.from_orm(row)

    def delete(self, id: UUID) -> None:
        row = self.db.get(db.Stop, id)
        if not row:
            raise HTTPException(HTTP_404_NOT_FOUND)
        self.db.delete(row)
        try:
            self.db.commit()
        except IntegrityError as exc:
            raise HTTPException(HTTP_409_CONFLICT, str(exc.orig))

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
    def list(self, route_id: UUID = None, stop_id: UUID = None) -> list[api.RouteStop]:
        query = select(db.RouteStop)
        if route_id:
            query = query.where(db.RouteStop.route_id == route_id)
        if stop_id:
            query = query.where(db.RouteStop.stop_id == stop_id)
        values = self.db.scalars(query).all()
        result = list(map(api.RouteStop.from_orm, values))
        return result

    def get(self, route_id: UUID, stop_id: UUID) -> api.RouteStop:
        value = self.db.get(db.RouteStop, (route_id, stop_id))
        if value is None:
            raise HTTPException(HTTP_404_NOT_FOUND)
        return api.RouteStop.from_orm(value)

    def create(
        self,
        route_id: UUID,
        stop_id: UUID,
        after_stop: UUID = None,
    ) -> api.RouteStop:
        row = self.db.get(db.RouteStop, (stop_id, route_id))
        if row is None:
            row = db.RouteStop(stop_id=stop_id, route_id=route_id)
            self.db.add(row)

        # TODO Proper distance calculation algorithm
        # Current solution:
        # * If previous stop is not specified, assume the last one as the previous.
        # * If a next stop after the previous one exists, insert the new stop
        #   exactly in the middle (e.g. 200 + 500 -> 350).
        # * If not, insert 200 meters ahead of the previous (e.g. 200 -> 400).
        prev_stop: db.RouteStop | None
        if after_stop:
            prev_stop = self.db.get(db.RouteStop, (route_id, after_stop))
            if prev_stop is None:
                raise HTTPException(HTTP_404_NOT_FOUND)
        else:
            query = select(db.RouteStop).order_by(desc(db.RouteStop.distance))
            prev_stop = self.db.scalars(query).first()
        prev_distance = prev_stop.distance if prev_stop else -200
        query = (
            select(db.RouteStop)
            .where(db.RouteStop.distance > prev_distance)
            .order_by(asc(db.RouteStop.distance))
        )
        next_stop: db.RouteStop | None = self.db.scalars(query).first()
        if next_stop:
            current_distance = (prev_distance + next_stop.distance) // 2
        else:
            current_distance = prev_distance + 200

        row.distance = current_distance
        self.db.commit()
        self.db.refresh(row)
        return api.RouteStop.from_orm(row)

    def delete(self, route_id: UUID, stop_id: UUID) -> None:
        row = self.db.get(db.RouteStop, (route_id, stop_id))
        if not row:
            raise HTTPException(HTTP_404_NOT_FOUND)
        self.db.delete(row)
        try:
            self.db.commit()
        except IntegrityError as exc:
            raise HTTPException(HTTP_409_CONFLICT, str(exc.orig))
