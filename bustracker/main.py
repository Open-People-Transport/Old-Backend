from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Session, select

from . import models
from .database import create_db_tables, get_session

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_tables()


@app.get("/", response_model=list[models.City])
def read_cities(session: Session = Depends(get_session)):
    query = select(models.City)
    cities = session.exec(query).all()
    return cities


@app.post("/", response_model=models.City, status_code=status.HTTP_201_CREATED)
def create_city(city: models.City, session: Session = Depends(get_session)):
    if session.get(models.City, city.abbr):
        raise HTTPException(status.HTTP_409_CONFLICT, detail="City already exists")
    session.add(city)
    session.commit()
    session.refresh(city)
    return city
