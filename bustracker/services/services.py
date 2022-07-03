from typing import Optional
from uuid import UUID

import geoalchemy2.shape
import shapely.geometry.point
from bustracker.core.models import Node as CoreNode
from bustracker.core.models import Route as CoreRoute
from bustracker.core.models import RouteStop as CoreRouteStop
from bustracker.core.models import Stop as CoreStop
from bustracker.core.models import Type as CoreType
from bustracker.database.models import Node as SQLNode
from bustracker.database.models import Route as SQLRoute
from bustracker.database.models import RouteStop as SQLRouteStop
from bustracker.database.models import Stop as SQLStop
from bustracker.database.models import Type as SQLType
from sqlalchemy import asc, desc, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .exceptions import (
    DatabaseIntegrityViolated,
    ResourceAlreadyExists,
    ResourceNotFound,
)


class Service:
    def __init__(self, session: Session) -> None:
        self.session = session

    def _try_commit(self) -> None:
        try:
            self.session.commit()
        except IntegrityError as exc:
            raise DatabaseIntegrityViolated(CoreRoute, exc.args[0])


class TypeService(Service):
    def list(self) -> list[CoreType]:
        query = select(SQLType)
        values = self.session.scalars(query).all()
        result = list(map(CoreType.from_orm, values))
        return result

    def get(self, name: str) -> CoreType:
        value = self.session.get(SQLType, name)
        if value is None:
            raise ResourceNotFound(CoreType, name)
        return CoreType.from_orm(value)

    def create(self, new: CoreType) -> CoreType:
        if new in self:
            raise ResourceAlreadyExists(CoreType, new.name)
        row = SQLType(name=new.name)
        self.session.add(row)
        self.session.commit()
        # No refresh needed
        return CoreType.from_orm(row)

    def update(self, name: str, new: CoreType) -> CoreType:
        row = self.session.get(SQLType, name)
        if row is None:
            raise ResourceNotFound(CoreType, name)
        row.name = new.name
        self._try_commit()
        self.session.refresh(row)
        return CoreType.from_orm(row)

    def delete(self, name: str) -> None:
        row = self.session.get(SQLType, name)
        if row is None:
            raise ResourceNotFound(CoreType, name)
        self.session.delete(row)
        self._try_commit()

    def __contains__(self, item: CoreType) -> bool:
        row = self.session.get(SQLType, item.name)
        return row is not None


class RouteService(Service):
    def list(self) -> list[CoreRoute]:
        query = select(SQLRoute)
        values = self.session.scalars(query).all()
        result = list(map(CoreRoute.from_orm, values))
        return result

    def get(self, id: UUID) -> CoreRoute:
        value = self.session.get(SQLRoute, id)
        if value is None:
            raise ResourceNotFound(CoreRoute, id)
        return CoreRoute.from_orm(value)

    def update(self, new: CoreRoute) -> CoreRoute:
        row = self.session.get(SQLRoute, new.id)
        if row is None:
            row = SQLRoute(id=new.id)
            self.session.add(row)
        row.number = new.number
        row.type_name = new.type_name
        self._try_commit()
        self.session.refresh(row)
        return CoreRoute.from_orm(row)

    def delete(self, id: UUID) -> None:
        row = self.session.get(SQLRoute, id)
        if not row:
            raise ResourceNotFound(CoreRoute, id)
        self.session.delete(row)
        self._try_commit()


class NodeService(Service):
    def list(self) -> list[CoreNode]:
        query = select(SQLNode)
        values = self.session.scalars(query).all()
        result = list(map(CoreNode.from_orm, values))
        return result

    def get(self, id: UUID) -> CoreNode:
        value = self.session.get(SQLNode, id)
        if value is None:
            raise ResourceNotFound(CoreRoute, id)
        return CoreNode.from_orm(value)

    def update(self, new: CoreNode) -> CoreNode:
        row = self.session.get(SQLNode, new.id)
        if row is None:
            row = SQLNode(id=new.id)
            self.session.add(row)
        row.name = new.name
        self.session.commit()
        self.session.refresh(row)
        return CoreNode.from_orm(row)

    def delete(self, id: UUID) -> None:
        row = self.session.get(SQLNode, id)
        if not row:
            raise ResourceNotFound(CoreRoute, id)
        self.session.delete(row)
        self._try_commit()


class StopService(Service):
    def list(self) -> list[CoreStop]:
        query = select(SQLStop)
        values = self.session.scalars(query).all()
        result = list(map(self.model_to_schema, values))
        return result

    def get(self, id: UUID) -> CoreStop:
        value = self.session.get(SQLStop, id)
        if value is None:
            raise ResourceNotFound(CoreStop, id)
        return self.model_to_schema(value)

    def update(self, new: CoreStop) -> CoreStop:
        row = self.session.get(SQLStop, new.id)
        if row is None:
            row = SQLStop(id=new.id)
            self.session.add(row)
        row.node_id = new.node_id
        shape = shapely.geometry.point.Point(new.lon, new.lat)
        row.location = geoalchemy2.shape.from_shape(shape)
        self.session.commit()
        self.session.refresh(row)
        return self.model_to_schema(row)

    def delete(self, id: UUID) -> None:
        row = self.session.get(SQLStop, id)
        if not row:
            raise ResourceNotFound(CoreStop, id)
        self.session.delete(row)
        self._try_commit()

    @staticmethod
    def model_to_schema(model: SQLStop) -> CoreStop:
        shape = geoalchemy2.shape.to_shape(model.location)
        if not isinstance(shape, shapely.geometry.point.Point):
            raise RuntimeError("Could not parse a Point from WKB")
        return CoreStop(
            id=model.id,
            lat=shape.y,
            lon=shape.x,
            node_id=model.node_id,
        )


class RouteStopService(Service):
    def list(
        self, route_id: Optional[UUID] = None, stop_id: Optional[UUID] = None
    ) -> list[CoreRouteStop]:
        query = select(SQLRouteStop)
        if route_id:
            query = query.where(SQLRouteStop.route_id == route_id)
        if stop_id:
            query = query.where(SQLRouteStop.stop_id == stop_id)
        values = self.session.scalars(query).all()
        result = list(map(CoreRouteStop.from_orm, values))
        return result

    def get(self, route_id: UUID, stop_id: UUID) -> CoreRouteStop:
        value = self.session.get(SQLRouteStop, (route_id, stop_id))
        if value is None:
            raise ResourceNotFound(CoreRouteStop, (route_id, stop_id))
        return CoreRouteStop.from_orm(value)

    def create(
        self,
        route_id: UUID,
        stop_id: UUID,
        after_stop: Optional[UUID] = None,
    ) -> CoreRouteStop:
        row = self.session.get(SQLRouteStop, (stop_id, route_id))
        if row is None:
            row = SQLRouteStop(stop_id=stop_id, route_id=route_id)
            self.session.add(row)

        # TODO Proper distance calculation algorithm
        # Current solution:
        # * If previous stop is not specified, assume the last one as the previous.
        # * If a next stop after the previous one exists, insert the new stop
        #   exactly in the middle (e.g. 200 + 500 -> 350).
        # * If not, insert 200 meters ahead of the previous (e.g. 200 -> 400).
        prev_stop: SQLRouteStop | None
        if after_stop:
            prev_stop = self.session.get(SQLRouteStop, (route_id, after_stop))
            if prev_stop is None:
                raise ResourceNotFound(CoreStop, after_stop)
        else:
            query = select(SQLRouteStop).order_by(desc(SQLRouteStop.distance))
            prev_stop = self.session.scalars(query).first()
        prev_distance = prev_stop.distance if prev_stop else -200
        query = (
            select(SQLRouteStop)
            .where(SQLRouteStop.distance > prev_distance)
            .order_by(asc(SQLRouteStop.distance))
        )
        next_stop: SQLRouteStop | None = self.session.scalars(query).first()
        if next_stop:
            current_distance = (prev_distance + next_stop.distance) // 2
        else:
            current_distance = prev_distance + 200

        row.distance = current_distance
        self.session.commit()
        self.session.refresh(row)
        return CoreRouteStop.from_orm(row)

    def delete(self, route_id: UUID, stop_id: UUID) -> None:
        row = self.session.get(SQLRouteStop, (route_id, stop_id))
        if not row:
            raise ResourceNotFound(CoreRouteStop, (route_id, stop_id))
        self.session.delete(row)
        self._try_commit()
