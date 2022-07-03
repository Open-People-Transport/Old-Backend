import random
from uuid import UUID

from uuid_extensions import uuid7

from .test_nodes import test_create_node

URL = "/stops/"


def mock_stop(node, id=None):
    return {
        "id": id or str(uuid7()),
        "node_id": node["id"],
        "lat": random.randint(-90_0000000, 90_0000000) / 1_0000000,
        "lon": random.randint(-180_0000000, 180_0000000) / 1_0000000,
    }


def test_create_stop(client):
    node = test_create_node(client)
    data = mock_stop(node)
    response = client.put(URL, json=data)
    assert response.status_code == 200 and response.json() == data
    return data


def test_create_stop_without_id(client):
    node = test_create_node(client)
    data = mock_stop(node)
    del data["id"]
    response = client.put(URL, json=data)
    assert response.status_code == 200
    data["id"] = str(UUID(response.json()["id"]))
    assert response.json() == data


def test_read_stop(client):
    data = test_create_stop(client)
    response = client.get(URL + data["id"])
    assert response.status_code == 200 and response.json() == data


def test_read_stops(client):
    response = client.get(URL)
    assert response.status_code == 200 and response.json() == []
    data1 = test_create_stop(client)
    response = client.get(URL)
    assert response.status_code == 200 and response.json() == [data1]
    data2 = test_create_stop(client)
    response = client.get(URL)
    assert response.status_code == 200 and response.json() == [data1, data2]


def test_update_stop(client):
    data1 = test_create_stop(client)
    node2 = test_create_node(client)
    data2 = mock_stop(node2, id=data1["id"])
    response = client.put(URL, json=data2)
    assert response.status_code == 200 and response.json() == data2
    response = client.get(URL)
    assert response.status_code == 200 and response.json() == [data2]


def test_delete_stop(client):
    data = test_create_stop(client)
    response = client.delete(URL + data["id"])
    assert response.status_code == 200 and response.json() == None
    response = client.get(URL)
    assert response.status_code == 200 and response.json() == []
