# from typing import Any, Dict, Sequence, TYPE_CHECKING
# from bilibili_api import user
# from pymongo.collection import ReturnDocument
# from utils.db import subscribes

# async def get_videos(uid: int) -> None:
#     """get video from bilibili by uid
#     save the videos in db, return nothing.

#     Args:
#         uid (int): uid
#     """
#     video_generator: Sequence[Dict[str, Any]] = user.get_videos_g(uid)

#     for video in video_generator:
#         video_info = {
#             'title': video['title'],
#             'description': video['description'],
#             'author': video['author'],
#             'author_id': video['mid'],
#             'created': video['created']
#         }
#         found = subscribes.find_one_and_update(
#             {"_id": video['bvid']},
#             {'$set': video_info},
#             upsert=True,
#         )
#         if len(video) > 25 and found is not None:
#             break
#         elif len(video) > 85:
#             break
