"""
Marketplace GSO – Aussteller-Anmelde-Portal für die Jobmesse des Georg-Simon-Ohm-Berufskollegs
"""
from flask import Flask


app = Flask(__name__)


@app.route('/')
def landing_page():
    """
Globaler Einstiegspunkt, insbesondere für nicht authentifizierte Nutzer
    """
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
