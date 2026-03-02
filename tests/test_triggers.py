import pytest

from triggers import notify_admins, syslog_handler
from database.models import Booking


TEST_BOOKING = Booking(user_id=1, event_year=2025, first=True, second=True, chairs_needed=2, tables_needed=1, presentation='Erfolgreich TDD vortäuschen')


def test_notification(mocker):
    spy = mocker.spy(syslog_handler, 'emit')

    notify_admins(TEST_BOOKING)

    spy.assert_called()


if __name__ == '__main__':
    pytest.main()
