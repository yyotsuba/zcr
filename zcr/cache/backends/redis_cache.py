import redis
from tornado.util import  import_object

from zcr.cache.base import CacheClient, CacheMixin
from zcr.exception import ConfigError

class RedisClient(CacheClient):
    def __init__(self, params):
        """Connect to Redis, and set up cache backend"""
        self._init(params)

    def _init(self, params):
        super(RedisClient, self).__init__(params)
        self._params = params

        host, port = self.server.rsplit(':', 1)
        try:
            port = int(port)
        except(ValueError, TypeError):
            raise ConfigError("port value must be an integer")

        try:
            self.pool = redis.ConnectionPool(host=host, port=port, db=self.db,
                                             max_connections=self.max_connections)
        except Exception as e:
            pass

    def get_redis_client(self):
        try:
            # 从连接池获取连接实例
            redis_conn = redis.StrictRedis(connection_pool=self.pool)
            if redis_conn.ping():
                return redis_conn
        except Exception as e:
            import traceback
            traceback.print_exc()
    @property
    def server(self):
        return self._params.get('SERVER', 'localhost:6379')

    @property
    def options(self):
        return self._params.get('OPTIONS', {})

    @property
    def max_connections(self):
        _max_connection = self.options.get('MAX_CONNECTIONS', 100)
        try:
            _max_connection = int(_max_connection)
        except (ValueError, TypeError):
            raise ConfigError("max_connection value must be an interger")
        return _max_connection

    @property
    def db(self):
        _db = self.options.get('DB', 2)
        try:
            _db = int(_db)
        except (ValueError, TypeError):
            raise ConfigError("db value must be an interger")
        return _db


class RedisCache(CacheMixin, RedisClient):
    def add(self, key, value, version=None):
        pass

    def call_method(self, method, key, *args, version=None):
        redis_conn = self.get_redis_client()
        key = self.make_key(key, version=version)
        if callable(getattr(redis_conn, method)):
            getattr(redis_conn, method)(key, *args)

