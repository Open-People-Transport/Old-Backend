from uuid import UUID

from bustracker.api import Stop
from bustracker.api.services import StopService
from bustracker.database import get_session
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/stops", tags=["stops"])


@router.get("/", response_model=list[Stop])
def read_stops(db: Session = Depends(get_session)):
    return StopService(db).list()


@router.put("/", response_model=Stop)
def create_or_update_stop(stop: Stop, db: Session = Depends(get_session)):
    return StopService(db).update(stop)


@router.get("/{stop_id}", response_model=Stop)
def read_stop(stop_id: UUID, db: Session = Depends(get_session)):
    return StopService(db).get(stop_id)


@router.delete("/{stop_id}")
def delete_stop(stop_id: UUID, db: Session = Depends(get_session)):
    return StopService(db).delete(stop_id)
