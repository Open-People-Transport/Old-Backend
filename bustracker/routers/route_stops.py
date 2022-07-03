from bustracker.core import RouteStop
from bustracker.core.services import RouteStopService
from bustracker.database import get_session
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/route_stops", tags=["route_stops"])
