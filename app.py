"""
Marketplace GSO – Aussteller-Anmelde-Portal für die Jobmesse des Georg-Simon-Ohm-Berufskollegs
"""
from typing import Optional

from flask import Flask, redirect, request, render_template
from flask_login import LoginManager, login_user, current_user
from sqlalchemy.exc import NoResultFound

from auth import Authenticated, generate_token
from database.models import Token, User
from db import db

app = Flask(__name__)
app.secret_key = 'de5f8d879a742af4533d19af9c5f52f34a4f15e385e96c23227a0e6a67afd40c'

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@app.route('/')
def landing_page():
    """
Globaler Einstiegspunkt, insbesondere für nicht authentifizierte Nutzer
    """
    return render_template('baseLayout.html')

@app.route('/marketplace')
def marketplaceLandingpage():
    if current_user.is_authenticated == False:
        return render_template('/login_form.html')
    return redirect('/to_a_route_that_make_sense') # To-Do sobald die seite fertig ist auf dei eingeloggte user geschickt werden, auf diese weiterleiten

@app.route('/dashboard')
def dashboard():
    if current_user.is_admin:
        return render_template('admin_dashboard.html', user=current_user, bookings=get_bookings())
    else:
        return render_template('user_dashboard.html', user=current_user, bookings=get_bookings(user_id=current_user.id))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_user = User(**request.form)
        db.add(new_user)
        db.commit()
        new_token = Token(token=generate_token(), user_id=new_user.id)
        db.add(new_token)
        db.commit()
        return f'Ihr Token ist {new_token.token}'

    return render_template('registration_form.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        return login(request.form.get('token'))
    return render_template('login_form.html')


@app.route('/login/<token>')
def login(token):
    try:
        token = db.query(Token).filter_by(token=token).one()
        login_user(Authenticated(token.user))
        return landing_page()
    except NoResultFound:
        return 'Nope, das war wohl nichts', 403


@login_manager.user_loader
def load_user(user_id) -> Optional[Authenticated[User]]:
    try:
        user_id = int(user_id)
        user_record = db.query(User).filter_by(id=user_id).one()
        return Authenticated(user_record)
    except (TypeError, ValueError, NoResultFound):
        print(f'[WARN] user id not found: {user_id}')
        return None


if __name__ == '__main__':
    app.run()
