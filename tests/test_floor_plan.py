import pytest
from random import randint, choice

from database.models import Booking
from db import decorate
from floor_plan import generate_floor_plan, FloorPlan

BOOKINGS = [
    Booking(user_id=randint(1, 2048))
]

def random_booking():
    return decorate(Booking(user_id=randint(1, 2048), first=choice([True, False]), second=choice([True, False])));


def pytest_generate_tests(metafunc):
    if "bookings" in metafunc.fixturenames:
        metafunc.parametrize("bookings", [
            [random_booking() for _ in
             range(randint(1, 36))]
            for _ in range(1024)
        ])


def does_not_need_to_move(booking: Booking, plan: FloorPlan):
    days = plan.days[:]
    first_day_hall = \
    [hall_assignment.hall for hall_assignment in days.pop(0).halls if booking in hall_assignment.bookings][0]
    for other_day in days:
        if not any(hall_assignment.hall == first_day_hall for hall_assignment in other_day.halls if
                   booking in hall_assignment.bookings) or \
               any(hall_assignment.hall != first_day_hall for hall_assignment in other_day.halls if
                       booking in hall_assignment.bookings):
            return False
    return True


def test_floor_plan_does_not_make_extended_term_exhibitors_move(bookings):
    plan = generate_floor_plan(bookings)
    long_term_exhibitors = [exhibitor for exhibitor in bookings if exhibitor.first and exhibitor.second]
    for lte in long_term_exhibitors:
        assert does_not_need_to_move(lte, plan)


def test_validate_predicate():

    plan = FloorPlan([

    ])


if __name__ == '__main__':
    pytest.main()
