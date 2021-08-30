from __future__ import annotations
from typing import Any, Dict, List, Sequence
from utils import link_parser
from bilibili_api import video as video_api
from models import VideoArchive, VerifiedUp
from datetime import datetime

# def add_video_archive(char: List[str], category: List[str], url: str):
#     bvid = link_parser(url)
#     video_info: Dict[str, Any] | None = video_api.get_video_info(bvid=bvid)
#     video_tags: Sequence[str] = video_api.get_tags(bvid=bvid)
#     tag_names: List[str] = [t['tag_name'] for t in video_tags]

#     fields = VideoArchive._fields.keys()
#     vid_doc = VideoArchive(
#         **{k: v
#            for k, v in video_info.items() if k in fields})
#     vid_doc._raw = video_info
#     vid_doc.publish = datetime.fromtimestamp(video_info['pubdate'])
#     vid_doc.uid = video_info['owner']['mid']
#     vid_doc.tags = tag_names
#     vid_doc.author = video_info['owner']['name']
#     up = VerifiedUp.objects(uid=vid_doc.uid)
#     if len(up):
#         vid_doc.up_ref = up[0]
#     vid_doc.save()
#     return vid_doc
