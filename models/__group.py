from enum import Enum

from mongoengine import Document
from mongoengine.fields import (BooleanField, EmbeddedDocumentField, EnumField,
                                ListField, StringField)

from .__event import _Address


class GroupType(Enum):
    OFFLINE = 1
    CHARACTER = 2
    GENERAL = 3
    OTHER = 4

    def to_string(self):
        str_dict = {
            'OFFLINE': '线下群',
            'CHARACTER': '角色群',
            'GENERAL': '综合群',
            'OTHER': '其他'
        }
        return str_dict[self.name]


class JoinType(Enum):
    WECHAT = 1
    QQ = 2
    KHL = 3
    OTHER = 4

    def to_string(self):
        str_dict = {
            'WECHAT': '微信好友',
            'QQ': 'QQ群号',
            'KHL': '开黑啦链接',
            'OTEHR': '其他'
        }
        return str_dict[self.name]


class Group(Document):
    name = StringField(required=True)
    type = EnumField(GroupType, required=True)
    join_type = EnumField(JoinType, required=True, db_field='join')
    contact = StringField(required=True)
    remark = StringField()
    address = EmbeddedDocumentField(_Address)
    char = ListField(StringField())
    meta = {'allow_inheritance': True, 'collection': 'groups'}

    def to_card(self):
        return [{}]

    def to_string(self):
        return ''


class OfflineGroup(Group):
    type = EnumField(GroupType, required=True, default=GroupType.OFFLINE)
    address = EmbeddedDocumentField(_Address, required=True)

    def to_string(self):
        return 'this is offline group'


class CharGroup(Group):
    type = EnumField(GroupType, required=True, default=GroupType.CHARACTER)
    char = ListField(StringField(), required=True)

    def to_string(self):
        return 'this is char group'


class GeneralGroup(Group):
    type = EnumField(GroupType, required=True, default=GroupType.GENERAL)

    def to_string(self):
        return 'this is General group'


class OtherGroup(Group):
    type = EnumField(GroupType, required=True, default=GroupType.OTHER)

    def to_string(self):
        return 'this is Other group'
