"""
Datenbank-Schicht mit Helfer-Funktionen
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Schema, Booking, User

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
    user_filters = dict()
    if filters.get('industry') is not None:
        user_filters['industry'] = filters.pop('industry')
    query = db.query(Booking).filter_by(**filters)
    query = query.join(User).filter_by(**user_filters)
    return [decorate(booking) for booking in query.all()]

def decorate(booking):
    """
    Berechnet die Dauer einer Buchung und hängt sie als Attribut an die Instanz an.
    :param booking:
    :return:
    """
    booking.duration = booking.first + booking.second
    return booking

def calculate_furniture_totals(bookings):
    """
    Berechnet die Gesamtanzahl der benötigten Tische und Stühle aus den gegebenen Buchungen.
    :param bookings: Iterable von Booking-Instanzen
    :return: Dictionary mit total_chairs und total_tables
    """
    return {
        'total_chairs': sum(booking.chairs_needed for booking in bookings),
        'total_tables': sum(booking.tables_needed for booking in bookings)
    }
