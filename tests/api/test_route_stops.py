import pytest

from .test_routes import test_create_route
from .test_stops import test_create_stop


def mock_route_stop(route, stop):
    return {
        "route_id": route["id"],
        "stop_id": stop["id"],
    }


def test_create_route_stop(client, route=None, stop=None):
    route = route or test_create_route(client)
    stop = stop or test_create_stop(client)
    data = mock_route_stop(route, stop)
    response = client.put(f"/routes/{data['route_id']}/stops/{data['stop_id']}")
    assert response.status_code == 200
    json = response.json()
    distance = json.pop("distance")
    assert isinstance(distance, int) and json == data
    return data | {"distance": distance}


def test_read_route_stop(client):
    data = test_create_route_stop(client)
    response = client.get(f"/routes/{data['route_id']}/stops/{data['stop_id']}")
    assert response.status_code == 200 and response.json() == data


@pytest.mark.skip(reason="/stops/.../routes/ endpoint not yet implemented")
def test_read_stop_route(client):
    data = test_create_route_stop(client)
    response = client.get(f"/stops/{data['stop_id']}/routes/{data['route_id']}")
    assert response.status_code == 200 and response.json() == data


def test_read_route_stops(client):
    route = test_create_route(client)
    stop1 = test_create_stop(client)
    stop2 = test_create_stop(client)
    response = client.get(f"/routes/{route['id']}/stops/")
    assert response.status_code == 200 and response.json() == []
    data1 = test_create_route_stop(client, route, stop1)
    response = client.get(f"/routes/{route['id']}/stops/")
    assert response.status_code == 200 and response.json() == [data1]
    data2 = test_create_route_stop(client, route, stop2)
    response = client.get(f"/routes/{route['id']}/stops/")
    assert response.status_code == 200 and response.json() == [data1, data2]


@pytest.mark.skip(reason="/stops/.../routes/ endpoint not yet implemented")
def test_read_stop_routes(client):
    stop = test_create_stop(client)
    route1 = test_create_route(client)
    route2 = test_create_route(client)
    response = client.get(f"/stops/{stop['id']}/routes/")
    assert response.status_code == 200 and response.json() == []
    data1 = test_create_route_stop(client, route1, stop)
    response = client.get(f"/stops/{stop['id']}/routes/")
    assert response.status_code == 200 and response.json() == [data1]
    data2 = test_create_route_stop(client, route2, stop)
    response = client.get(f"/stops/{stop['id']}/routes/")
    assert response.status_code == 200 and response.json() == [data1, data2]


def test_delete_route_stop(client):
    data = test_create_route_stop(client)
    response = client.delete(f"/routes/{data['route_id']}/stops/{data['stop_id']}")
    assert response.status_code == 200 and response.json() == None
    response = client.get(f"/routes/{data['route_id']}/stops/")
    assert response.status_code == 200 and response.json() == []


@pytest.mark.skip(reason="/stops/.../routes/ endpoint not yet implemented")
def test_delete_stop_route(client):
    data = test_create_route_stop(client)
    response = client.delete(f"/stops/{data['stop_id']}/routes/{data['route_id']}")
    assert response.status_code == 200 and response.json() == None
    response = client.get(f"/stops/{data['stop_id']}/routes/")
    assert response.status_code == 200 and response.json() == []
