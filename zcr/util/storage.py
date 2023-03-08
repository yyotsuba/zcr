class Storage(dict):
    """
    对字典进行拓展，使其支持通过dict.a形式访问以代替dict['a']
    """
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError(k):
            raise AttributeError(k)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError(k):
            raise AttributeError(k)

    def __repr__(self):
        return '<Storage ' + dict.__repr__(self) + '>'

storage = Storage
