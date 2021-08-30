import sys
sys.path.append('.')
from models.__event import OfflineEvent
from functions.event import get_address, get_time

text = """时间：8月30日20:00
地址：北京市东城区方家胡同野友趣
简介：北京周赛
"""

demo = """标题：北京周赛 #61
时间：8月30日 20:00
地址：北京市东城区方家胡同xx号野友趣
简介：北京周赛！晚上18:00开门，本周同时有双打，可以来玩。请尽量带setup！
联系方式：微信xxxxx（加好友）/QQ群xxxx
活动费用：购买饮料或任意食物
报名方式：微信群内报名 / https://smash.gg/xxxxxx/register
直播地址：暂无 / https://live.bilibili.com/xxxxx
"""


def parser(text: str) -> OfflineEvent:
    event = OfflineEvent()
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


result = parser(demo)
print(result.__dict__)
