import pytest
from fastapi.testclient import TestClient
from open_people_transport.api import app
from open_people_transport.database import BaseModel, get_session, init_models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

TESTING_DB_URL = "postgresql://bustracker1:GnhkLL82@localhost:5432/bustracker_test"
engine = create_engine(TESTING_DB_URL, future=True)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, future=True
)


@pytest.fixture()
def session():
    init_models()
    BaseModel.metadata.drop_all(bind=engine)
    BaseModel.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(session):
    def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session
    yield TestClient(app)
