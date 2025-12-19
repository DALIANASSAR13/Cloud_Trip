import pytest
from TRAVEL import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_signup_success(client):
    response = client.post('/signup', json={"email": "newuser@test.com", "password": "12345"})
    assert response.status_code == 201

def test_login_success(client):
    response = client.post('/login', json={"email": "newuser@test.com", "password": "12345"})
    assert response.status_code == 200

# ----------------- EDGE CASES -----------------
def test_signup_empty_fields(client):
    response = client.post('/signup', json={"email": "", "password": ""})
    assert response.status_code == 400

def test_signup_existing_email(client):
    response = client.post('/signup', json={"email": "existing@test.com", "password": "12345"})
    assert response.status_code == 409

def test_signup_invalid_email(client):
    response = client.post('/signup', json={"email": "invalidemail", "password": "12345"})
    assert response.status_code == 400

def test_login_empty_fields(client):
    response = client.post('/login', json={"email": "", "password": ""})
    assert response.status_code == 400

def test_login_wrong_password(client):
    response = client.post('/login', json={"email": "test@test.com", "password": "wrong"})
    assert response.status_code == 401

def test_login_nonexistent_user(client):
    response = client.post('/login', json={"email": "noone@test.com", "password": "12345"})
    assert response.status_code == 404