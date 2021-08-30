from __future__ import unicode_literals
import youtube_dl

" 'bestvideo[fps>50][vcodec^=avc1]+bestaudio' --merge-output-format mp4"


class MyLogger(object):
    def debug(self, msg):
        print(msg, end="\r")
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
    'format': 'bestvideo[fps>50][vcodec^=avc1]+bestaudio[acodec^=mp4a]',
    'merge_output_format': 'mp4',
    # 'listformats': True,
    'logger': MyLogger(),
    'verbose': True,
    'writeautomaticsub': True,
    'subtitleslangs': ['en'],
    'subtitlesformat': 'vtt',
    'outtmpl': 'video_dl/%(id)s-%(title)s.%(ext)s',
    'getthumbnail': True
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

url = 'https://www.youtube.com/watch?v=YD5HwVx7E38'

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    result = ydl.download([url])
    # print(ydl)

# with youtube_dl.YoutubeDL(sub_opts) as subdl:
#     subdl.download([url])

# with youtube_dl.YoutubeDL(thumb_opts) as thumbdl:
#     result = thumbdl.download([url])