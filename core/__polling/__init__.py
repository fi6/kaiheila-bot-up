import asyncio
import configs
from datetime import datetime, timedelta
from random import randint

from chinese_calendar.utils import is_workday
from utils.date import get_cn_time
from apscheduler.events import EVENT_ALL, EVENT_JOB_ERROR
from pyee import AsyncIOEventEmitter

from . import _check_live
from ._check_video import check_video
import logging
from .__scheduler import scheduler
from ._check_yt_video import check_yt_video

# def signal_handler(signal, frame):
#     global interrupted
#     interrupted = True

# signal.signal(signal.SIGINT, signal_handler)

# interrupted = False


class __Polling(AsyncIOEventEmitter):
    counter: int = 11
    start_flag: bool = True

    def __init__(self, loop=None):
        super().__init__(loop=loop)
        # self.scheduler.start(paused=True)
        # self.live_check_job = self.scheduler.add_job(self.check_living,
        #                                              'interval',
        #                                              seconds=2.7,
        #                                              jitter=0.5)
        # self.video_check_job = self.scheduler.add_job(self.check_video,
        #                                               'interval',
        #                                               seconds=180,
        #                                               jitter=20)
        # scheduler.add_listener(self.__job_listener, EVENT_ALL)

    async def start(self):
        logging.info('polling start')
        logging.getLogger('apscheduler').setLevel(logging.ERROR)
        scheduler.start()
        asyncio.create_task(self.check_live_start())
        asyncio.get_event_loop().create_task(self.check_video_start())
        asyncio.get_event_loop().create_task(self.check_yt_video_start())

    def pause(self):
        # self.start_flag = False
        scheduler.pause()
        logging.info('polling paused')

    def resume(self):
        # self.start_flag = True
        scheduler.resume()
        scheduler.add_job(self._check_live_task,
                          'date',
                          run_date=get_cn_time() + timedelta(seconds=3))
        scheduler.add_job(self.check_video_start,
                          'date',
                          run_date=get_cn_time() + timedelta(seconds=3))
        logging.info('polling resuming in 3s')

    async def check_live_start(self):
        await self._check_live_task()

    async def _check_live_task(self):
        # if not self.start_flag:
        #     return
        try:
            now = get_cn_time()
            if now.hour <= 18 and is_workday(now):
                return
            elif now.hour < 8:
                return
            logging.info('check live task start')
            live_info = await _check_live.check()
            if live_info:
                logging.info(
                    'sending live start info for {}'.format(live_info))
                self.emit('live_start', live_info)
            # schedule job for next time
            scheduler.add_job(self._check_live_task,
                              'date',
                              run_date=get_cn_time() + timedelta(seconds=90))
            # print('next check live in 5s')
        except Exception as e:
            logging.exception(e)
            self.pause()
            asyncio.get_event_loop().call_later(randint(1800, 2000),
                                                self.resume)

    async def check_video_start(self):
        for p in [1, 0, -1]:
            await self._check_video_task(priority=p)
            await asyncio.sleep(20)

    async def _check_video_task(self, priority):
        # if priority == 0:
        #     await asyncio.sleep(1)
        # elif priority == -1:
        #     await asyncio.sleep(2)
        try:
            async for video in check_video(priority):
                logging.info('new video: {user} {title}'.format(
                    user=video.author, title=video.title))
                self.emit('video_update', video)
            scheduler.add_job(self._check_video_task,
                              'date',
                              run_date=get_cn_time() +
                              timedelta(minutes=20 - 10 * priority),
                              args=[priority])
        except Exception as e:
            logging.error('error found when checking video')
            logging.exception(e)
            self.pause()
            asyncio.get_event_loop().call_later(randint(1800, 2000),
                                                self.resume)

    async def check_yt_video_start(self):
        job = scheduler.add_job(self.check_yt_video_task,
                                trigger='cron',
                                hour='14,21')
        logging.info('added youtube checker, next run at: {}'.format(
            job.next_run_time))

    async def check_yt_video_task(self):
        for server in configs.servers.all.values():
            vids_info = await check_yt_video(server.code)
            for vid_info in vids_info:
                logging.info('new youtube video: {}'.format(vid_info.title))
                self.emit('yt_video_update', vid_info, server)

    def __job_listener(self, event):
        print(event)
        if event.exception:
            logging.exception('event exception found: {exception}'.format(
                exception=event.exception))
            scheduler.pause()
            asyncio.get_event_loop().call_later(1200, scheduler.resume)


polling = __Polling()
