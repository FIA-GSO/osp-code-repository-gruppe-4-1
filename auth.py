"""
Authentifikations-Helfer-Funktionen und Adapter für flask_login
"""

import uuid
from typing import Generic, TypeVar

User = TypeVar('User')


class Authenticated(Generic[User]):
    """
Ein schmaler Wrapper um einen Nutzerdatensatz, der flask_logins Anforderungen erfüllt
    """
    def __init__(self, user_record: User):
        self.record = user_record
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def get_id(self):
        """
        Wird von flask_login gebraucht.
        :return: str die User-ID, stimmt mit der Tabellen-ID überein (zufällig)
        """
        return str(self.record.id)

    def __getattr__(self, attr):
        return getattr(self.record, attr)

    # Yeah, no, that doesn't work xD
    # the ctor will trigger an infinite loop
    # def __setattr__(self, attr, value):
    #     return setattr(self.record, attr, value)


def generate_token():
    """"
Erzeugt ein neues, sicheres Token, mit dem sich Nutzer authentifizieren können.
    """
    return str(uuid.uuid4())
