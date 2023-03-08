import json
import tornado.web

from zcr.core.status import Code, Message
from zcr.util.token import jwt_decode

class BaseHandler(tornado.web.RequestHandler):
	_current_user = None
	def __init__(self, application, request):
		super(BaseHandler, self).__init__(application, request)
		self._current_user = None

	@property
	def current_user(self):
		return self._current_user

	def set_current_user(self):
		token = self.get_secure_cookie('token')
		if not token:
			self._current_user = None
			return None
		settings = self.application.settings
		payload = jwt_decode(token, settings['token_secret_key'],
							 verify_exp=settings['token_verify_expire'])
		if not payload or not payload.get('data'):
			self._current_user = None
			return None
		self._current_user = payload['data']['name']
		return self._current_user

	def set_default_headers(self):
		self.set_header("Access-Control-Allow-Origin", '*')
		self.set_header("Access-Control-Allow-Headers", '*')
		self.set_header("Access-Control-Allow-Method", 'POST, GET, PUT, DELETE, OPTIONS')

	def write_fail(self, code=Code.System.ERROR, msg=Message.System.ERROR, data={}, ensure_ascii=False):
		"""
		Reuqest Fail. Return fail message.
		"""
		return self.write(json.dumps({'return_code': code, 'return_data': data, 'return_msg': msg}, ensure_ascii=ensure_ascii))
	
	def write_success(self, code=Code.System.SUCCESS, msg=Message.System.SUCCESS, data={}, ensure_ascii=False):
		"""
		Request Success. Return success message.
		"""
		return self.write(json.dumps({'return_code': code, 'return_data': data, 'return_msg': msg}, ensure_ascii=ensure_ascii))


