from __future__ import annotations
from typing import Any, Dict, List
from models import VerifiedUp


class LiveInfo(object):
    __slots__ = [
        'live_status', 'round_status', 'url', 'title', 'cover', 'online',
        'roomid', 'name', 'avatar', 'sign', 'mid'
    ]
    live_status: int
    round_status: int
    url: str
    title: str
    cover: str
    online: int
    roomid: int
    mid: int

    def __init__(self, live_info_response: Dict[str, Any]) -> None:
        self.live_status = live_info_response['live_status']
        self.mid = int(live_info_response['uid'])

    def add_extra(self, extra_info: Dict[str, Any]):
        self.name = extra_info['name']
        self.avatar = extra_info['face']
        self.sign = extra_info['sign']
        room = extra_info['live_room']
        self.live_status = int(room['liveStatus'])
        self.round_status = room['roundStatus']
        self.url = room['url']
        self.title = room['title']
        self.cover = room['cover']
        self.online = room['online']
        self.roomid = int(room['roomid'])

    def to_card(self) -> List[Dict[str, Any]]:
        try:
            up: VerifiedUp = VerifiedUp.objects.get(uid=self.mid)
        except Exception:
            up = None
        return [
            {
                "type":
                "card",
                "theme":
                "warning",
                "size":
                "lg",
                "modules": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain-text",
                            "content": "开播提醒"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "kmarkdown",
                            "content": "**{user}刚刚开播了！**".format(
                                user=self.name
                            )  #  if not up else f'{self.name} (met){up.kid}(met)')
                        },
                        "mode": "left",
                        "accessory": {
                            "type": "image",
                            "src": self.avatar,
                            "circle": True,
                            "size": "sm"
                        }
                    },
                    {
                        "type": "context",
                        "elements": [{
                            "type": "plain-text",
                            "content": self.sign
                        }]
                    }
                ]
            },
            {
                "type":
                "card",
                "theme":
                "secondary",
                "size":
                "lg",
                "modules": [{
                    "type": "section",
                    "text": {
                        "type":
                        "kmarkdown",
                        "content":
                        "直播间标题：\n**{title}**\n[点击前往观看]({url})".format(
                            title=self.title, url=self.url)
                    }
                }, {
                    "type": "image-group",
                    "elements": [{
                        "type": "image",
                        "src": self.cover
                    }]
                }]
            }
        ]


# {
#     'roomStatus':
#     1,
#     'roundStatus':
#     1,
#     'liveStatus':
#     0,
#     'url':
#     'https://live.bilibili.com/63319',
#     'title':
#     '冰飞FlappyIce的投稿视频',
#     'cover':
#     'http://i0.hdslb.com/bfs/live/keyframe020700210000000633190l4cx9.jpg',
#     'online':
#     0,
#     'roomid':
#     63319,
#     'broadcast_type':
#     0,
#     'online_hidden':
#     0,
#     'link':
#     'https://live.bilibili.com/63319?accept_quality=%5B4%5D&broadcast_type=0&current_qn=10000&current_quality=10000&is_room_feed=0&p2p_type=0&playurl_h264=http%3A%2F%2Fd1--cn-gotcha05.bilivideo.com%2Flive-bvc%2F603454%2Flive_2607110_9639553.flv%3Fcdn%3Dcn-gotcha05%26expires%3D1615242866%26len%3D0%26oi%3D1214109966%26pt%3D%26qn%3D10000%26trid%3D8f96465a12854207a0471224be529618%26sigparams%3Dcdn%2Cexpires%2Clen%2Coi%2Cpt%2Cqn%2Ctrid%26sign%3Da9694957250547c9994a94ef74da0616%26ptype%3D0%26src%3D8%26sl%3D1%26order%3D1&playurl_h265=&quality_description=%5B%7B%22qn%22%3A10000%2C%22desc%22%3A%22%E5%8E%9F%E7%94%BB%22%7D%5D'
# }

# {
#     'mid': 2607110,
#     'name': '冰飞FlappyIce',
#     'sex': '男',
#     'face':
#     'http://i0.hdslb.com/bfs/face/7b8c3171b0c7f22fe72b66221507badf523966c3.jpg',
#     'sign': '任天堂明星大乱斗玩家',
#     'rank': 10000,
#     'level': 5,
#     'jointime': 0,
#     'moral': 0,
#     'silence': 0,
#     'birthday': '03-29',
#     'coins': 0,
#     'fans_badge': True,
#     'official': {
#         'role': 0,
#         'title': '',
#         'desc': '',
#         'type': -1
#     },
#     'vip': {
#         'type': 2,
#         'status': 1,
#         'theme_type': 0,
#         'label': {
#             'path': '',
#             'text': '年度大会员',
#             'label_theme': 'annual_vip'
#         },
#         'avatar_subscript': 1,
#         'nickname_color': '#FB7299'
#     },
#     'pendant': {
#         'pid':
#         3609,
#         'name':
#         '雪未来',
#         'image':
#         'http://i2.hdslb.com/bfs/garb/item/0cc9d8cfa62d589c9caac1da2e52f0365514941a.png',
#         'expire':
#         0,
#         'image_enhance':
#         'http://i2.hdslb.com/bfs/garb/item/14d4fa56eecc644dfaef423de52d2ff5fa893192.webp',
#         'image_enhance_frame':
#         'http://i2.hdslb.com/bfs/garb/item/2d0d07c9f7e960e1085a3e84361500b5163c1c76.png'
#     },
#     'nameplate': {
#         'nid': 4,
#         'name': '青铜殿堂',
#         'image':
#         'http://i1.hdslb.com/bfs/face/2879cd5fb8518f7c6da75887994c1b2a7fe670bd.png',
#         'image_small':
#         'http://i0.hdslb.com/bfs/face/6707c120e00a3445933308fd9b7bd9fad99e9ec4.png',
#         'level': '普通勋章',
#         'condition': '单个自制视频总播放数>=1万'
#     },
#     'is_followed': False,
#     'top_photo':
#     'http://i1.hdslb.com/bfs/space/cb1c3ef50e22b6096fde67febe863494caefebad.png',
#     'theme': {},
#     'sys_notice': {},
#     'live_room': {
#         'roomStatus': 1,
#         'liveStatus': 0,
#         'url': 'https://live.bilibili.com/63319',
#         'title': '冰飞FlappyIce的投稿视频',
#         'cover':
#         'http://i0.hdslb.com/bfs/live/keyframe020700210000000633190l4cx9.jpg',
#         'online': 0,
#         'roomid': 63319,
#         'roundStatus': 1,
#         'broadcast_type': 0
#     }
# }
