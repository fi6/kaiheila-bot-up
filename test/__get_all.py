import sys

sys.path.append('.')

import asyncio
import logging

import core
from models import VerifiedUp, VideoArchive

logging_level = logging.DEBUG
logging.basicConfig(
    level=logging_level,
    format=
    '%(asctime)s.%(msecs)03d[%(levelname)s]%(module)s>%(funcName)s:%(message)s',
    datefmt='%y-%m-%d %H:%M:%S',
)

ups = list(VerifiedUp.objects(tag='porter'))
print([up.nickname for up in ups])
for up in ups:
    print(up.nickname, up.uid)

    videos = asyncio.get_event_loop().run_until_complete(
        core.api.bilibili.get_user_videos(up.uid))
    for v in videos:
        doc = core.video.add_user_video(v)
        if not doc:
            continue
        if not doc.original:
            id = core.api.youtube.get_id(doc.source)
            if id:
                asyncio.get_event_loop().run_until_complete(
                    core.api.youtube.save_videos(id))

# 奶丝dothatthang 9409346
# DioTV 4296924
# 冰枫-莫利亚 2728271
# srfhuman 793755
# 超懒Der八爷 7926167
# 大叔十四 1408305
# 樾哥soma 290997685
# 1UP游戏空间の日常 22295969
# 空巢派 7254207
# 烧焦的火龙 4731880
# 维京VKFire 37955477
# Carlos_Choi 330364988
# OC呆呆呆 2672015
# 冷场SwitchYourLife 4307615
# 杭州任天堂大乱斗 1867875
# 上海大乱斗SmashHai 692756674
# SZmash_dos 10032115
# MiriaOnoe 34785793
# 真言代理BriAu 4571634
# 莱打kiva 307889
# 寂寞小康 685092
# QC_-_ 67674065
# 控哥哥鸭 390851181
# Luminiscencia 47229249
# 光波大侠 5449804
# 蜀斗府 2094806655
# 汉尼拔_Official 465493
# 小魔王Mandom 20151162
# DoooDudo 296820
