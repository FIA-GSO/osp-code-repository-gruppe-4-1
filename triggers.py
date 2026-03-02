"""
Ereignisse/Nebenwirkungen in der externen Umgebung
"""

import logging
from logging.handlers import RotatingFileHandler, SysLogHandler

from database.models import Booking, User
from db import db


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

syslog_handler = SysLogHandler(address='/dev/log')
logger.addHandler(syslog_handler)

from os import makedirs
makedirs('logs', exist_ok=True)
file_handler = RotatingFileHandler('logs/triggers.log')
logger.addHandler(file_handler)


def notify_admins(booking: Booking) -> None:
    """
    Benachrichtige alle Veranstaltungsverwalter über eine neue Anmeldung
    :param booking: die neue Anmeldung
    :return: None
    """
    message = f'Neue Anmeldung: {booking}'

    logger.info(message)

    admins = db.query(User).filter_by(is_admin=True).all()
    for admin in admins:
        # this should be an actual notification, here we just log instead
        logger.debug(f"Notifying admin '{admin.name}/{admin.contact_person}': {message}")
