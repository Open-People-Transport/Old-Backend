from inflection import underscore
from open_people_transport.settings import get_settings
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import as_declarative, declared_attr, sessionmaker

engine = create_engine(get_settings().postgres_url, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)


@as_declarative()
class BaseModel:
    metadata: MetaData

    def __init__(self, *args, **kwargs) -> None:
        # TODO Remove when upgrading to SQLAlchemy 2
        super().__init__(*args, **kwargs)

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
