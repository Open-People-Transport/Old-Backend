from sqlmodel import SQLModel, create_engine

from . import models
from .settings import POSTGRES_URL

engine = create_engine(POSTGRES_URL, echo=True)


def create_db_tables():
    # All the models have to be imported before creation
    assert models  # nosec
    SQLModel.metadata.create_all(engine)
