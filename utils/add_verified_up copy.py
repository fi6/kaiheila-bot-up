from bilibili_api import user, live
import sys
sys.path.append('.')

from models import VerifiedUp

# ups = VerifiedUp.objects(tag='video', priority=1)
# print(ups)

up = VerifiedUp.objects.get(uid=793755)
up.kid = '1465834196'
up.save()
