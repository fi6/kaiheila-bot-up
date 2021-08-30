from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING

import configs
import requests
from core import polling
from models import VideoUpdate, YTVideo
from PIL import Image
from io import BytesIO
from urllib.request import urlopen

from ._instance import bot

if TYPE_CHECKING:
    from core.types import LiveInfo


async def live_notif(living: LiveInfo):
    logging.info('received live start event')
    card = living.to_card()
    await bot.send(configs.channel.chat, json.dumps(card), type=10)
    logging.info(await bot.send(configs.channel.notif,
                                json.dumps(card),
                                type=10))


async def video_notif(video: VideoUpdate):
    video = VideoUpdate.objects.get(id=video.id)
    card = video.to_card()
    await bot.send(configs.channel.chat, json.dumps(card), type=10)
    await bot.send(configs.channel.notif, json.dumps(card), type=10)


async def yt_video_notif(video: YTVideo, server):
    channel = server.chat_channel
    image = Image.open(urlopen(video.thumbnail))
    io = BytesIO()
    image.save(io, format='PNG')
    try:
        response = await bot.create_asset(io.getvalue())
        # print(response)
    except Exception as e:
        logging.exception(e.result)
    if not response.get('url'):
        return
    card = video.to_raw_card(response['url'])
    post = await bot.send(channel, json.dumps(card), type=10)
    video.post = post
    video.save()


polling.on('live_start', live_notif)
polling.on('video_update', video_notif)
polling.on('yt_video_update', yt_video_notif)

if len(polling.listeners('live_start')):
    logging.info('[init success] live start sender')
else:
    logging.exception('[init failed] live start sender')
