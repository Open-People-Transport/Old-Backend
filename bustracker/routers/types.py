from bustracker.api import Type
from bustracker.api.services import TypeService
from bustracker.database import get_session
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/types", tags=["items"])


@router.get("/", response_model=list[Type])
def read_types(db: Session = Depends(get_session)):
    return TypeService(db).list()


@router.put("/", response_model=Type)
def create_type(type: Type, db: Session = Depends(get_session)):
    return TypeService(db).create(type)


@router.get("/{type_name}", response_model=Type)
def read_type(type_name: str, db: Session = Depends(get_session)):
    return TypeService(db).get(type_name)


@router.put("/{type_name}", response_model=Type)
def update_type(type_name: str, type: Type, db: Session = Depends(get_session)):
    return TypeService(db).update(type_name, type)


@router.delete("/{type_name}")
def delete_type(type_name: str, db: Session = Depends(get_session)):
    return TypeService(db).delete(type_name)
