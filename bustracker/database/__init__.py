from bustracker.settings import get_settings
from inflection import underscore
from sqlalchemy import create_engine
from sqlalchemy.orm import as_declarative, declared_attr, sessionmaker

engine = create_engine(get_settings().postgres_url)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


@as_declarative()
class BaseModel:
    @classmethod
    @declared_attr
    def __tablename__(cls) -> str:
        return underscore(cls.__name__)


def init_models():
    """Ensure that all models are registered"""
    from . import models  # pylint: disable=unused-import, import-outside-toplevel


def get_session():
    with SessionLocal() as session:
        yield session


from .models import Node, Route, RouteStop, Stop, Type