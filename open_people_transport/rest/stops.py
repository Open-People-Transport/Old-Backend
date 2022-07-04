from uuid import UUID

from fastapi import APIRouter, Depends
from open_people_transport.core.models import Stop
from open_people_transport.crud.services import StopService
from open_people_transport.database import get_session
from sqlalchemy.orm import Session

router = APIRouter(prefix="/stops", tags=["stops"])


@router.get("/", response_model=list[Stop])
def read_stops(db: Session = Depends(get_session)):
    return StopService(db).list()


@router.put("/", response_model=Stop, responses={409: {}})
def create_or_update_stop(stop: Stop, db: Session = Depends(get_session)):
    return StopService(db).update(stop)


@router.get("/{stop_id}", response_model=Stop, responses={404: {}})
def read_stop(stop_id: UUID, db: Session = Depends(get_session)):
    return StopService(db).get(stop_id)


@router.delete("/{stop_id}", responses={409: {}})
def delete_stop(stop_id: UUID, db: Session = Depends(get_session)):
    return StopService(db).delete(stop_id)
