from __future__ import annotations
import asyncio
from typing import List

from bilibili_api import live
import core
import logging

from core.types import LiveInfo
from cacheout import Cache
from models import VerifiedUp
import random

living_cache = Cache(ttl=300, default=None)


async def check() -> LiveInfo | None:
    ups: List[VerifiedUp] = VerifiedUp.objects(tag='live')
    roomlist = list(filter(lambda x: x.roomid, ups))
    sleep_time = 10 + random.random() * 0.5
    for i, up in enumerate(roomlist):
        await asyncio.sleep(sleep_time)
        last_info: LiveInfo | None = living_cache.get(up.roomid)
        if not last_info:
            info = LiveInfo(await core.api.bilibili.get_live_info(up.roomid))
            logging.info('{} expired in cache'.format(
                (up.nickname, up.roomid)))
            living_cache.set(up.roomid, info)
            continue
        elif last_info.live_status != 1:
            logging.info('checking live info for {}'.format(
                (up.nickname, up.roomid)))
            info = LiveInfo(await core.api.bilibili.get_live_info(up.roomid))
            living_cache.set(up.roomid, info)
            # logging.debug(living_cache.expire_times())
            if info.live_status == 1:
                # just start living
                logging.info(
                    'found live start for {}, adding user info'.format(
                        up.nickname))
                return await core.api.bilibili.add_user_info(info)
        elif last_info.live_status == 1:
            pass
            # logging.debug('living')
        if i == len(roomlist) - 1:
            break

    return None


def get_room_info():
    pass