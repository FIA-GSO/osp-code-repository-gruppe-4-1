from datetime import datetime, timedelta
from sqlalchemy import Integer, String, Boolean, DateTime, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, mapped_column, declarative_base, relationship

base = declarative_base()

class User(base):
    __tablename__ = 'users'

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, nullable=False)
    contact_person = mapped_column(String, nullable=True)
    phone = mapped_column(String, nullable=True)
    email = mapped_column(String, nullable=False, unique=True)
    street = mapped_column(String, nullable=True)
    zip = mapped_column(String, nullable=True)
    city = mapped_column(String, nullable=True)
    support_association = mapped_column(Boolean, nullable=False, default=False)
    is_admin = mapped_column(Boolean, nullable=False, default=False)

    tokens = relationship("Token", back_populates="user")
    bookings = relationship("Booking", back_populates="user")

class Token(base):
    __tablename__ = 'tokens'

    token = mapped_column(String, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    last_seen = mapped_column(DateTime, nullable=True)
    valid_until = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now() + timedelta(days=365.25 * 2)
    )

    user = relationship("User", back_populates="tokens")

class Booking(base):
    __tablename__ = 'bookings'

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    duration = mapped_column(Integer, nullable=False)

    user = relationship("User", back_populates="bookings")

# Datenbankverbindung
engine = create_engine('sqlite:///database/marketplace.sqlite')
base.metadata.create_all(engine)
session = sessionmaker(bind=engine)
