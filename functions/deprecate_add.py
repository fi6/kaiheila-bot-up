from __future__ import annotations
from typing import Any, Dict, Sequence, Union

from khl.command import Command
from khl import Msg
from khl.message import TextMsg

from utils.link_parser import link_parser
from enum import Enum
from utils.db import archives
from bilibili_api import video
from ._instance import bot

# class Category(Enum):
#     GUIDE = '攻略',
#     COMP = '集锦',
#     REPLAY = '录像'
#     OTHER = '其他'

#     @classmethod
#     def get_key(cls, value: str) -> Union[Enum, None]:
#         try:
#             return cls._value2member_map_[(value, )]
#         except:
#             return None

# @bot.command(name='添加')
# async def add(self, msg: TextMsg):

#     bvid = await link_parser(link)

#     if not bvid:
#         await msg.reply_temp('不是有效的b站链接，请检查。如果这是一个误报，请在反馈频道描述问题。')
#         return

#     video_info: Dict[str, Any] | None = video.get_video_info(bvid=bvid)
#     video_tags: Sequence[str] = video.get_tags(bvid=bvid)

#     if not video_info:
#         return await msg.reply('无法从b站爬取~')

#     new_archive = {
#         'char': char,
#         'category': category,
#         'link': link,
#         'bvid': video_info['bvid'],
#         'owner': video_info['owner']['name'],
#         'title': video_info['title'],
#         'pubdate': video_info['pubdate']
#     }
#     archives.find({'bvid': link})
#     new_archive_doc = archives.insert_one(new_archive)
#     await msg.reply('档案已添加')
