import sys

sys.path.append('.')
from csv import reader

import core
import functions
from bilibili_api import utils
from models.__event import _Address
from models.group import (CharGroup, GeneralGroup, JoinType, OfflineGroup,
                          OtherGroup)
from utils.deprecated_char_parser import char_parser


def get_join_type(contact_type: str) -> JoinType:
    if contact_type == 'QQ群号':
        return JoinType.QQ
    if contact_type == '微信好友':
        return JoinType.WECHAT
    if contact_type == '开黑啦链接':
        return JoinType.KHL
    else:
        return JoinType.OTHER


def import_group():
    with open('test/groups.csv', 'r') as csv_file:
        csv_reader = reader(csv_file)

        for row in csv_reader:
            title = row[0]
            contact_type = row[1]
            contact = row[2]
            type = row[3]
            address = row[4]
            char = row[5]
            remark = row[6]
            try:
                if type == '线下群':
                    group = OfflineGroup()
                    group.name = title
                    group.contact = contact
                    group.join_type = get_join_type(contact_type)
                    group.address = _Address.from_str(address)
                    group.remark = remark
                elif type == '角色群':
                    group = CharGroup()
                    group.name = title
                    group.contact = contact
                    group.join_type = get_join_type(contact_type)
                    group.char = char_parser(char)
                    group.remark = remark
                elif type == '综合群':
                    group = GeneralGroup()
                    group.name = title
                    group.contact = contact
                    group.join_type = get_join_type(contact_type)
                    group.remark = remark
                else:
                    group = OtherGroup()
                    group.name = title
                    group.contact = contact
                    group.join_type = get_join_type(contact_type)
                    group.remark = remark

                group.save()
                print(group.name, group.type, group.join_type, group.contact)
                group = None
            except Exception as e:
                print(group.name)
                print(e)


import_group()