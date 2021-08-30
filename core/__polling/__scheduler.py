import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler(
    {'apscheduler.timezone': pytz.timezone('Asia/Shanghai')})
