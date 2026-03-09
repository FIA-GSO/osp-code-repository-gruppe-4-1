"""
Marketplace GSO – Aussteller-Anmelde-Portal für die Jobmesse des Georg-Simon-Ohm-Berufskollegs
"""
import os
from datetime import datetime, timedelta
from typing import Optional

from flask import Flask, Response, redirect, request, render_template, session
from flask_login import LoginManager, login_user, current_user, login_required
from gevent.pywsgi import WSGIServer
from sqlalchemy.exc import NoResultFound

from auth import Authenticated, generate_token
from constants import industry_names
from database.models import Token, User, Booking, BookingStatus
from db import db, get_bookings, send_message, save_note
from export import create_export
from floor_plan import decorate_hall_plans, generate_floor_plan
from input import validate_booking, transform_filters, preprocess_user
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


@app.route('/marketplace/message', methods=['POST'])
@app.route('/dashboard/message', methods=['POST'])
@login_required
def submit_request():
    this_year = datetime.now().year
    booking = get_bookings(user_id=current_user.id, event_year=this_year).pop()
    message = send_message(current_user, booking.id, request.form.get('message'))
    notify_admins(message)
    return redirect('/dashboard')


@app.route('/admin/booking/<int:booking_id>/<action>', methods=['GET', 'POST'])
@login_required
def edit_booking(booking_id: int, action: str):
    if not current_user.is_admin:
        return login_manager.unauthorized()

    try:
        match action:
            case 'confirm'|'reject':
                db.query(Booking).filter_by(id=booking_id).update(
                    {'status': BookingStatus.accepted if action == 'confirm' else BookingStatus.rejected}
                )
                db.commit()

            case 'respond':
                send_message(current_user, booking_id, request.form.get('response'))

            case 'note':
                save_note(booking_id, request.form.get('note'))

            case _:
                return fail_with(f'Nicht unterstützte Aktion: {action}') # , 400

        return redirect(request.referrer)

    except Exception as e:
        return fail_with(f'Ein Fehler ist aufgetreten: {e}')


@app.route('/admin/floorplan', methods=['GET'])
@login_required
def show_floor_plan():
    if not current_user.is_admin:
        return login_manager.unauthorized()

    registrations = get_bookings(event_year=datetime.now().year)
    floor_plan = decorate_hall_plans(generate_floor_plan(registrations, transform_filters(request.args)))
    return render_template('floor_plan.html', floor_plan=floor_plan)


@app.route('/join', methods=['GET', 'POST'])
def register():
    """
    Registrierungs-Formular und -Logik
    :return:
    """
    if request.method == 'POST':
        try:
            new_user = preprocess_user(**request.form)
            db.add(new_user)
            db.commit()

            new_token = Token(token=generate_token(), user_id=new_user.id)
            db.add(new_token)
            db.commit()

            push_notification(f'Ihr Token ist {new_token.token}')
            login_user(Authenticated(new_user))
            return redirect('/register')

        except Exception as e:
            db.rollback()
            return fail_with(f'Fehler beim Erstellen des Kontos: {e}'), 500

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
        return fail_with(f'Ein Fehler ist aufgetreten: {e}'), 500


@app.route('/confirm-receipt/<int:notif_index>')
def mark_notification_as_read(notif_index: int):
    # ToDo: do this right. not like this. disgusting.
    notification_list = [] if session.get('notifications') is None else session['notifications']
    if notif_index < len(notification_list):
        notification_list.pop(notif_index)
    session['notifications'] = notification_list[:]
    return redirect(request.referrer)


@app.route('/marketplace/export/<export_type>', methods=['POST'])
@app.route('/dashboard/export/<export_type>', methods=['POST'])
@login_required
def export(export_type):
    """
    Export-Logik für Admins
    :param export_type: csv oder pdf
    """
    if not current_user.is_admin:
        return fail_with('Sie haben keine Berechtigung, auf diese Funktion zuzugreifen.')

    if export_type not in ['csv']:
        return fail_with(f'Export-Format {export_type} ist noch nicht implementiert.') # , 501

    response = None

    csv_string = create_export(request.form.to_dict())
    if csv_string is not None:
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
        now = datetime.now()
        token = db.query(Token).filter_by(token=token).one()
        if token.valid_until < now and token.user.is_admin is False:
            raise NoResultFound()

        session.clear()
        token.last_seen = now
        token.valid_until = now + timedelta(days=365.25 * 2)
        db.commit()
        login_user(Authenticated(token.user))
        return redirect('/marketplace')
    except NoResultFound:
        return fail_with('Zugang verweigert: Ihr Token ist ungültig.') #, 403


@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect('/login')


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


@app.context_processor
def inject_constants():
    return { 'industry_names': industry_names }


def push_notification(message: str, type: str = NotificationType.info):
    notification_list = [] if session.get('notifications') is None else session['notifications']
    new = Notification(type=type, message=message)
    session['notifications'] = [new, *notification_list]


def fail_with(error: str):
    push_notification(error, NotificationType.error)
    return redirect(request.referrer if request.referrer is not None else '/marketplace')


if __name__ == '__main__':
    if os.getenv('FLASK_MODE', default='development') == 'production':
        http_server = WSGIServer(('0.0.0.0', 5000), app)
        http_server.serve_forever()
    else:
        app.run(debug=True)
