import pytest
from input import validate_booking, transform_filters, ConstraintViolation


def test_validate_booking_transforms_correctly_yes_no():
    result = validate_booking(user_id=1, first_day='yes')
    assert result.first
    assert not result.second


def test_validate_booking_transforms_correctly_no_yes():
    result = validate_booking(user_id=1, second_day='yes')
    assert not result.first
    assert result.second


def test_validate_booking_transforms_correctly_both():
    result = validate_booking(user_id=1, first_day='yes', second_day='yes')
    assert result.first and result.second


def test_validate_booking_transforms_correctly_no_no():
    with pytest.raises(ConstraintViolation):
        validate_booking(user_id=5)


def test_transform_filters_empty():
    result = transform_filters({})
    assert result == {}


def test_transform_filters_only_filters_on_all():
    result = transform_filters({'status': 'all', 'day': 'all', 'industry': 'all'})
    assert result == {}


def test_transform_filters_actual_filters():
    result = transform_filters({'status': 'accepted', 'day': 'both'})
    assert result == {'status': 'accepted', 'first': True, 'second': True}


def test_transform_filters_actual_filters_strip_industry():
    result = transform_filters({'status': 'accepted', 'day': 'both', 'industry': 'cybersec'})
    assert result == {'status': 'accepted', 'first': True, 'second': True}
