"""
Marketplace GSO – Aussteller-Anmelde-Portal für die Jobmesse des Georg-Simon-Ohm-Berufskollegs
"""
from flask import Flask
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def landing_page():
    """
Globaler Einstiegspunkt, insbesondere für nicht authentifizierte Nutzer
    """
def hello_world():  # put application's code here
    return render_template("baseTemplate.html")
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
