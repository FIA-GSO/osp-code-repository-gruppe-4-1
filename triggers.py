"""
Ereignisse/Nebenwirkungen in der externen Umgebung
"""

from database.models import Booking, User, Correspondence
from db import db
from log import logger


def notify_admins(event: Booking | Correspondence) -> None:
    """
    Benachrichtige alle Veranstaltungsverwalter über eine neue Anmeldung oder Anfrage
    eines Ausstellers
    :param event: die neue Anmeldung oder Anfrage
    :return: None
    """
    message = stringify(event)

    logger.info(message)

    admins = db.query(User).filter_by(is_admin=True).all()
    for admin in admins:
        # this should be an actual notification, here we just log instead
        logger.debug("Notifying admin '%s/%s': %s" % (admin.name, admin.contact_person, message))


def stringify(event: Booking|Correspondence) -> str:
    """
    Format ein ereignisbeschreibendes Datenobjekt
    :param event: Das ereignisbeschreibende Datenobjekt
    :return: die formatierte Zeichenkette
    """
    if isinstance(event, Booking):
        return f'Neue Anmeldung: {event}'
    else:
        return f'{event.sender.name}/{event.sender.contact_person} fragt an: {event.message}'
