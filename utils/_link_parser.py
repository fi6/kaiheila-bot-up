from __future__ import annotations
from typing import Any, Union
import requests
from urllib.parse import ParseResult, urlparse
import re
import asyncio
from bilibili_api import video
from datetime import datetime


def link_parser(text: str, scheme_only=False) -> Union[str, None]:
    """Parse bvid from link

    Args:
        url (str): url of the video

    Returns:
        Union[str, None]: bvid, if parse failed then return None
    """
    match = re.search("(?P<url>https?://[^\s]+)", text)
    if match is None:
        return
    url = match.group("url")
    if urlparse(url).scheme:
        if scheme_only:
            return url
        res = requests.get(url).request.url
        if not res:
            return None
        parse_result: ParseResult = urlparse(res)
        bvid: re.Match[Any] | None = re.search(r'BV.+$', parse_result.path)
        return bvid[0] if bvid else None


# video_info = video.get_video_info(
#     bvid=asyncio.run(link_parser('https://b23.tv/sx7ONL')))

# arc = {
#     'bvid': video_info['bvid'],
#     'owner': video_info['owner']['name'],
#     'title': video_info['title'],
#     'pubdate': datetime.fromtimestamp(video_info['pubdate'])
# }

# print(arc)
# 'https://b23.tv/sx7ONL'
# 'https://www.bilibili.com/video/BV1Cy4y1H7jm'
