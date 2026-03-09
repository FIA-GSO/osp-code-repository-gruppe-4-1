"""
Marketplace GSO – Archiv-Bereinigungsskript für die Jobmesse des Georg-Simon-Ohm-Berufskollegs
"""
from datetime import datetime, timedelta

from sqlalchemy import and_

from database.models import Token, User, Booking
from db import db
from log import logger


def prune_archive():
    """Lösche alle Nutzer, die sich seit 2 Jahren nicht mehr eingeloggt haben, sowie deren Buchungen."""

    date_to_delete = datetime.now() - timedelta(days=365.25 * 2)
    old_tokens = db.query(Token).filter(Token.last_seen <= date_to_delete).group_by(Token.user_id).all()
    for token in old_tokens:
        if token.user.is_admin:
            continue

        same_user_filter = and_(Token.user_id == token.user_id, Token.last_seen > date_to_delete)
        active_user_count = db.query(Token).filter(same_user_filter).count()

        if active_user_count == 0:
            message = f"Pruning user '{token.user.name}' (ID {token.user_id}) due to inactivity since {token.last_seen}"
            logger.info(message)

            db.query(Token).filter(Token.user_id == token.user_id).delete()
            db.query(Booking).filter(Booking.user_id == token.user_id).delete()
            db.query(User).filter(User.id == token.user_id).delete()
            db.commit()


if __name__ == '__main__':
    prune_archive()
