import os
from urllib.parse import quote_plus as urlquote

PROJECT_ROOT = os.path.dirname(__file__)

DEBUG = True

# tornado全局配置
TORNADO_CONF = {
    "static_path": os.path.join(PROJECT_ROOT, 'static'),
    "cookie_secret": 'my cookie secret',
    "token_secret": 'my token secret',
    "token_verify_expire": True,
    "token_expire_days": 7,
}

# log全局配置
LOG_CONF = {
    "log_path": os.path.join(PROJECT_ROOT, 'logs'),
    "log_format": '%(asctime)s - %(levelname)s - %(message)s',
}

# mysql全局配置
MYSQL_CONF = {
    "url":
    f'mysql+mysqlconnector://root:{urlquote("123456")}@localhost:3306/zcr?charset=utf8',
    "echo": False,
    "echo_pool": False,
    "pool_recycle": 25200,
    "pool_size": 20,
    "max_overflow": 20,
}

# celery全局配置
CELERY_CONF = {
    "timezone": "Asia/Shanghai",
    "enable_utc": False,
    "broker_url": "redis://:@localhost:6379/0",
    "result_backend": "redis://:@localhost:6379/1",
    "task_serializer": "json",
    "result_serializer": "json",
    "accept_content": ["json"],
    "task_result_expires": 24 * 60 * 60,
    "include": [
        "zcr.service.user",
    ],
}
