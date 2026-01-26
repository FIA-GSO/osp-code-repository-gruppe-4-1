"""
Marketplace GSO – Aussteller-Anmelde-Portal für die Jobmesse des Georg-Simon-Ohm-Berufskollegs
"""
from flask import Flask, redirect, request, render_template
from flask_login import LoginManager, login_user, UserMixin
from sqlalchemy.exc import NoResultFound

from auth import Authenticated, generate_token
from database.models import session, Token, User


app = Flask(__name__)
app.secret_key = 'de5f8d879a742af4533d19af9c5f52f34a4f15e385e96c23227a0e6a67afd40c'

login_manager = LoginManager()
login_manager.init_app(app)

db = session()


@app.route('/')
def landing_page():
    """
Globaler Einstiegspunkt, insbesondere für nicht authentifizierte Nutzer
    """
    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_user = User(**request.form)
        db.add(new_user)
        new_token = Token(token=generate_token(), user_id=new_user.id)
        db.add(new_token)
        db.commit()
        return 'Ihr Token ist {new_token.token}'
    else:
        return render_template('registration_form.html')


@app.route('/login/<token>')
def login(token):
    try:
        token = db.query(Token).filter_by(token=token).one()
        print(f'[DEBUG] token = {token}, user = {token.user}')
        login_user(Authenticated(token.user))
        return 'Laeuft! Passt!'
    except NoResultFound:
        return 'Nope, das war wohl nichts'


@login_manager.user_loader
def load_user(user_id):
    try:
        user_id = int(user_id)
        user_record = db.query(User).filter_by(id=user_id).one()
        return Authenticated(user_record)
    except Exception as e:
        print(f'[WARN] user id not found: {user_id}')
        return None


if __name__ == '__main__':
    app.run()
