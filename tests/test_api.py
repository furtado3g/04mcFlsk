import pytest
from app import app, db
from entities.user import AuthUser, User
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()

def test_register_user(client):
    resp = client.post('/api/v1/register', json={
        'username': 'testuser',
        'password': 'testpass'
    })
    assert resp.status_code == 201
    assert b'Novo usu' in resp.data

def test_register_duplicate_user(client):
    client.post('/api/v1/register', json={
        'username': 'testuser',
        'password': 'testpass'
    })
    resp = client.post('/api/v1/register', json={
        'username': 'testuser',
        'password': 'testpass'
    })
    assert resp.status_code == 409

def test_login_user(client):
    client.post('/api/v1/register', json={
        'username': 'testuser',
        'password': 'testpass'
    })
    resp = client.post('/api/v1/login', headers={
        'Authorization': 'Basic dGVzdHVzZXI6dGVzdHBhc3M='
    })
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert 'token' in data
