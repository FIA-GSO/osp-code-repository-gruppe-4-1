"""
Datenbank-Schicht mit Helfer-Funktionen
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Schema, Booking


# Datenbankverbindung
engine = create_engine('sqlite:///database/marketplace.sqlite')
Schema.metadata.create_all(engine)
session = sessionmaker(bind=engine)

db = session()


def get_bookings(**filters):
    """
    Alle Buchungen, die den gegebenen Filtern genügen.
    CAVE: An dieser Stelle findet keine Berechtigungsprüfung statt!
    :param filters:
    :return:
    """
    return map(decorate, db.query(Booking).filter_by(**filters).all())

def decorate(booking):
    """
    Berechnet die Dauer einer Buchung und hängt sie als Attribut an die Instanz an.
    :param booking:
    :return:
    """
    booking.duration = booking.first + booking.second
    return booking
