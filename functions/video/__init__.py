from __future__ import annotations

import logging
from enum import Enum
from typing import Any, Dict, List, Sequence, Union

from khl import Msg

from .._command import MyCommand
from .add import add_video
from .reprint import VideoReprint

# class Category(Enum):
#     GUIDE = '攻略',
#     COMP = '集锦',
#     REPLAY = '录像'
#     OTHER = '其他'

#     @classmethod
#     def get_key(cls, value: str) -> Union[Enum, None]:
#         try:
#             return cls._value2member_map_[(value, )]
#         except Exception as e:
#             logging.error(e)
#             return None


class VideoEntry(MyCommand):
    trigger = ['视频']

    command_map: Dict[str, MyCommand] = {}

    def __init__(self, *commands: MyCommand):
        super().__init__()
        for command in commands:
            for trigger in command.trigger:
                if self.command_map.get(trigger):
                    logging.warn('unexpected conflict on triggers')
                self.command_map[trigger] = command

    async def execute(self, msg: Msg, *args: str):
        if not len(args):
            return await self.entry(msg)
        if args[0] in ['add', '添加']:
            return await self.add(msg, list(args[1:]))
        if args[0] == 'search':
            return await self.search(msg, list(args[1:]))
        if self.command_map.get(args[0]):
            return await self.command_map[args[0]].execute(msg, *args[1:])

    async def entry(self, msg: Msg) -> str:
        pass

    async def add(self, msg: Msg, args: List[str]):
        try:
            await add_video(msg, args)
        except ValueError as e:
            await msg.ctx.bot.send(msg.ctx.channel.id,
                                   e.args[0],
                                   temp_target_id=msg.ctx.user.id)

    async def search(self, msg: Msg, args: List[str]):
        try:
            pass
        except Exception as e:
            await msg.ctx.bot.send(msg.ctx.channel.id,
                                   e.args[0],
                                   temp_target_id=msg.ctx.user.id)


video_entry = VideoEntry(VideoReprint())
