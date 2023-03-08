from sqlalchemy import Column, DateTime, Integer, String

from .base import MapBase, DbInit

class User(MapBase, DbInit):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, index=True)
    password = Column(String(128))
    email = Column(String(128))
