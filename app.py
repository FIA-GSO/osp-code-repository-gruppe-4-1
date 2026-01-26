"""
Marketplace GSO – Aussteller-Anmelde-Portal für die Jobmesse des Georg-Simon-Ohm-Berufskollegs
"""
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def landing_page():
    """
Globaler Einstiegspunkt, insbesondere für nicht authentifizierte Nutzer
    """
    return render_template('baseHomeContent.html')


if __name__ == '__main__':
    app.run()
