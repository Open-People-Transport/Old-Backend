import random
from string import ascii_letters
from uuid import UUID

from uuid_extensions import uuid7

URL = "/nodes/"


def mock_node(id=None):
    return {
        "id": id or str(uuid7()),
        "name": "".join(random.choice(ascii_letters) for _ in range(32)),
    }


def test_node_created(client):
    data = mock_node()
    response = client.put(URL, json=data)
    assert response.status_code == 200 and response.json() == data
    return data


def test_node_created_without_id(client):
    data = mock_node()
    del data["id"]
    response = client.put(URL, json=data)
    assert response.status_code == 200
    data["id"] = str(UUID(response.json()["id"]))
    assert response.json() == data


def test_node_read(client):
    data = test_node_created(client)
    response = client.get(URL + data["id"])
    assert response.status_code == 200 and response.json() == data


def test_nodes_listed(client):
    response = client.get(URL)
    assert response.status_code == 200 and response.json() == []
    data1 = test_node_created(client)
    response = client.get(URL)
    assert response.status_code == 200 and response.json() == [data1]
    data2 = test_node_created(client)
    response = client.get(URL)
    assert response.status_code == 200 and response.json() == [data1, data2]


def test_node_updated(client):
    data1 = test_node_created(client)
    data2 = mock_node(id=data1["id"])
    response = client.put(URL, json=data2)
    assert response.status_code == 200 and response.json() == data2
    response = client.get(URL)
    assert response.status_code == 200 and response.json() == [data2]


def test_node_deleted(client):
    data = test_node_created(client)
    response = client.delete(URL + data["id"])
    assert response.status_code == 200 and response.json() == None
    response = client.get(URL)
    assert response.status_code == 200 and response.json() == []
