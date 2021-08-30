from datetime import datetime, tzinfo
import pytz

tz_cn = pytz.timezone('Asia/Shanghai')


def get_cn_time(time: datetime = None):
    """
    return cn time now
    """
    if not time:
        return datetime.now().astimezone(tz_cn)
    else:
        return time.astimezone(tz_cn)


def get_time_str(datetime: datetime):
    return get_cn_time(datetime).strftime('%Y/%m/%d %H:%M')
