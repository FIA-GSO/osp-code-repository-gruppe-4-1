from database.models import Booking


def validate_booking(**kwargs) -> Booking:
    # TODO
    kwargs['first'] = kwargs['first_day'] == 'yes'
    kwargs['second'] = kwargs['second_day'] == 'yes'
    return Booking(**kwargs)
