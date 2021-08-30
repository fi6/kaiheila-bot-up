from __future__ import annotations
import re
import logging
from typing import List
from urllib.parse import urlparse
from mongoengine.errors import DoesNotExist

from pyyoutube.models.video import Video, VideoListResponse
from configs import auth
from pyyoutube import Api
from models import YTVideo


class __Youtube():
    api = Api(api_key=auth.y2b_api_key)

    async def _search_video(self, q):
        return self.api.search(q=q,
                               parts=['snippet'],
                               limit=30,
                               count=30,
                               order='date')

    async def search_character_en(self, char: str):
        q = 'smash ultimate vs {} -amiibo -bgm -dojo -cpu'.format(char)
        return await self._search_video(q)

    async def search_character_jp(self, char: str):
        q = '"{}"  スマブラ vs -bgm -amiibo'.format(char)
        return await self._search_video(q)

    async def save_videos(self, *id: str) -> List[YTVideo] | None:
        videos = await self.get_videos_raw(*id)
        if not videos:
            logging.warning('no video found for {}'.format(id))
            return
        result = []
        for video in videos:
            try:
                vid_doc = YTVideo.objects.get(vid=video.id)
                vid_doc.update_from_item(video)
            except DoesNotExist:
                vid_doc = YTVideo.from_item(video)
            # vid_doc.save()
            result.append(vid_doc)
        return result

    async def get_videos_raw(self, *id: str) -> List[Video] | None:
        r = self.api.get_video_by_id(video_id=id,
                                     parts=[
                                         'snippet', 'statistics', 'status',
                                         'contentDetails', 'id', 'topicDetails'
                                     ])
        response: VideoListResponse = r
        return response.items

    def get_id(self, url: str) -> str | None:
        result = urlparse(url)
        if not result:
            return
        id = re.match(
            r'.*(?:youtu.be\/|v\/|u\/\w\/|embed\/|watch\?(?:.*)v=)([^#\&\?]*).*',
            url)
        return id.group(1) if id and r'/' not in id.group(1) else None
