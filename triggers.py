"""
Ereignisse/Nebenwirkungen in der externen Umgebung
"""

from database.models import Booking


def notify_admins(booking: Booking) -> None:
    """
    Benachrichtige alle Veranstaltungsverwalter über eine neue Anmeldung
    :param booking: die neue Anmeldung
    :return: None
    """
    pass
