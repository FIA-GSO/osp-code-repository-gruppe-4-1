"""
Eingabe-Validations und -Transformations-Werkzeuge hier
"""
from database.models import Booking


def validate_booking(**kwargs) -> Booking:
    """
    Validiert einen einzufügenden Anmeldungs-Datensatz und bereitet ihn auf.
    :param kwargs: Unverarbeitete Formulardaten (!)
    :return: fertig bestücktes Booking-Objekt zum Einfügen in DB
    :raises: ValidationError
    """
    kwargs['first'] = kwargs['first_day'] == 'yes'
    kwargs['second'] = kwargs['second_day'] == 'yes'
    return Booking(**kwargs)
