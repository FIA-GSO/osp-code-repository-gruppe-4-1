import pytest

from database.models import Booking, BookingStatus
from db import get_bookings, db
from export import export_floor_plan, export_registrations
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


### TESTS (EXPORTS) ###


def test_export_floor_plan_empty_data():
    """Test floor plan export with empty form data"""
    result = export_floor_plan({})
    
    assert isinstance(result, str)
    assert len(result) > 0


def test_export_floor_plan_with_day_filter():
    """Test floor plan export with day filter"""
    form_data = {'day': 'first'}
    result = export_floor_plan(form_data)
    
    assert isinstance(result, str)
    assert len(result) > 0


def test_export_floor_plan_contains_headers():
    """Test floor plan export contains expected CSV headers"""
    result = export_floor_plan({})
    
    assert "Firma;Ansprechpartner;Branche;Benötigte Stühle;Benötigte Tische" in result


def test_export_floor_plan_contains_totals():
    """Test floor plan export contains total rows"""
    result = export_floor_plan({})
    
    assert "Gesamt:" in result


def test_export_floor_plan_all_days():
    """Test floor plan export with all days"""
    form_data = {'day': 'all'}
    result = export_floor_plan(form_data)
    
    assert isinstance(result, str)
    assert len(result) > 0


def test_export_registrations_empty_data():
    """Test registrations export with empty form data"""
    result = export_registrations({})
    
    assert isinstance(result, str)
    assert len(result) > 0


def test_export_registrations_with_filters():
    """Test registrations export with filters"""
    form_data = {'status': 'accepted', 'day': 'first'}
    result = export_registrations(form_data)
    
    assert isinstance(result, str)
    assert len(result) > 0


def test_export_registrations_contains_headers():
    """Test registrations export contains expected CSV headers"""
    result = export_registrations({})
    
    expected_headers = "Firma;Ansprechpartner;Branche;Anzahl Tage;Tag 1;Tag 2;Status;Stühle;Tische"
    assert expected_headers in result


def test_export_registrations_contains_count():
    """Test registrations export contains registration count"""
    result = export_registrations({})
    
    assert "Anmeldungen:" in result


def test_export_registrations_status_filter():
    """Test registrations export with status filter"""
    form_data = {'status': 'pending'}
    result = export_registrations(form_data)
    
    assert isinstance(result, str)
    assert len(result) > 0

if __name__ == '__main__':
    pytest.main()
