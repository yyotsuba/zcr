from tornado.util import import_object

def default_key_func(key, key_prefix, version):
    return f'{key_prefix}:{version}:{key}'

def get_key_func(key_func):
    """
    Function to decide which key function to use
    Defaults to ``default_key_func``.
    """
    if key_func is not None:
        if callable(key_func):
            return key_func
        else:
            return import_object(key_func)
    return default_key_func

class CacheClient(object):
    def __init__(self, params):
        self.version = params.get('VERSION', 1)
        self.key_prefix = params.get('KEY_PREFIX', '')
        self.key_func = get_key_func(params.get('KEY_FUNCTION', None))

    def make_key(self, key, version):
        if version is None:
            version = self.version

        new_key = self.key_func(key, self.key_prefix, version)
        return new_key

    def close(self, **kwargs):
        """Close the cache connection"""
        pass

class CacheMixin(object):
    def add (self, key, value, version=None):
        raise NotImplementedError('subclasses of BaseCache must provide an \
                                  add() method')
