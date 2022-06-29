from uuid import UUID

import geoalchemy2.shape
import shapely.geometry.point
from bustracker import core
from bustracker import database as db
from bustracker.core.exceptions import (
    DatabaseIntegrityViolated,
    ResourceAlreadyExists,
    ResourceNotFound,
)
from sqlalchemy import asc, desc, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


class Service:
    def __init__(self, session: Session) -> None:
        self.session = session

    def _try_commit(self) -> None:
        try:
            self.session.commit()
        except IntegrityError as exc:
            raise DatabaseIntegrityViolated(core.Route, exc.args[0])


class TypeService(Service):
    def list(self) -> list[core.Type]:
        query = select(db.Type)
        values = self.session.scalars(query).all()
        result = list(map(core.Type.from_orm, values))
        return result

    def get(self, name: str) -> core.Type:
        value = self.session.get(db.Type, name)
        if value is None:
            raise ResourceNotFound(core.Type, name)
        return core.Type.from_orm(value)

    def create(self, new: core.Type) -> core.Type:
        if new in self:
            raise ResourceAlreadyExists(core.Type, new.name)
        row = db.Type(name=new.name)
        self.session.add(row)
        self.session.commit()
        # No refresh needed
        return core.Type.from_orm(row)

    def update(self, name: str, new: core.Type) -> core.Type:
        row = self.session.get(db.Type, name)
        if row is None:
            raise ResourceNotFound(core.Type, name)
        row.name = new.name
        self._try_commit()
        self.session.refresh(row)
        return core.Type.from_orm(row)

    def delete(self, name: str) -> None:
        row = self.session.get(db.Type, name)
        if row is None:
            raise ResourceNotFound(core.Type, name)
        self.session.delete(row)
        self._try_commit()

    def __contains__(self, item: core.Type) -> bool:
        row = self.session.get(db.Type, item.name)
        return row is not None


class RouteService(Service):
    def list(self) -> list[core.Route]:
        query = select(db.Route)
        values = self.session.scalars(query).all()
        result = list(map(core.Route.from_orm, values))
        return result

    def get(self, id: UUID) -> core.Route:
        value = self.session.get(db.Route, id)
        if value is None:
            raise ResourceNotFound(core.Route, id)
        return core.Route.from_orm(value)

    def update(self, new: core.Route) -> core.Route:
        row = self.session.get(db.Route, new.id)
        if row is None:
            row = db.Route(id=new.id)
            self.session.add(row)
        row.number = new.number
        row.type_name = new.type_name
        self._try_commit()
        self.session.refresh(row)
        return core.Route.from_orm(row)

    def delete(self, id: UUID) -> None:
        row = self.session.get(db.Route, id)
        if not row:
            raise ResourceNotFound(core.Route, id)
        self.session.delete(row)
        self._try_commit()


class NodeService(Service):
    def list(self) -> list[core.Node]:
        query = select(db.Node)
        values = self.session.scalars(query).all()
        result = list(map(core.Node.from_orm, values))
        return result

    def get(self, id: UUID) -> core.Node:
        value = self.session.get(db.Node, id)
        if value is None:
            raise ResourceNotFound(core.Route, id)
        return core.Node.from_orm(value)

    def update(self, new: core.Node) -> core.Node:
        row = self.session.get(db.Node, new.id)
        if row is None:
            row = db.Node(id=new.id)
            self.session.add(row)
        row.name = new.name
        self.session.commit()
        self.session.refresh(row)
        return core.Node.from_orm(row)

    def delete(self, id: UUID) -> None:
        row = self.session.get(db.Node, id)
        if not row:
            raise ResourceNotFound(core.Route, id)
        self.session.delete(row)
        self._try_commit()


class StopService(Service):
    def list(self) -> list[core.Stop]:
        query = select(db.Stop)
        values = self.session.scalars(query).all()
        result = list(map(self.model_to_schema, values))
        return result

    def get(self, id: UUID) -> core.Stop:
        value = self.session.get(db.Stop, id)
        if value is None:
            raise ResourceNotFound(core.Stop, id)
        return self.model_to_schema(value)

    def update(self, new: core.Stop) -> core.Stop:
        row = self.session.get(db.Stop, new.id)
        if row is None:
            row = db.Stop(id=new.id)
            self.session.add(row)
        row.node_id = new.node_id
        shape = shapely.geometry.point.Point(new.lon, new.lat)
        row.location = geoalchemy2.shape.from_shape(shape)
        self.session.commit()
        self.session.refresh(row)
        return self.model_to_schema(row)

    def delete(self, id: UUID) -> None:
        row = self.session.get(db.Stop, id)
        if not row:
            raise ResourceNotFound(core.Stop, id)
        self.session.delete(row)
        self._try_commit()

    @staticmethod
    def model_to_schema(model: db.Stop) -> core.Stop:
        shape = geoalchemy2.shape.to_shape(model.location)
        if not isinstance(shape, shapely.geometry.point.Point):
            raise RuntimeError("Could not parse a Point from WKB")
        return core.Stop(
            id=model.id,
            lat=shape.y,
            lon=shape.x,
            node_id=model.node_id,
        )


class RouteStopService(Service):
    def list(self, route_id: UUID = None, stop_id: UUID = None) -> list[core.RouteStop]:
        query = select(db.RouteStop)
        if route_id:
            query = query.where(db.RouteStop.route_id == route_id)
        if stop_id:
            query = query.where(db.RouteStop.stop_id == stop_id)
        values = self.session.scalars(query).all()
        result = list(map(core.RouteStop.from_orm, values))
        return result

    def get(self, route_id: UUID, stop_id: UUID) -> core.RouteStop:
        value = self.session.get(db.RouteStop, (route_id, stop_id))
        if value is None:
            raise ResourceNotFound(core.RouteStop, (route_id, stop_id))
        return core.RouteStop.from_orm(value)

    def create(
        self,
        route_id: UUID,
        stop_id: UUID,
        after_stop: UUID = None,
    ) -> core.RouteStop:
        row = self.session.get(db.RouteStop, (stop_id, route_id))
        if row is None:
            row = db.RouteStop(stop_id=stop_id, route_id=route_id)
            self.session.add(row)

        # TODO Proper distance calculation algorithm
        # Current solution:
        # * If previous stop is not specified, assume the last one as the previous.
        # * If a next stop after the previous one exists, insert the new stop
        #   exactly in the middle (e.g. 200 + 500 -> 350).
        # * If not, insert 200 meters ahead of the previous (e.g. 200 -> 400).
        prev_stop: db.RouteStop | None
        if after_stop:
            prev_stop = self.session.get(db.RouteStop, (route_id, after_stop))
            if prev_stop is None:
                raise ResourceNotFound(core.Stop, after_stop)
        else:
            query = select(db.RouteStop).order_by(desc(db.RouteStop.distance))
            prev_stop = self.session.scalars(query).first()
        prev_distance = prev_stop.distance if prev_stop else -200
        query = (
            select(db.RouteStop)
            .where(db.RouteStop.distance > prev_distance)
            .order_by(asc(db.RouteStop.distance))
        )
        next_stop: db.RouteStop | None = self.session.scalars(query).first()
        if next_stop:
            current_distance = (prev_distance + next_stop.distance) // 2
        else:
            current_distance = prev_distance + 200

        row.distance = current_distance
        self.session.commit()
        self.session.refresh(row)
        return core.RouteStop.from_orm(row)

    def delete(self, route_id: UUID, stop_id: UUID) -> None:
        row = self.session.get(db.RouteStop, (route_id, stop_id))
        if not row:
            raise ResourceNotFound(core.RouteStop, (route_id, stop_id))
        self.session.delete(row)
        self._try_commit()
