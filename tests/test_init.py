from time import time
from werkzeug.test import TestResponse
import pytest
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


def is_ok(response: TestResponse):
    return 200 <= response.status_code <= 399


def test_login_happy_admin(client):
    response = client.get('/login/eb1696dd-a9b5-4527-8768-71b91151aa19')
    assert is_ok(response) and 'Set-Cookie' in response.headers


def test_login_happy_admin_follow2dashboard(client):
    response = client.get('/login/eb1696dd-a9b5-4527-8768-71b91151aa19', follow_redirects=True)
    assert is_ok(response) and 'Anmeldungen dieses Jahr' in response.text


def test_login_happy_user(client):
    response = client.get('/login/166202eb-419c-4cef-af14-90b002347887')
    assert is_ok(response) and 'Set-Cookie' in response.headers


def test_login_happy_user_follow2dashboard(client):
    response = client.get('/login/166202eb-419c-4cef-af14-90b002347887', follow_redirects=True)
    assert is_ok(response) and 'Firma:' in response.text


def test_login_sad(client):
    response = client.get('/login/expired-or-invalid-token')
    assert response.status == '403 FORBIDDEN'


def test_login_stupid(client):
    response = client.get('/login')
    assert is_ok(response) and '<input' in response.text


def test_login_manual(client):
    response = client.post('/login', data=dict(token='eb1696dd-a9b5-4527-8768-71b91151aa19'))
    assert is_ok(response) and 'Set-Cookie' in response.headers


def test_register(client):
    response = client.post('/join', data=dict(name=f"Siegma.IT UG", contact_person="Siegmar Gabriel", email=f"siggi+{int(time())}@t-online.de"))
    assert is_ok(response)


def test_registration_form(client):
    response = client.get('/join')
    assert is_ok(response) and '<input' in response.text


def test_register_for_event_not_logged_in(client):
    response = client.post('/register', data=dict(tables_needed=1, chairs_needed=2))
    assert response.status_code == 302


def test_register_for_event_logged_in(client):
    _ = client.get('/login/166202eb-419c-4cef-af14-90b002347887')
    response = client.post('/register', data=dict(tables_needed=1, chairs_needed=2))
    assert is_ok(response)


def test_event_registration_form(client):
    _ = client.get('/login/166202eb-419c-4cef-af14-90b002347887')
    response = client.get('/register')
    assert is_ok(response) and '<input' in response.text


def test_index_is_just_a_page(client):
    response = client.get('/')
    assert response.status_code == 200


def test_invalid_user_bogus_id_negative_int_string():
    """load_user must not throw but meekly return None"""
    assert load_user('-1337') is None


def test_invalid_user_bogus_id_random_string():
    """load_user must not throw but meekly return None"""
    assert load_user('schnitzel') is None


def test_invalid_user_bogus_id_none():
    """load_user must not throw but meekly return None"""
    assert load_user(None) is None
