import pytest

from triggers import notify_admins, logger
from database.models import Booking


TEST_BOOKING = Booking(user_id=1, event_year=2025, first=True, second=True, chairs_needed=2, tables_needed=1, presentation='Erfolgreich TDD vortäuschen')


def test_notification(mocker):
    log = mocker.spy(logger, '_log')
    info = mocker.spy(logger, 'info')
    debug = mocker.spy(logger, 'debug')

    notify_admins(TEST_BOOKING)

    log.assert_called() # called #admins + 1 times
    info.assert_called_once()
    debug.assert_called() # times #admins


if __name__ == '__main__':
    pytest.main()
