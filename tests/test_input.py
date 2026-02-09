import pytest
from input import validate_booking, transform_filters


def test_validate_booking_strip_form_fields():
    with pytest.raises(KeyError):
        validate_booking()


def test_transform_filters_empty():
    result = transform_filters({})
    assert result == {}


def test_transform_filters_only_filters_on_all():
    result = transform_filters({'status': 'all', 'day': 'all', 'industry': 'all'})
    assert result == {}


def test_transform_filters_actual_filters():
    result = transform_filters({'status': 'accepted', 'day': 'both'})
    assert result == {'status': 'accepted', 'first': True, 'second': True}
