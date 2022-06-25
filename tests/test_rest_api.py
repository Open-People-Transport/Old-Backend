import random
from random import randrange
from string import ascii_letters, digits
from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from uuid_extensions import uuid7

from tests import conftest


def _type():
    return {
        "name": "".join(random.choice(ascii_letters) for _ in range(12)),
    }


def _route(_type):
    return {
        "id": str(uuid7()),
        "number": "".join(random.choice(digits) for _ in range(6)),
        "type_name": _type["name"],
    }


def _node():
    return {
        "id": str(uuid7()),
        "name": "".join(random.choice(ascii_letters) for _ in range(32)),
    }


@pytest.fixture
def type():
    return _type()


@pytest.fixture
def route(type):
    return _route(type)


@pytest.fixture
def node():
    return _node()


def test_database_connection(session: Session):
    pass


def test_client_launch(client: TestClient):
    pass


def test_type_create(client: TestClient, type):
    response = client.put("/types/", json=type)
    assert response.status_code == 200
    assert response.json() == type


def test_type_read(client: TestClient, type):
    response = client.put("/types/", json=type)
    response = client.get("/types/" + type["name"])
    assert response.status_code == 200
    assert response.json() == type


def test_type_read_all(client: TestClient, type):
    response = client.put("/types/", json=type)
    response = client.get("/types/")
    assert response.status_code == 200
    assert response.json() == [type]


def test_type_update(client: TestClient, type):
    response = client.put("/types/", json=type)
    old_name = type["name"]
    type = _type()
    response = client.put("/types/" + old_name, json=type)
    assert response.status_code == 200
    assert response.json() == type
    response = client.get("/types/")
    assert response.json() == [type]


def test_type_delete(client: TestClient, type):
    response = client.put("/types/", json=type)
    response = client.delete("/types/" + type["name"])
    assert response.status_code == 200
    assert response.json() == None
    response = client.get("/types/")
    assert response.json() == []


def test_route_create_with_id(client: TestClient, type, route):
    response = client.put("/types/", json=type)
    response = client.put("/routes/", json=route)
    assert response.status_code == 200
    assert response.json() == route


def test_route_create_without_id(client: TestClient, type, route):
    del route["id"]
    response = client.put("/types/", json=type)
    response = client.put("/routes/", json=route)
    assert response.status_code == 200
    route["id"] = str(UUID(response.json()["id"]))
    assert response.json() == route


def test_route_read(client: TestClient, type, route):
    response = client.put("/types/", json=type)
    response = client.put("/routes/", json=route)
    response = client.get("/routes/" + route["id"])
    assert response.status_code == 200
    assert response.json() == route


def test_route_read_all(client: TestClient, type, route):
    response = client.put("/types/", json=type)
    response = client.put("/routes/", json=route)
    response = client.get("/routes/")
    assert response.status_code == 200
    assert response.json() == [route]


def test_route_update(client: TestClient, type, route):
    type2 = _type()
    route2 = _route(type2)
    route2["id"] = route["id"]
    response = client.put("/types/", json=type)
    response = client.put("/types/", json=type2)
    response = client.put("/routes/", json=route)
    response = client.put("/routes/", json=route2)
    assert response.status_code == 200
    assert response.json() == route2
    response = client.get("/routes/")
    assert response.status_code == 200
    assert response.json() == [route2]


def test_route_delete(client: TestClient, type, route):
    response = client.put("/types/", json=type)
    response = client.put("/routes/", json=route)
    response = client.delete(f"/routes/" + route["id"])
    assert response.status_code == 200
    assert response.json() == None
    response = client.get("/routes/")
    assert response.status_code == 200
    assert response.json() == []


def test_node_create_with_id(client: TestClient, node):
    response = client.put("/nodes/", json=node)
    assert response.status_code == 200
    assert response.json() == node


def test_node_create_without_id(client: TestClient, node):
    del node["id"]
    response = client.put("/nodes/", json=node)
    assert response.status_code == 200
    node["id"] = str(UUID(response.json()["id"]))
    assert response.json() == node


def test_node_read(client: TestClient, node):
    response = client.put("/nodes/", json=node)
    response = client.get("/nodes/" + node["id"])
    assert response.status_code == 200
    assert response.json() == node


def test_node_read_all(client: TestClient, node):
    response = client.put("/nodes/", json=node)
    response = client.get("/nodes/")
    assert response.status_code == 200
    assert response.json() == [node]


def test_node_update(client: TestClient, node):
    node2 = _node()
    node2["id"] = node["id"]
    response = client.put("/nodes/", json=node)
    response = client.put("/nodes/", json=node2)
    assert response.status_code == 200
    assert response.json() == node2
    response = client.get("/nodes/")
    assert response.status_code == 200
    assert response.json() == [node2]


def test_node_delete(client: TestClient, node):
    response = client.put("/nodes/", json=node)
    response = client.delete(f"/nodes/" + node["id"])
    assert response.status_code == 200
    assert response.json() == None
    response = client.get("/nodes/")
    assert response.status_code == 200
    assert response.json() == []
