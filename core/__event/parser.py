import cpca
from ChineseTimeNLP import TimeNormalizer
from dateutil.parser import parse
from models.__event import OfflineEvent, _Address

tn = TimeNormalizer(isPreferFuture=False)


def get_time(input: str):
    result = tn.parse(input)
    if result['type'] == 'timestamp':
        return parse(result['timestamp'])


def get_address(input: str):
    df = cpca.transform([input])
    result: dict = df.iloc[0].to_dict()
    if result['市']:
        return _Address(province=result['省'],
                        city=result['市'],
                        district=result.get('区'),
                        detail=result.get('地址'),
                        code=result.get('adcode'))


def event_parser(event: OfflineEvent, text: str) -> OfflineEvent:
    lines = text.splitlines()

    title = lines.pop(0)
    if not title.startswith('标题：'):
        raise ValueError('无法识别标题，请确认该行开头是否与示例保持一致')
    event.title = title[3:]
    if not event.title:
        raise ValueError('请填写活动标题！')

    start_time = lines.pop(0)
    if not start_time.startswith('时间：'):
        raise ValueError('无法识别时间，请确认该行开头是否与示例保持一致')
    event.start = get_time(start_time[3:])
    if not event.start:
        raise ValueError('无法解析时间，请尝试以下格式：x月x日 xx:xx')

    address = lines.pop(0)
    if not address.startswith('地址：'):
        raise ValueError('无法识别地址，请确认该行开头是否与示例保持一致')
    event.address = get_address(address[3:])
    if not event.address:
        raise ValueError('无法解析地址，请尝试以下格式：北京市东城区方家胡同xx号野友趣')

    info = lines.pop(0)
    if not info.startswith('简介：'):
        raise ValueError('无法识别简介，请确认该行开头是否与示例保持一致')
    event.info = info[3:]

    contact = lines.pop(0)
    if not contact.startswith('联系方式：'):
        raise ValueError('无法识别联系方式，请确认该行开头是否与示例保持一致')
    event.contact = contact[5:]

    fee = lines.pop(0)
    if not fee.startswith('活动费用：'):
        raise ValueError('无法识别活动费用，请确认该行开头是否与示例保持一致')
    event.fee = fee

    register = lines.pop(0)
    if not register.startswith('报名方式：'):
        raise ValueError('无法识别报名方式，请确认该行开头是否与示例保持一致')
    event.register = register[5:]

    live = lines.pop(0)
    if not live.startswith('直播地址：'):
        raise ValueError('无法识别直播地址，请确认该行开头是否与示例保持一致')
    event.live = live[5:]

    return event
