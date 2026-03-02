import pytest

from database.models import BookingStatus
from db import get_bookings
from tests import test_init

client = test_init.client
app = test_init.app

booking_id = 2


@pytest.fixture
def logged_in_client(client):
    _ = client.get('/login/166202eb-419c-4cef-af14-90b002347887') # user 2 has booking 2 and this token
    return client


def test_raise_issue(logged_in_client):
    unsinn = "Mama? Bist du's?"
    logged_in_client.post('/dashboard/message', data={ 'message': unsinn })

    booking = get_bookings(id=booking_id).pop()
    assert booking.needs_response
    issue = booking.correspondence.pop()
    assert not issue.from_admin
    assert issue.message == unsinn


if __name__ == '__main__':
    pytest.main()
