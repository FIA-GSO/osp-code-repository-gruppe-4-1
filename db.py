"""
Datenbank-Schicht mit Helfer-Funktionen
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from auth import Authenticated
from database.models import Schema, Booking, Correspondence

# Datenbankverbindung
engine = create_engine('sqlite:///database/marketplace.sqlite')
Schema.metadata.create_all(engine)
session = sessionmaker(bind=engine)

db = session()


def get_bookings(**filters) -> list[Booking]:
    """
    Alle Buchungen, die den gegebenen Filtern genügen.
    CAVE: An dieser Stelle findet keine Berechtigungsprüfung statt!
    :param filters:
    :return:
    """
    user_filters = {}
    if 'industry' in filters:
        user_filters['industry'] = filters.pop('industry')
    query = db.query(Booking).filter_by(**filters)
    query = query.join(Booking.user).filter_by(**user_filters)
    query = query.join(Booking.correspondence, isouter=True)
    return [decorate(booking) for booking in query.all()]


def decorate(booking: Booking) -> Booking:
    """
    Berechnet die Dauer einer Buchung und hängt sie als Attribut an die Instanz an.
    :param booking:
    :return:
    """
    booking.duration = booking.first + booking.second
    booking.needs_response =(
            bool(len(booking.correspondence)) and not booking.correspondence[-1].from_admin)
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


def send_message(current_user: Authenticated, booking_id: int, message: str):
    # ToDo: properly sanitize/validate!
    data_object = Correspondence(
        booking_id=booking_id,
        from_admin=current_user.is_admin,
        from_user=current_user.id,
        message=message
    )
    db.add(data_object)
    db.commit()
    return data_object


def save_note(booking_id: int, note: str):
    # ToDo: properly sanitize/validate!
    booking = get_bookings(id=booking_id)[0]
    booking.admin_note = note
    db.commit()
