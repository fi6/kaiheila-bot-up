import time
import youtube_dl
import os
from PIL import Image
import re

import ffmpeg

ydl_opts = {
    'format': 'bestvideo[fps>50][vcodec^=avc1]+bestaudio',
    'merge_output_format': 'mp4',
    # 'listformats': True,
    'verbose': True,
    'writeautomaticsub': True,
    'subtitleslangs': ['en'],
    'subtitlesformat': 'vtt',
    'outtmpl': 'video_dl/%(id)s-%(title)s.%(ext)s'
    # 'getthumbnail': True,
    # 'progress_hooks': [my_hook],
}

sub_opts = {
    'verbose': True,
    'writeautomaticsub': True,
    'subtitleslangs': ['zh-Hans', 'en'],
    'subtitlesformat': 'ttml',
    'skip_download': True,
    'outtmpl': 'video_dl/%(id)s-%(title)s.%(ext)s'
    # 'progress_hooks': [my_hook],
}

thumb_opts = {
    'writethumbnail': True,
    'skip_download': True,
    'outtmpl': 'video_dl/%(id)s-%(title)s.%(ext)s'
}


def download(id: str):
    url = 'https://www.youtube.com/watch?v={}'.format(id)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.download([url])

    with youtube_dl.YoutubeDL(sub_opts) as subdl:
        result = subdl.download([url])

    with youtube_dl.YoutubeDL(thumb_opts) as thumbdl:
        result = thumbdl.download([url])

    return get_files(id)


def get_files(id):
    result = {}
    expire_time = time.time() - 7 * 24 * 60 * 60
    with os.scandir('video_dl') as it:
        for entry in it:
            if not entry.is_file():
                continue
            if entry.stat().st_ctime < expire_time and entry.stat(
            ).st_size > 2e6:
                os.remove(entry.path)
                continue
            if not entry.name.startswith(id):
                continue
            if entry.name.endswith('mp4'):
                out_file = re.sub(r'(?:/.+\.)\w+$', '/out.mp4', entry.path)
                # print(out_file)
                _process_video(entry.path, out_file)
                result['video'] = out_file
            elif entry.name.endswith(('webp', 'png', 'jpg', 'jpeg')):
                png_cover = re.sub(r'(?:\.)\w+$', '.png', entry.path)
                __process_image(source_path=entry.path, save_path=png_cover)
                result['cover'] = png_cover
    if not (result['video'] and result['cover']):
        raise ValueError('未找到视频或封面文件：{}'.format(result))
    return result


def __process_image(source_path: str, save_path: str):
    main = Image.open(source_path).resize((1280, 720))
    frame = Image.open('core/__video/frame.png').resize((1280, 800))
    result = Image.new('RGB', (1280, 800))
    result.paste(frame, (0, 0))
    result.paste(main, (0, 40))
    result.save(save_path, 'png')


def _process_video(source_path: str, save_path: str):
    main = ffmpeg.input(source_path)
    logo = ffmpeg.input('core/__video/icefly.png')
    # (ffmpeg.filter([main, logo], 'overlay', 10, 10).output(save_path).run())
    (main.output(save_path, ss=1, vcodec='copy',
                 acodec='copy').run(overwrite_output=True))
