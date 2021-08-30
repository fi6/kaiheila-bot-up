from __future__ import annotations

import asyncio
import re

from pymongo.errors import DuplicateKeyError
import core
from datetime import datetime
import logging
from random import random
from typing import List

from core.types import UserVideo
from models import VideoUpdate, VerifiedUp
from models.__video import _Video


async def check_video(priority: int):
    # get up list
    ups: List[VerifiedUp] = VerifiedUp.objects(tag='video', priority=priority)
    uplist = [up.uid for up in ups]
    # calculate sleep time
    sleep_time = 3 * (2 - priority) + 2 * random()
    logging.info('priority: {p}, up list total: {total}'.format(
        p=priority, total=len(uplist)))
    for up in ups:
        id = up.uid
        logging.info('fetching videos for {}'.format((up.nickname, id)))
        existing = _Video.objects(
            uid=int(id)).order_by('-publish').only('bvid')[:16]
        exist_bvids = [v.bvid for v in existing]
        cnt = 0
        for vid in await core.api.bilibili.get_user_videos(int(id)):
            vid = UserVideo(**vid)
            if cnt >= 8:
                break
            cnt += 1
            if vid.bvid in exist_bvids:
                continue
            vid_all = None
            try:
                vid_all = await core.api.bilibili.get_video_info(vid.bvid)
                tags = await core.api.bilibili.get_video_tags(vid.bvid)
                tag_names: List[str] = [t['tag_name'] for t in tags]
                if '任天堂明星大乱斗' not in tag_names and not up.priority == 1:
                    logging.debug('no smash tag', (vid_all, tag_names))
                    continue
                vid_doc = create_video_doc(vid_all, tag_names, verified_up=up)
                # print(vid_doc)
                yield vid_doc
                logging.info('added new video: {vid}'.format(vid=vid_all))
            except DuplicateKeyError:
                video: _Video = _Video.objects.get(bvid=vid.bvid)
                if vid_all is not None:
                    video._raw = vid_all
                    video.author = vid_all['owner']['name']
                    video.publish = datetime.fromtimestamp(vid_all['pubdate'])
                    video.save()
            except Exception as e:
                logging.error(e)
                logging.error(('exist_bvids:', exist_bvids))

            await asyncio.sleep(random())

        await asyncio.sleep(sleep_time)


def create_video_doc(vid_all,
                     tag_names,
                     verified_up: VerifiedUp | None = None,
                     save=True):
    fields = VideoUpdate._fields.keys()
    vid_doc = VideoUpdate(**{k: v for k, v in vid_all.items() if k in fields})
    vid_doc._raw = vid_all
    vid_doc.publish = datetime.fromtimestamp(vid_all['pubdate'])
    vid_doc.uid = vid_all['owner']['mid']
    vid_doc.tags = tag_names
    vid_doc.author = vid_all['owner']['name']
    if vid_all['copyright'] == 1:
        vid_doc.original = True
    else:
        vid_doc.original = False
        source = re.search(r'^http.+?(?:$|\n)', vid_doc.desc)
        if not source:
            source = re.search(r'^.+?(?:$|\n)', vid_doc.desc)
        vid_doc.source = source.group(0).strip() if source else ''
    if verified_up:
        vid_doc.up_ref = verified_up
    if save:
        vid_doc.save()
    return vid_doc
