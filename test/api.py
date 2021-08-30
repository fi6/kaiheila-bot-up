import sys

sys.path.append('.')

import logging
import asyncio

import core
from bilibili_api import live, user
from core.__polling._check_video import create_video_doc
from core.types.__video import UserVideo
from models import VerifiedUp


# ups = VerifiedUp.objects(tag='video', priority=1)
# print(ups)

# u = user.get_user_info(22295969)
# up = VerifiedUp(uid=u['mid'],
#                 roomid=u['live_room']['roomid'],
#                 avatar=u['face'],
#                 nickname=u['name'],
#                 sign=u['sign'],
#                 priority=-1,
#                 tag=['video'])
# up.save()
async def main():
    lv = live.LiveRoom(room_display_id=63319)
    print(await lv.get_room_play_info())
    return
    u = user.User(2607110)
    print(await u.get_user_info())
    # print(await u.get_videos())
    vids = await core.api.bilibili.get_user_videos(2607110)
    for vid in vids:
        vid = UserVideo(**vid)
        print(vid)
        try:
            vid_all = await core.api.bilibili.get_video_info(vid.bvid)
            tags = await core.api.bilibili.get_video_tags(vid.bvid)
            tag_names = [t['tag_name'] for t in tags]
            vid_doc = create_video_doc(vid_all, tag_names, None, False)
            print(vid_doc.to_mongo())
        except Exception as e:
            logging.error(e)


asyncio.get_event_loop().run_until_complete(main())
