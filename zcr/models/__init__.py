from sqlalchemy import Column, DateTime, Integer, String

from .base import MapBase, DbInit

class User(MapBase, DbInit):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, index=True)
    password = Column(String(128))
    email = Column(String(128))

class ConferenceReservation(MapBase, DbInit):
    __tablename__ = 'conference_reservation'
    id = Column(Integer, primary_key=True)
    conference_id = Column(String(64))
    applicant = Column(String(64))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    status = Column(Integer)

class ConferenceParticipation(MapBase, DbInit):
    __tablename__ = 'conference_participation'
    id = Column(Integer, primary_key=True)
    reservation_id = Column(Integer)
    participant = Column(String(64))
