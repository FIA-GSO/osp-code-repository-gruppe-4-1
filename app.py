"""
Marketplace GSO – Aussteller-Anmelde-Portal für die Jobmesse des Georg-Simon-Ohm-Berufskollegs
"""
import os
from datetime import datetime
from typing import Optional

from flask import Flask, Response, redirect, request, render_template, session
from flask_login import LoginManager, login_user, current_user, login_required
from sqlalchemy.exc import NoResultFound

from auth import Authenticated, generate_token
from database.models import Token, User, Booking, BookingStatus
from db import db, get_bookings, calculate_furniture_totals
from input import validate_booking, transform_filters
from triggers import notify_admins
from utils import NotificationType, Notification

app = Flask(__name__)
app.secret_key = 'de5f8d879a742af4533d19af9c5f52f34a4f15e385e96c23227a0e6a67afd40c'

login_manager = LoginManager()
login_manager.login_view = 'login_page'
login_manager.init_app(app)


@app.route('/')
def landing_page():
    """
Globaler Einstiegspunkt, insbesondere für nicht authentifizierte Nutzer
    """
    return render_template('baseHomeContent.html')


@app.route('/marketplace')
@app.route('/dashboard')
@login_required
def dashboard():
    """
Startseite für eingeloggte Nutzer: Anzeige der aktuellen Teilnahme-Buchung,
bzw. aller aktuellen Buchungen f. Admins.
    :return:
    """
    this_year = datetime.now().year
    if current_user.is_admin:
        template = 'admin_dashboard.html'
        bookings = get_bookings(**transform_filters(request.args), event_year=this_year)
    else:
        template = 'user_dashboard.html'
        all_bookings = get_bookings(user_id=current_user.id)
        current = [b for b in all_bookings if b.event_year == this_year]
        bookings = {
            "past": [b for b in all_bookings if b.event_year < this_year],
            "current": current.pop() if len(current) > 0 else None,
        }
    return render_template(template, user=current_user, bookings=bookings)

@app.route('/admin/booking/<int:booking_id>/<action>', methods=['GET'])
@login_required
def edit_booking(booking_id: int, action: str):
    if not current_user.is_admin:
        return login_manager.unauthorized()

    if action in ['confirm', 'reject']:
        db.query(Booking).filter_by(id=booking_id).update(
            {'status': BookingStatus.accepted if action == 'confirm' else BookingStatus.rejected}
        )
        db.commit()
        return redirect(request.referrer) # ToDo: report success or failure
    else:
        return render_template(
            'error.html',
            error=f'Unsupported action: {action}'
        ), 400


@app.route('/join', methods=['GET', 'POST'])
def register():
    """
    Registrierungs-Formular und -Logik
    :return:
    """
    if request.method == 'POST':
        try:
            new_user = User(**request.form)
            db.add(new_user)
            db.commit()

            new_token = Token(token=generate_token(), user_id=new_user.id)
            db.add(new_token)
            db.commit()

            session['notifications'] = [Notification(NotificationType.info, f'Ihr Token ist {new_token.token}')]
            login_user(Authenticated(new_user))
            return redirect('/register')

        except Exception as e:

            db.rollback()
            return render_template('error.html', error=e)

    return render_template('registration_form.html')


@app.route('/register', methods=['GET', 'POST'])
@login_required
def register_for_event():
    """
    Anmeldung zu einem Event: Formular & Logik
    """
    if request.method != 'POST':
        return render_template('event_registration_form.html')

    try:
        this_year = datetime.now().year
        new_booking = validate_booking(**request.form, user_id=current_user.record.id, event_year=this_year)
        db.add(new_booking)
        db.commit()

        notify_admins(new_booking)

        return redirect('/dashboard')

    except Exception as e:
        return render_template('error.html', error=e)


@app.route('/marketplace/export/<export_type>', methods=['POST'])
@app.route('/dashboard/export/<export_type>', methods=['POST'])
@login_required
def export(export_type):
    """
    Export-Logik für Admins
    :param export_type: csv oder pdf
    """
    if not current_user.is_admin:
        return render_template('error.html', error='Unauthorized'), 403

    if export_type not in ['csv']:
        return render_template(
            'error.html',
            error=f'Export-Format {export_type} ist noch nicht implementiert'
        ), 501

    this_year = datetime.now().year
    bookings = get_bookings(event_year=this_year, **transform_filters(request.args))

    furniture = {
        "first_day": calculate_furniture_totals([b for b in bookings if b.first]),
        "second_day": calculate_furniture_totals([b for b in bookings if b.second])
    }

    response = None

    if export_type == 'csv':
        csv_string = (f"Firma;Ansprechpartner;Branche;Anzahl Tage;"
                      f"Tag 1;Tag 2;Status;Stühle;Tische{os.linesep}")
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
                           f"{os.linesep};")

        csv_string += (f"{os.linesep}"
                       f"Benötigte Möbel am ersten Tag:;{furniture['first_day']['total_chairs']};"
                       f"{"Stühle" if furniture['first_day']['total_chairs'] > 1 else "Stuhl"};"
                       f"{furniture['first_day']['total_tables']};"
                       f"{"Tische" if furniture['first_day']['total_tables'] > 1 else "Tisch"}"
                       f"{os.linesep}"
                       f"Benötigte Möbel am zweiten Tag:;{furniture['second_day']['total_chairs']};"
                       f"{"Stühle" if furniture['second_day']['total_chairs'] > 1 else "Stuhl"};"
                       f"{furniture['second_day']['total_tables']};"
                       f"{"Tische" if furniture['second_day']['total_tables'] > 1 else "Tisch"}"
                       f"{os.linesep}"
                       f"Anmeldungen:;{len(bookings)}")

        response = Response(csv_string, content_type="text/csv; charset=utf-8")
        response.headers["Content-Disposition"] = "attachment; filename=export.csv"

    return response

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    """
    Log-In-Formular und -Logik
    """
    if request.method == 'POST':
        return login(request.form.get('token'))
    return render_template('login_form.html')


@app.route('/login/<token>')
def login(token):
    """
    (Nur) Login-Logik
    :param token:
    """
    try:
        token = db.query(Token).filter_by(token=token).one()
        session.clear()
        login_user(Authenticated(token.user))
        return redirect('/marketplace')
    except NoResultFound:
        return render_template(
            'error.html',
            error='Nope, das war wohl nichts (ungültiges Token)'
        ), 403


@login_manager.user_loader
def load_user(user_id) -> Optional[Authenticated[User]]:
    """
    flask_login braucht dieses Loader-Plugin
    :param user_id:
    """
    try:
        user_id = int(user_id)
        user_record = db.query(User).filter_by(id=user_id).one()
        return Authenticated(user_record)
    except Exception:
        print(f'[WARN] user id not found: {user_id}')
        return None


if __name__ == '__main__':
    app.run(debug=True)
