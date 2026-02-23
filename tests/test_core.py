from db import calculate_furniture_totals
from database.models import BookingStatus


def test_calculate_furniture_totals():
    result = calculate_furniture_totals(event_year=2024, status=BookingStatus.accepted)
    assert 'total_chairs' in result and 'total_tables' in result
    assert isinstance(result['total_chairs'], int) and isinstance(result['total_tables'], int)
    assert result['total_chairs'] == 6 and result['total_tables'] == 2