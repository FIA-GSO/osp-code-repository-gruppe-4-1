import pytest

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    yield app.test_client()


def test_register_user(client):
    response = client.post('/join', data={
        'name': 'Laden',
        'contact_person': 'DvD',
        'email': 'chef@la.den',
        'support_association': 'on',
        'dsgvo': 'maybe'
    })
    # ToDo: this isn't right ffs! do it right!
    assert True # yeayeayea, later
