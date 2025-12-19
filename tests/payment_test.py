import pytest
from TRAVEL import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_payment_success(client):
    response = client.post('/payment', json={"card_number": "4111111111111111", "amount": 500})
    assert response.status_code == 200

# ----------------- EDGE CASES -----------------
def test_payment_negative_amount(client):
    response = client.post('/payment', json={"card_number": "4111111111111111", "amount": -100})
    assert response.status_code == 400

def test_payment_invalid_card(client):
    response = client.post('/payment', json={"card_number": "123", "amount": 500})
    assert response.status_code == 400

def test_payment_expired_card(client):
    response = client.post('/payment', json={"card_number": "4111111111111111", "expiry": "01/20", "amount": 500})
    assert response.status_code == 400

def test_payment_zero_amount(client):
    response = client.post('/payment', json={"card_number": "4111111111111111", "amount": 0})
    assert response.status_code == 400

def test_payment_unauthorized(client):
    response = client.post('/payment', json={"card_number": "4111111111111111", "amount": 500})
    assert response.status_code == 401