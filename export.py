
from datetime import datetime
import os

from db import get_bookings
from floor_plan import decorate_hall_plans, generate_floor_plan
from input import transform_filters


def export_floor_plan(form_data):
    # This function would contain the logic to export the floor plan data,
    # possibly as a CSV or Excel file. The implementation would depend on the
    # specific requirements for the export format and the data structure.

    this_year = datetime.now().year
    bookings = get_bookings(event_year=this_year)
    floor_plan = decorate_hall_plans(generate_floor_plan(bookings, transform_filters(form_data)))

    csv_string = ""

    for day in floor_plan.days:
        csv_string += f"{day.name}{os.linesep}"
        for hall in day.halls:
            csv_string += f"{hall.hall.name} ({len(hall.bookings)}){os.linesep}"
            csv_string += (f"Firma;Ansprechpartner;Branche;Benötigte Stühle;Benötigte Tische"
                        f"{os.linesep}")
            for booking in hall.bookings:
                csv_string += (f"{booking.user.name};"
                                f"{booking.user.contact_person};"
                                f"{(booking.user.industry if booking.user.industry else '-')};"
                                f"{booking.chairs_needed};"
                                f"{booking.tables_needed};"
                                f"{os.linesep}")
            csv_string += f"Gesamt:;;;{hall.chairs};{hall.tables}{os.linesep}"
        csv_string += os.linesep

    return csv_string

def export_registrations(form_data):
    this_year = datetime.now().year
    bookings = get_bookings(event_year=this_year, **transform_filters(form_data))

    csv_string = (f"Anmeldungen:;{len(bookings)};;;;;;;"
                  f"{os.linesep}"
                  f"Firma;Ansprechpartner;Branche;Anzahl Tage;"
                  f"Tag 1;Tag 2;Status;Stühle;Tische"
                  f"{os.linesep}")
    for booking in bookings:
        csv_string += (f"{booking.user.name};"
                        f"{booking.user.contact_person};"
                        f"{(booking.user.industry if booking.user.industry else '-')};"
                        f"{sum([booking.first, booking.second])};"
                        f"{("Ja" if booking.first else "Nein")};"
                        f"{("Ja" if booking.second else "Nein")};"
                        f"{booking.status.value};"
                        f"{booking.chairs_needed};"
                        f"{booking.tables_needed};"
                        f"{os.linesep}")

    return csv_string

def create_export(form_data):
    report = form_data.pop('report_type', 'bookings')

    if report == 'floor_plan':
        return export_floor_plan(form_data)

    return export_registrations(form_data)
