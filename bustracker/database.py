from inflection import underscore
from sqlalchemy.orm import declared_attr
from sqlmodel import Session, SQLModel, create_engine

from .settings import get_settings

engine = create_engine(get_settings().postgres_url)


def init_models():
    """Ensure that all models are registered"""
    from . import models  # pylint: disable=unused-import, import-outside-toplevel


def get_session():
    with Session(engine) as session:
        yield session


class BaseModel(SQLModel):
    @declared_attr
    def __tablename__(cls) -> str:  # type: ignore
        return underscore(cls.__name__)
