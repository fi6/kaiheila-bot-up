from __future__ import annotations

from datetime import datetime
from enum import Enum
import logging
from typing import Any, List

from mongoengine import Document
from mongoengine.fields import (BooleanField, DateTimeField, DynamicField,
                                EnumField, IntField, LazyReferenceField,
                                ListField, StringField)
from utils.date import get_time_str

__code_dict = {
    'GUIDE': '通用攻略',
    'CHARGUIDE': '角色攻略',
    'REPLAY': '比赛录像',
    'COMP': '精彩集锦',
    'FUN': '趣味视频',
    'INTRO': '背景知识'
}


class VideoTypes(Enum):
    GUIDE = 'GUIDE'
    CHAR_GUIDE = 'CHARGUIDE'
    REPLAY = 'REPLAY'
    COMPILATION = 'COMP'
    FUN = 'FUN'
    INTRO = 'INTRO'
    OTEHR = 'OTHER'

    @staticmethod
    def get_str(code) -> str:
        result = __code_dict.get(code)
        return result if result else '其他'

    def get_code(string) -> str:
        for code, cn in __code_dict:
            if string == cn:
                return code
        return 'OTHER'


class _Video(Document):
    # _cls = StringField()
    _raw = DynamicField()
    bvid: str = StringField(required=True, unique=True)
    title: str = StringField(required=True)
    desc: str = StringField(required=True)
    uid: int = IntField(required=True, db_field='uid')
    pic = StringField()
    author = StringField()
    publish = DateTimeField()
    duration = IntField()
    up_ref = LazyReferenceField('VerifiedUp', db_field='up', passthrough=True)
    dynamic = StringField()
    tags = ListField(StringField(), default=[])
    remark = StringField()
    original = BooleanField()
    source = StringField()
    meta = {'collection': 'videos', 'allow_inheritance': True}

    # @property
    # def uid(self) -> int:
    #     return self.mid

    def to_card(self) -> List[Any]:
        raise NotImplementedError()


class VideoUpdate(_Video):
    char = ListField(StringField())
    category = EnumField(VideoTypes)
    msg = StringField()

    @property
    def _card_author(self) -> str:

        return f'{self.author} (met){self._khl_id}(met)' if self._khl_id else str(
            self.author)

    @property
    def _khl_id(self) -> str | None:
        try:
            return self.up_ref.kid
        except Exception as e:
            logging.error('fail to get khl_id for video update {}'.format(e))
            return None

    def to_card(self) -> List[Any]:
        return [{
            "type":
            "card",
            "theme":
            "info",
            'color':
            '#FB7299',
            "size":
            "sm",
            "modules": [{
                "type": "image-group",
                "elements": [{
                    "type": "image",
                    "src": self.pic,
                }]
            }]
        }, {
            "type":
            "card",
            "theme":
            "info",
            'color':
            '#FB7299',
            "size":
            "lg",
            "modules": [{
                "type": "header",
                "text": {
                    "type": "plain-text",
                    "content": "视频更新"
                }
            }, {
                "type": "section",
                "text": {
                    "type":
                    "kmarkdown",
                    "content":
                    "**[{title}]({url})**".format(
                        url=f'https://www.bilibili.com/video/{self.bvid}',
                        title=self.title)
                }
            }, {
                "type":
                "context",
                "elements": [{
                    "type": "image",
                    "src": self.up_ref.avatar
                }, {
                    "type":
                    "kmarkdown",
                    "content":
                    "作者: {author}".format(author=self._card_author)
                }]
            }, {
                "type": "divider"
            }, {
                "type": "section",
                "text": {
                    "type":
                    "kmarkdown",
                    "content":
                    "{desc}".format(desc=self.desc if len(self.desc) <= 152
                                    else self.desc[:150] + '...', )
                }
            }, {
                "type":
                "context",
                "elements": [{
                    "type":
                    "kmarkdown",
                    "content":
                    "发布于：{pubdate}".format(pubdate=get_time_str(self.publish))
                }]
            }]
        }]


class VideoRecord(_Video):
    pass


class VideoArchive(_Video):
    category = EnumField(VideoTypes, required=True)
    char = ListField(StringField())
    referrer = StringField()
    msg = StringField()

    def to_card(self) -> List[Any]:
        # if self.up_ref and self.up_ref.kid:
        #     khl_id = self.up_ref.kid
        khl_id = None
        return [{
            "type":
            "card",
            "theme":
            "secondary",
            "size":
            "lg",
            "modules": [{
                "type": "header",
                "text": {
                    "type": "plain-text",
                    "content": "视频档案库新增"
                }
            }, {
                "type": "image-group",
                "elements": [{
                    "type": "image",
                    "src": self.pic
                }]
            }, {
                "type": "section",
                "text": {
                    "type":
                    "kmarkdown",
                    "content":
                    "**[{title}]({url})**\n作者: {author}".format(
                        url=f'https://www.bilibili.com/video/{self.bvid}',
                        title=self.title,
                        author=f'(met){khl_id}(met)'
                        if khl_id else self.author,
                    )
                }
            }]
        }, {
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
                    "{desc}".format(desc=self.desc if len(self.desc) <= 152
                                    else self.desc[:150] + '...', ) +
                    "\n发布于：{pubdate}".format(
                        pubdate=get_time_str(self.publish))
                }
            }, {
                "type": "divider"
            }, {
                "type": "section",
                "text": {
                    "type":
                    "kmarkdown",
                    "content":
                    "由(met){user}(met)推荐".format(user=self.referrer) +
                    '\n推荐语：{remark}'.format(remark=self.remark)
                }
            }]
        }]
