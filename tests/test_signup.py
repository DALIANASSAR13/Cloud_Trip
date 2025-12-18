import pytest
from TRAVEL import app as flask_app

@pytest.fixture
def client():
    flask_app.config.update({
        "TESTING": True
    })
    with flask_app.test_client() as client:
        yield client

class FakeCursor:
    def __init__(self, exists=False):
        self.exists = exists
        self.result = None

    def execute(self, query, params=None):
        if "SELECT user_id" in query:
            self.result = (1,) if self.exists else None
        elif "INSERT INTO users_data" in query:
            self.result = (123,)

    def fetchone(self):
        return self.result

    def close(self):
        pass

class FakeConn:
    def __init__(self, exists=False):
        self.exists = exists

    def cursor(self):
        return FakeCursor(self.exists)

    def commit(self):
        pass

    def close(self):
        pass

def test_signup_success(client, monkeypatch):
    """Test successful signup"""

    monkeypatch.setattr("TRAVEL.get_db_connection", lambda: FakeConn(exists=False))

    response = client.post("/signup", data={
        "first_name": "Yomna",
        "last_name": "Medhat",
        "email": "yomna@example.com",
        "password": "Password123"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"index.html" in response.data or b"Yomna" in response.data

def test_signup_missing_fields(client):
    """Test signup with missing fields"""

    response = client.post("/signup", data={
        "first_name": "",
        "email": "",
        "password": ""
    })

    assert b"All fields are required!" in response.data

def test_signup_existing_email(client, monkeypatch):
    """Test signup with an existing email"""

    monkeypatch.setattr("TRAVEL.get_db_connection", lambda: FakeConn(exists=True))

    response = client.post("/signup", data={
        "first_name": "Yomna",
        "last_name": "Medhat",
        "email": "existing@example.com",
        "password": "Password123"
    })

    assert b"Email already registered!" in response.data