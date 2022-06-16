from sqlmodel import Session, SQLModel, create_engine

from . import models
from .settings import get_settings

engine = create_engine(get_settings().postgres_url, echo=True)


def create_db_tables():
    # All the models have to be imported before creation
    assert models  # nosec
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
