import logging
import functools
import time

from zcr.core.log import Log
from zcr.core.status import Code, Message
from zcr.models.base import MysqlGlobal

class Route(object):
	_routes = []

	def __init__(self, url):
		self._url = url

	def __call__(self, _handler):
		"""gets called when we class decorate"""
		self._routes.append((self._url, _handler))
		return _handler

	@classmethod
	def get_routes(cls):
		return cls._routes

def jwt_auth(method):
	async def wrapper(self, *args, **kwargs):
		current_user = self.set_current_user()
		if not current_user:
			return self.write_fail(Code.User.TOKEN_INVALD,
								   Message.User.TOKEN_INVALID)
		return await method(self, *args, **kwargs)
	return wrapper

def mysql_session(method):
	@functools.wraps(method)
	def wrapper(*args, **kwargs):
		session = MysqlGlobal().mysql_session
		return method(session, *args, **kwargs)
	return wrapper

def timer(func):
	@functools.wraps(func)
	def wrap(*args, **kwargs):
		begin_time = time.perf_counter()
		result = func(*args, **kwargs)
		end_time = time.perf_counter()
		Log.log_show_store(f'func:{func.__name__} args:[args, kwargs] took: \
						   {end_time - begin_time} sec', logging.DEBUG)
		return result
	return wrap
