from uuid import UUID

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


def test_route_create_with_id(client: TestClient):
    response = client.put("/types/", json={"name": "bus"})
    id = str(uuid7())
    data = {
        "id": id,
        "number": "1",
        "type_name": "bus",
    }
    response = client.put("/routes/", json=data)
    assert response.status_code == 200
    assert response.json() == data


def test_route_create_without_id(client: TestClient):
    response = client.put("/types/", json={"name": "bus"})
    data = {
        "number": "1",
        "type_name": "bus",
    }
    response = client.put("/routes/", json=data)
    assert response.status_code == 200
    id = UUID(response.json()["id"])
    assert response.json() == ({"id": str(id)} | data)


def test_route_read(client: TestClient):
    response = client.put("/types/", json={"name": "bus"})
    id = str(uuid7())
    data = {
        "id": id,
        "number": "1",
        "type_name": "bus",
    }
    response = client.put("/routes/", json=data)
    response = client.get(f"/routes/{id}")
    assert response.status_code == 200
    assert response.json() == data


def test_route_read_all(client: TestClient):
    response = client.put("/types/", json={"name": "bus"})
    id = str(uuid7())
    data = {
        "id": id,
        "number": "1",
        "type_name": "bus",
    }
    response = client.put("/routes/", json=data)
    response = client.get("/routes/")
    assert response.status_code == 200
    assert response.json() == [data]


def test_route_update(client: TestClient):
    response = client.put("/types/", json={"name": "bus"})
    response = client.put("/types/", json={"name": "tram"})
    id = str(uuid7())
    data = {
        "id": id,
        "number": "1",
        "type_name": "bus",
    }
    response = client.put("/routes/", json=data)
    data = {
        "id": id,
        "number": "2",
        "type_name": "tram",
    }
    response = client.put("/routes/", json=data)
    assert response.status_code == 200
    assert response.json() == data
    response = client.get("/routes/")
    assert response.status_code == 200
    assert response.json() == [data]


def test_route_delete(client: TestClient):
    response = client.put("/types/", json={"name": "bus"})
    response = client.put("/types/", json={"name": "tram"})
    id = str(uuid7())
    data = {
        "id": id,
        "number": "1",
        "type_name": "bus",
    }
    response = client.put("/routes/", json=data)
    response = client.delete(f"/routes/{id}")
    assert response.status_code == 200
    assert response.json() == None
    response = client.get("/routes/")
    assert response.status_code == 200
    assert response.json() == []
