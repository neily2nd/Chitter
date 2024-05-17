import pytest
from app import app
from flask.testing import FlaskClient

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to Chitter!' in response.data

# Add more tests for other routes here


def test_register(client):
    response = client.post('/register', data=dict(
        username='test_user',
        email='test@example.com',
        password='password',
        name='Test User'
    ), follow_redirects=True)
    assert response.status_code == 200
    


def test_login(client):
    response = client.post('/login', data=dict(
        username='test_user',
        password='password'
    ), follow_redirects=True)
    assert response.status_code == 200
    

def test_logout(client):
    response = client.post('/logout', follow_redirects=True)
    assert response.status_code == 200
    
