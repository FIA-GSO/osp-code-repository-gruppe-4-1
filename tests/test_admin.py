import pytest

from database.models import Booking, BookingStatus
from db import get_bookings, db
from tests import test_init


client = test_init.client
app = test_init.app
booking_id = 1


@pytest.fixture
def admin_client(client):
    client.get('/login/eb1696dd-a9b5-4527-8768-71b91151aa19')
    reset_booking()
    assert get_booking(booking_id).status == BookingStatus.pending
    yield client


def get_booking(bid: int = booking_id) -> Booking:
    return get_bookings(id=bid).pop()


def reset_booking(bid: int = booking_id):
    db.query(Booking).filter_by(id=bid).update({'status': BookingStatus.pending})
    db.commit()


### TESTS (AUTH) ###


def test_must_be_logged_in(client):
    response = client.get(f'/admin/booking/{booking_id}/confirm')
    assert response.status_code == 302


def test_must_be_admin(client):
    client.get('/login/166202eb-419c-4cef-af14-90b002347887')
    response = client.get(f'/admin/booking/{booking_id}/confirm')
    assert response.status_code == 302


### TESTS (ACTIONS) ###


def test_admin_approve_registration(admin_client):
    admin_client.get(f'/admin/booking/{booking_id}/confirm')
    assert get_booking().status == BookingStatus.accepted
    reset_booking()


def test_admin_reject_registration(admin_client):
    admin_client.get(f'/admin/booking/{booking_id}/reject')
    assert get_booking().status == BookingStatus.rejected
    reset_booking()


if __name__ == '__main__':
    pytest.main()
