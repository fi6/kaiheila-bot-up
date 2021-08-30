from datetime import datetime
import logging
import re
from mongoengine.errors import DoesNotExist
from models import _Video, VideoRecord, VerifiedUp


def add_user_video(data: dict, smash_only=True):
    try:
        video: _Video = _Video.objects.get(bvid=data['bvid'])
    except DoesNotExist:
        video = VideoRecord()
        video._raw = data
        video.bvid = data['bvid']
        video.uid = data['mid']
        video.up_ref = VerifiedUp.objects.get(uid=video.uid)
    if isinstance(video, VideoRecord):
        video.publish = datetime.fromtimestamp(data['created'])
    video.title = data['title']
    video.pic = data['pic']
    video.desc = data['description']
    video.author = data['author']
    logging.debug((video, video.title))
    print((video, video.title))

    if data['copyright'] == 1:
        video.original = True
    else:
        video.original = False
        source = re.search(r'^http.+?(?:$|\n)', video.desc)
        if not source:
            source = re.search(r'^.+?(?:$|\n)', video.desc)
        video.source = source.group(0).strip() if source else ''

    video.save()
    return video


# {
#     'comment': 10,
#     'typeid': 17,
#     'play': 1764,
#     'pic':
#     'http://i1.hdslb.com/bfs/archive/9706620e4ce2fc83f3b920a3ab3bccaac851c969.jpg',
#     'subtitle': '',
#     'description':
#     'https://www.youtube.com/watch?v=AmHOz-KQYY4&t=717s\n转载：https://www.youtube.com/watch?v=AmHOz-KQYY4&t=717s\n原作者：BananaBoySSB\n原标题：How to Fight Every Character 2.0 (Part 2) - Smash Ultimate\n个人汉化，有错误的地方还请多多指正.\n本视频版本环境为ver10.0.0',
#     'copyright': '2',
#     'title': '【熟肉/大乱斗SP】全角色对策2.0（Part 2）',
#     'review': 0,
#     'author': '冰枫-莫利亚',
#     'mid': 2728271,
#     'created': 1617161556,
#     'length': '45:36',
#     'video_review': 5,
#     'aid': 544768066,
#     'bvid': 'BV14i4y1P7Ty',
#     'hide_click': False,
#     'is_pay': 0,
#     'is_union_video': 0,
#     'is_steins_gate': 0,
#     'is_live_playback': 0
# }
