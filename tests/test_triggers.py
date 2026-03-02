from logging.handlers import SysLogHandler

import pytest
from pytest_mock import mocker


# Ohmigod, this is so ugly...
_syslog_handler = None
_notify_admins = None

@pytest.fixture(autouse=True)
def prepare(mocker):
    mocker.patch('sys.platform', 'linux')
    global _syslog_handler, _notify_admins
    from triggers import notify_admins, syslog_handler
    _syslog_handler = syslog_handler
    _notify_admins = notify_admins
    yield


from database.models import Booking


TEST_BOOKING = Booking(user_id=1, event_year=2025, first=True, second=True, chairs_needed=2, tables_needed=1, presentation='Erfolgreich TDD vortäuschen')


def test_notification(mocker):
    spy = mocker.spy(_syslog_handler, 'emit')

    _notify_admins(TEST_BOOKING)

    spy.assert_called()


if __name__ == '__main__':
    pytest.main()
