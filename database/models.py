import enum
from datetime import datetime, timedelta
from sqlalchemy import Integer, String, Boolean, DateTime, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, declarative_base, relationship

Schema = declarative_base()

class User(Schema):
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

class Token(Schema):
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

class BookingStatus(enum.Enum):
    pending = "Wartend"
    accepted = "Bestätigt"
    rejected = "Abgelehnt"

class Booking(Schema):
    __tablename__ = 'bookings'

    id = mapped_column(Integer, primary_key=True)

    user_id = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    event_year = mapped_column(Integer, nullable=False, default=datetime.now().year)
    duration = mapped_column(Integer, nullable=False)
    status = mapped_column(Enum(BookingStatus), nullable=False, default=BookingStatus.pending)

    chairs_needed = mapped_column(Integer, nullable=False, default=0)
    tables_needed = mapped_column(Integer, nullable=False, default=0)
    remarks = mapped_column(String, nullable=True)
    presentation = mapped_column(String, nullable=True)

    user = relationship("User", back_populates="bookings")
    UniqueConstraint('user_id', 'event_year')
