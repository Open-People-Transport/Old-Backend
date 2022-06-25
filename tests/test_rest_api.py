from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from uuid_extensions import uuid7


def test_database_connection(session: Session):
    pass


def test_client_launch(client: TestClient):
    pass


def test_type_create(client: TestClient):
    response = client.put("/types/", json={"name": "bus"})
    assert response.status_code == 200
    assert response.json() == {"name": "bus"}


def test_type_read(client: TestClient):
    response = client.put("/types/", json={"name": "bus"})
    response = client.get("/types/bus")
    assert response.status_code == 200
    assert response.json() == {"name": "bus"}


def test_type_read_all(client: TestClient):
    response = client.put("/types/", json={"name": "bus"})
    response = client.get("/types/")
    assert response.status_code == 200
    assert response.json() == [{"name": "bus"}]


def test_type_update(client: TestClient):
    response = client.put("/types/", json={"name": "bus"})
    response = client.put("/types/bus", json={"name": "tram"})
    assert response.status_code == 200
    assert response.json() == {"name": "tram"}
    response = client.get("/types/")
    assert response.json() == [{"name": "tram"}]


def test_type_delete(client: TestClient):
    response = client.put("/types/", json={"name": "bus"})
    response = client.delete("/types/bus")
    assert response.status_code == 200
    assert response.json() == None
    response = client.get("/types/")
    assert response.json() == []
