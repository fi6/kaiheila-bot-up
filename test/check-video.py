import sys
sys.path.append('.')

import json
from core.__polling import check_video
from models.__video import _Video
from mongoengine.connection import get_db

# for video in check_video():
#     print(video.to_json())

# print(len(_Video.objects().order_by('-publish').only('bvid')))
print(json.dumps(_Video.objects.order_by('-id').first().to_card()))
# for video in _Video.objects():
#     # video._cls = '_Video.VideoUpdate'
#     video.save()
#     print(video)
# db = get_db()
# collection = db.get_collection('videos')
# print(
#     collection.update_many({}, {"$set": {
#         "_cls": "_Video.VideoUpdate"
#     }}))
