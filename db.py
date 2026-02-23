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

def calculate_furniture_totals(**filters):
    """
    Berechnet die Gesamtanzahl der benötigten Tische und Stühle aus allen gefilterten Buchungen.
    :param filters: Optional filters für die Buchungsabfrage (z.B. event_year=2026)
    :return: Dictionary mit total_chairs und total_tables
    """
    bookings = db.query(Booking).filter_by(**filters).all()

    total_chairs = sum(booking.chairs_needed for booking in bookings)
    total_tables = sum(booking.tables_needed for booking in bookings)

    return {
        'total_chairs': total_chairs,
        'total_tables': total_tables
    }
