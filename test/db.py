import asyncio
import json
import sys
sys.path.append('.')
import re
from typing import List
from urllib.parse import parse_qs, urlparse
from core.types import LiveInfo
import core
from models import VerifiedUp, _Video


async def main():
    vid = (await core.api.bilibili.get_video_info('BV1mt41167EA'))
    print(vid)


asyncio.get_event_loop().run_until_complete(main())
exit()
for video in _Video.objects():
    if not video.original:
        result = urlparse(video.source)
        print(video.source)
        if result:
            id = re.match(
                r'.*(?:youtu.be\/|v\/|u\/\w\/|embed\/|watch\?(?:.*)v=)([^#\&\?]*).*',
                video.source)
            print(id.group(1) if id and r'/' not in id.group(1) else None)
    # if video._raw['copyright'] == 1:
    #     video.original = True
    # else:
    #     video.original = False
    #     source = re.search(r'^http.+?(?:$|\n)', video.desc)
    #     if not source:
    #         source = re.search(r'^.+?(?:$|\n)', video.desc)
    #     video.source = source.group(0).strip() if source else ''
    # if not video.original:
    #     print(video._raw)
    #     print(video.source)
    #     print(video.original)
    # video.save()
