import mongoengine as __mongo
from mongoengine.connection import get_connection
from configs import auth
import logging

from .__video import _Video, VideoArchive, VideoUpdate, VideoTypes, VideoRecord  # noqa
from .__up import Up, VerifiedUp  # noqa
from .__group import Group  # noqa
from .__event import _Event, OnlineEvent, OfflineEvent  # noqa
from .__yt_video import YTVideo, MatchInfoDoc  # noqa

__mongo.connect(db='ttd', authentication_source='admin', host=auth.mongo_url)
if __mongo.connection.get_connection().connected:
    logging.info('db connected, models init success')
