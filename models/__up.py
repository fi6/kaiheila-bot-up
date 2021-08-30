from datetime import datetime
from typing import Any, Dict, List
from mongoengine import Document
from mongoengine.fields import DateTimeField, DynamicField, IntField, ListField, StringField


class Up(Document):
    _raw: Dict[str, Any] = DynamicField()
    uid: int = IntField(required=True, unique=True)
    roomid: int = IntField(db_field='room')
    avatar: str = StringField()
    nickname: str = StringField()
    sign: str = StringField()
    updated_at = DateTimeField(default=datetime.now, db_field='updatedAt')
    meta = {'allow_inheritance': True, 'collection': 'ups'}

    def update_from_info(self, info):
        self._raw = info
        self.avatar = info['face']
        self.nickname = info['name']
        self.sign = info['sign']
        self.updated_at = datetime.now()


class VerifiedUp(Up):
    follower_role: str = IntField(db_field='follower')
    kid: str = StringField()
    # 0: normal, -1: below, 1: high
    priority: int = IntField()
    tag: List[str] = ListField(StringField())


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