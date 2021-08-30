from bilibili_api import user
import sys

from mongoengine.errors import DoesNotExist
sys.path.append('.')

from models import VerifiedUp
from functions import bot

# ups = VerifiedUp.objects(tag='video', priority=1)
# print(ups)

bilibili_id = 4235540
kaiheila_id = 3311772366
live = False
priority = -1  # -1, 0, 1 low->high

u = user.get_user_info(int(bilibili_id))
try:
    up = VerifiedUp.objects.get(uid=bilibili_id)
    up.update(uid=u['mid'],
              roomid=u['live_room']['roomid'],
              avatar=u['face'],
              nickname=u['name'],
              sign=u['sign'],
              priority=priority,
              tag=['video'] if not live else ['video', 'live'],
              kid=str(kaiheila_id) if kaiheila_id else None)
except DoesNotExist:
    up = VerifiedUp(uid=u['mid'],
                    roomid=u['live_room']['roomid'],
                    avatar=u['face'],
                    nickname=u['name'],
                    sign=u['sign'],
                    priority=priority,
                    tag=['video'] if not live else ['video', 'live'],
                    kid=str(kaiheila_id) if kaiheila_id else None)
up.save()
print(up.to_mongo())
