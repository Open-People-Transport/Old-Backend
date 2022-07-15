import random
from string import digits
from uuid import UUID

from uuid_extensions import uuid7

from .test_types import test_create_type

URL = "/routes/"


def mock_route(type, id=None):
    return {
        "id": id or str(uuid7()),
        "number": "".join(random.choice(digits) for _ in range(6)),
        "type_id": type["id"],
    }


def test_create_route(client):
    type = test_create_type(client)
    data = mock_route(type)
    response = client.put(URL, json=data)
    assert response.status_code == 200 and response.json() == data
    return data


def test_create_route_without_id(client):
    type = test_create_type(client)
    data = mock_route(type)
    del data["id"]
    response = client.put(URL, json=data)
    assert response.status_code == 200
    data["id"] = str(UUID(response.json()["id"]))
    assert response.json() == data


def test_read_route(client):
    data = test_create_route(client)
    response = client.get(URL + data["id"])
    assert response.status_code == 200 and response.json() == data


def test_read_routes(client):
    response = client.get(URL)
    assert response.status_code == 200 and response.json() == []
    data1 = test_create_route(client)
    response = client.get(URL)
    assert response.status_code == 200 and response.json() == [data1]
    data2 = test_create_route(client)
    response = client.get(URL)
    assert response.status_code == 200 and response.json() == [data1, data2]


def test_update_route(client):
    data1 = test_create_route(client)
    type2 = test_create_type(client)
    data2 = mock_route(type2, id=data1["id"])
    response = client.put(URL, json=data2)
    assert response.status_code == 200 and response.json() == data2
    response = client.get(URL)
    assert response.status_code == 200 and response.json() == [data2]


def test_delete_route(client):
    data = test_create_route(client)
    response = client.delete(URL + data["id"])
    assert response.status_code == 200 and response.json() == None
    response = client.get(URL)
    assert response.status_code == 200 and response.json() == []
