from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List
from urllib.parse import urlparse
import cpca

from mongoengine import Document
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import (BooleanField, DateTimeField,
                                EmbeddedDocumentField, IntField, StringField)

GREATER_ADMIN_AREA = {
    '1': '华北',
    '2': '东北',
    '3': '华东',
    '4': '中南',
    '5': '西南',
    '6': '西北',
    '7': '台湾',
    '8': '港澳台'
}


class _Address(EmbeddedDocument):
    province = StringField(required=True)
    city = StringField()
    district = StringField()
    detail = StringField()
    code = IntField(required=True)

    def to_string(self):
        if self.city == '市辖区':
            return ' '.join([self.province, self.district, self.detail])
        return ' '.join(
            list(
                filter(
                    None,
                    [self.province, self.city, self.district, self.detail])))

    @classmethod
    def from_str(cls, input):
        df = cpca.transform([input])
        result: dict = df.iloc[0].to_dict()
        if result['省']:
            return cls(province=result['省'],
                       city=result['市'],
                       district=result.get('区'),
                       detail=result.get('地址'),
                       code=result.get('adcode'))

    @property
    def _greater_admin_area(self):
        number = str(self.code)[0]
        return GREATER_ADMIN_AREA[number] + '地区'


class _Event(Document):
    user = StringField(required=True)
    title = StringField(required=True)
    register = StringField(required=True)
    address = EmbeddedDocumentField(_Address, default=_Address())
    start = DateTimeField(required=True)
    end = DateTimeField()
    contact = StringField(required=True)
    info = StringField()
    series = BooleanField(default=False)
    code = StringField()
    live = StringField()
    publish = StringField()
    meta = {'allow_inheritance': True, 'collection': 'events'}

    @property
    def start_time_str(self):
        time: datetime = self.start
        return time.strftime('%m月%d日 %H:%M')

    def to_card(self) -> List[Dict[str, Any]]:
        raise NotImplementedError()

    def to_raw_info(self) -> str:
        raise NotImplementedError()


class OnlineEvent(_Event):
    pass

    def to_card(self):
        if urlparse(str(self.register)).scheme:
            register = '[点击报名]({url})'.format(url=self.register)
        else:
            register = self.register
        return [{
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
                        "content": "线上活动通知"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "kmarkdown",
                        "content": "**{title}**".format(title=self.title)
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type":
                        "kmarkdown",
                        "content":
                        "**时间**：{time}\n**简介**：{info}\n**直播地址**：{live}\n**联系方式**：{contact}"  # noqa
                        .format(time=self.start,
                                live=f'[点击进入直播间]({self.live})',
                                info=self.info,
                                contact=self.contact)
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type":
                        "kmarkdown",
                        "content":
                        "**报名方式**：{register}\n由{user}提交".format(
                            register=register, user=f'(met){self.user}(met)')
                    }
                }
            ]
        }]

    def to_raw_info(self) -> str:
        return super().to_raw_info()


class OfflineEvent(_Event):
    fee = StringField()

    def to_card(self):
        if urlparse(str(self.register)).scheme:
            register = '[点击报名]({url})'.format(url=self.register)
        else:
            register = self.register
        live = f'[点击进入直播间]({self.live})' if urlparse(str(
            self.live)).scheme else self.live
        return [{
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
                        "content": "🎮 线下活动通知"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "kmarkdown",
                        "content": "**{title}**".format(title=self.title)
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type":
                        "kmarkdown",
                        "content":
                        "**时间**：{time}\n**地址**：{address}\n**简介**：{info}\n**联系方式**：{contact}"  # noqa
                        .format(time=self.start,
                                address=self.address.to_string(),
                                info=self.info,
                                contact=self.contact)
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type":
                        "kmarkdown",
                        "content":
                        "**活动费用**：{fee}\n**报名方式**：{register}\n**直播地址**：{live}\n（由{user}提交）"  # noqa
                        .format(fee=self.fee,
                                register=register,
                                live=live,
                                user=f'(met){self.user}(met)')
                    }
                }
            ]
        }]

    def to_raw_info(self):
        first = "标题：{title}\n**时间**：{time}\n**地址**：{address}\n**简介**：{info}\n**联系方式**：{contact}".format(  # noqa
            title=self.title,
            time=self.start,
            address=self.address.to_string(),
            info=self.info,
            contact=self.contact)
        second = "**活动费用**：{fee}\n**报名方式**：{register}\n**直播地址**：{live}".format(
            fee=self.fee, register=self.register, live=self.live)
        return f'{first}\n{second}'
