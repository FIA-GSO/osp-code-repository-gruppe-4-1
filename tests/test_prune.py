from datetime import datetime, timedelta
from time import time

from auth import generate_token
from database.models import User, Token
from db import db
from prune_archive import prune_archive


def test_prune_archive():
    # Erstelle einen Testbenutzer, der seit mehr als 2 Jahren inaktiv ist
    old_user = User(name='Hans Peter', email=f'hans.peter+{int(time())}@bbk.de', is_admin=False)
    db.add(old_user)
    db.commit()

    old_token = generate_token()
    old_db_token = Token(token=old_token, user_id=old_user.id, last_seen=datetime.now() - timedelta(days=365.25 * 2 + 1))
    db.add(old_db_token)
    db.commit()

    # Erstelle einen Testbenutzer, der aktiv ist
    active_user = User(name='Günther Jauch', email=f'günther.jauch+{int(time())}@rtl.de', is_admin=False)
    db.add(active_user)
    db.commit()

    active_token = generate_token()
    active_db_token = Token(token=active_token, user_id=active_user.id, last_seen=datetime.now())
    db.add(active_db_token)
    db.commit()

    # Führe die Archivbereinigung durch
    prune_archive()

    # Überprüfe, ob der alte Benutzer gelöscht wurde
    assert db.query(User).filter_by(id=old_user.id).first() is None
    assert db.query(Token).filter_by(user_id=old_user.id).first() is None

    # Überprüfe, ob der aktive Benutzer nicht gelöscht wurde
    assert db.query(User).filter_by(id=active_user.id).first() is not None
    assert db.query(Token).filter_by(user_id=active_user.id).first() is not None

    db.delete(active_user)
    db.delete(active_db_token)
    db.commit()

    # Überprüfe, ob reinigen nach dem Test erfolgreich war
    assert db.query(User).filter_by(id=active_user.id).first() is None
    assert db.query(Token).filter_by(user_id=active_user.id).first() is None
