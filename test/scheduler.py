from datetime import date, datetime, timedelta
from typing import List
from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz
import asyncio
import time

tz_cn = pytz.timezone('Asia/Shanghai')
scheduler = AsyncIOScheduler({'apscheduler.timezone': tz_cn})


async def ring(content: str):
    print('ringing')

    # scheduler.add_job(ring,
    #                   'date',
    #                   run_date=datetime.now().astimezone(tz_cn) +
    #                   timedelta(seconds=4),
    #                   args=['added job'])
    # print(scheduler.print_jobs())


print(datetime.now().strftime('%H:%M:%S'))
scheduler.add_job(ring,
                  'date',
                  run_date=datetime.now().astimezone(tz_cn) +
                  timedelta(seconds=2),
                  args=['job1'])
scheduler.add_job(ring,
                  'date',
                  run_date=datetime.now().astimezone(tz_cn) +
                  timedelta(seconds=4),
                  args=['job2'])

scheduler.start()
jobs: List[Job] = list(scheduler.get_jobs())
jobs.sort(key=lambda job: job.next_run_time)
print(jobs[-1].next_run_time + timedelta(minutes=1))

asyncio.get_event_loop().run_until_complete(asyncio.sleep(60))