import json
import logging
from typing import Any, Dict, List
from urllib.parse import urlparse

import configs
import core
from cacheout import Cache
from core.__video import char_dict, char_parser
from khl.message import Msg
from models import VideoArchive, VideoTypes
from utils import link_parser

archive_cache = Cache(ttl=300, default=None)


async def add_video(msg: Msg, args: List[str]):
    # args: ['https://bilibili.com/xxx', 'guide']
    if not len(args):
        # cards shows basic video info and button for add this video into category  # noqa
        await msg.ctx.send_temp('请在30秒内输入视频链接，目前仅支持b站视频')
        input = await msg.ctx.wait_user(msg.ctx.user_id)
        if not input.msg_id:
            raise ValueError('没有收到输入。如需添加视频，请重新开始。')
        bvid = link_parser(input.content)
        if not bvid:
            raise ValueError('无法解析视频链接，请检查。如果这是一个误报，请在反馈频道描述问题。')
        archive = await core.api.bilibili.get_video_archive_doc(bvid)
        archive_cache.set(bvid, archive)
        await msg.ctx.send_card_temp(json.dumps(add_start_card(archive)))
        return

    elif len(args) == 1 and args[0].startswith('BV'):
        # user sent a link and catched by bot, asking whether add or not
        archive = archive_cache.get(args[0])
        if not archive_cache.get(args[0]):
            archive = await core.api.bilibili.get_video_archive_doc(args[0])
            archive_cache.set(archive.bvid, archive)
        if not archive:
            raise ValueError('无法找到对应的视频。如果这是一个错误，请在反馈频道寻求帮助。')
        await msg.ctx.send_card_temp(
            json.dumps(add_start_card(archive, auto=True)))
        return

    elif len(args) == 2:
        bvid = args[1]
        category = args[0]
        # input character
        archive = archive_cache.get(bvid)
        if not archive_cache.get(bvid):
            archive = await core.api.bilibili.get_video_archive_doc(bvid)
        archive_cache.set(archive.bvid, archive)
        if not archive:
            raise ValueError('无法找到对应的视频。如果这是一个错误，请在反馈频道寻求帮助。')
        archive.category = VideoTypes[category]

        await msg.ctx.send_temp(
            '请输入视频相关的角色，没有请发送`无`。' + '\n多个角色请用逗号分开，可以识别斗士编号、中英文名、常见昵称。' +
            '\n完整的角色列表请[点击查看](https://docs.qq.com/sheet/DS1liRnRpT1ZTUVpZ?tab=BB08J2)'
            + '\n示例：joker, 桃子，12')
        await msg.ctx.user.grant_role(msg.ctx.bot, configs.roles.guild,
                                      configs.roles.temp_input)
        input = await msg.ctx.wait_user(msg.ctx.user_id, 120)
        await msg.ctx.user.revoke_role(msg.ctx.bot, configs.roles.guild,
                                       configs.roles.temp_input)
        if not input.msg_id:
            raise ValueError('输入超时，请重新开始')
        char_result = char_parser(input.content)
        archive.char = char_result
        await msg.ctx.send_card_temp(json.dumps(char_confirm_card(archive)))
        return

    elif len(args) == 3:
        bvid = args[1]
        category = args[0]
        chars = args[2]
        archive: VideoArchive = archive_cache.get(bvid)
        if not archive:
            raise ValueError('未能获取到视频，是否等待时间过长？请尝试重新开始。')
        archive_cache.set(archive.bvid, archive)
        await msg.ctx.send_temp('请输入推荐语，如：新手向，空后讲解的很详细')
        await msg.ctx.user.grant_role(msg.ctx.bot, configs.roles.guild,
                                      configs.roles.temp_input)
        input = await msg.ctx.wait_user(msg.ctx.user_id, 120)
        await msg.ctx.user.revoke_role(msg.ctx.bot, configs.roles.guild,
                                       configs.roles.temp_input)
        if not input.msg_id:
            raise ValueError('输入超时，请重新开始')
        archive.remark = input.content
        archive.referrer = input.ctx.user_id

        sent = await msg.ctx.bot.send(configs.channel.notif,
                                      json.dumps(archive.to_card()),
                                      type=10)
        try:
            archive.msg = sent.get('msg_id')
        except Exception as e:
            logging.error(e)
        archive.save()
        await msg.ctx.send_temp('视频已添加至档案库，请前往(chn){channel}(chn)查看。'.format(
            channel=configs.channel.notif))


def add_start_card(archive: VideoArchive, auto=False):
    card = [] if not auto else [{
        "type":
        "card",
        "theme":
        "secondary",
        "size":
        "sm",
        "modules": [{
            "type": "section",
            "text": {
                "type": "kmarkdown",
                "content": "检测到b站视频！请问是否要添加至视频档案库？"
            }
        }]
    }]
    return [
        *card, {
            "type":
            "card",
            "theme":
            "secondary",
            "size":
            "sm",
            "modules": [{
                "type": "header",
                "text": {
                    "type": "plain-text",
                    "content": "添加视频到档案库"
                }
            }, {
                "type": "image-group",
                "elements": [{
                    "type": "image",
                    "src": archive.pic
                }]
            }, {
                "type": "section",
                "text": {
                    "type":
                    "kmarkdown",
                    "content":
                    "**{title}**\n作者：{author}".format(title=archive.title,
                                                      author=archive.author)
                }
            }]
        }, {
            "type":
            "card",
            "theme":
            "primary",
            "size":
            "lg",
            "modules": [{
                "type": "section",
                "text": {
                    "type": "kmarkdown",
                    "content": "请选择视频分类以进行添加"
                }
            }, {
                "type":
                "action-group",
                "elements": [{
                    "type":
                    "button",
                    "click":
                    "return-val",
                    "theme":
                    "primary",
                    "value":
                    ".菜单 视频 添加 GUIDE {bvid}".format(bvid=archive.bvid),
                    "text": {
                        "type": "plain-text",
                        "content": "通用攻略"
                    }
                }, {
                    "type":
                    "button",
                    "click":
                    "return-val",
                    "theme":
                    "primary",
                    "value":
                    ".菜单 视频 添加 CHARGUIDE {bvid}".format(bvid=archive.bvid),
                    "text": {
                        "type": "plain-text",
                        "content": "角色攻略"
                    }
                }, {
                    "type":
                    "button",
                    "click":
                    "return-val",
                    "theme":
                    "primary",
                    "value":
                    ".菜单 视频 添加 REPLAY {bvid}".format(bvid=archive.bvid),
                    "text": {
                        "type": "plain-text",
                        "content": "比赛录像"
                    }
                }, {
                    "type":
                    "button",
                    "click":
                    "return-val",
                    "theme":
                    "primary",
                    "value":
                    ".菜单 视频 添加 COMP {bvid}".format(bvid=archive.bvid),
                    "text": {
                        "type": "plain-text",
                        "content": "精彩集锦"
                    }
                }]
            }, {
                "type":
                "action-group",
                "elements": [{
                    "type":
                    "button",
                    "click":
                    "return-val",
                    "theme":
                    "primary",
                    "value":
                    ".菜单 视频 添加 FUN {bvid}".format(bvid=archive.bvid),
                    "text": {
                        "type": "plain-text",
                        "content": "趣味视频"
                    }
                }, {
                    "type":
                    "button",
                    "click":
                    "return-val",
                    "theme":
                    "primary",
                    "value":
                    ".菜单 视频 添加 INTRO {bvid}".format(bvid=archive.bvid),
                    "text": {
                        "type": "plain-text",
                        "content": "背景知识"
                    }
                }, {
                    "type":
                    "button",
                    "click":
                    "return-val",
                    "theme":
                    "primary",
                    "value":
                    ".菜单 视频 添加 OTHER {bvid}".format(bvid=archive.bvid),
                    "text": {
                        "type": "plain-text",
                        "content": "其他"
                    }
                }]
            }]
        }
    ]


def char_confirm_card(archive: VideoArchive):
    char_names = [char_dict[char][0] for char in archive.char]
    return [{
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
                "识别到的角色为`{char}`".format(
                    char=' '.join(char_names) if len(char_names) else '无角色')
            }
        }, {
            "type":
            "action-group",
            "elements": [{
                "type":
                "button",
                "click":
                "return-val",
                "theme":
                "success",
                "value":
                ".菜单 视频 添加 {type} {bvid} {char}".format(
                    type=archive.category.name,
                    bvid=archive.bvid,
                    char=','.join(archive.char) if len(archive.char) else 0),
                "text": {
                    "type": "plain-text",
                    "content": "确认添加"
                }
            }, {
                "type":
                "button",
                "click":
                "return-val",
                "theme":
                "warning",
                "value":
                ".菜单 视频 添加 {type} {bvid}".format(type=archive.category.name,
                                                 bvid=archive.bvid),
                "text": {
                    "type": "plain-text",
                    "content": "重新填写"
                }
            }]
        }]
    }]
