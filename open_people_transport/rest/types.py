from fastapi import APIRouter, Depends
from open_people_transport.core.models import Type
from open_people_transport.crud.services import TypeService
from open_people_transport.database import get_session
from sqlalchemy.orm import Session

router = APIRouter(prefix="/types", tags=["types"])


@router.get("/", response_model=list[Type])
def read_types(db: Session = Depends(get_session)):
    return TypeService(db).list()


@router.put("/", response_model=Type, responses={409: {}})
def create_type(type: Type, db: Session = Depends(get_session)):
    return TypeService(db).create(type)


@router.get("/{type_id}", response_model=Type, responses={404: {}})
def read_type(type_id: str, db: Session = Depends(get_session)):
    return TypeService(db).get(type_id)


@router.put("/{type_id}", response_model=Type, responses={409: {}})
def update_type(type_id: str, type: Type, db: Session = Depends(get_session)):
    return TypeService(db).update(type_id, type)


@router.delete("/{type_id}", responses={409: {}})
def delete_type(type_id: str, db: Session = Depends(get_session)):
    return TypeService(db).delete(type_id)
