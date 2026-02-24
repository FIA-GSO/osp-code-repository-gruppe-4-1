"""
Eingabe-Validations und -Transformations-Werkzeuge hier
"""
from typing import Any
from werkzeug.datastructures import MultiDict
from database.models import Booking


class ValidationError(Exception):
    pass


class ConstraintViolation(ValidationError):
    pass


def validate_booking(**kwargs) -> Booking:
    """
    Validiert einen einzufügenden Anmeldungs-Datensatz und bereitet ihn auf.
    :param kwargs: Unverarbeitete Formulardaten (!)
    :return: fertig bestücktes Booking-Objekt zum Einfügen in DB
    :raises: ValidationError
    """
    kwargs['first'] = kwargs.pop('first_day', 'no') == 'yes'
    kwargs['second'] = kwargs.pop('second_day', 'no') == 'yes'
    if not kwargs['first'] and not kwargs['second']:
        raise ConstraintViolation('Sie müssen an mindestens einem Tag teilnehmen!')
    return Booking(**kwargs)


def transform_filters(qparams: MultiDict[str, str]) -> dict[str, Any]:
    """
    Übersetzt die gesetzten Formular-Filter (aus admin_dashboard.html) in Datenbank-Filter.
    :param qparams: Formular-Filter
    :return: Datenbank-Filter
    """
    db_filters = {}
    if 'status' in qparams and qparams['status'] != 'all':
        db_filters['status'] = qparams['status']
    if 'day' in qparams and qparams['day'] != 'all':
        if qparams['day'] != 'second':
            db_filters['first'] = True
        if qparams['day'] != 'first':
            db_filters['second'] = True
    if 'industry' in qparams and qparams['industry'] != 'all':
        db_filters['industry'] = qparams['industry']
    return db_filters
