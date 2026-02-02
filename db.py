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
    return db.query(Booking).filter_by(**filters).all()