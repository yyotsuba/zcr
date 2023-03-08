"""
Created by yyotusba on 2023/03/06
"""

class BaseError(Exception):
    """Base Error"""

class ConfigError(BaseError):
    "raise config error"
