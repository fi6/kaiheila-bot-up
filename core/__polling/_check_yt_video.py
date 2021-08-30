from typing import List
from pyyoutube.models.search_result import SearchListResponse
import core
from models import YTVideo


async def check_yt_video(code: str):
    char_en = core.video.char_dict[code][1]
    char_jp = core.video.char_dict[code][2]
    en_vids = await core.api.youtube.search_character_en(char_en)
    jp_vids = await core.api.youtube.search_character_jp(char_jp)
    en_vid_ids = map(lambda vid: vid.id.videoId, en_vids.items)
    jp_vid_ids = map(lambda vid: vid.id.videoId, jp_vids.items)
    en_vid_infos = await core.api.youtube.save_videos(*en_vid_ids)
    jp_vid_infos = await core.api.youtube.save_videos(*jp_vid_ids)
    vids_info: List[YTVideo] = []
    if en_vid_infos:
        vids_info.extend([vid for vid in en_vid_infos if not vid.post])
    if jp_vid_infos:
        vids_info.extend([vid for vid in jp_vid_infos if not vid.post])
    return vids_info
