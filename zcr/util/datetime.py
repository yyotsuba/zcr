from pytz import timezone
from datetime import datetime

def datetime_to_eta(_datetime, _format="%Y-%m-%d %H:%M:%S", \
                    _timezone="Asia/Shanghai"):
    return datetime.strptime(_datetime, _format).astimezone(timezone(_timezone))
