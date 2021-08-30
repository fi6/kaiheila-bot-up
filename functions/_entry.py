import json
from typing import Set
from ._command import MyCommand
from khl.message import Msg


class BotEntry(MyCommand):
    trigger = ['菜单']
    name = 'entry'
    _sub_commands: Set[MyCommand] = set()

    def __init__(self, *sub_commands: MyCommand):
        for command in sub_commands:
            self.add_subcommand(command)

    async def execute(self, msg: Msg, *args: str):
        if not len(args):
            return await self.menu(msg)
        if args[0] == 'help':
            return await self.help(msg)

        for app in self._sub_commands:
            if args[0] in app.trigger:
                args = args[1:]
                await app.execute(msg, *args)

    def add_subcommand(self, cmd: MyCommand):
        self._sub_commands.add(cmd)

    async def menu(self, msg: Msg):
        await msg.ctx.send_card_temp(json.dumps(menu_card()))

    async def help(self, msg: Msg):
        await msg.ctx.send_card_temp(json.dumps(help_card()))


def menu_card():
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
                "content": "斗天堂档案库菜单"
            }
        }, {
            "type": "section",
            "text": {
                "type": "kmarkdown",
                "content": "视频相关"
            }
        }, {
            "type":
            "action-group",
            "elements": [{
                "type": "button",
                "click": "return-val",
                "theme": "primary",
                "value": ".菜单 视频 add",
                "text": {
                    "type": "plain-text",
                    "content": "添加视频"
                }
            }, {
                "type": "button",
                "click": "return-val",
                "theme": "primary",
                "value": ".菜单 视频 search",
                "text": {
                    "type": "plain-text",
                    "content": "检索视频"
                }
            }]
        }, {
            "type": "section",
            "text": {
                "type": "kmarkdown",
                "content": "活动相关"
            }
        }, {
            "type":
            "action-group",
            "elements": [{
                "type": "button",
                "click": "return-val",
                "theme": "primary",
                "value": ".菜单 活动 创建",
                "text": {
                    "type": "plain-text",
                    "content": "创建活动"
                }
            }, {
                "type": "button",
                "click": "return-val",
                "theme": "primary",
                "value": ".菜单 活动 查看",
                "text": {
                    "type": "plain-text",
                    "content": "查看近期活动"
                }
            }, {
                "type": "button",
                "click": "return-val",
                "theme": "primary",
                "value": ".菜单 群 地区",
                "text": {
                    "type": "plain-text",
                    "content": "查找地区群"
                }
            }, {
                "type": "button",
                "click": "return-val",
                "theme": "primary",
                "value": ".菜单 群 角色",
                "text": {
                    "type": "plain-text",
                    "content": "查找角色群"
                }
            }]
        }]
    }]


def help_card():
    pass