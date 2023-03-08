from tornado.options import options
from tornado.util import import_object

from zcr import global_settings
from zcr.exception import ConfigError
from zcr.util.storage import storage

class _Settings(object):
    def __getattr__(self, item):
        setting = _Settings.settings_object()
        if hasattr(setting, item):
            config = getattr(setting, item)
        else:
            raise ConfigError(f'settings "{item}" not exist!')
        return storage(config) if type(config) is dict else config

    @classmethod
    def settings_object(cls):
        if not hasattr(cls, '_sett'):
            cls._sett = global_settings

        return cls._sett

settings = _Settings()
