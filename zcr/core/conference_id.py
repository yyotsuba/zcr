import random
import redis

from zcr.cache.backends.redis_cache import RedisCache
from zcr.config.settings import settings

class ConferenceId(object):
    __cache = None
    __instance = None
    extra_max = 10**6-1

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            return object.__new__(cls)
        return cls.__instance

    def __init__(self):
        if __cache is None:
            self.__cache = RedisClient(settings.CACHES_CONF.default_redis

    def generate(self):
        _id = random.randint(10**5, 9 * 10**5 - 1)
        if (self.redis_cache.call_method(sismember, 'conference_id', str(_id))): 
            self.redis_cache.call_method(sadd, 'conference_id', str(self.extra_max))
            self.extra_max += 1
            return self.extra_max + 1
        else:
            self.redis_cache.call_method(sadd, 'conference_id', str(_id)
            return _id

    @property
    def redis_cache(self):
        return self.__cache
