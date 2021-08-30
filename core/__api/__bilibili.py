from datetime import date, datetime, timedelta
from random import random
from re import U
from typing import Any, Callable, Dict, List
from bilibili_api import live, user, video, channel, Credential, video_uploader
from mongoengine.errors import DoesNotExist
from core.types import LiveInfo
import logging
import asyncio
from models import VideoArchive, Up, VerifiedUp
import configs.auth


class __Bilibili():
    interval = 1
    jitter = 0.5
    last_time = datetime.now()
    credential = Credential(sessdata=configs.auth.bili_auth['sessdata'],
                            bili_jct=configs.auth.bili_auth['bili_jct'],
                            buvid3=configs.auth.bili_auth['buvid3'])

    async def check_frequency(self):
        if datetime.now() - self.last_time < timedelta(seconds=self.interval):
            self.last_time = datetime.now()
            await asyncio.sleep(self.interval + self.jitter * random())
        else:
            self.last_time = datetime.now()
        return

    async def add_user_info(self, info: LiveInfo):
        await self.check_frequency()
        user_info = await self.update_user_info(info.mid)
        logging.info('live start user info : {info}'.format(info=user_info))
        info.add_extra(user_info)
        return info

    async def update_user_info(self, uid: int):
        u = user.User(uid=uid)
        info = await u.get_user_info()
        try:
            up = Up.objects.get(uid=uid)
        except DoesNotExist:
            up = Up(uid=uid)
        up.update_from_info(info)
        return info

    async def get_live_info(self, room_display_id: int):
        await self.check_frequency()
        lv = live.LiveRoom(room_display_id=room_display_id)
        info = lv.get_room_play_info()
        return await info

    async def get_user_videos(self, uid: int):
        await self.check_frequency()
        u = user.User(uid=uid)
        vids = await u.get_videos()
        if not vids:
            raise ValueError('no user videos got for {}'.format(uid))
        return vids['list']['vlist']

    async def get_video_info(self, bvid: str) -> Dict[str, Any]:
        await self.check_frequency()
        v = video.Video(bvid=bvid)
        return await v.get_info()

    async def get_video_tags(self, bvid: str):
        await self.check_frequency()
        v = video.Video(bvid=bvid)
        return await v.get_tags()

    async def get_video_archive_doc(self, bvid: str, save=False):
        vid_all = await self.get_video_info(bvid)
        tags = await self.get_video_tags(bvid)
        tag_names: List[str] = [t['tag_name'] for t in tags]
        fields = VideoArchive._fields.keys()
        vid_doc = VideoArchive(
            **{k: v
               for k, v in vid_all.items() if k in fields})
        vid_doc._raw = vid_all
        vid_doc.publish = datetime.fromtimestamp(vid_all['pubdate'])
        vid_doc.uid = vid_all['owner']['mid']
        vid_doc.tags = tag_names
        vid_doc.author = vid_all['owner']['name']
        if save:
            vid_doc.save()
        return vid_doc

    async def submit_video(self, title: str, characters: List[str], id: str,
                           desc: str, video_path,
                           cover_path) -> Dict[str, str]:
        page = video_uploader.VideoUploaderPage(open(video_path, 'rb'),
                                                title=id)
        config = {
            "copyright": 2,  # "1 自制，2 转载。",
            "source": 'https://www.youtube.com/watch?v={}'.format(
                id),  # "str, 视频来源。投稿类型为转载时注明来源，为原创时为空。",
            "desc": desc,  # "str, 视频简介。",
            "desc_format_id": 0,
            "dynamic": "",  # "str, 动态信息。",
            "interactive": 0,
            "open_elec": 0,  # "int, 是否展示充电信息。1 为是，0 为否。",
            "no_reprint": 0,  # "int, 显示未经作者授权禁止转载，仅当为原创视频时有效。1 为启用，0 为关闭。",
            "subtitles": {
                "lan": "",  # "字幕语言，不清楚作用请将该项设置为空",
                "open": 0
            },
            "tag": "任天堂明星大乱斗,比赛录像," +
            ','.join(characters),  # "str, 视频标签。使用英文半角逗号分隔的标签组。示例：标签1,标签2,标签3",
            "tid": 17,  # "int, 分区ID。可以使用 channel 模块进行查询。",
            "title": title,  # "视频标题",
            "up_close_danmaku": False,  # "bool, 是否关闭弹幕。",
            "up_close_reply": False,  # "bool, 是否关闭评论。",
        }

        uploader = video_uploader.VideoUploader(
            cover_stream=open(cover_path, 'rb'),
            cover_type='image/png',
            pages=[page],
            meta=config,
            credential=video_uploader.VideoUploaderCredential(
                access_key=configs.auth.bili_auth['access_key']),
            threads=1)
        logging.info('uploading {}'.format(config['title']))

        @uploader.on("__ALL__")
        async def ev(data):
            print(data)

        all_chunks = []

        async def chunk_begin_handler(e):
            logging.info('start chunk: {}, total chunk: {}'.format(
                e['chunk_index'], e['total_chunk']))
            if not len(all_chunks):
                for i in range(1, e['total_chunk'] + 1):
                    all_chunks.append(i)

        async def chunk_finish_handler(e):
            index = all_chunks.index(e['chunk_index'])
            all_chunks.pop(index)
            logging.info('finish chunk: {}\nremaining: {}'.format(
                e['chunk_index'], all_chunks))

        uploader.add_event_listener('CHUNK_BEGIN', chunk_begin_handler)
        uploader.add_event_listener('CHUNK_END', chunk_finish_handler)
        result = await uploader.start()
        print(result)
        if not result:
            raise ValueError('上传可能失败了……而且没有错误信息，这很坑爹，请联系冰飞')
        return result


# UPLOAD_CONFIG = {
#   "copyright": 1, #"1 自制，2 转载。",
#   "source": "", #"str, 视频来源。投稿类型为转载时注明来源，为原创时为空。",
#   "desc": "", #"str, 视频简介。",
#   "desc_format_id": 0,
#   "dynamic": "", #"str, 动态信息。",
#   "interactive": 0,
#   "open_elec": 0, #"int, 是否展示充电信息。1 为是，0 为否。",
#   "no_reprint": 1, #"int, 显示未经作者授权禁止转载，仅当为原创视频时有效。1 为启用，0 为关闭。",
#   "subtitles": {
#     "lan": "", #"字幕语言，不清楚作用请将该项设置为空",
#     "open": 0
#   },
#   "tag": "学习,测试", #"str, 视频标签。使用英文半角逗号分隔的标签组。示例：标签1,标签2,标签3",
#   "tid": 208, #"int, 分区ID。可以使用 channel 模块进行查询。",
#   #"title": "英语测试第一弹", #"视频标题",
#   "up_close_danmaku": False, #"bool, 是否关闭弹幕。",
#   "up_close_reply": False, #"bool, 是否关闭评论。",
# }