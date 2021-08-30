import sys
sys.path.append('.')

from core.__video.__y2b_dl import get_files
import core

video_id = 'xlkk3Ng5Mv4'


async def main():
    raw = await core.api.youtube.get_videos_raw(video_id)
    raw_info = raw[0]
    if not raw_info.snippet:
        raise Exception('no raw info snippet')
    desc = raw_info.snippet.description
    title = raw_info.snippet.title
    info = core.video.match_parser.parse(title)
    if not info:
        raise Exception('no info')
    download_files = core.video.yt_download(video_id)
    vid_path = download_files['video']
    cover_path = download_files['cover']
    result = await core.api.bilibili.submit_video(
        info.format_title, [*info.p1_fighter, *info.p2_fighter], video_id,
        desc, vid_path, cover_path)
    print(result['bvid'])


def get_files_test():
    print(get_files('cWDWSBP0S00'))


get_files_test()
