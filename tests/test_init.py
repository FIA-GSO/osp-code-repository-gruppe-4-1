from time import time

import pytest
import random
from app import app as flask_app, load_user


@pytest.fixture()
def app():
    flask_app.config.update({
        "TESTING": True,
    })
    # other setup can go here
    yield flask_app
    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


def test_login_happy(client):
    response = client.get('/login/eb1696dd-a9b5-4527-8768-71b91151aa19')
    assert response.status == '200 OK' and 'Set-Cookie' in response.headers


def test_login_sad(client):
    response = client.get('/login/expired-or-invalid-token')
    assert response.status == '403 FORBIDDEN'


def test_login_stupid(client):
    response = client.get('/login')
    assert response.status == '200 OK' and '<input' in response.text


def test_login_manual(client):
    response = client.post('/login', data=dict(token='eb1696dd-a9b5-4527-8768-71b91151aa19'))
    assert response.status == '200 OK' and 'Set-Cookie' in response.headers


def test_register(client):
    response = client.post('/register', data=dict(name=f"Siegma.IT UG", contact_person="Siegmar Gabriel", email=f"siggi+{int(time())}@t-online.de"))
    assert response.status == '200 OK'


def test_registration_form(client):
    response = client.get('/register')
    assert response.status == '200 OK' and '<input' in response.text


def test_index(client):
    response = client.get('/')
    assert response.status == '302 FOUND' and "Redirect" in response.text


def test_invalid_user_bogus_id_negative_int_string():
    """load_user must not throw but meekly return None"""
    assert load_user('-1337') is None


def test_invalid_user_bogus_id_random_string():
    """load_user must not throw but meekly return None"""
    assert load_user('schnitzel') is None


def test_invalid_user_bogus_id_none():
    """load_user must not throw but meekly return None"""
    assert load_user(None) is None
