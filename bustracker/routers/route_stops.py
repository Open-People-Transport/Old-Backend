from bustracker.api import RouteStop
from bustracker.api.services import RouteStopService
from bustracker.database import get_session
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/route_stops", tags=["route_stops"])


@router.get("/", response_model=list[RouteStop])
def read_route_stops(db: Session = Depends(get_session)):
    return RouteStopService(db).list()
