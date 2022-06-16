from sqlmodel import Session, SQLModel, create_engine

from .settings import get_settings

engine = create_engine(get_settings().postgres_url, echo=True)


def init_models():
    """Ensure that all models are registered before creating tables"""
    from . import models  # pylint: disable=unused-import, import-outside-toplevel


def create_db_tables():
    init_models()
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
