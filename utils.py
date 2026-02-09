""""""

from dataclasses import dataclass


class NotificationType:
    """
    Ein Pseudo-Enum an Hinweistypen.
    """
    error = "error"
    warning = "warning"
    info = "info"
    success = "success"


@dataclass
class Notification:
    """
    Eine Benachrichtigung für den Nutzer (Record-/Datenklasse)
    """
    type: str
    message: str
