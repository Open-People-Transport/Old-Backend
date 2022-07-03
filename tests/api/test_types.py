import random
from string import ascii_letters

URL = "/types/"


def mock_type():
    return {
        "name": "".join(random.choice(ascii_letters) for _ in range(12)),
    }


def test_create_type(client):
    data = mock_type()
    response = client.put(URL, json=data)
    assert response.status_code == 200 and response.json() == data
    return data


def test_read_type(client):
    data = test_create_type(client)
    response = client.get(URL + data["name"])
    assert response.status_code == 200 and response.json() == data


def test_read_types(client):
    response = client.get(URL)
    assert response.status_code == 200 and response.json() == []
    data1 = test_create_type(client)
    response = client.get(URL)
    assert response.status_code == 200 and response.json() == [data1]
    data2 = test_create_type(client)
    response = client.get(URL)
    assert response.status_code == 200 and response.json() == [data1, data2]


def test_update_type(client):
    data1 = test_create_type(client)
    data2 = mock_type()
    response = client.put(URL + data1["name"], json=data2)
    assert response.status_code == 200 and response.json() == data2
    response = client.get(URL)
    assert response.status_code == 200 and response.json() == [data2]


def test_delete_type(client):
    data = test_create_type(client)
    response = client.delete(URL + data["name"])
    assert response.status_code == 200 and response.json() == None
    response = client.get(URL)
    assert response.status_code == 200 and response.json() == []
