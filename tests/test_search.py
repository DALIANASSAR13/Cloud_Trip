import pytest
from TRAVEL import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_search_get(client):
    """Test GET request returns the search page"""
    response = client.get("/search")
    assert response.status_code == 200
    assert b"<form" in response.data

def test_search_post_allowed_countries(client, monkeypatch):
    """Test POST request returns flights only for allowed countries"""

    allowed_countries = ["Japan", "Switzerland", "Italy", "Turkey"]

    class MockCursor:
        def execute(self, query, params):
            from_city, to_city = params
            assert any(country in from_city for country in allowed_countries)
            assert any(country in to_city for country in allowed_countries)

        def fetchall(self):
            return [
                (1, "Test Airline", "Test Airline", "Japan", "Turkey", "2025-12-17 12:00", "2025-12-17 14:00", "2h", 500)
            ]

        def close(self):
            pass

    class MockConnection:
        def cursor(self):
            return MockCursor()
        def close(self):
            pass

    monkeypatch.setattr("Database.get_db_connection", lambda: MockConnection())

    response = client.post("/search", data={"from_city": "Japan", "to_city": "Turkey"})

    assert response.status_code == 200
    assert b"Test Airline" in response.data
    assert b"Japan" in response.data
    assert b"Turkey" in response.data