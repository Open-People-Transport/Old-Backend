import pytest

from .test_routes import test_route_created
from .test_stops import test_stop_created


def mock_route_stop(route, stop):
    return {
        "route_id": route["id"],
        "stop_id": stop["id"],
    }


def test_route_stop_created(client, route=None, stop=None):
    route = route or test_route_created(client)
    stop = stop or test_stop_created(client)
    data = mock_route_stop(route, stop)
    response = client.put(f"/routes/{data['route_id']}/stops/{data['stop_id']}")
    assert response.status_code == 200
    json = response.json()
    distance = json.pop("distance")
    assert isinstance(distance, int) and json == data
    return data | {"distance": distance}


def test_route_stop_read(client):
    data = test_route_stop_created(client)
    response = client.get(f"/routes/{data['route_id']}/stops/{data['stop_id']}")
    assert response.status_code == 200 and response.json() == data


@pytest.mark.skip(reason="/stops/.../routes/ endpoint not yet implemented")
def test_stop_route_read(client):
    data = test_route_stop_created(client)
    response = client.get(f"/stops/{data['stop_id']}/routes/{data['route_id']}")
    assert response.status_code == 200 and response.json() == data


def test_route_stops_listed(client):
    route = test_route_created(client)
    stop1 = test_stop_created(client)
    stop2 = test_stop_created(client)
    response = client.get(f"/routes/{route['id']}/stops/")
    assert response.status_code == 200 and response.json() == []
    data1 = test_route_stop_created(client, route, stop1)
    response = client.get(f"/routes/{route['id']}/stops/")
    assert response.status_code == 200 and response.json() == [data1]
    data2 = test_route_stop_created(client, route, stop2)
    response = client.get(f"/routes/{route['id']}/stops/")
    assert response.status_code == 200 and response.json() == [data1, data2]


@pytest.mark.skip(reason="/stops/.../routes/ endpoint not yet implemented")
def test_stop_routes_listed(client):
    stop = test_stop_created(client)
    route1 = test_route_created(client)
    route2 = test_route_created(client)
    response = client.get(f"/stops/{stop['id']}/routes/")
    assert response.status_code == 200 and response.json() == []
    data1 = test_route_stop_created(client, route1, stop)
    response = client.get(f"/stops/{stop['id']}/routes/")
    assert response.status_code == 200 and response.json() == [data1]
    data2 = test_route_stop_created(client, route2, stop)
    response = client.get(f"/stops/{stop['id']}/routes/")
    assert response.status_code == 200 and response.json() == [data1, data2]


def test_route_stop_deleted(client):
    data = test_route_stop_created(client)
    response = client.delete(f"/routes/{data['route_id']}/stops/{data['stop_id']}")
    assert response.status_code == 200 and response.json() == None
    response = client.get(f"/routes/{data['route_id']}/stops/")
    assert response.status_code == 200 and response.json() == []


@pytest.mark.skip(reason="/stops/.../routes/ endpoint not yet implemented")
def test_stop_routes_deleted(client):
    data = test_route_stop_created(client)
    response = client.delete(f"/stops/{data['stop_id']}/routes/{data['route_id']}")
    assert response.status_code == 200 and response.json() == None
    response = client.get(f"/stops/{data['stop_id']}/routes/")
    assert response.status_code == 200 and response.json() == []
