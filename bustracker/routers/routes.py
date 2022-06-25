from uuid import UUID

from bustracker.api import Route
from bustracker.api.services import RouteService
from bustracker.database import get_session
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/routes", tags=["routes"])


@router.get("/", response_model=list[Route])
def read_routes(db: Session = Depends(get_session)):
    return RouteService(db).list()


@router.put("/", response_model=Route)
def create_or_update_route(route: Route, db: Session = Depends(get_session)):
    return RouteService(db).update(route)


@router.get("/{route_id}", response_model=Route)
def read_route(route_id: UUID, db: Session = Depends(get_session)):
    return RouteService(db).get(route_id)


@router.delete("/{route_id}")
def delete_route(route_id: UUID, db: Session = Depends(get_session)):
    return RouteService(db).delete(route_id)
