from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import registry, sessionmaker

from zcr.config.settings import settings

class MysqlGlobal(object):
    __instance = None
    __engine = None

    def __new(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def gen_engine(self):
        if not MysqlGlobal.__engine:
            engine = create_engine(**settings.MYSQL_CONF)
            MysqlGlobal.__engine = engine

        return MysqlGlobal.__engine

    @property
    def mysql_session(self):
        self.gen_engine()
        mysql_db = sessionmaker(bind=MysqlGlobal.__engine)
        return mysql_db

mapper_registry = registry()
MapBase = mapper_registry.generate_base()

class DbInit(object):
    created_at = Column(DateTime, default=datetime.now)
