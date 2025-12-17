import pytest
from TRAVEL import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_payment_not_logged_in(client):
    """User must be logged in to pay"""
    response = client.post(
        "/process_payment",
        json={"flight_id": 1, "travellers": 2}
    )

    assert response.status_code == 401
    assert response.json["success"] is False


def test_payment_success(client, monkeypatch):
    """Payment succeeds and total is calculated correctly"""

    class MockCursor:
        def execute(self, query, params):
            assert params[2] == 1000

        def close(self):
            pass

    class MockConnection:
        def cursor(self):
            return MockCursor()
        def commit(self):
            pass
        def close(self):
            pass

    monkeypatch.setattr(
        "Database.get_db_connection",
        lambda: MockConnection()
    )

    with client.session_transaction() as session:
        session["user_id"] = 1

    response = client.post(
        "/process_payment",
        json={"flight_id": 1, "travellers": 2}
    )

    assert response.status_code == 200
    assert response.json["success"] is True
    assert response.json["total"] == 1000