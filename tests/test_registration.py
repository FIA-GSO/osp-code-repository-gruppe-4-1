from time import time

import pytest

from app import app
from tests.test_init import is_ok


@pytest.fixture
def client():
    app.config['TESTING'] = True
    yield app.test_client()


def test_register_user_invalid_data_in_fields(client):
    response = client.post('/join', data={
        'name': 'Laden',
        'contact_person': 'DvD',
        'email': f'chef+{time()}@la.den',
        'support_association': 'on',
        'dsgvo': 'maybe' # <- maybe is not a valid value
    }, follow_redirects=True)
    assert 'notification-error' in response.text


def test_register_user_missing_fields(client):
    response = client.post('/join', data={
        'name': 'Laden',
        'contact_person': 'Donald Duck'
    }, follow_redirects=True)
    assert 'notification-error' in response.text


def test_register_user_valid_and_complete_data(client):
    response = client.post('/join', data={
        'name': 'Laden',
        'contact_person': 'DvD',
        'email': f'chef+{time()}@la.den',
        'support_association': 'on',
        'dsgvo': 'yes',
        'street': 'Amselweg 9',
        'zip': '10010',
        'city': 'Dingenskirchen'
    }, follow_redirects=True)

    assert is_ok(response) and 'notification-error' not in response.text and 'notification-info' in response.text and 'Token' in response.text
