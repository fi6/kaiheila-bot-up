from __future__ import unicode_literals
import asyncio

import sys

sys.path.append('.')
import os
import re
from typing import List

import configs
import youtube_dl
import core
from bilibili_api import Credential, video, video_uploader
from PIL import Image
from pycaption import DFXPReader, WebVTTWriter


class MyLogger(object):
    def debug(self, msg):
        # print(msg, end="\r")
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    pass
    # print(d.keys(), end='\r')
    # if d['status'] == 'finished':
    #     print('Done downloading, now merging ...')


ydl_opts = {
    'format': 'bestvideo[fps>50][vcodec^=avc1]+bestaudio',
    'merge_output_format': 'mp4',
    # 'listformats': True,
    'logger': MyLogger(),
    'verbose': True,
    'writeautomaticsub': True,
    'subtitleslangs': ['en'],
    'subtitlesformat': 'vtt',
    'outtmpl': 'video_dl/%(id)s-%(title)s.%(ext)s'
    # 'getthumbnail': True,
    # 'progress_hooks': [my_hook],
}

sub_opts = {
    'logger': MyLogger(),
    'verbose': True,
    'writeautomaticsub': True,
    'subtitleslangs': ['zh-Hans', 'en'],
    'subtitlesformat': 'ttml',
    'skip_download': True,
    'outtmpl': 'video_dl/%(id)s-%(title)s.%(ext)s'
    # 'progress_hooks': [my_hook],
}

thumb_opts = {
    'logger': MyLogger(),
    'writethumbnail': True,
    'skip_download': True,
    'outtmpl': 'video_dl/%(id)s-%(title)s.%(ext)s'
}

id = 'My-6TFk90u8'

url = 'https://www.youtube.com/watch?v={}'.format(id)


def download():
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.download([url])

    with youtube_dl.YoutubeDL(sub_opts) as subdl:
        subdl.download([url])

    with youtube_dl.YoutubeDL(thumb_opts) as thumbdl:
        result = thumbdl.download([url])


def get_files(id):
    result = {}
    with os.scandir('video_dl') as it:
        for entry in it:
            if not (entry.is_file() and entry.name.startswith(id)):
                continue
            if entry.name.endswith('mp4'):
                result['video'] = entry.path
            elif entry.name.endswith(('webp', 'png')):
                png_cover = re.sub(r'(?:\.).+$', '.png', entry.path)
                process_image(source_path=entry.path, save_path=png_cover)
                result['cover'] = png_cover
    return result


async def test(title: str, characters: List[str], id: str, desc: str,
               video_path, cover_path):
    page = video_uploader.VideoUploaderPage(open(video_path, 'rb'), title=id)
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
    cred = video_uploader.VideoUploaderCredential(account='冰飞FlappyIce',
                                                  password='Icefly73bli')
    access_key = await cred.get_access_key()
    print(access_key)
    # uploader = video.VideoUploader(cover=open(cover_path, 'rb'),
    #                                cover_type='png',
    #                                pages=[page],
    #                                config=config,
    #                                credential=cred)
    # print('uploading')

    # all_chunks = []

    # async def chunk_begin_handler(e):
    #     print('start chunk: {}, total chunk: {}'.format(
    #         e['chunk_index'], e['total_chunk']))
    #     if not len(all_chunks):
    #         for i in range(1, e['total_chunk'] + 1):
    #             all_chunks.append(i)

    # async def chunk_finish_handler(e):
    #     index = all_chunks.index(e['chunk_index'])
    #     all_chunks.pop(index)
    #     print('finish chunk: {}\nremaining: {}'.format(e['chunk_index'],
    #                                                    all_chunks))

    # uploader.add_event_listener('CHUNK_BEGIN', chunk_begin_handler)
    # uploader.add_event_listener('CHUNK_END', chunk_finish_handler)
    # result = await uploader.start()
    # print(result)


def process_image(source_path: str, save_path: str):
    main = Image.open(source_path).resize((1280, 720))
    frame = Image.open('video_dl/frame.png').resize((1280, 800))
    result = Image.new('RGB', (1280, 800))
    result.paste(frame, (0, 0))
    result.paste(main, (0, 40))
    result.save(save_path, 'png')


# download()
async def main():
    cred = video_uploader.VideoUploaderCredential()
    access_key = await cred.get_access_key()
    print(access_key)
    return
    # download()
    raw = await core.api.youtube.get_videos_raw(id)
    info = raw[0]
    # title = info.snippet.title
    desc = info.snippet.description

    title = '[比赛搬运]Hitpoint Summer July - Super Dan (马力欧) Vs. Mewmon (甲贺忍蛙)'
    file = get_files(id)
    await test(title, ['马力欧', '甲贺忍蛙'], id, desc, file['video'], file['cover'])


asyncio.get_event_loop().run_until_complete(main())
# asyncio.get_event_loop().run_until_complete(test())