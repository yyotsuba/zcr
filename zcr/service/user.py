from zcr.core.celery import app
from zcr.models import User
from zcr.view.decorators import mysql_session
class UserService(object):
    @staticmethod
    @mysql_session
    def fetch_by_name(session, name, queries=None):
        session = session()
        if queries is None:
            return session.query(User).filter_by(name = name).first()
        else:
            queries = [getattr(User, attr) for attr in queries]
            return session.query(*queries).filter_by(name = name).first()

    @staticmethod
    @app.task
    @mysql_session
    def create(session, user):
        print(user)
        user_obj = User(**user)
        session = session()
        session.add(User(**user))
        session.commit()
