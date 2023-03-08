from datetime import datetime

from zcr.config.settings import settings
from zcr.core.handler import BaseHandler
from zcr.core.status import Code, Message
from zcr.service.user import UserService
from zcr.view.decorators import Route, jwt_auth
from zcr.util.token import jwt_encode

@Route(r'/register/?')
class RegisterHandler(BaseHandler):
	async def post(self):
		name = self.get_argument('name')
		password = self.get_argument('password')
		email = self.get_argument('email')
		if (UserService.fetch_by_name(name, queries=['id'])):
			self.write_fail(Code.User.USER_IS_EXIST, Message.User.USER_IS_EXIST)
		else:
			user = {
				'name': name,
				'password': password,
				'email': email,
				'created_at': datetime.now()
			}
			UserService.create.apply_async((user, ))
			self.write_success()




@Route(r'/login/?')
class LoginHandler(BaseHandler):
	async def post(self):
		name = self.get_argument('name')
		password = self.get_argument('password')
		user = UserService.fetch_by_name(name, queries=['password'])
		if not user or user.password != password:
			self.write_fail(Code.User.USER_INVALID, Message.User.USER_INVALID)
		else:
			data = {
				'name': name,
				'login_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
			}
			token = jwt_encode(data, settings.TORNADO_CONF.token_secret,
							   settings.TORNADO_CONF.token_expire_days)
			self.set_secure_cookie('token', token)
			self.write_success(msg="登录成功!")
