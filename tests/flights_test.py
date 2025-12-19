import pytest
from TRAVEL import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_search_flights_success(client):
    response = client.post('/search-flights', json={"departure": "Switzerland", "arrival": "Japan", "date": "2025-12-25"})
    assert response.status_code == 200
    assert isinstance(response.json, list)

# ----------------- EDGE CASES -----------------
def test_search_empty(client):
    response = client.post('/search-flights', json={})
    assert response.status_code == 400

def test_search_same_departure_arrival(client):
    response = client.post('/search-flights', json={"departure": "Italy", "arrival": "Italy", "date": "2025-12-25"})
    assert response.status_code == 400

def test_search_past_date(client):
    response = client.post('/search-flights', json={"departure": "Turkey", "arrival": "Japan", "date": "2020-01-01"})
    assert response.status_code == 400

def test_search_no_flights(client):
    response = client.post('/search-flights', json={"departure": "Switzerland", "arrival": "Brazil", "date": "2025-12-25"})
    assert response.status_code == 200
    assert response.json == []