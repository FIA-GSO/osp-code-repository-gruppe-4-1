from dataclasses import dataclass


# @pretend_enum
class NotificationType:
    error = "error"
    warning = "warning"
    info = "info"
    success = "success"


@dataclass
class Notification:
    type: str
    message: str
