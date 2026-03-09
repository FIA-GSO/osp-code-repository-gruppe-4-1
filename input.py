"""
Eingabe-Validations und -Transformations-Werkzeuge hier
"""
from typing import Any
from werkzeug.datastructures import MultiDict
from database.models import Booking, User


class ValidationError(Exception):
    pass


class ConstraintViolation(ValidationError):
    pass


def validate_booking(**kwargs) -> Booking:
    """
    Validiert einen einzufügenden Anmeldungs-Datensatz und bereitet ihn auf.
    :param kwargs: Unverarbeitete Formulardaten (!)
    :return: fertig bestücktes Booking-Objekt zum Einfügen in DB
    :raises: ConstraintViolation
    """

    if not 'user_id' in kwargs or not isinstance(kwargs['user_id'], int):
        raise ConstraintViolation('Nutzer-ID nicht gesetzt!')

    kwargs['first'] = kwargs.pop('first_day', 'no') == 'yes'
    kwargs['second'] = kwargs.pop('second_day', 'no') == 'yes'
    if not kwargs['first'] and not kwargs['second']:
        raise ConstraintViolation('Sie müssen an mindestens einem Tag teilnehmen!')
    
    return Booking(**kwargs)


def has_non_empty_string(form: dict[str, Any], key: str) -> bool:
    return key in form and isinstance(form[key], str) and len(form[key]) > 0 and not form[key].isspace()


def preprocess_user(**fields) -> User:
    """
    Validiert einen einzufügenden Nutzer-Datensatz und bereitet ihn auf.
    :param fields: Unverarbeitete Formulardaten (!)
    :return: fertig bestücktes User-Objekt zum Einfügen in DB
    :raises: ConstraintViolation
    """
    # guards ensure that we don't miss anything
    if 'dsgvo' not in fields or fields['dsgvo'] != 'yes':
        raise ConstraintViolation('Zustimmung zur Datenverarbeitung ist zwingend erforderlich!')

    for field in ['contact_person', 'name', 'email']:
        if not has_non_empty_string(fields, field):
            raise ConstraintViolation('Kontaktdaten sind unvollständig!')

    for field in ['street', 'zip', 'city']:
        if not has_non_empty_string(fields, field):
            raise ConstraintViolation('Adressdaten sind unvollständig!')

    # transform
    del fields['dsgvo']
    fields['support_association'] = fields.get('support_association') == 'on'

    return User(**fields)


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
        if qparams['day'] == 'first':
            db_filters['first'] = True
            db_filters['second'] = False
        elif qparams['day'] == 'second':
            db_filters['first'] = False
            db_filters['second'] = True

    if 'industry' in qparams and qparams['industry'] != 'all':
        db_filters['industry'] = qparams['industry']

    return db_filters
