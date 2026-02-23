from calendar import Day
from dataclasses import dataclass

from database.models import Booking


@dataclass
class FloorPlan:
    days: list[Day]

@dataclass
class Day:
    name: str
    halls: list[HallPlan]
    def __init__(self, name: str):
        self.name = name
        self.halls = []

@dataclass
class HallPlan:
    hall: Hall
    bookings: list[Booking]

@dataclass
class Hall:
    name: str
    size: int


AVAILABLE_HALLS = [Hall('Sporthalle 1', 12), Hall('Sporthalle 2', 12), Hall('Sporthalle 3', 12)]
EVENT_DAYS = [('Freitag (Tag 1)', 'first'), ('Samstag (Tag 2)', 'second')]


def generate_floor_plan(registrations: list[Booking]) -> FloorPlan:
    # first, group by number of days present, then by days
    to_be_assigned = registrations[:]
    to_be_assigned.sort(key=lambda b: b.second)
    to_be_assigned.sort(key=lambda b: b.duration, reverse=True)

    result = FloorPlan([])
    for day in EVENT_DAYS:
        day_plan = Day(day[0])
        available_halls = AVAILABLE_HALLS[:]
        tba_for_day = [booking for booking in to_be_assigned if getattr(booking, day[1])]
        while len(tba_for_day) > 0:
            hall = HallPlan(available_halls.pop(0), [])
            while len(hall.bookings) < hall.hall.size and len(tba_for_day) > 0:
                hall.bookings.append(tba_for_day.pop(0))
            day_plan.halls.append(hall)
        result.days.append(day_plan)

    return result